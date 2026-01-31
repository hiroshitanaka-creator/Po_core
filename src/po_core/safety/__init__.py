"""
Po_core Safety System
=====================

Comprehensive safety framework for philosophical reasoning:

1. **Philosopher Profiles** (philosopher_profiles.py)
   - Safety tier classification (TRUSTED, RESTRICTED, MONITORED)
   - Risk factor identification
   - Usage validation

2. **W_ethics Boundaries** (w_ethics.py)
   - Absolute ethical red lines
   - Automatic violation detection
   - Session auto-stop on severe violations

3. **W_ethics Gate** (wethics_gate/)
   - Hard constraint filtering (W0-W4 violations)
   - Multi-axis scoring (Safety, Fairness, Privacy, Autonomy, Harm Avoidance)
   - Pareto + MCDA candidate selection
   - Repair mechanism for salvageable proposals

Purpose: Enable legitimate research while preventing misuse.
"""

from po_core.safety.philosopher_profiles import (
    SafetyTier,
    EthicalRiskPattern,
    PHILOSOPHER_SAFETY_PROFILES,
    get_trusted_philosophers,
    get_restricted_philosophers,
    get_monitored_philosophers,
    is_safe_for_general_use,
    requires_dangerous_pattern_mode,
    get_risk_factors,
    validate_philosopher_group,
)

from po_core.safety.w_ethics import (
    ViolationType,
    ViolationPattern,
    EthicsViolation,
    WEthicsGuardian,
    create_ethics_guardian,
    VIOLATION_PATTERNS,
)

# W_ethics Gate (advanced filtering and selection)
from po_core.safety.wethics_gate import (
    # Gate types
    GateDecision,
    GateViolationCode,
    RepairStage,
    AxisScore,
    Violation,
    RepairAction,
    GateResult,
    Candidate,
    SelectionResult,
    # Gate
    WethicsGate,
    create_wethics_gate,
    # Metrics
    ContextProfile,
    MetricsEvaluator,
    create_metrics_evaluator,
    # Selection
    CandidateSelector,
    create_candidate_selector,
    pareto_front,
)

__all__ = [
    # Philosopher profiles
    "SafetyTier",
    "EthicalRiskPattern",
    "PHILOSOPHER_SAFETY_PROFILES",
    "get_trusted_philosophers",
    "get_restricted_philosophers",
    "get_monitored_philosophers",
    "is_safe_for_general_use",
    "requires_dangerous_pattern_mode",
    "get_risk_factors",
    "validate_philosopher_group",

    # W_ethics boundaries
    "ViolationType",
    "ViolationPattern",
    "EthicsViolation",
    "WEthicsGuardian",
    "create_ethics_guardian",
    "VIOLATION_PATTERNS",

    # W_ethics Gate types
    "GateDecision",
    "GateViolationCode",
    "RepairStage",
    "AxisScore",
    "Violation",
    "RepairAction",
    "GateResult",
    "Candidate",
    "SelectionResult",

    # W_ethics Gate
    "WethicsGate",
    "create_wethics_gate",

    # W_ethics Metrics
    "ContextProfile",
    "MetricsEvaluator",
    "create_metrics_evaluator",

    # W_ethics Selection
    "CandidateSelector",
    "create_candidate_selector",
    "pareto_front",
]
