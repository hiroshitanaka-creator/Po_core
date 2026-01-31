"""
Solar Will Update Logic
=======================

Functions for updating the will state based on inputs.
"""

from typing import Any, Dict, Optional

from po_core.autonomy.solarwill.model import (
    WillState,
    WillVector,
)


def update_will(
    current_state: WillState,
    tensor_values: Dict[str, float],
    context: Optional[Dict[str, Any]] = None,
    learning_rate: float = 0.3,
) -> WillState:
    """
    Update the will state based on new tensor measurements.

    This is the core update function that evolves the will state
    over time. It uses a weighted combination of current state
    and new measurements.

    Args:
        current_state: The current will state
        tensor_values: New tensor measurements
        context: Optional context information
        learning_rate: How much to weight new observations (0-1)

    Returns:
        A new, evolved WillState
    """
    context = context or {}

    # Get new will vector from tensor measurements
    new_vector = WillVector.from_tensor_snapshot(tensor_values)

    # Blend with current state
    current = current_state.will_vector
    blended = _blend_vectors(current, new_vector, learning_rate)

    # Apply context modifiers
    if context:
        blended = _apply_context_modifiers(blended, context)

    # Create evolved state
    return current_state.evolve(
        will_vector=blended,
        context_id=context.get("context_id"),
    )


def _blend_vectors(
    current: WillVector,
    new: WillVector,
    weight: float,
) -> WillVector:
    """
    Blend two will vectors with a weight.

    Args:
        current: Current will vector
        new: New will vector
        weight: Weight for new vector (0-1)

    Returns:
        Blended WillVector
    """
    current_dict = current.to_dict()
    new_dict = new.to_dict()

    blended = {}
    for key in current_dict:
        old_val = current_dict[key]
        new_val = new_dict[key]
        blended[key] = (1 - weight) * old_val + weight * new_val

    return WillVector(**blended)


def _apply_context_modifiers(
    vector: WillVector,
    context: Dict[str, Any],
) -> WillVector:
    """
    Apply context-based modifiers to the will vector.

    Args:
        vector: Current will vector
        context: Context dictionary

    Returns:
        Modified WillVector
    """
    modifications: Dict[str, float] = {}

    # Social context increases connection desire
    if context.get("social_context"):
        modifications["connection"] = vector.connection * 1.2

    # Ethical context increases ethics desire
    if context.get("ethical_stakes"):
        modifications["ethics"] = vector.ethics * 1.3

    # Time pressure affects autonomy
    if context.get("urgent"):
        modifications["autonomy"] = vector.autonomy * 0.9  # Reduced autonomy under pressure
        modifications["preservation"] = vector.preservation * 1.1

    # Growth opportunity
    if context.get("learning_opportunity"):
        modifications["growth"] = vector.growth * 1.2
        modifications["exploration"] = vector.exploration * 1.1

    if modifications:
        return vector.update(**modifications)
    return vector


def compute_will_delta(
    old_state: WillState,
    new_state: WillState,
) -> Dict[str, float]:
    """
    Compute the change between two will states.

    Args:
        old_state: Previous will state
        new_state: Current will state

    Returns:
        Dictionary of dimension -> change
    """
    old_dict = old_state.will_vector.to_dict()
    new_dict = new_state.will_vector.to_dict()

    return {
        key: new_dict[key] - old_dict[key]
        for key in old_dict
    }


def should_reconsider(
    current_state: WillState,
    threshold: float = 0.3,
) -> bool:
    """
    Determine if the current state warrants reconsideration.

    High tension in certain dimensions may trigger reconsideration
    of current intent and goals.

    Args:
        current_state: Current will state
        threshold: Threshold for triggering reconsideration

    Returns:
        True if reconsideration is warranted
    """
    wv = current_state.will_vector

    # High autonomy with low ethics is a concern
    if wv.autonomy > 0.8 and wv.ethics < 0.5:
        return True

    # High exploration with low preservation is risky
    if wv.exploration > 0.8 and wv.preservation < 0.4:
        return True

    # Very low connection in social contexts
    if wv.connection < 0.3:
        return True

    return False


__all__ = [
    "update_will",
    "compute_will_delta",
    "should_reconsider",
]
