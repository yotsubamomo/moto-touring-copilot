"""Unit tests for the ingest Spike, on synthetic geometry.

The tracks here are generated shapes (a straight line, a circle), not rides. They test the
arithmetic of the pipeline and say nothing about real pace.
"""
from __future__ import annotations

import datetime as dt
import math

import pytest

from moto_copilot.contracts import validate_derived_segments, validate_public_private_pair
from moto_copilot.ingest import IngestParams, TrackPoint, build_rows, to_public
from moto_copilot.ingest.segments import EARTH_RADIUS_M, clean_points, haversine_m, trim_ends, TripReport

T0 = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
LAT0, LON0 = 10.0, 20.0


def at(x_m: float, y_m: float, second: float) -> TrackPoint:
    """A point x metres east and y metres north of the origin."""
    lat = LAT0 + math.degrees(y_m / EARTH_RADIUS_M)
    lon = LON0 + math.degrees(x_m / (EARTH_RADIUS_M * math.cos(math.radians(LAT0))))
    return TrackPoint(lat, lon, T0 + dt.timedelta(seconds=second))


def straight(metres: float, speed: float = 20.0, x0: float = 0.0, t0: float = 0.0) -> list[TrackPoint]:
    """East at a constant speed, one point per second."""
    return [at(x0 + speed * s, 0.0, t0 + s) for s in range(int(metres / speed) + 1)]


def rows_of(points, **overrides):
    return build_rows(points, trip_id="T900", trip_role="pace", route_id=None, params=IngestParams(**overrides))


def test_haversine_matches_a_known_distance():
    assert haversine_m(0, 0, 0, 1) == pytest.approx(111_195, rel=1e-3)  # one degree of longitude on the equator


def test_trim_removes_the_requested_distance_from_both_ends():
    pts = straight(12_000)
    start, end = trim_ends(pts, 2000.0)
    assert haversine_m(pts[0].lat, pts[0].lon, pts[start].lat, pts[start].lon) == pytest.approx(2000, abs=21)
    assert haversine_m(pts[end - 1].lat, pts[end - 1].lon, pts[-1].lat, pts[-1].lon) == pytest.approx(2000, abs=21)


def test_straight_ride_gives_valid_low_curvature_segments():
    rows, report = rows_of(straight(12_000))
    assert 7 <= len(rows) <= 8                       # 8 km left after trimming 2 km from each end
    assert sum(r["length_m"] for r in rows) == pytest.approx(8000, abs=45)
    for r in rows:
        assert r["quality"] == "ok" and r["seg_category"] == "C1"
        assert r["curvature_deg_per_km"] < 5
        assert r["moving_time_s"] == pytest.approx(r["length_m"] / 20.0, abs=1.0)
        assert r["stopped_time_s"] == 0
        assert r["start_time"].endswith("+08:00")
    assert [r["seg_index"] for r in rows] == list(range(len(rows)))
    assert report.quality["ok"] == len(rows)


def test_rows_conform_to_the_contract_in_both_versions():
    private, _ = rows_of(straight(12_000))
    public = to_public(private)
    assert validate_public_private_pair(public, private) == []
    assert all("start_time" not in r for r in public)


@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; "
                                       "build_rows does not write short_stop_time_s yet")
def test_rows_conform_to_the_contract_in_both_versions__v03_contract():
    private, _ = rows_of(straight(12_000))
    public = to_public(private)
    assert validate_derived_segments(private, "private") == []
    assert validate_derived_segments(public, "public") == []


def test_circle_has_the_curvature_of_its_radius():
    """A circle of radius 100 m turns 360 degrees every 628 m: about 573 degrees per kilometre."""
    radius, speed = 100.0, 10.0
    lead = straight(2500, speed)           # ends at x = 2500 m, second 250, heading east
    circle = []
    for s in range(1, 401):                # 4 km on a circle that starts tangent to the lead-in
        angle = speed * s / radius
        circle.append(at(2500.0 + radius * math.sin(angle), radius * (1 - math.cos(angle)), 250 + s))
    last = circle[-1]
    tail = [TrackPoint(last.lat, last.lon + (p.lon - LON0), last.time + (p.time - T0)) for p in straight(2500, speed)[1:]]
    rows, _ = rows_of(lead + circle + tail)
    curvy = [r for r in rows if r["curvature_deg_per_km"] > 450]
    assert curvy, [r["curvature_deg_per_km"] for r in rows]
    assert all(r["curvature_deg_per_km"] == pytest.approx(573, rel=0.12) and r["seg_category"] == "C3" for r in curvy)


def test_a_stop_counts_as_stopped_time_not_moving_time():
    first = straight(6000)
    here = first[-1]
    wait = [TrackPoint(here.lat, here.lon, here.time + dt.timedelta(seconds=s)) for s in range(1, 121)]
    rest = [TrackPoint(p.lat, p.lon + (here.lon - LON0), wait[-1].time + (p.time - T0)) for p in straight(6000)[1:]]
    rows, _ = rows_of(first + wait + rest)
    assert sum(r["stopped_time_s"] for r in rows) == pytest.approx(120, abs=1)
    assert sum(r["moving_time_s"] for r in rows) == pytest.approx(sum(r["length_m"] for r in rows) / 20.0, abs=3)
    assert all(r["quality"] == "ok" for r in rows)


def test_a_gps_jump_is_dropped_and_its_segment_marked_suspect():
    pts = straight(12_000)
    jump = pts[300]
    pts[300] = TrackPoint(jump.lat + 0.01, jump.lon, jump.time)  # about 1.1 km sideways for one second
    rows, report = rows_of(pts)
    assert report.dropped_jumps == 1
    assert [r["quality"] for r in rows].count("suspect") == 1
    assert sum(r["length_m"] for r in rows) == pytest.approx(8000, abs=45)  # the jump adds no distance


def test_timing_jitter_at_speed_is_kept_and_not_suspect():
    """At 126 km/h a point recorded 25 m ahead makes one step look like 216 km/h; it is not a jump."""
    pts = straight(14_000, speed=35.0)
    ahead = at(35.0 * 200 + 25.0, 0.0, 200)
    pts[200] = ahead
    rows, report = rows_of(pts)
    assert report.timing_jitter_steps == 1 and report.dropped_jumps == 0
    assert all(r["quality"] == "ok" for r in rows)
    assert sum(r["length_m"] for r in rows) == pytest.approx(10_000, abs=75)


def test_a_small_jump_at_low_speed_is_still_dropped():
    """100 m sideways at 36 km/h is far beyond the recent speed, so it is a jump, not jitter."""
    pts = straight(12_000, speed=10.0)
    pts[600] = at(10.0 * 600, 100.0, 600)
    _, report = rows_of(pts)
    assert report.dropped_jumps == 1 and report.timing_jitter_steps == 0


def test_a_recording_gap_while_riding_is_suspect():
    pts = straight(12_000)
    del pts[300:330]  # 30 seconds without points while still moving
    rows, _ = rows_of(pts)
    assert [r["quality"] for r in rows].count("suspect") == 1
    assert sum(r["length_m"] for r in rows) == pytest.approx(8000, abs=45)


def test_a_recording_gap_while_standing_is_a_stop():
    first = straight(6000)
    here = first[-1]
    rest = [TrackPoint(p.lat, p.lon + (here.lon - LON0), here.time + dt.timedelta(seconds=300) + (p.time - T0))
            for p in straight(6000)[1:]]
    rows, _ = rows_of(first + rest)
    assert sum(r["stopped_time_s"] for r in rows) == pytest.approx(300, abs=1)
    assert all(r["quality"] == "ok" for r in rows)


def test_points_with_a_repeated_time_are_dropped():
    pts = straight(12_000)
    pts[200:200] = [TrackPoint(pts[200].lat, pts[200].lon, pts[199].time)] * 3
    report = TripReport()
    kept, _ = clean_points(pts, IngestParams(), report)
    assert report.dropped_non_increasing_time == 3
    assert all(b.time > a.time for a, b in zip(kept, kept[1:]))
    rows, _ = rows_of(pts)


@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; "
                                       "build_rows does not write short_stop_time_s yet")
def test_points_with_a_repeated_time_are_dropped__v03_contract():
    pts = straight(12_000)
    pts[200:200] = [TrackPoint(pts[200].lat, pts[200].lon, pts[199].time)] * 3
    rows, _ = rows_of(pts)
    assert validate_derived_segments(rows, "private") == []


def test_a_trip_too_short_after_trimming_gives_no_rows():
    rows, report = rows_of(straight(4500))
    assert rows == [] and report.note


def test_category_scheme_names_the_thresholds():
    assert IngestParams().category_scheme == "curv-spike0-80-250"
    rows, _ = rows_of(straight(12_000), c1_max_deg_per_km=60.0)
    assert rows[0]["category_scheme"] == "curv-spike0-60-250"
