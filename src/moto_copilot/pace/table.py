"""Pace Table (data contract 3, v0.3 stop-allowance fields) and ETA Output (contract 4).

The pace table follows DESIGN.md §6.1 and SPEC-B1 CL-B1-4 (Issue #10): category thresholds are
recomputed from the curvature of the timed segments every time a table is built, each category
gets a speed (unweighted median) and a stop ratio (sum of short stops / sum of moving time), and the
safety margin coefficient comes from a leave-one-trip-out rule on the same trips. `eta_safe` is the
typical estimate plus that margin; it is not a P90 and carries no coverage guarantee.

`compute_eta` is still the Pre-Spec Spike version; its stop allowance belongs to Issue #11.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

from ..contracts import expected_break_times, pace_eligible, validate_pace_table
from ..contracts.schemas import CATEGORIES

TAIPEI = dt.timezone(dt.timedelta(hours=8))
METHOD = "median_unweighted"

# Pace table versions (contract 3): research- or user- plus two or more digits, numbered per prefix.
PACE_KINDS = ("research", "user")
_VERSION_FILE = re.compile(r"(research|user)-([0-9]{2,})\.json")

# Safety margin coefficient (DESIGN.md §6.1; CL-B1-4 items 6 and 7).
DEFAULT_MARGIN_COEFF = 0.20
MIN_COUNTED_FOLDS = 8      # fewer counted folds -> the default coefficient
MARGIN_STEP = 0.05
MARGIN_FLOOR = 0.05
TRIPS_ALLOWED_ABOVE = 2    # the rule may fail for at most two trips, so the third largest r decides
_CEIL_EPSILON = 1e-9       # same floating-point guard as the reference implementation


def _iso(moment: dt.datetime) -> str:
    """Nearest second, +08:00."""
    return (moment + dt.timedelta(milliseconds=500)).astimezone(TAIPEI).replace(microsecond=0).isoformat()


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# --- inputs --------------------------------------------------------------------
def _check_trip_ids(rows: list[dict], trip_ids: list[str]) -> None:
    """Refuse before any computation: every trip must be a pace trip of the derived segment table
    (CL-B1-4 item 10). A trip that is not in the table cannot be confirmed and is refused too."""
    if len(set(trip_ids)) != len(trip_ids):
        raise ValueError("trip_ids has a trip more than once")
    roles: dict[str, set] = defaultdict(set)
    for row in rows:
        roles[row.get("trip_id")].add(row.get("trip_role"))
    for trip_id in trip_ids:
        if roles.get(trip_id) != {"pace"}:
            raise ValueError(f"{trip_id} is not a pace trip (holdout, excluded, or not in the derived segment "
                             f"table); holdout trips must not enter the pace table")


def _check_min_segments(min_segments) -> None:
    if not isinstance(min_segments, int) or isinstance(min_segments, bool) or min_segments < 1:
        raise ValueError("min_segments must be an integer of at least 1")


def timed_rows(rows: list[dict], trip_ids: list[str]) -> list[dict]:
    """The timed segments (CL-B1-4 item 1): rows of the given trips with trip_role pace, quality ok,
    a curvature, and a moving time above 0. Raises ValueError if such a row has a missing or
    non-finite number in a field the pace table uses."""
    wanted = set(trip_ids)
    out = []
    for row in rows:
        if not (row.get("trip_id") in wanted and row.get("trip_role") == "pace" and row.get("quality") == "ok"
                and row.get("curvature_deg_per_km") is not None):
            continue
        moving = row.get("moving_time_s")
        if _is_number(moving) and not math.isfinite(moving):
            raise ValueError(f"trip {row.get('trip_id')} seg {row.get('seg_index')}: moving_time_s is {moving!r}, "
                             f"not a finite number")
        if _is_number(moving) and moving > 0:
            for field in ("length_m", "moving_time_s", "short_stop_time_s", "curvature_deg_per_km"):
                value = row.get(field)
                if not (_is_number(value) and math.isfinite(value) and value >= 0):
                    raise ValueError(f"trip {row.get('trip_id')} seg {row.get('seg_index')}: {field} is "
                                     f"{value!r}, not a finite number of at least 0")
            if not row["length_m"] > 0:
                raise ValueError(f"trip {row.get('trip_id')} seg {row.get('seg_index')}: length_m is not above 0")
            out.append(row)
    return out


# --- categories ----------------------------------------------------------------
def tercile_thresholds(curvatures: list[float]) -> tuple[int, int]:
    """(c1_max, c2_max): the values at positions n // 3 and 2n // 3 of the sorted curvatures, each
    rounded to 5 deg/km with Python's round (CL-B1-4 item 2)."""
    values = sorted(curvatures)
    n = len(values)
    if n == 0:
        raise ValueError("no timed segment: the category thresholds cannot be computed")
    return round(values[n // 3] / 5) * 5, round(values[2 * n // 3] / 5) * 5


def classify(curvature: float, c1_max: float, c2_max: float) -> str:
    """Same boundary as ingest: below c1_max is C1, below c2_max is C2, otherwise C3 (CL-B1-4 item 3)."""
    if curvature < c1_max:
        return "C1"
    return "C2" if curvature < c2_max else "C3"


def category_scheme(c1_max: int, c2_max: int) -> str:
    """`curv-tercile-<c1_max>-<c2_max>` with integer values (CL-B1-4 item 4)."""
    return f"curv-tercile-{int(c1_max)}-{int(c2_max)}"


def _speed_kmh(row: dict) -> float:
    return row["length_m"] / row["moving_time_s"] * 3.6


def _category_pace(timed: list[dict], c1_max: int, c2_max: int, min_segments: int) -> dict[str, dict]:
    """Per category: speed_kmh, stop_ratio and n_segments, from the timed rows classified with the
    given thresholds. A category with fewer than min_segments segments has no speed and no stop ratio."""
    grouped: dict[str, list[dict]] = {category: [] for category in CATEGORIES}
    for row in timed:
        grouped[classify(row["curvature_deg_per_km"], c1_max, c2_max)].append(row)
    out = {}
    for category, segs in grouped.items():
        if len(segs) >= min_segments:
            speed = round(statistics.median(_speed_kmh(r) for r in segs), 2)
            ratio = sum(r["short_stop_time_s"] for r in segs) / sum(r["moving_time_s"] for r in segs)
        else:
            speed = ratio = None
        out[category] = {"speed_kmh": speed, "stop_ratio": ratio, "n_segments": len(segs)}
    return out


# --- safety margin -------------------------------------------------------------
def loo_folds(rows: list[dict], trip_ids: list[str], min_segments: int) -> list[dict]:
    """Leave one trip out over trip_ids (CL-B1-4 item 6). One entry per trip, in trip_id order:
    the fold's thresholds (None when the other trips have no timed segment), whether the fold is
    counted, and r = actual / predicted - 1 for a counted fold.

    Each fold recomputes the thresholds and the pace from the other trips only. A fold is not
    counted when the left-out trip has no timed segment, or when any category among its timed
    segments has no speed in that fold."""
    _check_min_segments(min_segments)
    _check_trip_ids(rows, trip_ids)
    timed = timed_rows(rows, trip_ids)
    folds = []
    for left_out in sorted(trip_ids):
        others = [r for r in timed if r["trip_id"] != left_out]
        held = [r for r in timed if r["trip_id"] == left_out]
        fold = {"trip_id": left_out, "thresholds": None, "counted": False, "r": None}
        folds.append(fold)
        if not others:
            continue
        c1_max, c2_max = tercile_thresholds([r["curvature_deg_per_km"] for r in others])
        fold["thresholds"] = (c1_max, c2_max)
        if not held:
            continue
        pace = _category_pace(others, c1_max, c2_max, min_segments)
        cats = [classify(r["curvature_deg_per_km"], c1_max, c2_max) for r in held]
        if any(pace[c]["speed_kmh"] is None for c in cats):
            continue
        actual = sum(r["moving_time_s"] + r["short_stop_time_s"] for r in held)
        predicted = sum(r["length_m"] / (pace[c]["speed_kmh"] / 3.6) * (1 + pace[c]["stop_ratio"])
                        for r, c in zip(held, cats))
        fold.update(counted=True, r=actual / predicted - 1)
    return folds


def margin_from_residuals(residuals: list[float]) -> tuple[float, str]:
    """(margin_coeff, margin_basis) from the r of the counted folds (CL-B1-4 item 7).

    Fewer than 8 counted folds: (0.20, "default"). Otherwise the smallest multiple of 0.05, at
    least 0.05, such that r <= margin_coeff for all but at most two folds: from the third largest r,
    max(0.05, ceil(max(r3, 0) / 0.05) * 0.05), rounded to two decimals."""
    if any(not (_is_number(r) and math.isfinite(r)) for r in residuals):
        raise ValueError("every residual must be a finite number")
    if len(residuals) < MIN_COUNTED_FOLDS:
        return DEFAULT_MARGIN_COEFF, "default"
    r3 = sorted(residuals, reverse=True)[TRIPS_ALLOWED_ABOVE]
    coeff = max(MARGIN_FLOOR, math.ceil(max(r3, 0.0) / MARGIN_STEP - _CEIL_EPSILON) * MARGIN_STEP)
    return round(coeff, 2), "loo_rule"


# --- the pace table ------------------------------------------------------------
def build_pace_table(rows: list[dict], trip_ids: list[str], *, pace_version: str, min_segments: int,
                     built_at: dt.datetime) -> tuple[dict, list[dict]]:
    """Header and category records of one pace table, computed in memory (nothing is written).

    Refuses before computing when a trip is not a pace trip. Raises ValueError when there is no
    timed segment: no table is built then. The derived table's seg_category and category_scheme
    are not used; the categories come from the recomputed thresholds (CL-B1-4 item 3)."""
    _check_min_segments(min_segments)
    _check_trip_ids(rows, trip_ids)
    if built_at.tzinfo is None:
        raise ValueError("built_at must be timezone-aware")
    versions = {r.get("ingest_version") for r in rows}
    if len(versions) != 1:
        raise ValueError("the derived segment table must have one ingest_version")
    timed = timed_rows(rows, trip_ids)
    c1_max, c2_max = tercile_thresholds([r["curvature_deg_per_km"] for r in timed])
    pace = _category_pace(timed, c1_max, c2_max, min_segments)
    residuals = [f["r"] for f in loo_folds(rows, trip_ids, min_segments) if f["counted"]]
    margin_coeff, margin_basis = margin_from_residuals(residuals)
    header = {"pace_version": pace_version, "method": METHOD, "category_scheme": category_scheme(c1_max, c2_max),
              "ingest_version": versions.pop(), "min_segments": min_segments, "n_trips": len(trip_ids),
              "trip_ids": sorted(trip_ids), "margin_coeff": margin_coeff, "margin_basis": margin_basis,
              "built_at": _iso(built_at)}
    categories = [{"pace_version": pace_version, "seg_category": category, "speed_kmh": pace[category]["speed_kmh"],
                   "stop_ratio": pace[category]["stop_ratio"], "n_segments": pace[category]["n_segments"]}
                  for category in CATEGORIES]
    return header, categories


# --- versions and files --------------------------------------------------------
def _existing_versions(directory: Path, kind: str) -> dict[int, list[Path]]:
    found: dict[int, list[Path]] = defaultdict(list)
    for path in directory.iterdir():
        match = _VERSION_FILE.fullmatch(path.name)
        if match and match.group(1) == kind:
            found[int(match.group(2))].append(path)
    return found


def _require_directory(directory) -> Path:
    path = Path(directory)
    if not path.is_dir():
        raise FileNotFoundError(f"pace table directory {path} does not exist or is not a directory")
    return path


def create_pace_table(directory, rows: list[dict], trip_ids: list[str], *, kind: str, min_segments: int,
                      built_at: dt.datetime, number: int | None = None) -> tuple[Path, dict, list[dict]]:
    """Build a pace table and write it as a new file `<pace_version>.json` in `directory`, which the
    caller provides and which must exist. There is no default location.

    The version is `<kind>-NN`. Without `number`, NN is the largest existing number of that kind
    plus 1 (at least two digits); the two kinds are numbered separately. Only a research- version
    may be given a number by the caller. An existing version is an error: no file is overwritten,
    changed or deleted. Nothing is written when the table cannot be built or breaks contract 3."""
    if kind not in PACE_KINDS:
        raise ValueError(f"kind must be one of {PACE_KINDS}")
    path_dir = _require_directory(directory)
    existing = _existing_versions(path_dir, kind)
    if number is None:
        number = max(existing, default=0) + 1
    elif kind != "research":
        raise ValueError("only a research- version may be given a number; user- versions are numbered automatically")
    elif not isinstance(number, int) or isinstance(number, bool) or number < 0:
        raise ValueError("number must be a non-negative integer")
    pace_version = f"{kind}-{number:02d}"
    if number in existing:
        raise FileExistsError(f"pace table version {pace_version} already exists; it is not overwritten")

    header, categories = build_pace_table(rows, trip_ids, pace_version=pace_version, min_segments=min_segments,
                                          built_at=built_at)
    violations = validate_pace_table(header, categories)
    if violations:
        raise ValueError(f"the pace table does not conform to contract 3, nothing written: {violations}")
    path = path_dir / f"{pace_version}.json"
    text = json.dumps({"pace_header": header, "pace_categories": categories}, ensure_ascii=False, indent=2) + "\n"
    with path.open("x", encoding="utf-8") as handle:  # "x": fails if the file appeared meanwhile
        handle.write(text)
    return path, header, categories


def load_pace_table(path) -> tuple[dict, list[dict]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["pace_header"], data["pace_categories"]


def latest_user_pace_table(directory) -> Path | None:
    """The user- version with the latest built_at in `directory`; the larger number on a tie
    (CL-B1-4 item 9). None when the directory has no user- version: falling back to the research-
    version of the freeze list is outside this module."""
    path_dir = _require_directory(directory)
    best, best_key = None, None
    for number, paths in _existing_versions(path_dir, "user").items():
        for path in paths:
            header, _ = load_pace_table(path)
            if header.get("pace_version") != path.stem:
                raise ValueError(f"{path.name} holds pace_version {header.get('pace_version')!r}")
            built = header.get("built_at")
            try:
                moment = dt.datetime.fromisoformat(built) if isinstance(built, str) else None
            except ValueError:
                moment = None
            if moment is None or moment.tzinfo is None:
                raise ValueError(f"{path.name} has no timezone-aware built_at")
            key = (moment, number)
            if best_key is None or key > best_key:
                best, best_key = path, key
    return best


# --- method comparison (DC-10; unchanged Spike behaviour, derived seg_category) --------
def _eligible_by_category(rows: list[dict], trip_ids: list[str]) -> dict[str, list[dict]]:
    _check_trip_ids(rows, trip_ids)
    wanted = set(trip_ids)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row["trip_id"] in wanted and pace_eligible(row):
            grouped[row["seg_category"]].append(row)
    return grouped


def compare_methods(rows: list[dict], trip_ids: list[str]) -> dict[str, dict]:
    """Unweighted against length-weighted median, on pace trips only (DC-10). For choosing a
    method before the formal E1 run; holdout trips are rejected like in build_pace_table."""
    out = {}
    for category, segs in _eligible_by_category(rows, trip_ids).items():
        ordered = sorted(segs, key=_speed_kmh)
        half, running, weighted = sum(r["length_m"] for r in ordered) / 2, 0.0, None
        for r in ordered:
            running += r["length_m"]
            if running >= half:
                weighted = _speed_kmh(r)
                break
        out[category] = {"n_segments": len(segs),
                         "median_unweighted": round(statistics.median(_speed_kmh(r) for r in segs), 2),
                         "median_length_weighted": round(weighted, 2)}
    return out


# --- ETA (Spike; Issue #11) -------------------------------------------------------
def compute_eta(route: dict, route_segments: list[dict], checkpoints: list[dict], pace_header: dict,
                pace_categories: list[dict], *, plan_id: str, departure_time: dt.datetime, margin_coeff: float,
                breaks: list[dict], computed_at: dt.datetime) -> tuple[dict, list[dict]]:
    """ETA for one departure on one route. If any segment's category has no pace the status is
    `unknown` and no time is produced, not even a partial one."""
    if departure_time.tzinfo is None:
        raise ValueError("departure_time must be timezone-aware")
    segs = sorted((s for s in route_segments if s["route_id"] == route["route_id"]), key=lambda s: s["seg_index"])
    cps = [c for c in checkpoints if c["route_id"] == route["route_id"]]
    speed = {c["seg_category"]: c["speed_kmh"] for c in pace_categories}
    missing = sorted({s["seg_category"] for s in segs if speed.get(s["seg_category"]) is None})
    break_times = expected_break_times(route["n_segments"], breaks, cps)

    header = {"plan_id": plan_id, "route_id": route["route_id"], "departure_time": _iso(departure_time),
              "status": "unknown" if missing else "ok",
              "unknown_reason": f"no pace for category {', '.join(missing)}" if missing else None,
              "margin_coeff": margin_coeff, "breaks": breaks, "pace_version": pace_header["pace_version"],
              "catalog_version": route["catalog_version"], "computed_at": _iso(computed_at)}
    rows, cumulative = [], 0.0
    for seg, break_time in zip(segs, break_times):
        row = {"plan_id": plan_id, "seg_index": seg["seg_index"], "typ_seg_time_s": None,
               "break_time_s": break_time, "eta_typ": None, "eta_safe": None}
        if not missing:
            typical = round(seg["length_m"] / (speed[seg["seg_category"]] / 3.6), 3)
            cumulative += typical
            arrival = departure_time + dt.timedelta(seconds=cumulative + break_time)
            row.update(typ_seg_time_s=typical, eta_typ=_iso(arrival),
                       eta_safe=_iso(arrival + dt.timedelta(seconds=margin_coeff * cumulative)))
        rows.append(row)
    return header, rows
