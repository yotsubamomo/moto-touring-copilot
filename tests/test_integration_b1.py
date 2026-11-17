"""SPEC-B1 SB1-AC2: one integration test from synthetic tracks through ingest, a user- pace table
and an ETA on a route with the same category_scheme.

Every track is generated: straight lines and circular arcs around a made-up origin (the `at`
helper of test_ingest.py), with stops written in as repeated positions. Nothing here is a ride,
a place or a ride result. The route is a hand-built catalog entry; `routes` is not used, so the
handling of a different category_scheme (RI-1 to RI-3) is not covered here.

The contract 3 check with the derived rows only compares the total of n_segments on this path,
because the derived rows carry ingest's category_scheme and the pace table its own (CL-B1-12). The
per-category counts and stop ratios are asserted by this test from the track design, not by the
validator.
"""
from __future__ import annotations

import datetime as dt
import math

import pytest

from moto_copilot.contracts import (validate_dataset, validate_derived_segments, validate_eta_output,
                                    validate_pace_table, validate_public_private_pair, validate_route_catalog)
from moto_copilot.ingest import IngestParams, build_rows, to_public
from moto_copilot.pace import compute_eta, create_pace_table, latest_user_pace_table, load_pace_table
from test_ingest import at

TAIPEI = dt.timezone(dt.timedelta(hours=8))
BUILT = dt.datetime(2026, 11, 18, 9, 0, tzinfo=TAIPEI)
DEPART = dt.datetime(2026, 11, 21, 7, 0, tzinfo=TAIPEI)

# Each trip: 2000 m straight (trimmed), then six 1000 m segments, then 2000 m straight (trimmed).
# Segment k is straight (k = 0, 3: curvature about 0), an arc of radius 500 m (k = 1, 4: about
# 110-120 deg/km) or an arc of radius 150 m (k = 2, 5: about 360-370 deg/km). The recomputed
# terciles (112.1 -> 110, 361.4 -> 360) put two segments of each trip in each category.
LAYOUT = [(None, 20.0), (500.0, 15.0), (150.0, 10.0), (None, 20.0), (500.0, 15.0), (150.0, 10.0)]
EXPECTED_CATEGORY = ["C1", "C2", "C3", "C1", "C2", "C3"]
# Stops (seconds) in the middle of a segment: {seg_index: wait}. 1 s is a repeated position between
# fast steps (a suspected GPS false stop), 3 s to under 180 s is a short stop, 180 s or more is long.
TRIPS = {
    "T901": {0: [1, 30], 3: [200]},             # false, short and long stops in one track
    "T902": {0: [45], 1: [20], 3: [1], 5: [240]},
    "T903": {2: [12], 3: [60], 4: [1]},
}
EXPECTED_EVENTS = {"T901": {"false": 1, "short": 1, "long": 1},
                   "T902": {"false": 1, "short": 2, "long": 1},
                   "T903": {"false": 1, "short": 2, "long": 0}}


def track(waits: dict[int, list[int]]) -> list:
    """One point per second. A ride step moves `speed` metres along the current heading; on an arc
    the heading turns by speed / radius each step. A wait adds one point per second in place."""
    x = y = heading = 0.0
    t = 0
    points = [at(x, y, t)]

    def ride(length: float, speed: float, radius: float | None) -> None:
        nonlocal x, y, heading, t
        for _ in range(int(round(length / speed))):
            if radius:
                heading += speed / radius
            x, y, t = x + speed * math.cos(heading), y + speed * math.sin(heading), t + 1
            points.append(at(x, y, t))

    def wait(seconds: int) -> None:
        nonlocal t
        for _ in range(seconds):
            t += 1
            points.append(at(x, y, t))

    ride(2000.0, 20.0, None)
    for k, (radius, speed) in enumerate(LAYOUT):
        stops = waits.get(k, [])
        steps = int(round(1000.0 / speed))
        at_step = {round(steps * (i + 1) / (len(stops) + 1)): stop for i, stop in enumerate(stops)}
        for step in range(steps):          # the same steps with or without stops: the geometry does not change
            if step in at_step:
                wait(at_step[step])
            ride(speed, speed, radius)
    ride(2000.0, 20.0, None)
    return points


def ingest(trip_id: str, waits: dict[int, list[int]]):
    return build_rows(track(waits), trip_id=trip_id, trip_role="pace", route_id=None, params=IngestParams())


def catalog(scheme: str):
    """R08: C1 2000 m, C2 1500 m, C3 1000 m, C1 3000 m; a waypoint after segment 2. Hand-built, with
    the pace table's category_scheme; end coordinates are placeholders near (0, 0)."""
    parts = [("C1", 2000.0), ("C2", 1500.0), ("C3", 1000.0), ("C1", 3000.0)]
    segments, cum = [], 0.0
    for i, (category, length) in enumerate(parts):
        cum += length
        segments.append({"route_id": "R08", "seg_index": i, "length_m": length, "cum_length_m": cum,
                         "seg_category": category, "end_lat": 0.0, "end_lon": 0.01 * (i + 1)})
    route = {"route_id": "R08", "name": "合成整合路線（測試）", "n_segments": len(parts), "total_length_m": cum,
             "source_trip_id": "T901", "category_scheme": scheme, "catalog_version": "catalog-integration"}
    checkpoints = [
        {"checkpoint_id": "R08-CP01", "route_id": "R08", "kind": "start", "after_seg_count": 0, "name": None,
         "station_ref": None},
        {"checkpoint_id": "R08-CP02", "route_id": "R08", "kind": "waypoint", "after_seg_count": 2, "name": None,
         "station_ref": None},
        {"checkpoint_id": "R08-CP03", "route_id": "R08", "kind": "end", "after_seg_count": 4, "name": None,
         "station_ref": None},
    ]
    return route, segments, checkpoints


def t(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value)


def test_sb1_ac2_tracks_to_ingest_to_user_pace_table_to_eta(tmp_path):
    # --- 1. ingest: stop events, contract 1 -------------------------------------------------
    public_rows = []
    for trip_id, waits in TRIPS.items():
        private, report = ingest(trip_id, waits)
        plain, _ = ingest(trip_id, {})                       # the same track without any stop
        assert report.stop_events == EXPECTED_EVENTS[trip_id]
        assert len(private) == len(plain) == 6
        assert all(r["quality"] == "ok" for r in private)
        assert [r["length_m"] for r in private] == pytest.approx([r["length_m"] for r in plain], abs=1e-6)
        waits_by_seg = {k: waits.get(k, []) for k in range(6)}
        for row, base in zip(private, plain):
            stops = waits_by_seg[row["seg_index"]]
            short = [s for s in stops if 3 <= s < 180]
            # the 1 s false stops are moving time; short stops are short_stop_time_s; long stops only stopped_time_s
            assert row["moving_time_s"] == pytest.approx(base["moving_time_s"] + sum(s for s in stops if s < 3), abs=1e-6)
            assert row["short_stop_time_s"] == sum(short)
            assert row["stopped_time_s"] == sum(s for s in stops if s >= 3)
        assert validate_derived_segments(private, "private") == []
        public = to_public(private)
        assert validate_derived_segments(public, "public") == []
        assert validate_public_private_pair(public, private) == []
        public_rows += public
    assert validate_derived_segments(public_rows, "public") == []
    assert {r["category_scheme"] for r in public_rows} == {IngestParams().category_scheme}

    # --- 2. a user- pace table from the derived rows, contract 3 with the derived rows ---------
    path, header, categories = create_pace_table(tmp_path, public_rows, list(TRIPS), kind="user", min_segments=2,
                                                 built_at=BUILT)
    assert path.name == "user-01.json" and latest_user_pace_table(tmp_path) == path
    assert load_pace_table(path) == (header, categories)
    assert header["category_scheme"] == "curv-tercile-110-360" != IngestParams().category_scheme
    assert header["margin_basis"] == "default" and header["margin_coeff"] == 0.2   # 3 trips: fewer than 8 folds
    assert validate_pace_table(header, categories, public_rows) == []
    by_cat = {c["seg_category"]: c for c in categories}
    for category in ("C1", "C2", "C3"):
        mine = [r for r in public_rows if EXPECTED_CATEGORY[r["seg_index"]] == category]
        assert by_cat[category]["n_segments"] == len(mine) == 6
        assert by_cat[category]["speed_kmh"] is not None
        assert by_cat[category]["stop_ratio"] == pytest.approx(
            sum(r["short_stop_time_s"] for r in mine) / sum(r["moving_time_s"] for r in mine))
    assert by_cat["C1"]["stop_ratio"] == pytest.approx((30 + 45 + 60) / sum(
        r["moving_time_s"] for r in public_rows if r["seg_index"] in (0, 3)))
    assert all(by_cat[c]["stop_ratio"] > 0 for c in ("C1", "C2", "C3"))

    # --- 3. ETA on a route with the same category_scheme, contract 4 (invariants 8 and 9) -------
    route, segments, checkpoints = catalog(header["category_scheme"])
    assert validate_route_catalog([route], segments, checkpoints) == []
    pace_header, pace_categories = load_pace_table(latest_user_pace_table(tmp_path))
    outputs = {}
    for plan_id, breaks in (("P-INT-0", []), ("P-INT-1", [{"after_checkpoint_id": "R08-CP02", "duration_s": 600.0}])):
        eta_header, eta_rows = compute_eta(route, segments, checkpoints, pace_header, pace_categories, plan_id=plan_id,
                                           departure_time=DEPART, breaks=breaks, computed_at=BUILT)
        assert eta_header["status"] == "ok" and eta_header["unknown_reason"] is None
        assert eta_header["margin_coeff"] == pace_header["margin_coeff"]
        assert eta_header["pace_version"] == pace_header["pace_version"] == "user-01"
        ride = 0.0
        for row, seg in zip(eta_rows, segments):
            pace = by_cat[seg["seg_category"]]
            assert row["typ_seg_time_s"] == pytest.approx(seg["length_m"] / (pace["speed_kmh"] / 3.6), abs=1e-3)
            assert row["stop_allow_s"] == pytest.approx(pace["stop_ratio"] * row["typ_seg_time_s"], abs=1e-3)
            assert row["stop_allow_s"] > 0
            ride += row["typ_seg_time_s"] + row["stop_allow_s"]
            expected_typ = DEPART + dt.timedelta(seconds=ride + row["break_time_s"])
            assert abs((t(row["eta_typ"]) - expected_typ).total_seconds()) <= 1.0
            assert (t(row["eta_safe"]) - t(row["eta_typ"])).total_seconds() == pytest.approx(
                pace_header["margin_coeff"] * ride, abs=1.0)
        assert validate_eta_output([eta_header], eta_rows, [route], segments, checkpoints,
                                   pace_header, pace_categories) == []
        outputs[plan_id] = (eta_header, eta_rows)

    # the break adds only its own length; the stop allowance and the margin do not change
    (_, without), (_, with_break) = outputs["P-INT-0"], outputs["P-INT-1"]
    for a, b in zip(without, with_break):
        assert b["stop_allow_s"] == a["stop_allow_s"]
        assert t(b["eta_safe"]) - t(b["eta_typ"]) == t(a["eta_safe"]) - t(a["eta_typ"])
        assert t(b["eta_typ"]) - t(a["eta_typ"]) == dt.timedelta(seconds=b["break_time_s"])
    assert [r["break_time_s"] for r in with_break] == [0.0, 0.0, 600.0, 600.0]

    # --- 4. the whole chain as one dataset ----------------------------------------------------
    headers = [h for h, _ in outputs.values()]
    rows = [r for _, rs in outputs.values() for r in rs]
    report = validate_dataset({"derived_segments": public_rows, "routes": [route], "route_segments": segments,
                               "checkpoints": checkpoints, "pace_header": pace_header,
                               "pace_categories": pace_categories, "eta_headers": headers, "eta_segments": rows})
    assert report == {"derived_segments": [], "route_catalog": [], "pace_table": [], "eta_output": []}
