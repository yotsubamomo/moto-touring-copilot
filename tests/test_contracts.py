"""Tests for the data contracts v0.3 (DESIGN.md §5): the stop-allowance fields of contracts 1, 3, 4 and the
v0.3 ID formats with the contract 2 changes.

These tests check the validators against a mock fixture and against deliberately broken copies
of it. They say nothing about real rides: no GPX has been ingested yet.
"""
from __future__ import annotations

import json
import re

import pytest

from moto_copilot.contracts import (
    CONTRACT_VERSION,
    checkpoint_arrival,
    expected_break_times,
    pace_eligible,
    validate_dataset,
    validate_derived_segments,
    validate_eta_output,
    validate_pace_table,
    validate_public_private_pair,
    validate_route_catalog,
)


def eta_violations(d: dict) -> list[str]:
    return validate_eta_output(d["eta_headers"], d["eta_segments"], d["routes"], d["route_segments"],
                               d["checkpoints"], d["pace_header"], d["pace_categories"])


def catalog_violations(d: dict) -> list[str]:
    return validate_route_catalog(d["routes"], d["route_segments"], d["checkpoints"])


def assert_violation(violations: list[str], fragment: str) -> None:
    assert any(fragment in v for v in violations), f"expected a violation containing {fragment!r}, got {violations}"


def by_id(records: list[dict], key: str, value) -> dict:
    return next(r for r in records if r[key] == value)


# --- the mock fixture itself -------------------------------------------------
def test_fixture_is_marked_as_mock(data):
    assert data["_meta"]["mock"] is True
    assert data["_meta"]["contract_version"] == CONTRACT_VERSION == "0.3"   # SPEC-B1 CL-B1-2, Issue #13


def test_mock_fixture_conforms_to_every_contract(data, private_rows):
    report = validate_dataset(data, "public")
    assert set(report) == {"derived_segments", "route_catalog", "pace_table", "eta_output"}
    assert all(v == [] for v in report.values()), report
    assert validate_derived_segments(private_rows, "private") == []
    assert validate_public_private_pair(data["derived_segments"], private_rows) == []


# --- contract 1: derived segment table --------------------------------------
@pytest.mark.parametrize("value", [0, 0.0, -5.0])
def test_moving_time_must_be_positive(data, value):
    data["derived_segments"][0]["moving_time_s"] = value
    assert_violation(validate_derived_segments(data["derived_segments"]), "moving_time_s")


def test_invalid_segment_must_not_keep_a_moving_time(data):
    row = by_id(data["derived_segments"], "quality", "invalid")
    row["moving_time_s"] = 30.0
    assert_violation(validate_derived_segments(data["derived_segments"]), "quality is invalid but moving_time_s has a value")


def test_null_moving_time_needs_quality_invalid(data):
    data["derived_segments"][0]["moving_time_s"] = None
    assert_violation(validate_derived_segments(data["derived_segments"]), "moving_time_s is null but quality is not invalid")


def test_only_ok_pace_rows_with_a_category_are_pace_eligible(data):
    eligible = [(r["trip_id"], r["seg_index"]) for r in data["derived_segments"] if pace_eligible(r)]
    # excluded: T001/2 invalid, T002/1 suspect, every T003 row (holdout)
    assert eligible == [("T001", 0), ("T001", 1), ("T002", 0), ("T002", 2), ("T002", 3)]


def test_trip_role_must_be_constant_within_a_trip(data):
    data["derived_segments"][1]["trip_role"] = "holdout"
    assert_violation(validate_derived_segments(data["derived_segments"]), "more than one trip_role")


def test_one_table_has_one_ingest_version(data):
    data["derived_segments"][-1]["ingest_version"] = "ingest-other"
    assert_violation(validate_derived_segments(data["derived_segments"]), "more than one ingest_version")


def test_seg_index_has_no_gaps(data):
    data["derived_segments"][2]["seg_index"] = 5
    assert_violation(validate_derived_segments(data["derived_segments"]), "not 0..n-1 without gaps")


def test_duplicate_primary_key_is_rejected(data):
    data["derived_segments"][1]["seg_index"] = 0
    assert_violation(validate_derived_segments(data["derived_segments"]), "duplicate primary key")


def test_public_version_rejects_start_time(private_rows):
    assert_violation(validate_derived_segments(private_rows, "public"), "start_time")


def test_private_version_requires_start_time(data):
    assert_violation(validate_derived_segments(data["derived_segments"], "private"), "start_time")


@pytest.mark.parametrize("bad", ["2026-01-03T08:00:00", "2026-01-03T00:00:00Z", "2026-01-03 08:00:00+08:00", "2026-01-03"])
def test_private_start_time_needs_the_taipei_offset(private_rows, bad):
    private_rows[0]["start_time"] = bad
    assert_violation(validate_derived_segments(private_rows, "private"), "start_time")


def test_public_rows_hold_no_date_time_or_coordinates(data):
    """Privacy (DC-9, NFR2): nothing in the public table looks like a date, a time or a position."""
    date_or_time = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}")
    for row in data["derived_segments"]:
        assert not any(k in row for k in ("start_time", "lat", "lon", "end_lat", "end_lon"))
        for value in row.values():
            assert not (isinstance(value, str) and date_or_time.search(value)), value


def test_public_and_private_versions_must_match(data, private_rows):
    private_rows[3]["length_m"] += 1.0
    assert_violation(validate_public_private_pair(data["derived_segments"], private_rows), "differs between public and private")
    assert_violation(validate_public_private_pair(data["derived_segments"], private_rows[:-1]), "do not have the same rows")


# --- contract 2: route catalog and checkpoint boundaries --------------------
def test_checkpoint_positions_are_integers_not_distances(data):
    for cp in data["checkpoints"]:
        assert isinstance(cp["after_seg_count"], int) and "cum_length_m" not in cp


@pytest.mark.parametrize("count, fragment", [
    (5, "outside 0..4"),      # one past the end (n = 4)
    (-1, "after_seg_count"),  # rejected by the schema minimum
])
def test_checkpoint_outside_the_route_is_rejected(data, count, fragment):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["after_seg_count"] = count
    assert_violation(catalog_violations(data), fragment)


@pytest.mark.parametrize("count", [0, 4])
def test_checkpoint_on_the_first_and_last_boundary_is_allowed(data, count):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["after_seg_count"] = count
    assert catalog_violations(data) == []


def test_end_checkpoint_one_segment_short_is_rejected(data):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP05")["after_seg_count"] = 3  # n - 1
    assert_violation(catalog_violations(data), "is end but after_seg_count is not 4")


def test_start_checkpoint_must_be_at_zero(data):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP01")["after_seg_count"] = 1
    assert_violation(catalog_violations(data), "is start but after_seg_count is not 0")


def test_route_needs_exactly_one_start_and_one_end(data):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["kind"] = "end"
    assert_violation(catalog_violations(data), "exactly one end, found 2")
    data["checkpoints"] = [c for c in data["checkpoints"] if c["checkpoint_id"] != "R02-CP01"]
    assert_violation(catalog_violations(data), "exactly one start, found 0")


def test_several_checkpoints_may_share_a_position(data):
    same_place = [c for c in data["checkpoints"] if c["route_id"] == "R01" and c["after_seg_count"] == 0]
    assert {c["kind"] for c in same_place} == {"start", "fuel_station"}
    assert catalog_violations(data) == []


def test_station_ref_is_required_for_fuel_stations_only(data):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP03")["station_ref"] = None
    assert_violation(catalog_violations(data), "fuel_station without station_ref")
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["station_ref"] = "MOCK-ST-09"
    assert_violation(catalog_violations(data), "not a fuel_station but has station_ref")


def test_segment_count_must_match_the_route(data):
    by_id(data["routes"], "route_id", "R01")["n_segments"] = 5
    assert_violation(catalog_violations(data), "needs seg_index 0..5-1 exactly once, found 4")


def test_cumulative_length_is_the_running_sum(data):
    data["route_segments"][2]["cum_length_m"] = 7000.0
    assert_violation(catalog_violations(data), "not the running sum")


def test_route_segment_category_cannot_be_null(data):
    data["route_segments"][0]["seg_category"] = None
    assert_violation(catalog_violations(data), "seg_category")


# --- contract 3: pace table --------------------------------------------------
def pace_violations(d: dict) -> list[str]:
    return validate_pace_table(d["pace_header"], d["pace_categories"], d["derived_segments"])


def test_pace_table_keeps_method_and_speed_separate(data):
    assert data["pace_header"]["method"] == "median_unweighted"
    assert all("speed_kmh" in c and "median_speed_kmh" not in c for c in data["pace_categories"])


def test_every_category_has_exactly_one_record(data):
    data["pace_categories"] = data["pace_categories"][:2]
    assert_violation(pace_violations(data), "exactly one record for C3, found 0")


def test_holdout_trip_must_not_enter_the_pace_table(data):
    data["pace_header"]["trip_ids"].append("T003")
    data["pace_header"]["n_trips"] = 3
    assert_violation(pace_violations(data), "T003 is not a pace trip")


def test_too_few_segments_means_null_speed(data):
    by_id(data["pace_categories"], "seg_category", "C3")["speed_kmh"] = 30.0
    assert_violation(pace_violations(data), "C3 has speed_kmh with fewer than min_segments")


def test_enough_segments_means_a_speed(data):
    by_id(data["pace_categories"], "seg_category", "C1")["speed_kmh"] = None
    assert_violation(pace_violations(data), "C1 has enough segments but speed_kmh is null")


def test_segment_count_counts_only_eligible_rows(data):
    by_id(data["pace_categories"], "seg_category", "C1")["n_segments"] = 3  # would include the suspect row
    assert_violation(pace_violations(data), "C1 n_segments is 3, but 2 rows are eligible")


def recomputed_scheme(d: dict) -> dict:
    """The fixture's pace table rewritten as a table with its own category_scheme (CL-B1-12): the
    five eligible rows of T001 and T002 split 1 / 2 / 2 instead of the derived 2 / 2 / 1. C1 then has
    fewer than min_segments segments, so its speed and stop ratio are null."""
    d["pace_header"]["category_scheme"] = "curv-tercile-20-150"
    for category, n, speed, ratio in (("C1", 1, None, None), ("C2", 2, 52.5, 0.1), ("C3", 2, 40.5, 0.0)):
        by_id(d["pace_categories"], "seg_category", category).update(n_segments=n, speed_kmh=speed, stop_ratio=ratio)
    return d


def test_another_scheme_checks_the_total_not_the_derived_categories(data):
    """(i) The derived seg_category is not the pace table's category when the schemes differ."""
    assert pace_violations(recomputed_scheme(data)) == []


@pytest.mark.parametrize("category, n, total", [("C3", 3, 6), ("C2", 1, 4)])
def test_another_scheme_still_needs_the_total_of_eligible_rows(data, category, n, total):
    """(ii) One row too many (for example the suspect row) or one too few is a violation."""
    recomputed_scheme(data)
    rec = by_id(data["pace_categories"], "seg_category", category)
    rec.update(n_segments=n, speed_kmh=rec["speed_kmh"] if n >= 2 else None,
               stop_ratio=rec["stop_ratio"] if n >= 2 else None)
    assert_violation(pace_violations(data), f"n_segments add up to {total}, but 5 rows are eligible (invariant 3)")


def test_the_same_scheme_still_checks_each_category(data):
    """(iii) Same total, wrong split, same scheme as the derived table: the per-category check stays."""
    by_id(data["pace_categories"], "seg_category", "C1")["n_segments"] = 3
    by_id(data["pace_categories"], "seg_category", "C2")["n_segments"] = 1
    by_id(data["pace_categories"], "seg_category", "C2")["speed_kmh"] = None
    by_id(data["pace_categories"], "seg_category", "C2")["stop_ratio"] = None
    violations = pace_violations(data)
    assert_violation(violations, "C1 n_segments is 3, but 2 rows are eligible (invariant 3)")
    assert not any("add up to" in v for v in violations), violations


def test_rows_of_other_trips_and_holdout_rows_are_not_eligible(data):
    """(iv) Only the eligible rows of trip_ids count: not the holdout trip T003, not another pace trip."""
    recomputed_scheme(data)
    data["derived_segments"].append({**data["derived_segments"][0], "trip_id": "T004", "seg_index": 0})
    assert pace_violations(data) == []
    by_id(data["pace_categories"], "seg_category", "C3")["n_segments"] = 4   # + T003's two holdout rows
    assert_violation(pace_violations(data), "n_segments add up to 7, but 5 rows are eligible (invariant 3)")
    by_id(data["pace_categories"], "seg_category", "C3")["n_segments"] = 3   # + the row of T004
    assert_violation(pace_violations(data), "n_segments add up to 6, but 5 rows are eligible (invariant 3)")


def json_round_trip(d: dict) -> dict:
    return json.loads(json.dumps(d))


@pytest.mark.parametrize("counts, total", [
    ([1.0, 2.0, 2.0], None),        # whole-number floats, correct total
    ([1, 2.0, 2], None),            # mixed int and float, correct total
    ([1.0, 2.0, 3.0], 6),           # one too many
    ([1, 2, 3.0], 6),
    ([1.0, 1.0, 2.0], 4),           # one too few
])
@pytest.mark.parametrize("round_trip", [False, True])
def test_another_scheme_counts_whole_number_floats_too(data, counts, total, round_trip):
    """R1-F1: JSON Schema's integer accepts 3.0, so the total check must count it and not let a wrong
    total through. Also after a JSON round trip."""
    recomputed_scheme(data)
    for rec, n in zip(data["pace_categories"], counts):
        rec.update(n_segments=n, speed_kmh=rec["speed_kmh"] if n >= 2 else None,
                   stop_ratio=rec["stop_ratio"] if n >= 2 else None)
    if round_trip:
        data = json_round_trip(data)
    violations = pace_violations(data)
    if total is None:
        assert violations == []
    else:
        assert_violation(violations, f"n_segments add up to {total}, but 5 rows are eligible (invariant 3)")


def test_the_same_scheme_checks_each_category_with_whole_number_floats(data):
    for rec in data["pace_categories"]:
        rec["n_segments"] = float(rec["n_segments"])
    assert pace_violations(json_round_trip(data)) == []
    by_id(data["pace_categories"], "seg_category", "C1")["n_segments"] = 3.0
    by_id(data["pace_categories"], "seg_category", "C2")["n_segments"] = 1.0
    by_id(data["pace_categories"], "seg_category", "C2").update(speed_kmh=None, stop_ratio=None)
    assert_violation(pace_violations(json_round_trip(data)), "C1 n_segments is 3.0, but 2 rows are eligible")


@pytest.mark.parametrize("value", [2.5, "2", True, None, float("nan"), float("inf")])
def test_a_count_that_cannot_be_added_up_is_a_violation(data, value):
    """Any other value is reported for invariant 3 itself, not left to the schema alone."""
    recomputed_scheme(data)
    by_id(data["pace_categories"], "seg_category", "C3")["n_segments"] = value
    assert_violation(pace_violations(data), "n_segments cannot be added up, a value is not a whole number (invariant 3)")


# CL-B1-15: the min_segments checks run for every integer form that the schema accepts.
def speed_with_too_few_float(d):          # (i)
    by_id(d["pace_categories"], "seg_category", "C3").update(n_segments=1.0, speed_kmh=30.0, stop_ratio=0.0)


def speed_with_too_few_min_float(d):      # (ii)
    by_id(d["pace_categories"], "seg_category", "C3").update(speed_kmh=30.0, stop_ratio=0.0)
    d["pace_header"]["min_segments"] = 2.0


def no_speed_with_enough_float(d):        # (iii)
    by_id(d["pace_categories"], "seg_category", "C2").update(n_segments=2.0, speed_kmh=None, stop_ratio=None)


@pytest.mark.parametrize("round_trip", [False, True])   # (iv)
@pytest.mark.parametrize("change, fragment", [
    (speed_with_too_few_float, "C3 has speed_kmh with fewer than min_segments"),
    (speed_with_too_few_min_float, "C3 has speed_kmh with fewer than min_segments"),
    (no_speed_with_enough_float, "C2 has enough segments but speed_kmh is null"),
])
def test_min_segments_checks_count_whole_number_floats(data, change, fragment, round_trip):
    change(data)
    if round_trip:
        data = json_round_trip(data)
    assert_violation(pace_violations(data), fragment)


@pytest.mark.parametrize("round_trip", [False, True])
def test_a_correct_table_with_float_counts_passes_the_min_segments_checks(data, round_trip):   # (v)
    data["pace_header"]["min_segments"] = 2.0
    for rec in data["pace_categories"]:
        rec["n_segments"] = float(rec["n_segments"])
    if round_trip:
        data = json_round_trip(data)
    violations = pace_violations(data)
    assert not any("min_segments" in v or "enough segments" in v for v in violations), violations
    assert violations == []


@pytest.mark.parametrize("field, value", [("n_segments", 1.5), ("n_segments", True), ("n_segments", None),
                                          ("n_segments", "1"), ("n_segments", float("nan")),
                                          ("min_segments", 2.5), ("min_segments", True), ("min_segments", None),
                                          ("min_segments", "2"), ("min_segments", float("nan"))])
def test_a_count_the_min_segments_checks_cannot_use_is_still_a_violation(data, field, value):   # (vi)
    by_id(data["pace_categories"], "seg_category", "C3").update(speed_kmh=30.0, stop_ratio=0.0)
    if field == "n_segments":
        by_id(data["pace_categories"], "seg_category", "C3")["n_segments"] = value
    else:
        data["pace_header"]["min_segments"] = value
    assert pace_violations(data) != []


@pytest.mark.parametrize("round_trip", [False, True])
@pytest.mark.parametrize("indices, gap", [([0.0, 1.0, 7.0], True), ([0.0, 1.0, 2.0], False)])
def test_seg_index_gaps_are_found_with_float_indices(data, indices, gap, round_trip):   # (vii)
    rows = [r for r in data["derived_segments"] if r["trip_id"] == "T001"]
    for row, index in zip(sorted(rows, key=lambda r: r["seg_index"]), indices):
        row["seg_index"] = index
    if round_trip:
        data = json_round_trip(data)
    found = [v for v in validate_derived_segments(data["derived_segments"], "public")
             if "T001 seg_index is not 0..n-1 without gaps" in v]
    assert bool(found) is gap, found


@pytest.mark.parametrize("speed", [0, -10.0])
def test_speed_must_be_positive(data, speed):
    by_id(data["pace_categories"], "seg_category", "C1")["speed_kmh"] = speed
    assert_violation(pace_violations(data), "speed_kmh")


def test_other_methods_need_a_change_log_entry_first(data):
    data["pace_header"]["method"] = "median_length_weighted"
    assert_violation(pace_violations(data), "method")


# --- contract 4: ETA output, breaks and checkpoints -------------------------
def test_plan_id_must_be_unique(data):
    data["eta_headers"][1]["plan_id"] = "P-MOCK-1"
    assert_violation(eta_violations(data), "duplicate plan_id P-MOCK-1")


def test_segment_row_needs_a_known_plan(data):
    data["eta_segments"][0]["plan_id"] = "P-NOWHERE"
    assert_violation(eta_violations(data), "plan_id P-NOWHERE has no header")


@pytest.mark.parametrize("drop_last", [True, False])
def test_plan_has_exactly_n_rows(data, drop_last):
    rows = [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]
    if drop_last:
        data["eta_segments"].remove(rows[-1])                     # n - 1 rows
    else:
        data["eta_segments"].append({**rows[-1], "seg_index": 4})  # n + 1 rows
    assert_violation(eta_violations(data), "P-MOCK-1 needs seg_index 0..4-1 exactly once")


def test_break_delays_only_the_segments_after_its_checkpoint(data):
    """The break is at R01-CP03 (after_seg_count 2): rows 2 and 3 are delayed, rows 0 and 1 are not."""
    cps = [c for c in data["checkpoints"] if c["route_id"] == "R01"]
    assert expected_break_times(4, data["eta_headers"][0]["breaks"], cps) == [0.0, 0.0, 600.0, 600.0]


@pytest.mark.parametrize("wrong", [
    [0.0, 600.0, 600.0, 600.0],  # one segment too early
    [0.0, 0.0, 0.0, 600.0],      # one segment too late
])
def test_break_time_off_by_one_is_detected(data, wrong):
    rows = [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]
    for row, value in zip(rows, wrong):
        row["break_time_s"] = value
    assert_violation(eta_violations(data), "break_time_s should be")


@pytest.mark.parametrize("checkpoint_id", ["R01-CP01", "R01-CP02", "R01-CP05"])
def test_break_at_the_start_or_end_is_rejected(data, checkpoint_id):
    data["eta_headers"][0]["breaks"] = [{"after_checkpoint_id": checkpoint_id, "duration_s": 600.0}]
    assert_violation(eta_violations(data), "sits at the start or the end")


def test_break_must_use_a_checkpoint_of_the_same_route(data):
    data["eta_headers"][0]["breaks"] = [{"after_checkpoint_id": "R02-CP01", "duration_s": 600.0}]
    assert_violation(eta_violations(data), "not a checkpoint of R01")


def test_at_most_one_break_per_checkpoint(data):
    data["eta_headers"][0]["breaks"].append({"after_checkpoint_id": "R01-CP03", "duration_s": 60.0})
    assert_violation(eta_violations(data), "more than one break at R01-CP03")


@pytest.mark.parametrize("checkpoint_id, expected", [
    ("R01-CP01", ("2026-11-21T07:00:00+08:00", "2026-11-21T07:00:00+08:00")),  # c = 0: departure
    ("R01-CP02", ("2026-11-21T07:00:00+08:00", "2026-11-21T07:00:00+08:00")),  # station at the start
    ("R01-CP03", ("2026-11-21T07:05:09+08:00", "2026-11-21T07:06:11+08:00")),  # c = 2: row 1, before its own break
    ("R01-CP04", ("2026-11-21T07:19:27+08:00", "2026-11-21T07:21:20+08:00")),  # c = 3: row 2, after the break
    ("R01-CP05", ("2026-11-21T07:25:27+08:00", "2026-11-21T07:28:32+08:00")),  # c = n: last row
])
def test_checkpoint_arrival_uses_row_c_minus_one(data, checkpoint_id, expected):
    header = data["eta_headers"][0]
    checkpoint = by_id(data["checkpoints"], "checkpoint_id", checkpoint_id)
    assert checkpoint_arrival(header, data["eta_segments"], checkpoint) == expected


@pytest.mark.parametrize("column, value", [
    ("typ_seg_time_s", 120.0),
    ("eta_typ", "2026-11-21T07:10:00+08:00"),
    ("eta_safe", "2026-11-21T07:12:00+08:00"),
])
def test_unknown_plan_must_not_carry_any_time(data, column, value):
    row = next(s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-2")
    row[column] = value
    assert_violation(eta_violations(data), "carries a time although status is unknown")


def test_unknown_reason_goes_with_unknown_status(data):
    data["eta_headers"][1]["unknown_reason"] = None
    assert_violation(eta_violations(data), "P-MOCK-2 unknown_reason must be set exactly when status is unknown")
    data["eta_headers"][0]["unknown_reason"] = "something"
    assert_violation(eta_violations(data), "P-MOCK-1 unknown_reason must be set exactly when status is unknown")


def test_ok_plan_cannot_use_a_category_without_pace(data):
    """R02 has a C3 segment and C3 has no pace, so a plan on R02 cannot be ok."""
    header = data["eta_headers"][1]
    header.update(status="ok", unknown_reason=None)
    assert_violation(eta_violations(data), "category without pace")


def test_ok_plan_needs_every_time(data):
    data["eta_segments"][1]["eta_safe"] = None
    assert_violation(eta_violations(data), "null time although status is ok")


def test_eta_must_follow_the_formula(data):
    data["eta_segments"][2]["eta_typ"] = "2026-11-21T07:09:27+08:00"  # as if the break were not counted
    assert_violation(eta_violations(data), "eta_typ is not departure + cumulative time + break_time_s")
    data["eta_segments"][3]["eta_safe"] = "2026-11-21T07:25:30+08:00"
    assert_violation(eta_violations(data), "eta_safe is not eta_typ + margin_coeff x cumulative time")


def test_eta_safe_is_never_earlier_than_eta_typ(data):
    data["eta_segments"][0]["eta_safe"] = "2026-11-21T07:02:00+08:00"
    assert_violation(eta_violations(data), "eta_safe is earlier than eta_typ")


def test_eta_keeps_its_references(data):
    for column in ("route_id", "departure_time", "pace_version", "catalog_version", "unknown_reason"):
        assert all(column in h for h in data["eta_headers"])
    data["eta_headers"][0]["catalog_version"] = "catalog-other"
    assert_violation(eta_violations(data), "catalog_version differs")
    data["eta_headers"][1]["pace_version"] = "pace-other"
    assert_violation(eta_violations(data), "pace_version differs")


# --- v0.3 stop allowance (Issue #7; SPEC-RESOLUTION-001 1.4) -----------------
def ok_rows(d: dict) -> list[dict]:
    return [s for s in d["eta_segments"] if s["plan_id"] == "P-MOCK-1"]


# contract 1: short_stop_time_s
def test_short_stops_cannot_exceed_all_stops(data):
    row = by_id(data["derived_segments"], "stopped_time_s", 12.0)
    row["short_stop_time_s"] = 12.5
    assert_violation(validate_derived_segments(data["derived_segments"]), "short_stop_time_s is greater than stopped_time_s")


def test_short_stops_may_equal_all_stops(data):
    row = by_id(data["derived_segments"], "stopped_time_s", 12.0)
    assert row["short_stop_time_s"] == row["stopped_time_s"]
    assert validate_derived_segments(data["derived_segments"]) == []


def test_short_stops_above_zero_stops_are_rejected(data):
    data["derived_segments"][0]["short_stop_time_s"] = 3.0  # stopped_time_s is 0
    assert_violation(validate_derived_segments(data["derived_segments"]), "short_stop_time_s is greater than stopped_time_s")


@pytest.mark.parametrize("value", [-1.0, None, "0"])
def test_short_stop_time_is_a_non_negative_number(data, value):
    data["derived_segments"][0]["short_stop_time_s"] = value
    assert_violation(validate_derived_segments(data["derived_segments"]), "short_stop_time_s")


@pytest.mark.parametrize("visibility", ["public", "private"])
def test_short_stop_time_is_required_in_both_versions(data, private_rows, visibility):
    rows = data["derived_segments"] if visibility == "public" else private_rows
    del rows[0]["short_stop_time_s"]
    assert_violation(validate_derived_segments(rows, visibility), "'short_stop_time_s' is a required property")


# contract 3: stop_ratio, margin_coeff, margin_basis, pace_version
def test_stop_ratio_must_be_null_when_speed_is_null(data):
    by_id(data["pace_categories"], "seg_category", "C3")["stop_ratio"] = 0.1
    assert_violation(pace_violations(data), "C3 stop_ratio must be null exactly when speed_kmh is null")


def test_stop_ratio_must_have_a_value_when_speed_has_one(data):
    by_id(data["pace_categories"], "seg_category", "C2")["stop_ratio"] = None
    assert_violation(pace_violations(data), "C2 stop_ratio must be null exactly when speed_kmh is null")


def test_stop_ratio_may_be_zero(data):
    assert by_id(data["pace_categories"], "seg_category", "C1")["stop_ratio"] == 0.0
    assert pace_violations(data) == []


@pytest.mark.parametrize("value", [-0.01, "0.1"])
def test_stop_ratio_is_a_non_negative_number(data, value):
    by_id(data["pace_categories"], "seg_category", "C1")["stop_ratio"] = value
    assert_violation(pace_violations(data), "stop_ratio")


def test_stop_ratio_is_required(data):
    del by_id(data["pace_categories"], "seg_category", "C1")["stop_ratio"]
    assert_violation(pace_violations(data), "'stop_ratio' is a required property")


@pytest.mark.parametrize("basis", ["LOO_RULE", "loo", "fixed", None, ""])
def test_margin_basis_has_two_values_only(data, basis):
    data["pace_header"]["margin_basis"] = basis
    assert_violation(pace_violations(data), "margin_basis")


@pytest.mark.parametrize("field", ["margin_coeff", "margin_basis"])
def test_margin_fields_are_required(data, field):
    del data["pace_header"][field]
    assert_violation(pace_violations(data), f"'{field}' is a required property")


@pytest.mark.parametrize("coeff", [0.05, 0.25, 0.15, 0.3])
def test_default_margin_must_be_0_20(data, coeff):
    data["pace_header"]["margin_coeff"] = coeff
    data["eta_headers"][0]["margin_coeff"] = data["eta_headers"][1]["margin_coeff"] = coeff
    assert_violation(pace_violations(data), "margin_basis is default but margin_coeff")


@pytest.mark.parametrize("coeff", [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.45, 0.55, 0.7, 1.15, 2.0])
def test_loo_rule_margin_accepts_multiples_of_0_05(data, coeff):
    data["pace_header"].update(margin_basis="loo_rule", margin_coeff=coeff)
    assert pace_violations(data) == []


@pytest.mark.parametrize("coeff, fragment", [
    (0.12, "not a multiple of 0.05"),
    (0.149, "not a multiple of 0.05"),
    (0.051, "not a multiple of 0.05"),
    (0.04, "margin_coeff"),   # below the lower bound (schema)
    (0.0, "margin_coeff"),
    (-0.05, "margin_coeff"),
])
def test_loo_rule_margin_rejects_other_values(data, coeff, fragment):
    data["pace_header"].update(margin_basis="loo_rule", margin_coeff=coeff)
    assert_violation(pace_violations(data), fragment)


@pytest.mark.parametrize("coeff", ["0.2", None, True])
def test_margin_coeff_is_a_number(data, coeff):
    data["pace_header"]["margin_coeff"] = coeff
    assert_violation(pace_violations(data), "margin_coeff")


@pytest.mark.parametrize("version", ["research-01", "user-01", "user-10", "research-007", "user-12345"])
def test_pace_version_pattern_accepts_research_and_user(data, version):
    data["pace_header"]["pace_version"] = version
    for rec in data["pace_categories"]:
        rec["pace_version"] = version
    assert validate_pace_table(data["pace_header"], data["pace_categories"], data["derived_segments"]) == []


@pytest.mark.parametrize("version", [
    "pace-mock-1", "user-1", "user-", "research", "User-01", "RESEARCH-01", "user_01", "user01",
    "user-01a", "user-0x1", " user-01", "user-01 ", "user-01\n", "user-\uff10\uff11", "frozen-01", "user-01-02",
])
def test_pace_version_pattern_rejects_other_strings(data, version):
    data["pace_header"]["pace_version"] = version
    for rec in data["pace_categories"]:
        rec["pace_version"] = version
    assert_violation(pace_violations(data), "(invariant 7)")


# contract 4: stop_allow_s and invariants 6, 8, 9
def test_stop_allow_is_stop_ratio_times_typical_time(data):
    ok_rows(data)[1]["stop_allow_s"] = 20.0  # C2: 0.075 x 120 = 9
    assert_violation(eta_violations(data), "P-MOCK-1 seg 1 stop_allow_s is not stop_ratio x typ_seg_time_s")


@pytest.mark.parametrize("allowance, rejected", [(9.5, False), (8.5, False), (10.5, True), (7.5, True)])
def test_stop_allow_tolerates_one_second(data, allowance, rejected):
    ok_rows(data)[1]["stop_allow_s"] = allowance
    found = [v for v in eta_violations(data) if "stop_allow_s is not stop_ratio" in v]
    assert bool(found) is rejected, found


def test_eta_without_stop_allowance_is_rejected(data):
    """A v0.2-style ETA (no allowance in the times) cannot pass as v0.3 by writing stop_allow_s = 0."""
    for row, (typ, safe) in zip(ok_rows(data), [("07:03:00", "07:03:36"), ("07:05:00", "07:06:00"),
                                               ("07:19:00", "07:20:48"), ("07:25:00", "07:28:00")]):
        row.update(stop_allow_s=0.0, eta_typ=f"2026-11-21T{typ}+08:00", eta_safe=f"2026-11-21T{safe}+08:00")
    violations = eta_violations(data)
    assert_violation(violations, "P-MOCK-1 seg 1 stop_allow_s is not stop_ratio x typ_seg_time_s")
    assert_violation(violations, "P-MOCK-1 seg 2 stop_allow_s is not stop_ratio x typ_seg_time_s")


def test_eta_typ_steps_follow_typical_time_allowance_and_new_breaks(data):
    """Each eta_typ is within one second of its own target, but the step between them is two seconds off."""
    rows = ok_rows(data)
    rows[1]["eta_typ"] = "2026-11-21T07:05:10+08:00"   # +1 s
    rows[2]["eta_typ"] = "2026-11-21T07:19:26+08:00"   # -1 s
    violations = eta_violations(data)
    assert_violation(violations, "P-MOCK-1 seg 2 eta_typ minus the previous eta_typ is not")
    assert not any("eta_typ is not departure" in v for v in violations), violations


def test_eta_typ_step_counts_a_new_break_once(data):
    """Row 2 starts after the 600 s break; dropping the break from rows 2 and 3 breaks the step at row 2."""
    rows = ok_rows(data)
    rows[2]["eta_typ"], rows[2]["eta_safe"] = "2026-11-21T07:09:27+08:00", "2026-11-21T07:11:20+08:00"
    rows[3]["eta_typ"], rows[3]["eta_safe"] = "2026-11-21T07:15:27+08:00", "2026-11-21T07:18:32+08:00"
    assert_violation(eta_violations(data), "P-MOCK-1 seg 2 eta_typ minus the previous eta_typ is not")


def test_eta_safe_margin_covers_the_allowance(data):
    """The margin is applied to typ_seg_time_s + stop_allow_s, not to typ_seg_time_s alone."""
    rows = ok_rows(data)
    rows[2]["eta_safe"] = "2026-11-21T07:21:15+08:00"  # 0.2 x 540 = 108 s after eta_typ: allowance left out
    assert_violation(eta_violations(data), "P-MOCK-1 seg 2 eta_safe - eta_typ is not margin_coeff x cumulative")


def test_eta_safe_margin_tolerates_one_second(data):
    rows = ok_rows(data)
    rows[2]["eta_safe"] = "2026-11-21T07:21:21+08:00"  # 114 s after eta_typ; 0.2 x 567 = 113.4
    assert not any("eta_safe - eta_typ" in v for v in eta_violations(data))
    rows[2]["eta_safe"] = "2026-11-21T07:21:22+08:00"  # 115 s
    assert_violation(eta_violations(data), "P-MOCK-1 seg 2 eta_safe - eta_typ is not")


def test_ok_plan_needs_a_stop_allowance(data):
    ok_rows(data)[1]["stop_allow_s"] = None
    assert_violation(eta_violations(data), "P-MOCK-1 seg 1 has a null time although status is ok")


@pytest.mark.parametrize("value", [-1.0, "9"])
def test_stop_allow_is_a_non_negative_number(data, value):
    ok_rows(data)[1]["stop_allow_s"] = value
    assert_violation(eta_violations(data), "stop_allow_s")


def test_stop_allow_is_required(data):
    del ok_rows(data)[0]["stop_allow_s"]
    assert_violation(eta_violations(data), "'stop_allow_s' is a required property")


@pytest.mark.parametrize("value", [0.0, 9.0])
def test_unknown_plan_must_not_carry_a_stop_allowance(data, value):
    """No partial estimate when the ETA is unknown: not even an allowance of 0."""
    row = next(s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-2")
    row["stop_allow_s"] = value
    assert_violation(eta_violations(data), "P-MOCK-2 seg 0 carries a time although status is unknown")


def test_unknown_plan_with_every_time_null_passes(data):
    rows = [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-2"]
    assert all(r["stop_allow_s"] is None and r["eta_typ"] is None and r["eta_safe"] is None for r in rows)
    assert not any("P-MOCK-2" in v for v in eta_violations(data))


def test_stop_allow_needs_the_category_stop_ratio(data):
    """If the pace table has no stop_ratio for a category the ETA uses, stop_allow_s is not accepted unchecked."""
    by_id(data["pace_categories"], "seg_category", "C2")["stop_ratio"] = None
    assert_violation(eta_violations(data), "P-MOCK-1 seg 1 stop_allow_s cannot be checked: category C2 has no stop_ratio")


def test_eta_without_a_pace_table_checks_the_times_only(data):
    """stop_allow_s = stop_ratio x typ_seg_time_s needs the pace table; the time invariants do not."""
    args = (data["eta_headers"], data["eta_segments"], data["routes"], data["route_segments"], data["checkpoints"])
    assert validate_eta_output(*args) == []
    ok_rows(data)[1]["stop_allow_s"] = 20.0
    violations = validate_eta_output(*args)
    assert not any("stop_ratio" in v for v in violations)
    assert_violation(violations, "P-MOCK-1 seg 1 eta_typ is not departure + cumulative time + break_time_s")


@pytest.mark.parametrize("plan", [0, 1])
def test_eta_margin_must_equal_the_pace_table_margin(data, plan):
    data["eta_headers"][plan]["margin_coeff"] = 0.25
    assert_violation(eta_violations(data), f"{data['eta_headers'][plan]['plan_id']} margin_coeff 0.25 differs from "
                                           f"the pace table's 0.2 (invariant 9)")


def test_eta_margin_is_checked_against_the_pace_table_in_the_dataset(data):
    data["pace_header"].update(margin_basis="loo_rule", margin_coeff=0.15)
    report = validate_dataset(data)
    assert report["pace_table"] == []
    assert_violation(report["eta_output"], "P-MOCK-1 margin_coeff 0.2 differs from the pace table's 0.15")


def test_eta_margin_against_a_pace_table_without_margin_is_rejected(data):
    del data["pace_header"]["margin_coeff"]
    assert_violation(eta_violations(data), "differs from the pace table's None (invariant 9)")


@pytest.mark.parametrize("coeff", [0.0, 0.04, -0.2])
def test_eta_margin_is_at_least_0_05(data, coeff):
    data["eta_headers"][1]["margin_coeff"] = coeff
    args = (data["eta_headers"], data["eta_segments"], data["routes"], data["route_segments"], data["checkpoints"])
    assert_violation(validate_eta_output(*args), "eta_headers[1] schema: margin_coeff")


def test_eta_margin_of_0_05_is_allowed(data):
    data["pace_header"].update(margin_basis="loo_rule", margin_coeff=0.05)
    for header in data["eta_headers"]:
        header["margin_coeff"] = 0.05
    rows = ok_rows(data)
    for row, safe in zip(rows, ["07:03:09", "07:05:24", "07:19:55", "07:26:13"]):
        row["eta_safe"] = f"2026-11-21T{safe}+08:00"
    assert eta_violations(data) == []


# --- R1-F1 (issue-7-c1-r1): non-finite numbers in the v0.3 fields ------------
NON_FINITE = [float("nan"), float("inf"), float("-inf")]


def target_of(d: dict, where: str) -> dict:
    return {"derived": d["derived_segments"][0], "pace_category": by_id(d["pace_categories"], "seg_category", "C2"),
            "pace_header": d["pace_header"], "eta_header": d["eta_headers"][0],
            "eta_ok_row": ok_rows(d)[1], "eta_unknown_row": d["eta_segments"][4]}[where]


@pytest.mark.parametrize("value", NON_FINITE, ids=["nan", "inf", "-inf"])
@pytest.mark.parametrize("where, field, report_key, label", [
    ("derived", "short_stop_time_s", "derived_segments", "derived_segments(public)[0]"),
    ("pace_category", "stop_ratio", "pace_table", "pace_categories[1]"),
    ("pace_header", "margin_coeff", "pace_table", "pace_header[0]"),
    ("eta_header", "margin_coeff", "eta_output", "eta_headers[0]"),
    ("eta_ok_row", "stop_allow_s", "eta_output", "eta_segments[1]"),
    ("eta_unknown_row", "stop_allow_s", "eta_output", "eta_segments[4]"),
])
def test_non_finite_values_in_the_v03_fields_are_rejected(data, where, field, report_key, label, value):
    """validate_dataset returns a violation (and does not raise) for NaN and +/-infinity."""
    target_of(data, where)[field] = value
    report = validate_dataset(data)
    assert_violation(report[report_key], f"{label}: {field} is not a finite number")


@pytest.mark.parametrize("value", NON_FINITE, ids=["nan", "inf", "-inf"])
def test_non_finite_short_stops_are_rejected_on_their_own(data, value):
    data["derived_segments"][0]["short_stop_time_s"] = value
    assert_violation(validate_derived_segments(data["derived_segments"]), "short_stop_time_s is not a finite number")


@pytest.mark.parametrize("value", NON_FINITE, ids=["nan", "inf", "-inf"])
@pytest.mark.parametrize("basis", ["default", "loo_rule"])
def test_non_finite_margin_is_rejected_by_the_pace_table_alone(data, basis, value):
    data["pace_header"].update(margin_basis=basis, margin_coeff=value)
    assert_violation(validate_pace_table(data["pace_header"], data["pace_categories"], data["derived_segments"]),
                     "pace_header[0]: margin_coeff is not a finite number")


@pytest.mark.parametrize("value", NON_FINITE, ids=["nan", "inf", "-inf"])
def test_non_finite_stop_ratio_does_not_let_the_eta_pass(data, value):
    """Without the pace table check, the ETA itself must not accept a stop allowance it cannot verify."""
    by_id(data["pace_categories"], "seg_category", "C2")["stop_ratio"] = value
    assert_violation(eta_violations(data), "P-MOCK-1 seg 1 stop_allow_s cannot be checked: category C2 has a non-finite stop_ratio")


@pytest.mark.parametrize("value", NON_FINITE, ids=["nan", "inf", "-inf"])
def test_non_finite_eta_values_give_violations_without_a_pace_table(data, value):
    args = (data["eta_headers"], data["eta_segments"], data["routes"], data["route_segments"], data["checkpoints"])
    ok_rows(data)[1]["stop_allow_s"] = value
    assert_violation(validate_eta_output(*args), "eta_segments[1]: stop_allow_s is not a finite number")
    ok_rows(data)[1]["stop_allow_s"] = 9.0
    data["eta_headers"][0]["margin_coeff"] = value
    assert_violation(validate_eta_output(*args), "eta_headers[0]: margin_coeff is not a finite number")


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_literals_parsed_from_json_text_are_rejected(literal):
    """json.loads (used by the contracts CLI) accepts these non-standard literals; the validators must not."""
    from conftest import MOCK_DATASET
    text = MOCK_DATASET.read_text(encoding="utf-8").replace('"stop_ratio": 0.075', f'"stop_ratio": {literal}', 1)
    assert f'"stop_ratio": {literal}' in text
    report = validate_dataset(json.loads(text))
    assert_violation(report["pace_table"], "pace_categories[1]: stop_ratio is not a finite number")
    assert_violation(report["eta_output"], "has a non-finite stop_ratio")


# --- v0.3 IDs and contract 2 (SPEC-R1 R1-1, Issue #13; SPEC-001 §2, S37, S58) -------
# Synthetic IDs: the hex digits are invented, not taken from any snapshot or GPX file.
HEX_A, HEX_B = "a1b2c3d4e5", "0f9e8d7c6b"
RS_A, RG_B, SN_A = f"RS-{HEX_A}", f"RG-{HEX_B}", f"SN-{HEX_A}"
ROUTING = {"route_source": "routing", "source_trip_id": None, "snapshot_id": SN_A}
TARGET_GPX = {"route_source": "target_gpx", "source_trip_id": None, "snapshot_id": None}


def rename_route(d: dict, old: str, new: str, **fields) -> dict:
    """Give route `old` the route_id `new` everywhere (contracts 1, 2 and 4), with its checkpoint_ids."""
    def renamed(cid: str) -> str:
        return new + cid[len(old):] if cid.startswith(old + "-CP") else cid
    for route in d["routes"]:
        if route["route_id"] == old:
            route.update(route_id=new, **fields)
    for rec in d["route_segments"] + d["checkpoints"] + d["derived_segments"] + d["eta_headers"]:
        if rec.get("route_id") == old:
            rec["route_id"] = new
    for c in d["checkpoints"]:
        c["checkpoint_id"] = renamed(c["checkpoint_id"])
    for h in d["eta_headers"]:
        for b in h["breaks"]:
            b["after_checkpoint_id"] = renamed(b["after_checkpoint_id"])
    return d


def all_violations(d: dict) -> list[str]:
    return [v for violations in validate_dataset(d).values() for v in violations]


def test_r01_and_r02_stay_valid_trip_routes(data):
    """AC (1), (5): the demo routes keep their IDs; they are one-way routes taken from a trip."""
    assert [(r["route_id"], r["route_source"], r["snapshot_id"], r["trip_type"]) for r in data["routes"]] == \
        [("R01", "trip", None, "one_way"), ("R02", "trip", None, "one_way")]
    assert all_violations(data) == []


@pytest.mark.parametrize("old, new, fields", [
    ("R01", RS_A, ROUTING), ("R01", RG_B, TARGET_GPX), ("R01", "R99", {}),
    ("R02", RS_A, ROUTING), ("R02", RG_B, TARGET_GPX),
])
def test_s37_s58_every_route_id_format_passes_in_contracts_1_2_and_4(data, old, new, fields):
    """AC (1): RS-, RG- and R + two digits are accepted in contract 1 route_id, all of contract 2, and
    contract 4 route_id and breaks[].after_checkpoint_id (R01 carries derived rows and the ETA break)."""
    rename_route(data, old, new, **fields)
    assert all_violations(data) == []
    if old == "R01":
        assert {r["route_id"] for r in data["derived_segments"] if r["trip_id"] == "T002"} == {new}
        assert data["eta_headers"][0]["route_id"] == new
        assert data["eta_headers"][0]["breaks"][0]["after_checkpoint_id"] == f"{new}-CP03"


def test_routes_of_all_three_sources_in_one_catalog(data):
    rename_route(data, "R01", RS_A, **ROUTING)
    rename_route(data, "R02", RG_B, **TARGET_GPX)
    data["routes"].append({**data["routes"][1], "route_id": "R03", "route_source": "trip", "source_trip_id": "T001"})
    data["route_segments"] += [{**s, "route_id": "R03"} for s in data["route_segments"] if s["route_id"] == RG_B]
    data["checkpoints"] += [{**c, "route_id": "R03", "checkpoint_id": "R03" + c["checkpoint_id"][len(RG_B):]}
                            for c in data["checkpoints"] if c["route_id"] == RG_B]
    assert all_violations(data) == []


@pytest.mark.parametrize("suffix", ["CP04", "CP99", "CP100", "CP999"])
@pytest.mark.parametrize("route_id, fields", [("R01", {}), (RS_A, ROUTING), (RG_B, TARGET_GPX)])
def test_checkpoint_id_has_two_or_three_digits(data, route_id, fields, suffix):
    rename_route(data, "R01", route_id, **fields)
    by_id(data["checkpoints"], "checkpoint_id", f"{route_id}-CP04")["checkpoint_id"] = f"{route_id}-{suffix}"
    assert all_violations(data) == []


def test_a_break_may_use_a_three_digit_checkpoint(data):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP03")["checkpoint_id"] = "R01-CP103"
    data["eta_headers"][0]["breaks"][0]["after_checkpoint_id"] = "R01-CP103"
    assert all_violations(data) == []


BAD_ROUTE_IDS = [
    "R1", "R001", "r01", "R0a", "R-01", f"RS-{HEX_A[:9]}", f"RS-{HEX_A}f", f"RS-{HEX_A.upper()}", f"RX-{HEX_A}",
    f"RS_{HEX_A}", f"RS{HEX_A}", f"RG-{HEX_A[:9]}g", f"rs-{HEX_A}", SN_A, "T001", "", " R01", "R01 ", "R01\n",
    f"{RS_A}\n", "R\u0660\u0661", "R\uff10\uff11", "R01-CP01",
]


@pytest.mark.parametrize("bad", BAD_ROUTE_IDS)
@pytest.mark.parametrize("records, index, label", [
    ("routes", 1, "routes[1]"),
    ("route_segments", 0, "route_segments[0]"),
    ("checkpoints", 0, "checkpoints[0]"),
    ("derived_segments", 3, "derived_segments(public)[3]"),
    ("eta_headers", 0, "eta_headers[0]"),
])
def test_s37_s58_a_route_id_of_another_format_is_rejected(data, records, index, label, bad):
    """AC (1): contract 1 route_id, contract 2 (routes, route segments, checkpoints) and contract 4 route_id."""
    data[records][index]["route_id"] = bad
    assert_violation(all_violations(data), f"{label} schema: route_id")


BAD_CHECKPOINT_IDS = [
    "R01-CP4", "R01-CP1000", "R01-cp04", "R01CP04", "R01-CP 4", "R01-WP04", "R01-CP04-CP05", "-CP04", "R1-CP04",
    f"RS-{HEX_A.upper()}-CP04", f"RS-{HEX_A[:9]}-CP04", "R01-CP04\n", "R01-CP\u0660\u0664", "R01-CP\uff10\uff14", "R01",
]


@pytest.mark.parametrize("bad", BAD_CHECKPOINT_IDS)
def test_s37_s58_a_checkpoint_id_of_another_format_is_rejected(data, bad):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["checkpoint_id"] = bad
    assert_violation(catalog_violations(data), "checkpoints[3] schema: checkpoint_id")


@pytest.mark.parametrize("bad", BAD_CHECKPOINT_IDS)
def test_s37_s58_a_break_at_a_checkpoint_id_of_another_format_is_rejected(data, bad):
    data["eta_headers"][0]["breaks"][0]["after_checkpoint_id"] = bad
    assert_violation(eta_violations(data), "eta_headers[0] schema: breaks/0/after_checkpoint_id")


@pytest.mark.parametrize("bad", [
    f"SN-{HEX_A[:9]}", f"SN-{HEX_A}f", f"SN-{HEX_A.upper()}", f"sn-{HEX_A}", f"SN_{HEX_A}", f"SN{HEX_A}",
    f"SN-{HEX_A[:9]}g", RS_A, "", f"{SN_A}\n", f" {SN_A}", "SN-\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669",
])
def test_s58_a_snapshot_id_of_another_format_is_rejected(data, bad):
    rename_route(data, "R02", RS_A, **{**ROUTING, "snapshot_id": bad})
    assert_violation(catalog_violations(data), "routes[1] schema: snapshot_id")


# AC (2): the checkpoint_id prefix is its own route_id.
@pytest.mark.parametrize("checkpoint_id", ["R02-CP09", "R10-CP04", f"{RS_A}-CP04", f"{RG_B}-CP104"])
def test_checkpoint_id_starts_with_its_route_id(data, checkpoint_id):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["checkpoint_id"] = checkpoint_id
    assert_violation(catalog_violations(data), f"checkpoints: {checkpoint_id} does not start with its route_id R01")


@pytest.mark.parametrize("checkpoint_id", ["R02-CP01", f"RS-{HEX_B}-CP01", f"RG-{HEX_A}-CP01"])
def test_checkpoint_id_of_an_rs_route_starts_with_that_route_id(data, checkpoint_id):
    rename_route(data, "R02", RS_A, **ROUTING)
    by_id(data["checkpoints"], "checkpoint_id", f"{RS_A}-CP01")["checkpoint_id"] = checkpoint_id
    assert_violation(catalog_violations(data), f"checkpoints: {checkpoint_id} does not start with its route_id {RS_A}")


# AC (3): route_source agrees with the route_id format; an RS- route_id has its snapshot_id's hex digits.
@pytest.mark.parametrize("route_id, fields", [
    (RS_A, {}), (RG_B, {}),                     # trip
    ("R02", ROUTING), (RG_B, ROUTING),          # routing
    ("R02", TARGET_GPX), (RS_A, TARGET_GPX),    # target_gpx
])
def test_route_id_format_must_agree_with_route_source(data, route_id, fields):
    rename_route(data, "R02", route_id, **fields)
    source = fields.get("route_source", "trip")
    violations = catalog_violations(data)
    assert_violation(violations, f"routes: route_id {route_id} does not have the format for route_source {source}")
    assert not any("(invariant 5)" in v or "schema" in v for v in violations), violations


def test_rs_route_id_has_the_hex_digits_of_its_snapshot_id(data):
    rename_route(data, "R02", RS_A, **{**ROUTING, "snapshot_id": f"SN-{HEX_B}"})
    assert_violation(catalog_violations(data),
                     f"routes: {RS_A} and its snapshot_id SN-{HEX_B} do not have the same 10 hex digits")
    by_id(data["routes"], "route_id", RS_A)["snapshot_id"] = SN_A
    assert catalog_violations(data) == []


# AC (4): one violating case for each of contract 2 invariants 1-5 (4 and 5 are new in v0.3).
def make_round_trip(d: dict, at=2, checkpoint_id: str = "R01-CP06") -> dict:
    by_id(d["routes"], "route_id", "R01")["trip_type"] = "round_trip"
    d["checkpoints"].append({"checkpoint_id": checkpoint_id, "route_id": "R01", "kind": "turnaround",
                             "after_seg_count": at, "name": None, "station_ref": None})
    return d


def violate_invariant_1(d):
    by_id(d["checkpoints"], "checkpoint_id", "R01-CP01")["kind"] = "waypoint"


def violate_invariant_2(d):
    by_id(d["checkpoints"], "checkpoint_id", "R01-CP04")["after_seg_count"] = 5


def violate_invariant_3(d):
    """Checkpoints at one position are told apart by checkpoint_id: two with the same one are not."""
    by_id(d["checkpoints"], "checkpoint_id", "R01-CP02")["checkpoint_id"] = "R01-CP01"


def violate_invariant_4(d):
    by_id(d["routes"], "route_id", "R01")["trip_type"] = "round_trip"   # without a turnaround


def violate_invariant_5(d):
    by_id(d["routes"], "route_id", "R01")["snapshot_id"] = SN_A        # a trip route pointing at a snapshot


@pytest.mark.parametrize("change, fragment", [
    (violate_invariant_1, "checkpoints: R01 must have exactly one start, found 0 (invariant 1)"),
    (violate_invariant_2, "checkpoints: R01-CP04 after_seg_count 5 is outside 0..4 (invariant 2)"),
    (violate_invariant_3, "checkpoints: duplicate primary key R01-CP01"),
    (violate_invariant_4, "checkpoints: R01 is round_trip and needs exactly one turnaround, found 0 (invariant 4)"),
    (violate_invariant_5, "routes: R01 route_source is trip, so snapshot_id must be null (invariant 5)"),
])
def test_each_contract_2_invariant_has_a_rejected_violation(data, change, fragment):
    assert catalog_violations(data) == []
    change(data)
    assert_violation(catalog_violations(data), fragment)


@pytest.mark.parametrize("round_trip", [False, True])
@pytest.mark.parametrize("count, n, outside", [
    (9.0, 4, True), (5.0, 4, True), (5, 4.0, True), (5.0, 4.0, True),
    (3.0, 4, False), (4.0, 4.0, False), (0.0, 4, False), (3, 4.0, False),
])
def test_invariant_2_counts_whole_number_floats(data, count, n, outside, round_trip):
    """CL-R1-11: after_seg_count and n_segments are counted with _whole_count, also after a JSON round trip."""
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["after_seg_count"] = count
    by_id(data["routes"], "route_id", "R01")["n_segments"] = n
    if round_trip:
        data = json_round_trip(data)
        assert isinstance(by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["after_seg_count"], type(count))
    violations = catalog_violations(data)
    found = [v for v in violations if "R01-CP04 after_seg_count" in v and "(invariant 2)" in v]
    assert bool(found) is outside, violations
    if not outside:
        assert violations == []


@pytest.mark.parametrize("value", [1.5, True, None, "3", float("nan"), float("inf"), -1.0])
def test_an_after_seg_count_that_cannot_be_counted_is_still_a_violation(data, value):
    by_id(data["checkpoints"], "checkpoint_id", "R01-CP04")["after_seg_count"] = value
    assert_violation(catalog_violations(data), "checkpoints[3] schema: after_seg_count")


@pytest.mark.parametrize("at", [1, 2, 3, 2.0])
def test_round_trip_with_one_turnaround_inside_the_route_passes(data, at):
    make_round_trip(data, at=at)
    assert catalog_violations(data) == []
    assert catalog_violations(json_round_trip(data)) == []


def test_a_break_may_be_at_the_turnaround(data):
    """The turnaround (after_seg_count 2) replaces R01-CP03 (also 2) as the break checkpoint."""
    make_round_trip(data, at=2)
    data["eta_headers"][0]["breaks"] = [{"after_checkpoint_id": "R01-CP06", "duration_s": 600.0}]
    assert all_violations(data) == []


def two_turnarounds(d):
    make_round_trip(d, at=1)
    d["checkpoints"].append({**d["checkpoints"][-1], "checkpoint_id": "R01-CP07", "after_seg_count": 3})


@pytest.mark.parametrize("change, fragment", [
    (lambda d: make_round_trip(d, at=0), "R01-CP06 is the turnaround but after_seg_count 0 is not between 0 and 4"),
    (lambda d: make_round_trip(d, at=4), "R01-CP06 is the turnaround but after_seg_count 4 is not between 0 and 4"),
    (lambda d: make_round_trip(d, at=4.0), "R01-CP06 is the turnaround but after_seg_count 4.0 is not between 0 and 4"),
    (lambda d: make_round_trip(d, at=0.0), "R01-CP06 is the turnaround but after_seg_count 0.0 is not between 0 and 4"),
    (two_turnarounds, "R01 is round_trip and needs exactly one turnaround, found 2 (invariant 4)"),
    (violate_invariant_4, "R01 is round_trip and needs exactly one turnaround, found 0 (invariant 4)"),
])
@pytest.mark.parametrize("round_trip", [False, True])
def test_invariant_4_round_trip_needs_one_turnaround_strictly_inside(data, change, fragment, round_trip):
    change(data)
    if round_trip:
        data = json_round_trip(data)
    assert_violation(catalog_violations(data), fragment)


def test_invariant_4_one_way_route_has_no_turnaround(data):
    make_round_trip(data, at=2)
    by_id(data["routes"], "route_id", "R01")["trip_type"] = "one_way"
    assert_violation(catalog_violations(data), "checkpoints: R01 is one_way but has 1 turnaround(s) (invariant 4)")


@pytest.mark.parametrize("route_id, fields, field, value, must_be", [
    ("R02", {}, "source_trip_id", None, "set"),                       # trip
    ("R02", {}, "snapshot_id", SN_A, "null"),
    (RS_A, ROUTING, "snapshot_id", None, "set"),                      # routing
    (RS_A, ROUTING, "source_trip_id", "T002", "null"),
    (RG_B, TARGET_GPX, "source_trip_id", "T002", "null"),             # target_gpx
    (RG_B, TARGET_GPX, "snapshot_id", SN_A, "null"),
])
def test_invariant_5_route_source_decides_which_reference_is_set(data, route_id, fields, field, value, must_be):
    rename_route(data, "R02", route_id, **fields)
    by_id(data["routes"], "route_id", route_id)[field] = value
    source = fields.get("route_source", "trip")
    assert_violation(catalog_violations(data),
                     f"routes: {route_id} route_source is {source}, so {field} must be {must_be} (invariant 5)")


# v0.3 fields of the route record: required, with fixed values.
@pytest.mark.parametrize("field", ["route_source", "snapshot_id", "trip_type", "source_trip_id"])
def test_a_v02_route_record_without_the_v03_fields_is_rejected(data, field):
    del by_id(data["routes"], "route_id", "R02")[field]
    assert_violation(catalog_violations(data), f"routes[1] schema: (record): '{field}' is a required property")


@pytest.mark.parametrize("field, value", [
    ("route_source", "Trip"), ("route_source", "gpx"), ("route_source", ""), ("route_source", None),
    ("trip_type", "oneway"), ("trip_type", "ROUND_TRIP"), ("trip_type", "loop"), ("trip_type", None),
    ("source_trip_id", "T01"), ("source_trip_id", ""),
])
def test_route_source_and_trip_type_have_fixed_values(data, field, value):
    by_id(data["routes"], "route_id", "R02")[field] = value
    assert_violation(catalog_violations(data), f"routes[1] schema: {field}")


@pytest.mark.parametrize("value", [[], {}, ["trip"], {"trip": "trip"}], ids=["list", "dict", "list-trip", "dict-trip"])
def test_a_route_source_of_another_json_type_is_reported_not_raised(data, value):
    """R1-F1 (issue-13-c1-r1): an unhashable route_source after a JSON round trip is a schema violation of
    that route; the route_source cross-checks are skipped, and neither API raises."""
    by_id(data["routes"], "route_id", "R01")["route_source"] = value
    data = json_round_trip(data)
    catalog = validate_route_catalog(data["routes"], data["route_segments"], data["checkpoints"])
    assert_violation(catalog, "routes[0] schema: route_source")
    assert not any("R01 route_source is" in v or "route_id R01 does not have the format" in v for v in catalog), catalog
    report = validate_dataset(data)
    assert set(report) == {"derived_segments", "route_catalog", "pace_table", "eta_output"}
    assert_violation(report["route_catalog"], "routes[0] schema: route_source")
    assert report["derived_segments"] == report["pace_table"] == report["eta_output"] == []


@pytest.mark.parametrize("kind", ["TURNAROUND", "turn_around", "return"])
def test_checkpoint_kind_turnaround_is_spelled_exactly(data, kind):
    make_round_trip(data, at=2)
    data["checkpoints"][-1]["kind"] = kind
    assert_violation(catalog_violations(data), "schema: kind")


def test_contracts_cli_reports_no_violation_for_the_mock_fixture():
    """AC (5): python -m moto_copilot.contracts on the fixture (no network, no key, no GPX)."""
    import os
    import subprocess
    import sys
    from pathlib import Path

    from conftest import MOCK_DATASET
    src = Path(__file__).resolve().parents[1] / "src"
    env = {**os.environ, "PYTHONPATH": str(src)}
    result = subprocess.run([sys.executable, "-m", "moto_copilot.contracts", str(MOCK_DATASET)],
                            capture_output=True, text=True, encoding="utf-8", env=env, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "data contracts v0.3" in result.stdout
    assert "violation" not in result.stdout
