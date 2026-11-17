"""Validation of the minimal data contracts (DESIGN.md §5).

Contract v0.2 plus the approved v0.3 stop-allowance fields and invariants of contracts 1, 3 and 4
(Issue #7); see schemas.py for what is not covered yet.

Every validate_* function returns a list of violation messages; an empty list means the data
conforms. Nothing here computes pace or ETA: it only checks data that some producer wrote.
Contract 3 invariant 3 is checked as a total count of eligible rows, and per category only when the
derived rows carry the pace table's category_scheme (SPEC-B1 CL-B1-12).
"""
from __future__ import annotations

import datetime as dt
import math
import re
from collections import defaultdict
from typing import Any, Iterable

import jsonschema

from . import schemas as S

# ETA timestamps are ISO strings, so recomputed times are compared with a tolerance.
# Contract 4 invariant 8 (v0.3) allows one second.
ETA_TOLERANCE_S = 1.0
# Contract 3 (v0.3): pace_version is research- or user- followed by two or more ASCII digits.
PACE_VERSION_PATTERN = re.compile(r"(research|user)-[0-9]{2,}")
# Contract 3 invariant 6 (v0.3): margin_coeff is 0.20 for a default basis, and a multiple of
# 0.05 for a loo_rule basis. The tolerance only absorbs binary floating-point error.
DEFAULT_MARGIN_COEFF = 0.20
MARGIN_STEP = 0.05
MARGIN_FLOAT_TOLERANCE = 1e-9
# cum_length_m is a running sum of length_m written by the same producer.
LENGTH_TOLERANCE_M = 1e-6

Rows = list[dict[str, Any]]


def _schema_errors(label: str, rows: Iterable[dict], schema: dict) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema)
    out = []
    for i, row in enumerate(rows):
        for err in validator.iter_errors(row):
            where = "/".join(str(p) for p in err.absolute_path) or "(record)"
            out.append(f"{label}[{i}] schema: {where}: {err.message}")
    return out


def _duplicates(keys: Iterable[Any]) -> list[Any]:
    seen, dup = set(), []
    for key in keys:
        if key in seen and key not in dup:
            dup.append(key)
        seen.add(key)
    return dup


def _contiguous(indices: list[int]) -> bool:
    return sorted(indices) == list(range(len(indices)))


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_finite_number(value: Any) -> bool:
    return _is_number(value) and math.isfinite(value)


def _non_finite_errors(label: str, rows: Iterable[dict], fields: tuple[str, ...]) -> list[str]:
    """NaN and +/-infinity are not JSON numbers, but Python dicts (and json.loads) can carry them, and
    JSON Schema's minimum does not reject NaN. Reject them explicitly for the v0.3 fields (R1-F1)."""
    out = []
    for i, row in enumerate(rows):
        for field in fields:
            value = row.get(field)
            if _is_number(value) and not math.isfinite(value):
                out.append(f"{label}[{i}]: {field} is not a finite number ({value})")
    return out


def _is_multiple_of_step(value: float) -> bool:
    steps = value / MARGIN_STEP
    return math.isfinite(steps) and abs(steps - round(steps)) <= MARGIN_FLOAT_TOLERANCE


def _time(value: Any) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(value) if isinstance(value, str) else None
    except ValueError:
        return None


# --- Contract 1: Derived Segment Table -------------------------------------
def pace_eligible(row: dict) -> bool:
    """Invariant 4: only these rows may enter the Pace Table."""
    return (row.get("quality") == "ok" and row.get("seg_category") is not None
            and row.get("trip_role") == "pace" and row.get("moving_time_s") is not None)


def validate_derived_segments(rows: Rows, visibility: str = "public") -> list[str]:
    if visibility not in ("public", "private"):
        raise ValueError("visibility must be 'public' or 'private'")
    schema = S.DERIVED_SEGMENT_PUBLIC if visibility == "public" else S.DERIVED_SEGMENT_PRIVATE
    out = _schema_errors(f"derived_segments({visibility})", rows, schema)
    out += _non_finite_errors(f"derived_segments({visibility})", rows, ("short_stop_time_s",))

    for key in _duplicates((r.get("trip_id"), r.get("seg_index")) for r in rows):
        out.append(f"derived_segments: duplicate primary key {key}")

    by_trip: dict[Any, Rows] = defaultdict(list)
    for r in rows:
        by_trip[r.get("trip_id")].append(r)
    for trip_id, trip_rows in by_trip.items():
        indices = [r.get("seg_index") for r in trip_rows]
        if all(isinstance(i, int) for i in indices) and not _contiguous(indices):
            out.append(f"derived_segments: trip {trip_id} seg_index is not 0..n-1 without gaps")
        if len({r.get("trip_role") for r in trip_rows}) > 1:
            out.append(f"derived_segments: trip {trip_id} has more than one trip_role (invariant 1)")
        if len({r.get("route_id") for r in trip_rows}) > 1:
            out.append(f"derived_segments: trip {trip_id} has more than one route_id (invariant 1)")

    for column in ("ingest_version", "category_scheme"):
        if len({r.get(column) for r in rows}) > 1:
            out.append(f"derived_segments: more than one {column} in one table (invariant 2)")

    for i, r in enumerate(rows):
        invalid, has_time = r.get("quality") == "invalid", r.get("moving_time_s") is not None
        if invalid and has_time:
            out.append(f"derived_segments[{i}]: quality is invalid but moving_time_s has a value (invariant 3)")
        if not invalid and not has_time:
            out.append(f"derived_segments[{i}]: moving_time_s is null but quality is not invalid (invariant 3)")
        short, stopped = r.get("short_stop_time_s"), r.get("stopped_time_s")
        if _is_finite_number(short) and _is_number(stopped) and short > stopped:
            out.append(f"derived_segments[{i}]: short_stop_time_s is greater than stopped_time_s (invariant 6)")
    return out


def validate_public_private_pair(public: Rows, private: Rows) -> list[str]:
    """Invariant 5: same rows, same values, the private version only adds start_time."""
    out = []
    key = lambda r: (r.get("trip_id"), r.get("seg_index"))
    pub, prv = {key(r): r for r in public}, {key(r): r for r in private}
    if set(pub) != set(prv):
        out.append("derived_segments: public and private versions do not have the same rows (invariant 5)")
    for k in set(pub) & set(prv):
        for column, value in pub[k].items():
            if prv[k].get(column) != value:
                out.append(f"derived_segments: {k} differs between public and private in {column} (invariant 5)")
    return out


# --- Contract 2: Route Catalog ---------------------------------------------
def validate_route_catalog(routes: Rows, segments: Rows, checkpoints: Rows) -> list[str]:
    out = (_schema_errors("routes", routes, S.ROUTE) + _schema_errors("route_segments", segments, S.ROUTE_SEGMENT)
           + _schema_errors("checkpoints", checkpoints, S.CHECKPOINT))
    for name, keys in (("routes", [r.get("route_id") for r in routes]),
                       ("route_segments", [(s.get("route_id"), s.get("seg_index")) for s in segments]),
                       ("checkpoints", [c.get("checkpoint_id") for c in checkpoints])):
        for key in _duplicates(keys):
            out.append(f"{name}: duplicate primary key {key}")

    route_ids = {r.get("route_id") for r in routes}
    for label, records in (("route_segments", segments), ("checkpoints", checkpoints)):
        for rec in records:
            if rec.get("route_id") not in route_ids:
                out.append(f"{label}: route_id {rec.get('route_id')} is not in routes")

    for route in routes:
        rid, n = route.get("route_id"), route.get("n_segments")
        segs = sorted((s for s in segments if s.get("route_id") == rid), key=lambda s: s.get("seg_index", -1))
        if len(segs) != n or not _contiguous([s.get("seg_index") for s in segs]):
            out.append(f"routes: {rid} needs seg_index 0..{n}-1 exactly once, found {len(segs)} segments")
        else:
            running = 0.0
            for s in segs:
                running += s["length_m"]
                if abs(s["cum_length_m"] - running) > LENGTH_TOLERANCE_M * max(1.0, running):
                    out.append(f"route_segments: {rid} seg {s['seg_index']} cum_length_m is not the running sum of length_m")
            if segs and segs[-1]["cum_length_m"] != route.get("total_length_m"):
                out.append(f"routes: {rid} total_length_m differs from the last cum_length_m")

        cps = [c for c in checkpoints if c.get("route_id") == rid]
        for kind, position in (("start", 0), ("end", n)):
            of_kind = [c for c in cps if c.get("kind") == kind]
            if len(of_kind) != 1:
                out.append(f"checkpoints: {rid} must have exactly one {kind}, found {len(of_kind)} (invariant 1)")
            for c in of_kind:
                if c.get("after_seg_count") != position:
                    out.append(f"checkpoints: {c.get('checkpoint_id')} is {kind} but after_seg_count is not {position} (invariant 1)")
        for c in cps:
            count = c.get("after_seg_count")
            if isinstance(count, int) and isinstance(n, int) and not 0 <= count <= n:
                out.append(f"checkpoints: {c.get('checkpoint_id')} after_seg_count {count} is outside 0..{n} (invariant 2)")

    for c in checkpoints:
        is_station, has_ref = c.get("kind") == "fuel_station", c.get("station_ref") is not None
        if is_station and not has_ref:
            out.append(f"checkpoints: {c.get('checkpoint_id')} is a fuel_station without station_ref")
        if not is_station and has_ref:
            out.append(f"checkpoints: {c.get('checkpoint_id')} is not a fuel_station but has station_ref")
    return out


# --- Contract 3: Pace Table -------------------------------------------------
def validate_pace_table(header: dict, categories: Rows, derived_rows: Rows | None = None) -> list[str]:
    out = _schema_errors("pace_header", [header], S.PACE_HEADER) + _schema_errors("pace_categories", categories, S.PACE_CATEGORY)
    out += _non_finite_errors("pace_header", [header], ("margin_coeff",))
    out += _non_finite_errors("pace_categories", categories, ("stop_ratio",))
    version = header.get("pace_version")
    if isinstance(version, str) and not PACE_VERSION_PATTERN.fullmatch(version):
        out.append(f"pace_header: pace_version {version!r} is not research- or user- followed by "
                   f"two or more digits (invariant 7)")
    for rec in categories:
        if rec.get("pace_version") != version:
            out.append(f"pace_categories: {rec.get('seg_category')} belongs to another pace_version")

    basis, coeff = header.get("margin_basis"), header.get("margin_coeff")
    if _is_finite_number(coeff):
        if basis == "default" and abs(coeff - DEFAULT_MARGIN_COEFF) > MARGIN_FLOAT_TOLERANCE:
            out.append(f"pace_header: margin_basis is default but margin_coeff is {coeff}, not 0.20 (invariant 6)")
        if basis == "loo_rule" and not (coeff >= MARGIN_STEP - MARGIN_FLOAT_TOLERANCE and _is_multiple_of_step(coeff)):
            out.append(f"pace_header: margin_basis is loo_rule but margin_coeff {coeff} is not a multiple of 0.05 "
                       f"of at least 0.05 (invariant 6)")

    present = [rec.get("seg_category") for rec in categories]
    for category in S.CATEGORIES:
        if present.count(category) != 1:
            out.append(f"pace_categories: need exactly one record for {category}, found {present.count(category)} (invariant 1)")

    trip_ids = header.get("trip_ids") or []
    if header.get("n_trips") != len(trip_ids):
        out.append("pace_header: n_trips does not equal the number of trip_ids (invariant 2)")

    minimum = header.get("min_segments")
    for rec in categories:
        n, speed = rec.get("n_segments"), rec.get("speed_kmh")
        if isinstance(n, int) and isinstance(minimum, int):
            if n < minimum and speed is not None:
                out.append(f"pace_categories: {rec.get('seg_category')} has speed_kmh with fewer than min_segments segments")
            if n >= minimum and speed is None:
                out.append(f"pace_categories: {rec.get('seg_category')} has enough segments but speed_kmh is null")
    for rec in categories:
        if "stop_ratio" in rec and (rec.get("stop_ratio") is None) != (rec.get("speed_kmh") is None):
            out.append(f"pace_categories: {rec.get('seg_category')} stop_ratio must be null exactly when "
                       f"speed_kmh is null (invariant 4)")

    if derived_rows is not None:
        roles = {r.get("trip_id"): r.get("trip_role") for r in derived_rows}
        for trip_id in trip_ids:
            if roles.get(trip_id) != "pace":
                out.append(f"pace_header: trip {trip_id} is not a pace trip (holdout or unknown) (invariant 2)")
        if {r.get("ingest_version") for r in derived_rows} - {header.get("ingest_version")}:
            out.append("pace_header: ingest_version differs from the derived segment table")
        # Invariant 3 (CL-B1-12): the pace table classifies the eligible rows with its own
        # category_scheme. The total is always checked; the per-category count only when every
        # eligible row has the pace table's category_scheme, so that the derived seg_category is the
        # pace table's category. The scheme is not parsed and nothing is reclassified here.
        eligible_rows = [r for r in derived_rows if pace_eligible(r) and r.get("trip_id") in trip_ids]
        counts = [rec.get("n_segments") for rec in categories]
        if all(isinstance(n, int) and not isinstance(n, bool) for n in counts) and sum(counts) != len(eligible_rows):
            out.append(f"pace_categories: n_segments add up to {sum(counts)}, but {len(eligible_rows)} rows "
                       f"are eligible (invariant 3)")
        if all(r.get("category_scheme") == header.get("category_scheme") for r in eligible_rows):
            for rec in categories:
                eligible = sum(1 for r in eligible_rows if r.get("seg_category") == rec.get("seg_category"))
                if rec.get("n_segments") != eligible:
                    out.append(f"pace_categories: {rec.get('seg_category')} n_segments is {rec.get('n_segments')}, "
                               f"but {eligible} rows are eligible (invariant 3)")
    return out


# --- Contract 4: ETA Output -------------------------------------------------
def expected_break_times(n_segments: int, breaks: Rows, checkpoints: Rows) -> list[float]:
    """break_time_s for seg_index 0..n-1 (invariant 3).

    A break happens after arriving at its checkpoint. A checkpoint with after_seg_count c sits at
    the end of segment c-1, so the break delays segments c, c+1, ... and not segment c-1.
    """
    position = {c["checkpoint_id"]: c["after_seg_count"] for c in checkpoints}
    times = [0.0] * n_segments
    for b in breaks:
        c = position[b["after_checkpoint_id"]]
        for k in range(c, n_segments):
            times[k] += b["duration_s"]
    return times


def checkpoint_arrival(header: dict, eta_rows: Rows, checkpoint: dict) -> tuple[str | None, str | None]:
    """(eta_typ, eta_safe) on arrival at a checkpoint, before any break taken there (invariant 4)."""
    c = checkpoint["after_seg_count"]
    if c == 0:
        return header["departure_time"], header["departure_time"]
    row = next(r for r in eta_rows if r["plan_id"] == header["plan_id"] and r["seg_index"] == c - 1)
    return row["eta_typ"], row["eta_safe"]


def validate_eta_output(headers: Rows, eta_segments: Rows, routes: Rows, route_segments: Rows, checkpoints: Rows,
                        pace_header: dict | None = None, pace_categories: Rows | None = None) -> list[str]:
    out = _schema_errors("eta_headers", headers, S.ETA_HEADER) + _schema_errors("eta_segments", eta_segments, S.ETA_SEGMENT)
    out += _non_finite_errors("eta_headers", headers, ("margin_coeff",))
    out += _non_finite_errors("eta_segments", eta_segments, ("stop_allow_s",))
    for key in _duplicates(h.get("plan_id") for h in headers):
        out.append(f"eta_headers: duplicate plan_id {key}")
    for key in _duplicates((s.get("plan_id"), s.get("seg_index")) for s in eta_segments):
        out.append(f"eta_segments: duplicate primary key {key}")
    plan_ids = {h.get("plan_id") for h in headers}
    for s in eta_segments:
        if s.get("plan_id") not in plan_ids:
            out.append(f"eta_segments: plan_id {s.get('plan_id')} has no header")

    route_by_id = {r.get("route_id"): r for r in routes}
    null_speed = {c.get("seg_category") for c in (pace_categories or []) if c.get("speed_kmh") is None}

    for h in headers:
        pid, rid = h.get("plan_id"), h.get("route_id")
        status, reason = h.get("status"), h.get("unknown_reason")
        if (status == "unknown") != (reason is not None):
            out.append(f"eta_headers: {pid} unknown_reason must be set exactly when status is unknown")
        route = route_by_id.get(rid)
        if route is None:
            out.append(f"eta_headers: {pid} route_id {rid} is not in the route catalog")
            continue
        if h.get("catalog_version") != route.get("catalog_version"):
            out.append(f"eta_headers: {pid} catalog_version differs from the route catalog")
        if pace_header is not None and h.get("pace_version") != pace_header.get("pace_version"):
            out.append(f"eta_headers: {pid} pace_version differs from the pace table")
        if pace_header is not None and h.get("margin_coeff") != pace_header.get("margin_coeff"):
            out.append(f"eta_headers: {pid} margin_coeff {h.get('margin_coeff')} differs from the pace table's "
                       f"{pace_header.get('margin_coeff')} (invariant 9)")

        n = route["n_segments"]
        rows = sorted((s for s in eta_segments if s.get("plan_id") == pid), key=lambda s: s.get("seg_index", -1))
        if len(rows) != n or not _contiguous([s.get("seg_index") for s in rows]):
            out.append(f"eta_segments: {pid} needs seg_index 0..{n}-1 exactly once, found {len(rows)} rows (invariant 1)")
            continue

        cps = {c["checkpoint_id"]: c for c in checkpoints if c.get("route_id") == rid}
        breaks, breaks_ok = h.get("breaks") or [], True
        for key in _duplicates(b.get("after_checkpoint_id") for b in breaks):
            out.append(f"eta_headers: {pid} has more than one break at {key} (invariant 2)")
            breaks_ok = False
        for b in breaks:
            cp = cps.get(b.get("after_checkpoint_id"))
            if cp is None:
                out.append(f"eta_headers: {pid} break at {b.get('after_checkpoint_id')}, which is not a checkpoint of {rid} (invariant 2)")
                breaks_ok = False
            elif not 0 < cp["after_seg_count"] < n:
                out.append(f"eta_headers: {pid} break at {cp['checkpoint_id']} sits at the start or the end (invariant 2)")
                breaks_ok = False
        if breaks_ok:
            for k, expected in enumerate(expected_break_times(n, breaks, list(cps.values()))):
                if abs(rows[k].get("break_time_s", -1) - expected) > 1e-9:
                    out.append(f"eta_segments: {pid} seg {k} break_time_s should be {expected} (invariant 3)")

        if status == "unknown":
            for s in rows:
                if any(s.get(col) is not None for col in ("typ_seg_time_s", "stop_allow_s", "eta_typ", "eta_safe")):
                    out.append(f"eta_segments: {pid} seg {s['seg_index']} carries a time although status is unknown (invariant 6)")
            continue

        categories = {s.get("seg_category") for s in route_segments if s.get("route_id") == rid}
        if categories & null_speed:
            out.append(f"eta_headers: {pid} is ok but the route uses a category without pace: {sorted(categories & null_speed)} (invariant 7)")

        # cumulative is the running sum of typ_seg_time_s + stop_allow_s (the typical ride time).
        departure, margin = _time(h.get("departure_time")), h.get("margin_coeff", 0)
        margin_ok = _is_finite_number(margin)  # otherwise already reported; skip the margin arithmetic
        category_of = {s.get("seg_index"): s.get("seg_category") for s in route_segments if s.get("route_id") == rid}
        stop_ratio = ({c.get("seg_category"): c.get("stop_ratio") for c in pace_categories}
                      if pace_categories is not None else None)
        cumulative, previous = 0.0, None
        for s in rows:
            k, typ, safe = s["seg_index"], _time(s.get("eta_typ")), _time(s.get("eta_safe"))
            typical, allowance = s.get("typ_seg_time_s"), s.get("stop_allow_s")
            if typical is None or allowance is None or typ is None or safe is None:
                out.append(f"eta_segments: {pid} seg {k} has a null time although status is ok")
                break
            if not (_is_number(typical) and _is_finite_number(allowance)):
                break  # already reported (schema or non-finite check); the arithmetic below would be meaningless
            if stop_ratio is not None:  # invariant 8: needs the pace table
                ratio = stop_ratio.get(category_of.get(k))
                if not _is_number(ratio):
                    out.append(f"eta_segments: {pid} seg {k} stop_allow_s cannot be checked: category "
                               f"{category_of.get(k)} has no stop_ratio in the pace table (invariant 8)")
                elif not math.isfinite(ratio):
                    out.append(f"eta_segments: {pid} seg {k} stop_allow_s cannot be checked: category "
                               f"{category_of.get(k)} has a non-finite stop_ratio ({ratio}) in the pace table (invariant 8)")
                elif abs(allowance - ratio * typical) > ETA_TOLERANCE_S:
                    out.append(f"eta_segments: {pid} seg {k} stop_allow_s is not stop_ratio x typ_seg_time_s (invariant 8)")
            cumulative += typical + allowance
            if departure is not None and breaks_ok:
                expected = departure + dt.timedelta(seconds=cumulative + s["break_time_s"])
                if abs((typ - expected).total_seconds()) > ETA_TOLERANCE_S:
                    out.append(f"eta_segments: {pid} seg {k} eta_typ is not departure + cumulative time + break_time_s")
                expected_safe = expected + dt.timedelta(seconds=margin * cumulative) if margin_ok else None
                if expected_safe is not None and abs((safe - expected_safe).total_seconds()) > ETA_TOLERANCE_S:
                    out.append(f"eta_segments: {pid} seg {k} eta_safe is not eta_typ + margin_coeff x cumulative time")
            if margin_ok and abs((safe - typ).total_seconds() - margin * cumulative) > ETA_TOLERANCE_S:
                out.append(f"eta_segments: {pid} seg {k} eta_safe - eta_typ is not margin_coeff x cumulative "
                           f"(typ_seg_time_s + stop_allow_s) (invariant 8)")
            break_time = s.get("break_time_s")
            if previous is not None and breaks_ok and _is_number(break_time) and _is_number(previous[1]):
                step = (typ - previous[0]).total_seconds()
                expected_step = typical + allowance + break_time - previous[1]
                if abs(step - expected_step) > ETA_TOLERANCE_S:
                    out.append(f"eta_segments: {pid} seg {k} eta_typ minus the previous eta_typ is not "
                               f"typ_seg_time_s + stop_allow_s + the new break time (invariant 8)")
            if safe < typ:
                out.append(f"eta_segments: {pid} seg {k} eta_safe is earlier than eta_typ (invariant 5)")
            if previous is not None and typ < previous[0]:
                out.append(f"eta_segments: {pid} seg {k} eta_typ goes back in time (invariant 5)")
            previous = (typ, break_time)
    return out


# --- Whole dataset ----------------------------------------------------------
def validate_dataset(data: dict, visibility: str = "public") -> dict[str, list[str]]:
    """Validate whichever contracts are present in `data`. Keys of the result are contract names."""
    report: dict[str, list[str]] = {}
    derived = data.get("derived_segments")
    if derived is not None:
        report["derived_segments"] = validate_derived_segments(derived, visibility)
    if "routes" in data:
        report["route_catalog"] = validate_route_catalog(data["routes"], data.get("route_segments", []),
                                                         data.get("checkpoints", []))
    if "pace_header" in data:
        report["pace_table"] = validate_pace_table(data["pace_header"], data.get("pace_categories", []), derived)
    if "eta_headers" in data:
        report["eta_output"] = validate_eta_output(
            data["eta_headers"], data.get("eta_segments", []), data.get("routes", []),
            data.get("route_segments", []), data.get("checkpoints", []),
            data.get("pace_header"), data.get("pace_categories"))
    return report
