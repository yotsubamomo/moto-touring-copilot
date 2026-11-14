"""M1-B Technical Spike on the rider's GPX: trip roles, route catalog, pace table, ETA.

    PYTHONPATH=src python experiments/m1b_spike/run_m1b.py --gpx-dir data/bmw --out data/private/m1b

Everything is written to the private output folder (git-ignored). Only counts and aggregate
values are printed: no coordinates and no ride timestamps.

What this is not: it is not E1 or E2. Holdout trips are excluded from the pace table and their
ride times are never read here; no ETA is compared with any actual ride.

Choices made here (2026-11-14, by rule, the rider may change them):
  * demo routes are the stretches several trips ride in the same direction (DEMO_GROUPS)
  * on each demo route the most recent trip is the holdout; the earliest gives the geometry
  * category thresholds are the terciles of curvature over the ok rows of pace trips

M1 Review (2026-11-14): the T008/T010 stretch was dropped as a demo route. Judged from the pace
trip T008 and the route geometry only, it is a flat, straight, high-speed transit road and not a
mountain touring route. The rider then excluded T010 (EXCLUDED): it is in no pace table and is
not evaluation data. Excluded trips are marked in the private trip inventory and produce no rows;
the data contract's trip_role enum is unchanged. T010 was never a pace trip, so excluding it
leaves the pace table as it was.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from moto_copilot.contracts import validate_dataset, validate_derived_segments, validate_public_private_pair
from moto_copilot.ingest import IngestParams, build_rows, moving_path, read_gpx, to_public
from moto_copilot.pace import build_pace_table, compare_methods, compute_eta
from moto_copilot.routes import align_to_route, build_route, common_stretch

TAIPEI = dt.timezone(dt.timedelta(hours=8))
# Trips are numbered T001.. in file-name order (which is date order). Groups were found by
# comparing trimmed tracks; each list is in date order.
DEMO_GROUPS = {"R01": ["T001", "T002", "T007"], "R02": ["T009", "T014"]}
EXCLUDED = {  # trip -> reason; recorded in the private trip inventory
    "T010": "Excluded by the rider 2026-11-14. Its demo route (the T008/T010 stretch) was dropped in the M1 Review "
            "as a flat, straight, high-speed transit road. Not used in any pace table; not evaluation data. "
            "Its ride times were never read.",
}
MIN_SEGMENTS = 30
MARGIN_COEFF = 0.2  # provisional; the value is set after E1 Lite (DESIGN.md §6.1)
PLANNING_DEPARTURE = dt.datetime(2026, 11, 21, 7, 0, tzinfo=TAIPEI)  # an arbitrary future departure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gpx-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    now = dt.datetime.now(TAIPEI)

    files = sorted(args.gpx_dir.glob("*.gpx"))
    trip_file = {f"T{i + 1:03d}": f for i, f in enumerate(files)}
    holdout = {group[-1] for group in DEMO_GROUPS.values()}
    route_of = {trip: route for route, group in DEMO_GROUPS.items() for trip in group}
    manifest = []
    for t, f in trip_file.items():
        if t in EXCLUDED:
            manifest.append({"trip_id": t, "source_file": f.name, "inventory_status": "excluded", "trip_role": None,
                             "route_id": None, "exclusion_reason": EXCLUDED[t]})
        else:
            manifest.append({"trip_id": t, "source_file": f.name, "inventory_status": "included",
                             "trip_role": "holdout" if t in holdout else "pace", "route_id": route_of.get(t),
                             "role_status": "assigned by rule 2026-11-14; accepted in the M1 Review"})
    included = [trip for trip in manifest if trip["inventory_status"] == "included"]
    points = {trip["trip_id"]: read_gpx(trip_file[trip["trip_id"]])[0] for trip in included}

    def ingest(params: IngestParams) -> list[dict]:
        rows: list[dict] = []
        for trip in included:
            trip_rows, _ = build_rows(points[trip["trip_id"]], trip_id=trip["trip_id"], trip_role=trip["trip_role"],
                                      route_id=trip["route_id"], params=params)
            rows.extend(trip_rows)
        return rows

    # Category thresholds: terciles of curvature over ok rows of pace trips only.
    first_pass = ingest(IngestParams())
    curvature = sorted(r["curvature_deg_per_km"] for r in first_pass
                       if r["trip_role"] == "pace" and r["quality"] == "ok" and r["curvature_deg_per_km"] is not None)
    c1_max = float(round(curvature[len(curvature) // 3] / 5) * 5)
    c2_max = float(round(curvature[2 * len(curvature) // 3] / 5) * 5)
    params = IngestParams(c1_max_deg_per_km=c1_max, c2_max_deg_per_km=c2_max)
    private_rows = ingest(params)
    public_rows = to_public(private_rows)

    # Route catalog from the private trimmed tracks.
    catalog_version = "catalog-spike-0.2"
    routes, route_segments, checkpoints, route_notes, alignment = [], [], [], {}, {}
    for route_id, group in DEMO_GROUPS.items():
        paths = {t: moving_path(points[t], params) for t in group}
        source = group[0]
        start, end = common_stretch(paths[source], [paths[t] for t in group[1:]])
        route_path = paths[source][start:end]
        route, segs, cps = build_route(route_id, f"示範路線 {route_id}", route_path,
                                       source_trip_id=source, catalog_version=catalog_version, params=params)
        routes.append(route), route_segments.extend(segs), checkpoints.extend(cps)
        route_notes[route_id] = {"trips": group, "source": source, "holdout": group[-1]}
        # Geometry only: where each trip lies on the route. No timestamp is used.
        alignment[route_id] = {t: align_to_route(route_path, paths[t]) for t in group}

    # Pace table from pace trips only.
    trips_with_rows = {r["trip_id"] for r in private_rows}
    pace_trips = sorted(t["trip_id"] for t in included if t["trip_role"] == "pace" and t["trip_id"] in trips_with_rows)
    pace_header, pace_categories = build_pace_table(public_rows, pace_trips, pace_version="pace-spike-0.1",
                                                    min_segments=MIN_SEGMENTS, built_at=now)
    methods = compare_methods(public_rows, pace_trips)

    # One ETA per demo route, for a future departure. Not compared with any ride.
    eta_headers, eta_segments = [], []
    for route in routes:
        header, rows = compute_eta(route, route_segments, checkpoints, pace_header, pace_categories,
                                   plan_id=f"P-{route['route_id']}-0700", departure_time=PLANNING_DEPARTURE,
                                   margin_coeff=MARGIN_COEFF, breaks=[], computed_at=now)
        eta_headers.append(header), eta_segments.extend(rows)

    public_data = {"derived_segments": public_rows, "routes": routes, "route_segments": route_segments,
                   "checkpoints": checkpoints, "pace_header": pace_header, "pace_categories": pace_categories,
                   "eta_headers": eta_headers, "eta_segments": eta_segments}
    report = validate_dataset(public_data, "public")
    report["derived_segments_private"] = validate_derived_segments(private_rows, "private")
    report["public_private_pair"] = validate_public_private_pair(public_rows, private_rows)

    args.out.mkdir(parents=True, exist_ok=True)
    dump = lambda name, obj: (args.out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    dump("trip_manifest.json", {"note": "PRIVATE. Never commit.", "trips": manifest})
    dump("derived_segments_private.json", {"derived_segments": private_rows})
    dump("contract_dataset.json", public_data)
    dump("m1b_report.json", {"params": {"c1_max": c1_max, "c2_max": c2_max, "min_segments": MIN_SEGMENTS,
                                        "margin_coeff": MARGIN_COEFF, "ingest_version": params.ingest_version},
                             "routes": route_notes, "method_comparison": methods, "contract_violations": report})
    dump("route_alignment.json", {"note": "PRIVATE. Geometry only. trip_index_range indexes the trip's moving path; "
                                          "an Oracle may time only this stretch, never the whole trip.",
                                  "alignment": alignment})

    print(f"ingest {params.ingest_version} | scheme {params.category_scheme} (terciles of pace-trip curvature, n={len(curvature)})")
    print(f"trips {len(manifest)} | pace {len(pace_trips)} | holdout {sorted(holdout)} | excluded {sorted(EXCLUDED)} "
          f"| rows {len(private_rows)}")
    print("\nroute  trips (source first, holdout last)   km   segs  C1/C2/C3")
    for route in routes:
        segs = [s for s in route_segments if s["route_id"] == route["route_id"]]
        mix = "/".join(str(sum(1 for s in segs if s["seg_category"] == c)) for c in ("C1", "C2", "C3"))
        print(f"{route['route_id']}    {', '.join(route_notes[route['route_id']]['trips']):36} {route['total_length_m'] / 1000:5.1f} {len(segs):5d}  {mix}")
    print("\nalignment to the route (geometry only)  coverage  same-direction  length ratio  deviation median/p95 m")
    for route_id, per_trip in alignment.items():
        for trip_id, a in per_trip.items():
            role = "holdout" if trip_id in holdout else "pace"
            print(f"{route_id} {trip_id} {role:8}                      {a['coverage']:7.3f}  {str(a['same_direction']):14}  "
                  f"{a['length_ratio']:12.3f}  {a['deviation_median_m']:5.1f} / {a['deviation_p95_m']:5.1f}")
    print(f"\npace table {pace_header['pace_version']} | method {pace_header['method']} | min_segments {MIN_SEGMENTS}")
    print("category  n_segments  speed_kmh  length-weighted (comparison only)")
    for c in pace_categories:
        m = methods.get(c["seg_category"], {})
        print(f"{c['seg_category']:8}  {c['n_segments']:10d}  {str(c['speed_kmh']):>9}  {m.get('median_length_weighted')}")
    print(f"\nETA (planning output, margin_coeff {MARGIN_COEFF} is provisional; not compared with any ride)")
    for header in eta_headers:
        rows = [r for r in eta_segments if r["plan_id"] == header["plan_id"]]
        if header["status"] == "ok":
            typical = sum(r["typ_seg_time_s"] for r in rows)
            print(f"{header['plan_id']}: ok | typical {typical / 60:5.1f} min | conservative {typical * (1 + MARGIN_COEFF) / 60:5.1f} min")
        else:
            print(f"{header['plan_id']}: unknown | {header['unknown_reason']}")
    print()
    for name, found in report.items():
        print(f"contract check {name}: {'OK' if not found else f'{len(found)} violation(s)'}")
        for message in found[:8]:
            print(f"  - {message}")
    return 0 if not any(report.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
