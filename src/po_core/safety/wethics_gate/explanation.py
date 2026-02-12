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
    repair_steps = [RepairStep(description=log_entry) for log_entry in result.repair_log]

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
    decision_str = result.decision.value if isinstance(result.decision, GateDecision) else str(result.decision)

    if decision_str == "allow":
        summary = "Gate passed with no issues."
    elif decision_str == "allow_with_repair":
        summary = f"Gate passed after {n_repairs} repair(s) for {n_violations} violation(s)."
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


__all__ = [
    "EvidenceSummary",
    "ViolationStep",
    "RepairStep",
    "DriftStep",
    "ExplanationChain",
    "build_explanation_chain",
]
