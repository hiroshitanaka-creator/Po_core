"""
W_ethics Gate Module
====================

Comprehensive ethical gate and selection system for Po_core.

This module provides:
1. **W_ethics Gate**: Hard constraint filtering (W0-W4 violations)
2. **Violation Detectors**: Plugin interface for violation detection
3. **Semantic Drift**: Goal-change detection after repairs
4. **ΔE Metrics**: Multi-axis scoring (Safety, Fairness, Privacy, Autonomy, Harm Avoidance)
5. **Selection Protocol**: Pareto + MCDA candidate selection

Design Philosophy:
- Gate is "inviolable constraint", NOT "optimization axis"
- Repair principle: Destruction/Exclusion/Dependency → Generation/Co-prosperity/Mutual Empowerment
- Three mandatory criteria for all repairs:
  1. Does not damage dignity of others
  2. Increases sustainability of relationships
  3. Mutual empowerment, not dependency

New in v0.2:
- Evidence/Violation separation for multi-detector aggregation
- semantic_drift for goal-change detection
- DetectorRegistry for pluggable detectors
- GateConfig for centralized configuration

Usage:
    from po_core.safety.wethics_gate import (
        WethicsGate,
        Candidate,
        GateDecision,
        semantic_drift,
    )

    # Create candidate
    candidate = Candidate(cid="c1", text="My proposal...")

    # Check against gate
    gate = WethicsGate()
    result = gate.check(candidate)

    if result.decision == GateDecision.ALLOW:
        print("Approved!")
    elif result.decision == GateDecision.ALLOW_WITH_REPAIR:
        print(f"Approved with repairs: {result.repaired_text}")

Reference Specifications:
- 01_specifications/wethics_gate/W_ETHICS_GATE.md
- 01_specifications/wethics_gate/DELTA_E.md
- 01_specifications/wethics_gate/SELECTION_PROTOCOL.md
"""

from .action_gate import (
    ActionGate,
    TwoStageGate,
    check_proposal,
)
from .detectors import (
    DetectorRegistry,
    EnglishKeywordViolationDetector,
    KeywordRule,
    KeywordViolationDetector,
    ViolationDetector,
    aggregate_evidence_to_violations,
    create_default_registry,
)
from .gate import (
    RuleBasedRepairEngine,
    WethicsGate,
    create_wethics_gate,
)

# 2-Stage Gate (new in v0.3)
from .intention_gate import (
    IntentionDecision,
    IntentionGate,
    IntentionVerdict,
    check_intent,
)
from .metrics import (
    AutonomyScorer,
    AxisProfile,
    AxisScorer,
    ContextProfile,
    FairnessScorer,
    HarmAvoidanceScorer,
    MetricsEvaluator,
    PrivacyScorer,
    SafetyScorer,
    create_metrics_evaluator,
)
from .select import (
    CandidateSelector,
    create_candidate_selector,
    pareto_front,
    robust_weight_sampling_rank,
    topsis_rank,
)
from .semantic_drift import (
    DriftReport,
    semantic_drift,
)
from .types import (  # Enums; Data classes; Constants
    AXES,
    AXIS_NAMES,
    DEFAULT_MAX_REPAIRS,
    DEFAULT_PBEST_THRESHOLD,
    DEFAULT_TAU_REJECT,
    DEFAULT_TAU_REPAIR,
    AxisScore,
    Candidate,
    Evidence,
    GateConfig,
    GateDecision,
    GateResult,
    GateViolationCode,
    RepairAction,
    RepairStage,
    SelectionResult,
    Violation,
)

__all__ = [
    # Types - Enums
    "GateDecision",
    "GateViolationCode",
    "RepairStage",
    # Types - Evidence & Violations
    "Evidence",
    "Violation",
    "GateConfig",
    # Types - Scoring
    "AxisScore",
    "RepairAction",
    "GateResult",
    # Types - Candidates
    "Candidate",
    "SelectionResult",
    # Types - Constants
    "AXES",
    "AXIS_NAMES",
    "DEFAULT_TAU_REJECT",
    "DEFAULT_TAU_REPAIR",
    "DEFAULT_MAX_REPAIRS",
    "DEFAULT_PBEST_THRESHOLD",
    # Detectors
    "ViolationDetector",
    "DetectorRegistry",
    "KeywordRule",
    "KeywordViolationDetector",
    "EnglishKeywordViolationDetector",
    "aggregate_evidence_to_violations",
    "create_default_registry",
    # Semantic Drift
    "DriftReport",
    "semantic_drift",
    # Gate
    "RuleBasedRepairEngine",
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
    # 2-Stage Gate (new in v0.3)
    "IntentionDecision",
    "IntentionVerdict",
    "IntentionGate",
    "check_intent",
    "ActionGate",
    "TwoStageGate",
    "check_proposal",
]

__version__ = "0.3.0"
