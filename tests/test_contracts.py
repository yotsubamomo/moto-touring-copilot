"""Tests for the data contracts v0.2 (DESIGN.md §5).

These tests check the validators against a mock fixture and against deliberately broken copies
of it. They say nothing about real rides: no GPX has been ingested yet.
"""
from __future__ import annotations

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
    assert data["_meta"]["contract_version"] == CONTRACT_VERSION == "0.2"


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
    ("R01-CP03", ("2026-11-21T07:05:00+08:00", "2026-11-21T07:06:00+08:00")),  # c = 2: row 1, before its own break
    ("R01-CP04", ("2026-11-21T07:19:00+08:00", "2026-11-21T07:20:48+08:00")),  # c = 3: row 2, after the break
    ("R01-CP05", ("2026-11-21T07:25:00+08:00", "2026-11-21T07:28:00+08:00")),  # c = n: last row
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
    data["eta_segments"][2]["eta_typ"] = "2026-11-21T07:09:00+08:00"  # as if the break were not counted
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
