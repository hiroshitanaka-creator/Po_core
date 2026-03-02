# SPDX-License-Identifier: AGPL-3.0-or-later
"""Acceptance test fixtures.

Provides scenario-loading helpers and the shared StubComposer instance used
by AT-001 through AT-010+.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any, Callable

import pytest
import yaml
from jsonschema import Draft202012Validator

from po_core.app.composer import StubComposer

_SCENARIOS_DIR = pathlib.Path(__file__).parent.parent.parent / "scenarios"
_SCHEMA_PATH = (
    pathlib.Path(__file__).parent.parent.parent
    / "docs"
    / "spec"
    / "output_schema_v1.json"
)


def _load_scenario_by_pattern(pattern: str) -> dict[str, Any]:
    """Load a scenario YAML/JSON file by glob pattern."""
    matches = sorted(_SCENARIOS_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Scenario file not found: {_SCENARIOS_DIR / pattern}")

    scenario_path = matches[0]
    with scenario_path.open(encoding="utf-8") as fh:
        if scenario_path.suffix.lower() == ".json":
            return json.load(fh)  # type: ignore[no-any-return]
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
def validate_output_schema(output_schema: dict[str, Any]) -> Callable[[dict[str, Any], str], None]:
    """Return a reusable output-schema validator for acceptance tests."""

    validator = Draft202012Validator(output_schema)

    def _validate(output: dict[str, Any], test_id: str) -> None:
        errors = sorted(validator.iter_errors(output), key=lambda err: list(err.path))
        if errors:
            msg = f"[{test_id}] AT-OUT-001 FAIL — schema validation errors:\n"
            msg += "\n".join(f"  • {e.message} (path: {list(e.path)})" for e in errors)
            pytest.fail(msg)

    return _validate


@pytest.fixture(scope="session")
def scenario_loader() -> Callable[[str], dict[str, Any]]:
    """Load scenario files from scenarios/ by case prefix (e.g., 'case_001')."""

    def _load(case_id: str) -> dict[str, Any]:
        return _load_scenario_by_pattern(f"{case_id}*.yaml")

    return _load


@pytest.fixture(scope="session")
def composer() -> StubComposer:
    """Shared StubComposer with deterministic seed=42."""
    return StubComposer(seed=42)


# Per-scenario fixtures (function-scoped so each test gets fresh data)


@pytest.fixture()
def case_001(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_001")


@pytest.fixture()
def case_002(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_002")


@pytest.fixture()
def case_003(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_003")


@pytest.fixture()
def case_004(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_004")


@pytest.fixture()
def case_005(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_005")


@pytest.fixture()
def case_006(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_006")


@pytest.fixture()
def case_007(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_007")


@pytest.fixture()
def case_008(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_008")


@pytest.fixture()
def case_009(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_009")


@pytest.fixture()
def case_010(scenario_loader: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    return scenario_loader("case_010")
