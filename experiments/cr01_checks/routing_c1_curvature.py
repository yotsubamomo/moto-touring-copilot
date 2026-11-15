"""CR-01 check C1: does routing-engine geometry give the same typical time as GPS geometry?

    PYTHONPATH=src python experiments/cr01_checks/routing_c1_curvature.py [--plan-only]

Only pace trips of data/private/cr01/holdout_designation.json are read (never a holdout or an
excluded trip). No point of any track is sent anywhere: which public landmarks a pace trip passed
is worked out locally, and the only request is a route between two public landmarks.

Method (all of it fixed before any result was seen):
  * thresholds = terciles of curvature over the ok rows of pace trips (as in the M1-B spike),
    one pace table from the same trips (median, min_segments 30)
  * a pace trip "passes" a landmark when its trimmed moving path comes within PASS_M of it
  * candidate stretch = two landmarks passed one after the other by one trip, at least MIN_KM of
    track apart (the nearest later landmark that reaches MIN_KM), no landmark visited twice between
  * stretches are ranked by the number of pace trips that rode them, then by length; a stretch
    that shares more than 30% of its road with one already chosen is skipped; at most MAX_STRETCHES
  * GPS geometry = the moving path of the lowest-numbered trip between the two closest-approach
    points; routing geometry = the public-server route between the two landmarks
  * both are cut to their common extent (the route may start on a side street at the landmark),
    then each goes through build_route and compute_eta with the same thresholds and pace table
  * a stretch is valid when the route follows the ridden road: at least VALID_OVERLAP of each
    geometry lies within the catalog's matching tolerance of the other, in the same direction,
    and the common extent is still at least MIN_KM long

Pass condition (fixed): at least two valid stretches, each with |T_routing - T_gps| / T_gps <= 5%.
Prints P1, P2, ... and aggregates only. Names and trip ids stay in data/private/cr01/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys

from moto_copilot.ingest import IngestParams, TrackPoint, build_rows, haversine_m, moving_path, read_gpx, to_public
from moto_copilot.pace import build_pace_table, compute_eta
from moto_copilot.routes import align_to_route, build_route

from routing_client import PRIVATE, ROOT, Stopped, counts, decode6, route_body, valhalla

PASS_M = 300.0
MIN_KM = 15.0
MAX_STRETCHES = 4
MAX_ROUTE_REQUESTS = 6
VALID_OVERLAP = 0.95
MIN_SEGMENTS = 30
TAIPEI = dt.timezone(dt.timedelta(hours=8))
T0 = dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc)
CATS = ("C1", "C2", "C3")


def load_pace_trips() -> dict[str, list[TrackPoint]]:
    designation = json.loads((PRIVATE / "holdout_designation.json").read_text(encoding="utf-8"))
    forbidden = set(designation["holdout"]) | set(designation["excluded_pending_ruling"])
    manifest = json.loads((ROOT / "data" / "private" / "m1b" / "trip_manifest.json").read_text(encoding="utf-8"))["trips"]
    files = {t["trip_id"]: t["source_file"] for t in manifest}
    points = {}
    for trip_id in sorted(designation["pace"]):
        if trip_id in forbidden:
            raise RuntimeError("a pace trip is also listed as holdout or excluded")
        points[trip_id] = read_gpx(ROOT / "data" / "bmw" / files[trip_id])[0]
    return points


def thresholds_and_pace(points: dict[str, list[TrackPoint]], base: IngestParams = IngestParams()):
    def ingest(params):
        rows = []
        for trip_id, pts in points.items():
            rows.extend(build_rows(pts, trip_id=trip_id, trip_role="pace", route_id=None, params=params)[0])
        return rows
    curvature = sorted(r["curvature_deg_per_km"] for r in ingest(base)
                       if r["quality"] == "ok" and r["curvature_deg_per_km"] is not None)
    c1_max = float(round(curvature[len(curvature) // 3] / 5) * 5)
    c2_max = float(round(curvature[2 * len(curvature) // 3] / 5) * 5)
    params = IngestParams(c1_max_deg_per_km=c1_max, c2_max_deg_per_km=c2_max, resample_m=base.resample_m)
    rows = to_public(ingest(params))
    trips = sorted({r["trip_id"] for r in rows})
    header, categories = build_pace_table(rows, trips, pace_version="pace-cr01-check", min_segments=MIN_SEGMENTS,
                                          built_at=dt.datetime.now(TAIPEI))
    return params, header, categories, len(curvature)


def cumulative(path: list[TrackPoint]) -> list[float]:
    out = [0.0]
    for a, b in zip(path, path[1:]):
        out.append(out[-1] + haversine_m(a.lat, a.lon, b.lat, b.lon))
    return out


def passes(path: list[TrackPoint], cum: list[float], landmarks: list[dict]) -> list[dict]:
    """Every time the path comes within PASS_M of a landmark: the index of closest approach."""
    found = []
    for lm in landmarks:
        k = math.cos(math.radians(lm["lat"])) * 111_320.0
        run, last_i = None, None
        for i, p in enumerate(path):
            if abs(p.lat - lm["lat"]) > 0.004 or abs(p.lon - lm["lon"]) > 0.004:
                d = None
            else:
                d = math.hypot((p.lat - lm["lat"]) * 110_540.0, (p.lon - lm["lon"]) * k)
            if d is not None and d <= PASS_M:
                if run is not None and cum[i] - cum[last_i] > 2000.0:   # a separate visit
                    found.append(run)
                    run = None
                if run is None or d < run["d"]:
                    run = {"name": lm["name"], "index": i, "d": d} if run is None else {**run, "index": i, "d": d}
                last_i = i
        if run is not None:
            found.append(run)
    return sorted(found, key=lambda r: r["index"])


def candidates(paths: dict[str, list[TrackPoint]], landmarks: list[dict]) -> tuple[dict, dict]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    seen: dict[str, int] = {}
    for trip_id, path in paths.items():
        if len(path) < 2:
            continue
        cum = cumulative(path)
        visits = passes(path, cum, landmarks)
        for name in {v["name"] for v in visits}:
            seen[name] = seen.get(name, 0) + 1
        for i, a in enumerate(visits):
            names = {a["name"]}
            for b in visits[i + 1:]:
                if b["name"] in names:
                    break
                names.add(b["name"])
                if cum[b["index"]] - cum[a["index"]] >= MIN_KM * 1000:
                    grouped.setdefault((a["name"], b["name"]), []).append(
                        {"trip_id": trip_id, "start": a["index"], "end": b["index"],
                         "km": (cum[b["index"]] - cum[a["index"]]) / 1000, "via": len(names) - 2})
                    break
    return grouped, seen


def as_path(points: list[tuple[float, float]]) -> list[TrackPoint]:
    return [TrackPoint(lat, lon, T0) for lat, lon in points]   # build_route never reads .time


def nearest_index(path: list[TrackPoint], target: TrackPoint) -> int:
    return min(range(len(path)), key=lambda i: haversine_m(path[i].lat, path[i].lon, target.lat, target.lon))


def common_extent(route: list[TrackPoint], gps: list[TrackPoint]) -> tuple[list[TrackPoint], list[TrackPoint]]:
    """Cut both paths to the part between the same two places on the road."""
    r0, r1 = nearest_index(route, gps[0]), nearest_index(route, gps[-1])
    route = route[r0:r1 + 1] if r1 > r0 else route
    g0, g1 = nearest_index(gps, route[0]), nearest_index(gps, route[-1])
    gps = gps[g0:g1 + 1] if g1 > g0 else gps
    return route, gps


def length_m(path: list[TrackPoint]) -> float:
    return sum(haversine_m(a.lat, a.lon, b.lat, b.lon) for a, b in zip(path, path[1:]))


def typical(path: list[TrackPoint], params: IngestParams, header: dict, categories: list[dict]) -> dict:
    route, segs, cps = build_route("R90", "check", path, source_trip_id="T000", catalog_version="cr01-check", params=params)
    eta_header, rows = compute_eta(route, segs, cps, header, categories, plan_id="P-check",
                                   departure_time=dt.datetime(2027, 1, 2, 7, 0, tzinfo=TAIPEI), margin_coeff=0.0,
                                   breaks=[], computed_at=dt.datetime.now(TAIPEI))
    total = route["total_length_m"]
    share = {c: sum(s["length_m"] for s in segs if s["seg_category"] == c) / total for c in CATS}
    seconds = sum(r["typ_seg_time_s"] for r in rows) if eta_header["status"] == "ok" else None
    return {"km": total / 1000, "share": share, "typical_s": seconds, "status": eta_header["status"], "segments": len(segs)}


def overlap(a: list[TrackPoint], b: list[TrackPoint]) -> float:
    """Share of path a (sampled every 100 m) that lies on path b, by the catalog's own matcher."""
    return align_to_route(a, b)["coverage"]


def douglas_peucker(path: list[TrackPoint], tolerance_m: float) -> list[TrackPoint]:
    if len(path) < 3:
        return path
    lat0 = math.radians(path[0].lat)
    xy = [(math.radians(p.lon) * 6_371_000.0 * math.cos(lat0), math.radians(p.lat) * 6_371_000.0) for p in path]
    keep = [False] * len(path)
    keep[0] = keep[-1] = True
    stack = [(0, len(path) - 1)]
    while stack:
        i, j = stack.pop()
        (x0, y0), (x1, y1) = xy[i], xy[j]
        dx, dy = x1 - x0, y1 - y0
        norm = math.hypot(dx, dy)
        worst, at = 0.0, None
        for k in range(i + 1, j):
            x, y = xy[k]
            d = abs(dy * (x - x0) - dx * (y - y0)) / norm if norm else math.hypot(x - x0, y - y0)
            if d > worst:
                worst, at = d, k
        if at is not None and worst > tolerance_m:
            keep[at] = True
            stack.extend([(i, at), (at, j)])
    return [p for p, k in zip(path, keep) if k]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan-only", action="store_true", help="local work only; send no request")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    points = load_pace_trips()
    params, header, categories, n_curv = thresholds_and_pace(points)
    speed = {c["seg_category"]: c["speed_kmh"] for c in categories}
    print(f"pace trips {len(points)} | thresholds {params.c1_max_deg_per_km:g}/{params.c2_max_deg_per_km:g} deg/km "
          f"(terciles, n={n_curv}) | pace km/h {speed} | n_segments "
          f"{ {c['seg_category']: c['n_segments'] for c in categories} }")

    landmarks = [l for l in json.loads((PRIVATE / "routing_landmarks_c1.json").read_text(encoding="utf-8"))["landmarks"]
                 if l.get("resolved")]
    paths = {trip_id: moving_path(pts, params) for trip_id, pts in points.items()}
    grouped, seen = candidates(paths, landmarks)
    ranked = sorted(grouped.items(), key=lambda kv: (-len({r["trip_id"] for r in kv[1]}), -max(r["km"] for r in kv[1]), kv[0]))
    print(f"landmarks geocoded {len(landmarks)} | passed by at least one pace trip {len(seen)} | "
          f"candidate stretches (directed landmark pairs, >= {MIN_KM:g} km) {len(ranked)}")
    print("candidate lengths km:", sorted(round(max(r["km"] for r in rides), 1) for _, rides in ranked))
    if args.plan_only:
        return 0

    lm = {l["name"]: l for l in landmarks}
    chosen, private, requests_made = [], [], 0
    for (name_a, name_b), rides in ranked:
        if len(chosen) >= MAX_STRETCHES or requests_made >= MAX_ROUTE_REQUESTS:
            break
        ride = min(rides, key=lambda r: r["trip_id"])
        gps_raw = paths[ride["trip_id"]][ride["start"]:ride["end"] + 1]
        if any(max(overlap(gps_raw, other), overlap(gps_raw, list(reversed(other)))) > 0.30 for other in chosen):
            continue
        try:
            record = valhalla("route", route_body([lm[name_a], lm[name_b]]))
        except Stopped as stop:
            print(f"STOPPED: {stop}")
            return 2
        requests_made += 1
        entry = {"from": name_a, "to": name_b, "trip_id": ride["trip_id"], "n_pace_trips": len({r["trip_id"] for r in rides}),
                 "http_status": record["status"], "response_date": record["fetched_at"]}
        if record["status"] != 200:
            entry["error"] = record["body"]
            private.append(entry)
            continue
        trip = record["body"]["trip"]
        route_raw = as_path(decode6(trip["legs"][0]["shape"]))
        route_cut, gps_cut = common_extent(route_raw, gps_raw)
        forward = align_to_route(route_cut, gps_cut)
        entry.update({
            "engine_km": trip["summary"]["length"], "has_highway": trip["summary"]["has_highway"],
            "raw_km": {"gps": length_m(gps_raw) / 1000, "routing": length_m(route_raw) / 1000},
            "overlap_route_on_gps": forward["coverage"], "overlap_gps_on_route": overlap(gps_cut, route_cut),
            "same_direction": forward["same_direction"], "deviation_median_m": forward.get("deviation_median_m"),
            "deviation_p95_m": forward.get("deviation_p95_m"),
            "gps": typical(gps_cut, params, header, categories), "routing": typical(route_cut, params, header, categories),
            "gps_uncut": typical(gps_raw, params, header, categories), "routing_uncut": typical(route_raw, params, header, categories),
        })
        entry["valid"] = (entry["overlap_route_on_gps"] >= VALID_OVERLAP and entry["overlap_gps_on_route"] >= VALID_OVERLAP
                          and entry["same_direction"] and min(entry["gps"]["km"], entry["routing"]["km"]) >= MIN_KM
                          and entry["gps"]["typical_s"] is not None and entry["routing"]["typical_s"] is not None)
        if entry["valid"]:
            entry["diff"] = (entry["routing"]["typical_s"] - entry["gps"]["typical_s"]) / entry["gps"]["typical_s"]
            entry["diff_uncut"] = ((entry["routing_uncut"]["typical_s"] - entry["gps_uncut"]["typical_s"])
                                   / entry["gps_uncut"]["typical_s"])
            chosen.append(gps_raw)
            # Exploratory only: the same simplification on both geometries, thresholds and table unchanged.
            entry["exploratory"] = {}
            for label, spacing, tol in (("resample 40 m", 40.0, None), ("resample 60 m", 60.0, None),
                                        ("resample 100 m", 100.0, None), ("DP 3 m", 20.0, 3.0), ("DP 5 m", 20.0, 5.0),
                                        ("DP 10 m", 20.0, 10.0)):
                p2 = IngestParams(c1_max_deg_per_km=params.c1_max_deg_per_km, c2_max_deg_per_km=params.c2_max_deg_per_km,
                                  resample_m=spacing)
                g, r = (gps_cut, route_cut) if tol is None else (douglas_peucker(gps_cut, tol), douglas_peucker(route_cut, tol))
                tg, tr = typical(g, p2, header, categories), typical(r, p2, header, categories)
                entry["exploratory"][label] = {"gps": tg, "routing": tr,
                                               "diff": (tr["typical_s"] - tg["typical_s"]) / tg["typical_s"]}
        private.append(entry)

    valid = [e for e in private if e.get("valid")]
    for i, e in enumerate(valid, 1):
        e["label"] = f"P{i}"
    (PRIVATE / "routing_c1_private.json").write_text(json.dumps(
        {"note": "PRIVATE. Names of ridden stretches and trip ids. Never commit.",
         "thresholds": [params.c1_max_deg_per_km, params.c2_max_deg_per_km], "pace_kmh": speed,
         "stretches": private}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    pct = lambda share: "/".join(f"{share[c] * 100:.0f}" for c in CATS)
    print(f"\nroute requests for C1: {requests_made} | valid stretches {len(valid)} | "
          f"rejected (engine chose another road or error) {len(private) - len(valid)}")
    for e in private:
        if not e.get("valid") and "gps" in e:
            print(f"  rejected: overlap route-on-gps {e['overlap_route_on_gps']:.3f}, gps-on-route {e['overlap_gps_on_route']:.3f}, "
                  f"same direction {e['same_direction']}, common km {min(e['gps']['km'], e['routing']['km']):.1f}")
    print("\nstretch  trips  km gps/routing   C1/C2/C3 % gps   C1/C2/C3 % routing   T min gps/routing    diff %   overlap r/g   dev med/p95 m   (uncut: km gps/routing, diff %)")
    for e in valid:
        print(f"{e['label']:7}  {e['n_pace_trips']:5d}  {e['gps']['km']:5.1f} / {e['routing']['km']:5.1f}   {pct(e['gps']['share']):16} "
              f"{pct(e['routing']['share']):20} {e['gps']['typical_s'] / 60:6.1f} / {e['routing']['typical_s'] / 60:6.1f}   "
              f"{e['diff'] * 100:+6.2f}   {e['overlap_route_on_gps']:.3f}/{e['overlap_gps_on_route']:.3f}   "
              f"{e['deviation_median_m']:.1f}/{e['deviation_p95_m']:.1f}   "
              f"({e['raw_km']['gps']:.1f} / {e['raw_km']['routing']:.1f}, {e['diff_uncut'] * 100:+.2f})")
    passed = len(valid) >= 2 and all(abs(e["diff"]) <= 0.05 for e in valid)
    print(f"\nC1 verdict: {'PASS' if passed else 'FAIL'} ({len(valid)} valid stretches; max |diff| "
          f"{max((abs(e['diff']) for e in valid), default=float('nan')) * 100:.2f}%)")
    print("\nexploratory (not a pass condition): same simplification on both geometries; thresholds and pace table unchanged")
    print("variant          " + "   ".join(f"{e['label']} diff %  gps C1/C2/C3  routing C1/C2/C3" for e in valid))
    for label in (valid[0]["exploratory"] if valid else {}):
        print(f"{label:15}  " + "   ".join(
            f"{e['exploratory'][label]['diff'] * 100:+6.2f}     {pct(e['exploratory'][label]['gps']['share']):12}  "
            f"{pct(e['exploratory'][label]['routing']['share']):16}" for e in valid))
    print(f"\nrequests so far: {counts()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
