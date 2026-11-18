"""SPEC-R1 R1-2 (Issue #14): write-once snapshot storage and selection (SPEC-001 7.11 items 1, 3; CL-R1-3, CL-R1-4).

Every store lives in pytest's tmp_path. All inputs are synthetic (tests/routing_synthetic.py).
"""
from __future__ import annotations

import ast
import copy
import errno
import hashlib
import inspect
import json
import os
import socket
import stat
import traceback
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


@pytest.mark.parametrize("ahead", [timedelta(seconds=1), timedelta(days=1)])
def test_cl_r1_16_a_snapshot_acquired_after_now_is_not_reused(store, ahead):
    future = syn.snapshot("round_trip", fetched_at=(NOW + ahead).isoformat())
    store.put(future)
    assert find_reusable(store, future["request_key"], syn.METHOD, now=NOW) is None
    # Plain Snapshot Mode has no age limit and still selects it.
    assert select_snapshot_mode(store, future["request_key"], syn.METHOD).snapshot == future


def test_cl_r1_16_a_snapshot_acquired_exactly_now_is_reused(store):
    snap = syn.snapshot(fetched_at=NOW.isoformat())
    store.put(snap)
    assert find_reusable(store, snap["request_key"], syn.METHOD, now=NOW) == snap


def test_cl_r1_16_one_leg_after_now_makes_the_snapshot_not_reusable(store):
    legs = [syn.leg("outbound", fetched_at=at(timedelta(days=1))), syn.leg("return", fetched_at=(NOW + timedelta(seconds=1)).isoformat())]
    snap = syn.snapshot("round_trip", legs=legs)
    store.put(snap)
    assert find_reusable(store, snap["request_key"], syn.METHOD, now=NOW) is None


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
    """Only routing/http_transport.py may import `http` and `ssl` (CL-R1-25; changed in Issue #16 as
    decision-20261118-issue16-c161 sections 2.2 and 2.4 allow). Every other module, at any depth,
    imports no network module and does not import http_transport; no module reads env variables."""
    package = Path(routing.__file__).parent
    banned = {"socket", "http", "urllib", "requests", "httpx", "ssl", "subprocess"}
    transport = package / "http_transport.py"
    assert transport.is_file()  # the one exemption must point at an existing file
    sources = sorted(package.rglob("*.py"))  # recursive: a subpackage cannot get around the check
    assert transport in sources
    for source in sources:
        text = source.read_text(encoding="utf-8")
        allowed = {"http", "ssl"} if source == transport else set()
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
                refers = any("http_transport" in alias.name.split(".") for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names = [(node.module or "").split(".")[0]] if node.level == 0 else []
                refers = ("http_transport" in (node.module or "").split(".")
                          or any(alias.name == "http_transport" for alias in node.names))
            elif isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
                names = []
                refers = name in ("__import__", "import_module") and any(
                    isinstance(arg, ast.Constant) and isinstance(arg.value, str) and "http_transport" in arg.value
                    for arg in node.args)
            else:
                continue
            assert not (set(names) & (banned - allowed)), f"{source.name} imports {names}"
            if source != transport:
                assert not refers, f"{source.name} imports http_transport"
        assert "environ" not in text and "getenv" not in text


# --- R1-F1 (audit issue-14-c1-r1): a list or object trip_type in a file -----------------------

def _bad_trip_type_file(store: SnapshotStore, tmp_path: Path, bad) -> tuple[dict, bytes]:
    """Write a snapshot file whose trip_type is `bad`; returns the original snapshot and the bytes."""
    snap = syn.snapshot(shape_suffix="bad")
    broken = copy.deepcopy(snap)
    broken["trip_type"] = bad
    data = canonical_bytes(broken)
    (tmp_path / f"{snap['snapshot_id']}.json").write_bytes(data)
    return snap, data


@pytest.mark.parametrize("bad", [[], {}])
def test_r1_f1_put_rejects_a_list_or_object_trip_type(store, tmp_path, bad):
    snap = syn.snapshot()
    snap["trip_type"] = bad
    with pytest.raises(SnapshotValidationError) as exc:
        store.put(snap)
    assert any(e.startswith("$.trip_type:") for e in exc.value.errors)
    assert files(tmp_path) == {}


@pytest.mark.parametrize("bad", [[], {}])
def test_r1_f1_load_and_normal_selection_stop_on_a_list_or_object_trip_type(store, tmp_path, bad):
    good = syn.snapshot(fetched_at=at(timedelta(days=1)), shape_suffix="good")
    store.put(good)
    snap, data = _bad_trip_type_file(store, tmp_path, bad)
    with pytest.raises(SnapshotIntegrityError):
        store.load(snap["snapshot_id"])
    # The good compatible snapshot for the same request is not used instead.
    with pytest.raises(SnapshotIntegrityError):
        find_reusable(store, good["request_key"], syn.METHOD, now=NOW)
    with pytest.raises(SnapshotIntegrityError):
        select_snapshot_mode(store, good["request_key"], syn.METHOD)
    assert (tmp_path / f"{snap['snapshot_id']}.json").read_bytes() == data


@pytest.mark.parametrize("bad", [[], {}])
def test_r1_f1_strict_mode_stops_on_a_list_or_object_trip_type_with_the_real_sha256(store, tmp_path, bad):
    good = syn.snapshot(shape_suffix="good")
    store.put(good)
    snap, data = _bad_trip_type_file(store, tmp_path, bad)
    listed = {"request_key": snap["request_key"], "snapshot_id": snap["snapshot_id"],
              "sha256": hashlib.sha256(data).hexdigest()}
    assert listed["sha256"] == store.file_sha256(snap["snapshot_id"])
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, snap["request_key"], syn.METHOD, [listed])
    assert exc.value.reason == "invalid_snapshot"
    assert exc.value.__cause__ is None


# --- R1-F2 (audit issue-14-c1-r1): OS errors are converted and carry no path -------------------

# A synthetic directory name used to prove that no path reaches a message or a traceback.
MARKER = "synthetic-dir-0.000001N-0.000001E"


@pytest.fixture
def marked(tmp_path) -> tuple[SnapshotStore, Path]:
    directory = tmp_path / MARKER
    directory.mkdir()
    return SnapshotStore(directory), directory


def assert_path_free(exc: BaseException) -> None:
    text = "".join(traceback.format_exception(exc))
    assert MARKER not in text
    assert exc.__cause__ is None and exc.__suppress_context__


def _fail_reads_of(monkeypatch, name: str, error: type[OSError], errno_value: int) -> None:
    real = Path.read_bytes

    def fake(self):
        if self.name == name:
            raised = error(errno_value, os.strerror(errno_value), str(self))
            assert MARKER in str(raised)  # the raw OS error does carry the path
            raise raised
        return real(self)

    monkeypatch.setattr(Path, "read_bytes", fake)


@pytest.mark.parametrize("error, errno_value", [(PermissionError, errno.EACCES), (OSError, errno.EIO)])
def test_r1_f2_a_read_error_stops_normal_selection_without_a_path(marked, monkeypatch, error, errno_value):
    store, _ = marked
    good = syn.snapshot(fetched_at=at(timedelta(days=1)), shape_suffix="good")
    blocked = syn.snapshot(fetched_at=at(timedelta(days=2)), shape_suffix="blocked")
    store.put(good)
    store.put(blocked)
    _fail_reads_of(monkeypatch, f"{blocked['snapshot_id']}.json", error, errno_value)
    for call in (lambda: store.load(blocked["snapshot_id"]),
                 lambda: find_reusable(store, good["request_key"], syn.METHOD, now=NOW),
                 lambda: select_snapshot_mode(store, good["request_key"], syn.METHOD),
                 lambda: store.file_sha256(blocked["snapshot_id"])):
        with pytest.raises(SnapshotIntegrityError) as exc:
            call()
        assert not isinstance(exc.value, SnapshotNotFoundError)
        assert_path_free(exc.value)


@pytest.mark.parametrize("error, errno_value", [(PermissionError, errno.EACCES), (OSError, errno.EIO)])
def test_r1_f2_a_read_error_stops_strict_mode_without_a_path(marked, monkeypatch, error, errno_value):
    store, _ = marked
    listed = syn.snapshot(shape_suffix="listed")
    store.put(listed)
    store.put(syn.snapshot(shape_suffix="other"))
    frozen = [entry(store, listed)]
    _fail_reads_of(monkeypatch, f"{listed['snapshot_id']}.json", error, errno_value)
    with pytest.raises(StrictModeStop) as exc:
        select_strict(store, listed["request_key"], syn.METHOD, frozen)
    assert exc.value.reason == "unreadable"
    assert_path_free(exc.value)


def test_r1_f2_a_file_listed_and_then_gone_stops_normal_selection(marked, monkeypatch):
    store, directory = marked
    good = syn.snapshot(fetched_at=at(timedelta(days=1)), shape_suffix="good")
    store.put(good)
    vanished = syn.snapshot(shape_suffix="vanished")["snapshot_id"]
    assert not (directory / f"{vanished}.json").exists()
    monkeypatch.setattr(SnapshotStore, "snapshot_ids", lambda self: sorted([good["snapshot_id"], vanished]))
    for call in (lambda: find_reusable(store, good["request_key"], syn.METHOD, now=NOW),
                 lambda: select_snapshot_mode(store, good["request_key"], syn.METHOD)):
        with pytest.raises(SnapshotIntegrityError) as exc:
            call()
        assert not isinstance(exc.value, SnapshotNotFoundError)
        assert "no longer there" in str(exc.value)
        assert_path_free(exc.value)
    # A direct load of an id that never existed keeps the dedicated not-found error.
    with pytest.raises(SnapshotNotFoundError) as exc:
        store.load(vanished)
    assert_path_free(exc.value)


def test_r1_f2_a_directory_that_cannot_be_listed_stops_normal_selection(marked, monkeypatch):
    store, directory = marked
    store.put(syn.snapshot())

    def refuse(self):
        raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(self))

    monkeypatch.setattr(Path, "iterdir", refuse)
    for call in (lambda: find_reusable(store, syn.key("one_way"), syn.METHOD, now=NOW),
                 lambda: select_snapshot_mode(store, syn.key("one_way"), syn.METHOD)):
        with pytest.raises(SnapshotIntegrityError) as exc:
            call()
        assert_path_free(exc.value)


def test_r1_f2_put_errors_carry_no_path_and_write_nothing(marked, monkeypatch):
    store, directory = marked
    import moto_copilot.routing.store as store_module

    def refuse_open(path, *args, **kwargs):
        raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(path))

    monkeypatch.setattr(store_module, "open", refuse_open, raising=False)
    with pytest.raises(SnapshotStoreError) as exc:
        store.put(syn.snapshot())
    assert_path_free(exc.value)
    monkeypatch.undo()

    def refuse_status(self, *args, **kwargs):
        raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(self))

    monkeypatch.setattr(Path, "exists", refuse_status)
    with pytest.raises(SnapshotStoreError) as exc:
        store.put(syn.snapshot())
    assert_path_free(exc.value)
    monkeypatch.undo()
    assert list(directory.iterdir()) == []


# --- CL-R1-20 (decision-20261118-issue14-qalt1): candidates by name; every one must read --------

def _selection_stops(store: SnapshotStore, request_key: str) -> None:
    """Both normal-selection entry points stop with a path-free SnapshotIntegrityError."""
    for call in (lambda: find_reusable(store, request_key, syn.METHOD, now=NOW),
                 lambda: select_snapshot_mode(store, request_key, syn.METHOD)):
        with pytest.raises(SnapshotIntegrityError) as exc:
            call()
        assert not isinstance(exc.value, SnapshotNotFoundError)
        assert_path_free(exc.value)


def _good_snapshot(store: SnapshotStore, with_good: bool) -> dict:
    """A compatible, fresh snapshot for the request; stored only when `with_good`."""
    good = syn.snapshot(fetched_at=at(timedelta(days=1)), shape_suffix="good")
    if with_good:
        store.put(good)
    return good


def _fail_stat_of(monkeypatch, name: str, make_error) -> None:
    """Make os.stat (what snapshots() calls) fail for one entry; everything else is real."""
    real = os.stat

    def fake(path, *args, **kwargs):
        if os.fspath(path).endswith(os.sep + name):
            raised = make_error(os.fspath(path))
            assert MARKER in str(raised)
            raise raised
        return real(path, *args, **kwargs)

    monkeypatch.setattr(os, "stat", fake)


@pytest.mark.parametrize("with_good", [True, False])
def test_cl_r1_20_t1_a_directory_named_like_a_snapshot_stops_normal_selection(marked, with_good):
    store, directory = marked
    good = _good_snapshot(store, with_good)
    (directory / f"{syn.snapshot(shape_suffix='dir')['snapshot_id']}.json").mkdir()
    _selection_stops(store, good["request_key"])


@pytest.mark.parametrize("with_good", [True, False])
def test_cl_r1_20_t2_an_entry_deleted_after_listing_stops_normal_selection(marked, monkeypatch, with_good):
    store, directory = marked
    good = _good_snapshot(store, with_good)
    gone = syn.snapshot(fetched_at=at(timedelta(days=2)), shape_suffix="gone")
    store.put(gone)
    gone_path = directory / f"{gone['snapshot_id']}.json"
    real_iterdir = Path.iterdir

    def iterdir_then_delete(self):
        entries = list(real_iterdir(self))
        if self == directory and gone_path.exists():
            gone_path.unlink()  # a real deletion after listing, before the status check
        return iter(entries)

    monkeypatch.setattr(Path, "iterdir", iterdir_then_delete)
    with pytest.raises(SnapshotIntegrityError) as exc:
        find_reusable(store, good["request_key"], syn.METHOD, now=NOW)
    assert "no longer there" in str(exc.value)
    assert_path_free(exc.value)
    assert not gone_path.exists()
    store.put(gone)  # list again, delete again: Snapshot Mode stops the same way
    with pytest.raises(SnapshotIntegrityError) as exc:
        select_snapshot_mode(store, good["request_key"], syn.METHOD)
    assert_path_free(exc.value)


@pytest.mark.parametrize("with_good", [True, False])
@pytest.mark.parametrize("make_error", [
    lambda p: PermissionError(errno.EACCES, os.strerror(errno.EACCES), p),
    lambda p: OSError(errno.EIO, os.strerror(errno.EIO), p),
], ids=["EACCES", "EIO"])
def test_cl_r1_20_t3_a_status_error_stops_normal_selection(marked, monkeypatch, with_good, make_error):
    store, _ = marked
    good = _good_snapshot(store, with_good)
    blocked = syn.snapshot(fetched_at=at(timedelta(days=2)), shape_suffix="blocked")
    store.put(blocked)
    _fail_stat_of(monkeypatch, f"{blocked['snapshot_id']}.json", make_error)
    _selection_stops(store, good["request_key"])


@pytest.mark.parametrize("with_good", [True, False])
@pytest.mark.parametrize("make_error", [
    lambda p: FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), p),
    lambda p: OSError(errno.ELOOP, os.strerror(errno.ELOOP), p),
], ids=["dangling-ENOENT", "loop-ELOOP"])
def test_cl_r1_20_t4_a_dangling_or_looping_symlink_stops_normal_selection(marked, monkeypatch, with_good, make_error):
    store, _ = marked
    good = _good_snapshot(store, with_good)
    link = syn.snapshot(fetched_at=at(timedelta(days=2)), shape_suffix="link")
    store.put(link)
    _fail_stat_of(monkeypatch, f"{link['snapshot_id']}.json", make_error)
    _selection_stops(store, good["request_key"])


def test_cl_r1_20_t5_entries_with_other_names_are_still_ignored(marked, monkeypatch):
    store, directory = marked
    good = _good_snapshot(store, True)
    other = good["snapshot_id"]
    # (No upper-case variant of the good name: on a case-insensitive file system it is the same file.)
    for name in (f"{other}.json.tmp", f"{other}.jsonx", f"x{other}.json",
                 f"{other}x.json", "SN-ABCDEF0123.json", "notes.txt"):
        (directory / name).write_text("not a snapshot", encoding="utf-8")
    (directory / f"{other}.json.d").mkdir()
    # Entries with other names are not even stat'ed: a failing stat on them changes nothing.
    real = os.stat

    def fake(path, *args, **kwargs):
        if os.path.basename(os.fspath(path)) != f"{other}.json" and os.path.dirname(os.fspath(path)) == os.fspath(directory):
            raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), os.fspath(path))
        return real(path, *args, **kwargs)

    monkeypatch.setattr(os, "stat", fake)
    assert store.snapshot_ids() == [other]
    assert find_reusable(store, good["request_key"], syn.METHOD, now=NOW) == good
    assert select_snapshot_mode(store, good["request_key"], syn.METHOD).snapshot == good


@pytest.mark.parametrize("with_good", [True, False])
def test_cl_r1_20_t6_an_entry_that_is_not_a_regular_file_is_never_opened(marked, monkeypatch, with_good):
    store, directory = marked
    good = _good_snapshot(store, with_good)
    # A real directory, and a real valid snapshot file that os.stat reports as a FIFO.
    subdir_name = f"{syn.snapshot(shape_suffix='dir')['snapshot_id']}.json"
    (directory / subdir_name).mkdir()
    fifo = syn.snapshot(fetched_at=at(timedelta(hours=1)), shape_suffix="fifo")
    store.put(fifo)
    fifo_name = f"{fifo['snapshot_id']}.json"
    real_stat, real_read, real_open = os.stat, Path.read_bytes, open
    opened = []

    def fake_stat(path, *args, **kwargs):
        if os.fspath(path).endswith(os.sep + fifo_name):
            return os.stat_result((stat.S_IFIFO | 0o644, 0, 0, 1, 0, 0, 0, 0, 0, 0))
        return real_stat(path, *args, **kwargs)

    def fake_read(self):
        opened.append(self.name)
        return real_read(self)

    def fake_open(file, *args, **kwargs):
        opened.append(os.path.basename(os.fspath(file)))
        return real_open(file, *args, **kwargs)

    import moto_copilot.routing.store as store_module
    monkeypatch.setattr(os, "stat", fake_stat)
    monkeypatch.setattr(Path, "read_bytes", fake_read)
    monkeypatch.setattr(store_module, "open", fake_open, raising=False)
    for remove_dir in (False, True):
        if remove_dir:
            (directory / subdir_name).rmdir()  # leaves only the FIFO-like entry (and maybe the good one)
        opened.clear()
        _selection_stops(store, good["request_key"])
        assert subdir_name not in opened and fifo_name not in opened
