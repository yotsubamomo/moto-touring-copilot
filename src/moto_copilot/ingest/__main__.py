"""Rebuild the Derived Segment Table from a trip manifest and check it against the data contract.

    python -m moto_copilot.ingest --gpx-dir data/bmw --out data/private/m1a_check [--trips T001 T002]

Everything this writes is private (it holds start times) and must stay out of version control:
    derived_segments_private.json     contract 1, private version
    ingest_report.json                counts per trip, no coordinates and no timestamps

The trip manifest (`--manifest`, default `<out>/trip_manifest.json`) is the only source of trip_id
and trip_role, and it is never created here. Before the research freeze only pace trips are
rebuilt (SPEC-B1 CL-B1-3 items 4 and 5):
  * without a manifest the run is refused and no GPX file is opened;
  * manifest entries whose trip_role is not "pace" are not opened and give no rows;
  * a requested trip (`--trips`) that is not a pace trip in the manifest is refused before any
    file is opened;
  * a manifest that gives one source file both a pace role and another role is refused before any
    GPX file is opened, whichever trips are requested.

Which files are touched before the research freeze (SPEC-B1 CL-B1-11, decision-20261118-issue9-qda1):
  * nothing is done to the entry that a non-pace item names: it is not opened, read, hashed or
    even stat-ed. Its `source_file` string is only compared, as text, with the pace entries;
  * the GPX folder is listed for names only;
  * every pace entry of the manifest, selected by `--trips` or not, must name exactly an entry of
    that listing, and no other spelling of that entry (letter case, an NTFS stream suffix such as
    "::$DATA", trailing dots or spaces, its 8.3 short name) may be named by a non-pace item;
    otherwise the whole run is refused before the first GPX file is opened, whichever trips are
    requested. Short names are asked of pace entries only;
  * in addition, every selected pace entry must be, by its own metadata, a regular file that is
    not a symbolic link or other reparse point and has one hard link (CL-B1-11 item 3); otherwise
    the run is refused before the first GPX file is opened.
  * Not detected here (CL-B1-11 item 4, left to the later upload and de-duplication work): a
    non-pace item that is a symbolic link to a pace file, and two files with the same content
    under different names.

Only counts are printed.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import stat
import sys
import unicodedata
from pathlib import Path, PureWindowsPath

from ..contracts import validate_derived_segments, validate_public_private_pair
from . import IngestParams, build_rows, read_gpx, to_public

PACE = "pace"


class ManifestError(ValueError):
    """The manifest is missing or unusable, or the request names a trip that may not be opened."""


def load_manifest(path: Path) -> list[dict]:
    """The trips of an existing manifest. A missing or malformed manifest is an error; none is created."""
    if not path.is_file():
        raise ManifestError(f"no trip manifest at {path}; the rebuild needs one and does not create it")
    try:
        trips = json.loads(path.read_text(encoding="utf-8"))["trips"]
    except (ValueError, KeyError, TypeError) as error:
        raise ManifestError(f"the trip manifest cannot be read: {error.__class__.__name__}") from None
    if not isinstance(trips, list):
        raise ManifestError("the trip manifest has no list of trips")
    seen: set[str] = set()
    for n, trip in enumerate(trips):
        if not isinstance(trip, dict) or not all(isinstance(trip.get(k), str) and trip.get(k)
                                                  for k in ("trip_id", "source_file", "trip_role")):
            raise ManifestError(f"trip manifest entry {n} needs a trip_id, a source_file and a trip_role")
        if trip["trip_id"] in seen:
            raise ManifestError(f"trip manifest lists {trip['trip_id']} more than once")
        seen.add(trip["trip_id"])
    _refuse_conflicting_roles(trips)
    return trips


def source_key(source_file: str) -> str:
    """A text key for comparing a manifest `source_file` with the name of a pace entry.

    It keeps only the last path component (either separator), drops an NTFS stream suffix (from
    the first ":" on, e.g. "::$DATA"), and ignores trailing dots and spaces, letter case and the
    Unicode normalization form. It is computed from the string alone and touches no file. It does
    not by itself cover every spelling of a file: 8.3 short names are handled by comparing with
    the short name of each pace entry (`pace_entry_problem`), and pace entries are opened only
    under their exact listed name. Two strings with the same key are treated as one file even
    where they might not be: the comparison errs towards refusing.
    """
    name = PureWindowsPath(unicodedata.normalize("NFC", source_file)).name
    return name.split(":", 1)[0].rstrip(" .").casefold()


def _refuse_conflicting_roles(trips: list[dict]) -> None:
    """A source file listed both as a pace trip and with any other role may not be opened at all."""
    pace_ids: dict[str, str] = {}
    other_ids: dict[str, str] = {}
    for trip in trips:
        target = pace_ids if trip["trip_role"] == PACE else other_ids
        target.setdefault(source_key(trip["source_file"]), trip["trip_id"])
    clashes = sorted(pace_ids.keys() & other_ids.keys())
    if clashes:
        pairs = ", ".join(f"{pace_ids[k]} (pace) and {other_ids[k]}" for k in clashes)
        raise ManifestError(f"the trip manifest gives the same source file a pace role and another role: {pairs}")


_REPARSE_POINT = 0x400  # FILE_ATTRIBUTE_REPARSE_POINT


def short_name(path: Path) -> str | None:
    """The 8.3 short name of a pace entry, or None when the system has no such name.

    Only ever called for pace entries (CL-B1-11 item 1.3). Raises OSError when Windows cannot
    answer, so that the caller refuses instead of guessing.
    """
    if os.name != "nt":
        return None
    import ctypes
    size = 32768
    buffer = ctypes.create_unicode_buffer(size)
    got = ctypes.windll.kernel32.GetShortPathNameW(str(path), buffer, size)
    if got == 0 or got >= size:
        raise OSError("GetShortPathNameW failed")
    return PureWindowsPath(buffer.value).name


def pace_name_problem(gpx_dir: Path, name: str, listed: set[str], other_keys: set[str]) -> str | None:
    """Why a pace entry's name makes the manifest unusable, or None. Applied to every pace entry.

    `listed` holds the names in the GPX folder listing; `other_keys` holds `source_key` of every
    non-pace item. A name that is not exactly listed may be another spelling of any entry, which
    cannot be told without touching that entry, so it refuses. Otherwise only the pace entry
    itself is queried (its short name).
    """
    if name not in listed:
        return "is not exactly the name of an entry in the GPX folder"
    try:
        alias = short_name(gpx_dir / name)
    except OSError:
        return "cannot be checked"
    if alias is not None and source_key(alias) in other_keys:
        return "has a short name that a non-pace item names"
    return None


def pace_link_problem(gpx_dir: Path, name: str) -> str | None:
    """Why a selected pace entry may not be opened by its own metadata (CL-B1-11 item 3), or None."""
    try:
        info = os.lstat(gpx_dir / name)
    except OSError:
        return "cannot be checked"
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & _REPARSE_POINT:
        return "is a symbolic link or another reparse point"
    if not stat.S_ISREG(info.st_mode):
        return "is not a regular file"
    if info.st_nlink != 1:
        return "has more than one hard link"
    return None


def check_pace_entries(gpx_dir: Path, chosen: list[dict], trips: list[dict]) -> None:
    """Refuse the run (ManifestError) unless the manifest's pace names are consistent and every
    chosen pace entry may be opened.

    The name check covers every pace entry of the manifest, whichever trips are requested; the
    link check covers the chosen ones. Runs before any GPX file is opened. Lists the GPX folder
    for names only; never touches the entry that a non-pace item names. Messages name trip ids,
    never file names.
    """
    try:
        listed = set(os.listdir(gpx_dir))
    except OSError:
        raise ManifestError("the GPX folder cannot be listed") from None
    other_keys = {source_key(t["source_file"]) for t in trips if t["trip_role"] != PACE}
    problems = [(t["trip_id"], pace_name_problem(gpx_dir, t["source_file"], listed, other_keys))
                for t in trips if t["trip_role"] == PACE]
    named = {trip_id for trip_id, why in problems if why}
    problems += [(t["trip_id"], pace_link_problem(gpx_dir, t["source_file"]))
                 for t in chosen if t["trip_id"] not in named]
    problems = [(trip_id, why) for trip_id, why in problems if why]
    if problems:
        raise ManifestError("the pace entries of the manifest do not pass the checks before opening: "
                            + "; ".join(f"{trip_id} {why}" for trip_id, why in problems))


def select_pace_trips(trips: list[dict], requested: list[str] | None) -> tuple[list[dict], int]:
    """The manifest entries to open, and the number of non-pace entries left unopened.

    With `requested`, every requested trip_id must be a pace trip in the manifest; otherwise the
    whole request is refused (ManifestError) before anything is opened.
    """
    by_id = {t["trip_id"]: t for t in trips}
    if requested is not None:
        unknown = [t for t in requested if t not in by_id]
        if unknown:
            raise ManifestError(f"requested trip(s) not in the manifest: {', '.join(unknown)}")
        refused = [t for t in requested if by_id[t]["trip_role"] != PACE]
        if refused:
            raise ManifestError(f"requested trip(s) are not pace trips and may not be opened before the "
                                f"research freeze: {', '.join(refused)}")
        chosen = [by_id[t] for t in dict.fromkeys(requested)]
    else:
        chosen = [t for t in trips if t["trip_role"] == PACE]
    not_opened = sum(1 for t in trips if t["trip_role"] != PACE)
    return chosen, not_opened


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gpx-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="private output folder (must be git-ignored)")
    parser.add_argument("--manifest", type=Path, help="trip manifest (default: <out>/trip_manifest.json)")
    parser.add_argument("--trips", nargs="+", metavar="TRIP_ID", help="rebuild only these pace trips")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        manifest = load_manifest(args.manifest or args.out / "trip_manifest.json")
        chosen, not_opened = select_pace_trips(manifest, args.trips)
        check_pace_entries(args.gpx_dir, chosen, manifest)
    except ManifestError as error:
        print(f"refused: {error}")
        return 2

    params = IngestParams()
    all_rows: list[dict] = []
    reports: dict[str, dict] = {}
    for trip in chosen:
        points, without_time = read_gpx(args.gpx_dir / trip["source_file"])
        rows, report = build_rows(points, trip_id=trip["trip_id"], trip_role=PACE,
                                  route_id=trip.get("route_id"), params=params)
        report.dropped_no_time = without_time
        report.points_read += without_time
        all_rows.extend(rows)
        reports[trip["trip_id"]] = dataclasses.asdict(report)

    public_rows = to_public(all_rows)
    violations = {
        "private": validate_derived_segments(all_rows, "private"),
        "public": validate_derived_segments(public_rows, "public"),
        "pair": validate_public_private_pair(public_rows, all_rows),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "derived_segments_private.json").write_text(
        json.dumps({"derived_segments": all_rows}, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out / "ingest_report.json").write_text(json.dumps(
        {"params": dataclasses.asdict(params), "category_scheme": params.category_scheme,
         "trips": reports, "non_pace_entries_not_opened": not_opened,
         "contract_violations": violations}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    provisional = sum(1 for t in chosen if t.get("role_status") == "provisional")
    print(f"ingest {params.ingest_version} | {params.category_scheme} | pace trips: {len(chosen)} | "
          f"non-pace entries not opened: {not_opened} | rows: {len(all_rows)}")
    print(f"{'trip':5} {'points':>7} {'jumps':>5} {'jitter':>6} {'badtime':>7} {'km':>7} {'segs':>5} {'ok':>5} {'susp':>5} {'inv':>4}  "
          f"C1/C2/C3/null  stops false/short/long  note")
    for trip_id, r in reports.items():
        if "points_read" not in r:
            print(f"{trip_id:5} {r['note']}")
            continue
        q, c, s = r["quality"], r["categories"], r["stop_events"]
        print(f"{trip_id:5} {r['points_read']:7d} {r['dropped_jumps']:5d} {r['timing_jitter_steps']:6d} {r['dropped_non_increasing_time']:7d} "
              f"{r['trimmed_length_m'] / 1000:7.1f} {r['segments']:5d} {q['ok']:5d} {q['suspect']:5d} {q['invalid']:4d}  "
              f"{c['C1']}/{c['C2']}/{c['C3']}/{c['null']}  {s['false']}/{s['short']}/{s['long']}  {r['note'] or ''}")
    for name, found in violations.items():
        print(f"contract check ({name}): {'OK' if not found else f'{len(found)} violation(s)'}")
        for message in found[:10]:
            print(f"  - {message}")
    if provisional:
        print(f"NOTE: {provisional} trip(s) have a provisional trip_role. Confirm roles before building a pace table.")
    return 0 if not any(violations.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
