"""Pace table (contract 3) and ETA (contract 4)."""
from .table import (
    METHOD,
    build_pace_table,
    category_scheme,
    classify,
    compare_methods,
    compute_eta,
    create_pace_table,
    latest_user_pace_table,
    load_pace_table,
    loo_folds,
    margin_from_residuals,
    tercile_thresholds,
    timed_rows,
)

__all__ = [
    "METHOD",
    "build_pace_table",
    "category_scheme",
    "classify",
    "compare_methods",
    "compute_eta",
    "create_pace_table",
    "latest_user_pace_table",
    "load_pace_table",
    "loo_folds",
    "margin_from_residuals",
    "tercile_thresholds",
    "timed_rows",
]
