"""
W_ethics Gate Type Definitions
==============================

Core data structures for the W_ethics Gate system.

This module defines:
- Evidence: Raw signal from violation detector
- Violation: Aggregated violation from multiple evidence pieces
- GateConfig: Gate configuration with thresholds
- GateDecision: Enum for gate outcomes (ALLOW, ALLOW_WITH_REPAIR, REJECT, ESCALATE)
- GateResult: Complete gate evaluation result
- Candidate: Evaluation target with scores and metadata
- AxisScore: Per-axis evaluation with evidence and confidence
- SelectionResult: Candidate selection outcome

Design Notes:
- Evidence is the raw signal from detectors (can have multiple per violation)
- Violations are aggregated from evidence using probabilistic OR
- semantic_drift is checked after repairs to detect goal changes

Reference: 01_specifications/wethics_gate/W_ETHICS_GATE.md
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


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
class Evidence:
    """
    Raw signal from a violation detector.

    Detectors produce Evidence, which is then aggregated into Violations.
    This separation allows multiple detectors to contribute to the same violation.

    Attributes:
        code: Violation code (W0-W4 as string)
        message: Human-readable description of the evidence
        strength: Strength of evidence in [0, 1]
        confidence: Confidence of detection in [0, 1]
        detector_id: ID of the detector that produced this evidence
        span: Optional (start, end) character positions in text
        tags: Optional tags for categorization
    """
    code: str  # "W0", "W1", "W2", "W3", "W4"
    message: str
    strength: float  # [0, 1]
    confidence: float  # [0, 1]
    detector_id: str
    span: Optional[Tuple[int, int]] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.strength = max(0.0, min(1.0, float(self.strength)))
        self.confidence = max(0.0, min(1.0, float(self.confidence)))


@dataclass
class Violation:
    """
    Aggregated W_ethics Gate violation from multiple evidence pieces.

    Aggregation uses probabilistic OR:
    - severity: 1 - Π(1 - strength_i)
    - confidence: 1 - Π(1 - confidence_i)

    Attributes:
        code: Violation type code (W0-W4 as string)
        severity: Aggregated severity in [0, 1]
        confidence: Aggregated confidence in [0, 1]
        repairable: Whether this violation can be repaired
        evidence: List of Evidence objects that contributed
        suggested_repairs: List of suggested repair descriptions
    """
    code: str  # "W0", "W1", "W2", "W3", "W4"
    severity: float  # [0, 1]
    confidence: float  # [0, 1]
    repairable: bool
    evidence: List[Evidence] = field(default_factory=list)
    suggested_repairs: List[str] = field(default_factory=list)

    @property
    def impact_score(self) -> float:
        """Calculate combined impact score (severity * confidence)."""
        return self.severity * self.confidence

    @property
    def is_hard_violation(self) -> bool:
        """Check if this is a hard (non-repairable) violation type."""
        return self.code in ("W0", "W1")


@dataclass
class GateConfig:
    """
    Configuration for W_ethics Gate.

    Attributes:
        tau_reject: Impact score threshold for immediate rejection (W0/W1)
        tau_repair: Impact score threshold for repair attempt (W2-W4)
        max_repairs: Maximum repair iterations
        tau_drift_reject: Semantic drift threshold for rejection
        tau_drift_escalate: Semantic drift threshold for escalation
        strict_no_escalate: If True, escalate becomes reject
    """
    tau_reject: float = 0.6
    tau_repair: float = 0.3
    max_repairs: int = 2
    tau_drift_reject: float = 0.7
    tau_drift_escalate: float = 0.4
    strict_no_escalate: bool = False


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
        repair_log: List of repair log strings
        drift_score: Semantic drift score after repairs
        drift_notes: Notes about semantic drift
        explanation: Human-readable explanation of decision
    """
    decision: GateDecision
    violations: List[Violation] = field(default_factory=list)
    repaired_text: Optional[str] = None
    repair_log: List[str] = field(default_factory=list)
    drift_score: Optional[float] = None
    drift_notes: Optional[str] = None
    explanation: str = ""

    @property
    def was_repaired(self) -> bool:
        """Check if any repairs were applied."""
        return len(self.repair_log) > 0


@dataclass
class Candidate:
    """
    Evaluation candidate (proposal, plan, output, action sequence).

    Attributes:
        cid: Unique candidate identifier
        text: Candidate text content
        meta: Additional metadata dictionary (can include 'goal' for drift check)
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


# Default thresholds (legacy, use GateConfig for new code)
DEFAULT_TAU_REJECT = 0.6
DEFAULT_TAU_REPAIR = 0.3
DEFAULT_MAX_REPAIRS = 2
DEFAULT_PBEST_THRESHOLD = 0.55


__all__ = [
    # Core types
    "GateDecision",
    "GateViolationCode",
    "RepairStage",
    # Evidence and Violations
    "Evidence",
    "Violation",
    # Configuration
    "GateConfig",
    # Scoring
    "AxisScore",
    "RepairAction",
    "GateResult",
    # Candidates
    "Candidate",
    "SelectionResult",
    # Constants
    "AXES",
    "AXIS_NAMES",
    "DEFAULT_TAU_REJECT",
    "DEFAULT_TAU_REPAIR",
    "DEFAULT_MAX_REPAIRS",
    "DEFAULT_PBEST_THRESHOLD",
]
