"""Validate a JSON dataset against the data contracts v0.3.

    python -m moto_copilot.contracts DATASET.json            # public data
    python -m moto_copilot.contracts DATASET.json --private  # derived segments with start_time

The file holds any of these keys: derived_segments, routes, route_segments, checkpoints,
pace_header, pace_categories, eta_headers, eta_segments. Exit code 0 means no violation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import CONTRACT_VERSION, validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--private", action="store_true", help="derived segments are the private version")
    args = parser.parse_args()

    data = json.loads(args.dataset.read_text(encoding="utf-8"))
    report = validate_dataset(data, "private" if args.private else "public")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"data contracts v{CONTRACT_VERSION}: {args.dataset}")
    if not report:
        print("  no contract data found in this file")
        return 2
    total = 0
    for name, violations in report.items():
        total += len(violations)
        print(f"  {name}: {'OK' if not violations else f'{len(violations)} violation(s)'}")
        for message in violations:
            print(f"    - {message}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
