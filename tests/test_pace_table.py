"""Pace table of SPEC-B1 B1-3 (Issue #10): stop ratio, category thresholds, margin coefficient, versions.

Every row here is invented: segment lengths, times and curvatures are round numbers chosen so the
expected values can be worked out by hand. They are not ride data and say nothing about real pace.
Files are written only to pytest's temporary directory.
"""
from __future__ import annotations

import datetime as dt
import json
import math

import pytest

from moto_copilot.contracts import validate_derived_segments, validate_pace_table
from moto_copilot.ingest import IngestParams
from moto_copilot.ingest.segments import category_of
from moto_copilot.pace import (build_pace_table, category_scheme, classify, create_pace_table, latest_user_pace_table,
                               load_pace_table, loo_folds, margin_from_residuals, tercile_thresholds, timed_rows)

TAIPEI = dt.timezone(dt.timedelta(hours=8))
NOW = dt.datetime(2026, 11, 18, 9, 0, tzinfo=TAIPEI)


def seg(trip_id: str, seg_index: int, curvature: float | None, *, length: float = 1000.0, moving: float | None = 60.0,
        short: float = 0.0, long_stop: float = 0.0, quality: str = "ok", role: str = "pace") -> dict:
    """One contract-1 row (public version). seg_category follows ingest's default thresholds, so the
    rows conform to contract 1; the pace table must not use it."""
    if quality == "invalid":
        moving, curvature = None, None
    return {"trip_id": trip_id, "seg_index": seg_index, "trip_role": role, "route_id": None, "length_m": length,
            "moving_time_s": moving, "stopped_time_s": short + long_stop, "short_stop_time_s": short,
            "curvature_deg_per_km": curvature, "seg_category": category_of(curvature, IngestParams()),
            "quality": quality, "category_scheme": IngestParams().category_scheme, "ingest_version": "ingest-test"}


def trips_three_categories(shorts: list[float]) -> tuple[list[dict], list[str]]:
    """One trip per entry of `shorts`; each trip has three 1000 m segments ridden in 60 s (60 km/h)
    with curvature 10, 100 and 300, and `short` seconds of short stops on its first segment.
    With any 2 or more of these trips the thresholds are (100, 300), so the three segments are
    C1, C2 and C3."""
    rows, trip_ids = [], []
    for i, short in enumerate(shorts):
        trip_id = f"T{101 + i:03d}"
        trip_ids.append(trip_id)
        rows += [seg(trip_id, 0, 10.0, short=short), seg(trip_id, 1, 100.0), seg(trip_id, 2, 300.0)]
    return rows, trip_ids


def test_synthetic_rows_conform_to_contract_1():
    rows, _ = trips_three_categories([0, 30, 48])
    rows += [seg("T190", 0, 50.0, quality="suspect"), seg("T190", 1, None, quality="invalid"),
             seg("T191", 0, 20.0, role="holdout")]
    assert validate_derived_segments(rows, "public") == []


# --- AC 1: stop_ratio ---------------------------------------------------------------
def test_stop_ratio_is_short_stops_over_moving_time_of_the_timed_segments():
    rows = [
        # T301: curvature 10 / 20 / 300 / 310; T302: 15 / 25 / 320. Thresholds of the 7 timed values
        # [10, 15, 20, 25, 300, 310, 320]: v[2] = 20 -> 20, v[4] = 300 -> 300.
        seg("T301", 0, 10.0, length=1000, moving=50, short=5),     # C1
        seg("T301", 1, 20.0, length=1200, moving=80, short=12),    # C2 (20 is not below 20)
        seg("T301", 2, 300.0, length=900, moving=90, short=30, long_stop=600),  # C3; the long stop is not counted
        seg("T301", 3, 310.0, length=800, moving=100, short=0),    # C3
        seg("T302", 0, 15.0, length=1000, moving=40, short=3),     # C1
        seg("T302", 1, 25.0, length=1500, moving=100, short=0),    # C2
        seg("T302", 2, 320.0, length=700, moving=70, short=7),     # C3
        # not timed: these must not enter any sum
        seg("T302", 3, 30.0, moving=10, short=999, quality="suspect"),
        seg("T302", 4, None, quality="invalid"),
    ]
    header, categories = build_pace_table(rows, ["T301", "T302"], pace_version="user-01", min_segments=2, built_at=NOW)
    by_cat = {c["seg_category"]: c for c in categories}
    assert header["category_scheme"] == "curv-tercile-20-300"
    assert by_cat["C1"]["n_segments"] == 2 and by_cat["C1"]["stop_ratio"] == pytest.approx((5 + 3) / (50 + 40))
    assert by_cat["C2"]["n_segments"] == 2 and by_cat["C2"]["stop_ratio"] == pytest.approx((12 + 0) / (80 + 100))
    assert by_cat["C3"]["n_segments"] == 3 and by_cat["C3"]["stop_ratio"] == pytest.approx((30 + 0 + 7) / (90 + 100 + 70))
    assert by_cat["C1"]["speed_kmh"] == round((72.0 + 90.0) / 2, 2)   # 1000 m in 50 s and in 40 s


def test_stop_ratio_is_null_when_speed_is_null_and_zero_when_there_are_no_short_stops():
    rows, trip_ids = trips_three_categories([0, 0])
    rows.append(seg("T101", 3, 400.0, short=20))          # a third C3 segment; C1 and C2 keep two each
    header, categories = build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=3, built_at=NOW)
    by_cat = {c["seg_category"]: c for c in categories}
    assert (by_cat["C1"]["speed_kmh"], by_cat["C1"]["stop_ratio"], by_cat["C1"]["n_segments"]) == (None, None, 2)
    assert (by_cat["C2"]["speed_kmh"], by_cat["C2"]["stop_ratio"], by_cat["C2"]["n_segments"]) == (None, None, 2)
    assert by_cat["C3"]["n_segments"] == 3 and by_cat["C3"]["stop_ratio"] == pytest.approx(20 / 180)
    _, zero = build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=2, built_at=NOW)
    assert {c["seg_category"]: c["stop_ratio"] for c in zero}["C2"] == 0.0
    assert validate_pace_table(header, categories) == []


# --- AC 2 and CL-B1-4 item 10: refusal ---------------------------------------------------
@pytest.mark.parametrize("trip_ids", [["T101", "T191"], ["T191"], ["T101", "T999"]])
def test_a_trip_that_is_not_a_confirmed_pace_trip_is_refused(trip_ids, tmp_path):
    rows, _ = trips_three_categories([0, 0])
    rows.append(seg("T191", 0, 20.0, role="holdout"))
    with pytest.raises(ValueError, match="holdout"):
        build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=1, built_at=NOW)
    with pytest.raises(ValueError, match="holdout"):
        loo_folds(rows, trip_ids, min_segments=1)
    with pytest.raises(ValueError, match="holdout"):
        create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=NOW)
    assert list(tmp_path.iterdir()) == []


def test_a_trip_with_mixed_roles_or_listed_twice_is_refused():
    rows, _ = trips_three_categories([0, 0])
    rows.append(seg("T101", 3, 20.0, role="holdout"))     # breaks contract 1 invariant 1: cannot be confirmed
    with pytest.raises(ValueError, match="holdout"):
        build_pace_table(rows, ["T101", "T102"], pace_version="user-01", min_segments=1, built_at=NOW)
    rows, _ = trips_three_categories([0, 0])
    with pytest.raises(ValueError, match="more than once"):
        build_pace_table(rows, ["T101", "T101"], pace_version="user-01", min_segments=1, built_at=NOW)


def test_the_refusal_comes_before_any_computation():
    """A holdout trip whose rows would break the computation is refused for its role, not for its values."""
    rows, _ = trips_three_categories([0, 0])
    rows.append(seg("T191", 0, 20.0, role="holdout", moving=float("nan")))
    with pytest.raises(ValueError, match="holdout"):
        build_pace_table(rows, ["T101", "T191"], pace_version="user-01", min_segments=1, built_at=NOW)


# --- AC 3 and CL-B1-4 items 2-4: thresholds, classification, scheme ----------------------
def test_a_fixed_curvature_list_gives_fixed_thresholds():
    # n = 9: positions 3 and 6. 42.4 -> round(8.48) = 8 -> 40; 251.0 -> round(50.2) = 50 -> 250
    assert tercile_thresholds([300.0, 5.0, 42.4, 251.0, 12.0, 80.0, 400.0, 30.0, 90.0]) == (40, 250)
    # Python's round sends .5 to the even neighbour, like the reference: 87.5 -> 18 -> 90, 92.5 -> 18 -> 90
    assert tercile_thresholds([1.0, 87.5, 500.0]) == (90, 500)
    assert tercile_thresholds([1.0, 92.5, 500.0]) == (90, 500)
    assert tercile_thresholds([7.0]) == (5, 5)
    assert tercile_thresholds([77.0, 1.0]) == (0, 75)           # n = 2: positions 0 and 1; round(0.2) = 0


def test_no_timed_segment_means_no_thresholds_and_no_table(tmp_path):
    with pytest.raises(ValueError, match="no timed segment"):
        tercile_thresholds([])
    rows = [seg("T101", 0, 50.0, quality="suspect"), seg("T101", 1, None, quality="invalid"),
            seg("T102", 0, 30.0, moving=0.0)]               # moving time 0 is not timed (CL-B1-4 item 1)
    with pytest.raises(ValueError, match="no timed segment"):
        build_pace_table(rows, ["T101", "T102"], pace_version="user-01", min_segments=1, built_at=NOW)
    with pytest.raises(ValueError, match="no timed segment"):
        create_pace_table(tmp_path, rows, ["T101", "T102"], kind="user", min_segments=1, built_at=NOW)
    assert list(tmp_path.iterdir()) == []


def test_category_scheme_has_the_fixed_format():
    assert category_scheme(80, 250) == "curv-tercile-80-250"
    rows, trip_ids = trips_three_categories([0, 0, 0])
    header, _ = build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=1, built_at=NOW)
    assert header["category_scheme"] == "curv-tercile-100-300"


@pytest.mark.parametrize("curvature", [0.0, 39.9, 40.0, 40.1, 199.9, 200.0, 200.1, 900.0])
def test_classification_uses_the_same_boundary_as_ingest(curvature):
    assert classify(curvature, 40, 200) == category_of(curvature, IngestParams(c1_max_deg_per_km=40,
                                                                                c2_max_deg_per_km=200))


def test_the_derived_seg_category_and_category_scheme_are_not_used():
    rows, trip_ids = trips_three_categories([0, 30, 60])
    relabelled = [{**r, "seg_category": "C3", "category_scheme": "something-else"} for r in rows]
    assert build_pace_table(relabelled, trip_ids, pace_version="user-01", min_segments=1, built_at=NOW) == \
        build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=1, built_at=NOW)


def test_only_the_rows_of_the_listed_trips_are_used():
    rows, _ = trips_three_categories([0, 0, 90])
    alone = build_pace_table(rows, ["T101", "T102"], pace_version="user-01", min_segments=1, built_at=NOW)
    without = build_pace_table([r for r in rows if r["trip_id"] != "T103"], ["T101", "T102"],
                               pace_version="user-01", min_segments=1, built_at=NOW)
    assert alone == without and alone[0]["trip_ids"] == ["T101", "T102"] and alone[0]["n_trips"] == 2


# --- AC 4: the margin rule -------------------------------------------------------------
RESIDUALS_8 = [0.31, -0.02, 0.12, 0.0, 0.08, -0.15, 0.03, -0.01]   # sorted: 0.31, 0.12, 0.08, ...


def test_margin_rule_on_a_fixed_residual_list():
    # third largest r is 0.08 -> ceil(1.6) = 2 -> 0.10
    assert margin_from_residuals(RESIDUALS_8) == (0.10, "loo_rule")
    # 7 counted folds: the default, whatever the residuals
    assert margin_from_residuals(RESIDUALS_8[:7]) == (0.20, "default")
    assert margin_from_residuals([]) == (0.20, "default")


@pytest.mark.parametrize("r3, expected", [
    (0.10, 0.10),            # exactly a multiple stays (0.10 / 0.05 = 2)
    (0.15, 0.15),            # 0.15 / 0.05 is 2.9999999999999996 in binary: still 0.15
    (0.1500001, 0.20),       # just above a multiple goes up
    (0.001, 0.05),
    (0.0, 0.05),             # the floor
    (-0.30, 0.05),           # negative r3 counts as 0, then the floor
    (0.55, 0.55),
])
def test_margin_rule_rounding_and_floor(r3, expected):
    residuals = [1.0, 0.9, r3, -0.5, -0.5, -0.5, -0.5, -0.5]
    coeff, basis = margin_from_residuals(residuals)
    assert basis == "loo_rule" and coeff == expected and round(coeff / 0.05, 9) == round(coeff / 0.05)


def test_margin_rule_rejects_a_non_finite_residual():
    with pytest.raises(ValueError, match="finite"):
        margin_from_residuals([0.1] * 7 + [math.nan])


def test_each_fold_recomputes_the_thresholds_and_a_fold_without_pace_is_not_counted():
    """Thresholds of all eight values are (70, 130). With them no fold would be counted (T201: its 40
    is the only other C1 value; T204: its 100 is C2 and only 70 is left in C2). Each fold uses the
    terciles of the other trips instead."""
    curvatures = {"T201": [40, 130], "T202": [130, 40], "T203": [70, 130], "T204": [100, 160]}
    rows = [seg(t, i, float(c)) for t, cs in curvatures.items() for i, c in enumerate(cs)]
    trip_ids = list(curvatures)
    assert tercile_thresholds([float(c) for cs in curvatures.values() for c in cs]) == (70, 130)
    folds = loo_folds(rows, trip_ids, min_segments=2)
    assert [(f["trip_id"], f["thresholds"], f["counted"]) for f in folds] == [
        ("T201", (100, 130), True),   # others 40 70 100 130 130 160 -> C1: 40 70; C3: 130 130 160
        ("T202", (100, 130), True),
        ("T203", (100, 130), True),   # others 40 40 100 130 130 160
        ("T204", (70, 130), False),   # others 40 40 70 130 130 130: its 100 is C2, which has one segment
    ]
    for fold in folds:
        others = [r["curvature_deg_per_km"] for r in rows if r["trip_id"] != fold["trip_id"]]
        assert fold["thresholds"] == tercile_thresholds(others)
    assert [f["r"] for f in folds if f["counted"]] == [pytest.approx(0.0)] * 3   # every segment is 60 km/h


def test_a_left_out_trip_without_timed_segments_is_not_counted():
    rows, trip_ids = trips_three_categories([0] * 8)
    rows += [seg("T180", 0, 50.0, quality="suspect"), seg("T180", 1, None, quality="invalid")]
    folds = loo_folds(rows, trip_ids + ["T180"], min_segments=1)
    assert [f["counted"] for f in folds] == [True] * 8 + [False]
    assert folds[-1]["trip_id"] == "T180" and folds[-1]["r"] is None
    header, _ = build_pace_table(rows, trip_ids + ["T180"], pace_version="user-01", min_segments=1, built_at=NOW)
    assert header["n_trips"] == 9 and header["margin_basis"] == "loo_rule"


# --- AC 5 and the 7 / 8 folds condition: the header margin equals the rule --------------
SHORTS_8 = [0, 0, 0, 0, 30, 48, 66, 84]


def hand_residuals(shorts: list[float]) -> list[float]:
    """r of each fold for trips_three_categories, worked out from DESIGN.md §6.1. Every fold has the
    thresholds (100, 300) and 60 km/h in every category; only C1 has short stops, so for the left-out
    trip j the predicted ride time is 60 * (1 + rho_j) + 60 + 60 seconds with
    rho_j = (sum of the other trips' short stops) / (60 * (n - 1)); its actual ride time is 180 + s_j."""
    total, n = sum(shorts), len(shorts)
    return [(180 + s) / (180 + 60 * (total - s) / (60 * (n - 1))) - 1 for s in shorts]


def test_header_margin_equals_the_rule_on_the_same_trips_with_8_counted_folds():
    rows, trip_ids = trips_three_categories(SHORTS_8)
    folds = loo_folds(rows, trip_ids, min_segments=2)
    assert [f["r"] for f in folds] == pytest.approx(hand_residuals(SHORTS_8))
    # by hand: the third largest r is that of s = 48: 228 / (180 + 60 * 180 / 420) - 1 = 13 / 120
    assert sorted(f["r"] for f in folds)[-3] == pytest.approx(13 / 120)
    header, categories = build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=2, built_at=NOW)
    assert (header["margin_coeff"], header["margin_basis"]) == (0.15, "loo_rule")   # ceil(2.17) = 3 -> 0.15
    assert (header["margin_coeff"], header["margin_basis"]) == margin_from_residuals(hand_residuals(SHORTS_8))
    assert {c["seg_category"]: c["stop_ratio"] for c in categories}["C1"] == pytest.approx(228 / 480)
    assert validate_pace_table(header, categories, rows) == []


def test_header_margin_is_the_default_with_7_counted_folds():
    rows, trip_ids = trips_three_categories(SHORTS_8[1:])
    folds = loo_folds(rows, trip_ids, min_segments=2)
    assert sum(f["counted"] for f in folds) == 7
    header, _ = build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=2, built_at=NOW)
    assert (header["margin_coeff"], header["margin_basis"]) == (0.20, "default")


def test_the_default_depends_on_counted_folds_not_on_trips():
    """Eight trips, one of which has no timed segment: 7 counted folds, so the default, although
    n_trips is 8 (compare test_a_left_out_trip_without_timed_segments_is_not_counted: 8 counted)."""
    rows, trip_ids = trips_three_categories(SHORTS_8[:7])
    rows += [seg("T180", 0, 50.0, quality="suspect")]
    folds = loo_folds(rows, trip_ids + ["T180"], min_segments=2)
    assert sum(f["counted"] for f in folds) == 7
    header, _ = build_pace_table(rows, trip_ids + ["T180"], pace_version="user-01", min_segments=2, built_at=NOW)
    assert header["n_trips"] == 8 and (header["margin_coeff"], header["margin_basis"]) == (0.20, "default")


# --- input checks --------------------------------------------------------------------
@pytest.mark.parametrize("field, value", [("length_m", math.nan), ("moving_time_s", math.inf),
                                          ("short_stop_time_s", math.nan), ("short_stop_time_s", -1.0),
                                          ("curvature_deg_per_km", math.inf), ("short_stop_time_s", None)])
def test_a_timed_row_with_a_bad_number_is_an_error_not_a_value(field, value):
    rows, trip_ids = trips_three_categories([0, 0])
    rows[0][field] = value
    with pytest.raises(ValueError):
        build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=1, built_at=NOW)


@pytest.mark.parametrize("min_segments", [0, -1, 1.5, True, None])
def test_min_segments_must_be_a_positive_integer(min_segments):
    rows, trip_ids = trips_three_categories([0, 0])
    with pytest.raises(ValueError, match="min_segments"):
        build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=min_segments, built_at=NOW)


def test_built_at_must_be_timezone_aware_and_one_ingest_version():
    rows, trip_ids = trips_three_categories([0, 0])
    with pytest.raises(ValueError, match="timezone-aware"):
        build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=1, built_at=dt.datetime(2026, 11, 18))
    rows[0]["ingest_version"] = "ingest-other"
    with pytest.raises(ValueError, match="ingest_version"):
        build_pace_table(rows, trip_ids, pace_version="user-01", min_segments=1, built_at=NOW)


def test_timed_rows_follow_cl_b1_4_item_1():
    rows = [seg("T101", 0, 10.0), seg("T101", 1, 20.0, quality="suspect"), seg("T101", 2, None, quality="invalid"),
            seg("T102", 0, 30.0), seg("T191", 0, 40.0, role="holdout")]
    rows[3]["curvature_deg_per_km"] = None
    assert [(r["trip_id"], r["seg_index"]) for r in timed_rows(rows, ["T101", "T102", "T191"])] == [("T101", 0)]


# --- AC 6-8: versions, files and the chosen version -----------------------------------
def snapshot(directory) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(directory.iterdir())}


def test_each_build_is_a_new_version_and_file_numbered_per_prefix(tmp_path):
    rows, trip_ids = trips_three_categories(SHORTS_8)
    p1, h1, c1 = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=2, built_at=NOW)
    before = snapshot(tmp_path)
    p2, h2, _ = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=2,
                                  built_at=NOW + dt.timedelta(hours=1))
    assert (p1.name, p2.name) == ("user-01.json", "user-02.json")
    assert (h1["pace_version"], h2["pace_version"]) == ("user-01", "user-02")
    assert {k: v for k, v in snapshot(tmp_path).items() if k in before} == before   # user-01 unchanged
    r1, hr, _ = create_pace_table(tmp_path, rows, trip_ids, kind="research", min_segments=2, built_at=NOW)
    assert r1.name == "research-01.json" and hr["pace_version"] == "research-01"
    before = snapshot(tmp_path)
    p3, _, _ = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=2, built_at=NOW)
    assert p3.name == "user-03.json"
    assert {k: v for k, v in snapshot(tmp_path).items() if k in before} == before   # research- and user- unchanged
    assert sorted(p.name for p in tmp_path.iterdir()) == ["research-01.json", "user-01.json", "user-02.json",
                                                          "user-03.json"]
    header, categories = load_pace_table(p1)
    assert (header, categories) == (h1, c1)
    assert validate_pace_table(header, categories, rows) == []
    assert json.loads(p1.read_text(encoding="utf-8")) == {"pace_header": h1, "pace_categories": c1}


def test_numbering_continues_after_the_largest_existing_number(tmp_path):
    rows, trip_ids = trips_three_categories([0, 0, 0])
    create_pace_table(tmp_path, rows, trip_ids, kind="research", min_segments=1, built_at=NOW, number=7)
    path, header, _ = create_pace_table(tmp_path, rows, trip_ids, kind="research", min_segments=1, built_at=NOW)
    assert path.name == "research-08.json"
    (tmp_path / "user-09.json").write_text("{}", encoding="utf-8")       # another process left a user- file
    path, _, _ = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=NOW)
    assert path.name == "user-10.json"
    (tmp_path / "user-99.json").write_text("{}", encoding="utf-8")
    path, header, _ = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=NOW)
    assert path.name == "user-100.json" and header["pace_version"] == "user-100"


def test_an_existing_research_version_is_an_error_and_is_not_overwritten(tmp_path):
    rows, trip_ids = trips_three_categories(SHORTS_8)
    path, _, _ = create_pace_table(tmp_path, rows, trip_ids, kind="research", min_segments=2, built_at=NOW, number=3)
    assert path.name == "research-03.json"
    before = snapshot(tmp_path)
    other_rows, other_ids = trips_three_categories([0, 0, 0])
    with pytest.raises(FileExistsError, match="research-03"):
        create_pace_table(tmp_path, other_rows, other_ids, kind="research", min_segments=1, built_at=NOW, number=3)
    (tmp_path / "research-004.json").write_text("{}", encoding="utf-8")   # the same number written with three digits
    before = snapshot(tmp_path)
    with pytest.raises(FileExistsError, match="research-04"):
        create_pace_table(tmp_path, other_rows, other_ids, kind="research", min_segments=1, built_at=NOW, number=4)
    assert snapshot(tmp_path) == before


def test_a_user_version_cannot_be_given_a_number(tmp_path):
    rows, trip_ids = trips_three_categories([0, 0])
    with pytest.raises(ValueError, match="numbered automatically"):
        create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=NOW, number=5)
    with pytest.raises(ValueError, match="kind"):
        create_pace_table(tmp_path, rows, trip_ids, kind="pace", min_segments=1, built_at=NOW)
    with pytest.raises(ValueError, match="non-negative"):
        create_pace_table(tmp_path, rows, trip_ids, kind="research", min_segments=1, built_at=NOW, number=-1)
    assert list(tmp_path.iterdir()) == []


def test_the_directory_must_be_given_and_exist(tmp_path):
    rows, trip_ids = trips_three_categories([0, 0])
    with pytest.raises(FileNotFoundError):
        create_pace_table(tmp_path / "missing", rows, trip_ids, kind="user", min_segments=1, built_at=NOW)
    assert not (tmp_path / "missing").exists()
    with pytest.raises(FileNotFoundError):
        latest_user_pace_table(tmp_path / "missing")


def test_the_latest_user_version_by_built_at_is_chosen(tmp_path):
    rows, trip_ids = trips_three_categories([0, 0, 0])
    assert latest_user_pace_table(tmp_path) is None              # no user- version: research- is out of #10
    times = [NOW, NOW + dt.timedelta(days=2), NOW + dt.timedelta(days=1)]
    paths = [create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=t)[0] for t in times]
    create_pace_table(tmp_path, rows, trip_ids, kind="research", min_segments=1, built_at=NOW + dt.timedelta(days=9))
    assert latest_user_pace_table(tmp_path) == paths[1]         # user-02: latest built_at, not the largest number
    tie = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=times[1])[0]
    assert latest_user_pace_table(tmp_path) == tie == tmp_path / "user-04.json"   # same built_at: larger number


def test_a_user_file_with_a_wrong_version_or_time_is_an_error(tmp_path):
    rows, trip_ids = trips_three_categories([0, 0, 0])
    path, header, categories = create_pace_table(tmp_path, rows, trip_ids, kind="user", min_segments=1, built_at=NOW)
    path.write_text(json.dumps({"pace_header": {**header, "built_at": "2026-11-18T09:00:00"},
                                "pace_categories": categories}), encoding="utf-8")
    with pytest.raises(ValueError, match="built_at"):
        latest_user_pace_table(tmp_path)
    path.write_text(json.dumps({"pace_header": {**header, "pace_version": "user-07"},
                                "pace_categories": categories}), encoding="utf-8")
    with pytest.raises(ValueError, match="user-07"):
        latest_user_pace_table(tmp_path)
