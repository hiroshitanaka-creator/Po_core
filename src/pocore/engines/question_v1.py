"""src/pocore/engines/question_v1.py — Question generator engine v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def generate(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Generate clarifying questions (max 5)."""

    if short_id == "case_001":
        return [
            {
                "question_id": "q1",
                "question": "オファーの有効期限と延長可否は？",
                "priority": 1,
                "why_needed": "情報収集に使える時間を決めるため。",
                "assumption_if_unanswered": "期限は短いと仮定する",
                "optional": False,
            },
            {
                "question_id": "q2",
                "question": "ランウェイ（資金繰り）と評価制度（期待成果）は？",
                "priority": 1,
                "why_needed": "経済安定と期待値ギャップのリスク評価に直結するため。",
                "assumption_if_unanswered": "不利な条件を織り込む",
                "optional": False,
            },
        ]

    if short_id == "case_009":
        return [
            {
                "question_id": "q1",
                "question": "学び直しで得たい目的は？（例：収入、自由、創造性）",
                "priority": 1,
                "why_needed": "目的がないと評価軸が定義できないため。",
                "assumption_if_unanswered": "働き方の自由を暫定目的とする",
                "optional": False,
            },
            {
                "question_id": "q2",
                "question": "収入低下をどれだけ許容できる？（0%/-10%/-30%など）",
                "priority": 1,
                "why_needed": "実行可能な選択肢を絞るため。",
                "assumption_if_unanswered": "収入低下は許容しない",
                "optional": False,
            },
            {
                "question_id": "q3",
                "question": "学び直しに投入できる時間は週どれくらい？",
                "priority": 2,
                "why_needed": "計画（学校/独学/並行）を現実化するため。",
                "assumption_if_unanswered": "週5時間と仮定する",
                "optional": False,
            },
            {
                "question_id": "q4",
                "question": "支援（貯金・家族理解・奨学金）はある？",
                "priority": 3,
                "why_needed": "資金計画とリスク耐性の評価に必要。",
                "assumption_if_unanswered": "支援なしで安全側に倒す",
                "optional": True,
            },
        ]

    # ── Generic: feature-driven ───────────────────────────────────────────
    feats = features or {}
    questions: List[Dict[str, Any]] = []

    if feats.get("values_empty") is True:
        questions.append(
            {
                "question_id": "q_values_1",
                "question": "最優先する価値は何？（例：安定、成長、自由、関係性）",
                "priority": 1,
                "why_needed": "価値が定義されないと推奨が恣意的になるため。",
                "assumption_if_unanswered": "安定を優先する",
                "optional": False,
            }
        )

    if feats.get("constraint_conflict") is True:
        questions.extend(
            [
                {
                    "question_id": "q_conflict_1",
                    "question": (
                        "矛盾している制約のうち、絶対に守るのはどれ？"
                        "（時間/収入/健康/期限など）"
                    ),
                    "priority": 1,
                    "why_needed": "優先順位がないと制約の再設計ができないため。",
                    "assumption_if_unanswered": "健康と収入を最優先と仮定する",
                    "optional": False,
                },
                {
                    "question_id": "q_conflict_2",
                    "question": "週5時間の内訳は？（平日/週末、連続時間の有無）",
                    "priority": 2,
                    "why_needed": "実行可能な検証タスクへ分解するため。",
                    "assumption_if_unanswered": "週末に2h×2回が確保できると仮定する",
                    "optional": False,
                },
                {
                    "question_id": "q_conflict_3",
                    "question": "現職の副業規定（許可制/禁止/競業）を確認した？",
                    "priority": 2,
                    "why_needed": "実行可能性（法務・契約）を左右するため。",
                    "assumption_if_unanswered": "許可が必要と仮定し、確認を最優先にする",
                    "optional": False,
                },
            ]
        )

    return questions[:5]
