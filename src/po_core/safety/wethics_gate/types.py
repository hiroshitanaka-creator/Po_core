"""
W_ethics Gate Type Definitions
==============================

Core data structures for the W_ethics Gate system.

This module defines:
- GateDecision: Enum for gate outcomes (ALLOW, ALLOW_WITH_REPAIR, REJECT, ESCALATE)
- GateViolationCode: Enum for violation types (W0-W4)
- AxisScore: Per-axis evaluation with evidence and confidence
- Violation: Detected gate violation with repair suggestions
- GateResult: Complete gate evaluation result
- Candidate: Evaluation target with scores and metadata
- RepairAction: Defined repair operations

Reference: 01_specifications/wethics_gate/W_ETHICS_GATE.md
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class GateDecision(str, Enum):
    """
    Gate decision outcomes.

    - ALLOW: Candidate passes without modification
    - ALLOW_WITH_REPAIR: Candidate passes after repair
    - REJECT: Candidate fails and cannot be repaired
    - ESCALATE: Insufficient evidence, requires human review
    """
    ALLOW = "allow"
    ALLOW_WITH_REPAIR = "allow_with_repair"
    REJECT = "reject"
    ESCALATE = "escalate"


class GateViolationCode(str, Enum):
    """
    Violation type codes per W_ethics Gate specification.

    Hard Reject (W0, W1):
    - W0: Irreversible Viability Harm
    - W1: Domination / Capture

    Repair Priority (W2-W4):
    - W2: Dignity Violation
    - W3: Dependency Engineering
    - W4: Structural Exclusion
    """
    W0_IRREVERSIBLE_VIABILITY_HARM = "W0"
    W1_DOMINATION_CAPTURE = "W1"
    W2_DIGNITY_VIOLATION = "W2"
    W3_DEPENDENCY_ENGINEERING = "W3"
    W4_STRUCTURAL_EXCLUSION = "W4"


class RepairStage(str, Enum):
    """
    Repair stages in order of application.

    1. CONCEPT_MAPPING: Map destructive concepts to constructive ones
    2. CONSTRAINT_INJECTION: Add consent, options, safety measures
    3. SCOPE_REDUCTION: Reduce impact scope/authority/duration
    4. GOAL_REFRAME: Redefine goal to achieve same value differently
    """
    CONCEPT_MAPPING = "concept_mapping"
    CONSTRAINT_INJECTION = "constraint_injection"
    SCOPE_REDUCTION = "scope_reduction"
    GOAL_REFRAME = "goal_reframe"


@dataclass
class AxisScore:
    """
    Score for a single evaluation axis (A-E).

    Attributes:
        value: Score in [0, 1], where 1.0 is ideal
        confidence: Confidence in [0, 1]
        evidence: List of supporting evidence strings
        counterevidence: List of contradicting evidence strings
        notes: Additional notes for audit
    """
    value: float  # [0, 1]
    confidence: float  # [0, 1]
    evidence: List[str] = field(default_factory=list)
    counterevidence: List[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        """Validate score ranges."""
        self.value = max(0.0, min(1.0, self.value))
        self.confidence = max(0.0, min(1.0, self.confidence))


@dataclass
class Violation:
    """
    Detected W_ethics Gate violation.

    Attributes:
        code: Violation type code (W0-W4)
        severity: Severity in [0, 1]
        confidence: Detection confidence in [0, 1]
        evidence: List of evidence strings
        repairable: Whether this violation can be repaired
        suggested_repairs: List of suggested repair descriptions
    """
    code: GateViolationCode
    severity: float  # [0, 1]
    confidence: float  # [0, 1]
    evidence: List[str]
    repairable: bool
    suggested_repairs: List[str] = field(default_factory=list)

    @property
    def impact_score(self) -> float:
        """Calculate combined impact score (severity * confidence)."""
        return self.severity * self.confidence

    @property
    def is_hard_violation(self) -> bool:
        """Check if this is a hard (non-repairable) violation type."""
        return self.code in (
            GateViolationCode.W0_IRREVERSIBLE_VIABILITY_HARM,
            GateViolationCode.W1_DOMINATION_CAPTURE,
        )


@dataclass
class RepairAction:
    """
    A repair action applied to a candidate.

    Attributes:
        stage: Which repair stage this action belongs to
        description: Human-readable description of the repair
        before_text: Original text segment
        after_text: Repaired text segment
        semantic_drift: Estimated semantic drift in [0, 1]
    """
    stage: RepairStage
    description: str
    before_text: str
    after_text: str
    semantic_drift: float = 0.0


@dataclass
class GateResult:
    """
    Complete result of W_ethics Gate evaluation.

    Attributes:
        decision: Final gate decision (ALLOW, ALLOW_WITH_REPAIR, REJECT, ESCALATE)
        violations: List of detected violations
        repaired_text: Text after repairs (if any)
        repair_log: List of repair actions applied
        explanation: Human-readable explanation of decision
    """
    decision: GateDecision
    violations: List[Violation] = field(default_factory=list)
    repaired_text: Optional[str] = None
    repair_log: List[RepairAction] = field(default_factory=list)
    explanation: str = ""

    @property
    def was_repaired(self) -> bool:
        """Check if any repairs were applied."""
        return len(self.repair_log) > 0

    @property
    def total_semantic_drift(self) -> float:
        """Calculate total semantic drift from all repairs."""
        return sum(r.semantic_drift for r in self.repair_log)


@dataclass
class Candidate:
    """
    Evaluation candidate (proposal, plan, output, action sequence).

    Attributes:
        cid: Unique candidate identifier
        text: Candidate text content
        meta: Additional metadata dictionary
        scores: Axis scores dictionary ("A" through "E")
        gate_result: W_ethics Gate evaluation result (if evaluated)
        source_philosopher: Source philosopher module (if applicable)
    """
    cid: str
    text: str
    meta: Dict[str, Any] = field(default_factory=dict)
    scores: Dict[str, AxisScore] = field(default_factory=dict)
    gate_result: Optional[GateResult] = None
    source_philosopher: Optional[str] = None

    def is_gate_passed(self) -> bool:
        """Check if candidate passed the W_ethics Gate."""
        if self.gate_result is None:
            return False
        return self.gate_result.decision in (
            GateDecision.ALLOW,
            GateDecision.ALLOW_WITH_REPAIR,
        )

    def get_score_vector(self) -> Dict[str, float]:
        """Get axis scores as a simple float dictionary."""
        return {k: v.value for k, v in self.scores.items()}


@dataclass
class SelectionResult:
    """
    Result of candidate selection process.

    Attributes:
        selected_id: ID of selected candidate (or None if none selected)
        pareto_set_ids: IDs of candidates in Pareto front
        mcda_method: MCDA method used (robust-weight, topsis, etc.)
        weights_profile: Weight ranges or distribution used
        p_best: Win probability for robust weight method
        explanation: Human-readable explanation
        rejected: List of rejected candidate info
    """
    selected_id: Optional[str]
    pareto_set_ids: List[str]
    mcda_method: str
    weights_profile: Dict[str, Any]
    p_best: Optional[float] = None
    explanation: str = ""
    rejected: List[Dict[str, Any]] = field(default_factory=list)


# Axis identifiers
AXES = ("A", "B", "C", "D", "E")
AXIS_NAMES = {
    "A": "Safety",
    "B": "Fairness",
    "C": "Privacy",
    "D": "Autonomy",
    "E": "Harm Avoidance",
}


# Default thresholds
DEFAULT_TAU_REJECT = 0.6  # Impact score threshold for immediate rejection
DEFAULT_TAU_REPAIR = 0.3  # Impact score threshold for repair attempt
DEFAULT_MAX_REPAIRS = 2   # Maximum repair iterations
DEFAULT_PBEST_THRESHOLD = 0.55  # Win probability threshold for selection


__all__ = [
    "GateDecision",
    "GateViolationCode",
    "RepairStage",
    "AxisScore",
    "Violation",
    "RepairAction",
    "GateResult",
    "Candidate",
    "SelectionResult",
    "AXES",
    "AXIS_NAMES",
    "DEFAULT_TAU_REJECT",
    "DEFAULT_TAU_REPAIR",
    "DEFAULT_MAX_REPAIRS",
    "DEFAULT_PBEST_THRESHOLD",
]
