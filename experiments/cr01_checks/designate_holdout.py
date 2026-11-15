"""CR-01: apply the frozen holdout selection rule (docs/cr/CR-01-proposal-alignment.md §13).

Metadata only: reads the first track-point timestamp of each GPX file and nothing else.
Writes the designation to data/private/cr01/ (never committed) and prints aggregate counts.
It never prints trip ids, file names, dates or times.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "private" / "m1b" / "trip_manifest.json"
GPX_DIR = ROOT / "data" / "bmw"
OUT = ROOT / "data" / "private" / "cr01" / "holdout_designation.json"
RULE_ID = "CR-01 §13 (frozen 2026-11-15)"
TIME_RE = re.compile(rb"<trkpt\b.*?<time>([^<]+)</time>", re.S)


def first_timestamp(path: Path) -> str:
    """Return the first track-point time string. Reads only the head of the file."""
    with path.open("rb") as fh:
        head = fh.read(200_000)
    m = TIME_RE.search(head)
    if not m:
        raise ValueError("no track-point time in the head of a GPX file")
    return m.group(1).decode("ascii").strip()


def main() -> None:
    trips = json.loads(MANIFEST.read_text(encoding="utf-8"))["trips"]
    eligible = [t for t in trips if t["inventory_status"] == "included"]
    for t in eligible:
        t["_start"] = first_timestamp(GPX_DIR / t["source_file"])
    k = max(3, math.ceil(0.2 * len(eligible)))
    ordered = sorted(eligible, key=lambda t: (t["_start"], t["trip_id"]), reverse=True)
    holdout = ordered[:k]
    holdout_ids = sorted(t["trip_id"] for t in holdout)
    pace_ids = sorted(t["trip_id"] for t in ordered[k:])
    excluded_ids = sorted(t["trip_id"] for t in trips if t["inventory_status"] != "included")
    digest = hashlib.sha256(",".join(holdout_ids).encode()).hexdigest()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "rule": RULE_ID, "k": k, "holdout": holdout_ids, "pace": pace_ids,
        "excluded_pending_ruling": excluded_ids, "holdout_sha256": digest,
    }, indent=2), encoding="utf-8")

    prev = {t["trip_id"]: t["trip_role"] for t in trips}
    print(json.dumps({
        "trips_in_manifest": len(trips),
        "eligible": len(eligible),
        "excluded_pending_ruling": len(excluded_ids),
        "k": k,
        "holdout": len(holdout_ids),
        "pace": len(pace_ids),
        "holdout_previously_pace_in_spike": sum(1 for i in holdout_ids if prev[i] == "pace"),
        "holdout_previously_holdout": sum(1 for i in holdout_ids if prev[i] == "holdout"),
        "old_holdouts_now_pace": sum(1 for i in pace_ids if prev[i] == "holdout"),
        "holdout_sha256": digest,
    }, indent=2))


if __name__ == "__main__":
    main()
