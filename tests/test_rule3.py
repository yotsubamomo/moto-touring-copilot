"""Rule 3 range judgement of SPEC-B1 B1-5 (Issue #8; SPEC-RESOLUTION-001 §3.1 and SB9-T1 to SB9-T5).

Every route here is invented: round cumulative distances in metres and hand-picked rain probability
classes. None of it is a place, a ride or a forecast. The expected ranges are worked out by hand from
the definition (SPEC-B1 CL-B1-6) and written down before the function is called.
"""
from __future__ import annotations

import ast
import itertools
import json
import math
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from moto_copilot.validator import FAIL, PASS, UNKNOWN, Rule3Outcome, judge_rule3

VALIDATOR_DIR = Path(__file__).resolve().parents[1] / "src" / "moto_copilot" / "validator"
SRC_DIR = VALIDATOR_DIR.parents[1]

LOW, MED, HIGH, NONE = "LOW", "MEDIUM", "HIGH_ALERT", None
ALL_CLASSES = (LOW, MED, HIGH, NONE)


# ---------------------------------------------------------------- the five acceptance criteria


def test_round_trip_with_an_alert_only_on_the_outbound_leg_passes():
    """AC 1 (SB9-T1): outbound segments 0-2 carry the alert, the return 3-5 has none."""
    out = judge_rule3([10_000, 20_000, 30_000, 40_000, 50_000, 60_000], "round_trip",
                      [HIGH, HIGH, HIGH, LOW, MED, LOW], outbound_segments=3)
    assert out == Rule3Outcome(in_range=(False, False, False, True, True, True), result=PASS)


@pytest.mark.parametrize("classes", [
    [LOW, LOW, NONE, HIGH, NONE, LOW],
    [LOW, LOW, LOW, NONE, NONE, HIGH],
    [NONE, HIGH, NONE, HIGH, NONE, NONE],
])
def test_round_trip_alert_in_range_fails_even_with_missing_rain_probability(classes):
    """AC 2 (SB9-T2), round trip: the return has an alert and also segments without a probability."""
    out = judge_rule3([5_000, 9_000, 15_000, 21_000, 25_000, 30_000], "round_trip", classes,
                      outbound_segments=3)
    assert out.result == FAIL


@pytest.mark.parametrize("classes", [
    [LOW, LOW, LOW, NONE, HIGH],
    [LOW, LOW, LOW, HIGH, NONE],
])
def test_one_way_alert_in_range_fails_even_with_missing_rain_probability(classes):
    """AC 2 (SB9-T2), one way: T = 10 000, range starts beyond 8 000, so segments 3 and 4 are in."""
    out = judge_rule3([2_000, 4_000, 7_000, 9_000, 10_000], "one_way", classes)
    assert out.in_range == (False, False, False, True, True)
    assert out.result == FAIL


@pytest.mark.parametrize("trip_type, ends, k, classes", [
    ("round_trip", [10_000, 20_000, 30_000, 40_000], 2, [LOW, LOW, MED, NONE]),
    ("round_trip", [10_000, 20_000, 30_000, 40_000], 2, [HIGH, HIGH, NONE, NONE]),
    ("one_way", [2_000, 4_000, 7_000, 9_000, 10_000], None, [LOW, LOW, LOW, NONE, MED]),
    ("one_way", [2_000, 4_000, 7_000, 9_000, 10_000], None, [HIGH, NONE, HIGH, LOW, NONE]),
])
def test_no_alert_but_missing_rain_probability_in_range_is_unknown(trip_type, ends, k, classes):
    """AC 3 (SB9-T3, result only; reason codes are out of scope)."""
    assert judge_rule3(ends, trip_type, classes, outbound_segments=k).result == UNKNOWN


# One-way routes with the range worked out by hand: in range iff the segment's end is beyond 0.8 x T.
ONE_WAY_CASES = [
    # ends, expected in_range, note
    ([10_000], (True,), "one segment: the whole route"),
    ([2_000, 8_000, 10_000], (False, False, True), "segment 1 ends exactly at 0.8 x T = 8 000"),
    ([2_000, 7_000, 9_000, 10_000], (False, False, True, True), "segment 2 crosses 8 000"),
    ([2_000, 8_001, 10_000], (False, True, True), "segment 1 ends 1 m beyond 8 000"),
    ([1_000, 2_000, 3_000, 4_000, 5_000], (False, False, False, False, True), "T = 5 000, 0.8 x T = 4 000"),
    ([9_500, 10_000], (True, True), "segment 0 alone covers 0 to 9 500"),
    ([500, 1_000, 49_000, 50_000], (False, False, True, True), "a long segment from 1 000 to 49 000"),
    ([12_345, 23_456, 34_567], (False, False, True), "0.8 x T = 27 653.6"),
    ([3_000.5, 8_000.64, 10_000.8], (False, False, True), "0.8 x 10 000.8 = 8 000.64 exactly"),
    ([3_000.5, 8_000.65, 10_000.8], (False, True, True), "0.01 m beyond 8 000.64"),
    ([0.1, 0.242, 0.3], (False, True, True), "0.8 x 0.3 = 0.24; 0.242 is beyond it"),
    ([0.1, 0.232, 0.29], (False, False, True), "0.8 x 0.29 = 0.232 exactly (0.8 * 0.29 in floats is below it)"),
]


@pytest.mark.parametrize("ends, expected, note", ONE_WAY_CASES, ids=[c[2] for c in ONE_WAY_CASES])
def test_one_way_range_is_the_last_20_percent_with_crossing_segments(ends, expected, note):
    """AC 4 (SB9-T4) and the added condition: a segment ending exactly at 0.8 x T is not in range."""
    out = judge_rule3(ends, "one_way", [LOW] * len(ends))
    assert out.in_range == expected
    assert out.result == PASS


def _last_20_percent_by_overlap(ends):
    """An independent statement of the definition: the segment [start, end] shares a stretch of
    positive length with the last 20% (0.8 x T, T] of the cumulative distance."""
    exact = [Fraction(repr(e)) if isinstance(e, float) else Fraction(e) for e in ends]
    total = exact[-1]
    starts = [Fraction(0)] + exact[:-1]
    window_start = total * 4 / 5
    return tuple(min(end, total) - max(start, window_start) > 0 for start, end in zip(starts, exact))


def _result_from_definition(in_range, classes):
    inside = [c for c, flag in zip(classes, in_range) if flag]
    if HIGH in inside:
        return FAIL
    if NONE in inside:
        return UNKNOWN
    return PASS


ROUTES = [
    [2_000, 8_000, 10_000],
    [1_000, 3_000, 7_999, 8_000, 8_001, 10_000],
    [4_000, 6_000, 9_000],
    [12_345, 23_456, 34_567],
    [3_000.5, 8_000.64, 10_000.8],
    [100],
]


@pytest.mark.parametrize("ends", ROUTES)
def test_one_way_results_equal_the_last_20_percent_definition_for_every_class_combination(ends):
    """AC 4 (SB9-T4): across every class combination the range and the result match the definition
    written independently above (overlap with the last 20%, then FAIL > UNKNOWN > PASS)."""
    expected_range = _last_20_percent_by_overlap(ends)
    for classes in itertools.product(ALL_CLASSES, repeat=len(ends)):
        out = judge_rule3(ends, "one_way", list(classes))
        assert out.in_range == expected_range
        assert out.result == _result_from_definition(expected_range, classes), classes


def test_one_way_ignores_the_outbound_count():
    """CL-B1-6 item 3: k is not used for a one-way trip, whatever is passed."""
    ends, classes = [2_000, 7_000, 9_000, 10_000], [HIGH, NONE, LOW, LOW]
    reference = judge_rule3(ends, "one_way", classes)
    assert reference == Rule3Outcome((False, False, True, True), PASS)
    for k in (0, 1, 2, 3, 4, 99, -1):
        assert judge_rule3(ends, "one_way", classes, outbound_segments=k) == reference


@pytest.mark.parametrize("trip_type, ends, k", [
    ("one_way", [2_000, 4_000, 7_000, 9_000, 10_000], None),
    ("round_trip", [10_000, 20_000, 30_000, 40_000, 50_000], 2),
    ("round_trip", [10_000, 20_000, 30_000, 40_000, 50_000], 4),
])
def test_segments_outside_the_range_do_not_affect_the_result(trip_type, ends, k):
    """AC 5 (SB9-T5): for each fixed set of in-range classes, every combination of classes outside
    the range (missing probability and alerts included) gives the same result."""
    in_range = judge_rule3(ends, trip_type, [LOW] * len(ends), outbound_segments=k).in_range
    inside = [i for i, flag in enumerate(in_range) if flag]
    outside = [i for i, flag in enumerate(in_range) if not flag]
    assert inside and outside
    for inside_classes in itertools.product(ALL_CLASSES, repeat=len(inside)):
        results = set()
        for outside_classes in itertools.product(ALL_CLASSES, repeat=len(outside)):
            classes = [None] * len(ends)
            for i, c in zip(inside, inside_classes):
                classes[i] = c
            for i, c in zip(outside, outside_classes):
                classes[i] = c
            results.add(judge_rule3(ends, trip_type, classes, outbound_segments=k).result)
        assert results == {_result_from_definition([True] * len(inside), inside_classes)}


def test_missing_rain_probability_only_outside_the_range_still_passes():
    """AC 5 (SB9-T5), the plain case: one way and round trip."""
    assert judge_rule3([2_000, 4_000, 7_000, 9_000, 10_000], "one_way",
                       [NONE, NONE, NONE, LOW, MED]).result == PASS
    assert judge_rule3([10_000, 20_000, 30_000, 40_000], "round_trip",
                       [NONE, NONE, LOW, LOW], outbound_segments=2).result == PASS


# ---------------------------------------------------------------- round trip range and k


@pytest.mark.parametrize("n, k", [(2, 1), (3, 1), (3, 2), (6, 1), (6, 3), (6, 5)])
def test_round_trip_range_is_every_segment_from_k_on(n, k):
    """CL-B1-6 item 4: seg_index >= k is in range, whatever the distances."""
    expected = tuple(i >= k for i in range(n))
    even = [1_000 * (i + 1) for i in range(n)]
    uneven = [sum(range(1, i + 2)) * 700 for i in range(n)]  # lengths 700, 1 400, 2 100, ...
    for ends in (even, uneven):
        assert judge_rule3(ends, "round_trip", [LOW] * n, outbound_segments=k).in_range == expected


def test_round_trip_range_does_not_use_the_last_20_percent():
    """Plan A: the whole return is checked, not the route's last 20%. Segment 2 (20 000 to 30 000)
    is in the return but ends well before 0.8 x T = 48 000."""
    out = judge_rule3([10_000, 20_000, 30_000, 40_000, 50_000, 60_000], "round_trip",
                      [LOW, LOW, HIGH, LOW, LOW, LOW], outbound_segments=2)
    assert out.in_range == (False, False, True, True, True, True)
    assert out.result == FAIL


@pytest.mark.parametrize("k", [0, 4, 5, -1, None, True, False, 1.0, 2.0, "2"])
def test_round_trip_with_an_invalid_outbound_count_is_an_error(k):
    """Added condition (CL-B1-6 item 4): k must be an integer with 0 < k < number of segments."""
    with pytest.raises(ValueError, match="outbound_segments"):
        judge_rule3([10_000, 20_000, 30_000, 40_000], "round_trip", [LOW] * 4, outbound_segments=k)


def test_round_trip_with_one_segment_has_no_valid_outbound_count():
    for k in (0, 1, None):
        with pytest.raises(ValueError, match="outbound_segments"):
            judge_rule3([10_000], "round_trip", [LOW], outbound_segments=k)


# ---------------------------------------------------------------- result order


@pytest.mark.parametrize("classes, expected", [
    ([LOW, LOW], PASS),
    ([MED, MED], PASS),
    ([LOW, MED], PASS),
    ([LOW, NONE], UNKNOWN),
    ([NONE, NONE], UNKNOWN),
    ([MED, HIGH], FAIL),
    ([HIGH, NONE], FAIL),
    ([NONE, HIGH], FAIL),
    ([HIGH, HIGH], FAIL),
])
def test_three_valued_result_inside_the_range(classes, expected):
    """CL-B1-6 item 5: FAIL if any alert, else UNKNOWN if any missing, else PASS. `MEDIUM` is a rain
    probability like `LOW` and is not an alert."""
    out = judge_rule3([30_000, 40_000, 50_000], "round_trip", [HIGH, *classes], outbound_segments=1)
    assert out.in_range == (False, True, True)
    assert out.result == expected


# ---------------------------------------------------------------- invalid input: an error, no result


@pytest.mark.parametrize("ends", [
    [],
    [0, 1_000],
    [-1_000, 1_000],
    [1_000, 1_000, 2_000],
    [1_000, 3_000, 2_000],
    [1_000, math.nan, 3_000],
    [1_000, math.inf],
    [1_000, True],
    [1_000, "2000"],
    [1_000, None],
    "1000",
    None,
    {1_000, 2_000},
])
def test_invalid_cumulative_distances_are_an_error(ends):
    n = len(ends) if isinstance(ends, list) else 2
    for trip_type, k in (("one_way", None), ("round_trip", 1)):
        with pytest.raises(ValueError, match="cumulative_m"):
            judge_rule3(ends, trip_type, [LOW] * n, outbound_segments=k)


@pytest.mark.parametrize("classes", [
    [LOW, LOW],
    [LOW, LOW, LOW, LOW],
    [LOW, LOW, "low"],
    [LOW, LOW, "HIGH"],
    [LOW, LOW, ""],
    [LOW, LOW, "NONE"],
    [LOW, LOW, 70],
    [LOW, LOW, math.nan],
    "LOW",
    None,
])
def test_invalid_rain_probability_classes_are_an_error(classes):
    """An unknown class is not read as LOW or as missing; it stops the judgement."""
    for trip_type, k in (("one_way", None), ("round_trip", 1)):
        with pytest.raises(ValueError, match="pop_classes"):
            judge_rule3([1_000, 2_000, 3_000], trip_type, classes, outbound_segments=k)


@pytest.mark.parametrize("trip_type", ["oneway", "ROUND_TRIP", "loop", "", None])
def test_unknown_trip_type_is_an_error(trip_type):
    with pytest.raises(ValueError, match="trip_type"):
        judge_rule3([1_000, 2_000, 3_000], trip_type, [LOW] * 3, outbound_segments=1)


# ---------------------------------------------------------------- purity


def test_inputs_are_not_modified_and_the_answer_is_repeatable():
    ends, classes = [2_000, 7_000, 9_000, 10_000], [LOW, NONE, HIGH, LOW]
    ends_copy, classes_copy = list(ends), list(classes)
    first = judge_rule3(ends, "one_way", classes)
    assert judge_rule3(ends, "one_way", classes) == first
    assert (ends, classes) == (ends_copy, classes_copy)
    assert isinstance(first.in_range, tuple) and len(first.in_range) == len(ends)
    assert judge_rule3(tuple(ends), "one_way", tuple(classes)) == first


# ---------------------------------------------------------------- import restriction (CL-B1-6 item 1)

FORBIDDEN = ("moto_copilot.planner", "moto_copilot.sources", "moto_copilot.routing",
             "moto_copilot.routes", "moto_copilot.pace", "anthropic", "openai")
# The files Python loads for `import moto_copilot.validator.rule3`, besides moto_copilot/__init__.py.
RULE3_FILES = ("__init__.py", "rule3.py")


def _imports_in(source: str) -> list[str]:
    """Absolute module names imported by source code that lives in the moto_copilot.validator
    package (relative imports are resolved against it). Dynamic imports are reported as markers."""
    package = ["moto_copilot", "validator"]
    names = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                prefix = ".".join(package[: len(package) - (node.level - 1)])
                if node.module:
                    names.append(f"{prefix}.{node.module}")
                else:
                    names += [f"{prefix}.{alias.name}" for alias in node.names]
            else:
                names.append(node.module)
        elif isinstance(node, ast.Call) and getattr(node.func, "id", None) == "__import__":
            names.append("<__import__>")
        elif isinstance(node, ast.Attribute) and node.attr == "import_module":
            names.append("<importlib.import_module>")
    return names


def _violations(names: list[str]) -> list[str]:
    """Imports outside the standard library and this package, or in the forbidden list."""
    bad = []
    for name in names:
        top = name.split(".")[0]
        if name.startswith("<") or any(name == f or name.startswith(f + ".") for f in FORBIDDEN):
            bad.append(name)
        elif top == "moto_copilot":
            if name != "moto_copilot.validator" and not name.startswith("moto_copilot.validator."):
                bad.append(name)
        elif top not in sys.stdlib_module_names and top != "__future__":
            bad.append(name)
    return bad


def test_the_import_checker_catches_forbidden_and_relative_imports():
    """The static checker itself: `from .. import pace` resolves to moto_copilot.pace and is caught,
    as are the other forbidden modules, third-party packages and dynamic imports."""
    source = """
from .. import pace
from ..routes import catalog
from ..contracts import schemas
from .rule3 import judge_rule3
from . import rule3
import moto_copilot.planner
import anthropic
import jsonschema
import importlib
importlib.import_module('moto_copilot.sources')
__import__('moto_copilot.routing')
import math, os.path
"""
    names = _imports_in(source)
    assert names[:5] == ["moto_copilot.pace", "moto_copilot.routes", "moto_copilot.contracts",
                         "moto_copilot.validator.rule3", "moto_copilot.validator.rule3"]
    assert sorted(_violations(names)) == sorted([
        "moto_copilot.pace", "moto_copilot.routes", "moto_copilot.contracts", "moto_copilot.planner",
        "anthropic", "jsonschema", "<importlib.import_module>", "<__import__>"])
    assert "math" in names and "os.path" in names and "importlib" in names


@pytest.mark.parametrize("filename", RULE3_FILES)
def test_rule3_module_imports_only_the_standard_library(filename):
    """Static check (CL-B1-6 item 1): every import is the standard library or this package."""
    names = _imports_in((VALIDATOR_DIR / filename).read_text(encoding="utf-8"))
    assert names, filename
    assert _violations(names) == [], filename


def test_importing_rule3_loads_no_forbidden_or_third_party_module():
    """Runtime check (CL-B1-6 item 1) in a fresh interpreter: the modules that the import adds are
    the standard library and moto_copilot.validator only."""
    code = (
        "import json, sys\n"
        "before = set(sys.modules)\n"
        "import moto_copilot.validator.rule3 as rule3\n"
        "print(json.dumps({'added': sorted(set(sys.modules) - before), 'file': rule3.__file__}))\n"
    )
    env = {**os.environ, "PYTHONPATH": str(SRC_DIR)}
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env,
                          check=True, cwd=SRC_DIR)
    report = json.loads(done.stdout)
    assert Path(report["file"]).resolve() == VALIDATOR_DIR / "rule3.py"  # the source under test
    added = report["added"]
    assert "moto_copilot.validator.rule3" in added
    for name in added:
        assert not any(name == f or name.startswith(f + ".") for f in FORBIDDEN), name
        top = name.split(".")[0]
        if top == "moto_copilot":
            assert name in ("moto_copilot", "moto_copilot.validator", "moto_copilot.validator.rule3"), name
        else:
            assert top in sys.stdlib_module_names, name
