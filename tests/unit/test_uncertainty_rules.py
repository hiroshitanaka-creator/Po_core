"""Unit tests for deterministic uncertainty level rules (FR-UNC-001)."""

from __future__ import annotations

from po_core.app.output_adapter import _build_uncertainty, _uncertainty_level


def test_uncertainty_level_high_when_unknowns_are_many() -> None:
    case = {
        "constraints": ["予算上限を守る"],
        "unknowns": ["A", "B", "C"],
    }

    assert _uncertainty_level(case) == "high"


def test_uncertainty_level_high_when_constraints_contradict() -> None:
    case = {
        "constraints": [
            "品質を最優先しつつ、即時にリリースする",
            "現有人員は維持しつつ、コストを削減する",
        ],
        "unknowns": [],
    }

    assert _uncertainty_level(case) == "high"


def test_uncertainty_level_medium_with_small_unknowns() -> None:
    case = {
        "constraints": ["予算上限を守る"],
        "unknowns": ["関係者の同意可否"],
    }

    assert _uncertainty_level(case) == "medium"


def test_build_uncertainty_keeps_schema_shape_for_low_level() -> None:
    case = {"constraints": "invalid", "unknowns": "invalid"}

    uncertainty = _build_uncertainty(case)

    assert uncertainty["overall_level"] == "low"
    assert uncertainty["reasons"]
    assert isinstance(uncertainty["assumptions"], list)
    assert isinstance(uncertainty["known_unknowns"], list)
