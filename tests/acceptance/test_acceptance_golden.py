# SPDX-License-Identifier: AGPL-3.0-or-later
"""Golden diff tests for acceptance scenarios.

Phase 7 contract:
- Ensure AT-002..AT-008 (+AT-010 for >=8 total) are pinned with golden outputs.
- Keep comparisons deterministic by stripping volatile timestamps generated at runtime.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml

from po_core.app.composer import StubComposer

pytestmark = pytest.mark.acceptance

ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = Path(__file__).resolve().parent / "scenarios"
SCENARIOS_DIR = ROOT / "scenarios"


def _canonicalize(output: dict[str, Any]) -> dict[str, Any]:
    """Remove volatile fields (wall-clock-derived timestamps) before diff."""
    canonical = json.loads(json.dumps(output, ensure_ascii=False))
    canonical.get("meta", {}).pop("created_at", None)
    for step in canonical.get("trace", {}).get("steps", []):
        step.pop("started_at", None)
        step.pop("ended_at", None)
    return canonical


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize(
    "golden_path",
    sorted(GOLDEN_DIR.glob("at_*_expected.json")),
    ids=lambda p: p.stem,
)
def test_acceptance_golden_diff(golden_path: Path) -> None:
    golden = _load_json(golden_path)
    case_id = golden["case_id"]
    case = _load_yaml(SCENARIOS_DIR / f"{case_id}.yaml")

    composer = StubComposer(seed=42)
    actual = _canonicalize(composer.compose(case))

    assert actual == golden["expected"], (
        f"Golden mismatch for {golden['at_id']} ({case_id}). "
        f"To regenerate, update {golden_path.relative_to(ROOT)} with deterministic output."
    )
