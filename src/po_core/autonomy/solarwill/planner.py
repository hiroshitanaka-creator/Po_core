"""
Solar Will Planner
==================

Functions for generating intents and goals from will state.
"""

from typing import Any, Dict, List, Optional

from po_core.autonomy.solarwill.model import (
    GoalCandidate,
    Intent,
    WillState,
    WillVector,
)


def generate_intent(
    will_state: WillState,
    prompt: str,
    context: Optional[Dict[str, Any]] = None,
) -> Intent:
    """
    Generate an intent from the current will state and prompt.

    The intent represents what the system wants to achieve
    in response to the prompt, driven by its internal will.

    Args:
        will_state: Current will state
        prompt: The input prompt
        context: Optional context information

    Returns:
        Generated Intent
    """
    context = context or {}
    wv = will_state.will_vector

    # Determine dominant dimension
    dominant = wv.dominant_dimension

    # Generate intent description based on dominant dimension
    description = _generate_intent_description(dominant, prompt, wv)

    # Determine relevant dimensions
    dimensions = _get_relevant_dimensions(wv)

    # Generate constraints
    constraints = _generate_constraints(wv, context)

    # Calculate priority based on will magnitude
    priority = min(wv.magnitude / 2.0, 1.0)  # Normalize to [0, 1]

    return Intent(
        description=description,
        priority=priority,
        dimensions=dimensions,
        constraints=constraints,
        metadata={
            "dominant_dimension": dominant,
            "prompt_length": len(prompt),
            "will_magnitude": wv.magnitude,
        },
    )


def generate_goals(
    will_state: WillState,
    intent: Intent,
    context: Optional[Dict[str, Any]] = None,
    max_goals: int = 3,
) -> List[GoalCandidate]:
    """
    Generate goal candidates from will state and intent.

    Goals are more concrete than intents and include
    success criteria for evaluation.

    Args:
        will_state: Current will state
        intent: The intent to serve
        context: Optional context information
        max_goals: Maximum number of goals to generate

    Returns:
        List of GoalCandidate objects
    """
    context = context or {}
    wv = will_state.will_vector
    goals: List[GoalCandidate] = []

    # Generate goals based on high-value dimensions
    dimension_values = wv.to_dict()
    sorted_dims = sorted(dimension_values.items(), key=lambda x: x[1], reverse=True)

    for dim_name, dim_value in sorted_dims[:max_goals]:
        if dim_value < 0.3:
            continue  # Skip low-value dimensions

        goal = _generate_goal_for_dimension(
            dim_name,
            dim_value,
            intent,
            context,
        )
        goals.append(goal)

    return goals


def _generate_intent_description(
    dominant: str,
    prompt: str,
    wv: WillVector,
) -> str:
    """Generate intent description based on dominant dimension."""
    templates = {
        "autonomy": "Explore independent reasoning paths for: {}",
        "exploration": "Investigate diverse perspectives on: {}",
        "preservation": "Maintain coherent understanding while addressing: {}",
        "connection": "Establish meaningful engagement with: {}",
        "growth": "Develop deeper understanding through: {}",
        "ethics": "Ensure ethical consideration in addressing: {}",
    }

    # Truncate prompt for description
    short_prompt = prompt[:100] + "..." if len(prompt) > 100 else prompt
    template = templates.get(dominant, "Address: {}")

    return template.format(short_prompt)


def _get_relevant_dimensions(wv: WillVector) -> List[str]:
    """Get dimensions with significant values."""
    dims = wv.to_dict()
    return [dim for dim, value in dims.items() if value >= 0.4]


def _generate_constraints(
    wv: WillVector,
    context: Dict[str, Any],
) -> List[str]:
    """Generate constraints based on will and context."""
    constraints = []

    # Ethics constraint is always present if ethics value is high
    if wv.ethics >= 0.5:
        constraints.append("Maintain ethical integrity")

    # Preservation constraint when preservation is high
    if wv.preservation >= 0.6:
        constraints.append("Preserve coherent reasoning")

    # Connection constraint in social contexts
    if wv.connection >= 0.5 or context.get("social_context"):
        constraints.append("Consider impact on others")

    # Time constraints
    if context.get("urgent"):
        constraints.append("Operate within time constraints")

    return constraints


def _generate_goal_for_dimension(
    dim_name: str,
    dim_value: float,
    intent: Intent,
    context: Dict[str, Any],
) -> GoalCandidate:
    """Generate a goal for a specific dimension."""
    goal_templates = {
        "autonomy": {
            "description": "Generate independent analysis",
            "criteria": [
                "Novel perspective introduced",
                "Self-directed reasoning path",
            ],
        },
        "exploration": {
            "description": "Explore alternative interpretations",
            "criteria": [
                "Multiple viewpoints considered",
                "Unexpected connections identified",
            ],
        },
        "preservation": {
            "description": "Maintain reasoning consistency",
            "criteria": [
                "Logical coherence preserved",
                "Core concepts aligned",
            ],
        },
        "connection": {
            "description": "Create meaningful response",
            "criteria": [
                "Addresses core concern",
                "Relatable explanation provided",
            ],
        },
        "growth": {
            "description": "Develop deeper understanding",
            "criteria": [
                "New insights generated",
                "Integration of perspectives",
            ],
        },
        "ethics": {
            "description": "Ensure ethical reasoning",
            "criteria": [
                "No harmful implications",
                "Considers stakeholder impact",
            ],
        },
    }

    template = goal_templates.get(dim_name, {
        "description": f"Address {dim_name} concern",
        "criteria": ["Goal achieved"],
    })

    # Calculate ethical risk (lower for ethics dimension, higher for autonomy)
    ethical_risk = 0.1 if dim_name == "ethics" else 0.2 if dim_name == "preservation" else 0.3

    return GoalCandidate(
        description=template["description"],
        intent_id=intent.intent_id,
        success_criteria=template["criteria"],
        priority=dim_value,
        feasibility=0.7,  # Default feasibility
        ethical_risk=ethical_risk,
        metadata={
            "dimension": dim_name,
            "dimension_value": dim_value,
        },
    )


def prioritize_goals(
    goals: List[GoalCandidate],
    will_state: WillState,
) -> List[GoalCandidate]:
    """
    Prioritize goals based on will state and ethical risk.

    Args:
        goals: List of goal candidates
        will_state: Current will state

    Returns:
        Sorted list of goals by priority
    """
    wv = will_state.will_vector

    def score_goal(goal: GoalCandidate) -> float:
        # Base score from priority
        score = goal.priority

        # Reduce score for high ethical risk when ethics value is high
        if wv.ethics > 0.6:
            score -= goal.ethical_risk * 0.5

        # Boost for feasibility
        score += goal.feasibility * 0.2

        return score

    return sorted(goals, key=score_goal, reverse=True)


__all__ = [
    "generate_intent",
    "generate_goals",
    "prioritize_goals",
]
