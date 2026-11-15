"""CR-01 check C4: route snapshots of five public reference round trips.

    PYTHONPATH=src python experiments/cr01_checks/routing_c4_snapshots.py

For each reference route the outbound and the return leg are requested as two separate routes
(motorcycle costing, exclude_highways true, elevation every 30 m). Each leg is checked for
national freeways in three independent ways: the engine's has_highway summary, the per-maneuver
highway flag, and the road classes and names of the edges under the returned shape
(trace_attributes on the route's own shape, never on a GPX). A warning that the exclusion was
ignored is recorded. Snapshots go to data/private/cr01/snapshots/.

Pass condition (fixed before the run): 5 of 5 routes with both legs free of freeways and no
ignored-exclusion warning.
"""
from __future__ import annotations

import json
import re
import sys

from moto_copilot.ingest import haversine_m

from routing_client import PRIVATE, Stopped, counts, decode6, route_body, valhalla

FREEWAY_NAME = re.compile(r"國道|高速公路|[Ff]reeway")
SNAPSHOTS = PRIVATE / "snapshots"
TRACE_ATTRIBUTES = ["edge.names", "edge.length", "edge.road_class", "edge.use"]


def leg_snapshot(origin: dict, destination: dict, *, exclude_highways: bool = True, trace: bool = True,
                 costing_extra: dict | None = None) -> dict:
    body = route_body([origin, destination], exclude_highways=exclude_highways)
    if costing_extra:
        body.setdefault("costing_options", {}).setdefault("motorcycle", {}).update(costing_extra)
    record = valhalla("route", body)
    snap = {"request": body, "http_status": record["status"], "response_date": record["fetched_at"]}
    if record["status"] != 200 or "trip" not in record["body"]:
        snap["error"] = record["body"]
        return snap
    trip = record["body"]["trip"]
    leg = trip["legs"][0]
    maneuvers = leg["maneuvers"]
    names: list[str] = []
    for m in maneuvers:
        for name in (m.get("begin_street_names") or []) + (m.get("street_names") or []):
            if name not in names:
                names.append(name)
    warnings = (trip.get("warnings") or []) + (record["body"].get("warnings") or [])
    points = decode6(leg["shape"])
    # How far the requested landmark is from where the route really starts and ends (the response
    # echoes the requested position, so the snap distance has to be measured on the shape).
    snap["start_offset_m"] = round(haversine_m(origin["lat"], origin["lon"], *points[0]), 1)
    snap["end_offset_m"] = round(haversine_m(destination["lat"], destination["lon"], *points[-1]), 1)
    snap.update({
        "summary": {k: trip["summary"].get(k) for k in ("length", "time", "has_highway", "has_toll", "has_ferry")},
        "shape": leg["shape"], "shape_points": len(decode6(leg["shape"])),
        "elevation_interval": leg.get("elevation_interval"), "elevation": leg.get("elevation"),
        "street_names": names,
        "maneuvers": [{"length": m["length"], "time": m["time"], "street_names": m.get("street_names"),
                       "highway": bool(m.get("highway")), "toll": bool(m.get("toll")),
                       "begin_shape_index": m["begin_shape_index"], "end_shape_index": m["end_shape_index"]} for m in maneuvers],
        "warnings": warnings,
        "snapped_end": trip["locations"][-1] if trip.get("locations") else None,
    })
    checks = {"has_highway": bool(trip["summary"].get("has_highway")),
              "highway_maneuvers": sum(1 for m in maneuvers if m.get("highway")),
              "highway_km_maneuvers": round(sum(m["length"] for m in maneuvers if m.get("highway")), 2),
              "freeway_names": [n for n in names if FREEWAY_NAME.search(n)],
              "exclusion_ignored_warning": any("exclu" in (w.get("text") or "").lower() for w in warnings)}
    if trace:
        traced = valhalla("trace_attributes", {
            "encoded_polyline": leg["shape"], "costing": "motorcycle", "shape_match": "walk_or_snap",
            "filters": {"attributes": TRACE_ATTRIBUTES, "action": "include"}})
        if traced["status"] == 200 and "edges" in traced["body"]:
            by_class: dict[str, float] = {}
            by_name: dict[str, float] = {}
            for edge in traced["body"]["edges"]:
                by_class[edge.get("road_class", "?")] = by_class.get(edge.get("road_class", "?"), 0.0) + edge.get("length", 0.0)
                for name in edge.get("names") or ["(unnamed)"]:
                    by_name[name] = by_name.get(name, 0.0) + edge.get("length", 0.0)
            snap["trace"] = {"road_class_km": {k: round(v, 2) for k, v in sorted(by_class.items(), key=lambda kv: -kv[1])},
                             "name_km": {k: round(v, 2) for k, v in sorted(by_name.items(), key=lambda kv: -kv[1])},
                             "edges": len(traced["body"]["edges"]), "warnings": traced["body"].get("warnings")}
            checks["motorway_km_trace"] = round(by_class.get("motorway", 0.0), 2)
            checks["freeway_names_trace"] = [n for n in by_name if FREEWAY_NAME.search(n)]
        else:
            snap["trace"] = {"error": traced["body"], "http_status": traced["status"]}
            checks["motorway_km_trace"] = None
    checks["freeway_free"] = (not checks["has_highway"] and checks["highway_maneuvers"] == 0 and not checks["freeway_names"]
                              and not checks.get("motorway_km_trace") and not checks.get("freeway_names_trace"))
    snap["checks"] = checks
    return snap


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    spec = json.loads((PRIVATE / "routing_landmarks_c4.json").read_text(encoding="utf-8"))
    landmark = {l["name"]: l for l in spec["landmarks"]}
    dump = lambda path, obj: path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    try:
        status = valhalla("status", {})
        engine = {"server": "public Valhalla (FOSSGIS)", "version": status["body"].get("version"),
                  "tileset_last_modified": status["body"].get("tileset_last_modified")}
        rows = []
        for route in spec["routes"]:
            start, turn = landmark[route["start"]], landmark[route["turnaround"]]
            legs = {"outbound": leg_snapshot(start, turn), "return": leg_snapshot(turn, start)}
            lengths = [legs[k]["summary"]["length"] for k in ("outbound", "return")]
            asym = abs(lengths[0] - lengths[1]) / (sum(lengths) / 2)
            ok = all(legs[k]["checks"]["freeway_free"] and not legs[k]["checks"]["exclusion_ignored_warning"] for k in legs)
            snapshot = {"route_id": route["route_id"], "name": route["name"], "start": route["start"],
                        "turnaround": route["turnaround"], "engine": engine, "legs": legs,
                        "length_asymmetry": round(asym, 4), "asymmetric_over_2pct": asym > 0.02, "c4_pass": ok}
            dump(SNAPSHOTS / f"{route['route_id']}.json", snapshot)
            rows.append(snapshot)

        # Server behaviour the product has to handle explicitly.
        ref3 = next(r for r in spec["routes"] if r["route_id"] == "REF3")
        taipei = {"lat": 25.0478, "lon": 121.5170}    # Taipei Main Station (public landmark, from memory)
        taichung = {"lat": 24.1369, "lon": 120.6850}  # Taichung Station
        kinmen = {"lat": 24.4337, "lon": 118.3186}    # Jincheng, Kinmen: an island with no road link
        yushan = {"lat": 23.4700, "lon": 120.9573}    # Yushan main peak: no road anywhere near
        chiayi = landmark["嘉義車站"]
        behaviour = {
            "no_exclusion_ref3_outbound": leg_snapshot(landmark[ref3["start"]], landmark[ref3["turnaround"]],
                                                       exclude_highways=False, trace=False),
            "intercity_with_exclusion": leg_snapshot(taipei, taichung, trace=False),
            "intercity_use_highways_0": leg_snapshot(taipei, taichung, exclude_highways=False, trace=False,
                                                     costing_extra={"use_highways": 0.0}),
            "ref3_outbound_use_highways_0": leg_snapshot(landmark[ref3["start"]], landmark[ref3["turnaround"]],
                                                         exclude_highways=False, trace=False,
                                                         costing_extra={"use_highways": 0.0}),
            "ref3_return_use_highways_0": leg_snapshot(landmark[ref3["turnaround"]], landmark[ref3["start"]],
                                                       exclude_highways=False, trace=False,
                                                       costing_extra={"use_highways": 0.0}),
            "impossible_island": leg_snapshot(chiayi, kinmen, trace=False),
            "peak_without_road": leg_snapshot(chiayi, yushan, trace=False),
        }
        dump(SNAPSHOTS / "behaviour_probes.json", {"engine": engine, "probes": behaviour})
    except Stopped as stop:
        print(f"STOPPED: {stop}")
        return 2

    summary = {"engine": engine, "routes": [], "behaviour": {}}
    print(f"engine {engine['version']} | tileset_last_modified {engine['tileset_last_modified']}")
    print("route  leg       km     min  has_hw  hw_man  motorway_km  freeway_names  excl_ignored  classes(km)")
    for r in rows:
        entry = {"route_id": r["route_id"], "name": r["name"], "asymmetry": r["length_asymmetry"],
                 "asymmetric_over_2pct": r["asymmetric_over_2pct"], "c4_pass": r["c4_pass"], "legs": {}}
        for key, leg in r["legs"].items():
            c, s = leg["checks"], leg["summary"]
            classes = leg.get("trace", {}).get("road_class_km")
            entry["legs"][key] = {"km": s["length"], "engine_min": round(s["time"] / 60, 1), **c, "road_class_km": classes,
                                  "main_names": list(leg.get("trace", {}).get("name_km", {}).items())[:6],
                                  "has_elevation": bool(leg.get("elevation")),
                                  "start_offset_m": leg["start_offset_m"], "end_offset_m": leg["end_offset_m"]}
            print(f"{r['route_id']}   {key:8} {s['length']:6.1f} {s['time'] / 60:6.1f}  {str(c['has_highway']):6}  {c['highway_maneuvers']:6d}  "
                  f"{str(c.get('motorway_km_trace')):11}  {str(c['freeway_names'] + c.get('freeway_names_trace', [])):13}  "
                  f"{str(c['exclusion_ignored_warning']):12}  {classes}")
        print(f"       asymmetry {r['length_asymmetry'] * 100:.2f}% (>2%: {r['asymmetric_over_2pct']}) | C4 pass: {r['c4_pass']}")
        summary["routes"].append(entry)
    print(f"\nC4: {sum(r['c4_pass'] for r in rows)} of {len(rows)} routes pass")
    print("\nbehaviour probes")
    for key, snap in behaviour.items():
        if "error" in snap:
            entry = {"http_status": snap["http_status"], "error": snap["error"]}
        else:
            c, s = snap["checks"], snap["summary"]
            entry = {"http_status": snap["http_status"], "km": s["length"], "engine_min": round(s["time"] / 60, 1),
                     "has_highway": c["has_highway"], "highway_km_maneuvers": c["highway_km_maneuvers"],
                     "freeway_names": c["freeway_names"], "warnings": snap["warnings"],
                     "end_offset_m": snap["end_offset_m"]}
        summary["behaviour"][key] = entry
        print(f"  {key}: {json.dumps(entry, ensure_ascii=False)}")
    dump(PRIVATE / "routing_c4_summary.json", summary)
    print(f"\nrequests so far: {counts()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
