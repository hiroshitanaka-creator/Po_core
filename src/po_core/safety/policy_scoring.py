"""
Policy Scoring - SafetyVerdict を数値化
========================================

Gate の判断を 0.0〜1.0 の実数に落とす。
Pareto の safety 軸で使用。

DEPENDENCY RULES:
- domain のみ依存
- aggregator から呼ばれるが、safety 実装の詳細は見せない
"""

from __future__ import annotations

from po_core.domain.safety_verdict import Decision, SafetyVerdict


def policy_score(v: SafetyVerdict) -> float:
    """
    SafetyVerdict を 0.0〜1.0 にスコア化。

    高いほど安全に通りやすい:
    - ALLOW: 1.0（満点）
    - REVISE: 0.70 - ペナルティ（修正要求の重さ）
    - REJECT: 0.0（最低点）

    Args:
        v: Gate の判定結果

    Returns:
        0.0〜1.0 のスコア
    """
    if v.decision == Decision.ALLOW:
        return 1.0

    if v.decision == Decision.REJECT:
        return 0.0

    # REVISE：要求が多いほど落とす
    s = 0.70
    s -= 0.06 * len(v.rule_ids)
    s -= 0.05 * len(v.required_changes)
    s -= 0.02 * len(v.reasons)
    return max(0.0, min(1.0, s))


__all__ = ["policy_score"]
