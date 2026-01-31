"""
Po_core Tensors
===============

Mathematical tensor structures for philosophical concepts.

ARCHITECTURE:
- tensors/ is a PURE COMPUTATION module
- It ONLY depends on: stdlib, numpy, domain/
- It MUST NOT import from: philosophers/, safety/, ensemble.py

The primary API is through engine.py:
    from po_core.tensors.engine import compute_tensors

    snapshot = compute_tensors(prompt)
    print(snapshot.freedom_pressure)

Tensor classes are available for advanced use but the engine
provides the preferred interface.
"""

# Engine API (preferred)
from po_core.tensors.engine import (
    compute_tensors,
    compute_freedom_pressure,
    compute_semantic_delta,
    compute_blocked_tensor,
)

# Tensor classes (for advanced use)
from po_core.tensors.base import Tensor
from po_core.tensors.blocked_tensor import BlockedTensor
from po_core.tensors.concept_quantifier import (
    ConceptQuantifier,
    PhilosophicalConcept,
)
from po_core.tensors.freedom_pressure import FreedomPressureTensor
from po_core.tensors.interaction_tensor import (
    InteractionTensor,
    PhilosopherInteraction,
)
from po_core.tensors.semantic_profile import SemanticProfile

__all__ = [
    # Engine API (preferred)
    "compute_tensors",
    "compute_freedom_pressure",
    "compute_semantic_delta",
    "compute_blocked_tensor",
    # Tensor classes
    "Tensor",
    "FreedomPressureTensor",
    "SemanticProfile",
    "BlockedTensor",
    "ConceptQuantifier",
    "PhilosophicalConcept",
    "InteractionTensor",
    "PhilosopherInteraction",
]
