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
    file is opened.

Only counts are printed.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path

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
    return trips


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
    except ManifestError as error:
        print(f"refused: {error}")
        return 2

    params = IngestParams()
    all_rows: list[dict] = []
    reports: dict[str, dict] = {}
    for trip in chosen:
        name = trip["source_file"]
        if Path(name).name != name:
            reports[trip["trip_id"]] = {"note": "source_file is not a plain file name"}
            continue
        source = args.gpx_dir / name
        if not source.is_file():
            reports[trip["trip_id"]] = {"note": "source file not found"}
            continue
        points, without_time = read_gpx(source)
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
