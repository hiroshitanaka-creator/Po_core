from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from pocore.runner import run_case_file

ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "scenarios" / "case_010.yaml"


def test_planning_changes_do_not_change_recommendation(monkeypatch) -> None:
    baseline = run_case_file(
        CASE_PATH,
        seed=0,
        deterministic=True,
        now="2026-02-22T00:00:00Z",
    )

    def _fake_generate_options(
        case: Dict[str, Any],
        *,
        short_id: str,
        features: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        return [
            {
                "option_id": "opt_1",
                "title": "ダミー案1",
                "description": "planning非介入検証",
                "action_plan": [
                    {"step": "[Track A] 可逆対応だけ先に行う"},
                    {"step": "[Track B] 不足情報を集める"},
                ],
                "pros": ["検証用"],
                "cons": ["検証用"],
                "risks": [
                    {
                        "risk": "ダミーリスク",
                        "severity": "low",
                        "mitigation": "検証後に戻す",
                    }
                ],
                "feasibility": {
                    "effort": "low",
                    "timeline": "1 day",
                    "confidence": "low",
                },
                "uncertainty": {
                    "overall_level": "medium",
                    "reasons": ["dummy"],
                    "assumptions": ["dummy"],
                    "known_unknowns": ["dummy"],
                },
                "ethics_review": {
                    "principles_applied": ["integrity"],
                    "tradeoffs": [],
                    "concerns": [],
                    "confidence": "low",
                },
                "responsibility_review": {
                    "decision_owner": "user",
                    "stakeholders": [],
                    "accountability_notes": "",
                    "confidence": "low",
                },
            },
            {
                "option_id": "opt_2",
                "title": "ダミー案2",
                "description": "planning非介入検証",
                "action_plan": [{"step": "[Track A] まず共有"}],
                "pros": ["検証用"],
                "cons": ["検証用"],
                "risks": [
                    {
                        "risk": "ダミーリスク",
                        "severity": "low",
                        "mitigation": "検証後に戻す",
                    }
                ],
                "feasibility": {
                    "effort": "low",
                    "timeline": "1 day",
                    "confidence": "low",
                },
                "uncertainty": {
                    "overall_level": "medium",
                    "reasons": ["dummy"],
                    "assumptions": ["dummy"],
                    "known_unknowns": ["dummy"],
                },
                "ethics_review": {
                    "principles_applied": ["integrity"],
                    "tradeoffs": [],
                    "concerns": [],
                    "confidence": "low",
                },
                "responsibility_review": {
                    "decision_owner": "user",
                    "stakeholders": [],
                    "accountability_notes": "",
                    "confidence": "low",
                },
            },
        ]

    monkeypatch.setattr(
        "pocore.orchestrator.generator_stub.generate_options", _fake_generate_options
    )

    patched = run_case_file(
        CASE_PATH,
        seed=0,
        deterministic=True,
        now="2026-02-22T00:00:00Z",
    )

    assert patched["recommendation"] == baseline["recommendation"]
