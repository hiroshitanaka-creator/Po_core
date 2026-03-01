"""Public exports for deliberation package."""

from po_core.deliberation.clustering import ClusterResult, PositionClusterer
from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.engine import (
    DeliberationEngine,
    DeliberationResult,
    RoundTrace,
)
from po_core.deliberation.influence import InfluenceTracker, InfluenceWeight
from po_core.deliberation.protocol import ArgumentCard as ProtocolArgumentCard
from po_core.deliberation.protocol import CritiqueCard as ProtocolCritiqueCard
from po_core.deliberation.protocol import SynthesisEngine as ProtocolSynthesisEngine
from po_core.deliberation.protocol import (
    run_deliberation,
)
from po_core.deliberation.roles import (
    DEFAULT_ROLES,
    PHILOSOPHER_ROLE_MAP,
    SYNTHESIZER_PHILOSOPHERS,
    DebateRole,
    Role,
    RoleCoverage,
    assign_role,
    get_role_prompt_prefix,
    parse_roles_csv,
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
    "Role",
    "RoleCoverage",
    "DEFAULT_ROLES",
    "PHILOSOPHER_ROLE_MAP",
    "SYNTHESIZER_PHILOSOPHERS",
    "assign_role",
    "get_role_prompt_prefix",
    "ProtocolArgumentCard",
    "ProtocolCritiqueCard",
    "ProtocolSynthesisEngine",
    "parse_roles_csv",
    "ArgumentCard",
    "CritiqueCard",
    "SynthesisEngine",
    "run_deliberation",
    "AxisSpec",
    "ScoreboardEntry",
    "SynthesisReport",
]
