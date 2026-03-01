"""
Deliberation Engine
====================

Multi-round philosopher dialogue for emergent philosophical reasoning.

Round 1: All philosophers propose() independently (current pipeline behavior).
Round 2: InteractionMatrix identifies high-interference pairs.
         Those philosophers receive counterarguments and re-propose.
Round N: Repeat until max_rounds or convergence.

Phase 6-B additions:
- EmergenceDetector: detects genuinely novel proposals vs round-1 baseline
- InfluenceTracker: tracks how much each philosopher moved others

Usage:
    from po_core.deliberation import DeliberationEngine, EmergenceDetector

    engine = DeliberationEngine(max_rounds=2, top_k_pairs=5)
    result = engine.deliberate(philosophers, ctx, intent, tensors, memory, round1_proposals)
    print(result.peak_novelty)   # 0.0-1.0
    print(result.has_emergence)  # True if novel synthesis detected
"""

from po_core.deliberation.clustering import ClusterResult, PositionClusterer
from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.engine import DeliberationEngine, DeliberationResult, RoundTrace
from po_core.deliberation.influence import InfluenceTracker, InfluenceWeight
from po_core.deliberation.protocol import (
    ArgumentCard as ProtocolArgumentCard,
    CritiqueCard as ProtocolCritiqueCard,
    SynthesisEngine as ProtocolSynthesisEngine,
    run_deliberation,
)
from po_core.deliberation.roles import (
    SYNTHESIZER_PHILOSOPHERS,
    DebateRole,
    assign_role,
    get_role_prompt_prefix,
)
from po_core.deliberation.synthesis import (
    ArgumentCard,
    AxisSpec,
    CritiqueCard,
    ScoreboardEntry,
    SynthesisEngine,
    SynthesisReport,
)

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
    "ProtocolArgumentCard",
    "ProtocolCritiqueCard",
    "ProtocolSynthesisEngine",
    "run_deliberation",
    "ArgumentCard",
    "AxisSpec",
    "CritiqueCard",
    "ScoreboardEntry",
    "SynthesisEngine",
    "SynthesisReport",
]
