"""JSON Schemas for the minimal data contracts v0.2 (DESIGN.md §5).

One schema per record type. Rules that span several records (invariants) are in validate.py.
"""
from __future__ import annotations

CONTRACT_VERSION = "0.2"

CATEGORIES = ["C1", "C2", "C3"]

# ISO 8601 with an explicit +08:00 offset (Asia/Taipei). A time without an offset is invalid.
_DATETIME = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?\+08:00$"}
_TRIP_ID = {"type": "string", "pattern": r"^T\d{3}$"}
_ROUTE_ID = {"type": "string", "pattern": r"^R\d{2}$"}
_CHECKPOINT_ID = {"type": "string", "pattern": r"^R\d{2}-CP\d{2}$"}
_NAME = {"type": "string", "minLength": 1}
_POSITIVE = {"type": "number", "exclusiveMinimum": 0}
_NON_NEGATIVE = {"type": "number", "minimum": 0}
_CATEGORY = {"enum": CATEGORIES}


def _nullable(schema: dict) -> dict:
    return {"anyOf": [schema, {"type": "null"}]}


def _record(properties: dict, optional: tuple[str, ...] = ()) -> dict:
    """Every listed field must be present (nullable ones may hold null); no other field is allowed."""
    return {
        "type": "object",
        "properties": properties,
        "required": [k for k in properties if k not in optional],
        "additionalProperties": False,
    }


# --- Contract 1: Derived Segment Table -------------------------------------
_DERIVED_PUBLIC = {
    "trip_id": _TRIP_ID,
    "seg_index": {"type": "integer", "minimum": 0},
    "trip_role": {"enum": ["pace", "holdout"]},
    "route_id": _nullable(_ROUTE_ID),
    "length_m": _POSITIVE,
    "moving_time_s": _nullable(_POSITIVE),  # a number must be > 0; null when no valid moving time
    "stopped_time_s": _NON_NEGATIVE,
    "curvature_deg_per_km": _nullable(_NON_NEGATIVE),
    "seg_category": _nullable(_CATEGORY),
    "quality": {"enum": ["ok", "suspect", "invalid"]},
    "category_scheme": _NAME,
    "ingest_version": _NAME,
}
# The public version carries no date or time. The private version adds start_time and stays out of git.
DERIVED_SEGMENT_PUBLIC = _record(_DERIVED_PUBLIC)
DERIVED_SEGMENT_PRIVATE = _record({**_DERIVED_PUBLIC, "start_time": _DATETIME})

# --- Contract 2: Route Catalog ---------------------------------------------
ROUTE = _record({
    "route_id": _ROUTE_ID,
    "name": _NAME,
    "n_segments": {"type": "integer", "minimum": 1},
    "total_length_m": _POSITIVE,
    "source_trip_id": _TRIP_ID,
    "category_scheme": _NAME,
    "catalog_version": _NAME,
})
ROUTE_SEGMENT = _record({
    "route_id": _ROUTE_ID,
    "seg_index": {"type": "integer", "minimum": 0},
    "length_m": _POSITIVE,
    "cum_length_m": _POSITIVE,
    "seg_category": _CATEGORY,  # null is not allowed in the catalog
    "end_lat": {"type": "number", "minimum": -90, "maximum": 90},
    "end_lon": {"type": "number", "minimum": -180, "maximum": 180},
})
CHECKPOINT = _record({
    "checkpoint_id": _CHECKPOINT_ID,
    "route_id": _ROUTE_ID,
    "kind": {"enum": ["start", "fuel_station", "waypoint", "end"]},
    "after_seg_count": {"type": "integer", "minimum": 0},
    "name": _nullable(_NAME),
    "station_ref": _nullable(_NAME),
})

# --- Contract 3: Pace Table -------------------------------------------------
PACE_HEADER = _record({
    "pace_version": _NAME,
    "method": {"enum": ["median_unweighted"]},  # another method needs a Change Log entry first (DC-10)
    "category_scheme": _NAME,
    "ingest_version": _NAME,
    "min_segments": {"type": "integer", "minimum": 1},
    "n_trips": {"type": "integer", "minimum": 0},
    "trip_ids": {"type": "array", "items": _TRIP_ID, "uniqueItems": True},
    "built_at": _DATETIME,
})
PACE_CATEGORY = _record({
    "pace_version": _NAME,
    "seg_category": _CATEGORY,
    "speed_kmh": _nullable(_POSITIVE),
    "n_segments": {"type": "integer", "minimum": 0},
})

# --- Contract 4: ETA Output -------------------------------------------------
_BREAK = _record({"after_checkpoint_id": _CHECKPOINT_ID, "duration_s": _POSITIVE})
ETA_HEADER = _record({
    "plan_id": _NAME,
    "route_id": _ROUTE_ID,
    "departure_time": _DATETIME,
    "status": {"enum": ["ok", "unknown"]},
    "unknown_reason": _nullable(_NAME),
    "margin_coeff": _NON_NEGATIVE,
    "breaks": {"type": "array", "items": _BREAK},
    "pace_version": _NAME,
    "catalog_version": _NAME,
    "computed_at": _DATETIME,
})
ETA_SEGMENT = _record({
    "plan_id": _NAME,
    "seg_index": {"type": "integer", "minimum": 0},
    "typ_seg_time_s": _nullable(_POSITIVE),
    "break_time_s": _NON_NEGATIVE,
    "eta_typ": _nullable(_DATETIME),
    "eta_safe": _nullable(_DATETIME),
})
