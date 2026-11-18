"""RouteSnapshot and RouteLeg (SPEC-001 4.14): structure check, `snapshot_id` and the `RS-` route_id.

A route snapshot holds the polyline of every direction, so it never goes into a plan result or
to a language model (SPEC-001 §2, 4.14). Nothing here opens a network connection or writes a
file; storage is in store.py.

`snapshot_id` is `SN-` plus the first 10 hex characters of the SHA-256 of the canonical JSON
(canonical.py) of the snapshot without `snapshot_id` and without each leg's `fetched_at`
(SPEC-001 §2; 7.11 item 1). The `RS-` route_id uses the same 10 characters.

Error messages name the field and the rule, never the value (a request may hold positions).
"""
from __future__ import annotations

import copy
import re
from datetime import date, datetime, timedelta, timezone

from ..contracts.schemas import ROUTE_ID_PATTERN, SNAPSHOT_ID_PATTERN, TRIP_TYPES
from .canonical import CanonicalError, normalized, sha256_hex

TAIPEI = timezone(timedelta(hours=8))

DIRECTIONS = ("outbound", "return")
FREEWAY_CHECK_VALUES = ("pass", "fail")
# SPEC-001 4.14: one_way has one leg (outbound); round_trip has two, outbound then return.
LEG_DIRECTIONS = {"one_way": ("outbound",), "round_trip": ("outbound", "return")}
# SPEC-001 4.14 / 7.11 item 8: every stored offset is at most 200 m.
OFFSET_LIMIT_M = 200.0

SNAPSHOT_FIELDS = (
    "snapshot_id", "request_key", "trip_type", "routing_params",
    "engine_name", "engine_version", "map_data_date", "legs",
)
LEG_FIELDS = (
    "direction", "request", "shape", "distance_m", "engine_time_s", "road_names", "warnings",
    "has_highway", "freeway_check", "freeway_check_method", "endpoint_offset_m",
    "via_offset_m", "fetched_at",
)
WARNING_FIELDS = ("code", "text")
ENDPOINT_OFFSET_FIELDS = ("start", "end")

# The snapshot has no elevation (SPEC-001 4.14, Q-3 item 7). Besides the closed field sets above,
# no object anywhere in the snapshot (request and routing_params included) may carry a key that
# names elevation.
_ELEVATION_KEY = re.compile(r"elevation|altitude|height|^ele$", re.IGNORECASE)

# ASCII-only, whole-string patterns (CL-R1-13): fullmatch never accepts a final newline.
_HEX64 = re.compile(r"[0-9a-f]{64}")
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
# SPEC-001 §2: ISO 8601 with the +08:00 offset; a time without an offset is invalid.
_DATETIME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?\+08:00")


class SnapshotValidationError(ValueError):
    """A snapshot does not satisfy SPEC-001 4.14. `errors` lists every problem found."""

    def __init__(self, errors: list[str]):
        super().__init__("route snapshot is invalid: " + "; ".join(errors))
        self.errors = list(errors)


def is_snapshot_id(value) -> bool:
    return isinstance(value, str) and re.search(SNAPSHOT_ID_PATTERN, value) is not None


def is_request_key(value) -> bool:
    """`request_key` is the SHA-256 (64 lowercase hex characters) of the canonical request."""
    return isinstance(value, str) and _HEX64.fullmatch(value) is not None


def parse_datetime(value) -> datetime | None:
    """A SPEC-001 §2 datetime as an aware datetime, or None when the string is not one."""
    if not isinstance(value, str) or _DATETIME.fullmatch(value) is None:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def hash_scope(snapshot: dict) -> dict:
    """The part of a snapshot that `snapshot_id` hashes: all but `snapshot_id` and legs[].fetched_at."""
    scope = {key: copy.deepcopy(value) for key, value in snapshot.items() if key != "snapshot_id"}
    legs = scope.get("legs")
    if isinstance(legs, list):
        scope["legs"] = [
            {k: v for k, v in leg.items() if k != "fetched_at"} if isinstance(leg, dict) else leg
            for leg in legs
        ]
    return scope


def compute_snapshot_id(snapshot: dict) -> str:
    """`SN-` plus the first 10 hex characters of the SHA-256 of the hash scope."""
    return "SN-" + sha256_hex(hash_scope(snapshot))[:10]


def route_id_for(snapshot_id: str) -> str:
    """The `RS-` route_id of a routing-engine route: the same 10 hex characters as its snapshot."""
    if not is_snapshot_id(snapshot_id):
        raise ValueError("snapshot_id does not match ^SN-[0-9a-f]{10}$")
    route_id = "RS-" + snapshot_id[3:]
    assert re.search(ROUTE_ID_PATTERN, route_id)
    return route_id


def acquired_at(snapshot: dict) -> datetime:
    """The acquisition time of a snapshot: the latest `fetched_at` of its legs (CL-R1-3)."""
    times = [parse_datetime(leg.get("fetched_at")) for leg in snapshot["legs"]]
    if not times or any(t is None for t in times):
        raise ValueError("every leg needs a valid fetched_at")
    return max(times)


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_float(value) -> bool:
    return isinstance(value, float)


def _non_empty_str(value) -> bool:
    return isinstance(value, str) and value != ""


def _check_keys(obj: dict, fields: tuple[str, ...], path: str, errors: list[str]) -> None:
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing field {field}")
    for key in obj:
        if key not in fields:
            errors.append(f"{path}: unknown field {key!r}" if isinstance(key, str) else f"{path}: non-string key")


def _check_no_elevation(value, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(key, str) and _ELEVATION_KEY.search(key):
                errors.append(f"{path}.{key}: the snapshot has no elevation fields")
            _check_no_elevation(child, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _check_no_elevation(child, f"{path}[{i}]", errors)


def _check_offset(value, path: str, errors: list[str]) -> None:
    if not _is_float(value):
        errors.append(f"{path}: must be a float")
    elif not (0.0 <= value <= OFFSET_LIMIT_M):
        errors.append(f"{path}: must be between 0 and {OFFSET_LIMIT_M:g} m")


def _check_leg(leg, path: str, errors: list[str]) -> None:
    if not isinstance(leg, dict):
        errors.append(f"{path}: must be an object")
        return
    _check_keys(leg, LEG_FIELDS, path, errors)
    if "direction" in leg and leg["direction"] not in DIRECTIONS:
        errors.append(f"{path}.direction: must be one of {', '.join(DIRECTIONS)}")
    if "request" in leg and not isinstance(leg["request"], dict):
        errors.append(f"{path}.request: must be an object")
    if "shape" in leg and not _non_empty_str(leg["shape"]):
        errors.append(f"{path}.shape: must be a non-empty string")
    for field in ("distance_m", "engine_time_s"):
        if field in leg and not (_is_int(leg[field]) and leg[field] >= 0):
            errors.append(f"{path}.{field}: must be a non-negative integer")
    if "road_names" in leg:
        names = leg["road_names"]
        if not isinstance(names, list) or not all(_non_empty_str(n) for n in names):
            errors.append(f"{path}.road_names: must be a list of non-empty strings")
    if "warnings" in leg:
        warnings = leg["warnings"]
        if not isinstance(warnings, list):
            errors.append(f"{path}.warnings: must be a list")
        else:
            for i, warning in enumerate(warnings):
                wpath = f"{path}.warnings[{i}]"
                if not isinstance(warning, dict):
                    errors.append(f"{wpath}: must be an object")
                    continue
                _check_keys(warning, WARNING_FIELDS, wpath, errors)
                if "code" in warning and not _is_int(warning["code"]):
                    errors.append(f"{wpath}.code: must be an integer")
                if "text" in warning and not isinstance(warning["text"], str):
                    errors.append(f"{wpath}.text: must be a string")
            # 7.11 items 6 and 7: a response with any warning is not adopted, so not stored.
            if warnings:
                errors.append(f"{path}.warnings: a stored direction has no warnings")
    if "has_highway" in leg:
        if not isinstance(leg["has_highway"], bool):
            errors.append(f"{path}.has_highway: must be a boolean")
        elif leg["has_highway"]:
            # 4.14: a stored direction always has has_highway = false.
            errors.append(f"{path}.has_highway: a stored direction has has_highway = false")
    if "freeway_check" in leg:
        if leg["freeway_check"] not in FREEWAY_CHECK_VALUES:
            errors.append(f"{path}.freeway_check: must be one of {', '.join(FREEWAY_CHECK_VALUES)}")
        elif leg["freeway_check"] != "pass":
            # 4.14: every direction of a stored snapshot is pass.
            errors.append(f"{path}.freeway_check: a stored direction is pass")
    if "freeway_check_method" in leg and not _non_empty_str(leg["freeway_check_method"]):
        errors.append(f"{path}.freeway_check_method: must be a non-empty string")
    if "endpoint_offset_m" in leg:
        offsets = leg["endpoint_offset_m"]
        if not isinstance(offsets, dict):
            errors.append(f"{path}.endpoint_offset_m: must be an object")
        else:
            _check_keys(offsets, ENDPOINT_OFFSET_FIELDS, f"{path}.endpoint_offset_m", errors)
            for field in ENDPOINT_OFFSET_FIELDS:
                if field in offsets:
                    _check_offset(offsets[field], f"{path}.endpoint_offset_m.{field}", errors)
    if "via_offset_m" in leg:
        vias = leg["via_offset_m"]
        if not isinstance(vias, list):
            errors.append(f"{path}.via_offset_m: must be a list")
        else:
            for i, value in enumerate(vias):
                _check_offset(value, f"{path}.via_offset_m[{i}]", errors)
    if "fetched_at" in leg and parse_datetime(leg["fetched_at"]) is None:
        errors.append(f"{path}.fetched_at: must be an ISO 8601 datetime with +08:00")


def validate_snapshot(snapshot) -> list[str]:
    """Problems with a stored route snapshot (SPEC-001 4.14). An empty list means valid."""
    if not isinstance(snapshot, dict):
        return ["$: a route snapshot must be an object"]
    errors: list[str] = []
    _check_keys(snapshot, SNAPSHOT_FIELDS, "$", errors)
    if "snapshot_id" in snapshot and not is_snapshot_id(snapshot["snapshot_id"]):
        errors.append("$.snapshot_id: must match ^SN-[0-9a-f]{10}$")
    if "request_key" in snapshot and not is_request_key(snapshot["request_key"]):
        errors.append("$.request_key: must be 64 lowercase hex characters")
    trip_type = snapshot.get("trip_type")
    if "trip_type" in snapshot and trip_type not in TRIP_TYPES:
        errors.append(f"$.trip_type: must be one of {', '.join(TRIP_TYPES)}")
    if "routing_params" in snapshot and not isinstance(snapshot["routing_params"], dict):
        errors.append("$.routing_params: must be an object")
    for field in ("engine_name", "engine_version"):
        if field in snapshot and not _non_empty_str(snapshot[field]):
            errors.append(f"$.{field}: must be a non-empty string")
    if "map_data_date" in snapshot:
        value = snapshot["map_data_date"]
        if value is not None:
            ok = isinstance(value, str) and _DATE.fullmatch(value) is not None
            if ok:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    ok = False
            if not ok:
                errors.append("$.map_data_date: must be null or a YYYY-MM-DD date")
    if "legs" in snapshot:
        legs = snapshot["legs"]
        if not isinstance(legs, list):
            errors.append("$.legs: must be a list")
        else:
            for i, leg in enumerate(legs):
                _check_leg(leg, f"$.legs[{i}]", errors)
            if trip_type in LEG_DIRECTIONS:
                expected = LEG_DIRECTIONS[trip_type]
                actual = tuple(leg.get("direction") if isinstance(leg, dict) else None for leg in legs)
                if actual != expected:
                    errors.append(f"$.legs: {trip_type} needs the directions {', '.join(expected)} in this order")
    _check_no_elevation(snapshot, "$", errors)
    try:
        computed = compute_snapshot_id(snapshot)
    except CanonicalError as exc:
        errors.append(f"cannot be written as canonical JSON ({exc})")
    else:
        if is_snapshot_id(snapshot.get("snapshot_id")) and snapshot["snapshot_id"] != computed:
            errors.append("$.snapshot_id: does not match the hash of the snapshot content")
    return errors


def _as_float_offsets(leg: dict) -> None:
    offsets = leg.get("endpoint_offset_m")
    if isinstance(offsets, dict):
        for field, value in offsets.items():
            if _is_int(value):
                offsets[field] = float(value)
    vias = leg.get("via_offset_m")
    if isinstance(vias, list):
        leg["via_offset_m"] = [float(v) if _is_int(v) else v for v in vias]


def build_snapshot(
    *,
    request_key: str,
    trip_type: str,
    routing_params: dict,
    engine_name: str,
    engine_version: str,
    map_data_date: str | None,
    legs: list[dict],
) -> dict:
    """Assemble a route snapshot, give it its `snapshot_id` and return it in normalized form.

    The arguments are copied, not changed. Integer offsets are taken as floats (4.14 types them
    float). The result is what the canonical file reads back as, so the in-memory snapshot, the
    stored file and the hash all use the same values. Raises SnapshotValidationError.
    """
    snapshot = {
        "request_key": request_key,
        "trip_type": trip_type,
        "routing_params": copy.deepcopy(routing_params),
        "engine_name": engine_name,
        "engine_version": engine_version,
        "map_data_date": map_data_date,
        "legs": copy.deepcopy(legs),
    }
    if isinstance(snapshot["legs"], list):
        for leg in snapshot["legs"]:
            if isinstance(leg, dict):
                _as_float_offsets(leg)
    try:
        snapshot["snapshot_id"] = compute_snapshot_id(snapshot)
    except CanonicalError as exc:
        raise SnapshotValidationError([f"cannot be written as canonical JSON ({exc})"]) from exc
    errors = validate_snapshot(snapshot)
    if errors:
        raise SnapshotValidationError(errors)
    result = normalized(snapshot)
    errors = validate_snapshot(result)
    if errors:
        raise SnapshotValidationError(errors)
    return result
