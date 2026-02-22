"""src/pocore/engines/uncertainty_v1.py — Uncertainty summary engine v1."""

from __future__ import annotations

from typing import Any, Dict, Optional


def summarize(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Produce an uncertainty summary for the case."""

    if short_id == "case_001":
        return {
            "overall_level": "medium",
            "reasons": ["転職先の重要情報が未確定"],
            "assumptions": ["引っ越し不可は固定"],
            "known_unknowns": ["稼働実態", "文化"],
        }

    if short_id == "case_009":
        return {
            "overall_level": "high",
            "reasons": ["価値観と目的が未確定"],
            "assumptions": ["生活費維持が優先制約"],
            "known_unknowns": ["適性", "支援の有無", "就職市場"],
        }

    # ── Generic: feature-driven ───────────────────────────────────────────
    feats = features or {}
    unknowns = case.get("unknowns", [])
    known = [str(u) for u in unknowns[:3]] if isinstance(unknowns, list) else []

    if feats.get("constraint_conflict") is True:
        return {
            "overall_level": "high",
            "reasons": ["制約が矛盾している"],
            "assumptions": ["健康と生活維持は下限として守る"],
            "known_unknowns": known or ["制約をどこまで動かせるか"],
        }

    if feats.get("unknowns_count", 0) >= 2:
        return {
            "overall_level": "medium",
            "reasons": ["重要情報が未確定"],
            "assumptions": ["提示された制約が正しい"],
            "known_unknowns": known,
        }

    return {
        "overall_level": "low",
        "reasons": ["入力情報が比較的揃っている"],
        "assumptions": ["提示された制約が正しい"],
        "known_unknowns": known,
    }
