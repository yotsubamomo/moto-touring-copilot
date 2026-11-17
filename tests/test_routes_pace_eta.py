"""Unit tests for the routes, pace and ETA Spike.

Inputs are synthetic shapes and the mock contract fixture. Nothing here is a ride result.
"""
from __future__ import annotations

import datetime as dt

import pytest

from moto_copilot.contracts import validate_eta_output, validate_pace_table, validate_route_catalog
from moto_copilot.ingest import IngestParams, TrackPoint
from moto_copilot.pace import build_pace_table, compare_methods, compute_eta
from moto_copilot.routes import align_to_route, build_route, common_stretch
from test_ingest import at, straight

TAIPEI = dt.timezone(dt.timedelta(hours=8))
NOW = dt.datetime(2026, 11, 14, 20, 0, tzinfo=TAIPEI)


def shifted(points: list[TrackPoint], north_m: float) -> list[TrackPoint]:
    return [TrackPoint(p.lat + north_m / 111_195.0, p.lon, p.time) for p in points]


def length_between(points: list[TrackPoint], start: int, end: int) -> float:
    from moto_copilot.ingest import haversine_m
    return sum(haversine_m(a.lat, a.lon, b.lat, b.lon) for a, b in zip(points[start:end], points[start + 1:end]))


# --- routes ------------------------------------------------------------------
def test_common_stretch_is_the_part_both_trips_ride():
    source = straight(12_000)                                  # x from 0 to 12 km
    other = shifted(straight(6_000, x0=3_000), north_m=30)      # same road, 30 m off, x from 3 to 9 km
    start, end = common_stretch(source, [other])
    assert length_between(source, start, end) == pytest.approx(6_000, abs=350)
    assert length_between(source, 0, start) == pytest.approx(3_000, abs=250)


def test_common_stretch_needs_every_trip():
    source = straight(12_000)
    a = shifted(straight(6_000, x0=3_000), 30)   # 3 to 9 km
    b = shifted(straight(6_000, x0=5_000), -30)  # 5 to 11 km
    start, end = common_stretch(source, [a, b])
    assert length_between(source, start, end) == pytest.approx(4_000, abs=350)  # 5 to 9 km


def test_opposite_direction_is_not_the_same_route():
    source = straight(12_000)
    backwards = shifted(list(reversed(straight(12_000))), 30)
    backwards = [TrackPoint(p.lat, p.lon, source[i].time) for i, p in enumerate(backwards)]
    start, end = common_stretch(source, [backwards])
    assert length_between(source, start, end) < 500


def test_a_road_far_away_does_not_match():
    assert common_stretch(straight(12_000), [shifted(straight(12_000), 2_000)]) == (0, 0)


def test_alignment_finds_the_stretch_of_a_longer_trip():
    """The trip is longer than the route: only its part on the route may be timed later."""
    route_path = straight(6_000, x0=3_000)             # the route: x from 3 to 9 km
    trip = shifted(straight(12_000), 25)                # the trip: x from 0 to 12 km, 25 m off
    result = align_to_route(route_path, trip)
    assert result["coverage"] == pytest.approx(1.0, abs=0.02) and result["same_direction"]
    assert result["length_ratio"] == pytest.approx(1.0, abs=0.03)
    assert result["deviation_p95_m"] == pytest.approx(25, abs=12)
    start, end = result["trip_index_range"]
    assert length_between(trip, 0, start + 1) == pytest.approx(3_000, abs=150)
    assert length_between(trip, start, end) == pytest.approx(6_000, abs=150)


def test_alignment_rejects_the_opposite_direction():
    route_path = straight(6_000)
    backwards = shifted(list(reversed(straight(6_000))), 25)
    result = align_to_route(route_path, backwards)
    assert result["same_direction"] is False


def test_alignment_reports_partial_coverage():
    route_path = straight(6_000)
    half = shifted(straight(3_000), 25)
    result = align_to_route(route_path, half)
    assert result["coverage"] == pytest.approx(0.5, abs=0.05)


def test_alignment_of_an_unrelated_trip_is_empty():
    result = align_to_route(straight(6_000), shifted(straight(6_000), 3_000))
    assert result == {"coverage": 0.0, "same_direction": False, "trip_index_range": None}


def test_build_route_conforms_to_the_catalog_contract():
    route, segments, checkpoints = build_route("R09", "合成直線（測試）", straight(6_300), source_trip_id="T900",
                                               catalog_version="catalog-test")
    assert validate_route_catalog([route], segments, checkpoints) == []
    assert route["n_segments"] == len(segments) == 6           # the 300 m tail is merged or kept, never lost
    assert segments[-1]["cum_length_m"] == route["total_length_m"] == pytest.approx(6_300, abs=25)
    assert {s["seg_category"] for s in segments} == {"C1"}
    assert [(c["kind"], c["after_seg_count"]) for c in checkpoints] == [("start", 0), ("end", 6)]


def test_route_segments_use_the_same_category_rule_as_ingest():
    params = IngestParams(c1_max_deg_per_km=0.0001)  # every segment with any turning is at least C2
    wobble = [at(20.0 * s, 15.0 * (s % 2), s) for s in range(301)]
    _, segments, _ = build_route("R09", "鋸齒（測試）", wobble, source_trip_id="T900", catalog_version="c", params=params)
    assert all(s["seg_category"] in ("C2", "C3") for s in segments)


# --- pace --------------------------------------------------------------------
def test_pace_table_matches_the_mock_fixture(data):
    header, categories = build_pace_table(data["derived_segments"], ["T001", "T002"], pace_version="pace-mock-1",
                                          min_segments=2, built_at=NOW)
    assert [(c["seg_category"], c["speed_kmh"], c["n_segments"]) for c in categories] == \
        [("C1", 60.0, 2), ("C2", 45.0, 2), ("C3", None, 1)]
    assert header["method"] == "median_unweighted" and header["n_trips"] == 2


@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; "
                                       "build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet")
def test_pace_table_matches_the_mock_fixture__v03_contract(data):
    header, categories = build_pace_table(data["derived_segments"], ["T001", "T002"], pace_version="user-01",
                                          min_segments=2, built_at=NOW)
    assert validate_pace_table(header, categories, data["derived_segments"]) == []


def test_holdout_trip_is_refused(data):
    with pytest.raises(ValueError, match="holdout"):
        build_pace_table(data["derived_segments"], ["T001", "T003"], pace_version="p", min_segments=2, built_at=NOW)
    with pytest.raises(ValueError, match="holdout"):
        compare_methods(data["derived_segments"], ["T003"])


def test_suspect_and_invalid_rows_do_not_change_the_pace(data):
    rows = data["derived_segments"]
    for row in rows:
        if row["quality"] == "suspect":
            row["moving_time_s"] = 1.0  # an absurd speed that must be ignored
    _, categories = build_pace_table(rows, ["T001", "T002"], pace_version="p", min_segments=2, built_at=NOW)
    assert categories[0]["speed_kmh"] == 60.0


def test_method_comparison_reports_both_medians(data):
    result = compare_methods(data["derived_segments"], ["T001", "T002"])
    assert result["C1"] == {"n_segments": 2, "median_unweighted": 60.0, "median_length_weighted": 60.0}


# --- ETA ---------------------------------------------------------------------
def eta_for(data, route_id, plan_id, breaks):
    route = next(r for r in data["routes"] if r["route_id"] == route_id)
    return compute_eta(route, data["route_segments"], data["checkpoints"], data["pace_header"], data["pace_categories"],
                       plan_id=plan_id, departure_time=dt.datetime(2026, 11, 21, 7, 0, tzinfo=TAIPEI), margin_coeff=0.2,
                       breaks=breaks, computed_at=dt.datetime(2026, 11, 14, 20, 5, tzinfo=TAIPEI))


def test_eta_reproduces_the_mock_fixture(data):
    header, rows = eta_for(data, "R01", "P-MOCK-1", [{"after_checkpoint_id": "R01-CP03", "duration_s": 600.0}])
    assert header == data["eta_headers"][0]


@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                       "compute_eta does not write stop_allow_s yet")
def test_eta_reproduces_the_mock_fixture__v03_contract(data):
    header, rows = eta_for(data, "R01", "P-MOCK-1", [{"after_checkpoint_id": "R01-CP03", "duration_s": 600.0}])
    assert rows == [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]


def test_eta_is_unknown_when_a_category_has_no_pace(data):
    header, rows = eta_for(data, "R02", "P-MOCK-2", [])
    assert header["status"] == "unknown" and "C3" in header["unknown_reason"]
    assert all(r["typ_seg_time_s"] is None and r["eta_typ"] is None and r["eta_safe"] is None for r in rows)
    data["eta_headers"], data["eta_segments"] = [header], rows


@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                       "compute_eta does not write stop_allow_s yet")
def test_eta_is_unknown_when_a_category_has_no_pace__v03_contract(data):
    header, rows = eta_for(data, "R02", "P-MOCK-2", [])
    data["eta_headers"], data["eta_segments"] = [header], rows
    assert validate_eta_output([header], rows, data["routes"], data["route_segments"], data["checkpoints"],
                               data["pace_header"], data["pace_categories"]) == []


@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                       "compute_eta does not write stop_allow_s yet")
def test_eta_output_passes_the_contract_with_and_without_breaks(data):
    for plan_id, breaks in (("P-A", []), ("P-B", [{"after_checkpoint_id": "R01-CP04", "duration_s": 900.0}])):
        header, rows = eta_for(data, "R01", plan_id, breaks)
        assert validate_eta_output([header], rows, data["routes"], data["route_segments"], data["checkpoints"],
                                   data["pace_header"], data["pace_categories"]) == []


def test_eta_needs_an_aware_departure_time(data):
    route = data["routes"][0]
    with pytest.raises(ValueError, match="timezone-aware"):
        compute_eta(route, data["route_segments"], data["checkpoints"], data["pace_header"], data["pace_categories"],
                    plan_id="P", departure_time=dt.datetime(2026, 11, 21, 7, 0), margin_coeff=0.2, breaks=[],
                    computed_at=NOW)
