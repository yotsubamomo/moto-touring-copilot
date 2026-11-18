"""ETA of SPEC-B1 B1-4 (Issue #11): stop allowance and the safety margin from the pace table's header.

Every value here is invented: round segment lengths, speeds and stop ratios chosen so the expected
times can be worked out by hand. The route is a made-up catalog entry; its end coordinates are
placeholders near (0, 0) and are not a place. Nothing here is ride data or a ride result.
"""
from __future__ import annotations

import datetime as dt
import math

import pytest

from moto_copilot.contracts import validate_eta_output, validate_pace_table, validate_route_catalog
from moto_copilot.pace import build_pace_table, compute_eta
from test_pace_table import trips_three_categories

TAIPEI = dt.timezone(dt.timedelta(hours=8))
DEPART = dt.datetime(2026, 11, 21, 7, 0, tzinfo=TAIPEI)
COMPUTED = dt.datetime(2026, 11, 18, 9, 0, tzinfo=TAIPEI)
SCHEME = "curv-tercile-100-300"


def pace_table(*, margin_coeff: float = 0.15, margin_basis: str = "loo_rule", c3_speed: float | None = 30.0):
    """A contract-3 pace table: C1 60 km/h with stop ratio 0.05, C2 45 km/h with 0.10, C3 30 km/h
    with 0.20 (or no pace for C3: one segment, below min_segments)."""
    header = {"pace_version": "user-03", "method": "median_unweighted", "category_scheme": SCHEME,
              "ingest_version": "ingest-test", "min_segments": 2, "n_trips": 2, "trip_ids": ["T101", "T102"],
              "margin_coeff": margin_coeff, "margin_basis": margin_basis, "built_at": "2026-11-18T09:00:00+08:00"}
    categories = [
        {"pace_version": "user-03", "seg_category": "C1", "speed_kmh": 60.0, "stop_ratio": 0.05, "n_segments": 4},
        {"pace_version": "user-03", "seg_category": "C2", "speed_kmh": 45.0, "stop_ratio": 0.10, "n_segments": 3},
        {"pace_version": "user-03", "seg_category": "C3", "speed_kmh": c3_speed,
         "stop_ratio": 0.20 if c3_speed is not None else None, "n_segments": 2 if c3_speed is not None else 1},
    ]
    return header, categories


def catalog():
    """R05: C1 3000 m, C2 1500 m, C3 1000 m, C1 6000 m; a fuel station after segment 1 and a waypoint
    after segment 2. R06: C1 2000 m, C3 1000 m. R07: C1 2000 m, C2 1500 m (no C3)."""
    routes, segments, checkpoints = [], [], []
    for route_id, parts in (("R05", [("C1", 3000.0), ("C2", 1500.0), ("C3", 1000.0), ("C1", 6000.0)]),
                            ("R06", [("C1", 2000.0), ("C3", 1000.0)]),
                            ("R07", [("C1", 2000.0), ("C2", 1500.0)])):
        cum = 0.0
        for i, (category, length) in enumerate(parts):
            cum += length
            segments.append({"route_id": route_id, "seg_index": i, "length_m": length, "cum_length_m": cum,
                             "seg_category": category, "end_lat": 0.0, "end_lon": 0.01 * (i + 1)})
        routes.append({"route_id": route_id, "name": f"合成路線 {route_id}（測試）", "n_segments": len(parts),
                       "total_length_m": cum, "source_trip_id": "T900", "route_source": "trip", "snapshot_id": None,
                       "trip_type": "one_way", "category_scheme": SCHEME,
                       "catalog_version": "catalog-test"})
        checkpoints.append({"checkpoint_id": f"{route_id}-CP01", "route_id": route_id, "kind": "start",
                            "after_seg_count": 0, "name": None, "station_ref": None})
        if route_id == "R05":
            checkpoints += [
                {"checkpoint_id": "R05-CP02", "route_id": "R05", "kind": "fuel_station", "after_seg_count": 1,
                 "name": None, "station_ref": "SYN-ST-01"},
                {"checkpoint_id": "R05-CP03", "route_id": "R05", "kind": "waypoint", "after_seg_count": 2,
                 "name": None, "station_ref": None},
            ]
        checkpoints.append({"checkpoint_id": f"{route_id}-CP09", "route_id": route_id, "kind": "end",
                            "after_seg_count": len(parts), "name": None, "station_ref": None})
    return routes, segments, checkpoints


def eta(route_id: str, breaks: list[dict], pace=None, plan_id: str = "P-T", **kwargs):
    routes, segments, checkpoints = catalog()
    header, categories = pace if pace is not None else pace_table()
    route = next(r for r in routes if r["route_id"] == route_id)
    return compute_eta(route, segments, checkpoints, header, categories, plan_id=plan_id, departure_time=DEPART,
                       breaks=breaks, computed_at=COMPUTED, **kwargs)


def conforms(headers, rows, pace) -> list[str]:
    routes, segments, checkpoints = catalog()
    return validate_eta_output(headers, rows, routes, segments, checkpoints, pace[0], pace[1])


def t(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value)


BREAK_AT_WAYPOINT = [{"after_checkpoint_id": "R05-CP03", "duration_s": 900.0}]
BREAK_SETS = [
    [],
    BREAK_AT_WAYPOINT,
    [{"after_checkpoint_id": "R05-CP02", "duration_s": 600.0}],
    [{"after_checkpoint_id": "R05-CP02", "duration_s": 600.0}, {"after_checkpoint_id": "R05-CP03", "duration_s": 300.0}],
]


def test_synthetic_inputs_conform_to_contracts_2_and_3():
    assert validate_route_catalog(*catalog()) == []
    assert validate_pace_table(*pace_table()) == []
    assert validate_pace_table(*pace_table(c3_speed=None)) == []
    assert validate_pace_table(*pace_table(margin_coeff=0.2, margin_basis="default")) == []


# --- AC 1: stop_allow_s, eta_typ steps, eta_safe - eta_typ ----------------------------
def test_eta_follows_the_formula_worked_out_by_hand():
    """typ: 180, 120, 120, 360 s; stop allowance 0.05 / 0.10 / 0.20 / 0.05 of it: 9, 12, 24, 18 s;
    RIDE: 189, 321, 465, 843 s; margin 0.15 x RIDE: 28.35, 48.15, 69.75, 126.45 s. The 900 s break
    after segment 2 delays segments 2 and 3 and gets no margin."""
    header, rows = eta("R05", [])
    assert header["status"] == "ok" and header["margin_coeff"] == 0.15
    assert [r["typ_seg_time_s"] for r in rows] == [180.0, 120.0, 120.0, 360.0]
    assert [r["stop_allow_s"] for r in rows] == [9.0, 12.0, 24.0, 18.0]
    assert [r["eta_typ"][11:19] for r in rows] == ["07:03:09", "07:05:21", "07:07:45", "07:14:03"]
    assert [r["eta_safe"][11:19] for r in rows] == ["07:03:37", "07:06:09", "07:08:55", "07:16:09"]

    header, rows = eta("R05", BREAK_AT_WAYPOINT)
    assert [r["break_time_s"] for r in rows] == [0.0, 0.0, 900.0, 900.0]
    assert [r["eta_typ"][11:19] for r in rows] == ["07:03:09", "07:05:21", "07:22:45", "07:29:03"]
    assert [r["eta_safe"][11:19] for r in rows] == ["07:03:37", "07:06:09", "07:23:55", "07:31:09"]


@pytest.mark.parametrize("breaks", BREAK_SETS)
def test_eta_meets_the_stop_allowance_and_margin_invariants(breaks):
    pace = pace_table()
    header, rows = eta("R05", breaks, pace=pace)
    ratio = {"C1": 0.05, "C2": 0.10, "C3": 0.20}
    categories = ["C1", "C2", "C3", "C1"]
    ride, previous = 0.0, None
    for row, category in zip(rows, categories):
        assert row["stop_allow_s"] == pytest.approx(ratio[category] * row["typ_seg_time_s"], abs=1e-3)
        ride += row["typ_seg_time_s"] + row["stop_allow_s"]
        margin_s = (t(row["eta_safe"]) - t(row["eta_typ"])).total_seconds()
        assert margin_s == pytest.approx(0.15 * ride, abs=1.0)
        expected_typ = DEPART + dt.timedelta(seconds=ride + row["break_time_s"])
        assert abs((t(row["eta_typ"]) - expected_typ).total_seconds()) <= 1.0
        if previous is not None:
            step = (t(row["eta_typ"]) - t(previous["eta_typ"])).total_seconds()
            new_break = row["break_time_s"] - previous["break_time_s"]
            assert step == pytest.approx(row["typ_seg_time_s"] + row["stop_allow_s"] + new_break, abs=1.0)
        previous = row
    assert conforms([header], rows, pace) == []


# --- AC 2: a break adds only its own length --------------------------------------------
@pytest.mark.parametrize("breaks", BREAK_SETS[1:])
def test_a_break_shifts_eta_typ_and_eta_safe_by_its_length_only(breaks):
    _, without = eta("R05", [])
    _, with_break = eta("R05", breaks)
    for a, b in zip(without, with_break):
        assert b["typ_seg_time_s"] == a["typ_seg_time_s"] and b["stop_allow_s"] == a["stop_allow_s"]
        assert t(b["eta_safe"]) - t(b["eta_typ"]) == t(a["eta_safe"]) - t(a["eta_typ"])  # the margin is unchanged
        shift = dt.timedelta(seconds=b["break_time_s"])
        assert t(b["eta_typ"]) - t(a["eta_typ"]) == shift
        assert t(b["eta_safe"]) - t(a["eta_safe"]) == shift
    assert [r["break_time_s"] for r in without] == [0.0] * 4
    assert any(r["break_time_s"] > 0 for r in with_break)


# --- AC 3: unknown has no stop allowance and no time -------------------------------------
@pytest.mark.parametrize("breaks", [[], [{"after_checkpoint_id": "R05-CP03", "duration_s": 900.0}]])
def test_unknown_eta_has_no_stop_allowance_and_no_time(breaks):
    pace = pace_table(c3_speed=None)
    header, rows = eta("R05", breaks, pace=pace)
    assert header["status"] == "unknown" and header["unknown_reason"] == "no pace for category C3"
    assert len(rows) == 4
    for row in rows:
        assert row["typ_seg_time_s"] is None and row["stop_allow_s"] is None
        assert row["eta_typ"] is None and row["eta_safe"] is None
    assert [r["break_time_s"] for r in rows] == ([0.0, 0.0, 900.0, 900.0] if breaks else [0.0] * 4)
    assert conforms([header], rows, pace) == []


def test_only_the_route_categories_decide_unknown():
    pace = pace_table(c3_speed=None)
    header, rows = eta("R07", [], pace=pace)   # C1 and C2 only
    assert header["status"] == "ok" and [r["stop_allow_s"] for r in rows] == [6.0, 12.0]
    header, rows = eta("R06", [], pace=pace)   # uses C3
    assert header["status"] == "unknown" and all(r["stop_allow_s"] is None for r in rows)


# --- AC 4 and the added condition: margin_coeff comes from the pace table only --------------
@pytest.mark.parametrize("pace", [pace_table(), pace_table(margin_coeff=0.2, margin_basis="default"),
                                  pace_table(c3_speed=None)])
def test_eta_header_margin_coeff_is_the_pace_tables(pace):
    for route_id in ("R05", "R06"):
        header, _ = eta(route_id, [], pace=pace)
        assert header["margin_coeff"] == pace[0]["margin_coeff"]
        assert header["pace_version"] == pace[0]["pace_version"]
        header_checked, rows = eta(route_id, [], pace=pace, margin_coeff=pace[0]["margin_coeff"])
        assert header_checked == header   # passing the same value changes nothing


@pytest.mark.parametrize("given", [0.2, 0.1, 0.15000001, "0.15", float("nan"), True])
def test_a_caller_margin_coeff_that_differs_from_the_pace_table_is_an_error(given):
    with pytest.raises(ValueError, match="differs from the pace table's margin_coeff"):
        eta("R05", [], margin_coeff=given)


def test_the_caller_cannot_bring_back_a_default_margin():
    """0.20 is the default coefficient; with a loo_rule table of 0.15 it must be refused, not used."""
    with pytest.raises(ValueError, match="differs"):
        eta("R05", [], pace=pace_table(margin_coeff=0.15), margin_coeff=0.20)
    header, _ = eta("R05", [], pace=pace_table(margin_coeff=0.15))
    assert header["margin_coeff"] == 0.15


# --- missing or broken inputs: an error, never a default (H-4) -----------------------------
def _without_margin(pace):
    del pace[0]["margin_coeff"]


def _null_margin(pace):
    pace[0]["margin_coeff"] = None


def _nan_margin(pace):
    pace[0]["margin_coeff"] = math.nan


def _null_stop_ratio_with_pace(pace):
    pace[1][1]["stop_ratio"] = None


def _without_stop_ratio(pace):
    del pace[1][0]["stop_ratio"]


def _negative_stop_ratio(pace):
    pace[1][0]["stop_ratio"] = -0.05


def _infinite_stop_ratio(pace):
    pace[1][0]["stop_ratio"] = math.inf


def _missing_category(pace):
    del pace[1][2]


@pytest.mark.parametrize("damage", [_without_margin, _null_margin, _nan_margin, _null_stop_ratio_with_pace,
                                    _without_stop_ratio, _negative_stop_ratio, _infinite_stop_ratio,
                                    _missing_category])
def test_a_pace_table_that_breaks_contract_3_is_an_error(damage):
    pace = list(pace_table())  # fresh objects on every call
    damage(pace)
    with pytest.raises(ValueError, match="does not conform to contract 3"):
        eta("R05", [], pace=tuple(pace))


def test_route_segments_that_do_not_match_the_route_are_an_error():
    routes, segments, checkpoints = catalog()
    header, categories = pace_table()
    route = next(r for r in routes if r["route_id"] == "R05")
    kwargs = dict(plan_id="P", departure_time=DEPART, breaks=[], computed_at=COMPUTED)
    short = [s for s in segments if not (s["route_id"] == "R05" and s["seg_index"] == 3)]
    with pytest.raises(ValueError, match="exactly once"):
        compute_eta(route, short, checkpoints, header, categories, **kwargs)
    doubled = segments + [s for s in segments if s["route_id"] == "R05" and s["seg_index"] == 0]
    with pytest.raises(ValueError, match="exactly once"):
        compute_eta(route, doubled, checkpoints, header, categories, **kwargs)
    odd = [dict(s, seg_category="C4") if s["route_id"] == "R05" and s["seg_index"] == 1 else s for s in segments]
    with pytest.raises(ValueError, match="category"):
        compute_eta(route, odd, checkpoints, header, categories, **kwargs)


def test_departure_time_must_be_timezone_aware():
    routes, segments, checkpoints = catalog()
    with pytest.raises(ValueError, match="timezone-aware"):
        compute_eta(routes[0], segments, checkpoints, *pace_table(), plan_id="P",
                    departure_time=dt.datetime(2026, 11, 21, 7, 0), breaks=[], computed_at=COMPUTED)


# --- with a pace table built by build_pace_table (Issue #10) -------------------------------
def test_eta_from_a_pace_table_built_from_derived_segments():
    """Nine invented trips of three 1000 m segments at 60 km/h; the short stops are on the first
    (C1) segment only. The table's thresholds are (100, 300), the same scheme as the route."""
    rows, trip_ids = trips_three_categories([0, 5, 10, 15, 20, 25, 30, 35, 40])
    built = dt.datetime(2026, 11, 18, 9, 0, tzinfo=TAIPEI)
    pace = build_pace_table(rows, trip_ids, pace_version="user-02", min_segments=2, built_at=built)
    assert pace[0]["category_scheme"] == SCHEME and pace[0]["margin_basis"] == "loo_rule"
    header, eta_rows = eta("R05", BREAK_AT_WAYPOINT, pace=pace)
    assert header["status"] == "ok" and header["margin_coeff"] == pace[0]["margin_coeff"]
    ratio = {c["seg_category"]: c["stop_ratio"] for c in pace[1]}
    assert ratio["C2"] == ratio["C3"] == 0.0 and ratio["C1"] > 0
    for row, category in zip(eta_rows, ["C1", "C2", "C3", "C1"]):
        assert row["stop_allow_s"] == pytest.approx(ratio[category] * row["typ_seg_time_s"], abs=1e-3)
    assert eta_rows[1]["stop_allow_s"] == 0.0 and eta_rows[0]["stop_allow_s"] > 0
    assert conforms([header], eta_rows, pace) == []
