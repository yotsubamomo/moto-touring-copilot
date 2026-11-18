"""The target route GPX as a route source (SPEC-R1 R1-3 scope (b); SPEC-001 7.11 item 2; CL-R1-10).

Given a GPX file, the trip type chosen by the rider and, optionally, the rider's turnaround
position (`target_gpx_turnaround_km`), this module either returns the adopted route geometry or
one of the two target GPX route error codes:

- `target_gpx_invalid`: fewer than two points, a total length under 1 km, or two adjacent points
  (also across `trkseg`) more than 1 km apart (CL-R1-10 item 2). A file that cannot be read gives
  the same code.
- `target_gpx_not_round_trip`, with the case: `end_not_at_start` (the end is more than 200 m
  from the start, even when a turnaround position is given) or `turnaround_unconfirmed` (the
  rider's position is not legal, or no position was given and the track is not clearly out and
  back) (CL-R1-10 item 4).

The trip type comes only from the caller. It is never inferred from the geometry; a missing trip
type raises `TripTypeRequiredError` (CL-R1-10 item 3). One way: the geometry is used as it is and
no turnaround position is used. The geometry is never reversed, and no point is added, moved or
dropped: every point of a returned leg is a point of the file, in file order.

Round trip turnaround (CL-R1-10 item 4; CL-R1-22, decision-20261118-issue15-c151): a legal rider
position m (0 < m < total, CL-R1-18) is realised at the usable track point whose distance along
the track is closest to m, compared exactly with `Decimal` (the lower index on a tie); no point is
interpolated. Without a rider position, the detected turnaround is the farthest point. In both
cases the turnaround is a point of the file: it ends the outbound leg and starts the return leg.

Out-and-back detection (CL-R1-10 item 5) uses conservative heuristic thresholds (50 m / 100 m /
90%), NOT validated with real data; nothing in this module claims otherwise.

`route_id` (CL-R1-10 item 6; SPEC-001 §2): `RG-` plus the first 10 hex characters of the SHA-256 of
`<file SHA-256 hex>:<trip_type>`, followed for a round trip by `:<turnaround metres>`. The
turnaround metres are those of the adopted turnaround point, `c_k` (CL-R1-22 item 5), rounded half
up from the shortest decimal form of its distance along the track, for both the rider's and the
detected position (CL-R1-18, decision-20261118-issue14-c141); Python's `round()` is not used.
`target_gpx_ref` is the SHA-256 of the file's bytes.

Privacy (CL-R1-10 item 7): results and errors carry no path and no file name, and this module
does not log.
"""
from __future__ import annotations

import bisect
import hashlib
import math
import os
import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Context, Decimal

from ..contracts.schemas import ROUTE_ID_PATTERN, TRIP_TYPES
from ..ingest.geometry import GeoPoint, GpxGeometryError, parse_gpx_geometry, read_gpx_geometry
from ..ingest.segments import EARTH_RADIUS_M, haversine_m

ROUTE_SOURCE = "target_gpx"

TARGET_GPX_INVALID = "target_gpx_invalid"
TARGET_GPX_NOT_ROUND_TRIP = "target_gpx_not_round_trip"

# Cases of target_gpx_invalid (the code is what counts; the case says which check failed).
TOO_FEW_POINTS = "too_few_points"
TOO_SPARSE = "adjacent_points_too_far"
TOO_SHORT = "too_short"
# GpxGeometryError reasons ("unreadable", "malformed_point") are passed through as cases.

# The two cases of target_gpx_not_round_trip (SPEC-001 4.13).
END_NOT_AT_START = "end_not_at_start"
TURNAROUND_UNCONFIRMED = "turnaround_unconfirmed"

TURNAROUND_FROM_RIDER = "rider"
TURNAROUND_DETECTED = "detected"

# SPEC-001 5.4 and 7.11 item 2 (setting constants; not tuned to test results).
MIN_TOTAL_M = 1000.0        # a total length under this is target_gpx_invalid
MAX_STEP_M = 1000.0         # two adjacent points farther apart than this are target_gpx_invalid
MAX_END_TO_START_M = 200.0  # a round trip needs the end within this of the start
# Conservative heuristic thresholds of the out-and-back detection; NOT validated with real data.
SAMPLE_STEP_M = 100.0       # the back part is sampled every this many metres along the track
NEAR_M = 50.0               # a sample is near when a point of the front part is within this
NEAR_SHARE = (9, 10)        # detected when near samples / all samples >= 9/10

_DECIMAL = Context(prec=400)


class TripTypeRequiredError(ValueError):
    """No trip type was given. The trip type is never inferred from the geometry (CL-R1-10 item 3)."""


@dataclass(frozen=True)
class TargetGpxLeg:
    direction: str                  # "outbound" or "return"
    points: tuple[GeoPoint, ...]    # points of the file, in file order
    length_m: float                 # length along the track (sum of haversine steps)


@dataclass(frozen=True)
class TargetGpxRoute:
    """The adopted target GPX route. No path or file name is kept."""
    route_id: str
    trip_type: str
    target_gpx_ref: str             # SHA-256 of the file's bytes
    total_length_m: float
    turnaround_m: int | None        # integer metres of the adopted turnaround point (c_k); None for one way
    turnaround_source: str | None   # "rider", "detected", or None for one way
    legs: tuple[TargetGpxLeg, ...]  # one way: (outbound,); round trip: (outbound, return)
    route_source: str = ROUTE_SOURCE


@dataclass(frozen=True)
class TargetGpxError:
    """A target GPX route error: the code (SPEC-001 4.13) and which case it is."""
    code: str
    case: str


# --- public entry points -------------------------------------------------------------------------

def target_gpx_route(path: str | os.PathLike, trip_type: str | None,
                     turnaround_km: float | None = None) -> TargetGpxRoute | TargetGpxError:
    """The route from the target GPX at `path` (see the module docstring)."""
    _check_trip_type(trip_type)
    try:
        geometry = read_gpx_geometry(path)
    except GpxGeometryError as exc:
        return TargetGpxError(TARGET_GPX_INVALID, exc.reason)
    return _route(geometry.points, geometry.sha256, trip_type, turnaround_km)


def target_gpx_route_from_bytes(data: bytes, trip_type: str | None,
                                turnaround_km: float | None = None) -> TargetGpxRoute | TargetGpxError:
    """The same as `target_gpx_route`, for a GPX already read into memory."""
    _check_trip_type(trip_type)
    try:
        geometry = parse_gpx_geometry(data)
    except GpxGeometryError as exc:
        return TargetGpxError(TARGET_GPX_INVALID, exc.reason)
    return _route(geometry.points, geometry.sha256, trip_type, turnaround_km)


def target_gpx_route_id(target_gpx_ref: str, trip_type: str, turnaround_m: int | None = None) -> str:
    """The `RG-` route_id (SPEC-001 §2 ID row; CL-R1-10 item 6)."""
    if not _is_sha256_hex(target_gpx_ref):
        raise ValueError("target_gpx_ref must be 64 lowercase hex characters")
    if trip_type == "one_way":
        if turnaround_m is not None:
            raise ValueError("a one-way route has no turnaround position")
        text = f"{target_gpx_ref}:{trip_type}"
    elif trip_type == "round_trip":
        if isinstance(turnaround_m, bool) or not isinstance(turnaround_m, int) or turnaround_m <= 0:
            raise ValueError("a round trip needs a positive integer turnaround position in metres")
        text = f"{target_gpx_ref}:{trip_type}:{int(turnaround_m)}"
    else:
        raise ValueError("trip_type must be one_way or round_trip")
    route_id = "RG-" + hashlib.sha256(text.encode("ascii")).hexdigest()[:10]
    assert re.search(ROUTE_ID_PATTERN, route_id)
    return route_id


def turnaround_m_from_km(km: float) -> int | None:
    """The rider's turnaround position in integer metres (CL-R1-18 item 2).

    The shortest decimal form of `km` is multiplied by 1000 and rounded half up; the float is
    never multiplied first (0.5005 * 1000 is 500.49999999999994). Returns None when `km` is not
    finite (not a legal position).
    """
    if isinstance(km, bool) or not isinstance(km, (int, float)):
        raise TypeError("target_gpx_turnaround_km must be a number")
    if isinstance(km, float) and not math.isfinite(km):
        return None
    return _half_up(Decimal(repr(km)) * 1000)


def metres_half_up(value_m: float) -> int:
    """A length in metres rounded half up to an integer, from its shortest decimal form (CL-R1-18 item 3)."""
    if isinstance(value_m, bool) or not isinstance(value_m, (int, float)) or not math.isfinite(value_m):
        raise ValueError("a finite length in metres is required")
    return _half_up(Decimal(repr(value_m)))


def cumulative_m(points: tuple[GeoPoint, ...] | list[GeoPoint]) -> list[float]:
    """Distance along the track from the first point to each point (haversine steps, metres)."""
    out = [0.0]
    for a, b in zip(points, points[1:]):
        out.append(out[-1] + haversine_m(a.lat, a.lon, b.lat, b.lon))
    return out


def detect_out_and_back(points: tuple[GeoPoint, ...] | list[GeoPoint], cum: list[float] | None = None) -> int | None:
    """Out-and-back detection (CL-R1-10 item 5): the index of the turnaround point, or None.

    The boundary is the point farthest from the start in straight line (the first one when
    several are equally far). The back part, from the boundary along the track, is sampled at
    100 m, 200 m, ... (the boundary itself is not a sample). A sample is near when any point of
    the front part (start to boundary, both included) is within 50 m. Detected when the back part
    has at least one sample and at least 90% of the samples are near.

    Conservative heuristic thresholds; NOT validated with real data.
    """
    if len(points) < 2:
        return None
    if cum is None:
        cum = cumulative_m(points)
    start = points[0]
    boundary, farthest = 0, -1.0
    for index, point in enumerate(points):
        distance = haversine_m(start.lat, start.lon, point.lat, point.lon)
        if distance > farthest:
            boundary, farthest = index, distance
    back_length = cum[-1] - cum[boundary]
    count = int(back_length // SAMPLE_STEP_M)
    while count > 0 and count * SAMPLE_STEP_M > back_length:
        count -= 1
    if count == 0:
        return None
    index = _NearIndex(points[: boundary + 1])
    near = 0
    for i in range(1, count + 1):
        sample = _position_along(points, cum, cum[boundary] + i * SAMPLE_STEP_M)
        if index.has_point_within(sample):
            near += 1
    if near * NEAR_SHARE[1] >= NEAR_SHARE[0] * count:
        return boundary
    return None


# --- the decision --------------------------------------------------------------------------------

def _check_trip_type(trip_type) -> None:
    if trip_type is None:
        raise TripTypeRequiredError("trip_type is required; it is not inferred from the GPX geometry")
    if not isinstance(trip_type, str) or trip_type not in TRIP_TYPES:
        raise ValueError("trip_type must be one_way or round_trip")


def _route(points: tuple[GeoPoint, ...], ref: str, trip_type: str,
           turnaround_km: float | None) -> TargetGpxRoute | TargetGpxError:
    if len(points) < 2:
        return TargetGpxError(TARGET_GPX_INVALID, TOO_FEW_POINTS)
    cum = cumulative_m(points)
    for a, b in zip(points, points[1:]):
        if haversine_m(a.lat, a.lon, b.lat, b.lon) > MAX_STEP_M:
            return TargetGpxError(TARGET_GPX_INVALID, TOO_SPARSE)
    total = cum[-1]
    if total < MIN_TOTAL_M:
        return TargetGpxError(TARGET_GPX_INVALID, TOO_SHORT)

    if trip_type == "one_way":
        # The geometry as it is; a turnaround position is not used, even if one was given.
        leg = TargetGpxLeg("outbound", points, total)
        return TargetGpxRoute(target_gpx_route_id(ref, "one_way"), "one_way", ref, total, None, None, (leg,))

    start, end = points[0], points[-1]
    if haversine_m(start.lat, start.lon, end.lat, end.lon) > MAX_END_TO_START_M:
        return TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, END_NOT_AT_START)

    if turnaround_km is not None:
        # The rider's legal position comes first; an illegal one does not fall back to detection.
        metres = turnaround_m_from_km(turnaround_km)
        if metres is None or not 0 < metres < total:
            return TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)
        at = rider_turnaround_index(cum, metres)
        if at is None:
            return TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)
        return _round_trip(points, cum, ref, at, TURNAROUND_FROM_RIDER)

    boundary = detect_out_and_back(points, cum)
    if boundary is None or not _usable(cum, boundary):
        return TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)
    return _round_trip(points, cum, ref, boundary, TURNAROUND_DETECTED)


def rider_turnaround_index(cum: list[float], metres: int) -> int | None:
    """The track point that realises the rider's legal position `metres` (CL-R1-22 items 2-4).

    Among the usable points (`_usable`), the one with the smallest |Decimal(repr(cum_i)) - metres|,
    compared exactly; on a tie the lowest index (so a repeated point gives its first copy). None
    when no point is usable. No point is interpolated (decision-20261118-issue15-c151).
    """
    target = Decimal(metres)
    best: tuple[Decimal, int] | None = None
    for index in range(len(cum)):
        if not _usable(cum, index):
            continue
        distance = abs(Decimal(repr(cum[index])) - target)
        if best is None or distance < best[0]:
            best = (distance, index)
    return None if best is None else best[1]


def _usable(cum: list[float], index: int) -> bool:
    """A point can be the turnaround: 0 < cum_i < total and 0 < c_i < total (CL-R1-22 items 2, 6)."""
    total = cum[-1]
    if not 0 < cum[index] < total:
        return False
    return 0 < metres_half_up(cum[index]) < total


def _round_trip(points, cum, ref, at: int, source: str) -> TargetGpxRoute:
    """Cut at the track point `at` (CL-R1-22 item 7): outbound p_0..p_at, return p_at..p_{n-1}.

    Both legs include the turnaround point. `turnaround_m` and the `RG-` route_id use its integer
    metres c_at (CL-R1-22 item 5; CL-R1-18 item 3), not the rider's requested position.
    """
    metres = metres_half_up(cum[at])
    outbound = TargetGpxLeg("outbound", points[: at + 1], cum[at])
    back = TargetGpxLeg("return", points[at:], cum[-1] - cum[at])
    route_id = target_gpx_route_id(ref, "round_trip", metres)
    return TargetGpxRoute(route_id, "round_trip", ref, cum[-1], metres, source, (outbound, back))


# --- helpers -------------------------------------------------------------------------------------

def _half_up(value: Decimal) -> int:
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP, context=_DECIMAL))


def _is_sha256_hex(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _unit(lat: float, lon: float) -> tuple[float, float, float]:
    phi, lam = math.radians(lat), math.radians(lon)
    return (math.cos(phi) * math.cos(lam), math.cos(phi) * math.sin(lam), math.sin(phi))


def _position_along(points, cum: list[float], distance: float) -> GeoPoint:
    """The position `distance` metres along the track (a sampling position, not a new track point)."""
    if distance >= cum[-1]:
        return points[-1]
    j = bisect.bisect_right(cum, distance) - 1
    a, b = points[j], points[j + 1]
    fraction = (distance - cum[j]) / (cum[j + 1] - cum[j])
    ua, ub = _unit(a.lat, a.lon), _unit(b.lat, b.lon)
    x, y, z = (ua[k] + (ub[k] - ua[k]) * fraction for k in range(3))
    return GeoPoint(math.degrees(math.atan2(z, math.hypot(x, y))), math.degrees(math.atan2(y, x)))


class _NearIndex:
    """Points bucketed by their position on the unit sphere, to find points within a distance.

    Buckets are only a filter: every candidate is checked with the haversine distance. The bucket
    edge is larger than the chord of the search distance, so no point within it is missed.
    """

    def __init__(self, points):
        self._points = list(points)
        self._cell = 1.25 * 2 * math.sin(NEAR_M / (2 * EARTH_RADIUS_M))
        self._grid: dict[tuple[int, int, int], list[int]] = {}
        for i, p in enumerate(self._points):
            self._grid.setdefault(self._key(_unit(p.lat, p.lon)), []).append(i)

    def _key(self, u) -> tuple[int, int, int]:
        return (math.floor(u[0] / self._cell), math.floor(u[1] / self._cell), math.floor(u[2] / self._cell))

    def has_point_within(self, sample: GeoPoint) -> bool:
        """Whether any point is within NEAR_M (haversine) of `sample`."""
        kx, ky, kz = self._key(_unit(sample.lat, sample.lon))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for i in self._grid.get((kx + dx, ky + dy, kz + dz), ()):
                        p = self._points[i]
                        if haversine_m(sample.lat, sample.lon, p.lat, p.lon) <= NEAR_M:
                            return True
        return False
