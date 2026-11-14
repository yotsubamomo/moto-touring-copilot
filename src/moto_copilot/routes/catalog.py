"""Route Catalog (data contract v0.2, contract 2) from private trimmed tracks.

Pre-Spec Technical Spike (M1-B). A demo route is the longest stretch that several trips ride in
the same direction; its geometry comes from one of them (the source trip).
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

from ..ingest import IngestParams, TrackPoint, category_of, curvature_deg_per_km, haversine_m
from ..ingest.segments import EARTH_RADIUS_M


@dataclass(frozen=True)
class MatchParams:
    step_m: float = 100.0     # spacing at which tracks are compared
    tolerance_m: float = 120.0  # two tracks are on the same road within this distance
    max_missed: int = 3       # samples that may fail to match inside a stretch
    max_ahead: int = 15       # how far the other track may advance between two samples


def _project(points: list[TrackPoint], lat0: float) -> list[tuple[float, float]]:
    k = EARTH_RADIUS_M * math.cos(math.radians(lat0))
    return [(k * math.radians(p.lon), EARTH_RADIUS_M * math.radians(p.lat)) for p in points]


def _sample(points: list[TrackPoint], lat0: float, step_m: float) -> list[tuple[float, float, int]]:
    """Positions every step_m along the track, each with the index of the track point reached."""
    xy = _project(points, lat0)
    out, carried = [(xy[0][0], xy[0][1], 0)], 0.0
    for i in range(1, len(xy)):
        (x0, y0), (x1, y1) = xy[i - 1], xy[i]
        step = math.hypot(x1 - x0, y1 - y0)
        if step == 0:
            continue
        along = step_m - carried
        while along <= step:
            out.append((x0 + (x1 - x0) * along / step, y0 + (y1 - y0) * along / step, i))
            along += step_m
        carried = (carried + step) % step_m
    return out


def _grid(samples: list[tuple[float, float, int]], cell: float) -> dict:
    grid = defaultdict(list)
    for index, (x, y, _) in enumerate(samples):
        grid[(int(x // cell), int(y // cell))].append(index)
    return grid


def _nearest(x: float, y: float, samples, grid, cell: float, tolerance: float) -> int | None:
    best = None
    cx, cy = int(x // cell), int(y // cell)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for index in grid.get((cx + dx, cy + dy), ()):
                d = math.hypot(samples[index][0] - x, samples[index][1] - y)
                if d <= tolerance and (best is None or d < best[0]):
                    best = (d, index)
    return None if best is None else best[1]


def common_stretch(source: list[TrackPoint], others: list[list[TrackPoint]],
                   params: MatchParams = MatchParams()) -> tuple[int, int]:
    """Indices [start, end) into `source` of the longest stretch every other track also rides,
    in the same direction. Returns (0, 0) when there is none."""
    if len(source) < 2 or not others:
        return 0, 0
    lat0 = source[0].lat
    cell = max(params.tolerance_m, params.step_m) * 1.25
    src = _sample(source, lat0, params.step_m)
    targets = []
    for other in others:
        samples = _sample(other, lat0, params.step_m)
        targets.append((samples, _grid(samples, cell)))

    best = (0, 0, 0)  # (length in samples, first sample, last sample)
    first, missed = None, 0
    last = [None] * len(targets)
    for i, (x, y, _) in enumerate(src):
        found = [_nearest(x, y, s, g, cell, params.tolerance_m) for s, g in targets]
        matched = all(f is not None for f in found)
        forward = matched and all(l is None or 0 <= f - l <= params.max_ahead for f, l in zip(found, last))
        if forward:
            if first is None:
                first = i
            last, missed = found, 0
            if i - first + 1 > best[0]:
                best = (i - first + 1, first, i)
        elif first is not None and not matched and missed < params.max_missed:
            missed += 1
        else:
            first, missed = (i, 0) if matched else (None, 0)
            last = found if matched else [None] * len(targets)
    if best[0] < 2:
        return 0, 0
    return src[best[1]][2], src[best[2]][2] + 1


def align_to_route(route_path: list[TrackPoint], trip_path: list[TrackPoint],
                   params: MatchParams = MatchParams()) -> dict:
    """Check, from geometry alone, that a trip rides a route end to end in the route's direction.

    No timestamp is used. The result gives the stretch of the trip that lies on the route as
    indices into `trip_path`, so a later Oracle can time that stretch only and never the whole
    trip.
    """
    lat0 = route_path[0].lat
    fine = params.step_m / 4
    cell = params.tolerance_m * 1.25
    route = _sample(route_path, lat0, params.step_m)
    trip = _sample(trip_path, lat0, fine)
    grid = _grid(trip, cell)

    matched, deviations, backwards, last = [], [], 0, None
    for x, y, _ in route:
        j = _nearest(x, y, trip, grid, cell, params.tolerance_m)
        if j is None:
            continue
        if last is not None and j < last:
            backwards += 1
        last = j
        matched.append(j)
        deviations.append(math.hypot(trip[j][0] - x, trip[j][1] - y))
    if not matched:
        return {"coverage": 0.0, "same_direction": False, "trip_index_range": None}

    first, final = trip[min(matched)][2], trip[max(matched)][2]
    stretch = trip_path[first:final + 1]
    trip_m = sum(haversine_m(a.lat, a.lon, b.lat, b.lon) for a, b in zip(stretch, stretch[1:]))
    route_m = sum(haversine_m(a.lat, a.lon, b.lat, b.lon) for a, b in zip(route_path, route_path[1:]))
    deviations.sort()
    return {
        "coverage": round(len(matched) / len(route), 4),
        "same_direction": backwards <= max(1, len(matched) // 100),
        "backward_steps": backwards,
        "trip_index_range": [first, final + 1],
        "route_length_m": round(route_m, 1),
        "trip_stretch_length_m": round(trip_m, 1),
        "length_ratio": round(trip_m / route_m, 4) if route_m else None,
        "deviation_median_m": round(deviations[len(deviations) // 2], 1),
        "deviation_p95_m": round(deviations[min(int(len(deviations) * 0.95), len(deviations) - 1)], 1),
    }


def build_route(route_id: str, name: str, path: list[TrackPoint], *, source_trip_id: str,
                catalog_version: str, params: IngestParams = IngestParams()) -> tuple[dict, list[dict], list[dict]]:
    """Cut a path into route segments and return (route, route_segments, checkpoints).

    Segments use the same length target, curvature measure and category rule as ingest.
    Only the start and end checkpoints are created; fuel stations need station data (M2).
    """
    pieces: list[tuple[float, list[TrackPoint]]] = []
    length, piece = 0.0, [path[0]]
    for a, b in zip(path, path[1:]):
        length += haversine_m(a.lat, a.lon, b.lat, b.lon)
        piece.append(b)
        if length >= params.segment_m:
            pieces.append((length, piece))
            length, piece = 0.0, [b]
    if length >= params.min_last_m or not pieces:
        pieces.append((length, piece))
    elif pieces:
        last_length, last_piece = pieces[-1]
        pieces[-1] = (last_length + length, last_piece + piece[1:])

    segments, cumulative = [], 0.0
    for index, (seg_length, seg_path) in enumerate(pieces):
        category = category_of(curvature_deg_per_km(seg_path, seg_length, params.resample_m), params)
        if category is None:
            raise ValueError(f"{route_id} segment {index} cannot be classified; the catalog does not allow null")
        cumulative += round(seg_length, 1)
        segments.append({"route_id": route_id, "seg_index": index, "length_m": round(seg_length, 1),
                         "cum_length_m": round(cumulative, 1), "seg_category": category,
                         "end_lat": round(seg_path[-1].lat, 6), "end_lon": round(seg_path[-1].lon, 6)})
    route = {"route_id": route_id, "name": name, "n_segments": len(segments),
             "total_length_m": segments[-1]["cum_length_m"], "source_trip_id": source_trip_id,
             "category_scheme": params.category_scheme, "catalog_version": catalog_version}
    checkpoints = [
        {"checkpoint_id": f"{route_id}-CP01", "route_id": route_id, "kind": "start", "after_seg_count": 0,
         "name": None, "station_ref": None},
        {"checkpoint_id": f"{route_id}-CP02", "route_id": route_id, "kind": "end", "after_seg_count": len(segments),
         "name": None, "station_ref": None},
    ]
    return route, segments, checkpoints
