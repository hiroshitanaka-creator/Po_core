from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest

from pocore.runner import run_case_file

ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "scenarios" / "case_005.yaml"
FIXED_NOW = "2026-02-22T00:00:00Z"


def _run_once() -> Dict[str, Any]:
    return run_case_file(
        CASE_PATH,
        seed=0,
        deterministic=True,
        now=FIXED_NOW,
    )


def _apply_policy_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("pocore.policy_v1.UNKNOWN_BLOCK", 2)
    monkeypatch.setattr("pocore.policy_v1.TIME_PRESSURE_DAYS", 3)
    monkeypatch.setattr("pocore.orchestrator.UNKNOWN_BLOCK", 2)
    monkeypatch.setattr("pocore.orchestrator.TIME_PRESSURE_DAYS", 3)


@pytest.mark.parametrize("policy_mode", ["default", "override"])
def test_policy_mode_is_deterministic(
    policy_mode: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    if policy_mode == "override":
        _apply_policy_override(monkeypatch)

    first = _run_once()
    second = _run_once()

    assert first == second


def test_policy_override_does_not_leak_into_normal_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline = _run_once()

    _apply_policy_override(monkeypatch)
    _ = _run_once()

    monkeypatch.undo()
    after_override = _run_once()

    assert after_override == baseline


def test_ethics_non_interference_is_kept_under_policy_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _apply_policy_override(monkeypatch)
    baseline = _run_once()

    def _fake_ethics_apply(
        case: Dict[str, Any],
        *,
        short_id: str,
        features: Optional[Dict[str, Any]],
        options: List[Dict[str, Any]],
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        for opt in options:
            opt["ethics_review"] = {
                "principles_applied": ["integrity", "justice", "nonmaleficence"],
                "tradeoffs": [
                    {
                        "tension": "override下で倫理説明を増やしたダミー",
                        "between": ["autonomy", "justice"],
                        "mitigation": "判断説明を厚くする",
                        "severity": "high",
                    }
                ],
                "concerns": ["この倫理レビューはrecommendationへ介入しない"],
                "confidence": "low",
            }

        return options, {
            "principles_used": [
                "integrity",
                "autonomy",
                "nonmaleficence",
                "justice",
                "accountability",
            ],
            "tradeoffs": [
                {
                    "tension": "override下のダミー倫理トレードオフ",
                    "between": ["autonomy", "justice"],
                    "mitigation": "説明責任で緩和",
                    "severity": "high",
                }
            ],
            "guardrails": ["倫理出力は推奨裁定に介入しない"],
            "notes": "monkeypatch under policy override",
        }

    monkeypatch.setattr("pocore.orchestrator.ethics_v1.apply", _fake_ethics_apply)

    patched = _run_once()

    assert patched["recommendation"] == baseline["recommendation"]
