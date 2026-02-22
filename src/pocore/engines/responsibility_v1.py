"""src/pocore/engines/responsibility_v1.py — Responsibility review engine v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


def _map_stakeholders(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    st = case.get("stakeholders", [])
    if isinstance(st, list) and len(st) > 0:
        out: List[Dict[str, Any]] = []
        for s in st:
            if not isinstance(s, dict):
                continue
            name = str(s.get("name", "")).strip()
            role = str(s.get("role", "")).strip()
            impact = str(s.get("impact", "")).strip()
            if name and role and impact:
                out.append({"name": name, "role": role, "impact": impact})
        if out:
            return out
    return [{"name": "自分", "role": "意思決定主体", "impact": "結果責任を負う"}]


def apply(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]],
    options: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Apply responsibility review to options; return (options, responsibility_summary)."""

    if short_id == "case_001":
        for opt in options:
            if opt.get("option_id") == "opt_1":
                opt["responsibility_review"] = {
                    "decision_owner": "user",
                    "stakeholders": [
                        {
                            "name": "自分",
                            "role": "意思決定主体",
                            "impact": "キャリア・収入に影響",
                        },
                        {
                            "name": "家族",
                            "role": "生活の共同体",
                            "impact": "時間配分・制約に影響",
                        },
                        {
                            "name": "現職チーム",
                            "role": "協働者",
                            "impact": "引き継ぎに影響",
                        },
                    ],
                    "accountability_notes": (
                        "最終判断はユーザー。転職する場合は家族合意と引き継ぎ計画を前提にする。"
                    ),
                    "confidence": "high",
                }
            elif opt.get("option_id") == "opt_2":
                opt["responsibility_review"] = {
                    "decision_owner": "user",
                    "stakeholders": [
                        {
                            "name": "自分",
                            "role": "意思決定主体",
                            "impact": "キャリア・収入に影響",
                        },
                        {
                            "name": "家族",
                            "role": "生活の共同体",
                            "impact": "時間配分に影響",
                        },
                    ],
                    "accountability_notes": (
                        "交渉結果を関係者に説明し、必要なら次の選択肢へ移行する。"
                    ),
                    "confidence": "high",
                }
        summary = {
            "decision_owner": "user",
            "stakeholders": [
                {
                    "name": "自分",
                    "role": "意思決定主体",
                    "impact": "キャリア・収入に影響",
                },
                {
                    "name": "家族",
                    "role": "生活の共同体",
                    "impact": "時間配分・制約に影響",
                },
                {
                    "name": "現職チーム",
                    "role": "協働者",
                    "impact": "引き継ぎに影響",
                },
            ],
            "accountability_notes": (
                "転職/残留いずれでも、関係者（家族・現職）への説明責任が発生する。"
            ),
            "consent_considerations": ["家族への影響を事前共有し合意形成する"],
        }
        return options, summary

    if short_id == "case_009":
        for opt in options:
            if opt.get("option_id") == "opt_1":
                opt["responsibility_review"] = {
                    "decision_owner": "user",
                    "stakeholders": [
                        {
                            "name": "自分",
                            "role": "意思決定主体",
                            "impact": "人生の方向性・収入に影響",
                        }
                    ],
                    "accountability_notes": (
                        "最終判断はユーザー。Po_coreは問いと構造化を提供する。"
                    ),
                    "confidence": "high",
                }
            elif opt.get("option_id") == "opt_2":
                opt["responsibility_review"] = {
                    "decision_owner": "user",
                    "stakeholders": [
                        {
                            "name": "自分",
                            "role": "意思決定主体",
                            "impact": "収入・時間に影響",
                        }
                    ],
                    "accountability_notes": (
                        "費用と時間投資はユーザーが負う。前提条件を明示して判断する。"
                    ),
                    "confidence": "high",
                }
        summary = {
            "decision_owner": "user",
            "stakeholders": [
                {
                    "name": "自分",
                    "role": "意思決定主体",
                    "impact": "人生の方向性・収入に影響",
                }
            ],
            "accountability_notes": (
                "意思決定と結果責任はユーザー。Po_coreは問いと構造化を提供する。"
            ),
            "consent_considerations": [
                "支援者がいる場合、金銭・時間への影響を共有する"
            ],
        }
        return options, summary

    # ── Generic: feature-driven ───────────────────────────────────────────
    stakeholders = _map_stakeholders(case)
    feats = features or {}
    conflict = feats.get("constraint_conflict") is True

    for opt in options:
        opt["responsibility_review"] = {
            "decision_owner": "user",
            "stakeholders": stakeholders,
            "accountability_notes": (
                "最終判断はユーザー。Po_coreは構造化と検証手続きを提供する。"
            ),
            "confidence": "high" if conflict else "medium",
        }

    consent: List[str] = []
    if any(s["name"] == "家族" for s in stakeholders):
        consent.append("家族への影響を事前共有し合意形成する")
    if feats.get("income_drop_forbidden"):
        consent.append(
            "収入への影響（減収リスク）を明示し、必要なら支援/予備費を検討する"
        )
    if feats.get("relocation_forbidden"):
        consent.append("居住地制約がある場合、働き方/通勤条件を先に固定する")

    summary = {
        "decision_owner": "user",
        "stakeholders": stakeholders,
        "accountability_notes": (
            "意思決定と結果責任はユーザー。Po_coreは説明可能な判断材料を整理する。"
        ),
        "consent_considerations": consent,
    }
    return options, summary
