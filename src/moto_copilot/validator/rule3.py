"""Rule 3 range judgement (SPEC-B1 B1-5, Issue #8; SPEC-RESOLUTION-001 §3.1, plan A).

Rule 3 is this project's own weather policy. The function below is given the rain probability class
of each segment (`LOW`, `MEDIUM`, `HIGH_ALERT`, or `None` when the segment has no rain probability)
and does not know how a class was obtained. `HIGH_ALERT` is the project's own "high rain probability
reminder" class; it is not an official weather warning and does not mark a road as dangerous.

Range (SPEC-001 4.8 `in_rule3_range`; SPEC-B1 CL-B1-6 items 3 and 4):

- `one_way`: the last 20% of the route's cumulative distance, segments that cross into it included.
  With T the route's total length, a segment is in range when its end lies strictly beyond 0.8 x T;
  a segment ending exactly at 0.8 x T does not cross into it. The outbound count is not used.
- `round_trip`: every segment after the turnaround point, i.e. `seg_index >= k` where k is the number
  of outbound segments; k must satisfy 0 < k < number of segments.

Result (CL-B1-6 item 5): `FAIL` when any segment in range is `HIGH_ALERT`; otherwise `UNKNOWN` when
any segment in range has no rain probability; otherwise `PASS`. Segments outside the range do not
affect the result, so a `PASS` says nothing about rain on the outbound leg.

Not here (Issue #8, excluded scope): reason codes and their order, the RuleResult and WeatherSegment
schemas, mapping segments to townships, reading forecasts, and every other rule of the validator.

The module is a pure function on the standard library only. It must not import `planner`, any LLM
client, `sources`, `routing`, `routes` or `pace` (CL-B1-6 item 1; DESIGN.md §9.1).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import NamedTuple, Optional, Sequence

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"

ONE_WAY = "one_way"
ROUND_TRIP = "round_trip"
TRIP_TYPES = (ONE_WAY, ROUND_TRIP)

HIGH_ALERT = "HIGH_ALERT"
POP_CLASSES = ("LOW", "MEDIUM", HIGH_ALERT)  # None: the segment has no rain probability

# One-way range: the end lies strictly beyond RANGE_START_FRACTION x T, i.e. 5 x end > 4 x T.
RANGE_START_FRACTION = Fraction(4, 5)


class Rule3Outcome(NamedTuple):
    """`in_range[i]` tells whether segment i is in rule 3's range; `result` is PASS, FAIL or UNKNOWN."""

    in_range: tuple[bool, ...]
    result: str


def judge_rule3(
    cumulative_m: Sequence[float],
    trip_type: str,
    pop_classes: Sequence[Optional[str]],
    outbound_segments: Optional[int] = None,
) -> Rule3Outcome:
    """Decide which segments are in rule 3's range and the rule's three-valued result.

    `cumulative_m[i]` is the cumulative distance at the end of segment i (strictly increasing, the
    first one above 0; the last one is the route's total length). `pop_classes[i]` is segment i's
    rain probability class or None. `outbound_segments` is k, the number of outbound segments; it is
    required for `round_trip` and not used for `one_way`.

    Any input that does not meet these conditions raises ValueError; there is no default result.
    """
    ends = _segment_ends(cumulative_m)
    classes = _pop_classes(pop_classes, len(ends))
    if trip_type == ONE_WAY:
        in_range = _one_way_range(ends)
    elif trip_type == ROUND_TRIP:
        in_range = _round_trip_range(len(ends), outbound_segments)
    else:
        raise ValueError(f"trip_type must be one of {TRIP_TYPES}, got {trip_type!r}")

    in_range_classes = [c for c, inside in zip(classes, in_range) if inside]
    if any(c == HIGH_ALERT for c in in_range_classes):
        result = FAIL
    elif any(c is None for c in in_range_classes):
        result = UNKNOWN
    else:
        result = PASS
    return Rule3Outcome(in_range=tuple(in_range), result=result)


def _segment_ends(cumulative_m: Sequence[float]) -> list[Fraction]:
    """The segment ends as exact rationals of the decimal values given, checked to be finite, above 0 and
    strictly increasing."""
    if isinstance(cumulative_m, (str, bytes)) or not isinstance(cumulative_m, Sequence):
        raise ValueError("cumulative_m must be a sequence of cumulative distances")
    if not cumulative_m:
        raise ValueError("cumulative_m must have at least one segment")
    ends: list[Fraction] = []
    for i, value in enumerate(cumulative_m):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"cumulative_m[{i}] must be a finite number, got {value!r}")
        # repr() is the shortest decimal that gives back the same float, so a boundary written as
        # 8000.64 for T = 10000.8 compares as exactly 0.8 x T instead of through binary rounding.
        end = Fraction(repr(value)) if isinstance(value, float) else Fraction(value)
        previous = ends[-1] if ends else Fraction(0)
        if end <= previous:
            raise ValueError(
                f"cumulative_m must be strictly increasing and above 0; cumulative_m[{i}] = {value!r}")
        ends.append(end)
    return ends


def _pop_classes(pop_classes: Sequence[Optional[str]], n_segments: int) -> list[Optional[str]]:
    if isinstance(pop_classes, (str, bytes)) or not isinstance(pop_classes, Sequence):
        raise ValueError("pop_classes must be a sequence with one class (or None) per segment")
    if len(pop_classes) != n_segments:
        raise ValueError(
            f"pop_classes has {len(pop_classes)} entries but there are {n_segments} segments")
    for i, value in enumerate(pop_classes):
        if value is not None and value not in POP_CLASSES:
            raise ValueError(f"pop_classes[{i}] must be one of {POP_CLASSES} or None, got {value!r}")
    return list(pop_classes)


def _one_way_range(ends: list[Fraction]) -> list[bool]:
    start = RANGE_START_FRACTION * ends[-1]
    return [end > start for end in ends]


def _round_trip_range(n_segments: int, outbound_segments: Optional[int]) -> list[bool]:
    k = outbound_segments
    if isinstance(k, bool) or not isinstance(k, int):
        raise ValueError(f"outbound_segments (k) must be an integer for a round trip, got {k!r}")
    if not 0 < k < n_segments:
        raise ValueError(
            f"outbound_segments (k) must satisfy 0 < k < {n_segments} (the number of segments), got {k}")
    return [seg_index >= k for seg_index in range(n_segments)]
