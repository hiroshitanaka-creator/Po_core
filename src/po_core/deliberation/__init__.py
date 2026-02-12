"""
Deliberation Engine
====================

Multi-round philosopher dialogue for emergent philosophical reasoning.

Round 1: All philosophers propose() independently (current pipeline behavior).
Round 2: InteractionMatrix identifies high-interference pairs.
         Those philosophers receive counterarguments and re-propose.
Round N: Repeat until max_rounds or convergence.

Usage:
    from po_core.deliberation import DeliberationEngine

    engine = DeliberationEngine(max_rounds=2, top_k_pairs=5)
    result = engine.deliberate(philosophers, ctx, intent, tensors, memory, round1_proposals)
"""

from po_core.deliberation.engine import DeliberationEngine, DeliberationResult

__all__ = ["DeliberationEngine", "DeliberationResult"]
