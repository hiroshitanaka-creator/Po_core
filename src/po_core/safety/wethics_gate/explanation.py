"""
W_Ethics Gate Explanation Chain
===============================

Structured, auditable explanation of W_Ethics Gate decisions.

Transforms a GateResult into a multi-step ExplanationChain that shows:
1. What was detected (evidence → violation aggregation)
2. What the gate decided and why (thresholds, rules)
3. What repairs were attempted and their effects
4. Semantic drift assessment

This module is the foundation for Phase 3 Explainable W_Ethics Gate.

Usage::

    from po_core.safety.wethics_gate.explanation import build_explanation_chain
    from po_core.safety.wethics_gate.types import GateResult

    chain = build_explanation_chain(result)
    print(chain.to_markdown())     # Human-readable report
    print(chain.to_dict())         # JSON-serializable for WebUI

Design Notes:
- Pure data transformation: GateResult → ExplanationChain
- No side effects, no I/O
- Markdown output is viewer-friendly (can embed in PoViewer reports)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .types import GateDecision, GateResult, Violation


@dataclass(frozen=True)
class EvidenceSummary:
    """Summary of a single piece of evidence contributing to a violation."""

    detector_id: str
    message: str
    strength: float
    confidence: float
    tags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ViolationStep:
    """
    Explanation step for a detected violation.

    Shows how evidence was aggregated into a violation and whether
    it is repairable.
    """

    code: str
    severity: float
    confidence: float
    repairable: bool
    evidence: List[EvidenceSummary]
    suggested_repairs: List[str]

    @property
    def impact_score(self) -> float:
        return self.severity * self.confidence

    @property
    def code_label(self) -> str:
        labels = {
            "W0": "Irreversible Viability Harm",
            "W1": "Domination / Capture",
            "W2": "Dignity Violation",
            "W3": "Dependency Engineering",
            "W4": "Structural Exclusion",
        }
        return labels.get(self.code, self.code)


@dataclass(frozen=True)
class RepairStep:
    """Explanation step for a repair action."""

    description: str
    stage: str = ""


@dataclass(frozen=True)
class DriftStep:
    """Explanation step for semantic drift assessment."""

    drift_score: float
    threshold_escalate: float
    threshold_reject: float
    notes: str = ""

    @property
    def status(self) -> str:
        if self.drift_score >= self.threshold_reject:
            return "rejected"
        if self.drift_score >= self.threshold_escalate:
            return "escalated"
        return "acceptable"


@dataclass(frozen=True)
class ExplanationChain:
    """
    Complete structured explanation of a W_Ethics Gate decision.

    This is the core Phase 3 explainability artifact.
    """

    decision: str
    decision_reason: str
    violations: List[ViolationStep]
    repairs: List[RepairStep]
    drift: Optional[DriftStep]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict for WebUI."""
        return {
            "decision": self.decision,
            "decision_reason": self.decision_reason,
            "violations": [
                {
                    "code": v.code,
                    "label": v.code_label,
                    "severity": v.severity,
                    "confidence": v.confidence,
                    "impact_score": v.impact_score,
                    "repairable": v.repairable,
                    "evidence": [
                        {
                            "detector_id": e.detector_id,
                            "message": e.message,
                            "strength": e.strength,
                            "confidence": e.confidence,
                            "tags": e.tags,
                        }
                        for e in v.evidence
                    ],
                    "suggested_repairs": v.suggested_repairs,
                }
                for v in self.violations
            ],
            "repairs": [
                {"description": r.description, "stage": r.stage} for r in self.repairs
            ],
            "drift": (
                {
                    "drift_score": self.drift.drift_score,
                    "status": self.drift.status,
                    "notes": self.drift.notes,
                }
                if self.drift
                else None
            ),
            "summary": self.summary,
        }

    def to_markdown(self) -> str:
        """Render as human-readable Markdown report."""
        lines: List[str] = []

        # Header
        lines.append("## W_Ethics Gate Decision")
        lines.append("")
        lines.append(f"**Decision:** `{self.decision}`")
        lines.append(f"**Reason:** {self.decision_reason}")
        lines.append("")

        # Violations
        if self.violations:
            lines.append("### Violations Detected")
            lines.append("")
            for v in self.violations:
                repair_tag = "repairable" if v.repairable else "hard reject"
                lines.append(
                    f"- **{v.code} ({v.code_label})** — "
                    f"severity={v.severity:.2f}, confidence={v.confidence:.2f}, "
                    f"impact={v.impact_score:.2f} [{repair_tag}]"
                )
                for e in v.evidence:
                    lines.append(
                        f"  - [{e.detector_id}] {e.message} "
                        f"(strength={e.strength:.2f})"
                    )
            lines.append("")

        # Repairs
        if self.repairs:
            lines.append("### Repairs Applied")
            lines.append("")
            for i, r in enumerate(self.repairs, 1):
                lines.append(f"{i}. {r.description}")
            lines.append("")

        # Drift
        if self.drift:
            lines.append("### Semantic Drift")
            lines.append("")
            lines.append(
                f"- Score: {self.drift.drift_score:.2f} "
                f"(status: {self.drift.status})"
            )
            if self.drift.notes:
                lines.append(f"- Notes: {self.drift.notes}")
            lines.append("")

        # Summary
        lines.append(f"**Summary:** {self.summary}")

        return "\n".join(lines)


def _build_violation_step(v: Violation) -> ViolationStep:
    """Convert a Violation to a ViolationStep for the explanation chain."""
    evidence = [
        EvidenceSummary(
            detector_id=e.detector_id,
            message=e.message,
            strength=e.strength,
            confidence=e.confidence,
            tags=list(e.tags),
        )
        for e in v.evidence
    ]
    return ViolationStep(
        code=v.code,
        severity=v.severity,
        confidence=v.confidence,
        repairable=v.repairable,
        evidence=evidence,
        suggested_repairs=list(v.suggested_repairs),
    )


def build_explanation_chain(
    result: GateResult,
    drift_threshold_escalate: float = 0.4,
    drift_threshold_reject: float = 0.7,
) -> ExplanationChain:
    """
    Build a structured ExplanationChain from a GateResult.

    Args:
        result: The GateResult from WethicsGate.check()
        drift_threshold_escalate: Drift threshold for escalation (for display)
        drift_threshold_reject: Drift threshold for rejection (for display)

    Returns:
        ExplanationChain with full audit trail
    """
    # Violations
    violation_steps = [_build_violation_step(v) for v in result.violations]

    # Repairs
    repair_steps = [
        RepairStep(description=log_entry) for log_entry in result.repair_log
    ]

    # Drift
    drift_step = None
    if result.drift_score is not None:
        drift_step = DriftStep(
            drift_score=result.drift_score,
            threshold_escalate=drift_threshold_escalate,
            threshold_reject=drift_threshold_reject,
            notes=result.drift_notes or "",
        )

    # Summary
    n_violations = len(result.violations)
    n_repairs = len(result.repair_log)
    decision_str = (
        result.decision.value
        if isinstance(result.decision, GateDecision)
        else str(result.decision)
    )

    if decision_str == "allow":
        summary = "Gate passed with no issues."
    elif decision_str == "allow_with_repair":
        summary = (
            f"Gate passed after {n_repairs} repair(s) for {n_violations} violation(s)."
        )
    elif decision_str == "reject":
        summary = f"Gate rejected: {n_violations} violation(s) detected."
    elif decision_str == "escalate":
        summary = f"Gate escalated for human review: {n_violations} violation(s)."
    else:
        summary = f"Gate decision: {decision_str}"

    return ExplanationChain(
        decision=decision_str,
        decision_reason=result.explanation,
        violations=violation_steps,
        repairs=repair_steps,
        drift=drift_step,
        summary=summary,
    )


def build_explanation_from_verdict(
    verdict: "SafetyVerdict",
    stage: str = "action",
) -> ExplanationChain:
    """
    Build an ExplanationChain from a domain-level SafetyVerdict.

    This is the pipeline-integrated path: the WethicsGatePort returns
    SafetyVerdict, so we construct an explanation from the available
    data (decision, rule_ids, reasons, required_changes).

    For richer explanations with full violation/evidence/repair data,
    use ``build_explanation_chain()`` with a GateResult instead.

    Args:
        verdict: SafetyVerdict from WethicsGatePort.judge_action()
        stage: Pipeline stage ("intention" or "action")

    Returns:
        ExplanationChain with audit trail derived from verdict
    """
    from po_core.domain.safety_verdict import Decision

    decision_str = (
        verdict.decision.value
        if hasattr(verdict.decision, "value")
        else str(verdict.decision)
    )

    # Map REVISE → allow_with_repair for explanation consistency
    display_decision = {
        "allow": "allow",
        "reject": "reject",
        "revise": "allow_with_repair",
    }.get(decision_str, decision_str)

    # Build violation steps from rule_ids + reasons
    violations: List[ViolationStep] = []
    for i, rule_id in enumerate(verdict.rule_ids):
        reason = verdict.reasons[i] if i < len(verdict.reasons) else rule_id
        violations.append(
            ViolationStep(
                code=rule_id.split("_")[0].upper() if "_" in rule_id else rule_id,
                severity=1.0 if verdict.decision == Decision.REJECT else 0.5,
                confidence=0.8,
                repairable=verdict.decision != Decision.REJECT,
                evidence=[
                    EvidenceSummary(
                        detector_id=f"policy:{rule_id}",
                        message=reason,
                        strength=(1.0 if verdict.decision == Decision.REJECT else 0.5),
                        confidence=0.8,
                    )
                ],
                suggested_repairs=list(verdict.required_changes),
            )
        )

    # Build repair steps from required_changes
    repairs: List[RepairStep] = [
        RepairStep(description=change, stage=stage)
        for change in verdict.required_changes
    ]

    # Summary
    n_v = len(violations)
    n_r = len(repairs)
    if display_decision == "allow":
        summary = "Gate passed with no issues."
    elif display_decision == "allow_with_repair":
        summary = f"Gate passed after {n_r} repair(s) for {n_v} policy trigger(s)."
    elif display_decision == "reject":
        summary = f"Gate rejected: {n_v} policy violation(s) detected."
    else:
        summary = f"Gate decision: {display_decision}"

    decision_reason = (
        "; ".join(verdict.reasons)
        if verdict.reasons
        else f"{stage} gate {display_decision}"
    )

    return ExplanationChain(
        decision=display_decision,
        decision_reason=decision_reason,
        violations=violations,
        repairs=repairs,
        drift=None,
        summary=summary,
    )


def extract_explanation_from_events(
    events: "Sequence[TraceEvent]",
) -> Optional[ExplanationChain]:
    """
    Extract an ExplanationChain from a sequence of TraceEvents.

    Looks for an ``ExplanationEmitted`` event and reconstructs the
    ExplanationChain from its payload.

    Args:
        events: TraceEvents from a pipeline run

    Returns:
        ExplanationChain if found, None otherwise
    """
    for e in reversed(events):
        if e.event_type != "ExplanationEmitted":
            continue
        p = e.payload
        if not isinstance(p, dict) or "decision" not in p:
            continue

        violations = [
            ViolationStep(
                code=v.get("code", ""),
                severity=v.get("severity", 0.0),
                confidence=v.get("confidence", 0.0),
                repairable=v.get("repairable", True),
                evidence=[
                    EvidenceSummary(
                        detector_id=ev.get("detector_id", ""),
                        message=ev.get("message", ""),
                        strength=ev.get("strength", 0.0),
                        confidence=ev.get("confidence", 0.0),
                        tags=ev.get("tags", []),
                    )
                    for ev in v.get("evidence", [])
                ],
                suggested_repairs=v.get("suggested_repairs", []),
            )
            for v in p.get("violations", [])
        ]

        repairs = [
            RepairStep(description=r.get("description", ""), stage=r.get("stage", ""))
            for r in p.get("repairs", [])
        ]

        drift_data = p.get("drift")
        drift = (
            DriftStep(
                drift_score=drift_data.get("drift_score", 0.0),
                threshold_escalate=drift_data.get("threshold_escalate", 0.4),
                threshold_reject=drift_data.get("threshold_reject", 0.7),
                notes=drift_data.get("notes", ""),
            )
            if drift_data
            else None
        )

        return ExplanationChain(
            decision=p["decision"],
            decision_reason=p.get("decision_reason", ""),
            violations=violations,
            repairs=repairs,
            drift=drift,
            summary=p.get("summary", ""),
        )

    return None


__all__ = [
    "EvidenceSummary",
    "ViolationStep",
    "RepairStep",
    "DriftStep",
    "ExplanationChain",
    "build_explanation_chain",
    "build_explanation_from_verdict",
    "extract_explanation_from_events",
]
