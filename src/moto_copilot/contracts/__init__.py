"""Data contracts v0.2 (DESIGN.md §5): schemas and validation."""
from .schemas import CONTRACT_VERSION
from .validate import (
    checkpoint_arrival,
    expected_break_times,
    pace_eligible,
    validate_dataset,
    validate_derived_segments,
    validate_eta_output,
    validate_pace_table,
    validate_public_private_pair,
    validate_route_catalog,
)

__all__ = [
    "CONTRACT_VERSION",
    "checkpoint_arrival",
    "expected_break_times",
    "pace_eligible",
    "validate_dataset",
    "validate_derived_segments",
    "validate_eta_output",
    "validate_pace_table",
    "validate_public_private_pair",
    "validate_route_catalog",
]
