"""The rebuild flow `python -m moto_copilot.ingest` (Issue #9, SPEC-B1 CL-B1-3 items 4 and 5).

Everything runs in pytest's temporary directory on synthetic GPX files (straight lines from an
invented origin) and a synthetic trip manifest. Which files are opened is observed with a Python
audit hook on the "open" event, so a file counts as opened however the code opens it.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import sys
from pathlib import Path

import pytest

from moto_copilot.ingest import __main__ as cli
from moto_copilot.ingest.__main__ import ManifestError, load_manifest, main, select_pace_trips
from moto_copilot.ingest.segments import EARTH_RADIUS_M

T0 = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
LAT0, LON0 = 10.0, 20.0

_OPENED: list[str] | None = None


def _audit(event: str, args: tuple) -> None:
    if event == "open" and _OPENED is not None and isinstance(args[0], (str, bytes, os.PathLike)):
        _OPENED.append(os.path.normcase(os.path.abspath(os.fsdecode(args[0]))))


sys.addaudithook(_audit)


@pytest.fixture
def opened():
    """The absolute paths of every file opened while the test runs."""
    global _OPENED
    _OPENED = []
    try:
        yield _OPENED
    finally:
        _OPENED = None


def _gpx(metres: float, speed: float = 20.0) -> str:
    points = []
    for s in range(int(metres / speed) + 1):
        lon = LON0 + math.degrees(speed * s / (EARTH_RADIUS_M * math.cos(math.radians(LAT0))))
        stamp = (T0 + dt.timedelta(seconds=s)).strftime("%Y-%m-%dT%H:%M:%SZ")
        points.append(f'<trkpt lat="{LAT0:.7f}" lon="{lon:.7f}"><time>{stamp}</time></trkpt>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">'
            f'<trk><trkseg>{"".join(points)}</trkseg></trk></gpx>\n')


@pytest.fixture
def workspace(tmp_path: Path) -> dict:
    """A GPX folder with one pace trip, one holdout and one excluded trip, and a manifest.

    The holdout and the excluded files are not valid GPX, so reading them would also fail loudly.
    """
    gpx_dir, out = tmp_path / "gpx", tmp_path / "out"
    gpx_dir.mkdir()
    out.mkdir()
    (gpx_dir / "pace_a.gpx").write_text(_gpx(12_000), encoding="utf-8")
    (gpx_dir / "pace_b.gpx").write_text(_gpx(9_000), encoding="utf-8")
    (gpx_dir / "kept_back.gpx").write_text("not a GPX file\n", encoding="utf-8")
    (gpx_dir / "left_out.gpx").write_text("not a GPX file\n", encoding="utf-8")
    trips = [
        {"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace", "route_id": None},
        {"trip_id": "T902", "source_file": "kept_back.gpx", "trip_role": "holdout", "route_id": None},
        {"trip_id": "T903", "source_file": "left_out.gpx", "trip_role": "excluded", "route_id": None},
        {"trip_id": "T904", "source_file": "pace_b.gpx", "trip_role": "pace", "route_id": "R01"},
    ]
    manifest = out / "trip_manifest.json"
    manifest.write_text(json.dumps({"trips": trips}), encoding="utf-8")
    return {"gpx": gpx_dir, "out": out, "manifest": manifest}


def _norm(path: Path) -> str:
    return os.path.normcase(os.path.abspath(path))


def _gpx_opened(opened: list[str], gpx_dir: Path) -> set[str]:
    return {Path(p).name for p in opened if Path(p).parent == Path(_norm(gpx_dir))}


def test_only_pace_entries_are_opened_and_the_result_passes_the_contract(workspace, opened):
    """CL-B1-3 item 4, and C-2: the rebuilt table passes contract 1 (exit code 0)."""
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])])
    assert code == 0
    assert _gpx_opened(opened, workspace["gpx"]) == {"pace_a.gpx", "pace_b.gpx"}
    rows = json.loads((workspace["out"] / "derived_segments_private.json").read_text(encoding="utf-8"))["derived_segments"]
    assert {r["trip_id"] for r in rows} == {"T901", "T904"}
    assert {r["trip_role"] for r in rows} == {"pace"}
    assert all("short_stop_time_s" in r for r in rows)
    report = json.loads((workspace["out"] / "ingest_report.json").read_text(encoding="utf-8"))
    assert report["contract_violations"] == {"private": [], "public": [], "pair": []}
    assert report["non_pace_entries_not_opened"] == 2
    assert set(report["trips"]) == {"T901", "T904"}


def test_a_requested_holdout_trip_is_refused_before_any_file_is_opened(workspace, opened):
    """SB2-T11 / Issue #9 AC 4: the rebuild refuses a holdout trip code and opens no file."""
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"]), "--trips", "T901", "T902"])
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()
    assert not (workspace["out"] / "derived_segments_private.json").exists()
    assert not (workspace["out"] / "ingest_report.json").exists()


def test_a_requested_excluded_trip_is_refused_before_any_file_is_opened(workspace, opened):
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"]), "--trips", "T903"])
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()


def test_a_requested_trip_missing_from_the_manifest_is_refused(workspace, opened):
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"]), "--trips", "T901", "T999"])
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()


def test_requested_pace_trips_are_the_only_ones_opened(workspace, opened):
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"]), "--trips", "T904"])
    assert code == 0
    assert _gpx_opened(opened, workspace["gpx"]) == {"pace_b.gpx"}


def test_without_a_manifest_the_rebuild_is_refused_and_none_is_created(workspace, opened):
    """CL-B1-3 item 5: no provisional all-pace manifest is written and no GPX is opened."""
    workspace["manifest"].unlink()
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])])
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()
    assert not workspace["manifest"].exists()
    assert list(workspace["out"].iterdir()) == []


def test_an_explicit_manifest_path_is_used(workspace, opened, tmp_path):
    other = tmp_path / "elsewhere.json"
    other.write_text(workspace["manifest"].read_text(encoding="utf-8"), encoding="utf-8")
    workspace["manifest"].unlink()
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"]), "--manifest", str(other)])
    assert code == 0
    assert _gpx_opened(opened, workspace["gpx"]) == {"pace_a.gpx", "pace_b.gpx"}


@pytest.mark.parametrize("content", [
    "not json",
    json.dumps({"no_trips": []}),
    json.dumps({"trips": {"T901": "pace"}}),
    json.dumps({"trips": [{"trip_id": "T901", "source_file": "pace_a.gpx"}]}),
    json.dumps({"trips": [{"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace"},
                          {"trip_id": "T901", "source_file": "pace_b.gpx", "trip_role": "pace"}]}),
])
def test_a_malformed_manifest_is_refused_before_any_gpx_is_opened(workspace, opened, content):
    workspace["manifest"].write_text(content, encoding="utf-8")
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])])
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()


def test_a_source_file_outside_the_gpx_folder_is_not_opened(workspace, opened, tmp_path):
    (tmp_path / "outside.gpx").write_text(_gpx(12_000), encoding="utf-8")
    trips = [{"trip_id": "T905", "source_file": "../outside.gpx", "trip_role": "pace", "route_id": None}]
    workspace["manifest"].write_text(json.dumps({"trips": trips}), encoding="utf-8")
    opened.clear()                      # the writes above are the test's own
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])])
    assert code == 2                    # cycle 2: a pace name that is not a listed entry refuses the run
    assert _norm(tmp_path / "outside.gpx") not in opened
    assert not (workspace["out"] / "ingest_report.json").exists()


def test_select_pace_trips_and_load_manifest_directly(tmp_path):
    trips = [{"trip_id": "T901", "source_file": "a.gpx", "trip_role": "pace"},
             {"trip_id": "T902", "source_file": "b.gpx", "trip_role": "holdout"}]
    assert select_pace_trips(trips, None) == ([trips[0]], 1)
    assert select_pace_trips(trips, ["T901", "T901"]) == ([trips[0]], 1)
    with pytest.raises(ManifestError, match="not pace trips"):
        select_pace_trips(trips, ["T902"])
    with pytest.raises(ManifestError, match="no trip manifest"):
        load_manifest(tmp_path / "missing.json")


# --- R1-F1: one source file with a pace role and another role -----------------------------------

@pytest.mark.parametrize("other_name, other_role, requested", [
    ("pace_a.gpx", "holdout", None),
    ("pace_a.gpx", "holdout", ["T901"]),
    ("pace_a.gpx", "excluded", None),
    ("pace_a.gpx", "excluded", ["T901"]),
    ("PACE_A.GPX", "holdout", None),          # letter case
    ("Pace_A.gpx", "holdout", ["T901"]),
    ("pace_a.gpx.", "holdout", None),          # trailing dot (Windows ignores it)
    ("pace_a.gpx ", "holdout", None),          # trailing space
    ("sub/pace_a.gpx", "holdout", None),       # a path whose last part is the same name
    (r"sub\pace_a.gpx", "excluded", ["T901"]),
])
def test_a_source_file_with_a_pace_and_a_non_pace_role_is_refused_before_any_gpx_is_opened(
        workspace, opened, other_name, other_role, requested):
    """R1-F1: T901 (pace) and T902 (non-pace) name the same file. Whether the pace trips are chosen
    automatically or requested, the rebuild refuses and opens no GPX file and writes no rows."""
    trips = [
        {"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace", "route_id": None},
        {"trip_id": "T902", "source_file": other_name, "trip_role": other_role, "route_id": None},
        {"trip_id": "T904", "source_file": "pace_b.gpx", "trip_role": "pace", "route_id": "R01"},
    ]
    workspace["manifest"].write_text(json.dumps({"trips": trips}), encoding="utf-8")
    argv = ["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])]
    if requested:
        argv += ["--trips", *requested]
    opened.clear()
    code = main(argv)
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()
    assert not (workspace["out"] / "derived_segments_private.json").exists()
    assert not (workspace["out"] / "ingest_report.json").exists()


def test_the_conflict_is_reported_by_trip_id_and_found_by_load_manifest(tmp_path):
    manifest = tmp_path / "m.json"
    manifest.write_text(json.dumps({"trips": [
        {"trip_id": "T902", "source_file": "x.gpx", "trip_role": "holdout"},
        {"trip_id": "T901", "source_file": "X.GPX", "trip_role": "pace"},
    ]}), encoding="utf-8")
    with pytest.raises(ManifestError, match=r"T901 \(pace\) and T902"):
        load_manifest(manifest)


def test_non_pace_entries_sharing_a_file_and_distinct_pace_files_are_not_a_conflict(workspace, opened):
    trips = [
        {"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace", "route_id": None},
        {"trip_id": "T902", "source_file": "kept_back.gpx", "trip_role": "holdout", "route_id": None},
        {"trip_id": "T903", "source_file": "KEPT_BACK.gpx", "trip_role": "excluded", "route_id": None},
        {"trip_id": "T904", "source_file": "pace_b.gpx", "trip_role": "pace", "route_id": "R01"},
    ]
    workspace["manifest"].write_text(json.dumps({"trips": trips}), encoding="utf-8")
    code = main(["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])])
    assert code == 0
    assert _gpx_opened(opened, workspace["gpx"]) == {"pace_a.gpx", "pace_b.gpx"}


# --- Cycle 2 (FA ruling-20261117-issue9-c1 §3.2; CL-B1-11): other spellings and links -----------

def _write_manifest(workspace, trips):
    workspace["manifest"].write_text(json.dumps({"trips": trips}), encoding="utf-8")


def _run(workspace, opened, requested=None):
    argv = ["--gpx-dir", str(workspace["gpx"]), "--out", str(workspace["out"])]
    if requested:
        argv += ["--trips", *requested]
    opened.clear()
    return main(argv)


def _assert_refused(code, opened, workspace):
    assert code == 2
    assert _gpx_opened(opened, workspace["gpx"]) == set()
    assert not (workspace["out"] / "derived_segments_private.json").exists()
    assert not (workspace["out"] / "ingest_report.json").exists()


SELECTIONS = [None, ["T901"]]


@pytest.mark.parametrize("requested", SELECTIONS)
@pytest.mark.parametrize("role", ["holdout", "excluded"])
@pytest.mark.parametrize("pace_name, other_name", [
    ("pace_a.gpx::$DATA", "pace_a.gpx"),       # stream spelling on the pace entry
    ("pace_a.gpx::$data", "pace_a.gpx"),
    ("pace_a.gpx:other:$DATA", "pace_a.gpx"),
    ("pace_a.gpx", "pace_a.gpx::$DATA"),       # stream spelling on the non-pace item
    ("pace_a.gpx", "PACE_A.GPX::$data"),
    ("pace_a.gpx", "pace_a.gpx. ::$DATA"),
])
def test_an_ntfs_stream_spelling_on_either_side_is_refused_before_any_gpx_is_opened(
        workspace, opened, pace_name, other_name, role, requested):
    """R2-F1: "::$DATA" names the same directory entry. On the pace side the name is not a listed
    entry; on the non-pace side its key equals the pace entry's. Either way: exit 2, nothing opened."""
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": pace_name, "trip_role": "pace"},
        {"trip_id": "T902", "source_file": other_name, "trip_role": role},
    ])
    _assert_refused(_run(workspace, opened, requested), opened, workspace)


@pytest.mark.parametrize("requested", SELECTIONS)
def test_a_stream_spelling_alone_on_a_pace_entry_is_refused(workspace, opened, requested):
    _write_manifest(workspace, [{"trip_id": "T901", "source_file": "pace_a.gpx::$DATA", "trip_role": "pace"}])
    _assert_refused(_run(workspace, opened, requested), opened, workspace)


@pytest.mark.parametrize("requested", SELECTIONS)
@pytest.mark.parametrize("role", ["holdout", "excluded"])
def test_an_8_3_short_name_on_the_pace_entry_is_refused(workspace, opened, role, requested):
    """A pace entry spelled as a short name is never an entry of the folder listing (listings give
    long names), so this holds whether or not the volume makes short names."""
    long_name = "pace_long_named_trip_a.gpx"
    (workspace["gpx"] / long_name).write_text(_gpx(12_000), encoding="utf-8")
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": "PACE_L~1.GPX", "trip_role": "pace"},
        {"trip_id": "T902", "source_file": long_name, "trip_role": role},
    ])
    assert "PACE_L~1.GPX" not in os.listdir(workspace["gpx"])
    _assert_refused(_run(workspace, opened, requested), opened, workspace)


@pytest.mark.parametrize("requested", SELECTIONS)
@pytest.mark.parametrize("role", ["holdout", "excluded"])
def test_an_8_3_short_name_on_the_non_pace_item_is_refused(workspace, opened, monkeypatch, role, requested):
    """The non-pace item names the pace file by its short name. The short name is asked of the pace
    entry only; it is replaced here so the test does not depend on the volume making short names."""
    long_name = "pace_long_named_trip_a.gpx"
    (workspace["gpx"] / long_name).write_text(_gpx(12_000), encoding="utf-8")
    asked = []

    def fake_short_name(path):
        asked.append(Path(path).name)
        return "PACE_L~1.GPX" if Path(path).name == long_name else Path(path).name.upper()

    monkeypatch.setattr(cli, "short_name", fake_short_name)
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": long_name, "trip_role": "pace"},
        {"trip_id": "T902", "source_file": "PACE_L~1.GPX", "trip_role": role},
    ])
    _assert_refused(_run(workspace, opened, requested), opened, workspace)
    assert asked == [long_name]                       # only the pace entry was asked


def test_the_real_short_name_lookup_is_only_used_on_pace_entries_and_matches_the_os(workspace):
    """On this machine: the lookup returns the system's short name for a pace file, or the long name
    itself when the volume makes none. Either value is what the comparison uses."""
    long_name = "pace_long_named_trip_a.gpx"
    path = workspace["gpx"] / long_name
    path.write_text(_gpx(1_000), encoding="utf-8")
    got = cli.short_name(path)
    if os.name == "nt":
        assert got is not None and (got == long_name or "~" in got)
    else:
        assert got is None


@pytest.mark.parametrize("requested", SELECTIONS)
def test_a_pace_entry_that_is_a_hard_link_to_a_holdout_file_is_refused(workspace, opened, capsys, requested):
    """CL-B1-11 item 3 / L-1 (1)(2): the pace name is a real hard link to the holdout's file."""
    held = workspace["gpx"] / "held_trip.gpx"
    held.write_text(_gpx(12_000), encoding="utf-8")
    os.link(held, workspace["gpx"] / "alias_trip.gpx")
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": "alias_trip.gpx", "trip_role": "pace"},
        {"trip_id": "T902", "source_file": "held_trip.gpx", "trip_role": "holdout"},
    ])
    capsys.readouterr()
    _assert_refused(_run(workspace, opened, requested), opened, workspace)
    out = capsys.readouterr().out
    assert "T901" in out and "hard link" in out
    assert "alias_trip" not in out and "held_trip" not in out


def test_a_pace_file_with_a_hard_link_named_by_an_excluded_item_is_refused(workspace, opened, capsys):
    """L-1 (3): the pace entry is the original, the excluded item is the other link."""
    os.link(workspace["gpx"] / "pace_a.gpx", workspace["gpx"] / "other_name.gpx")
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace"},
        {"trip_id": "T903", "source_file": "other_name.gpx", "trip_role": "excluded"},
    ])
    capsys.readouterr()
    _assert_refused(_run(workspace, opened), opened, workspace)
    out = capsys.readouterr().out
    assert "T901" in out and "pace_a" not in out and "other_name" not in out


@pytest.mark.parametrize("requested", SELECTIONS)
@pytest.mark.parametrize("kind", ["symlink", "reparse_point"])
def test_a_pace_entry_that_is_a_symbolic_link_is_refused(workspace, opened, monkeypatch, capsys, kind, requested):
    """CL-B1-11 item 3 / L-2. Creating a symbolic link needs a privilege this machine may lack, so the
    answer of os.lstat for the pace entry is replaced; every other path gets the real answer."""
    import stat as st
    real_lstat = os.lstat
    target = _norm(workspace["gpx"] / "pace_a.gpx")

    def fake_lstat(path, *args, **kwargs):
        if _norm(Path(path)) != target:
            return real_lstat(path, *args, **kwargs)
        if kind == "symlink":
            return os.stat_result((st.S_IFLNK | 0o777, 0, 0, 1, 0, 0, 0, 0, 0, 0))
        return os.stat_result((st.S_IFREG | 0o644, 0, 0, 1, 0, 0, 0, 0, 0, 0), {"st_file_attributes": 0x400})

    monkeypatch.setattr(os, "lstat", fake_lstat)
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace"},
        {"trip_id": "T902", "source_file": "kept_back.gpx", "trip_role": "holdout"},
    ])
    capsys.readouterr()
    _assert_refused(_run(workspace, opened, requested), opened, workspace)
    out = capsys.readouterr().out
    assert "T901" in out and "symbolic link" in out and "pace_a" not in out


def test_no_metadata_is_asked_of_a_non_pace_item(workspace, opened, monkeypatch):
    """CL-B1-11 item 1: lstat and the short-name lookup are only used on pace entries, and the
    non-pace items' files are never opened (the audit hook sees no open of them)."""
    asked = []
    real_lstat, real_short = os.lstat, cli.short_name

    def spy_lstat(path, *args, **kwargs):
        asked.append(Path(path).name)
        return real_lstat(path, *args, **kwargs)

    def spy_short(path):
        asked.append(Path(path).name)
        return real_short(path)

    monkeypatch.setattr(os, "lstat", spy_lstat)
    monkeypatch.setattr(cli, "short_name", spy_short)
    gpx = workspace["gpx"]
    code = _run(workspace, opened)
    monkeypatch.undo()
    assert code == 0
    in_gpx = {n for n in asked if (gpx / n).exists()}
    assert in_gpx == {"pace_a.gpx", "pace_b.gpx"}                 # asked of both pace entries, nothing else
    assert "kept_back.gpx" not in asked and "left_out.gpx" not in asked
    assert _gpx_opened(opened, gpx) == {"pace_a.gpx", "pace_b.gpx"}


def test_a_missing_pace_file_refuses_the_run(workspace, opened):
    _write_manifest(workspace, [
        {"trip_id": "T901", "source_file": "pace_a.gpx", "trip_role": "pace"},
        {"trip_id": "T906", "source_file": "not_there.gpx", "trip_role": "pace"},
    ])
    _assert_refused(_run(workspace, opened), opened, workspace)
