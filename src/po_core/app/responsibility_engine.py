# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Responsibility engine v1 for output_schema_v1 responsibility blocks.

M2-B responsibility_v1:
- decision_owner is always non-empty.
- Po_core/system/AI-like forbidden subjects are never used as decision_owner.
- Returns both top-level responsibility summary and option-level review payload.
"""

from __future__ import annotations

from typing import Any

_FORBIDDEN_SUBJECTS = {
    "po_core",
    "pocore",
    "po core",
    "the system",
    "ai",
    "assistant",
}

_DEFAULT_OWNER = "意思決定者"


def _normalize_subject(value: str) -> str:
    return " ".join(value.strip().lower().split())


def sanitize_decision_owner(owner: str | None, *, fallback: str = _DEFAULT_OWNER) -> str:
    """Return a schema-safe decision owner.

    Empty/forbidden subjects are replaced by ``fallback``.
    """
    candidate = (owner or "").strip()
    if not candidate:
        return fallback
    if _normalize_subject(candidate) in _FORBIDDEN_SUBJECTS:
        return fallback
    return candidate


def _build_stakeholders(case: dict[str, Any], *, limit: int) -> list[dict[str, str]]:
    stakeholders = case.get("stakeholders", [])
    out = [
        {
            "name": str(s.get("name", "関係者")),
            "role": str(s.get("role", "関係者")),
            "impact": str(s.get("impact", "直接影響を受ける")),
        }
        for s in stakeholders[:limit]
    ]
    if out:
        return out
    return [{"name": "関係者", "role": "利害関係者", "impact": "直接影響を受ける"}]


def build_responsibility_summary(case: dict[str, Any], *, values: list[str]) -> dict[str, Any]:
    """Build top-level responsibility summary (FR-RES-001 compliant)."""
    stakeholders = case.get("stakeholders", [])
    raw_owner = str(stakeholders[0].get("name", "")) if stakeholders else ""
    owner = sanitize_decision_owner(raw_owner)

    consent_items: list[str] = []
    values_lower = [v.lower() for v in values]
    has_safety = any(
        kw in v
        for v in values_lower
        for kw in ("安全", "nonmaleficence", "ユーザー", "信頼", "リスク")
    )
    has_external_stakeholder = any(
        str(s.get("name", "")).lower() in ("ユーザー", "顧客", "患者", "市民", "利用者")
        for s in stakeholders
    )
    if has_safety or has_external_stakeholder:
        consent_items = [
            "影響を受けるすべての関係者に変更内容・リスクを事前に説明する",
            "重大なリスクが残る場合は関係者の同意を得てから進める",
        ]

    return {
        "decision_owner": owner,
        "stakeholders": _build_stakeholders(case, limit=5),
        "accountability_notes": "意思決定と結果責任はユーザー。Po_coreは問いと構造化を提供する。",
        "consent_considerations": consent_items,
    }


def build_option_responsibility_review(case: dict[str, Any]) -> dict[str, Any]:
    """Build option-level responsibility_review block."""
    stakeholders = case.get("stakeholders", [])
    raw_owner = str(stakeholders[0].get("name", "")) if stakeholders else ""
    owner = sanitize_decision_owner(raw_owner)
    return {
        "decision_owner": owner,
        "stakeholders": _build_stakeholders(case, limit=3),
        "accountability_notes": "意思決定と結果責任はユーザー。Po_coreは問いと構造化を提供する。",
        "confidence": "medium",
    }
