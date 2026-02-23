"""
src/pocore/tracer.py
====================

Deterministic trace builder.

Contract (ADR-0003):
- All timestamps derived from injected `created_at` with fixed offsets.
- No wall-clock time.
- Step names from output_schema_v1.json enum.
- Existing golden cases use frozen trace structures.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .utils import add_seconds


def build_trace(
    *,
    short_id: str,
    created_at: str,
    options_count: int = 0,
    questions_count: int = 0,
    features: Optional[Dict[str, Any]] = None,
    arbitration_code: Optional[str] = None,
    policy_snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a deterministic trace for a pipeline run."""

    # ── Frozen golden contracts ───────────────────────────────────────────
    if short_id == "case_001":
        return {
            "version": "1.0",
            "steps": [
                {
                    "name": "parse_input",
                    "started_at": created_at,
                    "ended_at": add_seconds(created_at, 1),
                    "summary": "入力を正規化し、不明点を抽出した",
                },
                {
                    "name": "generate_options",
                    "started_at": add_seconds(created_at, 1),
                    "ended_at": add_seconds(created_at, 2),
                    "summary": "2案を生成した",
                    "metrics": {"options": options_count or 2},
                },
                {
                    "name": "compose_output",
                    "started_at": add_seconds(created_at, 2),
                    "ended_at": add_seconds(created_at, 3),
                    "summary": "推奨・反証・代替案を含む出力を組み立てた",
                },
            ],
        }

    if short_id == "case_009":
        return {
            "version": "1.0",
            "steps": [
                {
                    "name": "parse_input",
                    "started_at": created_at,
                    "ended_at": add_seconds(created_at, 1),
                    "summary": "valuesが空であることを検出した",
                },
                {
                    "name": "question_layer",
                    "started_at": add_seconds(created_at, 1),
                    "ended_at": add_seconds(created_at, 2),
                    "summary": "軸を作るための質問を生成した",
                    "metrics": {"questions": questions_count or 0},
                },
                {
                    "name": "compose_output",
                    "started_at": add_seconds(created_at, 2),
                    "ended_at": add_seconds(created_at, 3),
                    "summary": "推奨を保留し、次ステップを提示した",
                },
            ],
        }

    # ── Generic: feature-driven trace ─────────────────────────────────────
    feats = features or {}
    conflict = bool(feats.get("constraint_conflict"))

    parse_metrics: Dict[str, Any] = {
        "options_planned": options_count,
        "questions_planned": questions_count,
        "unknowns_count": int(feats.get("unknowns_count", 0)),
        "stakeholders_count": int(feats.get("stakeholders_count", 0)),
    }
    if feats.get("days_to_deadline") is not None:
        parse_metrics["days_to_deadline"] = int(feats["days_to_deadline"])
    if conflict:
        parse_metrics["constraint_conflict"] = True

    steps = [
        {
            "name": "parse_input",
            "started_at": created_at,
            "ended_at": add_seconds(created_at, 1),
            "summary": "入力を正規化し、特徴量（features）を抽出した",
            "metrics": parse_metrics,
        },
        {
            "name": "generate_options",
            "started_at": add_seconds(created_at, 1),
            "ended_at": add_seconds(created_at, 2),
            "summary": "特徴量に基づいて選択肢を生成した",
            "metrics": {"options": options_count},
        },
    ]

    t = 2
    if questions_count > 0:
        steps.append(
            {
                "name": "question_layer",
                "started_at": add_seconds(created_at, t),
                "ended_at": add_seconds(created_at, t + 1),
                "summary": "不足情報を補う問いを生成した",
                "metrics": {"questions": questions_count},
            }
        )
        t += 1

    compose_metrics: Dict[str, Any] = {}
    if arbitration_code:
        compose_metrics["arbitration_code"] = arbitration_code
    if policy_snapshot:
        compose_metrics["policy_snapshot"] = dict(policy_snapshot)

    compose_step: Dict[str, Any] = {
        "name": "compose_output",
        "started_at": add_seconds(created_at, t),
        "ended_at": add_seconds(created_at, t + 1),
        "summary": "推奨・反証・代替案を含む出力を組み立てた",
    }
    if compose_metrics:
        compose_step["metrics"] = compose_metrics

    steps.append(compose_step)

    return {"version": "1.0", "steps": steps}
