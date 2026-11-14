"""Shared fixtures. The dataset is a mock: invented values, not ride data."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

MOCK_DATASET = Path(__file__).parent / "fixtures" / "contract_v02" / "mock_dataset.json"
_LOADED = json.loads(MOCK_DATASET.read_text(encoding="utf-8"))


@pytest.fixture
def data() -> dict:
    """A fresh copy of the mock dataset, safe to mutate inside a test."""
    return copy.deepcopy(_LOADED)


@pytest.fixture
def private_rows(data) -> list[dict]:
    """The private version of the derived segment table: the public rows plus start_time."""
    rows = []
    for row in data["derived_segments"]:
        rows.append({**row, "start_time": data["private_start_times"][row["trip_id"]][row["seg_index"]]})
    return rows
