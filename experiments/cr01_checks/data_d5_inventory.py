"""CR-01 check D5: aggregate inventory of the pace trips. Not E1, not E2.

    .venv/Scripts/python.exe experiments/cr01_checks/data_d5_inventory.py

Prints and writes aggregates only (counts, sums, medians, percentages, buckets). No coordinate,
no timestamp, no per-trip value, no trip id, no file name. Trip groups under 3 are shown as '<3'.
Holdout and excluded trips are never opened (see data_common.load_pace_points).

Definitions fixed before the run:
  * round trip: first and last raw track point within 3 km of each other; otherwise one-way.
  * out-and-back test (round trips only): cleaned track resampled every 25 m; the turnaround is
    the sample farthest (straight line) from the first point; a return sample "overlaps" if any
    outbound sample lies within 100 m. Out-and-back if >= 60% of return samples overlap, else loop.
  * one-way pairing (supplementary): a one-way trip is "paired" if another one-way pace trip starts
    within 3 km of its end and ends within 3 km of its start.
  * same-day leg chain (supplementary): pace trips that start on the same local calendar day,
    in start order; "chained" if each leg starts within 3 km of the previous leg's end; a
    "closed day" if the last leg also ends within 3 km of the first leg's start. The dates are
    used only to group; none is printed. Legs that are holdout or excluded trips are not visible.
  * stop event: maximal run of consecutive stopped steps of the trimmed track (ingest rules);
    short stop < 180 s. A sensitivity figure merges stop events separated by <= 5 s of movement.
  * micro-stop diagnostic: a stop event of at most 2 s whose neighbouring moving steps are both
    faster than 20 km/h cannot be a real stop; it is reported as a likely recording artefact.
"""
from __future__ import annotations

import json
import statistics
import sys

from data_common import (MIN_SEGMENTS, MIN_TRIPS, OUT_DIR, SHORT_STOP_S, IngestParams, TripReport, check_stops_match,
                         clean_points, haversine_m, ingest, load_pace_points, mask, mask_partition, pct, planar,
                         segment_stops, tercile_thresholds, usable)

CLOSE_M = 3000.0
RESAMPLE_M = 25.0
NEAR_M = 100.0
OUT_AND_BACK_SHARE = 0.60
LENGTH_BUCKETS_KM = [50, 100, 200, 300]
LENGTH_LABELS = ["<50", "50-100", "100-200", "200-300", ">300"]
OVERLAP_LABELS = ["<20%", "20-60%", "60-90%", ">=90%"]


def resample(xy: list[tuple[float, float]], spacing: float) -> list[tuple[float, float]]:
    out, carried = [xy[0]], 0.0
    for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
        step = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        if step == 0:
            continue
        along = spacing - carried
        while along <= step:
            out.append((x0 + (x1 - x0) * along / step, y0 + (y1 - y0) * along / step))
            along += spacing
        carried = (carried + step) % spacing
    return out


def return_overlap_share(points: list, params: IngestParams) -> float | None:
    kept, _ = clean_points(points, params, TripReport())
    if len(kept) < 2:
        return None
    samples = resample(planar(kept), RESAMPLE_M)
    if len(samples) < 10:
        return None
    turn = max(range(len(samples)), key=lambda i: samples[i][0] ** 2 + samples[i][1] ** 2)
    outbound, back = samples[:turn + 1], samples[turn + 1:]
    if not back:
        return None
    grid: dict[tuple[int, int], list[tuple[float, float]]] = {}
    for x, y in outbound:
        grid.setdefault((int(x // NEAR_M), int(y // NEAR_M)), []).append((x, y))
    near = 0
    for x, y in back:
        cx, cy = int(x // NEAR_M), int(y // NEAR_M)
        if any((x - ox) ** 2 + (y - oy) ** 2 <= NEAR_M ** 2
               for dx in (-1, 0, 1) for dy in (-1, 0, 1) for ox, oy in grid.get((cx + dx, cy + dy), ())):
            near += 1
    return near / len(back)


def merged_stops(points: list, params: IngestParams, bridge_s: float = 5.0) -> list[float]:
    """Sensitivity only: stop events of the trimmed track, joining events split by <= bridge_s of movement."""
    from data_common import trim_ends
    kept, _ = clean_points(points, params, TripReport())
    start, end = trim_ends(kept, params.trim_m)
    pts = kept[start:end]
    events, run, moving_since = [], 0.0, None
    for a, b in zip(pts, pts[1:]):
        step_s = (b.time - a.time).total_seconds()
        step_m = haversine_m(a.lat, a.lon, b.lat, b.lon)
        stopped = step_m < params.gap_move_m if step_s > params.gap_s else step_m / step_s * 3.6 < params.stop_kmh
        if stopped:
            if moving_since is not None and moving_since > bridge_s and run > 0:
                events.append(run)
                run = 0.0
            run += step_s
            moving_since = 0.0
        elif moving_since is not None:
            moving_since += step_s
    if run > 0:
        events.append(run)
    return events

STOP_BUCKETS_S = [1.5, 5.5, 30.0, SHORT_STOP_S]
STOP_LABELS = ["1 s", "2-5 s", "6-30 s", "30-180 s", ">=180 s"]
FAST_KMH = 20.0


def stop_event_profile(points: list, params: IngestParams) -> tuple[list[list[float]], list[float]]:
    """Per duration bucket [events, seconds], and [events, seconds] of stop events <= 2 s that sit
    between two moving steps faster than FAST_KMH (likely repeated-position artefacts)."""
    from data_common import trim_ends
    kept, _ = clean_points(points, params, TripReport())
    start, end = trim_ends(kept, params.trim_m)
    pts = kept[start:end]
    steps = []
    for a, b in zip(pts, pts[1:]):
        step_s = (b.time - a.time).total_seconds()
        step_m = haversine_m(a.lat, a.lon, b.lat, b.lon)
        stopped = step_m < params.gap_move_m if step_s > params.gap_s else step_m / step_s * 3.6 < params.stop_kmh
        steps.append((stopped, step_s, step_m / step_s * 3.6))
    buckets = [[0, 0.0] for _ in STOP_LABELS]
    artefact = [0, 0.0]
    i = 0
    while i < len(steps):
        if not steps[i][0]:
            i += 1
            continue
        j = i
        while j < len(steps) and steps[j][0]:
            j += 1
        duration = sum(s[1] for s in steps[i:j])
        bucket = buckets[sum(duration >= edge for edge in STOP_BUCKETS_S)]
        bucket[0] += 1
        bucket[1] += duration
        if duration <= 2.0 and i > 0 and j < len(steps) and steps[i - 1][2] > FAST_KMH and steps[j][2] > FAST_KMH:
            artefact[0] += 1
            artefact[1] += duration
        i = j
    return buckets, artefact


def day_chains(points: dict[str, list]) -> dict:
    """Supplementary: legs recorded as separate files on one day that together close a round trip."""
    import datetime as dt
    taipei = dt.timezone(dt.timedelta(hours=8))
    days: dict = {}
    for t, pts in points.items():
        days.setdefault(pts[0].time.astimezone(taipei).date(), []).append(t)
    multi = [sorted(legs, key=lambda t: points[t][0].time) for legs in days.values() if len(legs) >= 2]
    near = lambda p, q: haversine_m(p.lat, p.lon, q.lat, q.lon) <= CLOSE_M
    closed_days, closed_trips, shares = 0, 0, []
    for legs in multi:
        chained = all(near(points[a][-1], points[b][0]) for a, b in zip(legs, legs[1:]))
        if chained and near(points[legs[-1]][-1], points[legs[0]][0]):
            closed_days += 1
            closed_trips += len(legs)
            share = return_overlap_share([p for t in legs for p in points[t]], IngestParams())
            if share is not None:
                shares.append(share)
    out_and_back = sum(s >= OUT_AND_BACK_SHARE for s in shares)
    return {"days_with_2plus_legs": mask(len(multi)), "trips_on_those_days": mask(sum(len(m) for m in multi), len(points)),
            "closed_days": mask(closed_days), "trips_in_closed_days": mask(closed_trips, len(points)),
            "closed_days_out_and_back": mask(out_and_back, len(shares)) if len(shares) >= 3 else "withheld",
            "closed_days_loop": mask(len(shares) - out_and_back, len(shares)) if len(shares) >= 3 else "withheld",
            "closed_days_return_overlap_median_pct": pct(statistics.median(shares)) if len(shares) >= 3 else "withheld"}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    points = load_pace_points()
    n = len(points)
    base_rows, _ = ingest(points, IngestParams())
    c1_max, c2_max, n_curv = tercile_thresholds([r for rows in base_rows.values() for r in rows])
    params = IngestParams(c1_max_deg_per_km=c1_max, c2_max_deg_per_km=c2_max)
    rows, reports = ingest(points, params)
    out: dict = {"label": "CR-01 technical check D5, pace trips only; not an E1 result",
                 "trips_loaded": n, "thresholds_deg_per_km": {"c1_max": c1_max, "c2_max": c2_max, "n_ok_rows": n_curv}}

    # ---- lengths
    with_rows = [t for t in points if rows[t]]
    km = [reports[t].trimmed_length_m / 1000 for t in with_rows]
    buckets = [0] * 5
    for value in km:
        buckets[sum(value >= edge for edge in LENGTH_BUCKETS_KM)] += 1
    out["trips_with_usable_segments"] = mask(len(with_rows), n)
    out["trimmed_km_total"] = round(sum(km), 0)
    out["trimmed_km_median"] = round(statistics.median(km), 0) if len(km) >= 3 else "withheld"
    out["trimmed_km_buckets"] = dict(zip(LENGTH_LABELS, mask_partition(buckets)))

    # ---- round trip / one-way
    closed, one_way, shares = [], [], []
    for t, pts in points.items():
        gap = haversine_m(pts[0].lat, pts[0].lon, pts[-1].lat, pts[-1].lon)
        (closed if gap <= CLOSE_M else one_way).append(t)
    for t in closed:
        shares.append(return_overlap_share(points[t], params))
    known = [s for s in shares if s is not None]
    out_and_back = sum(s >= OUT_AND_BACK_SHARE for s in known)
    overlap_buckets = [0] * 4
    for s in known:
        overlap_buckets[sum(s >= edge for edge in (0.2, 0.6, 0.9))] += 1
    paired = 0
    for t in one_way:
        a = points[t]
        for u in one_way:
            b = points[u]
            if u != t and haversine_m(a[-1].lat, a[-1].lon, b[0].lat, b[0].lon) <= CLOSE_M \
                    and haversine_m(a[0].lat, a[0].lon, b[-1].lat, b[-1].lon) <= CLOSE_M:
                paired += 1
                break
    out["round_trips"] = mask(len(closed), n)
    out["one_way"] = mask(len(one_way), n)
    out["round_trips_out_and_back"] = mask(out_and_back, len(known))
    out["round_trips_loop"] = mask(len(known) - out_and_back, len(known))
    out["round_trips_untestable"] = mask(len(shares) - len(known))
    out["round_trip_return_overlap_buckets"] = dict(zip(OVERLAP_LABELS, mask_partition(overlap_buckets)))
    out["round_trip_return_overlap_median_pct"] = pct(statistics.median(known)) if len(known) >= 3 else "withheld"
    out["one_way_paired_with_reverse_trip"] = mask(paired, len(one_way)) if len(one_way) >= 3 else "withheld"
    out["same_day_leg_chains"] = day_chains(points)

    # ---- segments by quality and category
    all_rows = [r for t in points for r in rows[t]]
    quality = {q: sum(r["quality"] == q for r in all_rows) for q in ("ok", "suspect", "invalid")}
    out["segments_total"] = len(all_rows)
    out["segments_by_quality"] = quality
    out["km_by_quality"] = {q: round(sum(r["length_m"] for r in all_rows if r["quality"] == q) / 1000, 0)
                            for q in ("ok", "suspect", "invalid")}
    ok = [r for r in all_rows if usable(r)]
    ok_km = sum(r["length_m"] for r in ok) / 1000
    cats = {}
    for c in ("C1", "C2", "C3"):
        segs = [r for r in ok if r["seg_category"] == c]
        n_trips = len({r["trip_id"] for r in segs})
        if n_trips < MIN_TRIPS:
            cats[c] = {"trips": "<3", "ok_segments": "withheld", "km": "withheld", "km_share_pct": "withheld",
                       "sufficient": False}
        else:
            c_km = sum(r["length_m"] for r in segs) / 1000
            cats[c] = {"trips": mask(n_trips, n), "ok_segments": len(segs), "km": round(c_km, 0),
                       "km_share_pct": pct(c_km / ok_km),
                       "sufficient": len(segs) >= MIN_SEGMENTS and n_trips >= MIN_TRIPS}
    out["ok_by_category"] = cats
    out["sufficiency_rule"] = f">= {MIN_SEGMENTS} ok segments from >= {MIN_TRIPS} trips"
    c1_km = sum(r["length_m"] for r in ok if r["seg_category"] == "C1") / 1000
    out["ok_km_share_pct"] = {"C1": pct(c1_km / ok_km), "C2+C3": pct(1 - c1_km / ok_km)}
    # Supplementary: how the C1 share varies between trips (bucketed, so no single trip is described).
    per_trip = []
    for t in with_rows:
        t_ok = [r for r in rows[t] if usable(r)]
        if t_ok:
            per_trip.append(sum(r["length_m"] for r in t_ok if r["seg_category"] == "C1") / sum(r["length_m"] for r in t_ok))
    share_buckets = [0] * 4
    for value in per_trip:
        share_buckets[sum(value >= edge for edge in (0.2, 0.4, 0.6))] += 1
    out["per_trip_c1_km_share"] = {
        "median_pct": pct(statistics.median(per_trip)) if len(per_trip) >= 3 else "withheld",
        "buckets": dict(zip(["<20%", "20-40%", "40-60%", ">=60%"], mask_partition(share_buckets)))}
    # Supplementary: the same split at the code's provisional default thresholds (not tuned here).
    default = IngestParams()
    base_ok = [r for t in points for r in base_rows[t] if usable(r)]
    base_km = sum(r["length_m"] for r in base_ok)
    out["ok_km_share_pct_at_default_thresholds"] = {
        "thresholds": [default.c1_max_deg_per_km, default.c2_max_deg_per_km],
        **{c: pct(sum(r["length_m"] for r in base_ok if r["seg_category"] == c) / base_km) for c in ("C1", "C2", "C3")}}

    # ---- stops
    elapsed = moving_all = 0.0
    short_all = long_all = 0.0
    n_short = n_long = 0
    by_group = {"C1": {"short": 0.0, "moving": 0.0, "km": 0.0, "n_short": 0},
                "C2+C3": {"short": 0.0, "moving": 0.0, "km": 0.0, "n_short": 0}}
    mirror_ok = 0
    merged_short = merged_long = 0.0
    profile = [[0, 0.0] for _ in STOP_LABELS]
    artefact = [0, 0.0]
    for t in with_rows:
        stops, trip_elapsed = segment_stops(points[t], params)
        mirror_ok += check_stops_match(stops, rows[t])
        elapsed += trip_elapsed
        for seg_stops, row in zip(stops, rows[t]):
            moving_all += row["moving_time_s"] or 0.0
            for s in seg_stops:
                if s < SHORT_STOP_S:
                    short_all += s
                    n_short += 1
                else:
                    long_all += s
                    n_long += 1
            if usable(row):
                group = by_group["C1" if row["seg_category"] == "C1" else "C2+C3"]
                group["moving"] += row["moving_time_s"]
                group["km"] += row["length_m"] / 1000
                group["short"] += sum(s for s in seg_stops if s < SHORT_STOP_S)
                group["n_short"] += sum(s < SHORT_STOP_S for s in seg_stops)
        trip_profile, trip_artefact = stop_event_profile(points[t], params)
        for total, part in zip(profile, trip_profile):
            total[0] += part[0]
            total[1] += part[1]
        artefact[0] += trip_artefact[0]
        artefact[1] += trip_artefact[1]
        for s in merged_stops(points[t], params):
            if s < SHORT_STOP_S:
                merged_short += s
            else:
                merged_long += s
    stopped = short_all + long_all
    out["stops"] = {
        "mirror_matches_build_rows_on_every_trip": mirror_ok == len(with_rows),
        "elapsed_h_trimmed": round(elapsed / 3600, 1),
        "moving_h": round(moving_all / 3600, 1),
        "stopped_share_of_elapsed_pct": pct(stopped / elapsed),
        "short_share_of_stopped_pct": pct(short_all / stopped),
        "long_share_of_stopped_pct": pct(long_all / stopped),
        "short_stop_events": n_short, "long_stop_events": n_long,
        "short_stop_pct_of_moving_overall": pct(short_all / moving_all),
        "short_stop_pct_of_moving_ok_segments": {
            g: pct(v["short"] / v["moving"]) if v["moving"] else None for g, v in by_group.items()},
        "short_stops_per_100km_ok_segments": {
            g: round(100 * v["n_short"] / v["km"], 1) if v["km"] else None for g, v in by_group.items()},
        "events_by_duration": {label: {"events": b[0], "share_of_stopped_time_pct": pct(b[1] / stopped),
                                       "pct_of_moving_time": pct(b[1] / moving_all)}
                               for label, b in zip(STOP_LABELS, profile)},
        "micro_stops_between_fast_steps": {"events": artefact[0], "share_of_stopped_time_pct": pct(artefact[1] / stopped),
                                           "pct_of_moving_time": pct(artefact[1] / moving_all)},
        "sensitivity_merged_5s": {
            "short_share_of_stopped_pct": pct(merged_short / (merged_short + merged_long)),
            "short_stop_pct_of_moving_overall": pct(merged_short / moving_all)},
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "d5_inventory_aggregates.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                                                          encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
