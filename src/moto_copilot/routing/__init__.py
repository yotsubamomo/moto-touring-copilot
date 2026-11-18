"""Route snapshots for routing-engine routes (SPEC-R1 R1-2; SPEC-001 §2, 4.14, 7.11 items 1, 3, 4).

This package holds the snapshot model, the canonical hashing, write-once storage and selection.
Calling the routing engine, the freeway check and the offsets are not here (R1-4).
"""
from .canonical import CanonicalError, canonical_bytes, canonical_json, sha256_hex
from .request_key import RequestKeyError, place_fingerprint, request_key, request_key_content
from .snapshot import (
    SnapshotValidationError,
    acquired_at,
    build_snapshot,
    compute_snapshot_id,
    hash_scope,
    route_id_for,
    validate_snapshot,
)
from .store import (
    REUSE_WINDOW,
    SNAPSHOT_MISSING,
    FrozenEntry,
    PutResult,
    SnapshotConflictError,
    SnapshotIntegrityError,
    SnapshotModeResult,
    SnapshotNotFoundError,
    SnapshotStore,
    SnapshotStoreError,
    StrictModeStop,
    find_reusable,
    is_compatible,
    select_snapshot_mode,
    select_strict,
)

__all__ = [
    "CanonicalError",
    "FrozenEntry",
    "PutResult",
    "REUSE_WINDOW",
    "RequestKeyError",
    "SNAPSHOT_MISSING",
    "SnapshotConflictError",
    "SnapshotIntegrityError",
    "SnapshotModeResult",
    "SnapshotNotFoundError",
    "SnapshotStore",
    "SnapshotStoreError",
    "SnapshotValidationError",
    "StrictModeStop",
    "acquired_at",
    "build_snapshot",
    "canonical_bytes",
    "canonical_json",
    "compute_snapshot_id",
    "find_reusable",
    "hash_scope",
    "is_compatible",
    "place_fingerprint",
    "request_key",
    "request_key_content",
    "route_id_for",
    "select_snapshot_mode",
    "select_strict",
    "sha256_hex",
    "validate_snapshot",
]
