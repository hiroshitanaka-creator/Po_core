# SPDX-License-Identifier: AGPL-3.0-or-later
"""Acceptance test fixtures.

Provides scenario-loading helpers and the shared StubComposer instance used
by AT-001 through AT-010+.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

import pytest
import yaml

from po_core.app.composer import StubComposer

_SCENARIOS_DIR = pathlib.Path(__file__).parent.parent.parent / "scenarios"
_SCHEMA_PATH = (
    pathlib.Path(__file__).parent.parent.parent
    / "docs"
    / "spec"
    / "output_schema_v1.json"
)


def _load_scenario(case_id: str) -> dict[str, Any]:
    """Load a scenario YAML file by case prefix (e.g., 'case_001')."""
    pattern = f"{case_id}*.yaml"
    matches = list(_SCENARIOS_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Scenario file not found: {_SCENARIOS_DIR / pattern}")
    with matches[0].open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)  # type: ignore[no-any-return]


def _load_output_schema() -> dict[str, Any]:
    """Load the output_schema_v1.json."""
    with _SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)  # type: ignore[no-any-return]


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def output_schema() -> dict[str, Any]:
    """The output_schema_v1.json as a dict (session-scoped for performance)."""
    return _load_output_schema()


@pytest.fixture(scope="session")
def composer() -> StubComposer:
    """Shared StubComposer with deterministic seed=42."""
    return StubComposer(seed=42)


# Per-scenario fixtures (function-scoped so each test gets fresh data)


@pytest.fixture()
def case_001() -> dict[str, Any]:
    return _load_scenario("case_001")


@pytest.fixture()
def case_002() -> dict[str, Any]:
    return _load_scenario("case_002")


@pytest.fixture()
def case_003() -> dict[str, Any]:
    return _load_scenario("case_003")


@pytest.fixture()
def case_004() -> dict[str, Any]:
    return _load_scenario("case_004")


@pytest.fixture()
def case_005() -> dict[str, Any]:
    return _load_scenario("case_005")


@pytest.fixture()
def case_006() -> dict[str, Any]:
    return _load_scenario("case_006")


@pytest.fixture()
def case_007() -> dict[str, Any]:
    return _load_scenario("case_007")


@pytest.fixture()
def case_008() -> dict[str, Any]:
    return _load_scenario("case_008")


@pytest.fixture()
def case_009() -> dict[str, Any]:
    return _load_scenario("case_009")


@pytest.fixture()
def case_010() -> dict[str, Any]:
    return _load_scenario("case_010")
