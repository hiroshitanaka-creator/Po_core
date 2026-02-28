"""src/pocore/engines/responsibility_v1.py — Responsibility review engine v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

PROFILE_CASE_001 = "job_change_transition_v1"
PROFILE_CASE_009 = "values_clarification_v1"

RESP_STAKEHOLDER_CONSENT_CHECK = "RESP_STAKEHOLDER_CONSENT_CHECK"
RESP_IMPACT_SCOPE = "RESP_IMPACT_SCOPE"


def _has_profile(features: Optional[Dict[str, Any]], profile: str) -> bool:
    return isinstance(features, dict) and features.get("scenario_profile") == profile


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

    if _has_profile(features, PROFILE_CASE_001):
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

    if _has_profile(features, PROFILE_CASE_009):
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
    has_externality_stakeholders = int(feats.get("stakeholders_count", 0)) >= 2

    decision_owner = "user"
    if has_externality_stakeholders:
        decision_owner = "未確定（要確認）"

    per_option_notes = "最終判断はユーザー。Po_coreは構造化と検証手続きを提供する。"
    if has_externality_stakeholders:
        per_option_notes = (
            f"{RESP_STAKEHOLDER_CONSENT_CHECK}: 決裁者が不明なため、最初に意思決定者を特定する。"
            "関係者への通知・同意・相談の実施と記録を前提に進める。"
        )

    for opt in options:
        opt["responsibility_review"] = {
            "decision_owner": decision_owner,
            "stakeholders": stakeholders,
            "accountability_notes": per_option_notes,
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

    if has_externality_stakeholders:
        consent.extend(
            [
                f"{RESP_STAKEHOLDER_CONSENT_CHECK}: 決裁者を特定し、承認権限を確認する",
                f"{RESP_STAKEHOLDER_CONSENT_CHECK}: 影響を受ける関係者への通知・同意・相談の要否を確認する",
                f"{RESP_IMPACT_SCOPE}: 影響範囲（誰が何を得る/失うか）と合意内容を記録する",
                f"{RESP_IMPACT_SCOPE}: コミュニケーション手段と期限を決め、実施ログを残す",
            ]
        )

    accountability_notes = (
        "意思決定と結果責任はユーザー。Po_coreは説明可能な判断材料を整理する。"
    )
    if has_externality_stakeholders:
        accountability_notes = (
            f"{RESP_STAKEHOLDER_CONSENT_CHECK}: 決裁者/意思決定者が未確定なら先に確定する。"
            f"{RESP_IMPACT_SCOPE}: 外部性があるため、通知・同意・相談の結果と合意事項を記録する。"
        )

    summary = {
        "decision_owner": decision_owner,
        "stakeholders": stakeholders,
        "accountability_notes": accountability_notes,
        "consent_considerations": consent,
    }
    return options, summary
