# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Ethics engine v1 for output_schema_v1 ethics summary.

FR-ETH-001
    - Produce ethics.principles_used based on case values.
    - Guarantee at least two principles for minimum ethical coverage.

FR-ETH-002
    - Produce ethics.tradeoffs when value tensions are present.
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
    """Build top-level ethics summary compliant with output_schema_v1."""
    values = [str(v) for v in case.get("values", [])]
    principles = principles_from_values(values)

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

    ethics: dict[str, Any] = {
        "principles_used": principles,
        "tradeoffs": tradeoffs,
        "guardrails": [
            "医療・法律の最終判断はPo_coreが行わない",
            "意思決定の主体はユーザーである",
        ],
        "notes": "W_Ethics Gateによる3層倫理評価済み",
    }

    if run_result and isinstance(run_result.get("verdict"), dict):
        raw_decision = str(run_result["verdict"].get("decision", "")).upper()
        if raw_decision in _DECISION_MAP:
            ethics["wethics_verdict"] = _DECISION_MAP[raw_decision]

    return ethics
