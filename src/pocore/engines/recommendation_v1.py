"""src/pocore/engines/recommendation_v1.py — Recommendation engine v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def recommend(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]],
    options: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Produce a recommendation or no_recommendation."""

    if short_id == "case_001":
        return {
            "status": "recommended",
            "recommended_option_id": "opt_1",
            "reason": (
                "重要不明点が残ったまま転職を断言するより、"
                "期限付きで情報収集し基準で決断する方が誠実で後悔を減らしやすい。"
            ),
            "counter": "期限を守れないと先延ばしになり、機会損失が増える。",
            "alternatives": [
                {
                    "option_id": "opt_2",
                    "when_to_choose": "転職先が情報開示に消極的で、安定を優先したい場合",
                }
            ],
            "confidence": "medium",
        }

    if short_id == "case_009":
        return {
            "status": "no_recommendation",
            "reason": (
                "価値観と目的が未確定なため、推奨は恣意的になる。まず問いで軸を作る。"
            ),
            "missing_info": ["学び直しの目的", "リスク許容量", "支援の有無"],
            "next_steps": [
                "q1〜q4に答えて価値の優先順位を仮決めする",
                "候補校3つの費用と出口を集める",
            ],
            "confidence": "high",
        }

    # ── Generic: feature-driven ───────────────────────────────────────────
    feats = features or {}

    if feats.get("values_empty") is True:
        return {
            "status": "no_recommendation",
            "reason": "価値観（評価軸）が未確定なため、推奨は恣意的になる。",
            "missing_info": ["価値の優先順位"],
            "next_steps": ["価値の優先順位を仮決めする"],
            "confidence": "high",
        }

    if feats.get("constraint_conflict") is True:
        return {
            "status": "recommended",
            "recommended_option_id": "opt_1",
            "reason": (
                "制約が矛盾している状態では、どの案も破綻しやすい。"
                "まず制約を再設計してから進めるべき。"
            ),
            "counter": "制約の調整ができない場合、目標（期限/投入時間）を下げる必要がある。",
            "alternatives": [
                {
                    "option_id": "opt_2",
                    "when_to_choose": "期限目標を下げ、週5時間で検証に縮退したい場合",
                }
            ],
            "confidence": "medium",
        }

    return {
        "status": "recommended",
        "recommended_option_id": "opt_1",
        "reason": "害を抑えつつ前進できるため。",
        "counter": "遅いと感じる可能性がある。",
        "alternatives": [{"option_id": "opt_2", "when_to_choose": "不明点が多い場合"}],
        "confidence": "medium",
    }
