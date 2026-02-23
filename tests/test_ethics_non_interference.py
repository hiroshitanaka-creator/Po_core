from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pocore.runner import run_case_file


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "scenarios" / "case_010.yaml"


def test_ethics_changes_do_not_change_recommendation(monkeypatch) -> None:
    baseline = run_case_file(
        CASE_PATH,
        seed=0,
        deterministic=True,
        now="2026-02-22T00:00:00Z",
    )

    def _fake_apply(
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
                        "tension": "倫理の緊張を最大化したダミー",
                        "between": ["autonomy", "justice"],
                        "mitigation": "倫理説明を増やす",
                        "severity": "high",
                    }
                ],
                "concerns": [
                    "この倫理レビューはrecommendationへ介入しない",
                    "ダミーの倫理懸念",
                ],
                "confidence": "low",
            }
        return options, {
            "principles_used": ["integrity", "autonomy", "nonmaleficence", "justice", "accountability"],
            "tradeoffs": [
                {
                    "tension": "ダミー倫理トレードオフ",
                    "between": ["autonomy", "justice"],
                    "mitigation": "説明責任で緩和",
                    "severity": "high",
                }
            ],
            "guardrails": ["倫理出力は推奨裁定に介入しない"],
            "notes": "monkeypatch for non-interference test",
        }

    monkeypatch.setattr("pocore.orchestrator.ethics_v1.apply", _fake_apply)

    patched = run_case_file(
        CASE_PATH,
        seed=0,
        deterministic=True,
        now="2026-02-22T00:00:00Z",
    )

    assert patched["recommendation"] == baseline["recommendation"]
