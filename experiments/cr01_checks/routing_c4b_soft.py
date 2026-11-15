"""CR-01 check C4b: the five reference round trips with the soft highway preference.

    PYTHONPATH=src python experiments/cr01_checks/routing_c4b_soft.py

Same landmarks, legs and checks as routing_c4_snapshots.py, but the request carries
`use_highways: 0` and no `exclude_highways`. Requests identical to earlier ones come from the
disk cache. Snapshots go to data/private/cr01/snapshots_c4b/.

Pass condition (fixed before the run): on all five routes both legs have (i) no warning at all in
the route response, (ii) has_highway false and no maneuver flagged highway, (iii) 0 km of motorway
class and no national-freeway name among the street names (trace_attributes on the returned shape).

Recorded without affecting the verdict: distance and engine time against the C4 snapshot, whether
the shape is identical, and the km on trunk-class roads in each variant.
"""
from __future__ import annotations

import json
import sys

from routing_c4_snapshots import FREEWAY_NAME, leg_snapshot
from routing_client import PRIVATE, Stopped, counts, valhalla

OUT = PRIVATE / "snapshots_c4b"
SOFT = {"use_highways": 0.0}
EXPRESSWAY_NAME = ("台61線", "台64線", "台62線", "台66線", "台68線", "台72線", "台74線", "台76線", "台78線", "台82線",
                   "台84線", "台86線", "台88線")


def leg_passes(leg: dict) -> bool:
    c = leg["checks"]
    return (not leg["warnings"] and not c["has_highway"] and c["highway_maneuvers"] == 0
            and c.get("motorway_km_trace") == 0 and not c["freeway_names"] and not c.get("freeway_names_trace"))


def trunk_km(leg: dict) -> float | None:
    classes = leg.get("trace", {}).get("road_class_km")
    return None if classes is None else classes.get("trunk", 0.0)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    before = counts()["routing"]
    spec = json.loads((PRIVATE / "routing_landmarks_c4.json").read_text(encoding="utf-8"))
    landmark = {l["name"]: l for l in spec["landmarks"]}
    rows = []
    try:
        status = valhalla("status", {})   # cached: the same engine record as C4
        engine = {"server": "public Valhalla (FOSSGIS)", "version": status["body"].get("version"),
                  "tileset_last_modified": status["body"].get("tileset_last_modified")}
        for route in spec["routes"]:
            start, turn = landmark[route["start"]], landmark[route["turnaround"]]
            legs = {"outbound": leg_snapshot(start, turn, exclude_highways=False, costing_extra=SOFT),
                    "return": leg_snapshot(turn, start, exclude_highways=False, costing_extra=SOFT)}
            hard = json.loads((PRIVATE / "snapshots" / f"{route['route_id']}.json").read_text(encoding="utf-8"))["legs"]
            compare = {}
            for key, leg in legs.items():
                compare[key] = {"same_shape_as_c4": leg["shape"] == hard[key]["shape"],
                                "km": leg["summary"]["length"], "km_c4": hard[key]["summary"]["length"],
                                "min": round(leg["summary"]["time"] / 60, 1), "min_c4": round(hard[key]["summary"]["time"] / 60, 1),
                                "trunk_km": trunk_km(leg), "trunk_km_c4": trunk_km(hard[key])}
            lengths = [legs[k]["summary"]["length"] for k in ("outbound", "return")]
            asym = abs(lengths[0] - lengths[1]) / (sum(lengths) / 2)
            snapshot = {"route_id": route["route_id"], "name": route["name"], "start": route["start"],
                        "turnaround": route["turnaround"], "engine": engine, "variant": "use_highways 0, no exclude_highways",
                        "legs": legs, "compare_with_c4": compare, "length_asymmetry": round(asym, 4),
                        "c4b_pass": all(leg_passes(leg) for leg in legs.values())}
            (OUT / f"{route['route_id']}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            rows.append(snapshot)
    except Stopped as stop:
        print(f"STOPPED: {stop}")
        return 2

    print(f"engine {engine['version']} | new routing requests in this run: {counts()['routing'] - before}")
    print("route leg       km (C4)        min (C4)       same shape  warnings  has_hw  hw_man  motorway km  freeway names  trunk km (C4)  pass")
    for r in rows:
        for key, leg in r["legs"].items():
            c, x = leg["checks"], r["compare_with_c4"][key]
            print(f"{r['route_id']} {key:8} {x['km']:6.1f} ({x['km_c4']:5.1f})  {x['min']:6.1f} ({x['min_c4']:5.1f})  {str(x['same_shape_as_c4']):10}  "
                  f"{len(leg['warnings']):8d}  {str(c['has_highway']):6}  {c['highway_maneuvers']:6d}  {str(c.get('motorway_km_trace')):11}  "
                  f"{str(c['freeway_names'] + c.get('freeway_names_trace', [])):13}  {x['trunk_km']} ({x['trunk_km_c4']})  {leg_passes(leg)}"
                  f"  trace warnings {leg.get('trace', {}).get('warnings')}")
        print(f"     asymmetry {r['length_asymmetry'] * 100:.2f}% | C4b pass: {r['c4b_pass']}")
    print(f"\nC4b: {sum(r['c4b_pass'] for r in rows)} of {len(rows)} routes pass")

    # The flat intercity pair, from the cached probe responses only (no request): no road class is
    # available there, so expressway km is counted from maneuver street names.
    probes = json.loads((PRIVATE / "snapshots" / "behaviour_probes.json").read_text(encoding="utf-8"))["probes"]
    pair = {}
    for label, key in (("exclude_highways", "intercity_with_exclusion"), ("use_highways 0", "intercity_use_highways_0")):
        p = probes[key]
        named = sum(m["length"] for m in p["maneuvers"] if any(n in EXPRESSWAY_NAME for n in (m["street_names"] or [])))
        pair[label] = {"km": p["summary"]["length"], "min": round(p["summary"]["time"] / 60, 1),
                       "expressway_named_km_maneuvers": round(named, 1), "trunk_km_trace": None,
                       "freeway_names": [n for n in p["street_names"] if FREEWAY_NAME.search(n)]}
        print(f"flat pair, {label}: {pair[label]}")
    (PRIVATE / "routing_c4b_summary.json").write_text(json.dumps(
        {"engine": engine, "routes": [{"route_id": r["route_id"], "c4b_pass": r["c4b_pass"], "compare_with_c4": r["compare_with_c4"],
                                       "asymmetry": r["length_asymmetry"]} for r in rows],
         "flat_pair_from_cache": pair, "new_routing_requests": counts()["routing"] - before}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print(f"requests so far: {counts()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
