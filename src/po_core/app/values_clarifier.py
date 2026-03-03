# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Values Clarification Pack v1.

REQ-VALUES-001: features.values_empty が true のとき、
    questions（最大5・決定論順序）と action_plan（最大5ステップ・決定論順序）で
    価値軸獲得の手続きを出力する。

推奨裁定（status / recommended_option_id / arbitration_code）には介入しない。
"""

from __future__ import annotations

from typing import Any

# Fixed, deterministic value clarification questions (REQ-VALUES-001).
# Ordered by importance; only the first 5 are emitted.
_VALUE_CLARIFICATION_QUESTIONS: list[dict[str, Any]] = [
    {
        "question_id": "q_vc_01",
        "question": (
            "この状況で「うまくいった」と感じるのは、どんな状態のときですか？"
            "最も大切にしたい結果を具体的にイメージしてみてください。"
        ),
        "priority": 1,
        "why_needed": "重視する価値観が不明瞭な状態では推奨の方向性を定めることができないため",
        "assumption_if_unanswered": "価値観が不明確なまま保守的な選択肢を前提とします",
        "optional": False,
    },
    {
        "question_id": "q_vc_02",
        "question": (
            "今回の判断で「絶対に避けたいこと」は何ですか？"
            "許容できないリスク・損失・状態を具体的に教えてください。"
        ),
        "priority": 2,
        "why_needed": "ネガティブ制約が価値観の輪郭を明確にし、選択肢の絞り込みに役立つため",
        "assumption_if_unanswered": "損失回避を最優先と仮定します",
        "optional": False,
    },
    {
        "question_id": "q_vc_03",
        "question": (
            "この判断の結果が 1 年後・5 年後の自分にどう影響することを望みますか？"
            "短期 vs 長期でどちらを優先しますか？"
        ),
        "priority": 3,
        "why_needed": "時間軸による価値観の優先順位が選択肢評価に大きく影響するため",
        "assumption_if_unanswered": "短期・長期のバランスを等価と仮定します",
        "optional": False,
    },
    {
        "question_id": "q_vc_04",
        "question": (
            "この決断に影響を受ける人（家族・同僚・関係者）の幸福を、"
            "自分の利益と比べてどの程度重視しますか？"
        ),
        "priority": 4,
        "why_needed": "他者への影響の重み付けが責任評価と選択肢設計に影響するため",
        "assumption_if_unanswered": "自分と他者の利益を等価と仮定します",
        "optional": True,
    },
    {
        "question_id": "q_vc_05",
        "question": (
            "「公平さ」「自由」「安全」「誠実さ」「成長」の中で、"
            "今回の判断に最も関わるものを 1〜3 つ選んでください。"
        ),
        "priority": 5,
        "why_needed": "5 倫理原則との対応を確認し、評価軸を固定するため",
        "assumption_if_unanswered": "すべての価値を等価と仮定して評価します",
        "optional": True,
    },
]

# Deterministic action plan for value clarification (REQ-VALUES-001, max 5 steps).
_VALUE_CLARIFICATION_ACTION_PLAN: list[dict[str, Any]] = [
    {
        "step": "ステップ 1：「避けたいこと」を書き出す（15 分）",
        "rationale": "ネガティブ制約を明確化することで価値観の輪郭を掴む（損失回避から逆算）",
    },
    {
        "step": "ステップ 2：「理想の結果」を 3 つ書く（15 分）",
        "rationale": "ポジティブ目標を列挙し、重複・矛盾を確認する",
    },
    {
        "step": "ステップ 3：重要度で順位付け（10 分）",
        "rationale": "1 位〜3 位に絞ることで判断軸を確定し、選択肢評価の基準を作る",
    },
    {
        "step": "ステップ 4：価値観を言語化し関係者と共有（任意）",
        "rationale": "価値観の共有が合意形成を早め、説明責任を果たしやすくする",
    },
    {
        "step": "ステップ 5：価値観を整理した後で Po_core に再相談",
        "rationale": "価値観が明確になった状態で再検討することで推奨の精度が向上する",
    },
]


def needs_values_clarification(case: dict[str, Any]) -> bool:
    """Return True when values is empty (REQ-VALUES-001 trigger)."""
    values = case.get("values", [])
    return not bool(values)


def build_values_clarification_questions(
    case: dict[str, Any],
    unknowns_questions: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build question list for values clarification.

    Prepends value-clarification questions (q_vc_01..05) before unknowns
    questions. Total capped at 5.

    Args:
        case:               Case dict (used for unknowns context).
        unknowns_questions: Questions already generated from unknowns.

    Returns:
        Combined, capped-at-5 question list.
    """
    vc_questions = list(_VALUE_CLARIFICATION_QUESTIONS[:3])  # top 3 (non-optional)
    extra = list(_VALUE_CLARIFICATION_QUESTIONS[3:])

    combined: list[dict[str, Any]] = vc_questions
    for q in unknowns_questions or []:
        if len(combined) >= 5:
            break
        # Downgrade priority for unknowns questions (they follow vc questions)
        q_copy = dict(q)
        q_copy["priority"] = min(len(combined) + 1, 5)
        q_copy["optional"] = True
        combined.append(q_copy)

    # Fill remaining slots with optional vc questions
    for q in extra:
        if len(combined) >= 5:
            break
        combined.append(q)

    return combined[:5]


def build_values_clarification_action_plan() -> list[dict[str, Any]]:
    """Return the deterministic 5-step values clarification action plan."""
    return list(_VALUE_CLARIFICATION_ACTION_PLAN)
