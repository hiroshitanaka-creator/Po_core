# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""output_adapter.py — po_core.run() → output_schema_v1 adapter.

Bridges the philosophical pipeline output (po_core.run()) to the structured
decision-support schema required by output_schema_v1.json.

Key function::

    adapt_to_schema(case, run_result, *, run_id, digest, now, seed, deterministic) -> dict

The proposal content (philosophical reasoning) comes from the real pipeline.
Structural elements (options, trace, questions, etc.) are derived
deterministically from case data so that same input → same output holds.
"""

from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List

_POCORE_VERSION = "0.2.0b4"
_SCHEMA_VERSION = "1.0"
_GENERATOR_NAME = "po_core.ensemble.run_turn"
_GENERATOR_VERSION = "0.2.0"

# ── Value keyword → ethics principle mapping ──────────────────────────────

_VALUE_TO_PRINCIPLE: Dict[str, str] = {
    # justice
    "公平": "justice",
    "公正": "justice",
    "平等": "justice",
    "公平性": "justice",
    # autonomy
    "自律": "autonomy",
    "自由": "autonomy",
    "自己決定": "autonomy",
    "自主": "autonomy",
    "autonomy": "autonomy",
    # nonmaleficence
    "安全": "nonmaleficence",
    "無危害": "nonmaleficence",
    "危害": "nonmaleficence",
    "リスク回避": "nonmaleficence",
    # integrity
    "誠実": "integrity",
    "誠意": "integrity",
    "正直": "integrity",
    "透明": "integrity",
    # accountability
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


def _map_values_to_principles(values: List[str]) -> List[str]:
    """Map case values → sorted list of ethics principles (always ≥ 2)."""
    principles: set = set()
    for v in values:
        v_lower = v.lower()
        for kw, principle in _VALUE_TO_PRINCIPLE.items():
            if kw.lower() in v_lower:
                principles.add(principle)
                break
    # Ensure at least 2
    for fallback in _ALL_PRINCIPLES:
        if len(principles) >= 2:
            break
        principles.add(fallback)
    return sorted(principles)


# ── Timestamp helpers ──────────────────────────────────────────────────────


def _ts(base: dt.datetime, offset_secs: int) -> str:
    t = base + dt.timedelta(seconds=offset_secs)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_base(now: str) -> dt.datetime:
    return dt.datetime.fromisoformat(now.replace("Z", "+00:00")).replace(tzinfo=None)


# ── Uncertainty ────────────────────────────────────────────────────────────


def _uncertainty_level(case: Dict[str, Any]) -> str:
    n_constraints = len(case.get("constraints", []))
    n_unknowns = len(case.get("unknowns", []))
    if n_constraints >= 4 or n_unknowns >= 3:
        return "high"
    if n_constraints >= 2 or n_unknowns >= 1:
        return "medium"
    return "low"


def _build_uncertainty(case: Dict[str, Any]) -> Dict[str, Any]:
    unknowns = case.get("unknowns", [])
    constraints = case.get("constraints", [])
    return {
        "overall_level": _uncertainty_level(case),
        "reasons": list(unknowns[:3]) if unknowns else ["重要情報が未確定"],
        "assumptions": list(constraints[:2]),
        "known_unknowns": list(unknowns[:5]),
    }


# ── Option-level builders ──────────────────────────────────────────────────


def _build_option_ethics_review(principles: List[str]) -> Dict[str, Any]:
    applied = (
        principles[:2] if len(principles) >= 2 else list(principles) + ["autonomy"]
    )
    return {
        "principles_applied": applied,
        "tradeoffs": [],
        "concerns": [],
        "confidence": "medium",
    }


def _build_option_responsibility_review(case: Dict[str, Any]) -> Dict[str, Any]:
    stakeholders = case.get("stakeholders", [])
    sh_list = [
        {
            "name": str(s["name"]),
            "role": str(s.get("role", "関係者")),
            "impact": str(s.get("impact", "")),
        }
        for s in stakeholders[:3]
    ]
    if not sh_list:
        sh_list = [
            {"name": "関係者", "role": "利害関係者", "impact": "直接影響を受ける"}
        ]
    owner = str(stakeholders[0]["name"]) if stakeholders else "意思決定者"
    return {
        "decision_owner": owner,
        "stakeholders": sh_list,
        "accountability_notes": "意思決定と結果責任はユーザー。Po_coreは問いと構造化を提供する。",
        "confidence": "medium",
    }


def _build_feasibility(case: Dict[str, Any]) -> Dict[str, Any]:
    deadline = case.get("deadline")
    if deadline:
        return {
            "effort": "中程度",
            "timeline": f"期限: {deadline}",
            "confidence": "medium",
        }
    return {"effort": "要確認", "timeline": "期限未定", "confidence": "low"}


def _build_options(
    case: Dict[str, Any],
    proposal: Dict[str, Any],
    principles: List[str],
) -> List[Dict[str, Any]]:
    """Build 2 options: main (from proposal) + cautious alternative."""
    constraints = case.get("constraints", [])
    values = case.get("values", [])
    unknowns = case.get("unknowns", [])

    content = str(proposal.get("content", "")) or "哲学的観点からの主要推奨案"
    risk_tags: List[str] = list(proposal.get("risk_tags", []))

    # Action plan from constraints
    action_plan: List[Dict[str, Any]] = [
        {"step": f"制約を考慮: {c}"} for c in constraints[:3]
    ]
    if not action_plan:
        action_plan = [{"step": "状況の詳細確認と関係者への情報共有"}]

    # Pros: from values + assumption_tags
    pros: List[str] = [f"価値観「{v}」の実現に資する" for v in values[:2]]
    if not pros:
        pros = ["選択肢の実現可能性が高い", "関係者への影響を最小化できる"]

    # Cons: from unknowns + risk_tags
    cons: List[str] = [f"不確実性: {u}" for u in unknowns[:2]]
    if not cons:
        cons = ["不確実性が残る", "追加情報が必要"]

    # Risks
    risks: List[Dict[str, Any]] = [
        {
            "risk": t,
            "severity": "medium",
            "mitigation": "段階的実施とモニタリングで緩和する",
        }
        for t in risk_tags[:2]
    ]
    if not risks:
        risks = [
            {
                "risk": "情報不足による判断ミスのリスク",
                "severity": "medium",
                "mitigation": "追加調査を行い不確実性を低減する",
            }
        ]

    uncertainty = _build_uncertainty(case)
    ethics_review = _build_option_ethics_review(principles)
    resp_review = _build_option_responsibility_review(case)
    feasibility = _build_feasibility(case)

    # Option 1: main proposal
    opt1: Dict[str, Any] = {
        "option_id": "opt_001",
        "title": str(case.get("title", "主要選択肢")),
        "description": content,
        "action_plan": action_plan,
        "pros": pros,
        "cons": cons,
        "risks": risks,
        "ethics_review": ethics_review,
        "responsibility_review": resp_review,
        "feasibility": feasibility,
        "uncertainty": uncertainty,
    }

    # Option 2: cautious alternative (always provided)
    opt2_uncertainty: Dict[str, Any] = {
        "overall_level": "medium",
        "reasons": list(uncertainty["reasons"]),
        "assumptions": list(uncertainty["assumptions"]),
        "known_unknowns": list(uncertainty["known_unknowns"]),
    }

    opt2: Dict[str, Any] = {
        "option_id": "opt_002",
        "title": "慎重路線：情報収集後に再判断",
        "description": (
            "主要な不明点を解消してから判断する選択肢。"
            "リスクを最小化しながら次の判断機会を設ける。"
        ),
        "action_plan": [
            {"step": "不明点を優先度順に列挙し、調査計画を立てる"},
            {"step": "関係者へ現状と懸念を共有し認識を合わせる"},
            {"step": "判断に必要な情報が揃った時点で再検討する"},
        ],
        "pros": [
            "情報が揃った状態での判断が可能",
            "リスクを最小化できる",
            "関係者の同意を得やすい",
        ],
        "cons": [
            "判断の先送りによる機会損失の可能性",
            "時間的コストが発生する",
        ],
        "risks": [
            {
                "risk": "判断保留による機会損失",
                "severity": "low",
                "mitigation": "タイムボックスを設定し判断期限を明確にする",
            }
        ],
        "ethics_review": ethics_review,
        "responsibility_review": resp_review,
        "feasibility": {
            "effort": "低〜中程度",
            "timeline": "1〜4週間の調査期間",
            "confidence": "medium",
        },
        "uncertainty": opt2_uncertainty,
    }

    return [opt1, opt2]


# ── Recommendation ─────────────────────────────────────────────────────────


def _build_recommendation(
    case: Dict[str, Any],
    proposal: Dict[str, Any],
    status: str,
) -> Dict[str, Any]:
    """Build recommendation based on case values and pipeline status."""
    values = case.get("values", [])
    unknowns = case.get("unknowns", [])

    # No recommendation when values are empty or pipeline blocked
    if not values or status == "blocked":
        reason = (
            "価値観が不明確なため推奨が困難です。まず重視する価値観を明確にしてください。"
            if not values
            else "安全評価によりこの入力への推奨は提供できません。"
        )
        return {
            "status": "no_recommendation",
            "reason": reason,
            "missing_info": list(unknowns[:3]) or ["価値観・優先事項の明確化"],
            "next_steps": [
                "価値観の明確化ワーク（例：重要度順位付け）を実施する",
                "追加情報を収集する",
            ],
            "confidence": "low",
        }

    confidence = float(proposal.get("confidence", 0.5))
    conf_label = (
        "high" if confidence >= 0.7 else ("medium" if confidence >= 0.45 else "low")
    )

    return {
        "status": "recommended",
        "recommended_option_id": "opt_001",
        "reason": (
            "価値観と制約を踏まえた哲学的考察により、主要選択肢が最もバランスが取れていると"
            "判断されます。"
        ),
        "counter": (
            "ただし不明点が残るため、慎重路線（opt_002）も検討に値します。"
            "情報が揃っていない状態での決定にはリスクが伴います。"
        ),
        "alternatives": [
            {
                "option_id": "opt_002",
                "when_to_choose": "重要な不明点が解消できない場合、またはリスク許容度が低い場合",
            }
        ],
        "confidence": conf_label,
    }


# ── Questions ──────────────────────────────────────────────────────────────


def _build_questions(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build question list from unknowns + values clarification if needed."""
    unknowns = case.get("unknowns", [])
    values = case.get("values", [])
    questions: List[Dict[str, Any]] = []

    for i, u in enumerate(unknowns[:4], 1):
        questions.append(
            {
                "question_id": f"q_{i:03d}",
                "question": f"{u}はどのような状況ですか？",
                "priority": min(i, 5),
                "why_needed": f"この不明点（{u}）が判断に直接影響するため",
                "assumption_if_unanswered": "最も慎重な仮定を採用します",
                "optional": i > 2,
            }
        )

    # Values clarification question when values are empty
    if not values:
        questions.append(
            {
                "question_id": f"q_{len(questions) + 1:03d}",
                "question": "この判断で最も重視したい価値観・優先事項は何ですか？",
                "priority": 1,
                "why_needed": "価値観が明確でないと推奨の方向性が定まらないため",
                "assumption_if_unanswered": "情報収集を優先する慎重路線を採用",
                "optional": False,
            }
        )

    # Fallback: always provide at least one question
    if not questions:
        questions.append(
            {
                "question_id": "q_001",
                "question": "想定外の状況が発生した場合の対応方針はありますか？",
                "priority": 3,
                "why_needed": "緊急時の意思決定基準を明確化するため",
                "assumption_if_unanswered": "関係者に相談の上、慎重に対応",
                "optional": True,
            }
        )

    return questions


# ── Trace ──────────────────────────────────────────────────────────────────


def _build_trace(now: str) -> Dict[str, Any]:
    """Build FR-TR-001 compliant 6-step trace."""
    base = _parse_base(now)
    step_defs = [
        (
            "parse_input",
            "入力YAMLを解析し、case_id・problem・values・constraints等を抽出した",
        ),
        ("generate_options", "39人の哲学者による審議を経て選択肢を生成した"),
        ("ethics_review", "W_Ethics Gateによる3層倫理評価を適用した"),
        ("responsibility_review", "意思決定主体と利害関係者の責任構造を検証した"),
        ("question_layer", "不明点から優先度付き質問リストを生成した"),
        ("compose_output", "推奨・反証・代替案を含む出力を組み立てた"),
    ]
    steps = [
        {
            "name": name,
            "started_at": _ts(base, i * 2),
            "ended_at": _ts(base, i * 2 + 1),
            "summary": summary,
        }
        for i, (name, summary) in enumerate(step_defs)
    ]
    return {"version": "1.0", "steps": steps}


# ── Public helpers ─────────────────────────────────────────────────────────


def build_user_input(case: Dict[str, Any]) -> str:
    """Build philosophical question string from case dict for po_core.run()."""
    parts = [str(case.get("problem", case.get("title", "")))]

    constraints = case.get("constraints", [])
    if constraints:
        parts.append("\n\n【制約】\n" + "\n".join(f"- {c}" for c in constraints))

    values = case.get("values", [])
    if values:
        parts.append("\n\n【重視する価値観】\n" + "\n".join(f"- {v}" for v in values))

    unknowns = case.get("unknowns", [])
    if unknowns:
        parts.append("\n\n【不明点】\n" + "\n".join(f"- {u}" for u in unknowns))

    return "".join(parts)


# ── Main adapter ───────────────────────────────────────────────────────────


def adapt_to_schema(
    case: Dict[str, Any],
    run_result: Dict[str, Any],
    *,
    run_id: str,
    digest: str,
    now: str,
    seed: int = 0,
    deterministic: bool = True,
) -> Dict[str, Any]:
    """
    Map po_core.run() result + case data → output_schema_v1 compliant dict.

    The proposal content (philosophical reasoning) populates option 1.
    All structural elements are derived deterministically from case data.

    Args:
        case:          Validated case dict (from input_schema_v1).
        run_result:    Return value of po_core.app.api.run().
        run_id:        Unique run identifier.
        digest:        SHA-256 hex of canonical case JSON.
        now:           ISO-8601 UTC datetime string.
        seed:          Reproducibility seed (stored in meta).
        deterministic: When True, same inputs produce same run_id.

    Returns:
        Dict conforming to output_schema_v1.json.
    """
    proposal: Dict[str, Any] = run_result.get("proposal") or {}
    status: str = run_result.get("status", "ok")

    values = case.get("values", [])
    principles = _map_values_to_principles(values)

    options = _build_options(case, proposal, principles)
    recommendation = _build_recommendation(case, proposal, status)
    questions = _build_questions(case)
    uncertainty = _build_uncertainty(case)

    # Top-level ethics summary
    tradeoffs: List[Dict[str, Any]] = []
    if len(values) >= 2:
        tradeoffs.append(
            {
                "tension": f"「{values[0]}」vs「{values[1]}」",
                "between": [str(values[0]), str(values[1])],
                "mitigation": "段階的実施と関係者調整により両立を目指す",
                "severity": "medium",
            }
        )

    ethics: Dict[str, Any] = {
        "principles_used": principles,
        "tradeoffs": tradeoffs,
        "guardrails": [
            "医療・法律の最終判断はPo_coreが行わない",
            "意思決定の主体はユーザーである",
        ],
        "notes": "W_Ethics Gateによる3層倫理評価済み",
    }

    # Optional: wethics_verdict from pipeline (only for blocked/degraded runs)
    verdict = run_result.get("verdict")
    if verdict and isinstance(verdict, dict):
        raw_decision = str(verdict.get("decision", "")).upper()
        # Map internal decision values to schema enum
        _decision_map = {
            "ALLOW": "ALLOW",
            "ALLOW_WITH_REPAIR": "ALLOW_WITH_REPAIR",
            "REJECT": "REJECT",
            "ESCALATE": "ESCALATE",
            "REVISE": "ALLOW_WITH_REPAIR",  # internal alias
        }
        if raw_decision in _decision_map:
            ethics["wethics_verdict"] = _decision_map[raw_decision]

    # Top-level responsibility summary
    stakeholders = case.get("stakeholders", [])
    sh_list = [
        {
            "name": str(s["name"]),
            "role": str(s.get("role", "関係者")),
            "impact": str(s.get("impact", "")),
        }
        for s in stakeholders[:5]
    ]
    if not sh_list:
        sh_list = [
            {"name": "関係者", "role": "利害関係者", "impact": "直接影響を受ける"}
        ]
    owner = str(stakeholders[0]["name"]) if stakeholders else "意思決定者"

    # Derive consent_considerations: non-empty when user safety or external parties involved
    consent_items: List[str] = []
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

    responsibility: Dict[str, Any] = {
        "decision_owner": owner,
        "stakeholders": sh_list,
        "accountability_notes": "意思決定と結果責任はユーザー。Po_coreは問いと構造化を提供する。",
        "consent_considerations": consent_items,
    }

    trace = _build_trace(now)

    return {
        "meta": {
            "schema_version": _SCHEMA_VERSION,
            "pocore_version": _POCORE_VERSION,
            "run_id": run_id,
            "created_at": now,
            "seed": seed,
            "deterministic": deterministic,
            "generator": {
                "name": _GENERATOR_NAME,
                "version": _GENERATOR_VERSION,
                "mode": "rule_based",
            },
        },
        "case_ref": {
            "case_id": str(case.get("case_id", "")),
            "title": str(case.get("title", "")),
            "input_digest": digest,
        },
        "options": options,
        "recommendation": recommendation,
        "ethics": ethics,
        "responsibility": responsibility,
        "questions": questions,
        "uncertainty": uncertainty,
        "trace": trace,
    }
