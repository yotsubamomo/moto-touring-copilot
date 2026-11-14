"""Ingest GPX files into the Derived Segment Table and check the result against contract v0.2.

    python -m moto_copilot.ingest --gpx-dir data/bmw --out data/private/m1a_check

Everything this writes is private (it holds start times) and must stay out of version control:
    trip_manifest.json                trip_id <-> source file, trip_role, route_id
    derived_segments_private.json     contract 1, private version
    ingest_report.json                counts per trip, no coordinates and no timestamps

Only counts are printed. If no manifest exists, one is created with provisional roles; roles must
be confirmed before any pace table is built (M1-B).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path

from ..contracts import validate_derived_segments, validate_public_private_pair
from . import IngestParams, build_rows, read_gpx, to_public


def _load_or_create_manifest(path: Path, gpx_files: list[Path]) -> list[dict]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))["trips"]
    trips = [{"trip_id": f"T{i + 1:03d}", "source_file": f.name, "trip_role": "pace", "route_id": None,
              "role_status": "provisional"} for i, f in enumerate(gpx_files)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"note": "PRIVATE. Roles are provisional until confirmed by the rider.",
                                "trips": trips}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return trips


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gpx-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="private output folder (must be git-ignored)")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    gpx_files = sorted(args.gpx_dir.glob("*.gpx"))
    if not gpx_files:
        print(f"no GPX file in {args.gpx_dir}")
        return 2
    params = IngestParams()
    manifest = _load_or_create_manifest(args.out / "trip_manifest.json", gpx_files)
    by_file = {f.name: f for f in gpx_files}

    all_rows: list[dict] = []
    reports: dict[str, dict] = {}
    for trip in manifest:
        source = by_file.get(trip["source_file"])
        if source is None:
            reports[trip["trip_id"]] = {"note": "source file not found"}
            continue
        points, without_time = read_gpx(source)
        rows, report = build_rows(points, trip_id=trip["trip_id"], trip_role=trip["trip_role"],
                                  route_id=trip["route_id"], params=params)
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
         "trips": reports, "contract_violations": violations}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    provisional = sum(1 for t in manifest if t.get("role_status") == "provisional")
    print(f"ingest {params.ingest_version} | {params.category_scheme} | trips: {len(manifest)} | rows: {len(all_rows)}")
    print(f"{'trip':5} {'points':>7} {'jumps':>5} {'jitter':>6} {'badtime':>7} {'km':>7} {'segs':>5} {'ok':>5} {'susp':>5} {'inv':>4}  C1/C2/C3/null  note")
    for trip_id, r in reports.items():
        if "points_read" not in r:
            print(f"{trip_id:5} {r['note']}")
            continue
        q, c = r["quality"], r["categories"]
        print(f"{trip_id:5} {r['points_read']:7d} {r['dropped_jumps']:5d} {r['timing_jitter_steps']:6d} {r['dropped_non_increasing_time']:7d} "
              f"{r['trimmed_length_m'] / 1000:7.1f} {r['segments']:5d} {q['ok']:5d} {q['suspect']:5d} {q['invalid']:4d}  "
              f"{c['C1']}/{c['C2']}/{c['C3']}/{c['null']}  {r['note'] or ''}")
    for name, found in violations.items():
        print(f"contract check ({name}): {'OK' if not found else f'{len(found)} violation(s)'}")
        for message in found[:10]:
            print(f"  - {message}")
    if provisional:
        print(f"NOTE: {provisional} trip(s) have a provisional trip_role. Confirm roles before building a pace table.")
    return 0 if not any(violations.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
