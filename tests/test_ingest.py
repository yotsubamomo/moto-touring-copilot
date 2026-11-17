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
    assert validate_derived_segments(private, "private") == []
    assert validate_derived_segments(public, "public") == []
    assert validate_public_private_pair(public, private) == []
    assert all("start_time" not in r for r in public)


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
    assert validate_derived_segments(rows, "private") == []


def test_a_trip_too_short_after_trimming_gives_no_rows():
    rows, report = rows_of(straight(4500))
    assert rows == [] and report.note


def test_category_scheme_names_the_thresholds():
    assert IngestParams().category_scheme == "curv-spike0-80-250"
    rows, _ = rows_of(straight(12_000), c1_max_deg_per_km=60.0)
    assert rows[0]["category_scheme"] == "curv-spike0-60-250"


# --- Stop events (Issue #9, SPEC-B1 B1-2): synthetic tracks only ------------------------------

def ride_with_stops(waits: list[int], leg_m: float = 3100.0, speed: float = 20.0) -> list[TrackPoint]:
    """East at `speed` m/s, one point per second; after each leg, stand still for `waits[k]` seconds.

    Every wait is one point per second at the same position, so it is one stop event of that many
    seconds. Legs of 3100 m keep each wait in the middle of a 1000 m segment after trimming 2 km.
    """
    pts, x, t = [at(0.0, 0.0, 0)], 0.0, 0
    for wait in [*waits, None]:
        for _ in range(int(leg_m / speed)):
            x, t = x + speed, t + 1
            pts.append(at(x, 0.0, t))
        if wait is None:
            return pts
        for _ in range(wait):
            t += 1
            pts.append(at(x, 0.0, t))


def trimmed_duration_s(points: list[TrackPoint], params: IngestParams = IngestParams()) -> float:
    kept, _ = clean_points(points, params, TripReport())
    start, end = trim_ends(kept, params.trim_m)
    return (kept[end - 1].time - kept[start].time).total_seconds()


def test_sb2_t1_one_second_repeated_position_between_fast_steps_is_moving_time():
    """SB2-T1: both neighbouring steps are 72 km/h; the 1 s at the repeated position is moving time."""
    plain = straight(12_000)
    pts = straight(12_000)
    dup = pts[300]
    assert haversine_m(pts[299].lat, pts[299].lon, dup.lat, dup.lon) / 1 * 3.6 > 20   # step before: > 20 km/h
    later = [TrackPoint(p.lat, p.lon, p.time + dt.timedelta(seconds=1)) for p in pts[301:]]
    pts = pts[:301] + [TrackPoint(dup.lat, dup.lon, dup.time + dt.timedelta(seconds=1))] + later
    assert haversine_m(dup.lat, dup.lon, later[0].lat, later[0].lon) / 1 * 3.6 > 20     # step after: > 20 km/h
    rows, report = rows_of(pts)
    base, _ = rows_of(plain)
    assert all(r["stopped_time_s"] == 0 and r["short_stop_time_s"] == 0 for r in rows)
    assert report.stop_events == {"false": 1, "short": 0, "long": 0}
    assert sum(r["moving_time_s"] for r in rows) == pytest.approx(sum(r["moving_time_s"] for r in base) + 1, abs=0.2)
    assert sum(r["length_m"] for r in rows) == pytest.approx(sum(r["length_m"] for r in base), abs=0.2)  # no distance added
    assert validate_derived_segments(rows, "private") == []


def test_sb2_t2_stops_of_2_3_179_and_180_seconds_are_classified_by_length():
    """SB2-T2: 2 s -> moving time; 3 s and 179 s -> short_stop_time_s; 180 s -> stopped_time_s only."""
    plain, _ = rows_of(ride_with_stops([0, 0, 0, 0]))
    rows, report = rows_of(ride_with_stops([2, 3, 179, 180]))
    assert report.stop_events == {"false": 1, "short": 2, "long": 1}
    assert len(rows) == len(plain)
    stops = sorted((r["stopped_time_s"], r["short_stop_time_s"]) for r in rows if r["stopped_time_s"] > 0)
    assert stops == [(3.0, 3.0), (179.0, 179.0), (180.0, 0.0)]
    extra = [round(r["moving_time_s"] - p["moving_time_s"], 1) for r, p in zip(rows, plain)]
    assert sorted(e for e in extra if e != 0) == [2.0]                     # only the 2 s event is moving time
    assert [r["length_m"] for r in rows] == [p["length_m"] for p in plain]  # and it adds no distance
    assert sum(r["stopped_time_s"] for r in rows) == 362
    assert sum(r["short_stop_time_s"] for r in rows) == 182
    assert validate_derived_segments(rows, "private") == []


def test_stop_thresholds_are_ingest_parameters():
    rows, report = rows_of(ride_with_stops([2, 3, 179, 180]), false_stop_max_s=2.0, long_stop_min_s=179.0)
    assert report.stop_events == {"false": 0, "short": 2, "long": 2}
    assert sum(r["stopped_time_s"] for r in rows) == 2 + 3 + 179 + 180
    assert sum(r["short_stop_time_s"] for r in rows) == 5


def test_sb2_t3_short_stops_never_exceed_stops_and_times_add_up_to_the_trimmed_duration():
    """SB2-T3 on a track with short and long stops, a stop during a recording gap, a gap while
    riding, a GPS jump and a 1 s repeated position."""
    pts = ride_with_stops([1, 2, 45, 179, 600])
    jump = pts[400]
    pts[400] = TrackPoint(jump.lat + 0.01, jump.lon, jump.time)                    # GPS jump, dropped
    del pts[900:930]                                                                # 30 s gap while riding
    here = pts[1500]
    later = [TrackPoint(p.lat, p.lon, p.time + dt.timedelta(seconds=40)) for p in pts[1501:]]
    pts = pts[:1501] + [TrackPoint(here.lat, here.lon, here.time + dt.timedelta(seconds=40))] + later[1:]
    rows, report = rows_of(pts)
    assert report.dropped_jumps == 1
    assert all(r["short_stop_time_s"] <= r["stopped_time_s"] for r in rows)
    assert all(r["moving_time_s"] is not None for r in rows)
    total = sum(r["moving_time_s"] + r["stopped_time_s"] for r in rows)
    assert total == pytest.approx(trimmed_duration_s(pts), abs=0.05 * len(rows))
    assert validate_derived_segments(rows, "private") == []


def test_a_recording_gap_that_moved_50_m_or_more_is_moving_time_not_a_stop():
    """CL-B1-3 item 1: a gap over 10 s that covers 50 m or more is still a ridden step."""
    pts = straight(12_000)
    del pts[300:330]                                    # 31 s and 620 m between two points
    rows, report = rows_of(pts)
    assert sum(r["stopped_time_s"] for r in rows) == 0
    assert report.stop_events == {"false": 0, "short": 0, "long": 0}
    assert sum(r["moving_time_s"] for r in rows) == pytest.approx(trimmed_duration_s(pts), abs=0.1)


def test_a_standing_recording_gap_joins_the_neighbouring_stopped_steps_into_one_event():
    """100 s of points at one place followed by a 100 s gap there is one 200 s event: a long stop."""
    pts = ride_with_stops([100])
    i = next(k for k in range(1, len(pts)) if pts[k].lat == pts[k - 1].lat and pts[k].lon == pts[k - 1].lon) + 99
    here = pts[i]
    later = [TrackPoint(p.lat, p.lon, p.time + dt.timedelta(seconds=100)) for p in pts[i + 1:]]
    pts = pts[:i + 1] + [TrackPoint(here.lat, here.lon, here.time + dt.timedelta(seconds=100))] + later[1:]
    rows, report = rows_of(pts)
    assert report.stop_events == {"false": 0, "short": 0, "long": 1}
    assert sum(r["stopped_time_s"] for r in rows) == 200
    assert sum(r["short_stop_time_s"] for r in rows) == 0


def test_an_event_across_a_segment_boundary_is_classified_once_and_split_by_time():
    """CL-B1-3 item 2, on the allocation step directly (the distance cut only closes a segment on a
    moving step, so build_rows cannot produce this case from a track)."""
    from moto_copilot.ingest.segments import allocate_stop_events
    params, counts = IngestParams(), {"false": 0, "short": 0, "long": 0}
    steps = [(0, False, 1.0), (0, True, 100.0), (1, True, 100.0), (1, False, 1.0),   # 200 s: long
             (1, True, 2.0), (2, True, 2.0), (2, False, 1.0),                          # 4 s: short
             (2, True, 1.0), (3, True, 1.0)]                                           # 2 s: false
    out = allocate_stop_events(steps, params, counts)
    assert out[0] == {"false": 0.0, "short": 0.0, "long": 100.0}
    assert out[1] == {"false": 0.0, "short": 2.0, "long": 100.0}
    assert out[2] == {"false": 1.0, "short": 2.0, "long": 0.0}
    assert out[3] == {"false": 1.0, "short": 0.0, "long": 0.0}
    assert counts == {"false": 1, "short": 1, "long": 1}


def test_the_ingest_version_is_new():
    assert IngestParams().ingest_version != "ingest-spike-0.2"
    rows, _ = rows_of(straight(12_000))
    assert {r["ingest_version"] for r in rows} == {IngestParams().ingest_version}


def test_a_stop_in_a_short_tail_goes_with_the_tail_into_the_previous_segment():
    """3200 m after trimming: the last 200 m merge into segment 2, and so does the 50 s stop in them."""
    first = straight(5100)
    here = first[-1]
    wait = [TrackPoint(here.lat, here.lon, here.time + dt.timedelta(seconds=s)) for s in range(1, 51)]
    rest = [TrackPoint(p.lat, p.lon + (here.lon - LON0), wait[-1].time + (p.time - T0)) for p in straight(2100)[1:]]
    pts = first + wait + rest
    rows, report = rows_of(pts)
    assert len(rows) == 3 and rows[-1]["length_m"] == pytest.approx(1200, abs=25)
    assert report.stop_events == {"false": 0, "short": 1, "long": 0}
    assert [(r["stopped_time_s"], r["short_stop_time_s"]) for r in rows] == [(0, 0), (0, 0), (50, 50)]
    assert sum(r["moving_time_s"] + r["stopped_time_s"] for r in rows) == pytest.approx(trimmed_duration_s(pts), abs=0.2)


def test_a_stop_event_cut_by_the_trim_is_classified_by_its_part_inside_the_trimmed_track():
    """CL-B1-10: the start trim (2000 m) falls inside a 200 s stop whose GPS drift (0.5 m/s, a
    stopped step) carries the path past 2000 m. The whole event would be a long stop; only the part
    inside the trimmed track counts, and it is shorter than 180 s, so it is a short stop. The steps
    before the trim appear in no field."""
    params = IngestParams()
    ride_in = straight(1940)                                   # 97 steps of 20 m: 0 .. 1940 m
    here = ride_in[-1]
    drift = [at(1940.0 + 0.5 * s, 0.0, 97 + s) for s in range(1, 201)]          # 200 s, 100 m
    ride_on = [at(2040.0 + 20.0 * s, 0.0, 297 + s) for s in range(1, 501)]       # 10 km more
    pts = ride_in + drift + ride_on
    kept, _ = clean_points(pts, params, TripReport())
    start, _ = trim_ends(kept, params.trim_m)
    assert here.time < kept[start].time < drift[-1].time     # the trim boundary is inside the stop
    inside_s = (drift[-1].time - kept[start].time).total_seconds()
    whole_s = (drift[-1].time - here.time).total_seconds()
    assert whole_s >= params.long_stop_min_s > inside_s >= params.false_stop_max_s
    rows, report = rows_of(pts)
    assert report.stop_events == {"false": 0, "short": 1, "long": 0}
    assert rows[0]["stopped_time_s"] == inside_s and rows[0]["short_stop_time_s"] == inside_s
    assert sum(r["stopped_time_s"] for r in rows) == inside_s
    assert sum(r["short_stop_time_s"] for r in rows) == inside_s
    assert sum(r["moving_time_s"] + r["stopped_time_s"] for r in rows) == pytest.approx(trimmed_duration_s(pts), abs=0.2)
    assert validate_derived_segments(rows, "private") == []
