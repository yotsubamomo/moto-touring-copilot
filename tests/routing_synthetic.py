"""Synthetic inputs for the routing tests (Issue #14). Nothing here comes from ride data.

- Coordinates are invented values next to 0 deg N, 0 deg E (open ocean), not places anyone rides.
- Shapes are placeholder strings, not polylines returned by any engine.
- Codes (`SYN-...`), road names, the engine name and the check method are invented.
"""
from __future__ import annotations

import copy

from moto_copilot.routing import build_snapshot, request_key

METHOD = "synthetic-freeway-check-v1"
OTHER_METHOD = "synthetic-freeway-check-v2"
ROUTING_PARAMS = {"costing": "motorcycle", "costing_options": {"motorcycle": {"use_highways": 0}}}

DEFINITIONS = {
    "SYN-ORIGIN": {"lat": 0.101101, "lon": 0.202202},
    "SYN-DEST": {"lat": 0.111111, "lon": 0.222222},
    "SYN-VIA-A": {"lat": 0.105105, "lon": 0.205205},
    "SYN-VIA-B": {"lat": 0.107107, "lon": 0.207207},
    "SYN-ROAD": {"lat": 0.108108, "lon": 0.208208},
    "SYN-ROAD-ENTRY": {"lat": 0.109109, "lon": 0.209209},
    "SYN-UNUSED": {"lat": 0.199999, "lon": 0.299999},
}

ORIGIN = {"kind": "landmark", "ref_id": "SYN-ORIGIN", "name": "Synthetic origin", "entry_ref_id": None}
DEST = {"kind": "landmark", "ref_id": "SYN-DEST", "name": "Synthetic destination", "entry_ref_id": None}
VIA_A = {"kind": "landmark", "ref_id": "SYN-VIA-A", "name": "Synthetic via A", "entry_ref_id": None}
VIA_B = {"kind": "landmark", "ref_id": "SYN-VIA-B", "name": "Synthetic via B", "entry_ref_id": None}
ROAD = {"kind": "road", "ref_id": "SYN-ROAD", "name": "Synthetic road", "entry_ref_id": "SYN-ROAD-ENTRY"}


def key(trip_type="round_trip", via=(VIA_A, VIA_B), definitions=None, routing_params=None, origin=ORIGIN, destination=DEST):
    return request_key(
        trip_type=trip_type,
        origin=origin,
        destination=destination,
        via=list(via),
        routing_params=ROUTING_PARAMS if routing_params is None else routing_params,
        definitions=DEFINITIONS if definitions is None else definitions,
    )


def leg(direction="outbound", *, shape=None, fetched_at="2026-11-18T09:00:00+08:00", method=METHOD, **overrides):
    stops = ["SYN-ORIGIN", "SYN-VIA-A", "SYN-DEST"] if direction == "outbound" else ["SYN-DEST", "SYN-VIA-A", "SYN-ORIGIN"]
    value = {
        "direction": direction,
        "request": {
            "locations": [
                {"ref_id": code, "lat": DEFINITIONS[code]["lat"], "lon": DEFINITIONS[code]["lon"]} for code in stops
            ],
            "routing_params": copy.deepcopy(ROUTING_PARAMS),
        },
        "shape": shape if shape is not None else f"synthetic-shape-{direction}-1",
        "distance_m": 12345 if direction == "outbound" else 12401,
        "engine_time_s": 1500 if direction == "outbound" else 1510,
        "road_names": ["Synthetic Road 1", "Synthetic Road 2"],
        "warnings": [],
        "has_highway": False,
        "freeway_check": "pass",
        "freeway_check_method": method,
        "endpoint_offset_m": {"start": 12.3, "end": 45.6},
        "via_offset_m": [7.8],
        "fetched_at": fetched_at,
    }
    value.update(overrides)
    return value


def snapshot(trip_type="one_way", *, legs=None, rkey=None, fetched_at="2026-11-18T09:00:00+08:00", method=METHOD,
             shape_suffix="1", **overrides):
    if legs is None:
        directions = ["outbound"] if trip_type == "one_way" else ["outbound", "return"]
        legs = [leg(d, shape=f"synthetic-shape-{d}-{shape_suffix}", fetched_at=fetched_at, method=method) for d in directions]
    args = {
        "request_key": rkey if rkey is not None else key(trip_type),
        "trip_type": trip_type,
        "routing_params": ROUTING_PARAMS,
        "engine_name": "synthetic-engine",
        "engine_version": "0.0-synthetic",
        "map_data_date": "2026-11-01",
        "legs": legs,
    }
    args.update(overrides)
    return build_snapshot(**args)
