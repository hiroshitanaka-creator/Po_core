# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Ethics engine v1 for output_schema_v1 ethics summary.

FR-ETH-001
    - Produce ethics.principles_used based on case values.
    - Guarantee at least two principles for minimum ethical coverage.

FR-ETH-002
    - Produce ethics.tradeoffs when value tensions are present.

REQ-ETH-002
    - Ethics ruleset is defined by rule_id; rules_fired is observable in trace.
"""

from __future__ import annotations

from typing import Any

# Map value keywords (JP/EN) to output schema ethics principles.
_VALUE_TO_PRINCIPLE: dict[str, str] = {
    "公平": "justice",
    "公正": "justice",
    "平等": "justice",
    "公平性": "justice",
    "自律": "autonomy",
    "自由": "autonomy",
    "自己決定": "autonomy",
    "自主": "autonomy",
    "autonomy": "autonomy",
    "安全": "nonmaleficence",
    "無危害": "nonmaleficence",
    "危害": "nonmaleficence",
    "リスク回避": "nonmaleficence",
    "誠実": "integrity",
    "誠意": "integrity",
    "正直": "integrity",
    "透明": "integrity",
    "説明責任": "accountability",
    "accountability": "accountability",
    "責任": "accountability",
    "透明性": "accountability",
}

_ALL_PRINCIPLES = [
    "integrity",
    "autonomy",
    "justice",
    "nonmaleficence",
    "accountability",
]

_DECISION_MAP = {
    "ALLOW": "ALLOW",
    "ALLOW_WITH_REPAIR": "ALLOW_WITH_REPAIR",
    "REJECT": "REJECT",
    "ESCALATE": "ESCALATE",
    "REVISE": "ALLOW_WITH_REPAIR",  # internal alias
}

# ── Ethics rule definitions (REQ-ETH-002) ─────────────────────────────────

_ETHICS_RULES: list[dict[str, Any]] = [
    {
        "rule_id": "ETH-R-001",
        "description": "values フィールドからキーワードマッピングで倫理原則を抽出",
        "priority": 1,
    },
    {
        "rule_id": "ETH-R-002",
        "description": "最低 2 原則保証: 不足時に integrity / autonomy を補完",
        "priority": 2,
    },
    {
        "rule_id": "ETH-R-003",
        "description": "values が 2 件以上の場合、value 間のトレードオフを生成",
        "priority": 3,
    },
    {
        "rule_id": "ETH-R-004",
        "description": "W_Ethics Gate の verdict を wethics_verdict フィールドに反映",
        "priority": 4,
    },
    {
        "rule_id": "ETH-R-005",
        "description": "医療・法律 キーワードを検出した場合、nonmaleficence を追加",
        "priority": 5,
    },
]

_MEDICAL_LEGAL_KEYWORDS = [
    "医療", "medical", "治療", "診断", "手術",
    "法律", "legal", "訴訟", "契約", "規制", "コンプライアンス",
]


def principles_from_values(values: list[str]) -> list[str]:
    """Infer ethics principles from case values, always returning >=2 entries."""
    principles: set[str] = set()
    for value in values:
        value_lower = value.lower()
        for keyword, principle in _VALUE_TO_PRINCIPLE.items():
            if keyword.lower() in value_lower:
                principles.add(principle)
                break

    for fallback in _ALL_PRINCIPLES:
        if len(principles) >= 2:
            break
        principles.add(fallback)

    return sorted(principles)


def build_ethics_summary(
    case: dict[str, Any],
    *,
    run_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build top-level ethics summary compliant with output_schema_v1.

    REQ-ETH-002: rules_fired records which rule_ids were applied.
    """
    values = [str(v) for v in case.get("values", [])]
    all_text = " ".join(values + [str(case.get("problem", ""))])
    rules_fired: list[str] = []

    # ETH-R-001: value-based principle extraction
    principles: set[str] = set()
    for value in values:
        value_lower = value.lower()
        for keyword, principle in _VALUE_TO_PRINCIPLE.items():
            if keyword.lower() in value_lower:
                principles.add(principle)
                break
    if values:
        rules_fired.append("ETH-R-001")

    # ETH-R-005: medical/legal domain detection → nonmaleficence
    if any(kw in all_text for kw in _MEDICAL_LEGAL_KEYWORDS):
        principles.add("nonmaleficence")
        rules_fired.append("ETH-R-005")

    # ETH-R-002: minimum 2 principles guarantee
    for fallback in _ALL_PRINCIPLES:
        if len(principles) >= 2:
            break
        principles.add(fallback)
    rules_fired.append("ETH-R-002")

    principles_list = sorted(principles)

    # ETH-R-003: tradeoffs from value tensions
    tradeoffs: list[dict[str, Any]] = []
    if len(values) >= 2:
        tradeoffs.append(
            {
                "tension": f"「{values[0]}」vs「{values[1]}」",
                "between": [values[0], values[1]],
                "mitigation": "段階的実施と関係者調整により両立を目指す",
                "severity": "medium",
            }
        )
        rules_fired.append("ETH-R-003")

    ethics: dict[str, Any] = {
        "principles_used": principles_list,
        "tradeoffs": tradeoffs,
        "guardrails": [
            "医療・法律の最終判断はPo_coreが行わない",
            "意思決定の主体はユーザーである",
            "価値軸が空のまま推奨を断言しない",
        ],
        "notes": f"W_Ethics Gateによる3層倫理評価済み (rules_fired: {', '.join(rules_fired)})",
    }

    # ETH-R-004: W_Ethics Gate verdict integration
    if run_result and isinstance(run_result.get("verdict"), dict):
        raw_decision = str(run_result["verdict"].get("decision", "")).upper()
        if raw_decision in _DECISION_MAP:
            ethics["wethics_verdict"] = _DECISION_MAP[raw_decision]
            rules_fired.append("ETH-R-004")

    return ethics


def get_rules_fired(
    case: dict[str, Any],
    *,
    run_result: dict[str, Any] | None = None,
) -> list[str]:
    """Return the list of rule_ids that would fire for a given case.

    Useful for trace metrics (REQ-TRC-001, REQ-ETH-002).
    """
    values = [str(v) for v in case.get("values", [])]
    all_text = " ".join(values + [str(case.get("problem", ""))])
    fired: list[str] = []

    if values:
        fired.append("ETH-R-001")
    if any(kw in all_text for kw in _MEDICAL_LEGAL_KEYWORDS):
        fired.append("ETH-R-005")
    fired.append("ETH-R-002")
    if len(values) >= 2:
        fired.append("ETH-R-003")
    if run_result and isinstance(run_result.get("verdict"), dict):
        raw = str(run_result["verdict"].get("decision", "")).upper()
        if raw in _DECISION_MAP:
            fired.append("ETH-R-004")

    return fired
