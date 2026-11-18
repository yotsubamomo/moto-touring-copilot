"""SPEC-R1 Spec Integration (SR1-AC2; audit spec-SPEC-R1-c1-r1, SIA-R1-F1).

Every route here comes from R1-4's shared interface `get_route`, in each mode SR1-AC2 names:
normal mode (the first call fetches and stores a snapshot, the second reuses it), Snapshot Mode,
strict mode, and the target route GPX one way and round trip (including a rider turnaround that
falls between two track points). The `route_id`, `route_source`, `trip_type` and `snapshot_id`
that `get_route` returns are then carried into a minimal synthetic route catalog (contract 2) with
matching `checkpoint_id`s and checked with R1-1's `validate_route_catalog`: the ID patterns, the
checkpoint prefix, invariants 4 and 5 (references by route_source) and the RS-/SN- hex agreement.

The catalog rows are test data only: one segment per direction, checkpoints CP01.. in order. They
are not the product's route catalog and do not define how catalogs, segments or checkpoint numbers
are produced (that is G-RTE, excluded from SPEC-R1). All positions, engine replies and GPX files are
synthetic (tests/test_routing_engine.py helpers, next to 0 deg N, 0 deg E); no network is used.
"""
from __future__ import annotations

import re
import socket
from datetime import timedelta

import pytest

from moto_copilot.contracts import validate_route_catalog
from moto_copilot.contracts.schemas import CHECKPOINT_ID_PATTERN, ROUTE_ID_PATTERN, SNAPSHOT_ID_PATTERN
from moto_copilot.ingest.geometry import GeoPoint
from moto_copilot.routing import (
    AdoptedLeg,
    AdoptedRoute,
    SnapshotStore,
    TargetGpxRequest,
    ValhallaClient,
    get_route,
    target_gpx_route_from_bytes,
)
from moto_copilot.routing.target_gpx import cumulative_m

import test_routing_engine as eng


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)


# --- the minimal synthetic catalog built from a get_route result --------------------------------

def catalog_for(route: AdoptedRoute) -> tuple[list[dict], list[dict], list[dict]]:
    """Contract 2 rows that carry exactly the identity get_route returned (test data, not G-RTE)."""
    rid = route.route_id
    segments, running = [], 0.0
    for index, leg in enumerate(route.legs):
        length = float(leg.distance_m)
        running += length
        end = leg.points[-1]
        segments.append({"route_id": rid, "seg_index": index, "length_m": length, "cum_length_m": running,
                         "seg_category": "C1", "end_lat": end.lat, "end_lon": end.lon})
    n = len(segments)
    kinds = [("start", 0)] + ([("turnaround", 1)] if route.trip_type == "round_trip" else []) + [("end", n)]
    checkpoints = [{"checkpoint_id": f"{rid}-CP{i:02d}", "route_id": rid, "kind": kind, "after_seg_count": after,
                    "name": None, "station_ref": None} for i, (kind, after) in enumerate(kinds, start=1)]
    routes = [{"route_id": rid, "name": "Synthetic integration route", "n_segments": n, "total_length_m": running,
               "source_trip_id": None, "route_source": route.route_source, "snapshot_id": route.snapshot_id,
               "trip_type": route.trip_type, "category_scheme": "synthetic-v1", "catalog_version": "synthetic-v1"}]
    return routes, segments, checkpoints


def assert_contract_identity(route: AdoptedRoute) -> None:
    """The produced IDs pass R1-1's contract checks; RS- hex equals SN- hex for routing routes."""
    routes, segments, checkpoints = catalog_for(route)
    assert validate_route_catalog(routes, segments, checkpoints) == []
    assert re.search(ROUTE_ID_PATTERN, route.route_id)
    for c in checkpoints:
        assert re.search(CHECKPOINT_ID_PATTERN, c["checkpoint_id"])
        assert c["checkpoint_id"].rpartition("-CP")[0] == route.route_id
    if route.route_source == "routing":
        assert re.search(SNAPSHOT_ID_PATTERN, route.snapshot_id)
        assert route.route_id.startswith("RS-") and route.route_id[3:] == route.snapshot_id[3:]
        assert route.target_gpx_ref is None
    else:
        assert route.route_source == "target_gpx" and route.route_id.startswith("RG-")
        assert route.snapshot_id is None and re.fullmatch(r"[0-9a-f]{64}", route.target_gpx_ref)


def test_the_catalog_check_rejects_a_broken_identity():
    """The helper is not vacuous: a wrong hex, prefix or reference is reported by the validator."""
    leg = AdoptedLeg("outbound", (GeoPoint(0.0, 0.0), GeoPoint(0.0, 0.01)), 1000, ())
    route = AdoptedRoute("RS-0123456789", "routing", "one_way", "SN-0123456789", None, None, None, (leg,))
    assert validate_route_catalog(*catalog_for(route)) == []
    routes, segments, checkpoints = catalog_for(route)
    bad_hex = [dict(routes[0], snapshot_id="SN-ffffffffff")]
    assert any("same 10 hex digits" in e for e in validate_route_catalog(bad_hex, segments, checkpoints))
    bad_source = [dict(routes[0], route_source="target_gpx")]
    assert validate_route_catalog(bad_source, segments, checkpoints) != []
    bad_prefix = [dict(c, checkpoint_id="RS-ffffffffff-CP01") if c["kind"] == "start" else c for c in checkpoints]
    assert any("does not start with its route_id" in e for e in validate_route_catalog(routes, segments, bad_prefix))


# --- routing: normal mode (store, then reuse), Snapshot Mode, strict mode ------------------------

@pytest.mark.parametrize("trip_type", ["round_trip", "one_way"])
def test_sr1_ac2_engine_routes_in_every_mode_carry_a_valid_contract_identity(tmp_path, trip_type):
    store = SnapshotStore(tmp_path)
    request = eng.engine_request(trip_type)

    # Normal mode, first call: the engine is asked once per direction and the snapshot is stored.
    engine = eng.round_trip_engine() if trip_type == "round_trip" else eng.one_way_engine()
    first = eng.plan(engine, store, request)
    assert isinstance(first, AdoptedRoute) and first.trip_type == trip_type and first.route_source == "routing"
    directions = 2 if trip_type == "round_trip" else 1
    assert engine.actions() == ["route", "trace_attributes"] * directions + ["status"]
    assert sorted(p.name for p in tmp_path.iterdir()) == [f"{first.snapshot_id}.json"]
    stored = store.load(first.snapshot_id)
    assert stored["request_key"] == eng.the_key(trip_type) and stored["trip_type"] == trip_type
    assert_contract_identity(first)

    # Normal mode, second call: reused, no engine request at all.
    reuse_engine = eng.FakeEngine()
    second = eng.plan(reuse_engine, store, request, now=eng.NOW + timedelta(days=1))
    assert reuse_engine.calls == [] and second == first
    assert_contract_identity(second)

    # Snapshot Mode: only R1-2's selection; the transport refuses any call.
    snapshot_mode = get_route(request, store=store, client=ValhallaClient(eng.refusing_transport), snapshot_mode=True)
    assert snapshot_mode == first
    assert_contract_identity(snapshot_mode)

    # Strict mode: the frozen list names the snapshot and its file SHA-256.
    entry = {"request_key": stored["request_key"], "snapshot_id": first.snapshot_id,
             "sha256": store.file_sha256(first.snapshot_id)}
    strict = get_route(request, store=store, client=ValhallaClient(eng.refusing_transport), snapshot_mode=True,
                       frozen_entries=[entry])
    assert strict == first
    assert_contract_identity(strict)

    # Still exactly one snapshot file.
    assert sorted(p.name for p in tmp_path.iterdir()) == [f"{first.snapshot_id}.json"]


# --- target route GPX: one way, round trip (detected), round trip (rider position between points) -

def _rider_km_between_points(points) -> float:
    """A rider position (km) that is not the cumulative distance of any track point."""
    cum = cumulative_m([GeoPoint(lat, lon) for lat, lon in points])
    middle = len(cum) // 3
    metres = round((cum[middle] + cum[middle + 1]) / 2)
    assert all(abs(c - metres) > 1 for c in cum)
    return metres / 1000


@pytest.mark.parametrize("trip_type, rider", [("one_way", False), ("round_trip", False), ("round_trip", True)],
                         ids=["one_way", "round_trip_detected", "round_trip_rider_between_points"])
def test_sr1_ac2_target_gpx_routes_carry_a_valid_contract_identity(tmp_path, trip_type, rider):
    points = eng.out_and_back_points()
    data = eng.gpx(points)
    km = _rider_km_between_points(points) if rider else None
    result = get_route(TargetGpxRequest(trip_type, data=data, turnaround_km=km), store=eng.Untouchable(),
                       client=ValhallaClient(eng.refusing_transport))
    assert isinstance(result, AdoptedRoute) and result.trip_type == trip_type
    direct = target_gpx_route_from_bytes(data, trip_type, km)
    assert (result.route_id, result.target_gpx_ref, result.turnaround_m, result.turnaround_source) == \
        (direct.route_id, direct.target_gpx_ref, direct.turnaround_m, direct.turnaround_source)
    assert [leg.points for leg in result.legs] == [leg.points for leg in direct.legs]  # passthrough
    if rider:
        assert result.turnaround_source == "rider" and result.turnaround_m != round(km * 1000)
    if trip_type == "round_trip":
        assert result.legs[0].points[-1] == result.legs[1].points[0]
    assert list(tmp_path.iterdir()) == []
    assert_contract_identity(result)
