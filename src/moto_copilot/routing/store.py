"""Write-once storage of route snapshots and the selection rules (SPEC-001 7.11 items 1 and 3).

Storage (CL-R1-3): one file per `snapshot_id`, `<snapshot_id>.json`, in a directory the caller
gives. There is no default location: a snapshot that starts at the rider's start anchor must not
land in a tracked path. A file holds the canonical JSON (canonical.py) of the whole snapshot,
`snapshot_id` and `fetched_at` included; its bytes are what a frozen list's SHA-256 records.
Files are created once and never modified or deleted; there is no index file.

Selection (7.11 item 3, CL-R1-4):
- `find_reusable`: normal mode. Same `request_key`, every leg's `freeway_check_method` equal to
  the current method, acquired within 30 x 24 hours of "now"; the latest one, else None (the
  caller then asks the engine).
- `select_snapshot_mode`: plain Snapshot Mode. Same `request_key` and method, no age limit; the
  latest one, else the route error `snapshot_missing`.
- `select_strict`: strict mode (a frozen list was given). Only the listed snapshot, with the file
  SHA-256 checked; any problem raises `StrictModeStop` and nothing falls back to another snapshot.

The acquisition time of a snapshot is the latest `fetched_at` of its legs; a reused file keeps
its own times (they are never updated or rewritten). Nothing here opens a network connection.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from .canonical import canonical_bytes
from .snapshot import (
    TAIPEI,
    SnapshotValidationError,
    acquired_at,
    hash_scope,
    is_request_key,
    is_snapshot_id,
    route_id_for,
    validate_snapshot,
)

SNAPSHOT_MISSING = "snapshot_missing"
REUSE_WINDOW = timedelta(days=30)  # 30 x 24 hours (SPEC-001 5.4; CL-R1-3)

_FILE_NAME = re.compile(r"SN-[0-9a-f]{10}\.json")
_HEX64 = re.compile(r"[0-9a-f]{64}")


class SnapshotStoreError(Exception):
    """A problem with the snapshot directory or one of its files."""


class SnapshotConflictError(SnapshotStoreError):
    """A different content was written under an existing `snapshot_id` (7.11 item 1). Nothing was written."""


class SnapshotIntegrityError(SnapshotStoreError):
    """A snapshot file cannot be read, is not a valid snapshot, or does not match its name."""


class SnapshotNotFoundError(SnapshotStoreError):
    """No file exists for the `snapshot_id`."""


class StrictModeStop(Exception):
    """Strict mode stops (SPEC-001 7.11 item 3; CL-R1-4). Not a route error; there is no fallback.

    `reason` is one of: invalid_entry, no_entry, ambiguous_entry, file_missing, hash_mismatch,
    invalid_snapshot, request_key_mismatch, method_mismatch.
    """

    def __init__(self, reason: str, message: str):
        super().__init__(f"strict mode stopped ({reason}): {message}")
        self.reason = reason


@dataclass(frozen=True)
class PutResult:
    snapshot_id: str
    route_id: str
    path: Path
    created: bool  # False: the same content was already stored; the existing file was used
    snapshot: dict  # the stored snapshot (the existing one, with its own fetched_at, when reused)


@dataclass(frozen=True)
class SnapshotModeResult:
    snapshot: dict | None
    route_error: str | None  # SNAPSHOT_MISSING when no compatible snapshot exists


@dataclass(frozen=True)
class FrozenEntry:
    """One frozen-list item, passed as data (CL-R1-4; the list's file format is not defined here)."""

    request_key: str
    snapshot_id: str
    sha256: str

    @classmethod
    def from_mapping(cls, item: Mapping) -> "FrozenEntry":
        return cls(item.get("request_key"), item.get("snapshot_id"), item.get("sha256"))

    def is_well_formed(self) -> bool:
        return (
            is_request_key(self.request_key)
            and is_snapshot_id(self.snapshot_id)
            and isinstance(self.sha256, str)
            and _HEX64.fullmatch(self.sha256) is not None
        )


def _reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate key")
        obj[key] = value
    return obj


def _reject_constant(_name):
    raise ValueError("NaN and infinities are not JSON")


def _parse_snapshot_bytes(data: bytes, snapshot_id: str) -> dict:
    """Parse and validate the bytes of `<snapshot_id>.json`. Raises SnapshotIntegrityError."""
    try:
        snapshot = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise SnapshotIntegrityError(f"{snapshot_id}: the file is not valid JSON") from exc
    errors = validate_snapshot(snapshot)
    if errors:
        raise SnapshotIntegrityError(f"{snapshot_id}: the file is not a valid snapshot: " + "; ".join(errors))
    if snapshot["snapshot_id"] != snapshot_id:
        raise SnapshotIntegrityError(f"{snapshot_id}: the file holds a different snapshot_id")
    return snapshot


class SnapshotStore:
    """Route snapshots in one caller-given directory. The directory must already exist."""

    def __init__(self, directory: str | os.PathLike):
        path = Path(directory)
        if not path.is_dir():
            raise SnapshotStoreError("the snapshot directory does not exist or is not a directory")
        self.directory = path

    def path_for(self, snapshot_id: str) -> Path:
        if not is_snapshot_id(snapshot_id):
            raise ValueError("snapshot_id does not match ^SN-[0-9a-f]{10}$")
        return self.directory / f"{snapshot_id}.json"

    def put(self, snapshot: dict) -> PutResult:
        """Store a snapshot once (7.11 item 1).

        Same content (everything but `snapshot_id` and `fetched_at`) as an existing file: that file
        is used and nothing is written. Different content under an existing `snapshot_id`:
        SnapshotConflictError, nothing is written. The existing file is never modified.
        """
        errors = validate_snapshot(snapshot)
        if errors:
            raise SnapshotValidationError(errors)
        snapshot_id = snapshot["snapshot_id"]
        path = self.path_for(snapshot_id)
        data = canonical_bytes(snapshot)
        if not path.exists():
            try:
                with open(path, "xb") as handle:  # exclusive create: never replaces a file
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            except FileExistsError:
                pass  # created by someone else in between; compared below
            else:
                stored = _parse_snapshot_bytes(data, snapshot_id)
                return PutResult(snapshot_id, route_id_for(snapshot_id), path, True, stored)
        existing = self.load(snapshot_id)
        if canonical_bytes(hash_scope(existing)) != canonical_bytes(hash_scope(snapshot)):
            raise SnapshotConflictError(f"{snapshot_id}: a different content is already stored under this snapshot_id")
        return PutResult(snapshot_id, route_id_for(snapshot_id), path, False, existing)

    def load(self, snapshot_id: str) -> dict:
        path = self.path_for(snapshot_id)
        try:
            data = path.read_bytes()
        except FileNotFoundError as exc:
            raise SnapshotNotFoundError(f"{snapshot_id}: no snapshot file") from exc
        return _parse_snapshot_bytes(data, snapshot_id)

    def file_sha256(self, snapshot_id: str) -> str:
        """SHA-256 of the file bytes: the value a frozen list records."""
        return hashlib.sha256(self.path_for(snapshot_id).read_bytes()).hexdigest()

    def snapshot_ids(self) -> list[str]:
        """Every `snapshot_id` with a file here. Other files in the directory are ignored."""
        return sorted(
            entry.name[: -len(".json")]
            for entry in self.directory.iterdir()
            if _FILE_NAME.fullmatch(entry.name) and entry.is_file()
        )

    def snapshots(self) -> list[dict]:
        """Every stored snapshot. A file that is not a valid snapshot raises SnapshotIntegrityError."""
        return [self.load(snapshot_id) for snapshot_id in self.snapshot_ids()]


def _check_method(current_method) -> None:
    if not isinstance(current_method, str) or current_method == "":
        raise ValueError("the current freeway_check_method must be a non-empty string")


def _check_request_key(request_key) -> None:
    if not is_request_key(request_key):
        raise ValueError("request_key must be 64 lowercase hex characters")


def is_compatible(snapshot: dict, current_method: str) -> bool:
    """Every leg was checked with the current freeway check method (7.11 item 3)."""
    return all(leg["freeway_check_method"] == current_method for leg in snapshot["legs"])


def _latest(candidates: list[dict]) -> dict | None:
    """The snapshot with the latest acquisition time.

    Ties (equal acquisition times) go to the smallest `snapshot_id`, so the result never depends
    on the directory order (CL-R1-15, decision-20261118-issue14-c141).
    """
    if not candidates:
        return None
    ordered = sorted(candidates, key=lambda s: s["snapshot_id"])
    return max(ordered, key=acquired_at)


def _matching(store: SnapshotStore, request_key: str, current_method: str) -> list[dict]:
    return [
        s for s in store.snapshots()
        if s["request_key"] == request_key and is_compatible(s, current_method)
    ]


def find_reusable(
    store: SnapshotStore,
    request_key: str,
    current_method: str,
    now: datetime | None = None,
) -> dict | None:
    """Normal mode: the latest compatible snapshot acquired within 30 days, else None.

    "Within 30 days" is 0 <= now - acquisition time <= 30 x 24 hours (CL-R1-3, CL-R1-16 in
    decision-20261118-issue14-c141): a snapshot whose acquisition time is later than `now` is not
    reused. `now` defaults to the current time in +08:00 and must be timezone-aware.
    """
    _check_request_key(request_key)
    _check_method(current_method)
    if now is None:
        now = datetime.now(TAIPEI)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    fresh = [
        s for s in _matching(store, request_key, current_method)
        if timedelta(0) <= now - acquired_at(s) <= REUSE_WINDOW
    ]
    return _latest(fresh)


def select_snapshot_mode(store: SnapshotStore, request_key: str, current_method: str) -> SnapshotModeResult:
    """Plain Snapshot Mode: the latest compatible snapshot, no age limit; else `snapshot_missing`."""
    _check_request_key(request_key)
    _check_method(current_method)
    chosen = _latest(_matching(store, request_key, current_method))
    if chosen is None:
        return SnapshotModeResult(None, SNAPSHOT_MISSING)
    return SnapshotModeResult(chosen, None)


def select_strict(
    store: SnapshotStore,
    request_key: str,
    current_method: str,
    frozen_entries: Iterable[FrozenEntry | Mapping],
) -> dict:
    """Strict mode: only the frozen-list snapshot for `request_key`, file SHA-256 checked.

    Raises StrictModeStop when the list has no entry (or conflicting entries) for the key, an
    entry is malformed, the file is missing, its SHA-256 differs, it is not a valid snapshot, it
    holds another request_key, or its freeway check method is not the current one. Other stored
    snapshots are never consulted, even later ones.
    """
    _check_request_key(request_key)
    _check_method(current_method)
    items = list(frozen_entries)
    if not all(isinstance(e, (FrozenEntry, Mapping)) for e in items):
        raise StrictModeStop("invalid_entry", "a frozen-list entry is not an object")
    entries = [e if isinstance(e, FrozenEntry) else FrozenEntry.from_mapping(e) for e in items]
    if not all(e.is_well_formed() for e in entries):
        raise StrictModeStop("invalid_entry", "the frozen list has a malformed entry")
    matches = {e for e in entries if e.request_key == request_key}
    if not matches:
        raise StrictModeStop("no_entry", "the frozen list has no entry for this request")
    if len(matches) > 1:
        raise StrictModeStop("ambiguous_entry", "the frozen list has conflicting entries for this request")
    (entry,) = matches
    path = store.path_for(entry.snapshot_id)
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        raise StrictModeStop("file_missing", f"{entry.snapshot_id}: the listed snapshot file does not exist") from None
    if hashlib.sha256(data).hexdigest() != entry.sha256:
        raise StrictModeStop("hash_mismatch", f"{entry.snapshot_id}: the file SHA-256 differs from the frozen list")
    try:
        snapshot = _parse_snapshot_bytes(data, entry.snapshot_id)
    except SnapshotIntegrityError as exc:
        raise StrictModeStop("invalid_snapshot", str(exc)) from None
    if snapshot["request_key"] != request_key:
        raise StrictModeStop("request_key_mismatch", f"{entry.snapshot_id}: the file is for another request")
    if not is_compatible(snapshot, current_method):
        raise StrictModeStop("method_mismatch", f"{entry.snapshot_id}: checked with another freeway check method")
    return snapshot
