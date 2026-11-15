"""CR-01 technical checks D5 and C2: shared loading and helpers (pace trips only).

Rules this module enforces (CR-01 D5 ruling):
  * Only trips listed under `pace` in data/private/cr01/holdout_designation.json are opened.
    The filter is applied on trip id BEFORE any GPX file is touched; holdout and excluded trips
    are never read, not even to count something.
  * Nothing here prints. Callers print aggregates only, through `mask` / `mask_partition`, so a
    group of fewer than 3 trips is never shown as a number.
  * Fully local, no network. Nothing is tuned here; thresholds follow the spike's fixed rule.

Not E1 and not E2.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from moto_copilot.ingest import IngestParams, TripReport, build_rows, haversine_m, read_gpx  # noqa: E402
from moto_copilot.ingest.segments import clean_points, trim_ends  # noqa: E402

DESIGNATION = ROOT / "data" / "private" / "cr01" / "holdout_designation.json"
MANIFEST = ROOT / "data" / "private" / "m1b" / "trip_manifest.json"
GPX_DIR = ROOT / "data" / "bmw"
OUT_DIR = ROOT / "data" / "private" / "cr01"

MIN_SEGMENTS = 30          # same as the M1-B spike: a category needs this many ok segments for a pace
MIN_TRIPS = 3
SHORT_STOP_S = 180.0       # a stop shorter than this is a "short stop"
SMALL = 3                  # groups of fewer trips than this are never shown as a number


# ---------------------------------------------------------------- disclosure control
def mask(k: int, n: int | None = None) -> str:
    """A trip count that is safe to show. Fewer than 3 -> '<3'. When the total n is known and the
    complement would be fewer than 3, show '>=n-2' so the complement cannot be worked out."""
    if k < SMALL:
        return "<3"
    if n is not None and n - k < SMALL:
        return f">={n - SMALL + 1}"
    return str(k)


def mask_partition(counts: list[int]) -> list[str]:
    """Trip counts of buckets that add up to a known total. Cells under 3 are shown as '<3'. If the
    hidden cells could still be worked out from the total, the smallest shown cell is withheld too."""
    hidden = [i for i, c in enumerate(counts) if c < SMALL]
    hidden_sum = sum(counts[i] for i in hidden)
    solvable = hidden_sum > 0 and (len(hidden) == 1 or hidden_sum == 2 * len(hidden))
    out = [("<3" if i in hidden else str(c)) for i, c in enumerate(counts)]
    if solvable:
        shown = [i for i in range(len(counts)) if i not in hidden]
        if shown:
            out[min(shown, key=lambda i: counts[i])] = "withheld"
    return out


# ---------------------------------------------------------------- loading (pace only)
def load_pace_points() -> dict[str, list]:
    """trip_id -> raw track points, for pace trips only. Other trips' files are never opened."""
    designation = json.loads(DESIGNATION.read_text(encoding="utf-8"))
    pace = set(designation["pace"])
    forbidden = set(designation["holdout"]) | set(designation["excluded_pending_ruling"])
    if pace & forbidden:
        raise RuntimeError("designation is inconsistent: a trip is both pace and holdout/excluded")
    trips = json.loads(MANIFEST.read_text(encoding="utf-8"))["trips"]
    wanted = [t for t in trips if t["trip_id"] in pace and t["trip_id"] not in forbidden]
    if len(wanted) != len(pace):
        raise RuntimeError("a pace trip has no entry in the import manifest")
    points = {}
    for trip in sorted(wanted, key=lambda t: t["trip_id"]):
        points[trip["trip_id"]] = read_gpx(GPX_DIR / trip["source_file"])[0]
    return points


def ingest(points: dict[str, list], params: IngestParams) -> tuple[dict[str, list[dict]], dict[str, TripReport]]:
    rows, reports = {}, {}
    for trip_id, pts in points.items():
        rows[trip_id], reports[trip_id] = build_rows(pts, trip_id=trip_id, trip_role="pace", route_id=None,
                                                     params=params)
    return rows, reports


def tercile_thresholds(rows: list[dict]) -> tuple[float, float, int]:
    """The spike's rule (experiments/m1b_spike/run_m1b.py): terciles of curvature over ok rows,
    rounded to the nearest 5 deg/km. Returns (c1_max, c2_max, n_rows_used)."""
    curvature = sorted(r["curvature_deg_per_km"] for r in rows
                       if r["quality"] == "ok" and r["curvature_deg_per_km"] is not None)
    c1_max = float(round(curvature[len(curvature) // 3] / 5) * 5)
    c2_max = float(round(curvature[2 * len(curvature) // 3] / 5) * 5)
    return c1_max, c2_max, len(curvature)


def usable(row: dict) -> bool:
    """A segment that may be timed: ok quality, has a category and a moving time."""
    return row["quality"] == "ok" and row["seg_category"] is not None and row["moving_time_s"] is not None


def speed_kmh(row: dict) -> float:
    return row["length_m"] / row["moving_time_s"] * 3.6


# ---------------------------------------------------------------- stops
def segment_stops(points: list, params: IngestParams) -> tuple[list[list[float]], float]:
    """Stop events per segment, and the elapsed time of the trimmed track in seconds.

    Mirrors the step rules and the segment cutting of ingest.build_rows (same cleaning, trimming,
    stop speed, gap rules, segment length, tail merge), so index i here is seg_index i there.
    A stop event is a maximal run of consecutive stopped steps; its duration is the sum of them.
    A segment only closes on a moving step, so a stop event never spans two segments.
    """
    kept, _ = clean_points(points, params, TripReport())
    start, end = trim_ends(kept, params.trim_m)
    pts = kept[start:end]
    if len(pts) < 2:
        return [], 0.0
    segs: list[dict] = []
    current = {"length": 0.0, "stops": []}
    run = 0.0
    for a, b in zip(pts, pts[1:]):
        step_s = (b.time - a.time).total_seconds()
        step_m = haversine_m(a.lat, a.lon, b.lat, b.lon)
        if step_s > params.gap_s:
            stopped = step_m < params.gap_move_m
        else:
            stopped = step_m / step_s * 3.6 < params.stop_kmh
        if stopped:
            run += step_s
        else:
            if run > 0:
                current["stops"].append(run)
                run = 0.0
            current["length"] += step_m
        if current["length"] >= params.segment_m:
            segs.append(current)
            current = {"length": 0.0, "stops": []}
    if run > 0:
        current["stops"].append(run)
    if current["length"] >= params.min_last_m or (current["length"] > 0 and not segs):
        segs.append(current)
    elif segs:
        segs[-1]["stops"].extend(current["stops"])
    elapsed = (pts[-1].time - pts[0].time).total_seconds()
    return [s["stops"] for s in segs], elapsed


def check_stops_match(stops: list[list[float]], rows: list[dict]) -> bool:
    """The mirror must give the same segments and the same stopped time as build_rows."""
    if len(stops) != len(rows):
        return False
    return all(abs(sum(s) - r["stopped_time_s"]) <= 0.11 for s, r in zip(stops, rows))


# ---------------------------------------------------------------- small statistics
def mean(values: list[float]) -> float:
    return statistics.fmean(values)


def pct(x: float) -> float:
    return round(100.0 * x, 1)


def planar(points: list) -> list[tuple[float, float]]:
    """Local x/y in metres around the first point (good enough for 100 m comparisons)."""
    lat0, lon0 = points[0].lat, points[0].lon
    k = 6_371_000.0 * math.cos(math.radians(lat0))
    return [(k * math.radians(p.lon - lon0), 6_371_000.0 * math.radians(p.lat - lat0)) for p in points]
