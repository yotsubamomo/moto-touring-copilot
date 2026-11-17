"""SB-2 preview: stop allowance on the pace trips, leave-one-trip-out. Not E1, not E2.

    .venv/Scripts/python.exe experiments/cr01_checks/data_sb2_stop_allowance.py

Purpose: support the Spec Resolution Proposal for the stop allowance (CR-01 ruling P-2). It
emulates the proposed ingest fix on top of the current ingest code; `src/` is not changed. The
final parameters are to be produced by the implementation with the same procedure; the numbers
here are a preview. Only pace trips are opened (see data_common); holdout trips are never read.

Definitions, fixed before the run:
  * Stop event: a maximal run of consecutive stopped steps (ingest's step rules).
  * False stop: an event shorter than STOP_MIN_S (3 s). Its time is counted as moving time.
  * Short stop: STOP_MIN_S <= duration < SHORT_STOP_S (180 s). Unplanned stops.
  * Long stop: duration >= 180 s. Rider-arranged breaks; excluded everywhere.
  * Moving time of a segment = recorded moving time + false-stop time.
  * Ride time of a segment = moving time + short-stop time.
  * Pace: unweighted median of segment speed (length / moving time) per category, as in
    pace.build_pace_table, with the fold's tercile thresholds (as in check C2).
Candidate allowance models (parameters from the other trips of the fold, pooled over usable segments):
  * M0 none.
  * M1 one ratio:        r   = sum(short) / sum(moving);        allowance = r * typical moving time
  * M2 ratio per class:  r_c = the same within category c;      allowance = r_c * typical moving time
  * M3 per kilometre:    q   = sum(short) / sum(length);        allowance = q * length
Baselines for the ride time: B0 one median speed, no allowance; B1 one speed = sum(length) / sum(ride time).
Evaluation per left-out trip over its usable segments: error = (predicted - actual) / actual, for
the moving time (no allowance) and for the ride time. MAPE = mean |error| over trips; signed = mean.
Choice rule: the model with the lowest ride-time MAPE; models within 0.5 percentage point of the
best count as tied and the simplest one (M1, then M3, then M2) is taken.
Margin coefficient, descriptive rule: the smallest multiple of 0.05 such that the actual ride time
is within predicted * (1 + m) for all but at most two trips. It is not a quantile estimate and
carries no coverage guarantee.

Prints aggregates only.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import statistics
import sys

from data_common import (MIN_SEGMENTS, OUT_DIR, SHORT_STOP_S, IngestParams, check_stops_match, ingest,
                         load_pace_points, mask, mean, pct, segment_stops, tercile_thresholds, usable)

STOP_MIN_S = 3.0
CATS = ("C1", "C2", "C3")
MODELS = ("M0", "M1", "M2", "M3", "B0", "B1")
SIMPLEST_FIRST = ("M1", "M3", "M2")


def split(stops: list[float]) -> tuple[float, float]:
    """(false-stop seconds, short-stop seconds) of one segment."""
    return (sum(s for s in stops if s < STOP_MIN_S), sum(s for s in stops if STOP_MIN_S <= s < SHORT_STOP_S))


def enrich(rows: list[dict], stops: list[list[float]]) -> list[dict]:
    out = []
    for r, seg_stops in zip(rows, stops):
        if not usable(r):
            continue
        false_s, short_s = split(seg_stops)
        out.append({"cat": r["seg_category"], "len": r["length_m"], "mov": r["moving_time_s"] + false_s, "short": short_s})
    return out


def fit(train: list[dict]) -> dict:
    by_cat = {c: [s for s in train if s["cat"] == c] for c in CATS}
    speed = {c: (statistics.median(s["len"] / s["mov"] for s in v) if len(v) >= MIN_SEGMENTS else None) for c, v in by_cat.items()}
    mov, short, length = (sum(s[k] for s in train) for k in ("mov", "short", "len"))
    return {"speed": speed, "one_speed": statistics.median(s["len"] / s["mov"] for s in train),
            "r": short / mov, "q": short / length, "ride_speed": length / (mov + short),
            "r_c": {c: (sum(s["short"] for s in v) / sum(s["mov"] for s in v) if v else None) for c, v in by_cat.items()}}


def predict(test: list[dict], p: dict) -> dict | None:
    if any(p["speed"][s["cat"]] is None for s in test):
        return None
    typ = [s["len"] / p["speed"][s["cat"]] for s in test]
    return {"M0": sum(typ), "M1": sum(typ) * (1 + p["r"]),
            "M2": sum(t * (1 + p["r_c"][s["cat"]]) for t, s in zip(typ, test)),
            "M3": sum(typ) + p["q"] * sum(s["len"] for s in test),
            "B0": sum(s["len"] for s in test) / p["one_speed"], "B1": sum(s["len"] for s in test) / p["ride_speed"]}


def summary(errors: list[float], n: int) -> dict:
    return {"mape_pct": pct(mean([abs(e) for e in errors])), "signed_pct": pct(mean(errors)),
            "optimistic_trips": mask(sum(e < 0 for e in errors), n)}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    points = load_pace_points()
    base_rows, _ = ingest(points, IngestParams())
    trips = [t for t in sorted(points) if base_rows[t]]
    stops = {t: segment_stops(points[t], IngestParams())[0] for t in trips}
    if not all(check_stops_match(stops[t], base_rows[t]) for t in trips):
        raise RuntimeError("the stop mirror does not reproduce build_rows")

    cache: dict[tuple[float, float], dict[str, list[dict]]] = {}

    def segments(c1_max: float, c2_max: float) -> dict[str, list[dict]]:
        if (c1_max, c2_max) not in cache:
            rows = ingest(points, IngestParams(c1_max_deg_per_km=c1_max, c2_max_deg_per_km=c2_max))[0]
            cache[(c1_max, c2_max)] = {t: enrich(rows[t], stops[t]) for t in trips}
        return cache[(c1_max, c2_max)]

    ride_err = {m: [] for m in MODELS}
    mov_err, ratios, no_pace = [], [], 0
    for left_out in trips:
        others = [t for t in trips if t != left_out]
        c1_max, c2_max, _ = tercile_thresholds([r for t in others for r in base_rows[t]])
        segs = segments(c1_max, c2_max)
        p = fit([s for t in others for s in segs[t]])
        test = segs[left_out]
        pred = predict(test, p) if test else None
        if pred is None:
            no_pace += 1
            continue
        mov, ride = sum(s["mov"] for s in test), sum(s["mov"] + s["short"] for s in test)
        mov_err.append((pred["M0"] - mov) / mov)
        for m in MODELS:
            ride_err[m].append((pred[m] - ride) / ride)
        ratios.append({m: ride / pred[m] - 1 for m in SIMPLEST_FIRST})
    n = len(mov_err)

    best = min(statistics.fmean(abs(e) for e in ride_err[m]) for m in SIMPLEST_FIRST)
    chosen = next(m for m in SIMPLEST_FIRST if statistics.fmean(abs(e) for e in ride_err[m]) <= best + 0.005)

    def margin(model: str) -> dict:
        over = sorted((r[model] for r in ratios), reverse=True)
        m = max(0.05, math.ceil(max(over[2], 0.0) / 0.05 - 1e-9) * 0.05)
        return {"margin_coeff": round(m, 2),
                "trips_within_safe": mask(sum(r[model] <= m for r in ratios), n),
                "trips_within_safe_at_0.20": mask(sum(r[model] <= 0.20 for r in ratios), n)}

    # Parameters on all pace trips, with the thresholds of the full set (for the preview table only).
    c1_max, c2_max, _ = tercile_thresholds([r for t in trips for r in base_rows[t]])
    full = fit([s for t in trips for s in segments(c1_max, c2_max)[t]])
    all_stops = [s for t in trips for seg in stops[t] for s in seg]
    recorded_moving = sum(r["moving_time_s"] for t in trips for r in base_rows[t] if r["moving_time_s"])
    per_trip_r = sorted(sum(s["short"] for s in segments(c1_max, c2_max)[t]) / sum(s["mov"] for s in segments(c1_max, c2_max)[t])
                        for t in trips if segments(c1_max, c2_max)[t])
    out = {
        "label": "SB-2 preview on pace trips only (emulated ingest fix); not E1, not E2; final values come from the implementation",
        "trips_evaluated": mask(n, len(trips)), "trips_without_pace": mask(no_pace, len(trips)),
        "stop_min_s": STOP_MIN_S, "short_stop_s": SHORT_STOP_S,
        "false_stop_share_of_recorded_moving_pct": pct(sum(s for s in all_stops if s < STOP_MIN_S) / recorded_moving),
        "false_stop_events": sum(1 for s in all_stops if s < STOP_MIN_S),
        "short_stop_events": sum(1 for s in all_stops if STOP_MIN_S <= s < SHORT_STOP_S),
        "full_set_parameters": {"thresholds_deg_per_km": [c1_max, c2_max], "r_pct": pct(full["r"]),
                                "r_c_pct": {c: pct(v) for c, v in full["r_c"].items()},
                                "q_s_per_km": round(full["q"] * 1000, 1),
                                "per_trip_r_pct_quartiles": [pct(v) for v in statistics.quantiles(per_trip_r, n=4)]},
        "moving_time_M0": summary(mov_err, n),
        "ride_time": {m: summary(ride_err[m], n) for m in MODELS},
        "chosen_by_rule": chosen,
        "margin_rule": {m: margin(m) for m in SIMPLEST_FIRST},
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "sb2_stop_allowance_aggregates.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("generated", dt.date.today().isoformat())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
