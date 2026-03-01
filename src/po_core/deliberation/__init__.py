"""Public exports for deliberation package."""

from po_core.deliberation.clustering import ClusterResult, PositionClusterer
from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.engine import DeliberationEngine, DeliberationResult, RoundTrace
from po_core.deliberation.influence import InfluenceTracker, InfluenceWeight
from po_core.deliberation.protocol import (
    ArgumentCard,
    CritiqueCard,
    SynthesisEngine,
    run_deliberation,
)
from po_core.deliberation.roles import (
    SYNTHESIZER_PHILOSOPHERS,
    DebateRole,
    assign_role,
    get_role_prompt_prefix,
)
from po_core.deliberation.synthesis import AxisSpec, ScoreboardEntry, SynthesisReport

__all__ = [
    "ClusterResult",
    "DeliberationEngine",
    "DeliberationResult",
    "PositionClusterer",
    "RoundTrace",
    "EmergenceDetector",
    "EmergenceSignal",
    "InfluenceTracker",
    "InfluenceWeight",
    "DebateRole",
    "SYNTHESIZER_PHILOSOPHERS",
    "assign_role",
    "get_role_prompt_prefix",
    "ArgumentCard",
    "CritiqueCard",
    "SynthesisEngine",
    "run_deliberation",
    "AxisSpec",
    "ScoreboardEntry",
    "SynthesisReport",
]
