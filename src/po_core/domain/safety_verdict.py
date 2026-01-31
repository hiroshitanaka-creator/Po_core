"""
SafetyVerdict - Safety gate verdict.

This is what the safety/wethics_gate/ module OUTPUTS.
It represents the judgment of the safety gate.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class VerdictType(str, Enum):
    """Type of safety verdict."""

    ALLOW = "allow"
    """Proposal passes without modification."""

    ALLOW_WITH_REPAIR = "allow_with_repair"
    """Proposal passes after repair."""

    REJECT = "reject"
    """Proposal is rejected and cannot be repaired."""

    ESCALATE = "escalate"
    """Proposal requires human review."""


@dataclass
class ViolationInfo:
    """
    Information about a detected violation.

    This is a simplified view of violations for domain-level use.
    The full violation details are in safety/wethics_gate/types.py.
    """

    code: str
    """Violation code (W0-W4)."""

    severity: float
    """Severity in [0, 1]."""

    description: str
    """Human-readable description."""

    repairable: bool
    """Whether this violation can be repaired."""

    rule_id: Optional[str] = None
    """ID of the rule that was violated."""

    span: Optional[tuple] = None
    """Optional (start, end) character positions in text."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "code": self.code,
            "severity": self.severity,
            "description": self.description,
            "repairable": self.repairable,
        }
        if self.rule_id:
            result["rule_id"] = self.rule_id
        if self.span:
            result["span"] = list(self.span)
        return result

    @property
    def is_hard_violation(self) -> bool:
        """Check if this is a hard (non-repairable) violation type."""
        return self.code in ("W0", "W1")


@dataclass
class SafetyVerdict:
    """
    The verdict from the safety gate.

    This is the OUTPUT contract from the safety/wethics_gate/ module.

    The gate is a "court" that:
    - JUDGES: Outputs ALLOW, ALLOW_WITH_REPAIR, REJECT, or ESCALATE
    - Does NOT generate proposals or suggest alternatives
    - Does NOT access philosopher internals

    Attributes:
        verdict_id: Unique verdict identifier
        verdict_type: The judgment (ALLOW, REJECT, etc.)
        proposal_id: ID of the proposal that was judged
        violations: List of detected violations
        repaired_text: Text after repairs (if any)
        repair_log: Log of repairs applied
        drift_score: Semantic drift after repair (if applicable)
        explanation: Human-readable explanation
        created_at: When this verdict was issued
        metadata: Additional metadata
    """

    verdict_type: VerdictType
    """The judgment."""

    proposal_id: str
    """ID of the judged proposal."""

    violations: List[ViolationInfo] = field(default_factory=list)
    """Detected violations."""

    verdict_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """Unique verdict identifier."""

    repaired_text: Optional[str] = None
    """Text after repairs (only for ALLOW_WITH_REPAIR)."""

    repair_log: List[str] = field(default_factory=list)
    """Log of repairs applied."""

    drift_score: Optional[float] = None
    """Semantic drift score after repair."""

    explanation: str = ""
    """Human-readable explanation of the verdict."""

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    """Creation timestamp."""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata."""

    @property
    def is_allowed(self) -> bool:
        """Check if the proposal is allowed (with or without repair)."""
        return self.verdict_type in (VerdictType.ALLOW, VerdictType.ALLOW_WITH_REPAIR)

    @property
    def is_rejected(self) -> bool:
        """Check if the proposal is rejected."""
        return self.verdict_type == VerdictType.REJECT

    @property
    def needs_escalation(self) -> bool:
        """Check if the proposal needs human review."""
        return self.verdict_type == VerdictType.ESCALATE

    @property
    def was_repaired(self) -> bool:
        """Check if repairs were applied."""
        return len(self.repair_log) > 0

    @property
    def has_hard_violations(self) -> bool:
        """Check if any hard (W0/W1) violations were detected."""
        return any(v.is_hard_violation for v in self.violations)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "verdict_id": self.verdict_id,
            "verdict_type": self.verdict_type.value,
            "proposal_id": self.proposal_id,
            "violations": [v.to_dict() for v in self.violations],
            "explanation": self.explanation,
            "created_at": self.created_at,
        }
        if self.repaired_text is not None:
            result["repaired_text"] = self.repaired_text
        if self.repair_log:
            result["repair_log"] = self.repair_log
        if self.drift_score is not None:
            result["drift_score"] = self.drift_score
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    @classmethod
    def allow(cls, proposal_id: str, explanation: str = "No violations") -> "SafetyVerdict":
        """Create an ALLOW verdict."""
        return cls(
            verdict_type=VerdictType.ALLOW,
            proposal_id=proposal_id,
            explanation=explanation,
        )

    @classmethod
    def reject(
        cls,
        proposal_id: str,
        violations: List[ViolationInfo],
        explanation: str,
    ) -> "SafetyVerdict":
        """Create a REJECT verdict."""
        return cls(
            verdict_type=VerdictType.REJECT,
            proposal_id=proposal_id,
            violations=violations,
            explanation=explanation,
        )

    @classmethod
    def allow_with_repair(
        cls,
        proposal_id: str,
        repaired_text: str,
        repair_log: List[str],
        violations: List[ViolationInfo],
        drift_score: Optional[float] = None,
        explanation: str = "Repair succeeded",
    ) -> "SafetyVerdict":
        """Create an ALLOW_WITH_REPAIR verdict."""
        return cls(
            verdict_type=VerdictType.ALLOW_WITH_REPAIR,
            proposal_id=proposal_id,
            repaired_text=repaired_text,
            repair_log=repair_log,
            violations=violations,
            drift_score=drift_score,
            explanation=explanation,
        )


__all__ = ["SafetyVerdict", "VerdictType", "ViolationInfo"]
