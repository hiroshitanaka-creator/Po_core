"""
Po_core Autonomy Layer
======================

This module contains the autonomous decision-making components.

The primary component is Solar Will - the system that:
1. Maintains an internal will/intent state
2. Updates this state based on tensor measurements
3. Generates goals and intents for philosopher deliberation
4. Provides the "desire" that drives the reasoning process

Architecture:
    tensors/ -> autonomy/solarwill/ -> philosophers/
                     |
                     v
                 ensemble.py

Solar Will sits BEFORE philosophers in the pipeline:
1. Context + TensorSnapshot
2. Solar Will updates WillState
3. Solar Will generates Intent/GoalCandidates
4. Philosophers deliberate given Context + TensorSnapshot + Intent
5. Proposals are aggregated
6. Safety gate judges
7. Output

This ensures that "will" drives the system, not just reactive response.
"""

from po_core.autonomy.solarwill import (
    GoalCandidate,
    Intent,
    SolarWillEngine,
    WillState,
    generate_goals,
    generate_intent,
    update_will,
)

__all__ = [
    "WillState",
    "Intent",
    "GoalCandidate",
    "update_will",
    "generate_intent",
    "generate_goals",
    "SolarWillEngine",
]
