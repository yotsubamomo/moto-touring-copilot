"""Simplified input guard for the UI-0 skeleton (GitHub Issue #12, section 2).

This is a demo matcher that shows the fixed guard message. The exact patterns
belong to a later implementation Ticket (SPEC-001 7.12); this module is not that
check. The skeleton sends nothing anywhere, guarded or not.

Blocked: a street term (路、街、巷、弄、段) followed by a number and 「號」
(「中正路 123 號」「中正路一段 123 號」); a number with 「號」 followed by a floor
(「123 號 5 樓」); a pair of decimal numbers that looks like latitude and
longitude. Not blocked: road names such as 「國道 3 號」「台 9 線」.

Standard library only (CL-UI0-1).
"""

from __future__ import annotations

import re

_HOUSE_NUMBER = re.compile(r"[路街巷弄段]\s*\d+\s*號")
_FLOOR_CONTEXT = re.compile(r"\d+\s*號\s*\d+\s*樓")
_COORDINATE_PAIR = re.compile(r"-?\d{1,3}\.\d{3,}\s*[,，、 ]\s*-?\d{1,3}\.\d{3,}")


def guard_hits(text: str) -> bool:
    """Return True when ``text`` looks like it has a house number or a coordinate pair."""
    return bool(_HOUSE_NUMBER.search(text) or _FLOOR_CONTEXT.search(text) or _COORDINATE_PAIR.search(text))
