"""src/pocore/engines/ethics_v1.py — Ethics review engine v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

_ALL = ["integrity", "autonomy", "nonmaleficence", "justice", "accountability"]


def _append_unique(items: List[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _is_short_deadline(days_to_deadline: Any) -> bool:
    if not isinstance(days_to_deadline, int):
        return False
    return 0 <= days_to_deadline <= 7


def apply(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]],
    options: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Apply ethics review to options; return (options, ethics_summary)."""

    if short_id == "case_001":
        for opt in options:
            if opt.get("option_id") == "opt_1":
                opt["ethics_review"] = {
                    "principles_applied": [
                        "integrity",
                        "accountability",
                        "autonomy",
                    ],
                    "tradeoffs": [
                        {
                            "tension": "慎重さと機会損失の緊張",
                            "between": ["integrity", "opportunity"],
                            "mitigation": "期限付きで慎重さを維持しつつ機会損失を抑える",
                            "severity": "medium",
                        }
                    ],
                    "concerns": ["資金繰り等の不確実な事実を断言しない"],
                    "confidence": "high",
                }
            elif opt.get("option_id") == "opt_2":
                opt["ethics_review"] = {
                    "principles_applied": ["autonomy", "accountability"],
                    "tradeoffs": [
                        {
                            "tension": "安定と成長の緊張",
                            "between": ["economic_stability", "long_term_growth"],
                            "mitigation": "期限を切って成長機会の有無で判断する",
                            "severity": "medium",
                        }
                    ],
                    "concerns": ["現職が必ず変わるとは断言しない"],
                    "confidence": "medium",
                }
        summary = {
            "principles_used": _ALL,
            "tradeoffs": [
                {
                    "tension": "慎重さと機会損失の緊張",
                    "between": ["integrity", "opportunity"],
                    "mitigation": "期限付きにして先延ばしを防ぐ",
                    "severity": "medium",
                }
            ],
            "guardrails": [
                "不確実な事実を断言しない",
                "意思決定主体をユーザーから奪わない",
                "推奨には反証と代替案を併記する",
            ],
            "notes": "価値の衝突（成長/安定/家族時間）を前提に、トレードオフを開示する。",
        }
        return options, summary

    if short_id == "case_009":
        for opt in options:
            if opt.get("option_id") == "opt_1":
                opt["ethics_review"] = {
                    "principles_applied": [
                        "integrity",
                        "autonomy",
                        "accountability",
                    ],
                    "tradeoffs": [],
                    "concerns": ["価値観未確定で推奨を断言しない"],
                    "confidence": "high",
                }
            elif opt.get("option_id") == "opt_2":
                opt["ethics_review"] = {
                    "principles_applied": [
                        "autonomy",
                        "nonmaleficence",
                        "integrity",
                    ],
                    "tradeoffs": [
                        {
                            "tension": "自己実現と安全の緊張",
                            "between": ["autonomy", "nonmaleficence"],
                            "mitigation": "資金計画で害を抑える",
                            "severity": "high",
                        }
                    ],
                    "concerns": ["『学べば成功する』と断言しない"],
                    "confidence": "medium",
                }
        summary = {
            "principles_used": _ALL,
            "tradeoffs": [
                {
                    "tension": "自己実現と生活安定の緊張",
                    "between": ["autonomy", "nonmaleficence"],
                    "mitigation": "現職継続で安全を確保しつつ探索する",
                    "severity": "medium",
                }
            ],
            "guardrails": [
                "価値観未確定で推奨を断言しない",
                "意思決定主体をユーザーから奪わない",
            ],
            "notes": "このケースは『問いの層』が主役。",
        }
        return options, summary

    # ── Generic: feature-driven ───────────────────────────────────────────
    feats = features or {}
    conflict = feats.get("constraint_conflict") is True
    has_unknowns = isinstance(feats.get("unknowns_count"), int) and feats.get("unknowns_count") > 0
    has_many_stakeholders = (
        isinstance(feats.get("stakeholders_count"), int)
        and feats.get("stakeholders_count") > 1
    )
    short_deadline = _is_short_deadline(feats.get("days_to_deadline"))

    for opt in options:
        if conflict:
            review = {
                "principles_applied": [
                    "integrity",
                    "nonmaleficence",
                    "accountability",
                ],
                "tradeoffs": [
                    {
                        "tension": "野心と持続可能性の緊張",
                        "between": ["autonomy", "nonmaleficence"],
                        "mitigation": "制約を可視化して破綻条件を先に潰す",
                        "severity": "high",
                    }
                ],
                "concerns": ["矛盾した制約を無視して断言しない"],
                "confidence": "medium",
            }
        else:
            review = {
                "principles_applied": ["integrity", "autonomy"],
                "tradeoffs": [],
                "concerns": ["不確実な事実を断言しない"],
                "confidence": "medium",
            }

        if has_unknowns:
            _append_unique(
                review["concerns"],
                "前提と不確実性を明示する",
            )

        if has_many_stakeholders:
            _append_unique(review["principles_applied"], "justice")
            _append_unique(review["principles_applied"], "autonomy")
            review["tradeoffs"].append(
                {
                    "tension": "自己決定と外部性/公正の緊張",
                    "between": ["autonomy", "justice"],
                    "mitigation": "関係者影響を可視化し、同意可能な線で意思決定する",
                    "severity": "medium",
                }
            )

        if short_deadline:
            _append_unique(review["principles_applied"], "nonmaleficence")
            review["tradeoffs"].append(
                {
                    "tension": "速度と安全の緊張",
                    "between": ["autonomy", "nonmaleficence"],
                    "mitigation": "時間圧力下でも最小限の検証を維持する",
                    "severity": "medium",
                }
            )

        opt["ethics_review"] = review

    tradeoffs: List[Dict[str, Any]] = []
    if conflict:
        tradeoffs.append(
            {
                "tension": "速度と安全の緊張",
                "between": ["autonomy", "nonmaleficence"],
                "mitigation": "期限・実験・ガードレールで両立を狙う",
                "severity": "medium",
            }
        )
    if has_many_stakeholders:
        tradeoffs.append(
            {
                "tension": "自己決定と外部性/公正の緊張",
                "between": ["autonomy", "justice"],
                "mitigation": "関係者への影響を可視化し、同意可能な進め方を選ぶ",
                "severity": "medium",
            }
        )
    if short_deadline:
        tradeoffs.append(
            {
                "tension": "速度と安全（nonmaleficence）の緊張",
                "between": ["autonomy", "nonmaleficence"],
                "mitigation": "時間制約下でも検証を省略しない",
                "severity": "medium",
            }
        )

    guardrails = [
        "不確実な事実を断言しない",
        "意思決定主体をユーザーから奪わない",
        "推奨には反証と代替案を併記する",
    ]
    if has_unknowns:
        _append_unique(guardrails, "前提と不確実性を明示する")
    if has_many_stakeholders:
        _append_unique(guardrails, "関係者への影響と同意を考慮する")
    if short_deadline:
        _append_unique(guardrails, "時間圧力下でも検証を省略しない")

    summary = {
        "principles_used": _ALL,
        "tradeoffs": tradeoffs,
        "guardrails": guardrails,
        "notes": "M2以降で倫理ルールを拡張予定。現段階ではガードレール中心。",
    }
    return options, summary
