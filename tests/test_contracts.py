"""Tests for the data contracts v0.2 with the v0.3 stop-allowance fields of contracts 1, 3, 4 (DESIGN.md §5).

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
