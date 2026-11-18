"""Canonical JSON and SHA-256 shared by `snapshot_id` and `request_key` (SPEC-001 §2).

The rule (SPEC-001 §2, row "雜湊與正規化"): UTF-8 JSON, keys in dictionary order, no extra
whitespace; latitude and longitude to six decimal places; lengths and offsets in metres to one
decimal place; every other float to six decimal places.

How the rule is applied here:
- A float is a value in metres when its own key, or the key of an enclosing object or list, ends
  in `_m` (SPEC-001 §2 naming: the `_m` suffix means metres). Examples: `via_offset_m[0]`,
  `endpoint_offset_m.start`. Every other float, latitude and longitude included, gets six places.
- The decimal places are cut from the shortest decimal form of the float (`repr`), without
  rounding up (`ROUND_DOWN`). See `_ROUNDING`.
- Floats are written in fixed-point form with exactly that many places (`12.0`, `23.123456`);
  integers stay integers; `-0.0` is written as `0.0`. NaN and infinities are rejected.
- Only JSON types are accepted: dict with str keys, list, str, int, float, bool, None.
"""
from __future__ import annotations

import decimal
import hashlib
import json
import math
from decimal import Decimal

METRE_PLACES = 1
DEFAULT_PLACES = 6

# SPEC-001 §2 says "取小數六位" / "取小數一位" without naming a rounding mode. Cutting the extra
# digits (ROUND_DOWN on the shortest decimal form) is the reading under which S56 holds for
# every pair of values: two values that differ in the sixth decimal always hash differently,
# and two that differ only from the seventh decimal on always hash the same. Rounding to nearest
# breaks both halves near a rounding boundary (e.g. 23.1234561 and 23.1234569). This choice is
# reported for Design Authority confirmation (worklog issue-14, C-14-1).
_ROUNDING = decimal.ROUND_DOWN

# Enough precision to quantize any finite float (up to about 1.8e308) to six places.
_CONTEXT = decimal.Context(prec=400)


class CanonicalError(ValueError):
    """The value cannot be written as canonical JSON. Messages never include the value."""


def _format_float(value: float, places: int, path: str) -> str:
    if not math.isfinite(value):
        raise CanonicalError(f"{path}: a float must be finite")
    exponent = Decimal(1).scaleb(-places)
    cut = Decimal(repr(value)).quantize(exponent, rounding=_ROUNDING, context=_CONTEXT)
    if cut.is_zero():
        cut = abs(cut)
    return format(cut, "f")


def _encode(value, metres: bool, path: str) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(int(value))
    if isinstance(value, float):
        return _format_float(value, METRE_PLACES if metres else DEFAULT_PLACES, path)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ",".join(_encode(item, metres, f"{path}[{i}]") for i, item in enumerate(value)) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise CanonicalError(f"{path}: object keys must be strings")
        parts = []
        for key in sorted(value):
            child_metres = metres or key.endswith("_m")
            parts.append(json.dumps(key, ensure_ascii=False) + ":" + _encode(value[key], child_metres, f"{path}.{key}"))
        return "{" + ",".join(parts) + "}"
    raise CanonicalError(f"{path}: {type(value).__name__} is not a JSON type")


def canonical_json(value) -> str:
    """The canonical JSON text of `value` (SPEC-001 §2)."""
    return _encode(value, False, "$")


def canonical_bytes(value) -> bytes:
    """The canonical JSON of `value` as UTF-8 bytes."""
    try:
        return canonical_json(value).encode("utf-8")
    except UnicodeEncodeError as exc:
        raise CanonicalError("$: a string is not valid Unicode") from exc


def sha256_hex(value) -> str:
    """SHA-256 (lowercase hex) of the canonical JSON of `value`."""
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def normalized(value):
    """`value` as it reads back from its canonical JSON (floats cut to their places)."""
    return json.loads(canonical_json(value))
