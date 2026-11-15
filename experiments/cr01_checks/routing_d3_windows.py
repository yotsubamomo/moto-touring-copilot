"""CR-01 data for decision D3: how large are the candidate ranges of weather rule 3 on a round trip?

    PYTHONPATH=src python experiments/cr01_checks/routing_d3_windows.py

Reads the five reference snapshots of check C4 (no request is sent, no ride data is read except
the two curvature thresholds that check C1 derived from pace trips). For each round trip
(outbound + return) it measures, in km and as a share of the whole trip:
  * the last 20% of the trip by distance (the current rule)
  * the whole return leg
  * return-leg segments of category C2 or C3, and C3 alone
  * return-leg segments whose mean elevation is at least 500 m / 1000 m
  * the block from the turnaround to the end of the last return-leg segment at or above 500 m
and how much of the last-20% window each "mountain" definition covers, and in how many separate
runs each definition falls. It gives data only; it makes no recommendation.
"""
from __future__ import annotations

import datetime as dt
import json
import sys

from moto_copilot.ingest import IngestParams, TrackPoint
from moto_copilot.routes import build_route

from routing_client import PRIVATE, decode6

T0 = dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc)
LEVELS = (500.0, 1000.0)


def leg_segments(leg: dict, params: IngestParams) -> list[dict]:
    path = [TrackPoint(lat, lon, T0) for lat, lon in decode6(leg["shape"])]
    _, segs, _ = build_route("R90", "check", path, source_trip_id="T000", catalog_version="cr01-check", params=params)
    total, elevation = segs[-1]["cum_length_m"], leg.get("elevation") or []
    for seg in segs:
        start, end = seg["cum_length_m"] - seg["length_m"], seg["cum_length_m"]
        if elevation:   # samples are evenly spaced along the leg
            n = len(elevation) - 1
            inside = [e for i, e in enumerate(elevation) if start <= i / n * total <= end]
            seg["mean_elev_m"] = sum(inside) / len(inside) if inside else None
        seg["start_m"], seg["end_m"] = start, end
    return segs


def measure(segs: list[dict], member, window_start_m: float) -> dict:
    """km of the member segments, km of them inside [window_start, end], number of separate runs."""
    km = sum(s["length_m"] for s in segs if member(s)) / 1000
    in_window = sum(max(0.0, s["end_m"] - max(s["start_m"], window_start_m)) for s in segs if member(s)) / 1000
    runs = sum(1 for i, s in enumerate(segs) if member(s) and (i == 0 or not member(segs[i - 1])))
    return {"km": km, "km_in_last20": in_window, "runs": runs}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    c1_max, c2_max = json.loads((PRIVATE / "routing_c1_private.json").read_text(encoding="utf-8"))["thresholds"]
    params = IngestParams(c1_max_deg_per_km=c1_max, c2_max_deg_per_km=c2_max)
    definitions = ["C2+C3", "C3", "elev>=500", "elev>=1000", "block to last >=500"]
    rows = []
    for path in sorted((PRIVATE / "snapshots").glob("REF*.json")):
        snap = json.loads(path.read_text(encoding="utf-8"))
        out, ret = leg_segments(snap["legs"]["outbound"], params), leg_segments(snap["legs"]["return"], params)
        out_m, ret_m = out[-1]["cum_length_m"], ret[-1]["cum_length_m"]
        trip_m = out_m + ret_m
        window_m = 0.2 * trip_m
        window_start = ret_m - window_m               # measured along the return leg
        high = [i for i, s in enumerate(ret) if (s.get("mean_elev_m") or 0) >= 500.0]
        members = {
            "C2+C3": lambda s: s["seg_category"] in ("C2", "C3"),
            "C3": lambda s: s["seg_category"] == "C3",
            "elev>=500": lambda s: (s.get("mean_elev_m") or 0) >= 500.0,
            "elev>=1000": lambda s: (s.get("mean_elev_m") or 0) >= 1000.0,
            "block to last >=500": lambda s: bool(high) and s["seg_index"] <= ret[high[-1]]["seg_index"],
        }
        elev = [e for leg in ("outbound", "return") for e in (snap["legs"][leg].get("elevation") or [])]
        rows.append({"route_id": snap["route_id"], "name": snap["name"], "trip_km": trip_m / 1000, "return_km": ret_m / 1000,
                     "last20_km": window_m / 1000, "max_elev_m": max(elev) if elev else None,
                     "min_elev_m": min(elev) if elev else None,
                     "return_shares": {c: sum(s["length_m"] for s in ret if s["seg_category"] == c) / ret_m for c in ("C1", "C2", "C3")},
                     "defs": {name: measure(ret, member, window_start) for name, member in members.items()}})
    total = {"trip_km": sum(r["trip_km"] for r in rows), "return_km": sum(r["return_km"] for r in rows),
             "last20_km": sum(r["last20_km"] for r in rows),
             "defs": {d: {k: sum(r["defs"][d][k] for r in rows) for k in ("km", "km_in_last20", "runs")} for d in definitions}}
    (PRIVATE / "routing_d3_summary.json").write_text(json.dumps(
        {"thresholds_deg_per_km": [c1_max, c2_max], "levels_m": LEVELS, "routes": rows, "aggregate": total},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"thresholds {c1_max:g}/{c2_max:g} deg/km | km (share of whole trip) | [km inside the last-20% window = share of the window] | runs")
    header = "route      trip km  elev m      last 20%      whole return   " + "   ".join(f"{d:>27}" for d in definitions)
    print(header)
    for r in rows + [{"route_id": "ALL", **total, "min_elev_m": None, "max_elev_m": None}]:
        cells = []
        for d in definitions:
            m = r["defs"][d]
            cells.append(f"{m['km']:5.1f} ({m['km'] / r['trip_km'] * 100:4.1f}%) [{m['km_in_last20'] / r['last20_km'] * 100:3.0f}%] {m['runs']:2d}r")
        elev = f"{r['min_elev_m']:.0f}-{r['max_elev_m']:.0f}" if r.get("max_elev_m") is not None else "-"
        print(f"{r['route_id']:9} {r['trip_km']:7.1f}  {elev:10}  {r['last20_km']:5.1f} (20.0%)  {r['return_km']:5.1f} ({r['return_km'] / r['trip_km'] * 100:4.1f}%)   "
              + "   ".join(cells))
    print("\nreturn-leg category shares C1/C2/C3 %:",
          {r["route_id"]: "/".join(f"{r['return_shares'][c] * 100:.0f}" for c in ("C1", "C2", "C3")) for r in rows})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
