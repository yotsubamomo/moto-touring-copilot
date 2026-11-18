"""SPEC-R1 R1-2 (Issue #14): write-once snapshot storage and selection (SPEC-001 7.11 items 1, 3; CL-R1-3, CL-R1-4).

Every store lives in pytest's tmp_path. All inputs are synthetic (tests/routing_synthetic.py).
"""
from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import json
import socket
from datetime import datetime, timedelta
from pathlib import Path

import pytest

import moto_copilot.routing as routing
from moto_copilot.routing import (
    SNAPSHOT_MISSING,
    FrozenEntry,
    SnapshotConflictError,
    SnapshotIntegrityError,
    SnapshotNotFoundError,
    SnapshotStore,
    SnapshotStoreError,
    SnapshotValidationError,
    StrictModeStop,
    canonical_bytes,
    compute_snapshot_id,
    find_reusable,
    select_snapshot_mode,
    select_strict,
)
from moto_copilot.routing.snapshot import TAIPEI

import routing_synthetic as syn

NOW = datetime(2026, 11, 18, 12, 0, 0, tzinfo=TAIPEI)


def at(delta: timedelta) -> str:
    """A fetched_at that is `delta` before NOW."""
    return (NOW - delta).isoformat()


def files(directory: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(directory.iterdir())}


def entry(store: SnapshotStore, snap: dict) -> dict:
    return {"request_key": snap["request_key"], "snapshot_id": snap["snapshot_id"], "sha256": store.file_sha256(snap["snapshot_id"])}


@pytest.fixture
def store(tmp_path) -> SnapshotStore:
    return SnapshotStore(tmp_path)


# --- (e) write-once storage (S35, S36, S53, S54, S55; CL-R1-3) ---------------------------------

def test_store_needs_a_caller_given_existing_directory(tmp_path):
    assert "directory" in inspect.signature(SnapshotStore).parameters
    assert inspect.signature(SnapshotStore).parameters["directory"].default is inspect.Parameter.empty
    with pytest.raises(TypeError):
        SnapshotStore()
    with pytest.raises(SnapshotStoreError):
        SnapshotStore(tmp_path / "does-not-exist")
    (tmp_path / "a-file").write_text("x")
    with pytest.raises(SnapshotStoreError):
        SnapshotStore(tmp_path / "a-file")


def test_put_writes_one_canonical_file_named_after_the_snapshot_id(store, tmp_path):
    snap = syn.snapshot("round_trip")
    result = store.put(snap)
    assert result.created is True
    assert result.path == tmp_path / f"{snap['snapshot_id']}.json"
    assert result.route_id == "RS-" + snap["snapshot_id"][3:]
    assert list(files(tmp_path)) == [f"{snap['snapshot_id']}.json"]
    assert result.path.read_bytes() == canonical_bytes(snap)
    assert store.load(snap["snapshot_id"]) == snap
    assert result.snapshot == snap


def test_put_writes_only_inside_the_given_directory(tmp_path):
    inner = tmp_path / "snapshots"
    inner.mkdir()
    SnapshotStore(inner).put(syn.snapshot())
    assert [p.name for p in tmp_path.iterdir()] == ["snapshots"]
    assert len(list(inner.iterdir())) == 1


def test_s53_same_content_later_reuses_the_existing_file_without_writing(store, tmp_path):
    old = syn.snapshot("round_trip", fetched_at=at(timedelta(days=31)))
    store.put(old)
    before = files(tmp_path)
    mtime = (tmp_path / f"{old['snapshot_id']}.json").stat().st_mtime_ns
    again = syn.snapshot("round_trip", fetched_at=at(timedelta(0)))
    assert again["snapshot_id"] == old["snapshot_id"]
    result = store.put(again)
    assert result.created is False
    assert result.snapshot == old  # the existing file, with its own fetched_at
    assert result.snapshot["legs"][0]["fetched_at"] == old["legs"][0]["fetched_at"]
    assert files(tmp_path) == before
    assert (tmp_path / f"{old['snapshot_id']}.json").stat().st_mtime_ns == mtime


def test_s54_different_content_is_a_new_file_and_the_old_file_is_unchanged(store, tmp_path):
    old = syn.snapshot("round_trip", fetched_at=at(timedelta(days=31)))
    store.put(old)
    before = files(tmp_path)
    new = syn.snapshot("round_trip", fetched_at=at(timedelta(0)), shape_suffix="2")
    result = store.put(new)
    assert result.created is True
    assert new["snapshot_id"] != old["snapshot_id"]
    after = files(tmp_path)
    assert len(after) == 2
    assert after[f"{old['snapshot_id']}.json"] == before[f"{old['snapshot_id']}.json"]


def test_s55_s36_different_content_under_an_existing_id_is_an_error_and_the_file_is_unchanged(store, tmp_path, monkeypatch):
    # Different content can only arrive under an existing snapshot_id through a collision of the
    # 10 hex characters. Simulate one: every content hashes to the same snapshot_id.
    import moto_copilot.routing.snapshot as snapshot_module
    monkeypatch.setattr(snapshot_module, "compute_snapshot_id", lambda s: "SN-0000000000")
    stored = syn.snapshot()
    other = syn.snapshot(shape_suffix="2")
    assert stored["snapshot_id"] == other["snapshot_id"] == "SN-0000000000"
    assert store.put(stored).created is True
    before = files(tmp_path)
    with pytest.raises(SnapshotConflictError):
        store.put(other)
    assert files(tmp_path) == before
    # Same content again is still fine.
    assert store.put(copy.deepcopy(stored)).created is False


def test_s55_a_misnamed_existing_file_stops_the_write_and_is_not_overwritten(store, tmp_path):
    a = syn.snapshot()
    b = syn.snapshot(shape_suffix="2")
    # A file named after b's id but holding a's content fails as not matching its name...
    path = tmp_path / f"{b['snapshot_id']}.json"
    path.write_bytes(canonical_bytes(a))
    with pytest.raises(SnapshotIntegrityError):
        store.put(b)
    assert path.read_bytes() == canonical_bytes(a)


def test_put_rejects_an_invalid_snapshot_and_writes_nothing(store, tmp_path):
    snap = syn.snapshot()
    snap["legs"][0]["freeway_check"] = "fail"
    snap["snapshot_id"] = compute_snapshot_id(snap)
    with pytest.raises(SnapshotValidationError):
        store.put(snap)
    snap2 = syn.snapshot()
    snap2["snapshot_id"] = "SN-0000000000"
    with pytest.raises(SnapshotValidationError):
        store.put(snap2)
    assert files(tmp_path) == {}


def test_a_written_file_is_not_changed_by_later_puts_loads_or_selections(store, tmp_path):
    snaps = [syn.snapshot("round_trip", fetched_at=at(timedelta(days=d)), shape_suffix=str(d)) for d in (1, 5, 40)]
    for s in snaps:
        store.put(s)
    before = files(tmp_path)
    for s in snaps:
        store.put(copy.deepcopy(s))
        store.load(s["snapshot_id"])
    find_reusable(store, snaps[0]["request_key"], syn.METHOD, now=NOW)
    select_snapshot_mode(store, snaps[0]["request_key"], syn.METHOD)
    select_strict(store, snaps[2]["request_key"], syn.METHOD, [entry(store, snaps[2])])
    assert files(tmp_path) == before


def test_load_rejects_missing_tampered_and_misnamed_files(store, tmp_path):
    snap = syn.snapshot()
    with pytest.raises(SnapshotNotFoundError):
        store.load(snap["snapshot_id"])
    store.put(snap)
    path = tmp_path / f"{snap['snapshot_id']}.json"
    tampered = json.loads(path.read_text(encoding="utf-8"))
    tampered["legs"][0]["shape"] = "synthetic-shape-tampered"
    path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(SnapshotIntegrityError):
        store.load(snap["snapshot_id"])
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(SnapshotIntegrityError):
        store.load(snap["snapshot_id"])
    path.write_text('{"snapshot_id": "x", "snapshot_id": "y"}', encoding="utf-8")
    with pytest.raises(SnapshotIntegrityError):
        store.load(snap["snapshot_id"])


@pytest.mark.parametrize("bad", ["SN-0123456789\n", "SN-012345678٩", "SN-ABCDEF0123", "../SN-0123456789", "SN-0123456789/.."])
def test_cl_r1_13_store_paths_accept_only_snapshot_ids(store, bad):
    with pytest.raises(ValueError):
        store.path_for(bad)


def test_other_files_in_the_directory_are_ignored(store, tmp_path):
    snap = syn.snapshot()
    store.put(snap)
    (tmp_path / "notes.txt").write_text("synthetic")
    (tmp_path / "SN-0123456789.json.tmp").write_text("x")
    (tmp_path / "sn-0123456789.json.bak").write_text("x")
    assert store.snapshot_ids() == [snap["snapshot_id"]]


# --- (f) normal mode: reuse (S35; 7.11 item 3 (c)) --------------------------------------------

def test_s35_a_snapshot_within_30_days_is_reused(store):
    snap = syn.snapshot("round_trip", fetched_at=at(timedelta(days=3)))
    store.put(snap)
    assert find_reusable(store, snap["request_key"], syn.METHOD, now=NOW) == snap


def test_s35_a_31_day_old_snapshot_is_not_reused(store):
    snap = syn.snapshot("round_trip", fetched_at=at(timedelta(days=31)))
    store.put(snap)
    assert find_reusable(store, snap["request_key"], syn.METHOD, now=NOW) is None


def test_the_30_day_window_is_30_times_24_hours(store):
    edge = syn.snapshot(fetched_at=at(timedelta(days=30)))
    store.put(edge)
    assert find_reusable(store, edge["request_key"], syn.METHOD, now=NOW) == edge
    assert find_reusable(store, edge["request_key"], syn.METHOD, now=NOW + timedelta(seconds=1)) is None


def test_the_acquisition_time_is_the_latest_fetched_at_of_the_legs(store):
    legs = [syn.leg("outbound", fetched_at=at(timedelta(days=31))), syn.leg("return", fetched_at=at(timedelta(days=29)))]
    snap = syn.snapshot("round_trip", legs=legs)
    store.put(snap)
    assert find_reusable(store, snap["request_key"], syn.METHOD, now=NOW) == snap
    assert find_reusable(store, snap["request_key"], syn.METHOD, now=NOW + timedelta(days=1, seconds=1)) is None


def test_s35_normal_mode_takes_the_newest_of_several_fresh_snapshots(store):
    older = syn.snapshot(fetched_at=at(timedelta(days=10)), shape_suffix="a")
    newer = syn.snapshot(fetched_at=at(timedelta(days=2)), shape_suffix="b")
    stale = syn.snapshot(fetched_at=at(timedelta(days=40)), shape_suffix="c")
    for s in (newer, stale, older):
        store.put(s)
    assert find_reusable(store, older["request_key"], syn.METHOD, now=NOW) == newer


def test_normal_mode_needs_the_same_request_key(store):
    snap = syn.snapshot(fetched_at=at(timedelta(days=1)))
    store.put(snap)
    assert find_reusable(store, syn.key("one_way", via=(syn.VIA_B, syn.VIA_A)), syn.METHOD, now=NOW) is None


def test_s76_normal_mode_does_not_reuse_a_snapshot_checked_with_another_method(store):
    other = syn.snapshot(fetched_at=at(timedelta(days=1)), method=syn.OTHER_METHOD)
    store.put(other)
    assert find_reusable(store, other["request_key"], syn.METHOD, now=NOW) is None
    mixed = syn.snapshot("round_trip", legs=[syn.leg("outbound", fetched_at=at(timedelta(days=1))),
                                              syn.leg("return", fetched_at=at(timedelta(days=1)), method=syn.OTHER_METHOD)])
    store.put(mixed)
    assert find_reusable(store, mixed["request_key"], syn.METHOD, now=NOW) is None
    assert find_reusable(store, mixed["request_key"], syn.OTHER_METHOD, now=NOW) is None


def test_s35_refetch_after_31_days_same_content_keeps_one_file_and_snapshot_mode_uses_it(store, tmp_path):
    old = syn.snapshot("round_trip", fetched_at=at(timedelta(days=31)))
    store.put(old)
    old_bytes = files(tmp_path)
    assert find_reusable(store, old["request_key"], syn.METHOD, now=NOW) is None  # so the engine is asked again
    refetched = syn.snapshot("round_trip", fetched_at=at(timedelta(0)))
    assert store.put(refetched).created is False
    assert files(tmp_path) == old_bytes
    # The reused file keeps its old fetch time, so normal mode still does not reuse it (known MVP limit).
    assert find_reusable(store, old["request_key"], syn.METHOD, now=NOW) is None
    assert select_snapshot_mode(store, old["request_key"], syn.METHOD).snapshot == old


def test_s35_refetch_after_31_days_different_content_adds_a_file_and_the_old_one_stays_usable(store, tmp_path):
    old = syn.snapshot("round_trip", fetched_at=at(timedelta(days=31)))
    store.put(old)
    old_entry = entry(store, old)
    old_bytes = (tmp_path / f"{old['snapshot_id']}.json").read_bytes()
    new = syn.snapshot("round_trip", fetched_at=at(timedelta(0)), shape_suffix="2")
    assert store.put(new).created is True
    assert len(files(tmp_path)) == 2
    assert (tmp_path / f"{old['snapshot_id']}.json").read_bytes() == old_bytes
    assert find_reusable(store, old["request_key"], syn.METHOD, now=NOW) == new
    assert select_snapshot_mode(store, old["request_key"], syn.METHOD).snapshot == new
    # The old file can still be used in Snapshot Mode through a frozen list.
    assert select_strict(store, old["request_key"], syn.METHOD, [old_entry]) == old


def test_find_reusable_rejects_bad_arguments(store):
    k = syn.key()
    with pytest.raises(ValueError):
        find_reusable(store, k, syn.METHOD, now=datetime(2026, 11, 18, 12, 0, 0))
    with pytest.raises(ValueError):
        find_reusable(store, k + "\n", syn.METHOD, now=NOW)
    with pytest.raises(ValueError):
        find_reusable(store, k, "", now=NOW)


def test_a_broken_file_stops_selection_instead_of_being_skipped(store, tmp_path):
    good = syn.snapshot(fetched_at=at(timedelta(days=1)))
    store.put(good)
    (tmp_path / "SN-0123456789.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SnapshotIntegrityError):
        find_reusable(store, good["request_key"], syn.METHOD, now=NOW)
    with pytest.raises(SnapshotIntegrityError):
        select_snapshot_mode(store, good["request_key"], syn.METHOD)


def test_equal_acquisition_times_resolve_to_the_smallest_snapshot_id(store):
    same_time = at(timedelta(days=1))
    snaps = [syn.snapshot(fetched_at=same_time, shape_suffix=s) for s in "abcd"]
    for s in reversed(snaps):
        store.put(s)
    smallest = min(snaps, key=lambda s: s["snapshot_id"])
    assert find_reusable(store, smallest["request_key"], syn.METHOD, now=NOW) == smallest
    assert select_snapshot_mode(store, smallest["request_key"], syn.METHOD).snapshot == smallest


# --- (f) plain Snapshot Mode (S17, S76, S77) ----------------------------------------------------

def test_s17_snapshot_mode_without_a_matching_snapshot_returns_snapshot_missing(store):
    result = select_snapshot_mode(store, syn.key(), syn.METHOD)
    assert result.snapshot is None and result.route_error == SNAPSHOT_MISSING == "snapshot_missing"
    store.put(syn.snapshot("one_way"))  # another request_key
    assert select_snapshot_mode(store, syn.key("round_trip"), syn.METHOD).route_error == SNAPSHOT_MISSING


def test_s77_snapshot_mode_takes_the_latest_compatible_snapshot_with_no_age_limit(store):
    old = syn.snapshot(fetched_at=at(timedelta(days=400)), shape_suffix="a")
    older = syn.snapshot(fetched_at=at(timedelta(days=800)), shape_suffix="b")
    newest_incompatible = syn.snapshot(fetched_at=at(timedelta(days=1)), shape_suffix="c", method=syn.OTHER_METHOD)
    other_request = syn.snapshot(rkey=syn.key("one_way", via=(syn.VIA_B,)), fetched_at=at(timedelta(days=1)), shape_suffix="d")
    for s in (older, newest_incompatible, old, other_request):
        store.put(s)
    result = select_snapshot_mode(store, old["request_key"], syn.METHOD)
    assert result.route_error is None
    assert result.snapshot == old


def test_s76_snapshot_mode_with_only_incompatible_snapshots_returns_snapshot_missing(store):
    snap = syn.snapshot(method=syn.OTHER_METHOD)
    store.put(snap)
    result = select_snapshot_mode(store, snap["request_key"], syn.METHOD)
    assert result == routing.SnapshotModeResult(None, SNAPSHOT_MISSING)


# --- (f) strict mode (S36, S74, S75, S76, S86; CL-R1-4) -----------------------------------------

def test_strict_mode_returns_the_listed_snapshot(store):
    snap = syn.snapshot("round_trip")
    store.put(snap)
    assert select_strict(store, snap["request_key"], syn.METHOD, [entry(store, snap)]) == snap
    assert select_strict(store, snap["request_key"], syn.METHOD, [FrozenEntry(**entry(store, snap))]) == snap


def test_s74_the_frozen_list_wins_over_a_later_snapshot(store):
    frozen = syn.snapshot(fetched_at=at(timedelta(days=100)), shape_suffix="frozen")
    later = syn.snapshot(fetched_at=at(timedelta(days=1)), shape_suffix="later")
    store.put(frozen)
    store.put(later)
    assert select_snapshot_mode(store, frozen["request_key"], syn.METHOD).snapshot == later
    assert select_strict(store, frozen["request_key"], syn.METHOD, [entry(store, frozen)]) == frozen


def test_s86_no_frozen_entry_for_the_request_stops_without_using_any_snapshot(store):
    snap = syn.snapshot()
    store.put(snap)
    other = syn.snapshot(rkey=syn.key("one_way", via=(syn.VIA_B,)), shape_suffix="x")
    store.put(other)
    for frozen in ([], [entry(store, other)]):
        with pytest.raises(StrictModeStop) as exc:
            select_strict(store, snap["request_key"], syn.METHOD, frozen)
        assert exc.value.reason == "no_entry"


def test_s75_a_missing_listed_file_stops_without_fallback(store):
    listed = syn.snapshot(shape_suffix="listed")
    present = syn.snapshot(shape_suffix="present")
    store.put(present)
    fake = {"request_key": listed["request_key"], "snapshot_id": listed["snapshot_id"], "sha256": "0" * 64}
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, listed["request_key"], syn.METHOD, [fake])
    assert exc.value.reason == "file_missing"


def test_s75_s36_a_sha256_mismatch_stops_without_fallback(store, tmp_path):
    snap = syn.snapshot(shape_suffix="frozen")
    store.put(snap)
    store.put(syn.snapshot(shape_suffix="other"))
    good = entry(store, snap)
    wrong = dict(good, sha256=hashlib.sha256(b"something else").hexdigest())
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [wrong])
    assert exc.value.reason == "hash_mismatch"
    # A changed file (even one byte, even if still a valid snapshot) also stops.
    path = tmp_path / f"{snap['snapshot_id']}.json"
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [good])
    assert exc.value.reason == "hash_mismatch"


def test_s76_strict_mode_stops_on_another_freeway_check_method(store):
    snap = syn.snapshot(method=syn.OTHER_METHOD)
    store.put(snap)
    store.put(syn.snapshot(shape_suffix="compatible"))
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [entry(store, snap)])
    assert exc.value.reason == "method_mismatch"


def test_strict_mode_ignores_the_30_day_limit(store):
    snap = syn.snapshot(fetched_at=at(timedelta(days=900)))
    store.put(snap)
    assert select_strict(store, snap["request_key"], syn.METHOD, [entry(store, snap)]) == snap


def test_strict_mode_stops_when_the_file_is_for_another_request(store):
    snap = syn.snapshot()
    store.put(snap)
    asked = syn.key("one_way", via=(syn.VIA_B,))
    listed = dict(entry(store, snap), request_key=asked)
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, asked, syn.METHOD, [listed])
    assert exc.value.reason == "request_key_mismatch"


def test_strict_mode_stops_on_an_invalid_snapshot_file_with_a_matching_hash(store, tmp_path):
    snap = syn.snapshot()
    path = tmp_path / f"{snap['snapshot_id']}.json"
    broken = copy.deepcopy(snap)
    broken["legs"][0]["has_highway"] = True
    path.write_bytes(canonical_bytes(broken))
    listed = {"request_key": snap["request_key"], "snapshot_id": snap["snapshot_id"],
              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [listed])
    assert exc.value.reason == "invalid_snapshot"


def test_strict_mode_stops_on_conflicting_entries_and_accepts_exact_duplicates(store):
    a = syn.snapshot(shape_suffix="a")
    b = syn.snapshot(shape_suffix="b")
    store.put(a)
    store.put(b)
    assert select_strict(store, a["request_key"], syn.METHOD, [entry(store, a), entry(store, a)]) == a
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, a["request_key"], syn.METHOD, [entry(store, a), entry(store, b)])
    assert exc.value.reason == "ambiguous_entry"


@pytest.mark.parametrize("field, value", [
    ("snapshot_id", "SN-0123456789\n"),
    ("snapshot_id", "SN-012345678٩"),
    ("snapshot_id", "../SN-0123456789"),
    ("request_key", "A" * 64),
    ("sha256", "A" * 64),
    ("sha256", "0" * 63),
    ("sha256", None),
])
def test_cl_r1_13_strict_mode_stops_on_a_malformed_frozen_entry(store, field, value):
    snap = syn.snapshot()
    store.put(snap)
    good = entry(store, snap)
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [good, dict(good, **{field: value})])
    assert exc.value.reason == "invalid_entry"


def test_strict_mode_stops_on_a_frozen_entry_that_is_not_an_object(store):
    snap = syn.snapshot()
    store.put(snap)
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [entry(store, snap), snap["snapshot_id"]])
    assert exc.value.reason == "invalid_entry"


def test_strict_mode_stop_is_not_a_route_error(store):
    assert not issubclass(StrictModeStop, (SnapshotStoreError, ValueError))
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, syn.key(), syn.METHOD, [])
    assert "snapshot_missing" not in str(exc.value)


# --- no network; no default location ------------------------------------------------------------

def test_hashing_storage_and_selection_need_no_network(store, monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)
    snap = syn.snapshot("round_trip", fetched_at=at(timedelta(days=1)))
    store.put(snap)
    assert find_reusable(store, syn.key("round_trip"), syn.METHOD, now=NOW) == snap
    assert select_snapshot_mode(store, snap["request_key"], syn.METHOD).snapshot == snap
    assert select_strict(store, snap["request_key"], syn.METHOD, [entry(store, snap)]) == snap


def test_the_routing_package_imports_no_network_or_environment_modules():
    package = Path(routing.__file__).parent
    banned = {"socket", "http", "urllib", "requests", "httpx", "ssl", "subprocess"}
    for source in package.glob("*.py"):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                names = [(node.module or "").split(".")[0]]
            else:
                continue
            assert not (set(names) & banned), f"{source.name} imports {names}"
        assert "environ" not in source.read_text(encoding="utf-8") and "getenv" not in source.read_text(encoding="utf-8")
