"""
Po_core Tensors

Mathematical tensor structures for philosophical concepts.
"""

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
    "Tensor",
    "FreedomPressureTensor",
    "SemanticProfile",
    "BlockedTensor",
    "ConceptQuantifier",
    "PhilosophicalConcept",
    "InteractionTensor",
    "PhilosopherInteraction",
]
