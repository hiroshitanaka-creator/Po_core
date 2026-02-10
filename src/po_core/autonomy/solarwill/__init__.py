"""
Solar Will - Autonomous Will Engine
====================================

Solar Will is the autonomous decision-making core of Po_core.
It provides the "desire" and "intent" that drives philosophical reasoning.

Components:
- model.py: WillState data model
- update.py: Will state update logic
- planner.py: Intent and goal generation
- scoring.py: Multi-objective scoring
- interfaces.py: Integration interfaces

Usage:
    from po_core.autonomy.solarwill import SolarWillEngine

    engine = SolarWillEngine()
    will_state = engine.update(tensor_snapshot)
    intent = engine.generate_intent(will_state, context)
    goals = engine.generate_goals(will_state, context)

The Solar Will engine sits BEFORE philosophers in the pipeline,
ensuring that autonomous will drives the deliberation process.
"""

from po_core.autonomy.solarwill.engine import SolarWillEngine
from po_core.autonomy.solarwill.model import (
    GoalCandidate,
    Intent,
    WillState,
    WillVector,
)
from po_core.autonomy.solarwill.planner import generate_goals, generate_intent
from po_core.autonomy.solarwill.update import update_will

__all__ = [
    # Model
    "WillState",
    "WillVector",
    "Intent",
    "GoalCandidate",
    # Functions
    "update_will",
    "generate_intent",
    "generate_goals",
    # Engine
    "SolarWillEngine",
]
