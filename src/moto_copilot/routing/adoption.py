"""Adoption checks for one direction of a routing-engine route (SPEC-R1 R1-4 scope (b), (c), (d)).

For one direction this module sends one route request and, when the response has a shape, one
road attribute query on that shape (CL-R1-5; no retry). It then collects every check of SPEC-001
7.11 items 5, 7 and 8:

- freeway check (item 5): four signals. A direction is `pass` only when all four hold:
  (1) the road attribute query succeeded and its total length is within 2% of the route length;
  (2) no edge has road class `motorway`;
  (3) no edge name and no maneuver street name matches 國道|高速公路|Freeway (case-insensitive),
      and no maneuver is marked highway;
  (4) the engine reported `has_highway` and it is `false`.
  Any freeway signal (2)-(4) makes it `fail`, also when other information disagrees (fail
  closed). No freeway signal but something that cannot be verified (the query failed, the
  lengths differ by more than 2%, `has_highway` not reported, a response that cannot be read):
  no `freeway_check` value at all.
- warnings (item 7): any warning in the response means the direction is not adopted.
- offsets and order (item 8; CL-R1-7): start offset = start position to the first shape point;
  end offset = end position to the last shape point; each intermediate offset = distance to the
  nearest point of the shape (point to segment). Every offset must be at most 200 m, and the
  along-shape distance of the intermediates' nearest points must be strictly increasing.

Every threshold is checked on the values computed here, never on the canonical values stored in
a snapshot (CL-R1-19 item 1). Only a direction with no freeway signal and no other reason is
turned into a RouteLeg (SPEC-001 4.14). Reasons and signals are codes; nothing here holds or
reports a coordinate in a message. This check uses the same engine and the same open map data
as the route; it is not an independent check against road authority data (SPEC-001 4.12).
"""
from __future__ import annotations

import math
import re
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Context, Decimal

from ..ingest.segments import EARTH_RADIUS_M, haversine_m
from .snapshot import OFFSET_LIMIT_M, TAIPEI
from .valhalla import (
    PolylineError,
    Position,
    TransportError,
    ValhallaClient,
    decode_polyline6,
    route_locations,
    routing_params,
)

ROUTING_UNAVAILABLE = "routing_unavailable"
HIGHWAY_IN_ROUTE = "highway_in_route"

# The current freeway check method (SPEC-001 4.14 freeway_check_method). Changing the method or
# a threshold changes this string, so older snapshots are no longer reused or selected.
FREEWAY_CHECK_METHOD = (
    "valhalla-trace_attributes-v1: pass needs has_highway reported false, no maneuver marked "
    "highway, no motorway edge, no edge or maneuver name matching 國道|高速公路|Freeway "
    "(case-insensitive), and a trace length within 2% of the route length"
)
FREEWAY_NAME = re.compile(r"國道|高速公路|freeway", re.IGNORECASE)
LENGTH_TOLERANCE = Decimal("0.02")  # SPEC-001 5.4 / 7.11 item 5

# Reasons a direction is not adopted (codes only).
ENGINE_UNREACHABLE = "engine_unreachable"   # no HTTP response to the route request
NOT_SENT = "not_sent"                       # not sent: the engine could not be reached before
ENGINE_ERROR = "engine_error"               # an HTTP error, a body that is not JSON, or no trip
RESPONSE_MALFORMED = "response_malformed"   # a field needed for a check cannot be read
WARNINGS = "warnings"
HAS_HIGHWAY_UNREPORTED = "has_highway_unreported"
TRACE_FAILED = "trace_failed"
TRACE_LENGTH_MISMATCH = "trace_length_mismatch"
START_OFFSET = "start_offset"
END_OFFSET = "end_offset"
VIA_OFFSET = "via_offset"
VIA_ORDER = "via_order"

# Freeway signals (any one of them: freeway_check = fail).
SIGNAL_HAS_HIGHWAY = "has_highway"
SIGNAL_MANEUVER_HIGHWAY = "maneuver_highway"
SIGNAL_FREEWAY_NAME = "freeway_name"
SIGNAL_MOTORWAY_EDGE = "motorway_edge"

# Reasons that leave the freeway check unverifiable (no freeway_check value).
_UNVERIFIABLE = (RESPONSE_MALFORMED, HAS_HIGHWAY_UNREPORTED, TRACE_FAILED, TRACE_LENGTH_MISMATCH)

_DECIMAL = Context(prec=400)


@dataclass(frozen=True)
class DirectionOutcome:
    """The result of the checks of one direction.

    `leg` is the RouteLeg (SPEC-001 4.14) only when the direction can be adopted: no signal and
    no reason. `freeway_check` is "pass", "fail" or None (unverifiable, or nothing to check).
    `unreachable` is True when a request of this direction got no response at all.
    """

    direction: str
    signals: tuple[str, ...]
    reasons: tuple[str, ...]
    freeway_check: str | None
    leg: dict | None
    unreachable: bool = False


def not_sent(direction: str) -> DirectionOutcome:
    return DirectionOutcome(direction, (), (NOT_SENT,), None, None)


# --- numbers -------------------------------------------------------------------------------------

def _real(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _dec(value) -> Decimal:
    """The shortest decimal form of a finite number, exactly (no float arithmetic)."""
    return Decimal(repr(value)) if isinstance(value, float) else Decimal(value)


def _half_up(value: Decimal) -> int:
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP, context=_DECIMAL))


# --- the route response --------------------------------------------------------------------------

@dataclass
class _RouteFacts:
    signals: list[str]
    reasons: list[str]
    shape: str | None = None
    points: list[tuple[float, float]] | None = None
    length_km: Decimal | None = None
    time_s: Decimal | None = None
    road_names: list[str] | None = None
    has_highway: bool | None = None


def _names_of(maneuver: dict, facts: _RouteFacts, names: list[str]) -> None:
    for key in ("begin_street_names", "street_names"):
        value = maneuver.get(key)
        if value is None:
            continue
        if not isinstance(value, list):
            facts.reasons.append(RESPONSE_MALFORMED)
            continue
        for name in value:
            if not isinstance(name, str):
                facts.reasons.append(RESPONSE_MALFORMED)
                continue
            if FREEWAY_NAME.search(name):
                facts.signals.append(SIGNAL_FREEWAY_NAME)
            if name and name not in names:
                names.append(name)


def _route_facts(body: dict) -> _RouteFacts:
    """Everything the checks need from a route response, and every freeway signal it holds."""
    facts = _RouteFacts([], [])
    trip = body["trip"]

    # Warnings (7.11 item 7): any entry, well formed or not, is a warning.
    for holder in (body, trip):
        warnings = holder.get("warnings")
        if warnings is None:
            continue
        if not isinstance(warnings, list) or warnings:
            facts.reasons.append(WARNINGS)

    summary = trip.get("summary")
    if isinstance(summary, dict):
        has_highway = summary.get("has_highway")
        if isinstance(has_highway, bool):
            facts.has_highway = has_highway
            if has_highway:
                facts.signals.append(SIGNAL_HAS_HIGHWAY)
        else:
            facts.reasons.append(HAS_HIGHWAY_UNREPORTED)
            if has_highway is not None and has_highway:
                facts.signals.append(SIGNAL_HAS_HIGHWAY)  # a truthy non-boolean flag: fail closed
        length, time = summary.get("length"), summary.get("time")
        if _real(length) and length >= 0:
            facts.length_km = _dec(length)
        else:
            facts.reasons.append(RESPONSE_MALFORMED)
        if _real(time) and time >= 0:
            facts.time_s = _dec(time)
        else:
            facts.reasons.append(RESPONSE_MALFORMED)
    else:
        facts.reasons.extend((HAS_HIGHWAY_UNREPORTED, RESPONSE_MALFORMED))

    legs = trip.get("legs")
    if not isinstance(legs, list) or not legs:
        facts.reasons.append(RESPONSE_MALFORMED)
        return facts
    names: list[str] = []
    for leg in legs:
        if not isinstance(leg, dict):
            facts.reasons.append(RESPONSE_MALFORMED)
            continue
        leg_summary = leg.get("summary")
        if isinstance(leg_summary, dict) and leg_summary.get("has_highway") not in (None, False):
            facts.signals.append(SIGNAL_HAS_HIGHWAY)
        maneuvers = leg.get("maneuvers")
        if not isinstance(maneuvers, list) or not maneuvers:
            facts.reasons.append(RESPONSE_MALFORMED)
            continue
        for maneuver in maneuvers:
            if not isinstance(maneuver, dict):
                facts.reasons.append(RESPONSE_MALFORMED)
                continue
            if maneuver.get("highway") not in (None, False):
                facts.signals.append(SIGNAL_MANEUVER_HIGHWAY)
            _names_of(maneuver, facts, names)
    facts.road_names = names

    # One direction is one leg with one shape (intermediates are "via" locations).
    if len(legs) != 1 or not isinstance(legs[0], dict):
        facts.reasons.append(RESPONSE_MALFORMED)
        return facts
    shape = legs[0].get("shape")
    try:
        points = decode_polyline6(shape)
    except PolylineError:
        facts.reasons.append(RESPONSE_MALFORMED)
        return facts
    if len(points) < 2:
        facts.reasons.append(RESPONSE_MALFORMED)
        return facts
    facts.shape, facts.points = shape, points
    return facts


# --- the road attribute query --------------------------------------------------------------------

def _trace_facts(body, route_length_km: Decimal | None) -> tuple[list[str], list[str]]:
    """Freeway signals and reasons from a road attribute query response."""
    signals: list[str] = []
    reasons: list[str] = []
    edges = body.get("edges") if isinstance(body, dict) else None
    if not isinstance(edges, list) or not edges:
        return signals, [TRACE_FAILED]
    total = Decimal(0)
    readable = True
    for edge in edges:
        if not isinstance(edge, dict):
            readable = False
            continue
        road_class = edge.get("road_class")
        if road_class == "motorway":
            signals.append(SIGNAL_MOTORWAY_EDGE)
        elif not isinstance(road_class, str):
            readable = False
        names = edge.get("names")
        if names is not None:
            if not isinstance(names, list):
                readable = False
            else:
                for name in names:
                    if not isinstance(name, str):
                        readable = False
                    elif FREEWAY_NAME.search(name):
                        signals.append(SIGNAL_FREEWAY_NAME)
        length = edge.get("length")
        if _real(length) and length >= 0:
            total += _dec(length)
        else:
            readable = False
    if not readable:
        reasons.append(TRACE_FAILED)
    elif route_length_km is None:
        reasons.append(TRACE_LENGTH_MISMATCH)
    elif abs(total - route_length_km) > route_length_km * LENGTH_TOLERANCE:
        reasons.append(TRACE_LENGTH_MISMATCH)
    return signals, reasons


# --- offsets and order (CL-R1-7) -----------------------------------------------------------------

def _plane(lat0: float, lon0: float, lat: float, lon: float) -> tuple[float, float]:
    """Local east/north metres of (lat, lon) around (lat0, lon0)."""
    dlon = (lon - lon0 + 180.0) % 360.0 - 180.0
    return (EARTH_RADIUS_M * math.radians(dlon) * math.cos(math.radians(lat0)),
            EARTH_RADIUS_M * math.radians(lat - lat0))


def nearest_on_shape(lat: float, lon: float, points: Sequence[tuple[float, float]]) -> tuple[float, float]:
    """(distance to the nearest point of the shape, along-shape distance of that point), metres.

    Point to segment in the local plane around the position; the along-shape distance is the sum
    of the haversine lengths of the earlier segments plus the share of the nearest segment. On a
    tie the first segment counts.
    """
    best: tuple[float, float] | None = None
    along = 0.0
    for (alat, alon), (blat, blon) in zip(points, points[1:]):
        ax, ay = _plane(lat, lon, alat, alon)
        bx, by = _plane(lat, lon, blat, blon)
        dx, dy = bx - ax, by - ay
        squared = dx * dx + dy * dy
        t = 0.0 if squared == 0.0 else min(1.0, max(0.0, -(ax * dx + ay * dy) / squared))
        distance = math.hypot(ax + t * dx, ay + t * dy)
        segment = haversine_m(alat, alon, blat, blon)
        if best is None or distance < best[0]:
            best = (distance, along + t * segment)
        along += segment
    assert best is not None
    return best


def offsets(positions: Sequence[Position], points: Sequence[tuple[float, float]]) -> tuple[float, float, list[float], list[float]]:
    """(start offset, end offset, intermediate offsets, their along-shape distances), metres."""
    start, end = positions[0], positions[-1]
    start_m = haversine_m(start.lat, start.lon, *points[0])
    end_m = haversine_m(end.lat, end.lon, *points[-1])
    via_m, along_m = [], []
    for p in positions[1:-1]:
        distance, along = nearest_on_shape(p.lat, p.lon, points)
        via_m.append(distance)
        along_m.append(along)
    return start_m, end_m, via_m, along_m


def offset_reasons(start_m: float, end_m: float, via_m: Sequence[float], along_m: Sequence[float]) -> list[str]:
    """The reasons of 7.11 item 8, judged on the computed values (CL-R1-19 item 1)."""
    reasons = []
    if not start_m <= OFFSET_LIMIT_M:
        reasons.append(START_OFFSET)
    if not end_m <= OFFSET_LIMIT_M:
        reasons.append(END_OFFSET)
    if any(not v <= OFFSET_LIMIT_M for v in via_m):
        reasons.append(VIA_OFFSET)
    if any(not a < b for a, b in zip(along_m, along_m[1:])):
        reasons.append(VIA_ORDER)  # strictly increasing; equal is out of order (CL-R1-7)
    return reasons


# --- one direction -------------------------------------------------------------------------------

def _fetched_at(reply) -> str:
    """The receipt time cut to the second (never rounded up; CL-R1-19 item 3), in +08:00."""
    return reply.received_at.astimezone(TAIPEI).replace(microsecond=0).isoformat()


def _unique(items: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


def evaluate_direction(client: ValhallaClient, direction: str, positions: Sequence[Position],
                       method: str = FREEWAY_CHECK_METHOD) -> DirectionOutcome:
    """Send the route request (and the road attribute query) of one direction and check it."""
    try:
        reply = client.route(positions)
    except TransportError:
        return DirectionOutcome(direction, (), (ENGINE_UNREACHABLE,), None, None, unreachable=True)
    body = reply.body
    if reply.status != 200 or not isinstance(body, dict) or not isinstance(body.get("trip"), dict):
        return DirectionOutcome(direction, (), (ENGINE_ERROR,), None, None)

    facts = _route_facts(body)
    signals, reasons = list(facts.signals), list(facts.reasons)
    unreachable = False
    if facts.shape is not None:
        # The query runs even when another check already failed: every available freeway signal
        # is collected before the code is decided (CL-R1-8).
        try:
            trace = client.trace_attributes(facts.shape)
        except TransportError:
            reasons.append(TRACE_FAILED)
            unreachable = True
        else:
            if trace.status != 200:
                reasons.append(TRACE_FAILED)
            else:
                trace_signals, trace_reasons = _trace_facts(trace.body, facts.length_km)
                signals += trace_signals
                reasons += trace_reasons
        start_m, end_m, via_m, along_m = offsets(positions, facts.points)
        reasons += offset_reasons(start_m, end_m, via_m, along_m)
    else:
        reasons.append(RESPONSE_MALFORMED)

    signals_t, reasons_t = _unique(signals), _unique(reasons)
    if signals_t:
        freeway_check = "fail"
    elif any(r in reasons_t for r in _UNVERIFIABLE):
        freeway_check = None
    else:
        freeway_check = "pass"
    if signals_t or reasons_t:
        return DirectionOutcome(direction, signals_t, reasons_t, freeway_check, None, unreachable)

    leg = {
        "direction": direction,
        "request": {
            "locations": [
                {"ref_id": p.ref_id, "role": p.role, **loc}
                for p, loc in zip(positions, route_locations(positions))
            ],
            "routing_params": routing_params(),
        },
        "shape": facts.shape,
        "distance_m": _half_up(facts.length_km * 1000),
        "engine_time_s": _half_up(facts.time_s),
        "road_names": list(facts.road_names),
        "warnings": [],
        "has_highway": False,
        "freeway_check": "pass",
        "freeway_check_method": method,
        "endpoint_offset_m": {"start": float(start_m), "end": float(end_m)},
        "via_offset_m": [float(v) for v in via_m],
        "fetched_at": _fetched_at(reply),
    }
    return DirectionOutcome(direction, (), (), "pass", leg, False)


def decide_code(outcomes: Sequence[DirectionOutcome]) -> str | None:
    """The route error code over all directions (CL-R1-8), or None when every direction is adopted.

    Any freeway signal in any direction: highway_in_route, before every other reason. Otherwise
    any reason in any direction: routing_unavailable.
    """
    if any(o.signals for o in outcomes):
        return HIGHWAY_IN_ROUTE
    if any(o.reasons or o.leg is None for o in outcomes):
        return ROUTING_UNAVAILABLE
    return None
