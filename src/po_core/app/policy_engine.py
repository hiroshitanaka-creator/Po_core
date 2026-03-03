# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Policy engine v1 — deterministic recommendation arbitration.

REQ-ARB-001: recommendation は policy_v1 の裁定ルールで arbitration_code を返す。
REQ-TRC-001: compose_output.metrics に arbitration_code を格納する。

Arbitration codes (deterministic, derived from case features):
    VALUES_EMPTY        — values is empty; no confident recommendation
    BLOCKED             — W_Ethics Gate rejected the input
    HIGH_UNCERTAINTY    — unknowns >= 5; too uncertain to recommend
    CONSTRAINT_CONFLICT — contradictory constraints detected
    RECOMMEND_OPT_001   — opt_001 recommended (main proposal)
"""

from __future__ import annotations

from typing import Any

# Arbitration code constants
ARB_VALUES_EMPTY = "VALUES_EMPTY"
ARB_BLOCKED = "BLOCKED"
ARB_HIGH_UNCERTAINTY = "HIGH_UNCERTAINTY"
ARB_CONSTRAINT_CONFLICT = "CONSTRAINT_CONFLICT"
ARB_RECOMMEND = "RECOMMEND_OPT_001"

_CONTRADICTION_PAIRS = [
    (("早", "即", "迅速", "speed", "fast"), ("慎重", "品質", "quality")),
    (("維持", "keep"), ("削減", "減ら", "reduce")),
]


def _detect_constraint_conflict(constraints: list[str]) -> bool:
    normalized = " ".join(str(c).lower() for c in constraints)
    for left_terms, right_terms in _CONTRADICTION_PAIRS:
        if any(t in normalized for t in left_terms) and any(
            t in normalized for t in right_terms
        ):
            return True
    return False


def arbitrate(
    case: dict[str, Any],
    run_result: dict[str, Any],
) -> tuple[str, str]:
    """Return (arbitration_code, recommended_option_id).

    Applies policy_v1 rules in priority order and returns the first matching
    arbitration code.  The evaluation is fully deterministic given the same
    case and run_result.

    Args:
        case:       Validated case dict (from input_schema_v1).
        run_result: Return value of po_core.app.api.run().

    Returns:
        Tuple of (arbitration_code, recommended_option_id).
        recommended_option_id is "opt_001" for RECOMMEND, else "".
    """
    values: list[str] = list(case.get("values", []) or [])
    unknowns: list[str] = list(case.get("unknowns", []) or [])
    constraints: list[str] = list(case.get("constraints", []) or [])
    status: str = str(run_result.get("status", "ok")).lower()
    verdict: dict[str, Any] = run_result.get("verdict") or {}
    gate_decision: str = str(verdict.get("decision", "")).upper()

    # P1: Pipeline blocked by W_Ethics Gate
    if status == "blocked" or gate_decision in {"REJECT", "ESCALATE"}:
        return ARB_BLOCKED, ""

    # P2: Values empty — cannot determine what to optimize for
    if not values:
        return ARB_VALUES_EMPTY, ""

    # P3: Contradictory constraints — structurally irresolvable
    if constraints and _detect_constraint_conflict(constraints):
        return ARB_CONSTRAINT_CONFLICT, ""

    # P4: Too many unknowns — high uncertainty prevents recommendation
    if len(unknowns) >= 5:
        return ARB_HIGH_UNCERTAINTY, ""

    # P5: Default — recommend main proposal
    return ARB_RECOMMEND, "opt_001"


def build_recommendation(
    case: dict[str, Any],
    run_result: dict[str, Any],
    arbitration_code: str,
    recommended_option_id: str,
) -> dict[str, Any]:
    """Build the recommendation block from arbitration result.

    Args:
        case:                  Validated case dict.
        run_result:            Pipeline result.
        arbitration_code:      From arbitrate().
        recommended_option_id: From arbitrate().

    Returns:
        Schema-compliant recommendation dict.
    """
    unknowns: list[str] = list(case.get("unknowns", []) or [])
    values: list[str] = list(case.get("values", []) or [])

    if arbitration_code == ARB_BLOCKED:
        return {
            "status": "no_recommendation",
            "reason": "安全評価によりこの入力への推奨は提供できません。",
            "missing_info": [],
            "next_steps": ["入力内容を修正の上、再度お試しください。"],
            "confidence": "low",
        }

    if arbitration_code == ARB_VALUES_EMPTY:
        return {
            "status": "no_recommendation",
            "reason": "価値観・優先事項が不明確なため、推奨を断言できません。",
            "missing_info": ["重視する価値観（例: 公平・自律・安全）の明確化"],
            "next_steps": [
                "価値観の優先順位付けワークを実施する（重要度 1〜5 で評価）",
                "ステークホルダーと価値観を共有・合意形成する",
                "価値観が明確になった後に再検討する",
            ],
            "confidence": "low",
        }

    if arbitration_code == ARB_HIGH_UNCERTAINTY:
        return {
            "status": "no_recommendation",
            "reason": f"重要な未知事項が {len(unknowns)} 件あり、現時点では特定の選択肢を推奨できません。",
            "missing_info": list(unknowns[:3]),
            "next_steps": [
                "未知事項の優先度を評価し、最重要情報から収集する",
                "情報収集フェーズを設けて不確実性を低減する",
                "情報が揃った時点で再度 Po_core に相談する",
            ],
            "confidence": "low",
        }

    if arbitration_code == ARB_CONSTRAINT_CONFLICT:
        return {
            "status": "no_recommendation",
            "reason": "制約条件に矛盾が検出されました。矛盾を解消してから判断することを推奨します。",
            "missing_info": ["制約の矛盾解消（優先順位付けまたは条件緩和）"],
            "next_steps": [
                "相矛盾する制約を列挙し、どちらを優先するか関係者と合意する",
                "条件を緩和できる余地がないか検討する",
                "制約を整理した後に再検討する",
            ],
            "confidence": "low",
        }

    # RECOMMEND_OPT_001
    proposal: dict[str, Any] = run_result.get("proposal") or {}
    confidence_raw = float(proposal.get("confidence", 0.5))
    conf_label = (
        "high" if confidence_raw >= 0.7 else ("medium" if confidence_raw >= 0.45 else "low")
    )

    reason_parts = ["価値観と制約を踏まえた哲学的考察により、主要選択肢が最もバランスが取れています。"]
    if values:
        reason_parts.append(f"重視する価値観「{'・'.join(values[:2])}」との整合性が高い。")

    return {
        "status": "recommended",
        "recommended_option_id": recommended_option_id,
        "reason": "".join(reason_parts),
        "counter": (
            "ただし不明点が残るため、慎重路線（opt_002）も検討に値します。"
            "情報が揃っていない状態での決定にはリスクが伴います。"
        ),
        "alternatives": [
            {
                "option_id": "opt_002",
                "when_to_choose": (
                    "重要な不明点が解消できない場合、またはリスク許容度が低い場合"
                ),
            }
        ],
        "confidence": conf_label,
    }
