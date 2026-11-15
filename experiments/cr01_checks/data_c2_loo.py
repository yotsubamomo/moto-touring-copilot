"""CR-01 check C2: whole-trip leave-one-out error on the pace trips. Not E1, not E2.

    .venv/Scripts/python.exe experiments/cr01_checks/data_c2_loo.py

Pass condition (fixed before this run, CR-01 section "C2 整趟誤差"; not changed here):
  (a) MAPE of C1 predicted time <= MAPE of C2+C3 predicted time + 5 percentage points, and
  (b) mean signed error of whole-trip moving time within +-10%.

Method, fixed before the run:
  * For each pace trip in turn, the other pace trips give the category thresholds (terciles of
    ok-segment curvature, the spike's rule, rounded to 5 deg/km) and the pace table
    (pace.build_pace_table: unweighted median of segment moving speed per category, a category
    needs MIN_SEGMENTS ok segments). All trips are re-ingested with the fold's thresholds.
  * The left-out trip's ok segments are predicted as length / category pace and compared with
    their recorded moving time, summed per trip over (i) all, (ii) C1, (iii) C2+C3 segments.
  * Error of a trip = (predicted - actual) / actual. MAPE = mean |error| over trips; signed =
    mean error over trips; optimistic = predicted shorter than actual.
  * A trip whose needed category has no pace is counted and left out of that group; no value is
    substituted. A trip with no segment in a group is left out of that group as well.
  * Baseline: one speed for every segment, the unweighted median speed of all ok segments of the
    other trips.
  * Short-stop variant: actual = moving time + stop events under 180 s inside the same ok segments.
  * Supplementary (not used for the verdict): the same MAPE taken per segment instead of per trip.

Prints and writes aggregates only. Holdout and excluded trips are never opened.
"""
from __future__ import annotations

import datetime as dt
import json
import statistics
import sys

from data_common import (MIN_SEGMENTS, OUT_DIR, SHORT_STOP_S, IngestParams, check_stops_match, ingest,
                         load_pace_points, mask, mean, pct, segment_stops, speed_kmh, tercile_thresholds, usable)

from moto_copilot.pace import build_pace_table

GROUPS = {"all": ("C1", "C2", "C3"), "C1": ("C1",), "C2+C3": ("C2", "C3")}
MARGIN_PP = 5.0
SIGNED_LIMIT_PCT = 10.0


def summarise(errors: list[float], n_trips: int) -> dict:
    if len(errors) < 3:
        return {"trips_evaluated": "<3", "mape_pct": "withheld", "signed_pct": "withheld", "optimistic_trips": "withheld"}
    return {"trips_evaluated": mask(len(errors), n_trips), "mape_pct": pct(mean([abs(e) for e in errors])),
            "signed_pct": pct(mean(errors)), "optimistic_trips": mask(sum(e < 0 for e in errors), len(errors))}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    points = load_pace_points()
    trips = sorted(points)
    n = len(trips)
    base_rows, _ = ingest(points, IngestParams())
    with_rows = [t for t in trips if base_rows[t]]
    stops = {t: segment_stops(points[t], IngestParams())[0] for t in with_rows}
    if not all(check_stops_match(stops[t], base_rows[t]) for t in with_rows):
        raise RuntimeError("the stop mirror does not reproduce build_rows")

    cache: dict[tuple[float, float], dict[str, list[dict]]] = {}
    now = dt.datetime.now(dt.timezone.utc)
    err = {m: {g: [] for g in GROUPS} for m in ("category", "baseline")}
    err_short = {m: [] for m in ("category", "baseline")}
    seg_abs = {m: {g: [] for g in GROUPS} for m in ("category", "baseline")}
    no_pace = {g: 0 for g in GROUPS}
    no_segments = {g: 0 for g in GROUPS}
    thresholds_seen = set()
    for left_out in with_rows:
        others = [t for t in with_rows if t != left_out]
        c1_max, c2_max, _ = tercile_thresholds([r for t in others for r in base_rows[t]])
        thresholds_seen.add((c1_max, c2_max))
        if (c1_max, c2_max) not in cache:
            cache[(c1_max, c2_max)] = ingest(points, IngestParams(c1_max_deg_per_km=c1_max, c2_max_deg_per_km=c2_max))[0]
        rows = cache[(c1_max, c2_max)]
        training = [r for t in others for r in rows[t]]
        _, categories = build_pace_table(training, others, pace_version="cr01-c2-loo", min_segments=MIN_SEGMENTS,
                                         built_at=now)
        pace = {c["seg_category"]: c["speed_kmh"] for c in categories}
        overall = statistics.median(speed_kmh(r) for r in training if usable(r))
        test = [(r, sum(s for s in seg_stops if s < SHORT_STOP_S))
                for r, seg_stops in zip(rows[left_out], stops[left_out]) if usable(r)]
        for group, cats in GROUPS.items():
            segs = [(r, short) for r, short in test if r["seg_category"] in cats]
            if not segs:
                no_segments[group] += 1
                continue
            actual = sum(r["moving_time_s"] for r, _ in segs)
            short = sum(s for _, s in segs)
            base_pred = sum(r["length_m"] / (overall / 3.6) for r, _ in segs)
            err["baseline"][group].append((base_pred - actual) / actual)
            seg_abs["baseline"][group].extend(abs(r["length_m"] / (overall / 3.6) - r["moving_time_s"]) / r["moving_time_s"]
                                              for r, _ in segs)
            if group == "all":
                err_short["baseline"].append((base_pred - actual - short) / (actual + short))
            if any(pace[r["seg_category"]] is None for r, _ in segs):
                no_pace[group] += 1
                continue
            pred = sum(r["length_m"] / (pace[r["seg_category"]] / 3.6) for r, _ in segs)
            err["category"][group].append((pred - actual) / actual)
            seg_abs["category"][group].extend(
                abs(r["length_m"] / (pace[r["seg_category"]] / 3.6) - r["moving_time_s"]) / r["moving_time_s"]
                for r, _ in segs)
            if group == "all":
                err_short["category"].append((pred - actual - short) / (actual + short))

    out: dict = {"label": "CR-01 technical check C2, leave-one-out on pace trips only; not an E1 result",
                 "trips_loaded": n, "folds": mask(len(with_rows), n), "min_segments": MIN_SEGMENTS,
                 "distinct_fold_threshold_pairs": len(thresholds_seen),
                 "fold_c1_max_range": [min(a for a, _ in thresholds_seen), max(a for a, _ in thresholds_seen)],
                 "fold_c2_max_range": [min(b for _, b in thresholds_seen), max(b for _, b in thresholds_seen)],
                 "trips_without_pace": {g: mask(k, len(with_rows)) for g, k in no_pace.items()},
                 "trips_without_segments": {g: mask(k, len(with_rows)) for g, k in no_segments.items()}}
    for model in ("category", "baseline"):
        out[model] = {g: summarise(err[model][g], len(with_rows)) for g in GROUPS}
        out[model]["all_with_short_stops_in_actual"] = summarise(err_short[model], len(with_rows))
        out[model]["supplementary_segment_level_mape_pct"] = {
            g: pct(mean(v)) if len(err[model][g]) >= 3 else "withheld" for g, v in seg_abs[model].items()}

    cat = out["category"]
    if any(cat[g]["mape_pct"] == "withheld" for g in GROUPS):
        verdict = {"a": None, "b": None, "verdict": "NOT EVALUABLE (a group has fewer than 3 trips)"}
    else:
        a = cat["C1"]["mape_pct"] <= cat["C2+C3"]["mape_pct"] + MARGIN_PP
        b = abs(cat["all"]["signed_pct"]) <= SIGNED_LIMIT_PCT
        verdict = {"a_c1_mape_le_c2c3_mape_plus_5pp": a, "b_whole_trip_signed_within_10pct": b,
                   "verdict": "PASS" if a and b else "FAIL"}
    out["verdict"] = verdict

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "c2_loo_aggregates.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
