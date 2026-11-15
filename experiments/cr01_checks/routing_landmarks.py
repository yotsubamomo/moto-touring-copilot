"""CR-01 routing checks: geocode the public landmarks used by checks C4 and C1.

Both lists were written before any ride data was looked at:
  * REFERENCE_ROUTES: five well-known public mountain routes (start and turnaround landmark)
  * CANDIDATES: public landmarks on well-known mountain roads all over Taiwan, used by C1 to find
    stretches a pace trip rode (that test is done locally, never by a request)

Each name is sent to Nominatim once (cached). `near` is a rough expected position, used only to
reject a homonym somewhere else; the stored position is the one Nominatim returned.

    PYTHONPATH=src python experiments/cr01_checks/routing_landmarks.py
"""
from __future__ import annotations

import json
import sys

from routing_client import PRIVATE, Stopped, counts, geocode

REFERENCE_ROUTES = [  # (route id, public name, start landmark, turnaround landmark)
    ("REF1", "陽金公路：陽明山 ↔ 金山", "中國文化大學", "金山區公所"),
    ("REF2", "中橫西段：東勢 ↔ 谷關", "東勢區公所", "谷關"),
    ("REF3", "北宜公路：新店 ↔ 頭城", "新店區公所", "頭城車站"),
    ("REF4", "台14／台14甲：埔里 ↔ 武嶺", "埔里酒廠", "武嶺"),
    ("REF5", "阿里山公路：嘉義 ↔ 阿里山", "嘉義車站", "阿里山車站"),
]
NEAR = {  # rough expected position (lat, lon); a result further than 0.1 degree away is rejected
    "陽明山國家公園遊客中心": (25.155, 121.547), "金山區公所": (25.222, 121.636),
    "東勢區公所": (24.259, 120.828), "谷關遊客中心": (24.203, 121.005),
    "新店區公所": (24.967, 121.541), "頭城車站": (24.859, 121.822),
    "埔里酒廠": (23.967, 120.960), "武嶺": (24.137, 121.276),
    "嘉義車站": (23.479, 120.441), "阿里山車站": (23.510, 120.803),
    # Replacements after the first geocoding pass (still before any ride data was read): the first
    # name gave no result, the second resolved to a visitor centre up a side road outside the village.
    "中國文化大學": (25.136, 121.540), "谷關": (24.203, 121.005),
}
# The C1 candidate landmarks are not kept in version control: together with stretch lengths they
# could hint at which roads were ridden. They live in data/private/cr01/ (same list as used on
# 2026-11-15, written before any ride data was read).
_C1_FILE = PRIVATE / "routing_c1_candidates.json"
if _C1_FILE.exists():
    NEAR.update({name: tuple(pos) for name, pos in json.loads(_C1_FILE.read_text(encoding="utf-8"))["near"].items()})
C4_NAMES = [name for route in REFERENCE_ROUTES for name in route[2:]]
CANDIDATES = [name for name in NEAR if name not in C4_NAMES]


def resolve(name: str) -> dict:
    record = geocode(name)
    lat0, lon0 = NEAR[name]
    for hit in record["body"] if isinstance(record["body"], list) else []:
        lat, lon = float(hit["lat"]), float(hit["lon"])
        if abs(lat - lat0) <= 0.1 and abs(lon - lon0) <= 0.1:
            return {"name": name, "lat": lat, "lon": lon, "osm_type": hit.get("osm_type"), "osm_id": hit.get("osm_id"),
                    "category": hit.get("category"), "type": hit.get("type"), "display_name": hit.get("display_name"),
                    "geocoded_at": record["fetched_at"], "resolved": True}
    return {"name": name, "resolved": False, "n_results": len(record["body"]) if isinstance(record["body"], list) else 0,
            "geocoded_at": record["fetched_at"]}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        c4 = [resolve(name) for name in C4_NAMES]
        c1 = [resolve(name) for name in CANDIDATES]
    except Stopped as stop:
        print(f"STOPPED: {stop}")
        return 2
    dump = lambda name, obj: (PRIVATE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    dump("routing_landmarks_c4.json", {"note": "Public landmarks of the five reference routes.",
                                       "routes": [{"route_id": r[0], "name": r[1], "start": r[2], "turnaround": r[3]}
                                                  for r in REFERENCE_ROUTES], "landmarks": c4})
    dump("routing_landmarks_c1.json", {"note": "PRIVATE once combined with ride data. Generic candidate list.",
                                       "landmarks": c1 + c4})
    print(f"C4 landmarks resolved {sum(l['resolved'] for l in c4)}/{len(c4)}; unresolved: "
          f"{[l['name'] for l in c4 if not l['resolved']]}")
    print(f"C1 candidates resolved {sum(l['resolved'] for l in c1)}/{len(c1)} (names not printed)")
    print(f"requests so far: {counts()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
