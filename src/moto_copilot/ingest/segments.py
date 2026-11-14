"""GPX track -> Derived Segment Table rows (data contract v0.2, contract 1).

Pre-Spec Technical Spike (M1-A). Every threshold lives in IngestParams and is provisional; the
values are identified by `ingest_version` and `category_scheme` in the output.

Pipeline: drop unusable points -> drop GPS jumps -> trim both ends -> split time into moving and
stopped -> cut into segments by distance -> curvature -> category.
"""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field

EARTH_RADIUS_M = 6_371_000.0
TAIPEI = dt.timezone(dt.timedelta(hours=8))


@dataclass(frozen=True)
class IngestParams:
    trim_m: float = 2000.0          # removed from each end (home and workplace privacy)
    min_trip_m: float = 1000.0      # a trip shorter than this after trimming gives no rows
    max_speed_kmh: float = 200.0    # a step faster than this is checked as a possible GPS jump
    jitter_ratio: float = 1.6       # a fast step is timing jitter if the two-step speed stays within
    jitter_slack_kmh: float = 20.0  # jitter_ratio x recent speed + this slack (and within max_speed_kmh)
    recent_steps: int = 5           # steps used for the recent speed
    gap_s: float = 10.0             # a longer step between points is a recording gap
    gap_move_m: float = 50.0        # a gap that covers more than this was ridden, not a stop
    stop_kmh: float = 3.0           # slower than this counts as stopped
    segment_m: float = 1000.0       # target segment length
    min_last_m: float = 300.0       # a shorter tail is merged into the previous segment
    resample_m: float = 20.0        # spacing used to measure heading changes
    c1_max_deg_per_km: float = 80.0   # C1 below this
    c2_max_deg_per_km: float = 250.0  # C2 below this, C3 from here on
    ingest_version: str = "ingest-spike-0.2"

    @property
    def category_scheme(self) -> str:
        return f"curv-spike0-{self.c1_max_deg_per_km:g}-{self.c2_max_deg_per_km:g}"


@dataclass(frozen=True)
class TrackPoint:
    lat: float
    lon: float
    time: dt.datetime  # timezone-aware


@dataclass
class TripReport:
    """Counts only. No coordinate and no timestamp is kept here."""
    points_read: int = 0
    dropped_no_time: int = 0
    dropped_non_increasing_time: int = 0
    dropped_jumps: int = 0
    timing_jitter_steps: int = 0
    points_after_trim: int = 0
    trimmed_length_m: float = 0.0
    segments: int = 0
    quality: dict = field(default_factory=lambda: {"ok": 0, "suspect": 0, "invalid": 0})
    categories: dict = field(default_factory=lambda: {"C1": 0, "C2": 0, "C3": 0, "null": 0})
    note: str | None = None


def haversine_m(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b_lon - a_lon) / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(h))


def _dist(a: TrackPoint, b: TrackPoint) -> float:
    return haversine_m(a.lat, a.lon, b.lat, b.lon)


def clean_points(points: list[TrackPoint], params: IngestParams, report: TripReport) -> tuple[list[TrackPoint], set[int]]:
    """Drop points whose time does not increase and points that imply an impossible speed.

    Timestamps are whole seconds, so at speed one step can look twice as long as its neighbours
    although the position is right. Such a step is kept (timing jitter) when the speed over the
    last two steps is still plausible next to the recent speed; otherwise the point is a GPS jump.

    Returns the kept points and the indices (into the kept list) of points that follow a dropped
    jump, so the segment containing that step can be marked suspect.
    """
    kept: list[TrackPoint] = []
    after_jump: set[int] = set()
    pending_jump = False
    for p in points:
        if not kept:
            kept.append(p)
            continue
        step_s = (p.time - kept[-1].time).total_seconds()
        if step_s <= 0:
            report.dropped_non_increasing_time += 1
            continue
        if _dist(kept[-1], p) / step_s * 3.6 > params.max_speed_kmh:
            is_jitter = False
            if len(kept) >= 2:
                two_s = (p.time - kept[-2].time).total_seconds()
                two_kmh = (_dist(kept[-2], kept[-1]) + _dist(kept[-1], p)) / two_s * 3.6
                recent = kept[-(params.recent_steps + 1):]
                recent_s = (recent[-1].time - recent[0].time).total_seconds()
                recent_kmh = sum(_dist(a, b) for a, b in zip(recent, recent[1:])) / recent_s * 3.6
                is_jitter = (two_kmh <= params.max_speed_kmh
                             and two_kmh <= params.jitter_ratio * recent_kmh + params.jitter_slack_kmh)
            if is_jitter:
                report.timing_jitter_steps += 1
            else:
                report.dropped_jumps += 1
                pending_jump = True
                continue
        if pending_jump:
            after_jump.add(len(kept))
            pending_jump = False
        kept.append(p)
    return kept, after_jump


def trim_ends(points: list[TrackPoint], trim_m: float) -> tuple[int, int]:
    """Indices [start, end) of the points left after removing trim_m of path from each end."""
    cumulative = [0.0]
    for a, b in zip(points, points[1:]):
        cumulative.append(cumulative[-1] + _dist(a, b))
    total = cumulative[-1] if points else 0.0
    start = next((i for i, c in enumerate(cumulative) if c >= trim_m), len(points))
    end = next((i for i in range(len(points) - 1, -1, -1) if total - cumulative[i] >= trim_m), -1) + 1
    return (start, end) if end > start else (0, 0)


def moving_path(points: list[TrackPoint], params: IngestParams = IngestParams()) -> list[TrackPoint]:
    """The cleaned, trimmed track with the points recorded while standing still left out.

    This is the private trimmed track that `routes` builds route geometry from (DC-5). It uses the
    same rules as build_rows, so a route segment and a trip segment over the same road get the
    same kind of path.
    """
    kept, _ = clean_points(points, params, TripReport())
    start, end = trim_ends(kept, params.trim_m)
    pts = kept[start:end]
    if len(pts) < 2:
        return []
    path = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        step_s, step_m = (b.time - a.time).total_seconds(), _dist(a, b)
        if step_s > params.gap_s:
            if step_m >= params.gap_move_m:
                path.append(b)
        elif step_m / step_s * 3.6 >= params.stop_kmh:
            path.append(b)
    return path


def curvature_deg_per_km(path: list[TrackPoint], length_m: float, spacing_m: float) -> float | None:
    """Public name of the curvature measure, shared with `routes`."""
    return _curvature_deg_per_km(path, length_m, spacing_m)


def category_of(curvature: float | None, params: IngestParams) -> str | None:
    """Public name of the category rule, shared with `routes`."""
    return _category(curvature, params)


def _curvature_deg_per_km(path: list[TrackPoint], length_m: float, spacing_m: float) -> float | None:
    """Sum of absolute heading changes along the path, per kilometre.

    The path is resampled at a fixed spacing first, so GPS jitter between 1 Hz points does not
    count as turning.
    """
    if len(path) < 2 or length_m <= 0:
        return None
    lat0 = math.radians(path[0].lat)
    xy = [(EARTH_RADIUS_M * math.radians(p.lon - path[0].lon) * math.cos(lat0),
           EARTH_RADIUS_M * math.radians(p.lat - path[0].lat)) for p in path]
    samples, carried = [xy[0]], 0.0
    for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
        step = math.hypot(x1 - x0, y1 - y0)
        if step == 0:
            continue
        along = spacing_m - carried
        while along <= step:
            samples.append((x0 + (x1 - x0) * along / step, y0 + (y1 - y0) * along / step))
            along += spacing_m
        carried = (carried + step) % spacing_m
    if len(samples) < 3:
        return None
    headings = [math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) for a, b in zip(samples, samples[1:])]
    turned = sum(abs((h1 - h0 + 180) % 360 - 180) for h0, h1 in zip(headings, headings[1:]))
    return turned / (length_m / 1000.0)


def _category(curvature: float | None, params: IngestParams) -> str | None:
    if curvature is None:
        return None
    if curvature < params.c1_max_deg_per_km:
        return "C1"
    return "C2" if curvature < params.c2_max_deg_per_km else "C3"


def build_rows(points: list[TrackPoint], *, trip_id: str, trip_role: str, route_id: str | None,
               params: IngestParams = IngestParams()) -> tuple[list[dict], TripReport]:
    """Return the private rows (with start_time) of one trip and a count-only report."""
    report = TripReport(points_read=len(points))
    kept, after_jump = clean_points(points, params, report)
    start, end = trim_ends(kept, params.trim_m)
    pts = kept[start:end]
    after_jump = {i - start for i in after_jump if start < i < end}
    report.points_after_trim = len(pts)
    if len(pts) < 2:
        report.note = "nothing left after trimming both ends"
        return [], report

    # Split every step into moving or stopped, and close a segment when it has enough distance.
    raw: list[dict] = []
    current = {"first": 0, "length": 0.0, "moving": 0.0, "stopped": 0.0, "suspect": False, "path": [pts[0]]}
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        step_s, step_m = (b.time - a.time).total_seconds(), _dist(a, b)
        if i in after_jump:
            current["suspect"] = True
        if step_s > params.gap_s:
            if step_m < params.gap_move_m:
                current["stopped"] += step_s           # paused while standing still
            else:
                current["moving"] += step_s            # ridden without a recording
                current["length"] += step_m
                current["suspect"] = True
                current["path"].append(b)
        elif step_m / step_s * 3.6 < params.stop_kmh:
            current["stopped"] += step_s
        else:
            current["moving"] += step_s
            current["length"] += step_m
            current["path"].append(b)
        if current["length"] >= params.segment_m:
            raw.append(current)
            current = {"first": i, "length": 0.0, "moving": 0.0, "stopped": 0.0, "suspect": False, "path": [b]}
    if current["length"] >= params.min_last_m or (current["length"] > 0 and not raw):
        raw.append(current)
    elif raw:  # short tail: merge into the previous segment
        last = raw[-1]
        for key in ("length", "moving", "stopped"):
            last[key] += current[key]
        last["suspect"] = last["suspect"] or current["suspect"]
        last["path"].extend(current["path"][1:])

    report.trimmed_length_m = round(sum(s["length"] for s in raw), 1)
    if report.trimmed_length_m < params.min_trip_m:
        report.note = "trip is too short after trimming"
        return [], report

    rows = []
    for index, seg in enumerate(raw):
        valid = seg["moving"] > 0 and seg["length"] > 0
        curvature = _curvature_deg_per_km(seg["path"], seg["length"], params.resample_m) if valid else None
        category = _category(curvature, params)
        quality = "invalid" if not valid else ("suspect" if seg["suspect"] else "ok")
        report.quality[quality] += 1
        report.categories[category or "null"] += 1
        rows.append({
            "trip_id": trip_id,
            "seg_index": index,
            "trip_role": trip_role,
            "route_id": route_id,
            "start_time": pts[seg["first"]].time.astimezone(TAIPEI).isoformat(timespec="seconds"),
            "length_m": round(seg["length"], 1),
            "moving_time_s": round(seg["moving"], 1) if valid else None,
            "stopped_time_s": round(seg["stopped"], 1),
            "curvature_deg_per_km": round(curvature, 1) if curvature is not None else None,
            "seg_category": category,
            "quality": quality,
            "category_scheme": params.category_scheme,
            "ingest_version": params.ingest_version,
        })
    report.segments = len(rows)
    return rows, report


def to_public(private_rows: list[dict]) -> list[dict]:
    """The public version: the same rows without start_time (DC-9)."""
    return [{k: v for k, v in row.items() if k != "start_time"} for row in private_rows]
