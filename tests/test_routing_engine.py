"""SPEC-R1 R1-4 (Issue #16): routing-engine requests, adoption checks and the shared route interface.

Everything here is synthetic:
- Positions are invented points a few kilometres from 0 deg N, 0 deg E (open ocean), built with
  `at(x, y)` (metres east and north). They are not places anyone rides.
- Engine replies are hand-built JSON in the shape of Valhalla replies; shapes are encoded here
  from the synthetic points. Road names, versions and dates are invented.
- Codes and request places come from tests/routing_synthetic.py.

No test sends a network request: the transport is a double (`FakeEngine`), and an autouse
fixture makes every socket call fail. Snapshot stores live in pytest's tmp_path.
"""
from __future__ import annotations

import ast
import copy
import errno
import json
import math
import os
import re
import socket
import subprocess
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import moto_copilot.routing as routing
from moto_copilot.contracts.schemas import ROUTE_ID_PATTERN, SNAPSHOT_ID_PATTERN
from moto_copilot.ingest.segments import EARTH_RADIUS_M, haversine_m
from moto_copilot.routing import adoption, http_transport, source, store as store_module, valhalla
from moto_copilot.routing import (
    ENGINE_NAME,
    ENGINE_VERSION_UNREPORTED,
    FREEWAY_CHECK_METHOD,
    HIGHWAY_IN_ROUTE,
    ROUTING_UNAVAILABLE,
    SNAPSHOT_MISSING,
    TARGET_GPX_INVALID,
    TARGET_GPX_NOT_ROUND_TRIP,
    USER_AGENT,
    VALHALLA_ENDPOINT,
    AdoptedRoute,
    EngineRouteRequest,
    HttpResponse,
    Position,
    RouteFailure,
    SnapshotConflictError,
    SnapshotIntegrityError,
    SnapshotStore,
    SnapshotStoreError,
    StrictModeStop,
    TargetGpxRequest,
    TransportError,
    TripTypeRequiredError,
    ValhallaClient,
    decode_polyline6,
    evaluate_direction,
    get_route,
    request_key,
    routing_params,
    target_gpx_route_from_bytes,
)
from moto_copilot.routing.snapshot import TAIPEI

import routing_synthetic as syn

NOW = datetime(2026, 11, 18, 12, 0, 0, tzinfo=TAIPEI)
NEW_MODULES = (valhalla, adoption, source, http_transport)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """E-4: any socket use in this module fails the test."""
    def refuse(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)


# --- synthetic geometry --------------------------------------------------------------------------

def at(x_m: float, y_m: float) -> tuple[float, float]:
    """A synthetic position x metres east and y metres north of 0 deg N, 0 deg E."""
    return (math.degrees(y_m / EARTH_RADIUS_M), math.degrees(x_m / EARTH_RADIUS_M))


def line(x0, y0, x1, y1, step=100.0):
    n = max(1, math.ceil(math.hypot(x1 - x0, y1 - y0) / step))
    return [at(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]


def encode6(points) -> str:
    """An independent Valhalla polyline6 encoder (the product only decodes)."""
    out, plat, plon = [], 0, 0
    for lat, lon in points:
        ilat, ilon = round(lat * 1e6), round(lon * 1e6)
        for delta in (ilat - plat, ilon - plon):
            value = ~(delta << 1) if delta < 0 else delta << 1
            while value >= 0x20:
                out.append(chr((0x20 | (value & 0x1F)) + 63))
                value >>= 5
            out.append(chr(value + 63))
        plat, plon = ilat, ilon
    return "".join(out)


def length_m(points) -> float:
    return sum(haversine_m(*a, *b) for a, b in zip(points, points[1:]))


def pos(ref_id, role, x, y):
    lat, lon = at(x, y)
    return {"ref_id": ref_id, "role": role, "lat": lat, "lon": lon}


OUT_POINTS = line(0, 0, 3000, 0)            # outbound: east along y = 0
BACK_POINTS = line(3000, 30, 0, 30)         # return: west along y = 30 (a different road)
OUT_POSITIONS = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1500, 0), pos("SYN-DEST", "destination", 3000, 0)]
BACK_POSITIONS = [pos("SYN-DEST", "destination", 3000, 0), pos("SYN-VIA-A", "via", 1500, 0), pos("SYN-ORIGIN", "origin", 0, 0)]


# --- engine replies ------------------------------------------------------------------------------

def reply(body, status=200) -> HttpResponse:
    data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
    return HttpResponse(status, data)


def route_body(points, *, has_highway=False, warnings=None, names=("Synthetic Road 1", "Synthetic Road 2"),
               maneuvers=None, time_s=612.4, length_km=None, trip_warnings=None, drop_has_highway=False):
    shape = encode6(points)
    km = length_m(decode_polyline6(shape)) / 1000 if length_km is None else length_km
    if maneuvers is None:
        maneuvers = [
            {"type": 1, "begin_street_names": [names[0]], "street_names": [names[0]], "length": km / 2,
             "time": time_s / 2, "begin_shape_index": 0, "end_shape_index": len(points) // 2},
            {"type": 10, "street_names": [names[1], names[0]], "length": km / 2, "time": time_s / 2,
             "begin_shape_index": len(points) // 2, "end_shape_index": len(points) - 1},
            {"type": 4, "length": 0.0, "time": 0.0, "begin_shape_index": len(points) - 1,
             "end_shape_index": len(points) - 1},
        ]
    summary = {"length": km, "time": time_s, "has_highway": has_highway, "has_toll": False, "has_ferry": False}
    if drop_has_highway:
        del summary["has_highway"]
    trip = {"legs": [{"maneuvers": maneuvers, "summary": dict(summary), "shape": shape}],
            "summary": summary, "status": 0, "units": "kilometers"}
    if trip_warnings is not None:
        trip["warnings"] = trip_warnings
    body = {"trip": trip}
    if warnings is not None:
        body["warnings"] = warnings
    return body


def trace_body(points, *, scale=1.0, road_class="primary", names=("Synthetic Road 1",), extra_edges=()):
    km = length_m(decode_polyline6(encode6(points))) / 1000 * scale
    edges = [{"names": list(names), "length": km / 2, "road_class": road_class},
             {"names": ["Synthetic Road 2"], "length": km / 2, "road_class": "secondary"}]
    return {"edges": edges + list(extra_edges), "units": "kilometers"}


STATUS = {"version": "0.0.0-synthetic", "tileset_last_modified": 1762300800, "available_actions": ["route"]}


@dataclass
class Call:
    action: str
    url: str
    body: dict
    headers: dict
    raw: bytes


class FakeEngine:
    """Transport double: answers each action from its own queue and records every call."""

    def __init__(self, routes=(), traces=(), statuses=None):
        self.queue = {"route": list(routes), "trace_attributes": list(traces),
                      "status": list(statuses) if statuses is not None else [reply(STATUS)]}
        self.calls: list[Call] = []

    def __call__(self, url, body, headers):
        assert url.startswith(VALHALLA_ENDPOINT + "/")
        action = url[len(VALHALLA_ENDPOINT) + 1:]
        self.calls.append(Call(action, url, json.loads(body.decode("utf-8")), dict(headers), body))
        if not self.queue[action]:
            raise AssertionError(f"unexpected {action} request")
        answer = self.queue[action].pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def actions(self):
        return [c.action for c in self.calls]


def refusing_transport(url, body, headers):
    raise AssertionError("the routing engine must not be called")


class Clock:
    """Successive receipt times, one second apart, starting at `start`."""

    def __init__(self, start=NOW):
        self.next = start

    def __call__(self):
        value = self.next
        self.next = value + timedelta(seconds=1)
        return value


def round_trip_engine(out=None, back=None, out_trace=None, back_trace=None, statuses=None):
    return FakeEngine(
        routes=[reply(out if out is not None else route_body(OUT_POINTS)),
                reply(back if back is not None else route_body(BACK_POINTS))],
        traces=[reply(out_trace if out_trace is not None else trace_body(OUT_POINTS)),
                reply(back_trace if back_trace is not None else trace_body(BACK_POINTS))],
        statuses=statuses,
    )


def one_way_engine(points=OUT_POINTS, route=None, trace=None):
    return FakeEngine(routes=[reply(route if route is not None else route_body(points))],
                      traces=[reply(trace if trace is not None else trace_body(points))])


def engine_request(trip_type="round_trip", positions=None, via=(syn.VIA_A,)):
    if positions is None:
        positions = {"outbound": OUT_POSITIONS, "return": BACK_POSITIONS} if trip_type == "round_trip" else {"outbound": OUT_POSITIONS}
    return EngineRouteRequest(trip_type=trip_type, origin=syn.ORIGIN, destination=syn.DEST, via=list(via),
                              definitions=syn.DEFINITIONS, positions=positions)


def the_key(trip_type="round_trip", via=(syn.VIA_A,)):
    return request_key(trip_type=trip_type, origin=syn.ORIGIN, destination=syn.DEST, via=list(via),
                       routing_params=routing_params(), definitions=syn.DEFINITIONS)


def plan(engine, store, request=None, *, now=NOW, clock=None, **kwargs):
    client = ValhallaClient(engine, clock=clock or Clock(now - timedelta(minutes=5)))
    return get_route(request or engine_request(), store=store, client=client, now=now, **kwargs)


@pytest.fixture
def store(tmp_path) -> SnapshotStore:
    return SnapshotStore(tmp_path)


def stored_files(directory: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(directory.iterdir())}


def assert_no_route(result):
    """S15 / S38: a route error has no route, no distance and no road names."""
    assert isinstance(result, RouteFailure)
    assert not hasattr(result, "legs") and not hasattr(result, "distance_m") and not hasattr(result, "road_names")


# --- (a) the client: requests, endpoint, identification (CL-R1-5, CL-R1-9; H-1, H-2) ---------------

def test_s30_route_request_is_motorcycle_with_use_highways_0_and_no_exclusion_or_elevation(store):
    engine = round_trip_engine()
    assert isinstance(plan(engine, store), AdoptedRoute)
    routes = [c for c in engine.calls if c.action == "route"]
    assert len(routes) == 2
    for call in routes:
        body = call.body
        assert body["costing"] == "motorcycle"
        assert body["costing_options"] == {"motorcycle": {"use_highways": 0}}
        raw = call.raw.decode("utf-8")
        assert "exclude" not in raw and "elevation" not in raw and "height" not in raw
        assert set(body) == {"locations", "costing", "costing_options", "units"}
        assert [loc["type"] for loc in body["locations"]] == ["break", "via", "break"]
        assert all(set(loc) == {"lat", "lon", "type"} for loc in body["locations"])


def test_cl_r1_5_each_direction_gets_its_own_positions_one_route_and_one_trace_request(store):
    engine = round_trip_engine()
    plan(engine, store)
    assert engine.actions() == ["route", "trace_attributes", "route", "trace_attributes", "status"]
    out_call, back_call = [c for c in engine.calls if c.action == "route"]
    assert [(l["lat"], l["lon"]) for l in out_call.body["locations"]] == [(p["lat"], p["lon"]) for p in OUT_POSITIONS]
    assert [(l["lat"], l["lon"]) for l in back_call.body["locations"]] == [(p["lat"], p["lon"]) for p in BACK_POSITIONS]


def test_the_road_attribute_query_sends_only_the_engines_own_shape(store):
    engine = round_trip_engine()
    plan(engine, store)
    traces = [c for c in engine.calls if c.action == "trace_attributes"]
    assert [c.body["encoded_polyline"] for c in traces] == [encode6(OUT_POINTS), encode6(BACK_POINTS)]
    for call in traces:
        assert set(call.body) == {"encoded_polyline", "costing", "shape_match", "filters"}
        assert "locations" not in call.body and "shape" not in call.body
        assert call.body["filters"] == {"attributes": ["edge.names", "edge.length", "edge.road_class"], "action": "include"}


def test_user_agent_and_request_content_hold_no_personal_information(store):
    engine = round_trip_engine()
    plan(engine, store)
    assert USER_AGENT == "route-client/1.0"
    lowered = USER_AGENT.lower()
    for token in ("@", "moto", "copilot", "touring", "nchu", "aiot", "course", "project", "http"):
        assert token not in lowered
    for call in engine.calls:
        assert call.headers == {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        raw = call.raw.decode("utf-8")
        for text in ("SYN-", "origin", "destination", "Synthetic", "ref_id", "role", '"name"'):
            assert text not in raw  # codes, roles and place names stay in the program
        if call.action == "route":
            assert "@" not in raw


def test_the_endpoint_is_the_constant_and_every_request_goes_to_it(store):
    assert VALHALLA_ENDPOINT == "https://valhalla1.openstreetmap.de"
    engine = round_trip_engine()
    plan(engine, store)
    assert [c.url for c in engine.calls] == [
        f"{VALHALLA_ENDPOINT}/route", f"{VALHALLA_ENDPOINT}/trace_attributes",
        f"{VALHALLA_ENDPOINT}/route", f"{VALHALLA_ENDPOINT}/trace_attributes", f"{VALHALLA_ENDPOINT}/status"]


def test_h1_the_endpoint_is_not_affected_by_env_variables(tmp_path):
    """Run in a fresh interpreter with env variables that name another host and proxies."""
    code = (
        "import json\n"
        "from moto_copilot.routing import ValhallaClient, VALHALLA_ENDPOINT, HttpResponse\n"
        "seen = []\n"
        "def transport(url, body, headers):\n"
        "    seen.append(url)\n"
        "    return HttpResponse(503, b'{}')\n"
        "client = ValhallaClient(transport)\n"
        "client.status()\n"
        "print(json.dumps({'constant': VALHALLA_ENDPOINT, 'client': client.endpoint, 'seen': seen}))\n"
    )
    marker = "https://redirected.invalid"
    env = {key: value for key, value in os.environ.items()}
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    for name in ("VALHALLA_URL", "VALHALLA_ENDPOINT", "VALHALLA_HOST", "ROUTING_ENDPOINT", "ROUTING_URL",
                 "MOTO_COPILOT_VALHALLA", "HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "https_proxy", "http_proxy"):
        env[name] = marker
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8",
                          env=env, timeout=60, cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    report = json.loads(done.stdout)
    assert report == {"constant": VALHALLA_ENDPOINT, "client": VALHALLA_ENDPOINT,
                      "seen": [f"{VALHALLA_ENDPOINT}/status"]}


@pytest.mark.parametrize("bad", [
    "http://valhalla1.openstreetmap.de", "https://valhalla1.openstreetmap.de/", "https://host/route",
    "https://host?x=1", "https://user@host", "https://", "valhalla1.openstreetmap.de", "https://host\n", "",
    None, 42,
])
def test_an_explicit_endpoint_must_be_a_bare_https_host(bad):
    with pytest.raises(ValueError):
        ValhallaClient(refusing_transport, endpoint=bad)


def test_an_explicitly_passed_endpoint_is_used():
    seen = []

    def transport(url, body, headers):
        seen.append(url)
        return reply(STATUS)

    ValhallaClient(transport, endpoint="https://engine.example:8002").status()
    assert seen == ["https://engine.example:8002/status"]


def test_the_new_modules_do_not_read_env_log_print_or_import_network_modules():
    """Only http_transport may import http and ssl (CL-R1-25); nothing else is relaxed for it."""
    for module in NEW_MODULES:
        banned = {"logging", "socket", "http", "urllib", "requests", "httpx", "ssl", "subprocess"}
        if module is http_transport:
            banned -= {"http", "ssl"}
        text = Path(module.__file__).read_text(encoding="utf-8")
        assert "environ" not in text and "getenv" not in text
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Import):
                names = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                names = {(node.module or "").split(".")[0]}
            else:
                names = set()
            assert not names & banned, module.__name__
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "print"


def test_no_request_is_retried_after_an_error_reply(store):
    engine = FakeEngine(routes=[reply({"error": "synthetic"}, status=500), reply({"error": "synthetic"}, status=500)])
    result = plan(engine, store)
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:engine_error", "return:engine_error"))
    assert engine.actions() == ["route", "route"]


# --- polyline decoding ---------------------------------------------------------------------------

def test_decode_polyline6_round_trips_an_independent_encoder():
    points = [at(0, 0), at(-1234.5, 678.9), at(2_000_000, -3_000_000), (-89.999999, 179.999999), (12.5, -0.000001)]
    decoded = decode_polyline6(encode6(points))
    assert len(decoded) == len(points)
    for (a, b), (c, d) in zip(decoded, points):
        assert abs(a - c) <= 5e-7 and abs(b - d) <= 5e-7


@pytest.mark.parametrize("bad", ["", "_", "~~~~", "a b", "éé", None])
def test_decode_polyline6_rejects_bad_shapes(bad):
    with pytest.raises(valhalla.PolylineError):
        decode_polyline6(bad)


# --- (b)(c)(d)(e) adoption, storage and order ----------------------------------------------------

def test_a_round_trip_is_adopted_and_stored_once(store, tmp_path):
    engine = round_trip_engine()
    result = plan(engine, store)
    assert isinstance(result, AdoptedRoute)
    files = stored_files(tmp_path)
    assert list(files) == [f"{result.snapshot_id}.json"]
    snapshot = store.load(result.snapshot_id)
    assert snapshot["request_key"] == the_key()
    assert snapshot["routing_params"] == routing_params()
    assert snapshot["engine_name"] == ENGINE_NAME == "Valhalla"
    assert snapshot["engine_version"] == "0.0.0-synthetic"
    assert snapshot["map_data_date"] == datetime.fromtimestamp(1762300800, TAIPEI).date().isoformat()
    assert [leg["direction"] for leg in snapshot["legs"]] == ["outbound", "return"]
    for leg in snapshot["legs"]:
        assert leg["has_highway"] is False and leg["freeway_check"] == "pass" and leg["warnings"] == []
        assert leg["freeway_check_method"] == FREEWAY_CHECK_METHOD
    assert result.route_source == "routing" and result.trip_type == "round_trip"
    assert result.target_gpx_ref is None and result.turnaround_m is None and result.turnaround_source is None


def test_s23_each_direction_has_its_own_request_shape_and_fetched_at_and_return_is_not_reversed(store):
    engine = round_trip_engine()
    clock = Clock(datetime(2026, 11, 18, 9, 0, 0, tzinfo=TAIPEI))
    result = plan(engine, store, clock=clock)
    out, back = store.load(result.snapshot_id)["legs"]
    assert out["shape"] == encode6(OUT_POINTS) and back["shape"] == encode6(BACK_POINTS)
    assert back["shape"] != encode6(list(reversed(OUT_POINTS)))
    assert [l["ref_id"] for l in out["request"]["locations"]] == ["SYN-ORIGIN", "SYN-VIA-A", "SYN-DEST"]
    assert [l["ref_id"] for l in back["request"]["locations"]] == ["SYN-DEST", "SYN-VIA-A", "SYN-ORIGIN"]
    assert out["request"] != back["request"]
    assert out["fetched_at"] != back["fetched_at"]
    # The route's geometry is each direction's own decoded shape, in order (never a reversal).
    out_leg, back_leg = result.legs
    assert [(p.lat, p.lon) for p in out_leg.points] == decode_polyline6(encode6(OUT_POINTS))
    assert [(p.lat, p.lon) for p in back_leg.points] == decode_polyline6(encode6(BACK_POINTS))
    assert [(p.lat, p.lon) for p in back_leg.points] != list(reversed([(p.lat, p.lon) for p in out_leg.points]))


def test_a_one_way_route_has_one_outbound_leg(store):
    engine = one_way_engine()
    result = plan(engine, store, engine_request("one_way"))
    assert isinstance(result, AdoptedRoute) and result.trip_type == "one_way"
    assert [leg.direction for leg in result.legs] == ["outbound"]
    assert engine.actions() == ["route", "trace_attributes", "status"]
    assert store.load(result.snapshot_id)["request_key"] == the_key("one_way")


def test_cl_r1_6_road_names_follow_the_maneuvers_in_order_without_repeats(store):
    maneuvers = [
        {"begin_street_names": ["Synthetic B"], "street_names": ["Synthetic A", "Synthetic B"]},
        {"street_names": ["Synthetic C"]},
        {"begin_street_names": ["Synthetic A"], "street_names": ["Synthetic D", "Synthetic C"]},
        {"street_names": []},
        {},
    ]
    engine = one_way_engine(route=route_body(OUT_POINTS, maneuvers=maneuvers))
    result = plan(engine, store, engine_request("one_way"))
    assert result.legs[0].road_names == ("Synthetic B", "Synthetic A", "Synthetic C", "Synthetic D")
    assert store.load(result.snapshot_id)["legs"][0]["road_names"] == ["Synthetic B", "Synthetic A", "Synthetic C", "Synthetic D"]


def test_distance_and_time_are_integers_from_the_reported_values(store):
    engine = one_way_engine(route=route_body(OUT_POINTS, length_km=3.0005, time_s=612.5),
                            trace=trace_body(OUT_POINTS))
    result = plan(engine, store, engine_request("one_way"))
    leg = store.load(result.snapshot_id)["legs"][0]
    assert leg["distance_m"] == 3001 and leg["engine_time_s"] == 613  # half up
    assert result.legs[0].distance_m == 3001


def test_s35_the_same_request_a_second_time_does_not_call_the_engine(store, tmp_path):
    first = plan(round_trip_engine(), store)
    again = plan(FakeEngine(), store, now=NOW + timedelta(days=1))  # FakeEngine() has no route replies
    assert again == first
    assert len(stored_files(tmp_path)) == 1


def test_s35_after_31_days_the_route_is_fetched_again_and_the_same_content_keeps_the_old_file(store, tmp_path):
    old = NOW - timedelta(days=31)
    first = plan(round_trip_engine(), store, now=old, clock=Clock(old))
    before = stored_files(tmp_path)
    engine = round_trip_engine()
    again = plan(engine, store, now=NOW, clock=Clock(NOW))
    assert engine.actions()[0] == "route"           # fetched again
    assert again == first                           # same content: the same snapshot
    assert stored_files(tmp_path) == before         # no new file; the old file is unchanged
    # The reused file keeps its own fetched_at (7.11 item 3).
    assert store.load(first.snapshot_id)["legs"][0]["fetched_at"] == old.isoformat()


def test_s35_after_31_days_a_different_reply_is_a_new_snapshot_and_the_old_one_stays(store, tmp_path):
    old = NOW - timedelta(days=31)
    first = plan(round_trip_engine(), store, now=old, clock=Clock(old))
    before = stored_files(tmp_path)
    changed = round_trip_engine(out=route_body(OUT_POINTS, names=("Synthetic Road 9", "Synthetic Road 2")))
    again = plan(changed, store, now=NOW, clock=Clock(NOW))
    assert again.snapshot_id != first.snapshot_id and again.route_id != first.route_id
    after = stored_files(tmp_path)
    assert len(after) == 2 and all(after[name] == data for name, data in before.items())


def test_s35_s15_engine_failure_with_only_an_expired_snapshot_is_routing_unavailable(store, tmp_path):
    old = NOW - timedelta(days=31)
    plan(round_trip_engine(), store, now=old, clock=Clock(old))
    before = stored_files(tmp_path)
    for engine in (FakeEngine(routes=[TransportError("synthetic")]),
                   FakeEngine(routes=[reply({"error": "x"}, 503), reply({"error": "x"}, 503)])):
        result = plan(engine, store, now=NOW)
        assert result.code == ROUTING_UNAVAILABLE
        assert_no_route(result)
    assert stored_files(tmp_path) == before


def test_s15_a_snapshot_checked_with_another_method_is_not_used_when_the_engine_fails(store):
    other = syn.snapshot("round_trip", rkey=the_key(), method=syn.OTHER_METHOD,
                         fetched_at=(NOW - timedelta(days=1)).isoformat())
    store.put(other)
    result = plan(FakeEngine(routes=[TransportError("synthetic")]), store)
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:engine_unreachable", "return:not_sent"))


def test_an_unreachable_engine_stops_further_requests(store, tmp_path):
    engine = FakeEngine(routes=[TransportError("synthetic")])
    result = plan(engine, store)
    assert engine.actions() == ["route"]
    assert result.code == ROUTING_UNAVAILABLE
    assert stored_files(tmp_path) == {}


def test_an_unreachable_engine_during_the_outbound_trace_does_not_send_the_return(store, tmp_path):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS))], traces=[TransportError("synthetic")])
    result = plan(engine, store)
    assert engine.actions() == ["route", "trace_attributes"]
    assert result.code == ROUTING_UNAVAILABLE
    assert "return:not_sent" in result.reasons
    assert stored_files(tmp_path) == {}


@pytest.mark.parametrize("failing", ["outbound", "return"])
def test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route(store, tmp_path, failing):
    bad = reply({"error_code": 442, "error": "synthetic no path"}, status=400)
    if failing == "outbound":
        engine = FakeEngine(routes=[bad, reply(route_body(BACK_POINTS))], traces=[reply(trace_body(BACK_POINTS))])
    else:
        engine = FakeEngine(routes=[reply(route_body(OUT_POINTS)), bad], traces=[reply(trace_body(OUT_POINTS))])
    result = plan(engine, store)
    assert result.code == ROUTING_UNAVAILABLE
    assert f"{failing}:engine_error" in result.reasons
    assert_no_route(result)
    assert stored_files(tmp_path) == {}
    assert "status" not in engine.actions()
    # Both directions were sent and checked (CL-R1-8).
    assert engine.actions().count("route") == 2


@pytest.mark.parametrize("body", [b"not json", b"{\"trip\": 3}", b"[]", b"{\"x\": NaN}"])
def test_a_reply_without_a_trip_is_an_engine_error(store, tmp_path, body):
    engine = FakeEngine(routes=[HttpResponse(200, body)])
    result = plan(engine, store, engine_request("one_way"))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:engine_error",))
    assert stored_files(tmp_path) == {}


def _malformed(kind):
    body = route_body(OUT_POINTS)
    trip = body["trip"]
    if kind == "two_legs":
        trip["legs"].append(copy.deepcopy(trip["legs"][0]))
    elif kind == "bad_shape":
        trip["legs"][0]["shape"] = "~~~~"
    elif kind == "one_point_shape":
        trip["legs"][0]["shape"] = encode6(OUT_POINTS[:1])
    elif kind == "no_maneuvers":
        trip["legs"][0]["maneuvers"] = []
    elif kind == "name_not_a_string":
        trip["legs"][0]["maneuvers"][0]["street_names"] = [7]
    elif kind == "no_length":
        del trip["summary"]["length"]
    elif kind == "negative_time":
        trip["summary"]["time"] = -1.0
    elif kind == "no_summary":
        del trip["summary"]
    return body


@pytest.mark.parametrize("kind", ["two_legs", "bad_shape", "one_point_shape", "no_maneuvers", "name_not_a_string",
                                  "no_length", "negative_time", "no_summary"])
def test_a_route_reply_that_cannot_be_read_is_routing_unavailable_with_no_freeway_check(store, tmp_path, kind):
    body = _malformed(kind)
    outcome, _ = outcome_of(route=body)
    assert "response_malformed" in outcome.reasons and outcome.leg is None and outcome.freeway_check is None
    traces = [reply(trace_body(OUT_POINTS))] if kind in ("no_maneuvers", "name_not_a_string", "no_length", "negative_time", "no_summary") else []
    engine = FakeEngine(routes=[reply(body)], traces=traces)
    result = plan(engine, store, engine_request("one_way"))
    assert result.code == ROUTING_UNAVAILABLE
    assert stored_files(tmp_path) == {}


# --- warnings (7.11 item 7; S30) -----------------------------------------------------------------

@pytest.mark.parametrize("kind", ["top", "trip", "malformed", "not_a_list", "empty_object"])
def test_s30_a_reply_with_any_warning_is_routing_unavailable(store, tmp_path, kind):
    warning = [{"code": 999, "text": "synthetic warning"}]
    body = {
        "top": route_body(OUT_POINTS, warnings=warning),
        "trip": route_body(OUT_POINTS, trip_warnings=warning),
        "malformed": route_body(OUT_POINTS, warnings=["synthetic"]),
        "not_a_list": route_body(OUT_POINTS, warnings={"code": 1}),
        "empty_object": route_body(OUT_POINTS, warnings={}),
    }[kind]
    result = plan(one_way_engine(route=body), store, engine_request("one_way"))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:warnings",))
    assert stored_files(tmp_path) == {}


def test_an_empty_warning_list_is_no_warning(store):
    result = plan(one_way_engine(route=route_body(OUT_POINTS, warnings=[], trip_warnings=[])), store, engine_request("one_way"))
    assert isinstance(result, AdoptedRoute)


# --- freeway check (7.11 item 5; S24, S39) -------------------------------------------------------

def outcome_of(route=None, trace=None, positions=OUT_POSITIONS, points=OUT_POINTS):
    engine = one_way_engine(points=points, route=route, trace=trace)
    client = ValhallaClient(engine, clock=Clock())
    return evaluate_direction(client, "outbound", [valhalla.position_from(p) for p in positions]), engine


def test_s39_has_highway_true_with_no_freeway_in_the_road_attributes_is_fail():
    outcome, _ = outcome_of(route=route_body(OUT_POINTS, has_highway=True))
    assert outcome.freeway_check == "fail" and outcome.signals == ("has_highway",) and outcome.leg is None


@pytest.mark.parametrize("trip_flag, leg_flag", [(True, False), (True, "absent"), (False, True)])
def test_s39_has_highway_true_in_the_trip_or_the_leg_summary_is_fail(trip_flag, leg_flag):
    body = route_body(OUT_POINTS)
    body["trip"]["summary"]["has_highway"] = trip_flag
    leg_summary = body["trip"]["legs"][0]["summary"]
    if leg_flag == "absent":
        del leg_summary["has_highway"]
    else:
        leg_summary["has_highway"] = leg_flag
    outcome, _ = outcome_of(route=body)
    assert outcome.freeway_check == "fail" and outcome.signals == ("has_highway",) and outcome.leg is None


@pytest.mark.parametrize("trace, signal", [
    (trace_body(OUT_POINTS, road_class="motorway"), "motorway_edge"),
    (trace_body(OUT_POINTS, extra_edges=[{"names": [], "length": 0.0, "road_class": "motorway"}]), "motorway_edge"),
    (trace_body(OUT_POINTS, names=("國道3號",)), "freeway_name"),
    (trace_body(OUT_POINTS, names=("Synthetic 高速公路",)), "freeway_name"),
    (trace_body(OUT_POINTS, names=("Synthetic FREEWAY 9",)), "freeway_name"),
])
def test_s39_road_attributes_with_a_motorway_or_a_freeway_name_are_fail(trace, signal):
    outcome, _ = outcome_of(trace=trace)
    assert outcome.freeway_check == "fail" and signal in outcome.signals and outcome.leg is None


@pytest.mark.parametrize("route, signal", [
    (route_body(OUT_POINTS, names=("國道1號", "Synthetic Road 2")), "freeway_name"),
    (route_body(OUT_POINTS, maneuvers=[{"street_names": ["Synthetic Road 1"], "highway": True}]), "maneuver_highway"),
])
def test_maneuver_names_and_highway_flags_are_freeway_signals(route, signal):
    outcome, _ = outcome_of(route=route)
    assert outcome.freeway_check == "fail" and signal in outcome.signals


@pytest.mark.parametrize("failing", ["outbound", "return"])
def test_s24_a_fail_in_either_direction_stores_nothing_and_is_highway_in_route(store, tmp_path, failing):
    kwargs = {"out": route_body(OUT_POINTS, has_highway=True)} if failing == "outbound" else \
        {"back_trace": trace_body(BACK_POINTS, road_class="motorway")}
    engine = round_trip_engine(**kwargs)
    result = plan(engine, store)
    assert result.code == HIGHWAY_IN_ROUTE
    assert_no_route(result)
    assert stored_files(tmp_path) == {}
    assert engine.actions().count("route") == 2 and "status" not in engine.actions()


@pytest.mark.parametrize("trace", [
    reply({"error": "synthetic"}, status=500),
    reply({"edges": []}),
    reply({"no_edges": True}),
    reply(b"not json"),
    reply({"edges": [{"length": 1.0}]}),                                     # no road class
    reply({"edges": [{"road_class": "primary", "length": "1"}]}),            # length not a number
    reply({"edges": [{"road_class": "primary", "length": 1.0, "names": "x"}]}),
    TransportError("synthetic"),
])
def test_s39_a_failed_road_attribute_query_is_routing_unavailable_with_no_snapshot(store, tmp_path, trace):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS))], traces=[trace])
    result = plan(engine, store, engine_request("one_way"))
    assert result.code == ROUTING_UNAVAILABLE and "outbound:trace_failed" in result.reasons
    assert stored_files(tmp_path) == {}


@pytest.mark.parametrize("trace", [
    reply({"error": "synthetic"}, status=500), reply({"edges": []}), reply({"edges": [{"length": 1.0}]}),
])
def test_a_failed_road_attribute_query_gives_no_freeway_check_value(trace):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS))], traces=[trace])
    outcome = evaluate_direction(ValhallaClient(engine, clock=Clock()), "outbound",
                                 [valhalla.position_from(p) for p in OUT_POSITIONS])
    assert outcome.freeway_check is None and outcome.leg is None and "trace_failed" in outcome.reasons


@pytest.mark.parametrize("summary_value", ["drop", None, "false", 0, 1, "true"])
def test_has_highway_not_reported_is_routing_unavailable_with_no_freeway_check_value(store, tmp_path, summary_value):
    body = route_body(OUT_POINTS, drop_has_highway=summary_value == "drop")
    if summary_value != "drop":
        body["trip"]["summary"]["has_highway"] = summary_value
    outcome, _ = outcome_of(route=body)
    assert "has_highway_unreported" in outcome.reasons and outcome.leg is None
    if summary_value in (1, "true", "false"):   # a truthy non-boolean flag is also a freeway signal (fail closed)
        assert outcome.freeway_check == "fail"
    else:
        assert outcome.signals == () and outcome.freeway_check is None
        result = plan(one_way_engine(route=body), store, engine_request("one_way"))
        assert result.code == ROUTING_UNAVAILABLE
        assert stored_files(tmp_path) == {}


@pytest.mark.parametrize("scale, adopted", [(1.0, True), (1.02, True), (0.98, True), (1.0201, False), (0.9799, False), (1.5, False)])
def test_the_road_attribute_length_must_be_within_2_percent(store, tmp_path, scale, adopted):
    route_km = 3.0
    edges = {"edges": [{"names": [], "length": route_km * scale, "road_class": "primary"}]}
    route = route_body(OUT_POINTS, length_km=route_km)
    outcome, _ = outcome_of(route=route, trace=edges)
    if adopted:
        assert outcome.freeway_check == "pass" and outcome.leg is not None
    else:
        assert outcome.freeway_check is None and outcome.reasons == ("trace_length_mismatch",)
        result = plan(one_way_engine(route=route, trace=edges), store, engine_request("one_way"))
        assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:trace_length_mismatch",))
        assert stored_files(tmp_path) == {}


def test_the_2_percent_check_is_exact_at_the_boundary():
    # 1.02 * 2.5 is not exactly representable; the comparison is on the decimal values.
    edges = {"edges": [{"names": [], "length": 2.55, "road_class": "primary"}]}
    outcome, _ = outcome_of(route=route_body(OUT_POINTS, length_km=2.5), trace=edges)
    assert outcome.freeway_check == "pass"
    edges = {"edges": [{"names": [], "length": 2.5500001, "road_class": "primary"}]}
    outcome, _ = outcome_of(route=route_body(OUT_POINTS, length_km=2.5), trace=edges)
    assert outcome.reasons == ("trace_length_mismatch",)


@pytest.mark.parametrize("other", ["warning", "offset", "trace_mismatch", "trace_failed", "return_error"])
def test_a_freeway_signal_with_another_reason_is_highway_in_route(store, tmp_path, other):
    out = route_body(OUT_POINTS, has_highway=True)
    out_trace = trace_body(OUT_POINTS)
    back = None
    if other == "warning":
        out = route_body(OUT_POINTS, has_highway=True, warnings=[{"code": 1, "text": "synthetic"}])
    elif other == "trace_mismatch":
        out_trace = trace_body(OUT_POINTS, scale=1.5)
    elif other == "trace_failed":
        out_trace = {"edges": []}
    if other == "return_error":
        engine = FakeEngine(routes=[reply(out), reply({"error": "x"}, 400)], traces=[reply(out_trace)])
    else:
        engine = round_trip_engine(out=out, out_trace=out_trace, back=back)
    positions = None
    if other == "offset":
        far = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1500, 0), pos("SYN-DEST", "destination", 9800, 0)]
        positions = {"outbound": far, "return": BACK_POSITIONS}
    result = plan(engine, store, engine_request(positions=positions))
    assert result.code == HIGHWAY_IN_ROUTE
    assert stored_files(tmp_path) == {}


def test_a_freeway_signal_is_highway_in_route_even_when_the_other_direction_is_unreachable(store):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS, has_highway=True)), TransportError("synthetic")],
                        traces=[reply(trace_body(OUT_POINTS))])
    assert plan(engine, store).code == HIGHWAY_IN_ROUTE


def test_the_freeway_check_runs_even_when_the_offsets_already_fail():
    far = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-DEST", "destination", 9800, 0)]
    outcome, engine = outcome_of(trace=trace_body(OUT_POINTS, road_class="motorway"), positions=far)
    assert engine.actions() == ["route", "trace_attributes"]
    assert outcome.freeway_check == "fail" and "end_offset" in outcome.reasons


def test_the_freeway_check_method_names_the_method_and_thresholds():
    for text in ("trace_attributes", "has_highway", "motorway", "國道|高速公路|Freeway", "2%",
                 "a road attribute reply without warnings"):
        assert text in FREEWAY_CHECK_METHOD
    lowered = (adoption.__doc__ + source.__doc__).lower()
    assert "not an independent check against road authority data" in lowered
    for claim in ("verified by the road authority", "independently verified", "official freeway data"):
        assert claim not in Path(adoption.__file__).read_text(encoding="utf-8").lower()


# --- R1-F1 (audit issue-16-c1-r1): signals in a reply that is not HTTP 200 (CL-R1-8) ---------------

ERROR_STATUSES = [302, 400, 429, 500, 503]


def _error_route(status, **kwargs):
    return reply(route_body(OUT_POINTS, **kwargs), status=status)


@pytest.mark.parametrize("status", ERROR_STATUSES)
@pytest.mark.parametrize("kwargs, signal", [
    ({"has_highway": True}, "has_highway"),
    ({"names": ("國道1號", "Synthetic Road 2")}, "freeway_name"),
    ({"maneuvers": [{"street_names": ["Synthetic Road 1"], "highway": True}]}, "maneuver_highway"),
])
def test_r1_f1_a_non_200_route_reply_with_a_freeway_signal_is_highway_in_route(store, tmp_path, status, kwargs, signal):
    engine = FakeEngine(routes=[_error_route(status, **kwargs), reply(route_body(BACK_POINTS))],
                        traces=[reply(trace_body(BACK_POINTS))])
    result = plan(engine, store)
    assert result.code == HIGHWAY_IN_ROUTE
    assert f"outbound:{signal}" in result.reasons and "outbound:engine_error" in result.reasons
    assert_no_route(result)
    assert stored_files(tmp_path) == {}
    # No road attribute query is based on an error reply; both directions are still sent; no status.
    assert engine.actions() == ["route", "route", "trace_attributes"]


@pytest.mark.parametrize("status", ERROR_STATUSES)
def test_r1_f1_a_non_200_route_reply_is_never_adopted(status):
    engine = FakeEngine(routes=[_error_route(status)])
    outcome = evaluate_direction(ValhallaClient(engine, clock=Clock()), "outbound",
                                 [valhalla.position_from(p) for p in OUT_POSITIONS])
    assert outcome.leg is None and outcome.signals == () and outcome.reasons == ("engine_error",)
    assert outcome.freeway_check is None
    assert engine.actions() == ["route"]


@pytest.mark.parametrize("status", ERROR_STATUSES)
@pytest.mark.parametrize("trace_kw, signal", [
    ({"road_class": "motorway"}, "motorway_edge"),
    ({"names": ("Synthetic Freeway 9",)}, "freeway_name"),
    ({"names": ("國道3號",)}, "freeway_name"),
])
def test_r1_f1_a_non_200_road_attribute_reply_with_a_freeway_signal_is_highway_in_route(store, tmp_path, status, trace_kw, signal):
    engine = round_trip_engine(out_trace=None)
    engine.queue["trace_attributes"][0] = reply(trace_body(OUT_POINTS, **trace_kw), status=status)
    result = plan(engine, store)
    assert result.code == HIGHWAY_IN_ROUTE
    assert f"outbound:{signal}" in result.reasons and "outbound:trace_failed" in result.reasons
    assert_no_route(result)
    assert stored_files(tmp_path) == {}
    assert engine.actions() == ["route", "trace_attributes", "route", "trace_attributes"]  # no retry, no status


@pytest.mark.parametrize("status", ERROR_STATUSES)
def test_r1_f1_a_non_200_road_attribute_reply_without_a_signal_is_routing_unavailable(store, tmp_path, status):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS))], traces=[reply(trace_body(OUT_POINTS), status=status)])
    result = plan(engine, store, engine_request("one_way"))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:trace_failed",))
    assert stored_files(tmp_path) == {}
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS))], traces=[reply(trace_body(OUT_POINTS), status=status)])
    outcome = evaluate_direction(ValhallaClient(engine, clock=Clock()), "outbound",
                                 [valhalla.position_from(p) for p in OUT_POSITIONS])
    assert outcome.freeway_check is None and outcome.leg is None and outcome.signals == ()


@pytest.mark.parametrize("status", ERROR_STATUSES)
def test_r1_f1_a_non_200_route_reply_without_a_signal_is_routing_unavailable(store, tmp_path, status):
    engine = FakeEngine(routes=[_error_route(status)])
    result = plan(engine, store, engine_request("one_way"))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:engine_error",))
    assert stored_files(tmp_path) == {}


UNREADABLE_ROUTE_BODIES = [
    b"not json", b"\xff\xfe\x00", b"", b"[]", b"null", b"{\"x\": NaN}", b"{\"trip\": \"x\"}",
    b"{\"trip\": {}}", b"{\"trip\": {\"summary\": 5, \"legs\": \"bad\"}}",
    b"{\"trip\": {\"summary\": {\"has_highway\": null}, \"legs\": [7, {\"maneuvers\": [3, {\"street_names\": [1]}]}]}}",
    b"{\"trip\": {\"legs\": [{\"shape\": 5, \"maneuvers\": [{\"begin_street_names\": \"x\"}]}], \"warnings\": 3}}",
]


@pytest.mark.parametrize("status", [200, 302, 500])
@pytest.mark.parametrize("body", UNREADABLE_ROUTE_BODIES)
def test_r1_f1_unreadable_route_bodies_are_routing_unavailable_and_do_not_raise(store, tmp_path, status, body):
    engine = FakeEngine(routes=[HttpResponse(status, body)], traces=[])
    result = plan(engine, store, engine_request("one_way"))
    assert result.code == ROUTING_UNAVAILABLE
    assert stored_files(tmp_path) == {}


UNREADABLE_TRACE_BODIES = [
    b"not json", b"\xff\xfe", b"", b"[]", b"7", b"{\"edges\": \"bad\"}", b"{\"edges\": [5, null]}",
    b"{\"edges\": [{\"road_class\": 5, \"names\": \"x\", \"length\": \"y\"}]}",
    b"{\"edges\": [{\"names\": [1, {}], \"length\": -1}], \"warnings\": 3}",
]


@pytest.mark.parametrize("status", [302, 500])
@pytest.mark.parametrize("body", UNREADABLE_TRACE_BODIES)
def test_r1_f1_unreadable_non_200_trace_bodies_are_routing_unavailable_and_do_not_raise(store, tmp_path, status, body):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS))], traces=[HttpResponse(status, body)])
    result = plan(engine, store, engine_request("one_way"))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:trace_failed",))
    assert stored_files(tmp_path) == {}


def test_r1_f1_a_non_200_trace_with_a_signal_in_one_direction_and_an_error_route_in_the_other(store, tmp_path):
    engine = FakeEngine(routes=[reply(route_body(OUT_POINTS)), _error_route(500)],
                        traces=[reply(trace_body(OUT_POINTS, road_class="motorway"), status=503)])
    result = plan(engine, store)
    assert result.code == HIGHWAY_IN_ROUTE
    assert set(result.reasons) >= {"outbound:motorway_edge", "outbound:trace_failed", "return:engine_error"}
    assert stored_files(tmp_path) == {}


# --- CL-R1-27: warnings in the road attribute reply (decision-20261118-issue16-c161 section 4.5) ---

@pytest.mark.parametrize("warnings", [
    [{"code": 400, "text": "synthetic trace warning"}],
    [{"code": 1, "text": "a"}, {"code": 2, "text": "b"}],
    "synthetic warning",
    {"code": 1},
    {},
    ["not an object"],
])
def test_cl_r1_27_a_road_attribute_reply_with_warnings_is_unverifiable(store, tmp_path, warnings):
    trace = dict(trace_body(OUT_POINTS), warnings=warnings)
    outcome, engine = outcome_of(trace=trace)
    assert outcome.reasons == ("trace_warnings",) and outcome.signals == ()
    assert outcome.freeway_check is None and outcome.leg is None
    assert engine.actions() == ["route", "trace_attributes"]
    engine = one_way_engine(trace=trace)
    result = plan(engine, store, engine_request("one_way"))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:trace_warnings",))
    assert engine.actions() == ["route", "trace_attributes"]  # one query, no retry, no status
    assert stored_files(tmp_path) == {}


@pytest.mark.parametrize("edges_kw, signal", [
    ({"road_class": "motorway"}, "motorway_edge"),
    ({"names": ("國道5號",)}, "freeway_name"),
])
def test_cl_r1_27_warnings_with_a_freeway_signal_are_still_highway_in_route(store, tmp_path, edges_kw, signal):
    trace = dict(trace_body(OUT_POINTS, **edges_kw), warnings=[{"code": 1, "text": "synthetic"}])
    outcome, _ = outcome_of(trace=trace)
    assert outcome.freeway_check == "fail" and signal in outcome.signals and "trace_warnings" in outcome.reasons
    result = plan(one_way_engine(trace=trace), store, engine_request("one_way"))
    assert result.code == HIGHWAY_IN_ROUTE
    assert stored_files(tmp_path) == {}


@pytest.mark.parametrize("warnings", [[], None])
def test_cl_r1_27_empty_or_null_warnings_in_the_road_attribute_reply_change_nothing(store, warnings):
    trace = dict(trace_body(OUT_POINTS), warnings=warnings)
    outcome, _ = outcome_of(trace=trace)
    assert outcome.freeway_check == "pass" and outcome.leg is not None
    assert outcome.leg["warnings"] == []
    assert isinstance(plan(one_way_engine(trace=trace), store, engine_request("one_way")), AdoptedRoute)


def test_cl_r1_27_warnings_only_in_the_return_road_attribute_reply_store_nothing(store, tmp_path):
    engine = round_trip_engine(back_trace=dict(trace_body(BACK_POINTS), warnings=[{"code": 1, "text": "synthetic"}]))
    result = plan(engine, store)
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("return:trace_warnings",))
    assert engine.actions() == ["route", "trace_attributes", "route", "trace_attributes"]
    assert stored_files(tmp_path) == {}


def test_cl_r1_27_status_reply_warnings_do_not_affect_adoption(store):
    status = reply(dict(STATUS, warnings=[{"code": 1, "text": "synthetic"}]))
    result = plan(round_trip_engine(statuses=[status]), store)
    assert isinstance(result, AdoptedRoute)
    assert store.load(result.snapshot_id)["engine_version"] == STATUS["version"]


# --- offsets and order (7.11 item 8; CL-R1-7; S40, S68, S69, S70) ---------------------------------

def test_s40_an_end_offset_of_several_kilometres_is_rejected(store, tmp_path):
    far = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1500, 0), pos("SYN-DEST", "destination", 9800, 0)]
    result = plan(one_way_engine(), store, engine_request("one_way", positions={"outbound": far}))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:end_offset",))
    assert stored_files(tmp_path) == {}


@pytest.mark.parametrize("y", [200.5, 250.0, 5000.0])
def test_s40_s68_a_via_more_than_200_m_from_the_shape_is_rejected(store, tmp_path, y):
    positions = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1500, y), pos("SYN-DEST", "destination", 3000, 0)]
    result = plan(one_way_engine(), store, engine_request("one_way", positions={"outbound": positions}))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:via_offset",))
    assert stored_files(tmp_path) == {}


def test_s69_two_vias_within_200_m_but_passed_in_reverse_order_are_rejected(store, tmp_path):
    via_b = {"kind": "landmark", "ref_id": "SYN-VIA-B", "name": "Synthetic via B", "entry_ref_id": None}
    positions = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-B", "via", 2000, 50), pos("SYN-VIA-A", "via", 1000, 50),
                 pos("SYN-DEST", "destination", 3000, 0)]
    request = engine_request("one_way", positions={"outbound": positions}, via=(via_b, syn.VIA_A))
    result = plan(one_way_engine(), store, request)
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:via_order",))
    assert stored_files(tmp_path) == {}
    # The same two vias in the travel order are adopted.
    positions[1], positions[2] = positions[2], positions[1]
    assert isinstance(plan(one_way_engine(), store, engine_request("one_way", positions={"outbound": positions})), AdoptedRoute)


def test_cl_r1_7_vias_with_equal_along_shape_distance_are_out_of_order(store, tmp_path):
    positions = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1500, 40), pos("SYN-VIA-B", "via", 1500, -40),
                 pos("SYN-DEST", "destination", 3000, 0)]
    via_b = {"kind": "landmark", "ref_id": "SYN-VIA-B", "name": "Synthetic via B", "entry_ref_id": None}
    result = plan(one_way_engine(), store, engine_request("one_way", positions={"outbound": positions}, via=(syn.VIA_A, via_b)))
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:via_order",))


def test_s70_the_road_entry_position_also_has_a_via_offset(store):
    positions = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1000, 12),
                 pos("SYN-ROAD-ENTRY", "entry", 2000, 34), pos("SYN-ROAD", "destination", 3000, 0)]
    request = EngineRouteRequest(trip_type="one_way", origin=syn.ORIGIN, destination=syn.ROAD, via=[syn.VIA_A],
                                 definitions=syn.DEFINITIONS, positions={"outbound": positions})
    result = plan(one_way_engine(), store, request)
    leg = store.load(result.snapshot_id)["legs"][0]
    assert len(leg["via_offset_m"]) == 2
    assert leg["via_offset_m"][0] == pytest.approx(12.0, abs=0.2) and leg["via_offset_m"][1] == pytest.approx(34.0, abs=0.2)
    assert [l["role"] for l in leg["request"]["locations"]] == ["origin", "via", "entry", "destination"]


def test_the_offsets_are_recorded_for_both_ends():
    outcome, _ = outcome_of(positions=[pos("SYN-ORIGIN", "origin", 0, 25), pos("SYN-DEST", "destination", 3000, -60)])
    offsets = outcome.leg["endpoint_offset_m"]
    assert offsets["start"] == pytest.approx(25.0, abs=0.01) and offsets["end"] == pytest.approx(60.0, abs=0.01)
    assert outcome.leg["via_offset_m"] == []


@pytest.mark.parametrize("which", ["start", "end", "via"])
def test_cl_r1_19_an_offset_just_above_200_m_is_rejected_on_the_raw_value(store, tmp_path, which):
    """200.04 m is cut to 200.0 m in a stored snapshot; the check uses the raw value."""
    d = 200.04
    positions = {
        "start": [pos("SYN-ORIGIN", "origin", 0, d), pos("SYN-DEST", "destination", 3000, 0)],
        "end": [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-DEST", "destination", 3000, d)],
        "via": [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-VIA-A", "via", 1550, d), pos("SYN-DEST", "destination", 3000, 0)],
    }[which]
    outcome, _ = outcome_of(positions=positions)
    assert outcome.reasons == ({"start": "start_offset", "end": "end_offset", "via": "via_offset"}[which],)
    result = plan(one_way_engine(), store, engine_request("one_way", positions={"outbound": positions}))
    assert isinstance(result, RouteFailure) and stored_files(tmp_path) == {}
    # Just below the limit is adopted, and the stored value is the canonical cut of the raw value.
    ok = copy.deepcopy(positions)
    target = {"start": 0, "end": -1, "via": 1}[which]
    lat, lon = at(1550 if which == "via" else (0 if which == "start" else 3000), 199.96)
    ok[target]["lat"], ok[target]["lon"] = lat, lon
    adopted = plan(one_way_engine(), store, engine_request("one_way", positions={"outbound": ok}))
    leg = store.load(adopted.snapshot_id)["legs"][0]
    stored = leg["via_offset_m"][0] if which == "via" else leg["endpoint_offset_m"][which]
    assert stored == 199.9


def test_cl_r1_19_coordinates_in_the_stored_request_are_floats(store):
    positions = [{"ref_id": "SYN-ORIGIN", "role": "origin", "lat": 0, "lon": 0},
                 {"ref_id": "SYN-DEST", "role": "destination", "lat": at(3000, 0)[0], "lon": at(3000, 0)[1]}]
    engine = one_way_engine()
    result = plan(engine, store, engine_request("one_way", positions={"outbound": positions}))
    first = store.load(result.snapshot_id)["legs"][0]["request"]["locations"][0]
    assert isinstance(first["lat"], float) and isinstance(first["lon"], float)
    sent = engine.calls[0].raw.decode("utf-8")
    assert '"lat":0.0' in sent and '"lon":0.0' in sent


def test_cl_r1_19_fetched_at_is_cut_to_the_second_and_not_after_receipt(store):
    receipt = datetime(2026, 11, 18, 1, 2, 3, 999999, tzinfo=timezone.utc)
    clock = Clock(receipt)
    result = plan(one_way_engine(), store, engine_request("one_way"), clock=clock, now=receipt + timedelta(hours=1))
    fetched_at = store.load(result.snapshot_id)["legs"][0]["fetched_at"]
    assert fetched_at == "2026-11-18T09:02:03+08:00"
    assert datetime.fromisoformat(fetched_at) <= receipt


def test_a_snapshot_stored_this_second_is_reused_right_away(store):
    receipt = datetime(2026, 11, 18, 9, 0, 0, 900000, tzinfo=TAIPEI)
    first = plan(one_way_engine(), store, engine_request("one_way"), clock=Clock(receipt), now=receipt)
    assert plan(FakeEngine(), store, engine_request("one_way"), now=receipt) == first


# --- Snapshot Mode and strict mode (7.11 item 3 (b); S17) -----------------------------------------

def test_s17_snapshot_mode_does_not_call_the_engine(store):
    first = plan(round_trip_engine(), store)
    client = ValhallaClient(refusing_transport)
    later = NOW + timedelta(days=400)
    assert get_route(engine_request(positions=None), store=store, client=client, snapshot_mode=True, now=later) == first
    assert get_route(engine_request(positions=None), store=store, snapshot_mode=True) == first


def test_s17_snapshot_mode_without_a_snapshot_returns_snapshot_missing(store, tmp_path):
    result = get_route(engine_request(), store=store, client=ValhallaClient(refusing_transport), snapshot_mode=True)
    assert result == RouteFailure(SNAPSHOT_MISSING)
    assert stored_files(tmp_path) == {}


def test_strict_mode_uses_the_frozen_snapshot_and_never_the_engine(store):
    first = plan(round_trip_engine(), store)
    entry = {"request_key": the_key(), "snapshot_id": first.snapshot_id, "sha256": store.file_sha256(first.snapshot_id)}
    client = ValhallaClient(refusing_transport)
    assert get_route(engine_request(), store=store, client=client, snapshot_mode=True, frozen_entries=[entry]) == first


def test_strict_mode_stop_propagates_and_nothing_else_is_used(store):
    plan(round_trip_engine(), store)
    with pytest.raises(StrictModeStop) as exc:
        get_route(engine_request(), store=store, client=ValhallaClient(refusing_transport), snapshot_mode=True, frozen_entries=[])
    assert exc.value.reason == "no_entry"


def test_a_frozen_list_outside_snapshot_mode_is_refused(store):
    with pytest.raises(ValueError):
        get_route(engine_request(), store=store, client=ValhallaClient(refusing_transport), frozen_entries=[])


# --- store errors propagate (CL-R1-17, CL-R1-21) --------------------------------------------------

MARKER = "synthetic-dir-0.000002N-0.000002E"


@pytest.fixture
def marked(tmp_path) -> tuple[SnapshotStore, Path]:
    directory = tmp_path / MARKER
    directory.mkdir()
    return SnapshotStore(directory), directory


def assert_path_free(exc: BaseException) -> None:
    assert MARKER not in "".join(traceback.format_exception(exc))


def _broken_file(directory: Path) -> None:
    (directory / "SN-0123456789.json").write_bytes(b"{not a snapshot")


def test_cl_r1_21_i_a_selection_error_in_normal_mode_propagates_and_the_engine_is_not_called(marked):
    store, directory = marked
    plan(round_trip_engine(), store, now=NOW - timedelta(days=1), clock=Clock(NOW - timedelta(days=1)))
    _broken_file(directory)
    engine = FakeEngine()
    with pytest.raises(SnapshotIntegrityError) as exc:
        plan(engine, store)
    assert engine.calls == []
    assert type(exc.value) is SnapshotIntegrityError
    assert_path_free(exc.value)


def test_cl_r1_21_ii_a_selection_error_in_snapshot_mode_is_not_snapshot_missing(marked):
    store, directory = marked
    _broken_file(directory)
    with pytest.raises(SnapshotIntegrityError) as exc:
        get_route(engine_request(), store=store, client=ValhallaClient(refusing_transport), snapshot_mode=True)
    assert_path_free(exc.value)


def test_cl_r1_21_a_listed_entry_that_is_a_directory_stops_normal_mode(marked):
    store, directory = marked
    (directory / "SN-ffffffffff.json").mkdir()
    engine = FakeEngine()
    with pytest.raises(SnapshotIntegrityError):
        plan(engine, store)
    assert engine.calls == []


@pytest.mark.parametrize("error", [SnapshotStoreError, SnapshotConflictError])
def test_cl_r1_21_iii_a_put_error_propagates_and_no_route_is_returned(marked, monkeypatch, error):
    store, directory = marked
    raised = error("SN-0000000000: synthetic store failure")

    def failing_put(self, snapshot):
        raise raised

    monkeypatch.setattr(SnapshotStore, "put", failing_put)
    with pytest.raises(error) as exc:
        plan(round_trip_engine(), store)
    assert exc.value is raised
    assert stored_files(directory) == {}


def test_cl_r1_21_iii_a_real_write_failure_propagates_without_a_path(marked, monkeypatch):
    store, directory = marked

    def refuse_open(path, mode="r", *args, **kwargs):
        raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(path))

    monkeypatch.setattr(store_module, "open", refuse_open, raising=False)
    with pytest.raises(SnapshotStoreError) as exc:
        plan(round_trip_engine(), store)
    assert_path_free(exc.value)
    assert stored_files(directory) == {}


def test_a_store_must_be_given_and_no_default_location_exists(tmp_path):
    with pytest.raises(TypeError):
        get_route(engine_request(), client=ValhallaClient(refusing_transport))
    with pytest.raises(TypeError):
        get_route(engine_request(), store=str(tmp_path), client=ValhallaClient(refusing_transport))


# --- request input checks; privacy of messages (CL-R1-9; H-2) -------------------------------------

@pytest.mark.parametrize("positions", [
    None,
    {"outbound": OUT_POSITIONS},                                         # round trip without return
    {"outbound": OUT_POSITIONS, "return": BACK_POSITIONS, "extra": OUT_POSITIONS},
    {"outbound": OUT_POSITIONS[:1], "return": BACK_POSITIONS},
    {"outbound": "SYN", "return": BACK_POSITIONS},
])
def test_normal_mode_needs_positions_for_exactly_the_directions(store, positions):
    request = EngineRouteRequest(trip_type="round_trip", origin=syn.ORIGIN, destination=syn.DEST, via=[syn.VIA_A],
                                 definitions=syn.DEFINITIONS, positions=positions)
    engine = FakeEngine()
    with pytest.raises(ValueError):
        plan(engine, store, request)
    assert engine.calls == []


SECRET_LAT = 0.0123456789


@pytest.mark.parametrize("change", [
    {"lat": 91.0}, {"lon": -180.5}, {"lat": float("nan")}, {"lat": "0.1"}, {"lat": True},
    {"ref_id": ""}, {"role": None},
])
def test_bad_positions_are_refused_without_the_coordinates_in_the_message(store, change):
    bad = dict(OUT_POSITIONS[1], lat=SECRET_LAT, **change) if "lat" not in change else dict(OUT_POSITIONS[1], lon=SECRET_LAT, **change)
    positions = {"outbound": [OUT_POSITIONS[0], bad, OUT_POSITIONS[2]], "return": BACK_POSITIONS}
    engine = FakeEngine()
    with pytest.raises(ValueError) as exc:
        plan(engine, store, engine_request(positions=positions))
    text = "".join(traceback.format_exception(exc.value))
    assert str(SECRET_LAT) not in text and "0.0123" not in text
    assert engine.calls == []


def test_route_errors_hold_codes_only():
    far = [pos("SYN-ORIGIN", "origin", 0, 0), pos("SYN-DEST", "destination", 9800, 0)]
    outcome, _ = outcome_of(positions=far)
    for item in (*outcome.reasons, *outcome.signals):
        assert re.fullmatch(r"[a-z_]+", item)


# --- (f) the shared interface: the target GPX source (CL-R1-24) ----------------------------------

GPX11 = "http://www.topografix.com/GPX/1/1"


def gpx(points) -> bytes:
    body = "".join(f'<trkpt lat="{lat!r}" lon="{lon!r}"/>' for lat, lon in points)
    return f'<?xml version="1.0"?><gpx xmlns="{GPX11}" version="1.1"><trk><trkseg>{body}</trkseg></trk></gpx>'.encode()


def out_and_back_points(length=3000.0, offset=10.0, step=50.0):
    return line(0, 0, length, 0, step=step) + line(length - step, offset, 0, offset, step=step)[0:]


class Untouchable:
    def __getattr__(self, name):
        raise AssertionError("the snapshot store must not be used for a target GPX")


@pytest.mark.parametrize("trip_type, km", [("one_way", None), ("round_trip", None), ("round_trip", 1.2345), ("one_way", 1.0)])
def test_cl_r1_24_a_target_gpx_route_is_carried_as_it_is(trip_type, km):
    data = gpx(out_and_back_points())
    direct = target_gpx_route_from_bytes(data, trip_type, km)
    client = ValhallaClient(refusing_transport)
    result = get_route(TargetGpxRequest(trip_type, data=data, turnaround_km=km), store=Untouchable(), client=client)
    assert isinstance(result, AdoptedRoute)
    assert result.route_id == direct.route_id and result.route_source == "target_gpx" == direct.route_source
    assert result.trip_type == direct.trip_type and result.target_gpx_ref == direct.target_gpx_ref
    assert result.snapshot_id is None
    assert result.turnaround_m == direct.turnaround_m and result.turnaround_source == direct.turnaround_source
    assert [leg.direction for leg in result.legs] == [leg.direction for leg in direct.legs]
    for mine, theirs in zip(result.legs, direct.legs):
        assert mine.points == theirs.points and mine.distance_m == theirs.length_m and mine.road_names == ()
    if trip_type == "round_trip":
        assert result.legs[0].points[-1] == result.legs[1].points[0]  # the shared turnaround point stays
        if km is not None:
            assert result.turnaround_m != round(km * 1000)  # the adopted c_k, not the requested metres
    else:
        assert result.turnaround_m is None and len(result.legs) == 1


def test_cl_r1_24_a_target_gpx_path_is_read_and_carried_as_it_is(tmp_path):
    file = tmp_path / "synthetic-route.gpx"
    file.write_bytes(gpx(out_and_back_points()))
    result = get_route(TargetGpxRequest("round_trip", path=file))
    assert isinstance(result, AdoptedRoute)
    assert "synthetic-route" not in repr(result) and str(tmp_path) not in repr(result)


@pytest.mark.parametrize("data, trip_type, km, code, case", [
    (gpx([at(0, 0)]), "one_way", None, TARGET_GPX_INVALID, "too_few_points"),
    (b"not xml", "one_way", None, TARGET_GPX_INVALID, "unreadable"),
    (gpx(line(0, 0, 3000, 0, step=50)), "round_trip", None, TARGET_GPX_NOT_ROUND_TRIP, "end_not_at_start"),
    (gpx(out_and_back_points()), "round_trip", 99.0, TARGET_GPX_NOT_ROUND_TRIP, "turnaround_unconfirmed"),
])
def test_cl_r1_24_target_gpx_errors_pass_through_with_their_case(data, trip_type, km, code, case):
    result = get_route(TargetGpxRequest(trip_type, data=data, turnaround_km=km), store=Untouchable(),
                       client=ValhallaClient(refusing_transport))
    assert result == RouteFailure(code, case)


def test_cl_r1_24_caller_errors_of_the_target_gpx_propagate():
    data = gpx(out_and_back_points())
    with pytest.raises(TripTypeRequiredError):
        get_route(TargetGpxRequest(None, data=data))
    with pytest.raises(ValueError):
        get_route(TargetGpxRequest("both", data=data))
    with pytest.raises(ValueError):
        get_route(TargetGpxRequest("one_way"))
    with pytest.raises(ValueError):
        get_route(TargetGpxRequest("one_way", data=data, path="x.gpx"))


def test_get_route_refuses_other_request_types():
    with pytest.raises(TypeError):
        get_route({"trip_type": "one_way"})


# --- DD-R1-2: engine version and map data date ---------------------------------------------------

@pytest.mark.parametrize("status, version, map_date", [
    (reply({"version": "9.9.9-synthetic", "tileset_last_modified": 1762300800}), "9.9.9-synthetic",
     datetime.fromtimestamp(1762300800, TAIPEI).date().isoformat()),
    (reply({"tileset_last_modified": 1762300800}), ENGINE_VERSION_UNREPORTED,
     datetime.fromtimestamp(1762300800, TAIPEI).date().isoformat()),
    (reply({"version": "9.9.9-synthetic"}), "9.9.9-synthetic", None),
    (reply({"version": "", "tileset_last_modified": "2026-11-01"}), ENGINE_VERSION_UNREPORTED, None),
    (reply({"version": 3, "tileset_last_modified": True}), ENGINE_VERSION_UNREPORTED, None),
    (reply({"version": "9.9.9"}, status=500), ENGINE_VERSION_UNREPORTED, None),
    (reply(b"not json"), ENGINE_VERSION_UNREPORTED, None),
    (TransportError("synthetic"), ENGINE_VERSION_UNREPORTED, None),
])
def test_dd_r1_2_engine_version_and_map_data_date(store, status, version, map_date):
    engine = round_trip_engine(statuses=[status])
    result = plan(engine, store)
    snapshot = store.load(result.snapshot_id)
    assert snapshot["engine_version"] == version and snapshot["map_data_date"] == map_date


# --- ID patterns and the R1-2 contract on the integration path (CL-R1-13; SR1-AC2) ---------------

def test_cl_r1_13_the_ids_on_the_engine_path_follow_the_contract_patterns(store):
    result = plan(round_trip_engine(), store)
    assert re.fullmatch(r"RS-[0-9a-f]{10}", result.route_id) and re.search(ROUTE_ID_PATTERN, result.route_id)
    assert re.fullmatch(r"SN-[0-9a-f]{10}", result.snapshot_id) and re.search(SNAPSHOT_ID_PATTERN, result.snapshot_id)
    assert result.route_id[3:] == result.snapshot_id[3:]


def test_every_new_name_is_exported_from_the_routing_package():
    for name in ("get_route", "EngineRouteRequest", "TargetGpxRequest", "AdoptedRoute", "AdoptedLeg", "RouteFailure",
                 "ValhallaClient", "HttpResponse", "TransportError", "VALHALLA_ENDPOINT", "USER_AGENT",
                 "evaluate_direction", "decide_code", "FREEWAY_CHECK_METHOD"):
        assert name in routing.__all__ and hasattr(routing, name)


def test_positions_accept_the_dataclass_too():
    p = Position("SYN-ORIGIN", "origin", 0, 0)
    assert valhalla.position_from(p) == Position("SYN-ORIGIN", "origin", 0.0, 0.0)
