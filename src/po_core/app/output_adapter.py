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

from po_core.app.ethics_engine import (
    build_ethics_summary,
    get_rules_fired,
    principles_from_values,
)
from po_core.app.plan_builder import build_two_track_plan, needs_two_track_plan
from po_core.app.policy_engine import arbitrate, build_recommendation
from po_core.app.question_layer import build_questions
from po_core.app.responsibility_engine import (
    build_option_responsibility_review,
    build_responsibility_summary,
)
from po_core.app.values_clarifier import (
    build_values_clarification_action_plan,
    build_values_clarification_questions,
    needs_values_clarification,
)

# Version metadata: derive from the package source of truth so these never drift.
# import here is deferred to avoid circular imports at module load time.
def _pkg_version() -> str:
    from po_core import __version__

    return __version__


_SCHEMA_VERSION = "1.0"
_GENERATOR_NAME = "po_core.ensemble.run_turn"

# Lazily resolved at first call.  Use _get_pocore_version() / _get_generator_version()
# internally instead of the old string constants.
def _get_pocore_version() -> str:
    return _pkg_version()


def _get_generator_version() -> str:
    return _pkg_version()


# Backward-compat aliases (read from package at access time).
class _VersionProxy:
    """Descriptor that reads po_core.__version__ on every attribute access."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: object, objtype: type | None = None) -> str:
        return _pkg_version()


class _VersionConstants:
    _POCORE_VERSION = _VersionProxy()
    _GENERATOR_VERSION = _VersionProxy()


_version_constants = _VersionConstants()

# Module-level attribute access kept for backward compat via __getattr__
_POCORE_VERSION: str  # type: ignore[assignment]
_GENERATOR_VERSION: str  # type: ignore[assignment]


def __getattr__(name: str) -> str:
    if name in ("_POCORE_VERSION", "_GENERATOR_VERSION"):
        return _pkg_version()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _map_values_to_principles(values: List[str]) -> List[str]:
    """Compatibility wrapper around ethics_engine principle extraction."""
    return principles_from_values(values)


# ── Timestamp helpers ──────────────────────────────────────────────────────


def _ts(base: dt.datetime, offset_secs: int) -> str:
    t = base + dt.timedelta(seconds=offset_secs)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_base(now: str) -> dt.datetime:
    return dt.datetime.fromisoformat(now.replace("Z", "+00:00")).replace(tzinfo=None)


# ── Uncertainty ────────────────────────────────────────────────────────────


def _has_constraint_contradiction(constraints: List[str]) -> bool:
    """Return True when constraints include a deterministic contradiction signal.

    Rule (FR-UNC-001 helper): when one of the following contradictory pairs appears
    in the same case, uncertainty is escalated regardless of unknown count.
      - speed vs quality (早く/即時 vs 慎重/品質)
      - keep-all vs reduce (維持/削減)
    """

    normalized = " ".join(str(c).lower() for c in constraints)
    contradiction_pairs = [
        (("早", "即", "迅速", "speed", "fast"), ("慎重", "品質", "quality")),
        (("維持", "keep"), ("削減", "減ら", "reduce")),
    ]
    for left_terms, right_terms in contradiction_pairs:
        if any(term in normalized for term in left_terms) and any(
            term in normalized for term in right_terms
        ):
            return True
    return False


def _uncertainty_level(case: Dict[str, Any]) -> str:
    constraints = case.get("constraints", [])
    unknowns = case.get("unknowns", [])
    n_unknowns = len(unknowns) if isinstance(unknowns, list) else 0

    # FR-UNC-001 level rule (deterministic):
    #   high   = contradiction exists OR unknowns >= 3
    #   medium = unknowns in [1, 2]
    #   low    = unknowns == 0
    if isinstance(constraints, list) and _has_constraint_contradiction(constraints):
        return "high"
    if n_unknowns >= 3:
        return "high"
    if n_unknowns >= 1:
        return "medium"
    return "low"


def _build_uncertainty(case: Dict[str, Any]) -> Dict[str, Any]:
    unknowns = case.get("unknowns", [])
    constraints = case.get("constraints", [])
    unknowns_list = list(unknowns[:5]) if isinstance(unknowns, list) else []
    constraints_list = list(constraints[:2]) if isinstance(constraints, list) else []
    return {
        "overall_level": _uncertainty_level(case),
        "reasons": unknowns_list[:3] if unknowns_list else ["重要情報が未確定"],
        "assumptions": constraints_list,
        "known_unknowns": unknowns_list,
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
    now: str | None = None,
) -> List[Dict[str, Any]]:
    """Build 2 options: main (from proposal) + cautious alternative.

    REQ-VALUES-001: When values is empty, opt_001 action_plan becomes the
    Values Clarification Pack (5-step procedure).
    REQ-PLAN-001: When unknowns + deadline pressure, opt_001 action_plan
    becomes a Two-Track Plan (Track A: reversible actions / Track B: unknowns).
    """
    constraints = case.get("constraints", [])
    values = case.get("values", [])
    unknowns = case.get("unknowns", [])

    content = str(proposal.get("content", "")) or "哲学的観点からの主要推奨案"
    risk_tags: List[str] = list(proposal.get("risk_tags", []))

    # ── Action plan selection (REQ-VALUES-001, REQ-PLAN-001) ──────────────
    if needs_values_clarification(case):
        # REQ-VALUES-001: values empty → value-elicitation procedure
        action_plan: List[Dict[str, Any]] = build_values_clarification_action_plan()
    elif needs_two_track_plan(case, now):
        # REQ-PLAN-001: unknowns + time pressure → Two-Track Plan
        action_plan = build_two_track_plan(case, now)
    else:
        action_plan = [{"step": f"制約を考慮: {c}"} for c in constraints[:3]]
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
    resp_review = build_option_responsibility_review(case)
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


def _build_questions(
    case: Dict[str, Any], *, suppress: bool = False, now: str | None = None
) -> List[Dict[str, Any]]:
    """Build question list with values clarification or deadline priority.

    Priority order:
    1. Suppressed (IntentionGate reject / information complete) → []
    2. REQ-VALUES-001: values empty → Values Clarification Pack questions
    3. REQ-QST-001: unknowns + deadline → question_layer with deadline priority
    """
    if suppress:
        return []
    unknowns = case.get("unknowns", [])
    base_questions = build_questions(list(unknowns), case=case, now=now)

    # REQ-VALUES-001: when values empty, prepend value-clarification questions
    if needs_values_clarification(case):
        return build_values_clarification_questions(case, base_questions)

    return base_questions


def _should_suppress_questions(
    case: Dict[str, Any], run_result: Dict[str, Any]
) -> bool:
    """Suppress question layer when IntentionGate degrades output or case is already sufficient."""
    verdict = run_result.get("verdict")
    if isinstance(verdict, dict):
        decision = str(verdict.get("decision", "")).lower()
        if decision in {"reject", "revise"}:
            return True

    unknowns = case.get("unknowns", [])
    values = case.get("values", [])
    # Never suppress when values is empty — questions must be generated
    if not values:
        return False
    return not unknowns and bool(values)


# ── Trace ──────────────────────────────────────────────────────────────────


def _build_trace(
    now: str,
    *,
    arbitration_code: str = "",
    rules_fired: List[str] | None = None,
) -> Dict[str, Any]:
    """Build FR-TR-001 compliant 6-step trace.

    REQ-TRC-001: compose_output step carries arbitration_code in metrics.
    REQ-ETH-002: ethics_review step carries rules_fired in metrics.
    """
    base = _parse_base(now)

    steps = [
        {
            "name": "parse_input",
            "started_at": _ts(base, 0),
            "ended_at": _ts(base, 1),
            "summary": "入力YAMLを解析し、case_id・problem・values・constraints等を抽出した",
        },
        {
            "name": "generate_options",
            "started_at": _ts(base, 2),
            "ended_at": _ts(base, 3),
            "summary": "42人の哲学者による審議を経て選択肢を生成した",
        },
        {
            "name": "ethics_review",
            "started_at": _ts(base, 4),
            "ended_at": _ts(base, 5),
            "summary": "W_Ethics Gateによる3層倫理評価を適用した",
            "metrics": {"rules_fired": list(rules_fired or [])},
        },
        {
            "name": "responsibility_review",
            "started_at": _ts(base, 6),
            "ended_at": _ts(base, 7),
            "summary": "意思決定主体と利害関係者の責任構造を検証した",
        },
        {
            "name": "question_layer",
            "started_at": _ts(base, 8),
            "ended_at": _ts(base, 9),
            "summary": "不明点から優先度付き質問リストを生成した（deadline 優先順位付き）",
        },
        {
            "name": "compose_output",
            "started_at": _ts(base, 10),
            "ended_at": _ts(base, 11),
            "summary": "推奨・反証・代替案を含む出力を組み立てた",
            "metrics": {
                "arbitration_code": arbitration_code,
                "policy_version": "policy_v1",
            },
        },
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

    values = case.get("values", [])
    principles = _map_values_to_principles(values)

    # REQ-ARB-001: policy_v1 arbitration (M2)
    arbitration_code, recommended_option_id = arbitrate(case, run_result)

    options = _build_options(case, proposal, principles, now=now)
    recommendation = build_recommendation(
        case, run_result, arbitration_code, recommended_option_id
    )
    questions = _build_questions(
        case,
        suppress=_should_suppress_questions(case, run_result),
        now=now,
    )
    uncertainty = _build_uncertainty(case)

    # REQ-ETH-002: ethics_engine with rules_fired tracking (M2)
    ethics = build_ethics_summary(case, run_result=run_result)
    rules_fired = get_rules_fired(case, run_result=run_result)

    # M2-B responsibility_v1
    responsibility: Dict[str, Any] = build_responsibility_summary(case, values=values)

    trace = _build_trace(
        now, arbitration_code=arbitration_code, rules_fired=rules_fired
    )

    return {
        "meta": {
            "schema_version": _SCHEMA_VERSION,
            "pocore_version": _get_pocore_version(),
            "run_id": run_id,
            "created_at": now,
            "seed": seed,
            "deterministic": deterministic,
            "generator": {
                "name": _GENERATOR_NAME,
                "version": _get_generator_version(),
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
