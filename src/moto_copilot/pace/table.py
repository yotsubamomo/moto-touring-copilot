"""Pace Table and ETA Output (data contract v0.2, contracts 3 and 4).

Pre-Spec Technical Spike (M1-B). The pace is a per-category speed taken from the rider's own
pace trips. `eta_safe` is the typical estimate plus a safety margin; it is not a P90 and carries
no coverage guarantee (DESIGN.md §6.1).
"""
from __future__ import annotations

import datetime as dt
import statistics
from collections import defaultdict

from ..contracts import expected_break_times, pace_eligible
from ..contracts.schemas import CATEGORIES

TAIPEI = dt.timezone(dt.timedelta(hours=8))
METHOD = "median_unweighted"


def _iso(moment: dt.datetime) -> str:
    """Nearest second, +08:00."""
    return (moment + dt.timedelta(milliseconds=500)).astimezone(TAIPEI).replace(microsecond=0).isoformat()


def _eligible_by_category(rows: list[dict], trip_ids: list[str]) -> dict[str, list[dict]]:
    roles = {r["trip_id"]: r["trip_role"] for r in rows}
    for trip_id in trip_ids:
        if roles.get(trip_id) != "pace":
            raise ValueError(f"{trip_id} is not a pace trip; holdout trips must not enter the pace table")
    wanted = set(trip_ids)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row["trip_id"] in wanted and pace_eligible(row):
            grouped[row["seg_category"]].append(row)
    return grouped


def _speed_kmh(row: dict) -> float:
    return row["length_m"] / row["moving_time_s"] * 3.6


def build_pace_table(rows: list[dict], trip_ids: list[str], *, pace_version: str, min_segments: int,
                     built_at: dt.datetime) -> tuple[dict, list[dict]]:
    """Unweighted median of segment speed per category, from eligible rows of the given pace trips."""
    grouped = _eligible_by_category(rows, trip_ids)
    versions = {r["ingest_version"] for r in rows}
    schemes = {r["category_scheme"] for r in rows}
    if len(versions) != 1 or len(schemes) != 1:
        raise ValueError("the derived segment table must have one ingest_version and one category_scheme")
    header = {"pace_version": pace_version, "method": METHOD, "category_scheme": schemes.pop(),
              "ingest_version": versions.pop(), "min_segments": min_segments, "n_trips": len(trip_ids),
              "trip_ids": sorted(trip_ids), "built_at": _iso(built_at)}
    categories = []
    for category in CATEGORIES:
        segs = grouped.get(category, [])
        speed = round(statistics.median(_speed_kmh(r) for r in segs), 2) if len(segs) >= min_segments else None
        categories.append({"pace_version": pace_version, "seg_category": category, "speed_kmh": speed,
                           "n_segments": len(segs)})
    return header, categories


def compare_methods(rows: list[dict], trip_ids: list[str]) -> dict[str, dict]:
    """Unweighted against length-weighted median, on pace trips only (DC-10). For choosing a
    method before the formal E1 run; holdout trips are rejected like in build_pace_table."""
    out = {}
    for category, segs in _eligible_by_category(rows, trip_ids).items():
        ordered = sorted(segs, key=_speed_kmh)
        half, running, weighted = sum(r["length_m"] for r in ordered) / 2, 0.0, None
        for r in ordered:
            running += r["length_m"]
            if running >= half:
                weighted = _speed_kmh(r)
                break
        out[category] = {"n_segments": len(segs),
                         "median_unweighted": round(statistics.median(_speed_kmh(r) for r in segs), 2),
                         "median_length_weighted": round(weighted, 2)}
    return out


def compute_eta(route: dict, route_segments: list[dict], checkpoints: list[dict], pace_header: dict,
                pace_categories: list[dict], *, plan_id: str, departure_time: dt.datetime, margin_coeff: float,
                breaks: list[dict], computed_at: dt.datetime) -> tuple[dict, list[dict]]:
    """ETA for one departure on one route. If any segment's category has no pace the status is
    `unknown` and no time is produced, not even a partial one."""
    if departure_time.tzinfo is None:
        raise ValueError("departure_time must be timezone-aware")
    segs = sorted((s for s in route_segments if s["route_id"] == route["route_id"]), key=lambda s: s["seg_index"])
    cps = [c for c in checkpoints if c["route_id"] == route["route_id"]]
    speed = {c["seg_category"]: c["speed_kmh"] for c in pace_categories}
    missing = sorted({s["seg_category"] for s in segs if speed.get(s["seg_category"]) is None})
    break_times = expected_break_times(route["n_segments"], breaks, cps)

    header = {"plan_id": plan_id, "route_id": route["route_id"], "departure_time": _iso(departure_time),
              "status": "unknown" if missing else "ok",
              "unknown_reason": f"no pace for category {', '.join(missing)}" if missing else None,
              "margin_coeff": margin_coeff, "breaks": breaks, "pace_version": pace_header["pace_version"],
              "catalog_version": route["catalog_version"], "computed_at": _iso(computed_at)}
    rows, cumulative = [], 0.0
    for seg, break_time in zip(segs, break_times):
        row = {"plan_id": plan_id, "seg_index": seg["seg_index"], "typ_seg_time_s": None,
               "break_time_s": break_time, "eta_typ": None, "eta_safe": None}
        if not missing:
            typical = round(seg["length_m"] / (speed[seg["seg_category"]] / 3.6), 3)
            cumulative += typical
            arrival = departure_time + dt.timedelta(seconds=cumulative + break_time)
            row.update(typ_seg_time_s=typical, eta_typ=_iso(arrival),
                       eta_safe=_iso(arrival + dt.timedelta(seconds=margin_coeff * cumulative)))
        rows.append(row)
    return header, rows
