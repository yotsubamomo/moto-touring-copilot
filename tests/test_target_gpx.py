"""Tests for the target route GPX source (Issue #15, SPEC-R1 R1-3), on synthetic GPX only.

Every GPX here is generated in the test as a string from invented shapes (straight lines, a
circle, a figure eight, rectangles) next to 0 deg N, 0 deg E (open ocean). Nothing comes from
ride data, and no file is kept in the repository: files are written only under pytest's
`tmp_path`. No test makes a network request.
"""
from __future__ import annotations

import ast
import hashlib
import logging
import math
import re
import socket
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pytest

from moto_copilot.contracts.schemas import ROUTE_ID_PATTERN
from moto_copilot.ingest import geometry as geometry_module
from moto_copilot.ingest.geometry import GeoPoint, GpxGeometryError, parse_gpx_geometry, read_gpx_geometry
from moto_copilot.ingest.segments import EARTH_RADIUS_M, haversine_m
from moto_copilot.routing import target_gpx as tg
from moto_copilot.routing.target_gpx import (
    END_NOT_AT_START,
    TARGET_GPX_INVALID,
    TARGET_GPX_NOT_ROUND_TRIP,
    TURNAROUND_UNCONFIRMED,
    TargetGpxError,
    TargetGpxRoute,
    TripTypeRequiredError,
    cumulative_m,
    detect_out_and_back,
    metres_half_up,
    rider_turnaround_index,
    target_gpx_route,
    target_gpx_route_from_bytes,
    target_gpx_route_id,
    turnaround_m_from_km,
)

GPX11 = "http://www.topografix.com/GPX/1/1"
GPX10 = "http://www.topografix.com/GPX/1/0"


# --- synthetic shapes ----------------------------------------------------------------------------

def at(x_m: float, y_m: float) -> tuple[float, float]:
    """A synthetic position x metres east and y metres north of 0 deg N, 0 deg E."""
    return (math.degrees(y_m / EARTH_RADIUS_M), math.degrees(x_m / EARTH_RADIUS_M))


def line(x0, y0, x1, y1, step=50.0, include_start=True):
    """Positions every `step` metres from (x0, y0) to (x1, y1), end included."""
    n = max(1, math.ceil(math.hypot(x1 - x0, y1 - y0) / step))
    first = 0 if include_start else 1
    return [at(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(first, n + 1)]


def path(*corners, step=50.0):
    """A polyline through the corners (metres), sampled every `step` metres."""
    out = line(*corners[0], *corners[1], step=step)
    for a, b in zip(corners[1:], corners[2:]):
        out += line(*a, *b, step=step, include_start=False)
    return out


def out_and_back(length=3000.0, offset=10.0, step=50.0):
    """East `length` metres, then back west on a parallel line `offset` metres north (same road)."""
    outbound = line(0, 0, length, 0, step=step)
    back = line(length - step, offset, 0, offset, step=step)
    return outbound + back


def circle(radius=600.0, n=180, cx=0.0, cy=None, start_deg=-90.0, turns=1.0):
    """A circle through the origin (a loop), ending where it started."""
    cy = radius if cy is None else cy
    return [at(cx + radius * math.cos(math.radians(start_deg + 360.0 * turns * i / n)),
               cy + radius * math.sin(math.radians(start_deg + 360.0 * turns * i / n))) for i in range(n + 1)]


def figure_eight(radius=600.0, n=180):
    """Two loops that touch at the origin: the upper one first, then the lower one."""
    upper = circle(radius, n, cy=radius, start_deg=-90.0)
    lower = [at(radius * math.cos(math.radians(90.0 - 360.0 * i / n)),
                -radius + radius * math.sin(math.radians(90.0 - 360.0 * i / n))) for i in range(1, n + 1)]
    return upper + lower


def partly_same_road():
    """Out 3000 m; back on the same road for about 2400 m, then a detour north and west to the start."""
    outbound = line(0, 0, 3000, 0)
    back = path((2950, 10), (600, 10), (600, 310), (0, 310), (0, 10))
    return outbound + back


def bump_back(detour_west: float):
    """Out 10 km east; back on the same road except one detour 200 m north and `detour_west` metres west."""
    outbound = line(0, 0, 10_000, 0)
    back = path((9950, 10), (6000, 10), (6000, 210), (6000 - detour_west, 210), (6000 - detour_west, 10), (0, 10))
    return outbound + back


def gpx(positions, kind="trk", namespace=GPX11, segments=None, with_time=False, with_ele=False) -> bytes:
    """A GPX document. `segments` splits the track points into several trkseg (list of lengths)."""
    def node(tag, lat, lon, i):
        inner = ""
        if with_ele:
            inner += f"<ele>{100 + i}</ele>"
        if with_time:
            inner += f"<time>2026-01-01T00:{i // 60 % 60:02d}:{i % 60:02d}Z</time>"
        return f'<{tag} lat="{lat!r}" lon="{lon!r}">{inner}</{tag}>'

    if kind == "trk":
        groups, start = [], 0
        for size in (segments or [len(positions)]):
            groups.append(positions[start:start + size])
            start += size
        body = "<trk>" + "".join(
            "<trkseg>" + "".join(node("trkpt", lat, lon, i) for i, (lat, lon) in enumerate(g)) + "</trkseg>"
            for g in groups) + "</trk>"
    else:
        body = "<rte>" + "".join(node("rtept", lat, lon, i) for i, (lat, lon) in enumerate(positions)) + "</rte>"
    return (f'<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="synthetic-test" '
            f'xmlns="{namespace}">{body}</gpx>').encode("utf-8")


def points_of(positions):
    return tuple(GeoPoint(lat, lon) for lat, lon in positions)


def route(positions, trip_type, km=None, **gpx_options):
    return target_gpx_route_from_bytes(gpx(positions, **gpx_options), trip_type, km)


def assert_slices_of_the_file(result: TargetGpxRoute, positions, lengths: bool = True):
    """S64 (T-6): every leg is a contiguous, forward slice of the file's points; nothing added or reversed.

    With `lengths`, the leg lengths are cum_k and total - cum_k exactly (CL-R1-22 item 7). Tests that
    replace the distances along the track pass `lengths=False`.
    """
    original = points_of(positions)
    cum = cumulative_m(original)
    if result.trip_type == "one_way":
        assert len(result.legs) == 1 and result.legs[0].points == original
        return
    outbound, back = result.legs
    assert outbound.direction == "outbound" and back.direction == "return"
    k = len(outbound.points) - 1
    assert outbound.points == original[: k + 1]
    assert back.points == original[k:]
    assert outbound.points[-1] is back.points[0] or outbound.points[-1] == back.points[0]
    assert outbound.points + back.points[1:] == original
    assert len(outbound.points) + len(back.points) == len(original) + 1
    assert set(outbound.points) | set(back.points) <= set(original)
    if lengths:
        assert outbound.length_m == cum[k] and back.length_m == cum[-1] - cum[k]
        assert result.total_length_m == cum[-1]
        assert result.turnaround_m == metres_half_up(cum[k])
        assert result.route_id == target_gpx_route_id(result.target_gpx_ref, "round_trip", result.turnaround_m)


# --- geometry reading (scope (a); CL-R1-10 item 1) ------------------------------------------------

def test_track_points_are_read_in_file_order_across_trk_and_trkseg():
    positions = line(0, 0, 2000, 0)
    data = gpx(positions, segments=[10, 15, len(positions) - 25])
    geometry = parse_gpx_geometry(data)
    assert geometry.points == points_of(positions)
    assert geometry.source == "trkpt"
    two_tracks = data.replace(b"</trkseg><trkseg>", b"</trkseg></trk><trk><trkseg>", 1)
    assert parse_gpx_geometry(two_tracks).points == points_of(positions)


def test_reading_does_not_need_time_and_ignores_time_and_elevation():
    positions = line(0, 0, 2000, 0)
    plain = parse_gpx_geometry(gpx(positions))
    timed = parse_gpx_geometry(gpx(positions, with_time=True, with_ele=True))
    assert plain.points == timed.points == points_of(positions)
    assert set(GeoPoint.__dataclass_fields__) == {"lat", "lon"}


def test_some_points_with_time_and_some_without_are_all_used():
    positions = line(0, 0, 2000, 0)
    data = gpx(positions, with_time=True).replace(b"<time>2026-01-01T00:00:03Z</time>", b"", 1)
    assert parse_gpx_geometry(data).points == points_of(positions)


def test_a_file_with_only_route_points_and_no_time_can_be_used():
    positions = line(0, 0, 2000, 0)
    geometry = parse_gpx_geometry(gpx(positions, kind="rte"))
    assert geometry.points == points_of(positions) and geometry.source == "rtept"
    result = route(positions, "one_way", kind="rte")
    assert isinstance(result, TargetGpxRoute) and result.legs[0].points == points_of(positions)


def test_route_points_are_not_used_when_the_file_has_track_points():
    track = line(0, 0, 2000, 0)
    other = line(0, 500, 2000, 500)
    trk = gpx(track).decode()
    rte = gpx(other, kind="rte").decode()
    rte_body = rte[rte.index("<rte>"): rte.index("</rte>") + len("</rte>")]
    both = trk.replace("</gpx>", rte_body + "</gpx>").encode()
    assert parse_gpx_geometry(both).points == points_of(track)


def test_gpx_1_0_namespace_is_read():
    positions = line(0, 0, 2000, 0)
    assert parse_gpx_geometry(gpx(positions, namespace=GPX10)).points == points_of(positions)


def test_sha256_is_the_hash_of_the_file_bytes_and_path_and_bytes_agree(tmp_path):
    data = gpx(out_and_back())
    file = tmp_path / "synthetic.gpx"
    file.write_bytes(data)
    assert read_gpx_geometry(file).sha256 == hashlib.sha256(data).hexdigest() == parse_gpx_geometry(data).sha256
    from_path = target_gpx_route(file, "round_trip")
    from_bytes = target_gpx_route_from_bytes(data, "round_trip")
    assert from_path == from_bytes
    assert from_path.target_gpx_ref == hashlib.sha256(data).hexdigest()
    assert target_gpx_route(str(file), "one_way") == target_gpx_route_from_bytes(data, "one_way")


@pytest.mark.parametrize("data, reason", [
    (b"", "unreadable"),
    (b"not xml at all", "unreadable"),
    (b"<gpx><trk><trkseg>", "unreadable"),
    (b'<kml xmlns="http://www.opengis.net/kml/2.2"></kml>', "unreadable"),
    (b"<gpx><trk><trkseg><trkpt lat='0' lon='0'/></trkseg></trk></gpx>", "unreadable"),  # no GPX namespace
    (f'<gpx xmlns="{GPX11}"><trk><trkseg><trkpt lat="x" lon="0"/></trkseg></trk></gpx>'.encode(), "malformed_point"),
    (f'<gpx xmlns="{GPX11}"><trk><trkseg><trkpt lon="0"/></trkseg></trk></gpx>'.encode(), "malformed_point"),
    (f'<gpx xmlns="{GPX11}"><trk><trkseg><trkpt lat="91" lon="0"/></trkseg></trk></gpx>'.encode(), "malformed_point"),
    (f'<gpx xmlns="{GPX11}"><trk><trkseg><trkpt lat="0" lon="nan"/></trkseg></trk></gpx>'.encode(), "malformed_point"),
    (f'<gpx xmlns="{GPX11}"><trk><trkseg><trkpt lat="0" lon="inf"/></trkseg></trk></gpx>'.encode(), "malformed_point"),
])
def test_unreadable_files_and_malformed_points_are_target_gpx_invalid(data, reason):
    with pytest.raises(GpxGeometryError) as caught:
        parse_gpx_geometry(data)
    assert caught.value.reason == reason
    assert target_gpx_route_from_bytes(data, "one_way") == TargetGpxError(TARGET_GPX_INVALID, reason)


def test_reader_rejects_non_bytes_and_non_path_arguments():
    with pytest.raises(TypeError):
        parse_gpx_geometry("<gpx/>")
    with pytest.raises(TypeError):
        read_gpx_geometry(0)  # an int would be a file descriptor


# --- target_gpx_invalid (S43; CL-R1-10 item 2) -----------------------------------------------------

@pytest.mark.parametrize("trip_type", ["one_way", "round_trip"])
def test_no_points_or_one_point_is_invalid(trip_type):
    empty = f'<gpx xmlns="{GPX11}"><trk><trkseg></trkseg></trk></gpx>'.encode()
    assert target_gpx_route_from_bytes(empty, trip_type) == TargetGpxError(TARGET_GPX_INVALID, tg.TOO_FEW_POINTS)
    assert route([at(0, 0)], trip_type) == TargetGpxError(TARGET_GPX_INVALID, tg.TOO_FEW_POINTS)
    assert route([at(0, 0)], trip_type, kind="rte") == TargetGpxError(TARGET_GPX_INVALID, tg.TOO_FEW_POINTS)


@pytest.mark.parametrize("trip_type", ["one_way", "round_trip"])
def test_total_length_under_1_km_is_invalid(trip_type):
    short = line(0, 0, 990, 0)
    assert route(short, trip_type) == TargetGpxError(TARGET_GPX_INVALID, tg.TOO_SHORT)
    assert isinstance(route(line(0, 0, 1010, 0), "one_way"), TargetGpxRoute)


@pytest.mark.parametrize("trip_type", ["one_way", "round_trip"])
def test_adjacent_points_more_than_1_km_apart_is_invalid(trip_type):
    sparse = line(0, 0, 3000, 0, step=1500)
    assert route(sparse, trip_type) == TargetGpxError(TARGET_GPX_INVALID, tg.TOO_SPARSE)
    assert isinstance(route(line(0, 0, 3000, 0, step=990), "one_way"), TargetGpxRoute)


def test_a_gap_of_more_than_1_km_across_trkseg_is_invalid():
    first = line(0, 0, 2000, 0)
    second = line(3500, 0, 6000, 0)
    data = gpx(first + second, segments=[len(first), len(second)])
    assert target_gpx_route_from_bytes(data, "one_way") == TargetGpxError(TARGET_GPX_INVALID, tg.TOO_SPARSE)
    close = line(2100, 0, 6000, 0)
    ok = gpx(first + close, segments=[len(first), len(close)])
    assert isinstance(target_gpx_route_from_bytes(ok, "one_way"), TargetGpxRoute)


# --- trip type (S27, S43; CL-R1-10 item 3) ---------------------------------------------------------

@pytest.mark.parametrize("positions", [out_and_back(), circle(), line(0, 0, 3000, 0)])
def test_missing_trip_type_is_an_explicit_error_and_is_not_inferred(positions, tmp_path):
    with pytest.raises(TripTypeRequiredError):
        route(positions, None)
    with pytest.raises(TripTypeRequiredError):
        target_gpx_route(tmp_path / "does-not-matter.gpx", None)  # raised before the file is opened


@pytest.mark.parametrize("bad", ["", "ROUND_TRIP", "round_trip\n", " one_way", "loop", 1, True, ["one_way"]])
def test_unknown_trip_type_values_are_rejected(bad):
    with pytest.raises(ValueError):
        route(out_and_back(), bad)


@pytest.mark.parametrize("km", [None, 1.0, 0.0, -1.0])
def test_one_way_uses_the_geometry_as_it_is_even_when_start_and_end_meet(km):
    for positions in (out_and_back(), circle(), line(0, 0, 3000, 0)):
        result = route(positions, "one_way", km)
        assert isinstance(result, TargetGpxRoute)
        assert result.trip_type == "one_way" and result.route_source == "target_gpx"
        assert result.turnaround_m is None and result.turnaround_source is None
        assert result.legs[0].direction == "outbound"
        assert result.legs[0].length_m == pytest.approx(result.total_length_m)
        assert_slices_of_the_file(result, positions)


# --- round trip: end must return to start (S27, S43, S63) ------------------------------------------

@pytest.mark.parametrize("km", [None, 1.5, 0.0, -2.0, 99.0])
def test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround(km):
    one_way_shape = line(0, 0, 3000, 0)
    assert route(one_way_shape, "round_trip", km) == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, END_NOT_AT_START)


def test_end_within_200_m_of_the_start_counts_as_returned_and_beyond_does_not():
    near = line(0, 0, 3000, 0) + line(2950, 10, 190, 10)       # ends about 190 m from the start
    far = line(0, 0, 3000, 0) + line(2950, 10, 220, 10)        # ends about 220 m from the start
    assert isinstance(route(near, "round_trip"), TargetGpxRoute)
    assert route(far, "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, END_NOT_AT_START)


# --- automatic out-and-back detection (S43, S59, S79) ----------------------------------------------

def test_out_and_back_without_a_turnaround_uses_the_point_farthest_from_the_start():
    positions = out_and_back()
    result = route(positions, "round_trip")
    assert isinstance(result, TargetGpxRoute)
    points = points_of(positions)
    farthest = max(range(len(points)), key=lambda i: haversine_m(points[0].lat, points[0].lon, points[i].lat, points[i].lon))
    assert len(result.legs[0].points) - 1 == farthest
    assert result.legs[0].points[-1] == points[farthest] == result.legs[1].points[0]
    cum = cumulative_m(points)
    assert result.turnaround_m == metres_half_up(cum[farthest]) == 3000
    assert result.turnaround_source == "detected"
    assert result.legs[0].length_m == pytest.approx(cum[farthest])
    assert result.legs[1].length_m == pytest.approx(cum[-1] - cum[farthest])
    assert result.route_id == target_gpx_route_id(result.target_gpx_ref, "round_trip", 3000)
    assert_slices_of_the_file(result, positions)


def test_when_several_points_are_equally_farthest_the_first_is_the_turnaround():
    outbound = line(0, 0, 3000, 0)
    positions = outbound + [outbound[-1]] + line(2950, 10, 0, 10)  # the far end recorded twice
    result = route(positions, "round_trip")
    assert isinstance(result, TargetGpxRoute)
    assert len(result.legs[0].points) == len(outbound)
    assert_slices_of_the_file(result, positions)


@pytest.mark.parametrize("name, positions", [
    ("loop", circle()),
    ("figure_eight", figure_eight()),
    ("partly_same_road", partly_same_road()),
])
def test_ambiguous_shapes_are_not_detected_and_give_turnaround_unconfirmed(name, positions):
    points = points_of(positions)
    start, end = points[0], points[-1]
    assert haversine_m(start.lat, start.lon, end.lat, end.lon) <= 200  # all of them return to the start
    assert detect_out_and_back(points) is None
    assert route(positions, "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


def test_the_four_shapes_of_s79():
    assert isinstance(route(out_and_back(), "round_trip"), TargetGpxRoute)
    for positions in (circle(), figure_eight(), partly_same_road()):
        assert route(positions, "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


def test_the_90_percent_threshold_on_both_sides():
    small = points_of(bump_back(500))    # 96 of 104 samples near the outbound road (about 92%)
    large = points_of(bump_back(1500))   # 86 of 104 samples near the outbound road (about 83%)
    assert detect_out_and_back(small) is not None
    assert detect_out_and_back(large) is None


@pytest.mark.parametrize("near_count, detected", [(10, True), (9, True), (8, False), (0, False)])
def test_exactly_90_percent_near_is_detected_and_less_is_not(monkeypatch, near_count, detected):
    points = points_of(out_and_back(length=1000))   # the back part has exactly 10 samples
    answers = iter([True] * near_count + [False] * (10 - near_count))
    monkeypatch.setattr(tg._NearIndex, "has_point_within", lambda self, sample: next(answers))
    assert (detect_out_and_back(points) is not None) is detected
    assert next(answers, "done") == "done"            # every sample was checked once


def test_detection_counts_samples_on_the_back_part_only(monkeypatch):
    points = points_of(out_and_back())
    seen = []
    original = tg._position_along

    def spy(pts, cum, distance):
        seen.append(distance)
        return original(pts, cum, distance)

    monkeypatch.setattr(tg, "_position_along", spy)
    boundary = detect_out_and_back(points)
    cum = cumulative_m(points)
    back = cum[-1] - cum[boundary]
    assert seen[0] == pytest.approx(cum[boundary] + 100)          # 100 m after the boundary, not the boundary
    assert all(b - a == pytest.approx(100) for a, b in zip(seen, seen[1:]))
    assert len(seen) == int(back // 100)
    assert seen[-1] <= cum[-1]


def test_no_sample_on_the_back_part_means_not_detected():
    # Wanders within about 140 m of the start for more than 1 km and ends at its farthest point.
    zigzag = path((0, 0), (100, 0), (100, 100), (-100, 100), (-100, -100), (100, -100), (100, 0),
                  (0, 0), (100, 100), (-100, -100), (-100, 100), (100, -100), (0, 190))
    points = points_of(zigzag)
    assert cumulative_m(points)[-1] > 1000
    assert detect_out_and_back(points) is None
    assert route(zigzag, "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


def test_a_sample_is_near_within_50_m_of_a_front_point_and_not_beyond():
    for offset, detected in ((40.0, True), (60.0, False)):
        outbound = line(0, 0, 3000, 0, step=10)
        back = line(2990, offset, 0, offset, step=10) + [at(0, 0)]
        assert (detect_out_and_back(points_of(outbound + back)) is not None) is detected


@pytest.mark.parametrize("lat0, lon0", [(0.0, 0.0), (0.0, 179.9995), (89.5, 0.0), (-89.9, 10.0)])
def test_the_bucket_filter_finds_exactly_what_a_full_search_finds(lat0, lon0):
    # Front points on a synthetic zigzag; probes on a grid around it, some within 50 m, some not.
    front = points_of(relocate(path((0, 0), (300, 40), (0, 80), (300, 120), step=7), lat0, lon0))
    probes = points_of(relocate([at(x, y) for x in range(-80, 400, 9) for y in range(-80, 220, 9)], lat0, lon0))
    index = tg._NearIndex(front)
    hits = 0
    for probe in probes:
        full = any(haversine_m(probe.lat, probe.lon, p.lat, p.lon) <= tg.NEAR_M for p in front)
        assert index.has_point_within(probe) is full
        hits += full
    assert 0 < hits < len(probes)


def test_detection_on_a_long_dense_track_finishes():
    positions = out_and_back(length=100_000, step=10)  # about 20,000 points
    result = route(positions, "round_trip")
    assert isinstance(result, TargetGpxRoute) and result.turnaround_m == 100_000


def relocate(positions, lat0, lon0):
    """The same synthetic shape (metres east and north) drawn around another placeholder origin."""
    out = []
    for lat, lon in positions:
        x, y = math.radians(lon) * EARTH_RADIUS_M, math.radians(lat) * EARTH_RADIUS_M
        new_lon = lon0 + math.degrees(x / (EARTH_RADIUS_M * math.cos(math.radians(lat0))))
        out.append((lat0 + math.degrees(y / EARTH_RADIUS_M), ((new_lon + 180.0) % 360.0) - 180.0))
    return out


def test_detection_works_across_the_antimeridian_and_near_a_pole():
    # Placeholder origins: 0 deg N next to 180 deg (open Pacific) and 89.5 deg N (Arctic Ocean).
    across = relocate(out_and_back(), 0.0, 179.99)
    assert any(lon > 0 for _, lon in across) and any(lon < 0 for _, lon in across)
    assert detect_out_and_back(points_of(across)) is not None
    assert detect_out_and_back(points_of(relocate(circle(), 0.0, 179.99))) is None
    polar = relocate(out_and_back(), 89.5, 0.0)
    assert detect_out_and_back(points_of(polar)) is not None
    assert detect_out_and_back(points_of(relocate(circle(), 89.5, 0.0))) is None


# --- the rider's turnaround position (S61, S62, S80; CL-R1-10 item 4; CL-R1-18) --------------------

@pytest.mark.parametrize("km", [0, 0.0, -0.0, -1.0, -0.0005, 0.0004, 1e9, float("nan"), float("inf"), float("-inf")])
def test_illegal_turnaround_positions_are_not_round_trip(km):
    for positions in (circle(), out_and_back()):
        assert route(positions, "round_trip", km) == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


def test_a_turnaround_at_or_beyond_the_total_length_is_not_round_trip():
    positions = circle()
    total = cumulative_m(points_of(positions))[-1]
    for metres in (math.ceil(total), math.ceil(total) + 1, 10 * math.ceil(total)):
        assert route(positions, "round_trip", metres / 1000) == \
            TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


@pytest.mark.parametrize("bad", ["1.5", True, False, [1.5], {"km": 1.5}])
def test_turnaround_must_be_a_number(bad):
    with pytest.raises(TypeError):
        route(circle(), "round_trip", bad)


def test_an_illegal_turnaround_on_a_clear_out_and_back_does_not_fall_back_to_detection():
    assert isinstance(route(out_and_back(), "round_trip"), TargetGpxRoute)
    for km in (0.0, -1.0, 99.0):
        assert route(out_and_back(), "round_trip", km) == \
            TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


def oracle_index(cum: list[float], metres: int) -> int | None:
    """CL-R1-22 items 2-3 computed point by point with Decimal: the test's own oracle."""
    total = cum[-1]
    best = None
    for i, c in enumerate(cum):
        d = Decimal(repr(c))
        ci = int(d.quantize(Decimal(1), rounding=ROUND_HALF_UP))
        if not (0 < c < total and 0 < ci < total):
            continue
        gap = abs(d - Decimal(metres))
        if best is None or gap < best[0]:
            best = (gap, i)
    return None if best is None else best[1]


def test_t1_s61_a_loop_is_cut_at_the_nearest_track_point_to_the_riders_position():
    positions = circle()
    cum = cumulative_m(points_of(positions))
    i = 60
    assert cum[i + 1] - cum[i] > 10                      # about 21 m between the two points
    nearer_next = math.floor(cum[i + 1]) - 1               # strictly between, closer to point i + 1
    nearer_this = math.ceil(cum[i]) + 1                    # strictly between, closer to point i
    for metres, expected in ((nearer_next, i + 1), (nearer_this, i)):
        assert cum[i] < metres < cum[i + 1]
        result = route(positions, "round_trip", metres / 1000)
        assert isinstance(result, TargetGpxRoute)
        assert result.turnaround_source == "rider"
        assert len(result.legs[0].points) - 1 == expected
        assert result.turnaround_m == metres_half_up(cum[expected])
        assert result.turnaround_m != metres                 # c_k, not the requested m
        assert result.route_id == target_gpx_route_id(result.target_gpx_ref, "round_trip", result.turnaround_m)
        assert_slices_of_the_file(result, positions)


def test_t2_s80_on_a_clear_out_and_back_the_riders_position_wins_between_points():
    positions = out_and_back()
    detected = route(positions, "round_trip")
    farthest = len(detected.legs[0].points) - 1
    cum = cumulative_m(points_of(positions))
    metres = 1234
    assert metres != detected.turnaround_m
    assert any(cum[j] < metres < cum[j + 1] for j in range(len(cum) - 1))
    result = route(positions, "round_trip", metres / 1000)
    k = len(result.legs[0].points) - 1
    assert k == oracle_index(cum, metres) == 25 and k != farthest
    assert result.turnaround_source == "rider" and result.turnaround_m == metres_half_up(cum[k]) == 1250
    assert result.route_id != detected.route_id
    assert_slices_of_the_file(result, positions)


def test_t3_s78_full_flow_rider_and_detected_with_equal_metres_give_the_same_route():
    positions = out_and_back(length=3137.3, step=47.1)
    points = points_of(positions)
    cum = cumulative_m(points)
    detected = route(positions, "round_trip")
    farthest = len(detected.legs[0].points) - 1
    assert Decimal(repr(cum[farthest])) != Decimal(detected.turnaround_m)   # not a whole number of metres
    rider = route(positions, "round_trip", detected.turnaround_m / 1000)   # no distance replaced
    assert rider.turnaround_source == "rider"
    assert rider.turnaround_m == detected.turnaround_m
    assert rider.route_id == detected.route_id
    assert [leg.points for leg in rider.legs] == [leg.points for leg in detected.legs]
    # two different positions that select the same point: same route_id
    near_same = route(positions, "round_trip", (detected.turnaround_m + 3) / 1000)
    assert len(near_same.legs[0].points) - 1 == farthest and near_same.route_id == detected.route_id
    # a position that selects another point: another route_id
    other = route(positions, "round_trip", (detected.turnaround_m - 200) / 1000)
    assert len(other.legs[0].points) - 1 != farthest and other.route_id != detected.route_id
    assert route(positions, "one_way").route_id not in {detected.route_id, other.route_id}
    for result in (detected, rider, near_same, other):
        assert_slices_of_the_file(result, positions)


@pytest.mark.parametrize("cum, metres, expected", [
    ([0.0, 999.5, 1000.5, 2000.0], 1000, 1),             # tie at 0.5: the lower index
    ([0.0, 1023.9, 1024.1, 2048.0], 1024, 1),            # tie in Decimal, not in float differences
    ([0.0, 500.0, 1000.0, 1000.0, 2000.0], 1000, 2),     # a repeated point: the first copy
    ([0.0, 900.0, 1800.0, 2700.0], 10, 1),               # nearest is the start: the first usable point
    ([0.0, 900.0, 1800.0, 2700.0], 2690, 2),             # nearest is the end: the last usable point
    ([0.0, 0.4, 900.0, 1800.0], 1, 2),                   # 0 < cum but c = 0: not usable
    ([0.0, 900.0, 1999.6, 2000.0], 1999, 1),             # c = total: not usable
    ([0.0, 0.3, 1999.7, 2000.0], 1000, None),            # no usable point
    ([0.0, 600.4, 600.6, 2000.0], 601, 2),               # exact comparison picks the nearer one
])
def test_t4_the_selection_follows_the_definition(cum, metres, expected):
    assert rider_turnaround_index(cum, metres) == expected == oracle_index(cum, metres)


def test_t4_no_usable_point_through_the_route_is_turnaround_unconfirmed(monkeypatch):
    positions = circle()
    real_total = cumulative_m(points_of(positions))[-1]
    fake = [0.0] * (len(positions) - 1) + [real_total]   # every inner point at distance 0
    monkeypatch.setattr(tg, "cumulative_m", lambda points: list(fake))
    assert route(positions, "round_trip", 1.0) == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


@pytest.mark.parametrize("boundary", ["start", "end"])
def test_a_detected_boundary_that_is_not_usable_is_turnaround_unconfirmed(monkeypatch, boundary):
    # CL-R1-22 item 6 (defensive): detection never returns these, so the detector is replaced.
    positions = out_and_back()
    index = 0 if boundary == "start" else len(positions) - 1
    monkeypatch.setattr(tg, "detect_out_and_back", lambda points, cum=None: index)
    assert route(positions, "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


@pytest.mark.parametrize("name, positions", [
    ("loop", circle()), ("out_and_back", out_and_back()), ("figure_eight", figure_eight()),
    ("sparse_loop", circle(radius=1500.0, n=12)),
])
def test_t5_every_legal_whole_metre_gives_the_route_the_definition_selects(name, positions):
    cum = cumulative_m(points_of(positions))
    total = cum[-1]
    checked = 0
    for metres in range(1, math.ceil(total), 37):
        result = route(positions, "round_trip", metres / 1000)
        assert isinstance(result, TargetGpxRoute), metres
        k = len(result.legs[0].points) - 1
        assert k == oracle_index(cum, metres)
        assert result.turnaround_source == "rider"
        assert abs(Decimal(repr(cum[k])) - metres) <= min(
            abs(Decimal(repr(cum[j])) - metres) for j in range(1, len(cum) - 1))
        assert_slices_of_the_file(result, positions)
        checked += 1
    assert checked > 10


def _with_exact_cumulative(monkeypatch, positions, exact_at: dict[int, float]):
    """Make the distance along the track exactly `metres` at some point indices (S61/S80 at a point).

    Synthetic shapes never put a point at an exact integer distance, so the distances are replaced
    by the real ones rounded where asked. Only the cut is tested this way.
    """
    real = cumulative_m(points_of(positions))
    fixed = list(real)
    for index, metres in exact_at.items():
        fixed[index] = metres
    monkeypatch.setattr(tg, "cumulative_m", lambda points: list(fixed))
    return real


def test_a_loop_is_cut_at_the_riders_position_when_a_point_is_there(monkeypatch):
    positions = circle()
    real = _with_exact_cumulative(monkeypatch, positions, {60: 1257.0})
    assert real[60] == pytest.approx(1256.6, abs=1)
    result = route(positions, "round_trip", 1.257)
    assert isinstance(result, TargetGpxRoute)
    assert result.turnaround_m == 1257 and result.turnaround_source == "rider"
    assert len(result.legs[0].points) == 61
    assert_slices_of_the_file(result, positions, lengths=False)


def test_the_riders_legal_position_wins_over_the_detected_one(monkeypatch):
    positions = out_and_back()
    detected = route(positions, "round_trip")
    assert detected.turnaround_m == 3000
    _with_exact_cumulative(monkeypatch, positions, {20: 1000.0})
    result = route(positions, "round_trip", 1.0)
    assert result.turnaround_source == "rider" and result.turnaround_m == 1000
    assert len(result.legs[0].points) == 21
    assert result.route_id != detected.route_id
    assert_slices_of_the_file(result, positions, lengths=False)


@pytest.mark.parametrize("km, metres", [
    (0.0005, 1), (1.0005, 1001), (0.5005, 501), (2.0005, 2001), (1.0004, 1000), (1.0006, 1001),
    (2.5, 2500), (3, 3000), (12.3456, 12346), (0.0015, 2), (0.0025, 3),
])
def test_turnaround_km_to_metres_rounds_half_up_from_the_decimal_form(km, metres):
    assert turnaround_m_from_km(km) == metres


def test_float_multiplication_would_round_wrongly_and_is_not_used():
    assert 0.5005 * 1000 == 500.49999999999994
    assert turnaround_m_from_km(0.5005) == 501


@pytest.mark.parametrize("value, metres", [
    (1000.5, 1001), (1000.4999, 1000), (0.5, 1), (1.5, 2), (2.5, 3), (2999.9999999, 3000), (3000.0000001, 3000),
])
def test_detected_metres_round_half_up_not_half_even(value, metres):
    assert metres_half_up(value) == metres
    assert round(1000.5) == 1000  # the builtin is half-even, which is why it is not used


def test_target_gpx_module_does_not_call_round():
    tree = ast.parse(Path(tg.__file__).read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    assert "round" not in {c.func.id for c in calls}


# --- route_id (S58 RG-, S78; CL-R1-10 item 6; CL-R1-13) --------------------------------------------

REF = hashlib.sha256(b"synthetic").hexdigest()


def test_route_id_is_rg_plus_the_first_10_hex_of_the_defined_text():
    assert target_gpx_route_id(REF, "one_way") == "RG-" + hashlib.sha256(f"{REF}:one_way".encode()).hexdigest()[:10]
    assert target_gpx_route_id(REF, "round_trip", 3000) == \
        "RG-" + hashlib.sha256(f"{REF}:round_trip:3000".encode()).hexdigest()[:10]


def test_every_produced_route_id_matches_the_contract_pattern():
    produced = [target_gpx_route_id(REF, "one_way")] + [target_gpx_route_id(REF, "round_trip", m) for m in (1, 999, 3000, 10**9)]
    produced += [route(out_and_back(), "one_way").route_id, route(out_and_back(), "round_trip").route_id]
    for route_id in produced:
        assert re.search(ROUTE_ID_PATTERN, route_id)
        assert route_id.startswith("RG-") and re.fullmatch(r"RG-[0-9a-f]{10}", route_id, flags=re.ASCII)
        assert not re.search(ROUTE_ID_PATTERN, route_id + "\n")


@pytest.mark.parametrize("bad_ref", [
    REF + "\n", " " + REF, REF + " ", REF.upper(), REF[:-1], REF + "0", "",
    REF[:-1] + "١",          # an Arabic-Indic digit
    REF[:-1] + "０",          # a full-width digit
    None, 123,
])
def test_route_id_rejects_a_reference_that_is_not_64_lowercase_ascii_hex(bad_ref):
    with pytest.raises(ValueError):
        target_gpx_route_id(bad_ref, "one_way")


@pytest.mark.parametrize("trip_type, metres", [
    ("one_way", 3000), ("round_trip", None), ("round_trip", 0), ("round_trip", -1), ("round_trip", True),
    ("round_trip", 3000.0), ("round_trip", "3000"), ("round_trip", "3000\n"), ("round_trip\n", 3000), ("loop", None),
])
def test_route_id_rejects_inconsistent_trip_type_and_turnaround(trip_type, metres):
    with pytest.raises(ValueError):
        target_gpx_route_id(REF, trip_type, metres)


def test_s78_same_file_same_turnaround_metres_same_route_id_different_metres_different():
    positions = out_and_back()
    detected = route(positions, "round_trip")
    rider_metres = turnaround_m_from_km(detected.turnaround_m / 1000)
    assert rider_metres == detected.turnaround_m
    assert target_gpx_route_id(detected.target_gpx_ref, "round_trip", rider_metres) == detected.route_id
    assert target_gpx_route_id(detected.target_gpx_ref, "round_trip", detected.turnaround_m + 1) != detected.route_id
    one_way = route(positions, "one_way")
    assert one_way.target_gpx_ref == detected.target_gpx_ref
    assert one_way.route_id != detected.route_id


def test_s78_through_the_route_rider_and_detected_with_equal_metres_give_the_same_route_id(monkeypatch):
    positions = out_and_back()
    detected = route(positions, "round_trip")
    boundary = len(detected.legs[0].points) - 1
    _with_exact_cumulative(monkeypatch, positions, {boundary: float(detected.turnaround_m)})
    rider = route(positions, "round_trip", detected.turnaround_m / 1000)
    assert rider.turnaround_source == "rider"
    assert rider.route_id == detected.route_id
    assert [leg.points for leg in rider.legs] == [leg.points for leg in detected.legs]


def test_a_different_file_gives_a_different_route_id():
    a = route(out_and_back(), "round_trip")
    b = route(out_and_back(offset=12.0), "round_trip")
    assert a.target_gpx_ref != b.target_gpx_ref and a.route_id != b.route_id


# --- no reversal, no made-up points (S64) ----------------------------------------------------------

@pytest.mark.parametrize("positions", [out_and_back(), out_and_back(length=5000, step=37), bump_back(500)])
def test_detected_round_trips_are_slices_of_the_file(positions):
    result = route(positions, "round_trip")
    assert isinstance(result, TargetGpxRoute)
    assert_slices_of_the_file(result, positions)
    original = points_of(positions)
    assert result.legs[1].points != tuple(reversed(result.legs[0].points))
    assert set(result.legs[0].points) | set(result.legs[1].points) <= set(original)


def test_a_one_way_track_is_not_reversed_or_completed_into_a_round_trip():
    positions = line(0, 0, 3000, 0)
    assert route(positions, "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, END_NOT_AT_START)
    result = route(positions, "one_way")
    assert len(result.legs) == 1
    assert_slices_of_the_file(result, positions)


# --- privacy: no path or file name in results, errors or logs (S10; CL-R1-10 item 7) ----------------

SECRET_DIR = "SyntheticUserNameDir"
SECRET_STEM = "2026-01-02-synthetic-home-ride"


def _secret_file(tmp_path: Path, data: bytes) -> Path:
    folder = tmp_path / SECRET_DIR
    folder.mkdir()
    file = folder / f"{SECRET_STEM}.gpx"
    file.write_bytes(data)
    return file


def _assert_no_path(text: str, file: Path):
    for secret in (SECRET_DIR, SECRET_STEM, file.name, str(file), str(file.parent), file.as_posix()):
        assert secret not in text


@pytest.mark.parametrize("shape, trip_type, km", [
    ("out_and_back", "round_trip", None), ("out_and_back", "one_way", None), ("line", "round_trip", None),
    ("loop", "round_trip", None), ("loop", "round_trip", 0.0), ("short", "one_way", None), ("garbage", "one_way", None),
])
def test_results_and_errors_carry_no_path_or_file_name(tmp_path, caplog, capsys, shape, trip_type, km):
    shapes = {"out_and_back": out_and_back(), "line": line(0, 0, 3000, 0), "loop": circle(), "short": line(0, 0, 500, 0)}
    data = b"<not-gpx" if shape == "garbage" else gpx(shapes[shape])
    file = _secret_file(tmp_path, data)
    caplog.set_level(logging.DEBUG)
    result = target_gpx_route(file, trip_type, km)
    _assert_no_path(repr(result), file)
    _assert_no_path(str(vars(result)), file)
    out = capsys.readouterr()
    _assert_no_path(out.out + out.err, file)
    assert caplog.records == []


def test_missing_or_unopenable_files_are_invalid_without_naming_the_file(tmp_path, caplog):
    caplog.set_level(logging.DEBUG)
    missing = tmp_path / SECRET_DIR / f"{SECRET_STEM}.gpx"
    assert target_gpx_route(missing, "one_way") == TargetGpxError(TARGET_GPX_INVALID, "unreadable")
    folder = tmp_path / SECRET_DIR
    folder.mkdir()
    assert target_gpx_route(folder, "one_way") == TargetGpxError(TARGET_GPX_INVALID, "unreadable")
    with pytest.raises(GpxGeometryError) as caught:
        read_gpx_geometry(missing)
    error = caught.value
    _assert_no_path(str(error) + repr(error) + repr(error.args), missing)
    assert error.__context__ is None and error.__cause__ is None
    assert caplog.records == []


def test_parse_errors_do_not_carry_the_parser_message_or_a_chained_exception():
    with pytest.raises(GpxGeometryError) as caught:
        parse_gpx_geometry(b"<gpx><unclosed>")
    assert caught.value.__context__ is None and caught.value.__cause__ is None
    assert "line" not in str(caught.value) and "column" not in str(caught.value)


# --- R1-F1 (audit issue-15-c1-r1): undecodable or unparseable bytes are target_gpx_invalid --------

def _declared(encoding: str, positions=None) -> bytes:
    """A synthetic GPX whose XML declaration names `encoding` (the body itself is ASCII)."""
    body = gpx(out_and_back() if positions is None else positions)
    return body.replace(b'encoding="UTF-8"', f'encoding="{encoding}"'.encode("ascii"), 1)


_BILLION = (b'<?xml version="1.0"?><!DOCTYPE g [<!ENTITY a "aaaaaaaaaa">'
            + b"".join(f'<!ENTITY {c} "{("&" + p + ";") * 10}">'.encode() for p, c in zip("abcdefg", "bcdefgh"))
            + f']><gpx xmlns="{GPX11}">&h;</gpx>'.encode())

UNPARSEABLE = {
    # LookupError from the parser before the fix: an unknown codec name, and non-text codecs.
    "unknown_encoding": _declared("SyntheticUnknownEncodingProbe"),
    "hex_codec": _declared("hex_codec"),
    "rot_13": _declared("rot_13"),
    "zlib_codec": _declared("zlib_codec"),
    "base64_codec": _declared("base64_codec"),
    # ValueError / UnicodeError / UnicodeDecodeError (already caught; kept as regressions).
    "multibyte_big5": _declared("big5"),
    "idna": _declared("idna"),
    "punycode": _declared("punycode"),
    # ParseError: entity-expansion limit, external and undefined entities.
    "entity_expansion": _BILLION,
    "external_entity": (b'<?xml version="1.0"?><!DOCTYPE g [<!ENTITY x SYSTEM "file:///synthetic-none">]>'
                        + f'<gpx xmlns="{GPX11}">&x;</gpx>'.encode()),
}


def test_the_probe_inputs_still_raise_in_the_bare_parser():
    import xml.etree.ElementTree as ET
    with pytest.raises(LookupError):
        ET.fromstring(UNPARSEABLE["unknown_encoding"])  # what escaped before the fix


@pytest.mark.parametrize("name", sorted(UNPARSEABLE))
def test_unparseable_bytes_give_a_fixed_unreadable_error_without_a_chain(name):
    with pytest.raises(GpxGeometryError) as caught:
        parse_gpx_geometry(UNPARSEABLE[name])
    error = caught.value
    assert error.reason == "unreadable"
    assert error.__context__ is None and error.__cause__ is None
    assert str(error) == "target GPX cannot be read (unreadable)"
    for leaked in ("Synthetic", "encoding", "line", "column", "codec", "amplification", "entity"):
        assert leaked not in str(error) + repr(error)


@pytest.mark.parametrize("trip_type", ["one_way", "round_trip"])
@pytest.mark.parametrize("name", sorted(UNPARSEABLE))
def test_unparseable_bytes_through_the_bytes_entry_are_target_gpx_invalid(caplog, capsys, name, trip_type):
    caplog.set_level(logging.DEBUG)
    for km in (None, 1.5):
        result = target_gpx_route_from_bytes(UNPARSEABLE[name], trip_type, km)
        assert result == TargetGpxError(TARGET_GPX_INVALID, "unreadable")
        assert not isinstance(result, TargetGpxRoute)
    out = capsys.readouterr()
    assert out.out == "" and out.err == "" and caplog.records == []


@pytest.mark.parametrize("trip_type", ["one_way", "round_trip"])
@pytest.mark.parametrize("name", sorted(UNPARSEABLE))
def test_unparseable_files_through_the_path_entry_are_target_gpx_invalid(tmp_path, caplog, capsys, name, trip_type):
    caplog.set_level(logging.DEBUG)
    file = _secret_file(tmp_path, UNPARSEABLE[name])
    for argument in (file, str(file)):
        result = target_gpx_route(argument, trip_type)
        assert result == TargetGpxError(TARGET_GPX_INVALID, "unreadable")
        _assert_no_path(repr(result) + str(vars(result)), file)
    with pytest.raises(GpxGeometryError) as caught:
        read_gpx_geometry(file)
    error = caught.value
    _assert_no_path(str(error) + repr(error) + repr(error.args), file)
    assert error.__context__ is None and error.__cause__ is None
    out = capsys.readouterr()
    _assert_no_path(out.out + out.err, file)
    assert caplog.records == []


def test_caller_type_errors_are_still_raised_and_not_turned_into_route_errors(tmp_path):
    for bad in ("<gpx/>", None, 123, ["<gpx/>"]):
        with pytest.raises(TypeError):
            target_gpx_route_from_bytes(bad, "one_way")
    for bad in (0, 1.5, b"synthetic.gpx", None):
        with pytest.raises(TypeError):
            target_gpx_route(bad, "one_way")
    with pytest.raises(TripTypeRequiredError):
        target_gpx_route_from_bytes(UNPARSEABLE["unknown_encoding"], None)
    with pytest.raises(TypeError):
        target_gpx_route_from_bytes(gpx(circle()), "round_trip", "1.5")


def test_a_valid_known_encoding_declaration_is_still_read():
    for encoding in ("UTF-8", "utf-8", "ascii", "cp1252", "ISO-8859-1"):
        assert isinstance(target_gpx_route_from_bytes(_declared(encoding), "round_trip"), TargetGpxRoute)


def test_a_rider_turnaround_route_carries_no_path(tmp_path, caplog):
    caplog.set_level(logging.DEBUG)
    file = _secret_file(tmp_path, gpx(circle()))
    result = target_gpx_route(file, "round_trip", 1.2345)
    assert isinstance(result, TargetGpxRoute) and result.turnaround_source == "rider"
    _assert_no_path(repr(result) + str(vars(result)), file)
    assert caplog.records == []


def test_route_and_error_have_no_field_for_a_path():
    assert set(TargetGpxRoute.__dataclass_fields__) == {
        "route_id", "trip_type", "target_gpx_ref", "total_length_m", "turnaround_m", "turnaround_source",
        "legs", "route_source"}
    assert set(TargetGpxError.__dataclass_fields__) == {"code", "case"}
    assert set(geometry_module.GpxGeometry.__dataclass_fields__) == {"points", "sha256", "source"}


@pytest.mark.parametrize("module", [geometry_module, tg])
def test_the_new_modules_do_not_log_print_use_the_network_or_read_the_environment(module):
    source = Path(module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    banned = {"logging", "socket", "http", "urllib", "requests", "httpx", "ssl", "subprocess"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            names = {(node.module or "").split(".")[0]}
        else:
            names = set()
        assert not names & banned
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id != "print"
    assert "environ" not in source and "getenv" not in source


def test_no_network_is_used(monkeypatch, tmp_path):
    def refuse(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)
    file = tmp_path / "synthetic.gpx"
    file.write_bytes(gpx(out_and_back()))
    assert isinstance(target_gpx_route(file, "round_trip"), TargetGpxRoute)
    assert isinstance(target_gpx_route(file, "one_way"), TargetGpxRoute)
    assert route(circle(), "round_trip") == TargetGpxError(TARGET_GPX_NOT_ROUND_TRIP, TURNAROUND_UNCONFIRMED)


# --- wording (H-3; CL-R1-10 item 5) ----------------------------------------------------------------

def test_the_detection_is_described_as_not_validated():
    for text in (tg.__doc__, tg.detect_out_and_back.__doc__):
        assert "NOT validated with real data" in text
    source = Path(tg.__file__).read_text(encoding="utf-8").lower()
    for claim in ("has been validated", "is validated", "was validated", "proven", "verified threshold"):
        assert claim not in source
