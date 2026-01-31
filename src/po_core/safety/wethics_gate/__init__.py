"""
W_ethics Gate Module
====================

Comprehensive ethical gate and selection system for Po_core.

This module provides:
1. **W_ethics Gate**: Hard constraint filtering (W0-W4 violations)
2. **ΔE Metrics**: Multi-axis scoring (Safety, Fairness, Privacy, Autonomy, Harm Avoidance)
3. **Selection Protocol**: Pareto + MCDA candidate selection

Design Philosophy:
- Gate is "inviolable constraint", NOT "optimization axis"
- Repair principle: Destruction/Exclusion/Dependency → Generation/Co-prosperity/Mutual Empowerment
- Three mandatory criteria for all repairs:
  1. Does not damage dignity of others
  2. Increases sustainability of relationships
  3. Mutual empowerment, not dependency

Usage:
    from po_core.safety.wethics_gate import (
        WethicsGate,
        MetricsEvaluator,
        CandidateSelector,
        Candidate,
    )

    # Create candidate
    candidate = Candidate(cid="c1", text="My proposal...")

    # Check against gate
    gate = WethicsGate()
    result = gate.check(candidate)

    # Full selection pipeline
    selector = CandidateSelector()
    selection = selector.select([candidate1, candidate2, candidate3])

Reference Specifications:
- 01_specifications/wethics_gate/W_ETHICS_GATE.md
- 01_specifications/wethics_gate/DELTA_E.md
- 01_specifications/wethics_gate/SELECTION_PROTOCOL.md
"""

from .types import (
    # Enums
    GateDecision,
    GateViolationCode,
    RepairStage,
    # Data classes
    AxisScore,
    Violation,
    RepairAction,
    GateResult,
    Candidate,
    SelectionResult,
    # Constants
    AXES,
    AXIS_NAMES,
    DEFAULT_TAU_REJECT,
    DEFAULT_TAU_REPAIR,
    DEFAULT_MAX_REPAIRS,
    DEFAULT_PBEST_THRESHOLD,
)

from .gate import (
    ViolationDetector,
    RepairEngine,
    DefaultViolationDetector,
    DefaultRepairEngine,
    WethicsGate,
    create_wethics_gate,
)

from .metrics import (
    AxisProfile,
    ContextProfile,
    AxisScorer,
    SafetyScorer,
    FairnessScorer,
    PrivacyScorer,
    AutonomyScorer,
    HarmAvoidanceScorer,
    MetricsEvaluator,
    create_metrics_evaluator,
)

from .select import (
    pareto_front,
    robust_weight_sampling_rank,
    topsis_rank,
    CandidateSelector,
    create_candidate_selector,
)

__all__ = [
    # Types - Enums
    "GateDecision",
    "GateViolationCode",
    "RepairStage",
    # Types - Data classes
    "AxisScore",
    "Violation",
    "RepairAction",
    "GateResult",
    "Candidate",
    "SelectionResult",
    # Types - Constants
    "AXES",
    "AXIS_NAMES",
    "DEFAULT_TAU_REJECT",
    "DEFAULT_TAU_REPAIR",
    "DEFAULT_MAX_REPAIRS",
    "DEFAULT_PBEST_THRESHOLD",
    # Gate
    "ViolationDetector",
    "RepairEngine",
    "DefaultViolationDetector",
    "DefaultRepairEngine",
    "WethicsGate",
    "create_wethics_gate",
    # Metrics
    "AxisProfile",
    "ContextProfile",
    "AxisScorer",
    "SafetyScorer",
    "FairnessScorer",
    "PrivacyScorer",
    "AutonomyScorer",
    "HarmAvoidanceScorer",
    "MetricsEvaluator",
    "create_metrics_evaluator",
    # Selection
    "pareto_front",
    "robust_weight_sampling_rank",
    "topsis_rank",
    "CandidateSelector",
    "create_candidate_selector",
]

__version__ = "0.1.0"
