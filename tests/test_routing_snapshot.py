"""SPEC-R1 R1-2 (Issue #14): canonical JSON, snapshot_id / RS- route_id, snapshot structure, request_key.

All inputs are synthetic (tests/routing_synthetic.py). No test opens a network connection.
"""
from __future__ import annotations

import copy
import re

import pytest

from moto_copilot.contracts import validate_route_catalog
from moto_copilot.contracts.schemas import ROUTE_ID_PATTERN, SNAPSHOT_ID_PATTERN
from moto_copilot.routing import (
    CanonicalError,
    RequestKeyError,
    SnapshotValidationError,
    canonical_json,
    compute_snapshot_id,
    place_fingerprint,
    request_key_content,
    route_id_for,
    sha256_hex,
    validate_snapshot,
)
from moto_copilot.routing.snapshot import LEG_FIELDS, SNAPSHOT_FIELDS

import routing_synthetic as syn


# --- (a) canonical JSON (SPEC-001 §2) -------------------------------------------------------

def test_canonical_json_sorts_keys_and_has_no_whitespace():
    assert canonical_json({"b": 1, "a": {"d": [1, 2], "c": None}, "e": True}) == '{"a":{"c":null,"d":[1,2]},"b":1,"e":true}'


def test_canonical_json_is_utf8_without_escaping_non_ascii():
    from moto_copilot.routing import canonical_bytes
    assert canonical_bytes({"name": "台 1 線"}) == '{"name":"台 1 線"}'.encode("utf-8")


def test_canonical_json_six_places_for_coordinates_and_other_floats():
    assert canonical_json({"lat": 23.12345678, "lon": 120.5}) == '{"lat":23.123456,"lon":120.500000}'
    assert canonical_json({"factor": 0.1234567}) == '{"factor":0.123456}'


def test_canonical_json_one_place_for_values_in_metres():
    assert canonical_json({"endpoint_offset_m": {"start": 12.36, "end": 0.04}}) == '{"endpoint_offset_m":{"end":0.0,"start":12.3}}'
    assert canonical_json({"via_offset_m": [7.89, 200.0]}) == '{"via_offset_m":[7.8,200.0]}'
    # _km is not metres: six places.
    assert canonical_json({"turnaround_km": 1.23456789}) == '{"turnaround_km":1.234567}'


def test_canonical_json_keeps_integers_and_writes_negative_zero_as_zero():
    assert canonical_json({"distance_m": 12345, "x": -0.0, "y": -1e-9}) == '{"distance_m":12345,"x":0.000000,"y":0.000000}'


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_canonical_json_rejects_non_finite_floats(value):
    with pytest.raises(CanonicalError):
        canonical_json({"x": value})


@pytest.mark.parametrize("value", [{1: "a"}, {"a": (1, 2)}, {"a": {1, 2}}, {"a": b"x"}])
def test_canonical_json_rejects_non_json_values(value):
    with pytest.raises(CanonicalError):
        canonical_json(value)


def test_canonical_json_is_idempotent():
    from moto_copilot.routing.canonical import normalized
    value = {"lat": 23.1234569, "via_offset_m": [1.99], "n": 3}
    once = normalized(value)
    assert canonical_json(once) == canonical_json(value)
    assert normalized(once) == once


# --- S56: precision of the normalization -----------------------------------------------------

@pytest.mark.parametrize("a, b", [
    (23.123456, 23.123457),
    (23.1234569, 23.1234571),   # sixth decimal differs (6 vs 7) though the values are 2e-7 apart
    (-0.0000011, -0.0000021),
])
def test_s56_coordinates_differing_in_the_sixth_decimal_hash_differently(a, b):
    assert sha256_hex({"lat": a}) != sha256_hex({"lat": b})
    s1 = syn.snapshot(legs=[_leg_with_lat(a)])
    s2 = syn.snapshot(legs=[_leg_with_lat(b)])
    assert s1["snapshot_id"] != s2["snapshot_id"]


@pytest.mark.parametrize("a, b", [
    (23.1234561, 23.1234569),   # only the seventh decimal differs, across a rounding boundary
    (23.123456, 23.12345699999),
    (120.0000001, 120.0000009),
])
def test_s56_coordinates_differing_only_after_the_sixth_decimal_hash_the_same(a, b):
    assert sha256_hex({"lat": a}) == sha256_hex({"lat": b})
    s1 = syn.snapshot(legs=[_leg_with_lat(a)])
    s2 = syn.snapshot(legs=[_leg_with_lat(b)])
    assert s1["snapshot_id"] == s2["snapshot_id"]


def test_s56_offsets_in_metres_use_one_decimal_place():
    base = syn.snapshot()
    same = syn.snapshot(legs=[syn.leg(shape="synthetic-shape-outbound-1", endpoint_offset_m={"start": 12.34, "end": 45.69})])
    other = syn.snapshot(legs=[syn.leg(shape="synthetic-shape-outbound-1", endpoint_offset_m={"start": 12.4, "end": 45.6})])
    assert same["snapshot_id"] == base["snapshot_id"]
    assert other["snapshot_id"] != base["snapshot_id"]


def _leg_with_lat(lat):
    value = syn.leg()
    value["request"]["locations"][0]["lat"] = lat
    return value


# --- (b) snapshot_id and the RS- route_id (S36, S53, S54, S58) -------------------------------

def test_s58_generated_ids_match_the_section_2_patterns():
    for trip_type in ("one_way", "round_trip"):
        snap = syn.snapshot(trip_type)
        assert re.search(SNAPSHOT_ID_PATTERN, snap["snapshot_id"])
        route_id = route_id_for(snap["snapshot_id"])
        assert re.search(ROUTE_ID_PATTERN, route_id)
        assert route_id.startswith("RS-") and route_id[3:] == snap["snapshot_id"][3:]


def test_s58_snapshot_id_is_sn_plus_first_10_hex_of_the_hash_scope():
    snap = syn.snapshot("round_trip")
    scope = {k: v for k, v in snap.items() if k != "snapshot_id"}
    scope["legs"] = [{k: v for k, v in leg.items() if k != "fetched_at"} for leg in scope["legs"]]
    assert snap["snapshot_id"] == "SN-" + sha256_hex(scope)[:10]


def test_s58_ids_pass_the_contract_2_checks_for_a_routing_route():
    snap = syn.snapshot()
    route_id = route_id_for(snap["snapshot_id"])
    routes = [{
        "route_id": route_id, "name": "Synthetic", "n_segments": 1, "total_length_m": 12345.0,
        "source_trip_id": None, "route_source": "routing", "snapshot_id": snap["snapshot_id"],
        "trip_type": "one_way", "category_scheme": "synthetic", "catalog_version": "synthetic",
    }]
    segments = [{
        "route_id": route_id, "seg_index": 0, "length_m": 12345.0, "cum_length_m": 12345.0,
        "seg_category": "C1", "end_lat": syn.DEFINITIONS["SYN-DEST"]["lat"], "end_lon": syn.DEFINITIONS["SYN-DEST"]["lon"],
    }]
    checkpoints = [
        {"checkpoint_id": f"{route_id}-CP01", "route_id": route_id, "kind": "start", "after_seg_count": 0,
         "name": "Start", "station_ref": None},
        {"checkpoint_id": f"{route_id}-CP02", "route_id": route_id, "kind": "end", "after_seg_count": 1,
         "name": "End", "station_ref": None},
    ]
    assert validate_route_catalog(routes, segments, checkpoints) == []


@pytest.mark.parametrize("bad", [
    "SN-0123456789\n", "SN-0123456789 ", " SN-0123456789", "SN-012345678٩", "SN-０１２３４５６７８９",
    "SN-ABCDEF0123", "SN-012345678", "SN-01234567890", "RS-0123456789", "", None, 123,
])
def test_s58_cl_r1_13_bad_snapshot_ids_are_rejected(bad):
    with pytest.raises(ValueError):
        route_id_for(bad)
    snap = syn.snapshot()
    snap["snapshot_id"] = bad
    assert any("snapshot_id" in e for e in validate_snapshot(snap))


def test_s53_same_content_with_other_fetch_times_has_the_same_snapshot_id():
    first = syn.snapshot("round_trip", fetched_at="2026-10-01T08:00:00+08:00")
    later = syn.snapshot("round_trip", fetched_at="2026-11-18T17:30:05.250+08:00")
    assert first["legs"][0]["fetched_at"] != later["legs"][0]["fetched_at"]
    assert first["snapshot_id"] == later["snapshot_id"]
    assert compute_snapshot_id(first) == compute_snapshot_id(later)


def _hash_scope_changes():
    """One change for every field inside the hash scope (S36, S54)."""
    def top(field, value):
        return lambda s: s.__setitem__(field, value)

    def first_leg(field, value):
        return lambda s: s["legs"][0].__setitem__(field, value)

    return {
        "shape": first_leg("shape", "synthetic-shape-outbound-2"),
        "request": lambda s: s["legs"][0]["request"]["locations"][1].__setitem__("ref_id", "SYN-VIA-B"),
        "leg_routing_params": lambda s: s["legs"][0]["request"]["routing_params"].__setitem__("costing", "auto"),
        "distance_m": first_leg("distance_m", 12346),
        "engine_time_s": first_leg("engine_time_s", 1501),
        "road_names": first_leg("road_names", ["Synthetic Road 2", "Synthetic Road 1"]),
        "freeway_check_method": first_leg("freeway_check_method", syn.OTHER_METHOD),
        "endpoint_offset_m": first_leg("endpoint_offset_m", {"start": 12.3, "end": 45.7}),
        "via_offset_m": first_leg("via_offset_m", [7.9]),
        "return_leg_shape": lambda s: s["legs"][1].__setitem__("shape", "synthetic-shape-return-2"),
        "request_key": top("request_key", syn.key("round_trip", via=(syn.VIA_B, syn.VIA_A))),
        "routing_params": top("routing_params", {"costing": "motorcycle"}),
        "engine_name": top("engine_name", "synthetic-engine-b"),
        "engine_version": top("engine_version", "unreported"),
        "map_data_date": top("map_data_date", None),
    }


@pytest.mark.parametrize("name", sorted(_hash_scope_changes()))
def test_s36_s54_any_change_inside_the_hash_scope_gives_a_new_snapshot_id(name):
    base = syn.snapshot("round_trip")
    changed = copy.deepcopy(base)
    _hash_scope_changes()[name](changed)
    assert compute_snapshot_id(changed) != base["snapshot_id"]


def test_s36_snapshot_id_and_fetched_at_are_outside_the_hash_scope():
    base = syn.snapshot("round_trip")
    changed = copy.deepcopy(base)
    changed["snapshot_id"] = "SN-ffffffffff"
    changed["legs"][0]["fetched_at"] = "2027-01-01T00:00:00+08:00"
    changed["legs"][1]["fetched_at"] = "2025-01-01T00:00:00+08:00"
    assert compute_snapshot_id(changed) == base["snapshot_id"]


def test_build_snapshot_does_not_change_its_arguments():
    legs = [syn.leg()]
    before = copy.deepcopy(legs)
    syn.snapshot(legs=legs)
    assert legs == before


def test_build_snapshot_takes_integer_offsets_as_floats():
    a = syn.snapshot(legs=[syn.leg(endpoint_offset_m={"start": 12, "end": 45}, via_offset_m=[7])])
    b = syn.snapshot(legs=[syn.leg(endpoint_offset_m={"start": 12.0, "end": 45.0}, via_offset_m=[7.0])])
    assert a == b
    assert isinstance(a["legs"][0]["via_offset_m"][0], float)


# --- (c) structure (SPEC-001 4.14; S23 structure part) ----------------------------------------

def test_s23_valid_one_way_and_round_trip_snapshots():
    one = syn.snapshot("one_way")
    two = syn.snapshot("round_trip")
    assert validate_snapshot(one) == []
    assert validate_snapshot(two) == []
    assert set(one) == set(SNAPSHOT_FIELDS)
    assert [leg["direction"] for leg in one["legs"]] == ["outbound"]
    assert [leg["direction"] for leg in two["legs"]] == ["outbound", "return"]
    for leg in two["legs"]:
        assert set(leg) == set(LEG_FIELDS)


@pytest.mark.parametrize("field", SNAPSHOT_FIELDS)
def test_s23_every_snapshot_field_is_required(field):
    snap = syn.snapshot()
    del snap[field]
    assert any(f"missing field {field}" in e for e in validate_snapshot(snap))


@pytest.mark.parametrize("field", LEG_FIELDS)
def test_s23_every_leg_field_is_required(field):
    snap = syn.snapshot("round_trip")
    del snap["legs"][1][field]
    assert any(f"missing field {field}" in e for e in validate_snapshot(snap))


@pytest.mark.parametrize("trip_type, directions", [
    ("one_way", []),
    ("one_way", ["return"]),
    ("one_way", ["outbound", "return"]),
    ("round_trip", ["outbound"]),
    ("round_trip", ["return", "outbound"]),
    ("round_trip", ["outbound", "outbound"]),
    ("round_trip", ["outbound", "return", "return"]),
])
def test_s23_legs_count_and_order_follow_the_trip_type(trip_type, directions):
    with pytest.raises(SnapshotValidationError) as exc:
        syn.snapshot(trip_type, legs=[syn.leg(d) for d in directions])
    assert any("$.legs" in e for e in exc.value.errors)


@pytest.mark.parametrize("where, key", [
    ("top", "elevation"),
    ("leg", "elevation"),
    ("leg", "height"),
    ("leg", "altitude_m"),
    ("request", "ele"),
    ("routing_params", "elevation_interval"),
])
def test_s23_snapshot_has_no_elevation_fields(where, key):
    snap = syn.snapshot()
    target = {
        "top": snap,
        "leg": snap["legs"][0],
        "request": snap["legs"][0]["request"]["locations"][0],
        "routing_params": snap["routing_params"],
    }[where]
    target[key] = 0
    assert any("elevation" in e or "unknown field" in e for e in validate_snapshot(snap))


@pytest.mark.parametrize("field, value", [
    ("request_key", "abc"),
    ("request_key", "A" * 64),
    ("request_key", "a" * 64 + "\n"),
    ("trip_type", "loop"),
    ("trip_type", None),
    ("routing_params", None),
    ("routing_params", []),
    ("engine_name", ""),
    ("engine_name", None),
    ("engine_version", ""),
    ("engine_version", None),
    ("map_data_date", "2026-13-01"),
    ("map_data_date", "2026-11-01T00:00:00+08:00"),
    ("map_data_date", "2026-11-01\n"),
    ("map_data_date", ""),
    ("legs", None),
    ("legs", {}),
])
def test_s23_snapshot_field_types(field, value):
    snap = syn.snapshot()
    snap[field] = value
    assert validate_snapshot(snap) != []


def test_dd_r1_2_map_data_date_may_be_null_and_engine_version_may_be_unreported():
    snap = syn.snapshot(map_data_date=None, engine_version="unreported")
    assert validate_snapshot(snap) == []
    assert snap["map_data_date"] is None


@pytest.mark.parametrize("field, value", [
    ("direction", "inbound"),
    ("request", None),
    ("request", "SYN-ORIGIN"),
    ("shape", ""),
    ("shape", None),
    ("distance_m", 12345.0),
    ("distance_m", -1),
    ("distance_m", True),
    ("engine_time_s", None),
    ("engine_time_s", 1.5),
    ("road_names", None),
    ("road_names", ["Synthetic Road 1", ""]),
    ("road_names", "Synthetic Road 1"),
    ("warnings", None),
    ("warnings", [{"code": "1", "text": "x"}]),
    ("warnings", [{"code": 1}]),
    ("warnings", [{"code": 1, "text": "x", "extra": 2}]),
    ("has_highway", None),
    ("has_highway", 0),
    ("freeway_check", "PASS"),
    ("freeway_check", None),
    ("freeway_check_method", ""),
    ("freeway_check_method", None),
    ("endpoint_offset_m", None),
    ("endpoint_offset_m", {"start": 1.0}),
    ("endpoint_offset_m", {"start": 1.0, "end": 2.0, "mid": 3.0}),
    ("endpoint_offset_m", {"start": "1.0", "end": 2.0}),
    ("endpoint_offset_m", {"start": -0.1, "end": 2.0}),
    ("via_offset_m", None),
    ("via_offset_m", [None]),
    ("via_offset_m", ["7.8"]),
    ("fetched_at", "2026-11-18T09:00:00"),
    ("fetched_at", "2026-11-18T09:00:00Z"),
    ("fetched_at", "2026-11-18T09:00:00+09:00"),
    ("fetched_at", "2026-11-18T09:00:00+08:00\n"),
    ("fetched_at", "2026-11-18T25:00:00+08:00"),
    ("fetched_at", None),
])
def test_s23_leg_field_types(field, value):
    snap = syn.snapshot()
    snap["legs"][0][field] = value
    assert validate_snapshot(snap) != []


@pytest.mark.parametrize("field, value", [
    ("has_highway", True),
    ("freeway_check", "fail"),
    ("warnings", [{"code": 1, "text": "synthetic warning"}]),
    ("endpoint_offset_m", {"start": 200.1, "end": 2.0}),
    ("endpoint_offset_m", {"start": 1.0, "end": 250.0}),
    ("via_offset_m", [7.8, 200.01]),
])
def test_stored_directions_satisfy_the_adoption_values_of_4_14(field, value):
    with pytest.raises(SnapshotValidationError):
        syn.snapshot(legs=[syn.leg(**{field: value})])


def test_offsets_of_exactly_200_m_and_empty_lists_are_valid():
    snap = syn.snapshot(legs=[syn.leg(endpoint_offset_m={"start": 200.0, "end": 0.0}, via_offset_m=[], road_names=[])])
    assert validate_snapshot(snap) == []


def test_snapshot_id_must_match_the_content():
    snap = syn.snapshot()
    snap["legs"][0]["shape"] = "synthetic-shape-outbound-tampered"
    assert any("does not match the hash" in e for e in validate_snapshot(snap))


def test_validation_messages_do_not_echo_values():
    snap = syn.snapshot()
    snap["legs"][0]["request"]["locations"][0]["height"] = 0.123987
    snap["legs"][0]["endpoint_offset_m"]["start"] = 987.654
    snap["legs"][0]["direction"] = "secret-direction-value"
    text = " ".join(validate_snapshot(snap))
    for fragment in ("0.123987", "987.654", "secret-direction-value", "0.101101", "0.202202"):
        assert fragment not in text


def test_validate_snapshot_rejects_a_non_object():
    assert validate_snapshot([]) != []
    assert validate_snapshot(None) != []


def test_validate_snapshot_reports_values_that_cannot_be_canonical():
    snap = syn.snapshot()
    snap["routing_params"] = {"x": float("nan")}
    assert any("canonical" in e for e in validate_snapshot(snap))


# --- (d) request_key (7.11 item 4; CL-R1-2; S37, S71, S72, S73) --------------------------------

def test_request_key_is_64_lowercase_hex_and_deterministic():
    k = syn.key()
    assert re.fullmatch(r"[0-9a-f]{64}", k)
    assert syn.key() == k


def test_s37_s73_swapping_the_order_of_the_vias_changes_the_request_key():
    assert syn.key(via=(syn.VIA_A, syn.VIA_B)) != syn.key(via=(syn.VIA_B, syn.VIA_A))


def test_s71_a_referenced_landmark_moved_within_six_decimals_changes_the_request_key():
    moved = copy.deepcopy(syn.DEFINITIONS)
    moved["SYN-VIA-B"]["lat"] = round(moved["SYN-VIA-B"]["lat"] + 0.000001, 6)
    assert syn.key(definitions=moved) != syn.key()
    moved_entry = copy.deepcopy(syn.DEFINITIONS)
    moved_entry["SYN-ROAD-ENTRY"]["lon"] = round(moved_entry["SYN-ROAD-ENTRY"]["lon"] + 0.000001, 6)
    assert syn.key(via=(syn.ROAD,), definitions=moved_entry) != syn.key(via=(syn.ROAD,))


def test_s71_a_change_after_the_sixth_decimal_does_not_change_the_request_key():
    moved = copy.deepcopy(syn.DEFINITIONS)
    moved["SYN-VIA-B"]["lat"] = moved["SYN-VIA-B"]["lat"] + 0.0000004
    assert syn.key(definitions=moved) == syn.key()


def test_s72_an_unreferenced_landmark_change_leaves_the_request_key_unchanged():
    changed = copy.deepcopy(syn.DEFINITIONS)
    changed["SYN-UNUSED"]["lat"] = 0.155555
    changed["SYN-NEW"] = {"lat": 0.1, "lon": 0.2}
    del changed["SYN-ROAD"]
    assert syn.key(definitions=changed) == syn.key()


@pytest.mark.parametrize("change", ["trip_type", "origin", "destination", "routing_params", "entry", "drop_via"])
def test_request_key_covers_every_part_of_the_request(change):
    base = syn.key()
    if change == "trip_type":
        assert syn.key(trip_type="one_way") != base
    elif change == "origin":
        assert syn.key(origin=syn.VIA_A) != base
    elif change == "destination":
        assert syn.key(destination=syn.VIA_A) != base
    elif change == "routing_params":
        assert syn.key(routing_params={"costing": "motorcycle"}) != base
    elif change == "entry":
        no_entry = dict(syn.ROAD, entry_ref_id=None)
        assert syn.key(via=(syn.ROAD,)) != syn.key(via=(no_entry,))
    else:
        assert syn.key(via=(syn.VIA_A,)) != base


def test_request_key_ignores_place_names_and_kinds_and_holds_no_coordinates():
    renamed = dict(syn.VIA_A, name="Another display name", kind="road")
    assert syn.key(via=(renamed, syn.VIA_B)) == syn.key()
    content = request_key_content(
        trip_type="round_trip", origin=syn.ORIGIN, destination=syn.DEST, via=[syn.VIA_A, syn.ROAD],
        routing_params=syn.ROUTING_PARAMS, definitions=syn.DEFINITIONS,
    )
    text = canonical_json(content)
    for definition in syn.DEFINITIONS.values():
        assert f"{definition['lat']:.6f}" not in text and f"{definition['lon']:.6f}" not in text
    assert content["via"][1]["entry_fingerprint"] == place_fingerprint(syn.DEFINITIONS["SYN-ROAD-ENTRY"])
    assert content["origin"]["fingerprint"] == sha256_hex(syn.DEFINITIONS["SYN-ORIGIN"])[:16]


def test_fingerprint_normalizes_coordinates_to_six_decimals():
    assert place_fingerprint({"lat": 0.1234561, "lon": 0.2}) == place_fingerprint({"lat": 0.1234569, "lon": 0.2})
    assert place_fingerprint({"lat": 0.123456, "lon": 0.2}) != place_fingerprint({"lat": 0.123457, "lon": 0.2})
    assert len(place_fingerprint({"lat": 0.1, "lon": 0.2})) == 16


@pytest.mark.parametrize("kwargs", [
    {"trip_type": None},
    {"trip_type": "loop"},
    {"origin": None},
    {"origin": {"ref_id": ""}},
    {"destination": {"name": "no ref_id"}},
    {"via": "SYN-VIA-A"},
    {"via": [{"ref_id": "SYN-VIA-A", "entry_ref_id": ""}]},
    {"via": [{"ref_id": "SYN-MISSING"}]},
    {"via": [{"ref_id": "SYN-VIA-A", "entry_ref_id": "SYN-MISSING"}]},
    {"routing_params": None},
    {"routing_params": {"x": float("nan")}},
    {"definitions": None},
    {"definitions": {**syn.DEFINITIONS, "SYN-VIA-A": "not an object"}},
])
def test_request_key_rejects_incomplete_requests(kwargs):
    args = {"trip_type": "round_trip", "origin": syn.ORIGIN, "destination": syn.DEST, "via": [syn.VIA_A],
            "routing_params": syn.ROUTING_PARAMS, "definitions": syn.DEFINITIONS}
    args.update(kwargs)
    from moto_copilot.routing import request_key
    with pytest.raises(RequestKeyError) as exc:
        request_key(**args)
    assert "0.10" not in str(exc.value)  # no coordinates in the message
