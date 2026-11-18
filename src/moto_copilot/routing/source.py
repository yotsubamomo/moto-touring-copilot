"""The shared route interface (SPEC-R1 R1-4 scope (e), (f); SPEC-001 7.11 item 3).

`get_route` is the one function that returns either the adopted route or a route error code,
for both route sources:

- `TargetGpxRequest` (route_source `target_gpx`, R1-3): the result of `target_gpx` is carried as
  it is (CL-R1-24). The routing engine and the snapshot store are not used; no freeway, warning,
  offset or order check is applied; nothing is recomputed, reversed, reordered, interpolated or
  deduplicated, and the shared turnaround point stays in both legs. Its error code and case are
  passed through; `TripTypeRequiredError`, `ValueError` and `TypeError` propagate.
- `EngineRouteRequest` (route_source `routing`), in the order of 7.11 item 3:
  - Snapshot Mode: only R1-2's selection, never the engine. With a frozen list, strict mode
    (`select_strict`; `StrictModeStop` propagates); without, `select_snapshot_mode`
    (`snapshot_missing` when there is none).
  - normal mode: R1-2's `find_reusable` first (same `request_key` and method, within 30 days);
    only when there is none, the engine: one route request and one road attribute query per
    direction (adoption.py). Only when every direction is adopted is the snapshot built and
    stored through R1-2 (`SnapshotStore.put`). Otherwise the route error code of CL-R1-8 is
    returned, nothing is stored, and no expired snapshot is used instead.

Errors of the snapshot store are never caught here (CL-R1-17, CL-R1-21): `SnapshotIntegrityError`
from selection, `SnapshotStoreError` / `SnapshotConflictError` from `put` all propagate; they are
not retried, not turned into a route error code, and no route is returned that was not stored.
Snapshots are obtained only through `find_reusable`, `select_snapshot_mode` and `select_strict`.

Nothing here logs. Results and errors carry no file path and no file name; route errors carry
codes only, never a coordinate.
"""
from __future__ import annotations

import os
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime

from ..contracts.schemas import TRIP_TYPES
from ..ingest.geometry import GeoPoint
from .adoption import FREEWAY_CHECK_METHOD, DirectionOutcome, decide_code, evaluate_direction, not_sent
from .request_key import request_key
from .snapshot import LEG_DIRECTIONS, TAIPEI, build_snapshot, route_id_for
from .store import (
    FrozenEntry,
    SnapshotIntegrityError,
    SnapshotStore,
    find_reusable,
    select_snapshot_mode,
    select_strict,
)
from .target_gpx import TargetGpxError, target_gpx_route, target_gpx_route_from_bytes
from .valhalla import (
    ENGINE_NAME,
    PolylineError,
    Position,
    TransportError,
    ValhallaClient,
    decode_polyline6,
    position_from,
    routing_params,
)

ROUTE_SOURCE_ROUTING = "routing"
ROUTE_SOURCE_TARGET_GPX = "target_gpx"
ENGINE_VERSION_UNREPORTED = "unreported"  # DD-R1-2


@dataclass(frozen=True)
class AdoptedLeg:
    """One direction of the adopted route: its geometry in order, its length and its road names."""

    direction: str                  # "outbound" or "return"
    points: tuple[GeoPoint, ...]
    distance_m: int | float         # routing: the stored integer metres; target_gpx: its length as it is
    road_names: tuple[str, ...]     # in travel order; empty for target_gpx


@dataclass(frozen=True)
class AdoptedRoute:
    route_id: str
    route_source: str               # "routing" or "target_gpx"
    trip_type: str
    snapshot_id: str | None         # routing only
    target_gpx_ref: str | None      # target_gpx only (SHA-256 of the file)
    turnaround_m: int | None        # target_gpx round trip only: the adopted turnaround position
    turnaround_source: str | None   # target_gpx round trip only; information, not identity
    legs: tuple[AdoptedLeg, ...]    # one_way: (outbound,); round_trip: (outbound, return)


@dataclass(frozen=True)
class RouteFailure:
    """A route error code (SPEC-001 4.13). `case` is the target GPX case; `reasons` are codes only."""

    code: str
    case: str | None = None
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class TargetGpxRequest:
    """A target route GPX given as bytes or as a path (exactly one), the trip type and the rider's km."""

    trip_type: str | None
    data: bytes | None = None
    path: str | os.PathLike | None = None
    turnaround_km: float | None = None


@dataclass(frozen=True)
class EngineRouteRequest:
    """A routing-engine route request.

    `origin`, `destination` and `via` are the places of the request (`ref_id`, `entry_ref_id`) and
    `definitions` their coordinate definitions: they make the `request_key` (CL-R1-2).
    `positions` maps each direction of the trip type to its request positions in order (start,
    intermediates, end; each with ref_id, role, lat, lon; CL-R1-5). The caller gives the return
    positions; they are not derived from the outbound ones. Positions are needed only when the
    engine may be called (normal mode).
    """

    trip_type: str
    origin: Mapping
    destination: Mapping
    via: Sequence[Mapping]
    definitions: Mapping[str, Mapping]
    positions: Mapping[str, Sequence] | None = None


def get_route(
    request: EngineRouteRequest | TargetGpxRequest,
    *,
    store: SnapshotStore | None = None,
    client: ValhallaClient | None = None,
    snapshot_mode: bool = False,
    frozen_entries: Iterable[FrozenEntry | Mapping] | None = None,
    now: datetime | None = None,
) -> AdoptedRoute | RouteFailure:
    """The adopted route, or the route error code (see the module docstring).

    Engine requests: `store` is required; `client` is required in normal mode. A frozen list
    (`frozen_entries`, possibly empty) means strict mode and `snapshot_mode` must then be True.
    `now` is the time used for the 30-day reuse window (default: the current time in +08:00).
    """
    if isinstance(request, TargetGpxRequest):
        return _target_gpx(request)
    if not isinstance(request, EngineRouteRequest):
        raise TypeError("request must be an EngineRouteRequest or a TargetGpxRequest")
    if not isinstance(store, SnapshotStore):
        raise TypeError("an engine route needs a SnapshotStore")
    if request.trip_type not in TRIP_TYPES:
        raise ValueError(f"trip_type must be one of {', '.join(TRIP_TYPES)}")
    if frozen_entries is not None and not snapshot_mode:
        raise ValueError("a frozen list is used only in Snapshot Mode (strict mode)")

    if snapshot_mode:
        rkey = _request_key(request)
        if frozen_entries is not None:
            return _from_snapshot(select_strict(store, rkey, FREEWAY_CHECK_METHOD, frozen_entries))
        selected = select_snapshot_mode(store, rkey, FREEWAY_CHECK_METHOD)
        if selected.snapshot is None:
            return RouteFailure(selected.route_error)
        return _from_snapshot(selected.snapshot)

    if not isinstance(client, ValhallaClient):
        raise TypeError("normal mode needs a ValhallaClient")
    positions = _positions(request)
    rkey = _request_key(request)
    if now is None:
        now = datetime.now(TAIPEI)
    reusable = find_reusable(store, rkey, FREEWAY_CHECK_METHOD, now=now)
    if reusable is not None:
        return _from_snapshot(reusable)

    outcomes = _ask_engine(client, request.trip_type, positions)
    code = decide_code(outcomes)
    if code is not None:
        return RouteFailure(code, None, _reasons(outcomes))
    version, map_date = _engine_info(client)
    snapshot = build_snapshot(
        request_key=rkey,
        trip_type=request.trip_type,
        routing_params=routing_params(),
        engine_name=ENGINE_NAME,
        engine_version=version,
        map_data_date=map_date,
        legs=[o.leg for o in outcomes],
    )
    stored = store.put(snapshot)  # SnapshotStoreError / SnapshotConflictError propagate (CL-R1-21)
    return _from_snapshot(stored.snapshot)


# --- engine route --------------------------------------------------------------------------------

def _request_key(request: EngineRouteRequest) -> str:
    return request_key(
        trip_type=request.trip_type,
        origin=request.origin,
        destination=request.destination,
        via=list(request.via),
        routing_params=routing_params(),
        definitions=request.definitions,
    )


def _positions(request: EngineRouteRequest) -> dict[str, list[Position]]:
    expected = LEG_DIRECTIONS[request.trip_type]
    given = request.positions
    if not isinstance(given, Mapping) or set(given) != set(expected):
        raise ValueError(f"{request.trip_type} needs request positions for exactly: {', '.join(expected)}")
    out = {}
    for direction in expected:
        items = given[direction]
        if isinstance(items, (str, bytes)) or not isinstance(items, Sequence) or len(items) < 2:
            raise ValueError(f"{direction}: request positions must be a list of at least two positions")
        out[direction] = [position_from(item) for item in items]
    return out


def _ask_engine(client: ValhallaClient, trip_type: str, positions: dict[str, list[Position]]) -> list[DirectionOutcome]:
    """Every direction is sent and checked, unless the engine cannot be reached at all (CL-R1-8)."""
    outcomes: list[DirectionOutcome] = []
    unreachable = False
    for direction in LEG_DIRECTIONS[trip_type]:
        if unreachable:
            outcomes.append(not_sent(direction))
            continue
        outcome = evaluate_direction(client, direction, positions[direction])
        outcomes.append(outcome)
        unreachable = outcome.unreachable
    return outcomes


def _reasons(outcomes: Sequence[DirectionOutcome]) -> tuple[str, ...]:
    return tuple(f"{o.direction}:{item}" for o in outcomes for item in (*o.signals, *o.reasons))


def _engine_info(client: ValhallaClient) -> tuple[str, str | None]:
    """(engine_version, map_data_date) from the status reply (DD-R1-2).

    No version reported: the fixed string `unreported`, nothing guessed. `map_data_date` is the
    +08:00 date of the reported `tileset_last_modified` (Unix seconds); not reported: None, never
    the acquisition date.
    """
    try:
        reply = client.status()
    except TransportError:
        return ENGINE_VERSION_UNREPORTED, None
    body = reply.body if reply.status == 200 and isinstance(reply.body, dict) else {}
    version = body.get("version")
    if not isinstance(version, str) or version == "":
        version = ENGINE_VERSION_UNREPORTED
    modified = body.get("tileset_last_modified")
    map_date = None
    if isinstance(modified, int) and not isinstance(modified, bool) and modified >= 0:
        try:
            map_date = datetime.fromtimestamp(modified, TAIPEI).date().isoformat()
        except (OverflowError, OSError, ValueError):
            map_date = None
    return version, map_date


def _from_snapshot(snapshot: dict) -> AdoptedRoute:
    """The adopted route of a stored (validated) snapshot. The shapes are decoded, never reversed."""
    snapshot_id = snapshot["snapshot_id"]
    legs = []
    for leg in snapshot["legs"]:
        try:
            points = tuple(GeoPoint(lat, lon) for lat, lon in decode_polyline6(leg["shape"]))
        except PolylineError:
            raise SnapshotIntegrityError(f"{snapshot_id}: a stored shape cannot be decoded") from None
        legs.append(AdoptedLeg(leg["direction"], points, leg["distance_m"], tuple(leg["road_names"])))
    return AdoptedRoute(
        route_id=route_id_for(snapshot_id),
        route_source=ROUTE_SOURCE_ROUTING,
        trip_type=snapshot["trip_type"],
        snapshot_id=snapshot_id,
        target_gpx_ref=None,
        turnaround_m=None,
        turnaround_source=None,
        legs=tuple(legs),
    )


# --- target route GPX ----------------------------------------------------------------------------

def _target_gpx(request: TargetGpxRequest) -> AdoptedRoute | RouteFailure:
    if (request.data is None) == (request.path is None):
        raise ValueError("give the target GPX either as data or as a path, not both")
    if request.data is not None:
        result = target_gpx_route_from_bytes(request.data, request.trip_type, request.turnaround_km)
    else:
        result = target_gpx_route(request.path, request.trip_type, request.turnaround_km)
    if isinstance(result, TargetGpxError):
        return RouteFailure(result.code, result.case)
    return AdoptedRoute(
        route_id=result.route_id,
        route_source=result.route_source,
        trip_type=result.trip_type,
        snapshot_id=None,
        target_gpx_ref=result.target_gpx_ref,
        turnaround_m=result.turnaround_m,
        turnaround_source=result.turnaround_source,
        legs=tuple(AdoptedLeg(leg.direction, leg.points, leg.length_m, ()) for leg in result.legs),
    )
