"""Validator. Only rule 3's range judgement exists so far (SPEC-B1 B1-5, Issue #8); the other rules,
reason codes and RuleResult are not built here.

This package must not import `planner` or any LLM client (DESIGN.md §9.1); the rule 3 module also
stays clear of `sources`, `routing`, `routes` and `pace` (SPEC-B1 CL-B1-6 item 1).
"""
from .rule3 import FAIL, PASS, UNKNOWN, Rule3Outcome, judge_rule3

__all__ = ["FAIL", "PASS", "UNKNOWN", "Rule3Outcome", "judge_rule3"]
