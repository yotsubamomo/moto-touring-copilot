"""`request_key`: the key that matches a route request to stored snapshots (SPEC-001 7.11 item 4).

`request_key` is the SHA-256 of the canonical JSON (canonical.py) of `trip_type`, `origin`,
`destination`, `via` (in order, with `entry_ref_id`) and `routing_params`. Each place is its code
plus a fingerprint: the first 16 hex characters of the SHA-256 of the canonical JSON of that
code's coordinate definition (CL-R1-2). The caller gives the coordinate definitions; what a
definition contains is defined elsewhere (gazetteer Spec). The key holds no coordinates.

Only the codes the request refers to are looked up, so a change to a definition that the request
does not use leaves the key unchanged (S72). Nothing here opens a network connection.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

from ..contracts.schemas import TRIP_TYPES
from .canonical import CanonicalError, sha256_hex

FINGERPRINT_LENGTH = 16


class RequestKeyError(ValueError):
    """The request cannot be turned into a `request_key`. Messages never include coordinates."""


def place_fingerprint(definition: Mapping) -> str:
    """First 16 hex characters of the SHA-256 of a coordinate definition's canonical JSON."""
    if not isinstance(definition, Mapping):
        raise RequestKeyError("a coordinate definition must be an object")
    try:
        return sha256_hex(dict(definition))[:FINGERPRINT_LENGTH]
    except CanonicalError as exc:
        raise RequestKeyError(f"a coordinate definition cannot be written as canonical JSON ({exc})") from exc


def _fingerprint_of(code: str, definitions: Mapping, role: str) -> str:
    if code not in definitions:
        raise RequestKeyError(f"{role}: no coordinate definition was given for code {code!r}")
    return place_fingerprint(definitions[code])


def _place(place, definitions: Mapping, role: str) -> dict:
    if not isinstance(place, Mapping):
        raise RequestKeyError(f"{role}: a place must be an object with ref_id")
    ref_id = place.get("ref_id")
    if not isinstance(ref_id, str) or ref_id == "":
        raise RequestKeyError(f"{role}: ref_id must be a non-empty string")
    entry = place.get("entry_ref_id")
    if entry is not None and (not isinstance(entry, str) or entry == ""):
        raise RequestKeyError(f"{role}: entry_ref_id must be null or a non-empty string")
    return {
        "ref_id": ref_id,
        "fingerprint": _fingerprint_of(ref_id, definitions, role),
        "entry_ref_id": entry,
        "entry_fingerprint": None if entry is None else _fingerprint_of(entry, definitions, f"{role}.entry_ref_id"),
    }


def request_key_content(
    *,
    trip_type: str,
    origin: Mapping,
    destination: Mapping,
    via: Sequence[Mapping],
    routing_params: Mapping,
    definitions: Mapping[str, Mapping],
) -> dict:
    """The object whose canonical JSON is hashed into `request_key`.

    Each place keeps only `ref_id` and `entry_ref_id` (other PlaceRef fields such as `name` are
    not part of the key) and gets the fingerprints of the definitions of those codes.
    """
    if trip_type not in TRIP_TYPES:
        raise RequestKeyError(f"trip_type must be one of {', '.join(TRIP_TYPES)}")
    if not isinstance(definitions, Mapping):
        raise RequestKeyError("definitions must map codes to coordinate definitions")
    if isinstance(via, (str, bytes)) or not isinstance(via, Sequence):
        raise RequestKeyError("via must be a list of places (it may be empty)")
    if not isinstance(routing_params, Mapping):
        raise RequestKeyError("routing_params must be an object")
    return {
        "trip_type": trip_type,
        "origin": _place(origin, definitions, "origin"),
        "destination": _place(destination, definitions, "destination"),
        "via": [_place(p, definitions, f"via[{i}]") for i, p in enumerate(via)],
        "routing_params": dict(routing_params),
    }


def request_key(
    *,
    trip_type: str,
    origin: Mapping,
    destination: Mapping,
    via: Sequence[Mapping],
    routing_params: Mapping,
    definitions: Mapping[str, Mapping],
) -> str:
    """`request_key` (64 lowercase hex characters) of a route request (7.11 item 4; CL-R1-2)."""
    content = request_key_content(
        trip_type=trip_type, origin=origin, destination=destination, via=via,
        routing_params=routing_params, definitions=definitions,
    )
    try:
        return sha256_hex(content)
    except CanonicalError as exc:
        raise RequestKeyError(f"routing_params cannot be written as canonical JSON ({exc})") from exc
