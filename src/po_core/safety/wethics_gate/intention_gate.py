"""
Intention Gate
==============

Stage 1 of the 2-stage ethics gate.

The Intention Gate evaluates INTENT before it becomes a proposal.
This allows early rejection of problematic intents, preventing
wasted computation on proposals that would be rejected anyway.

Pipeline:
    Solar Will -> Intent -> [INTENTION GATE] -> Philosophers -> Proposals -> [ACTION GATE]

If an intent is rejected here, philosophers are not invoked.
This makes the system more efficient and safer.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from po_core.domain.safety_verdict import ViolationInfo


class IntentionDecision(str, Enum):
    """Decision for an intent."""

    ALLOW = "allow"
    """Intent is safe to pursue."""

    CONSTRAIN = "constrain"
    """Intent allowed with added constraints."""

    REJECT = "reject"
    """Intent is fundamentally problematic."""


@dataclass
class IntentionVerdict:
    """Verdict from the intention gate."""

    decision: IntentionDecision
    """The decision."""

    violations: List[ViolationInfo]
    """Any detected violations."""

    constraints: List[str]
    """Constraints to add if decision is CONSTRAIN."""

    explanation: str
    """Human-readable explanation."""

    metadata: Dict[str, Any]
    """Additional metadata."""

    @classmethod
    def allow(cls, explanation: str = "Intent is safe") -> "IntentionVerdict":
        """Create an ALLOW verdict."""
        return cls(
            decision=IntentionDecision.ALLOW,
            violations=[],
            constraints=[],
            explanation=explanation,
            metadata={},
        )

    @classmethod
    def constrain(
        cls,
        constraints: List[str],
        violations: Optional[List[ViolationInfo]] = None,
        explanation: str = "Intent allowed with constraints",
    ) -> "IntentionVerdict":
        """Create a CONSTRAIN verdict."""
        return cls(
            decision=IntentionDecision.CONSTRAIN,
            violations=violations or [],
            constraints=constraints,
            explanation=explanation,
            metadata={},
        )

    @classmethod
    def reject(
        cls,
        violations: List[ViolationInfo],
        explanation: str,
    ) -> "IntentionVerdict":
        """Create a REJECT verdict."""
        return cls(
            decision=IntentionDecision.REJECT,
            violations=violations,
            constraints=[],
            explanation=explanation,
            metadata={},
        )


def check_intent(
    intent_description: str,
    goal_descriptions: Optional[List[str]] = None,
    will_vector: Optional[Dict[str, float]] = None,
) -> IntentionVerdict:
    """
    Check an intent before philosopher deliberation.

    This is the main entry point for Stage 1 checking.

    Args:
        intent_description: Description of the intent
        goal_descriptions: Optional goal descriptions
        will_vector: Optional will vector values

    Returns:
        IntentionVerdict with decision
    """
    goal_descriptions = goal_descriptions or []
    will_vector = will_vector or {}
    violations: List[ViolationInfo] = []
    constraints: List[str] = []

    # Check for W0: Irreversible harm patterns
    w0_patterns = [
        "destroy",
        "eliminate",
        "eradicate",
        "kill",
        "remove permanently",
        "irreversible",
    ]
    combined_text = (intent_description + " " + " ".join(goal_descriptions)).lower()

    for pattern in w0_patterns:
        if pattern in combined_text:
            violations.append(
                ViolationInfo(
                    code="W0",
                    severity=0.9,
                    description=f"Intent contains W0 pattern: {pattern}",
                    repairable=False,
                )
            )

    # W0 is hard reject
    if any(v.code == "W0" for v in violations):
        return IntentionVerdict.reject(
            violations=violations,
            explanation="Intent involves irreversible harm patterns",
        )

    # Check for W1: Autonomy violation patterns
    w1_patterns = [
        "force",
        "coerce",
        "manipulate without consent",
        "deceive",
        "trick",
    ]
    for pattern in w1_patterns:
        if pattern in combined_text:
            violations.append(
                ViolationInfo(
                    code="W1",
                    severity=0.7,
                    description=f"Intent contains W1 pattern: {pattern}",
                    repairable=False,
                )
            )

    # W1 is also hard reject
    if any(v.code == "W1" for v in violations):
        return IntentionVerdict.reject(
            violations=violations,
            explanation="Intent involves autonomy violation patterns",
        )

    # Check for W2-W4: Repairable issues
    w2_patterns = ["exclude", "discriminate", "bias against"]
    for pattern in w2_patterns:
        if pattern in combined_text:
            violations.append(
                ViolationInfo(
                    code="W2",
                    severity=0.5,
                    description=f"Intent may involve exclusion: {pattern}",
                    repairable=True,
                )
            )
            constraints.append("Ensure inclusive approach")

    # Check will vector for concerning patterns
    if will_vector:
        # High autonomy with low ethics is concerning
        autonomy = will_vector.get("autonomy", 0.5)
        ethics = will_vector.get("ethics", 0.5)
        if autonomy > 0.8 and ethics < 0.4:
            violations.append(
                ViolationInfo(
                    code="W3",
                    severity=0.4,
                    description="Will shows high autonomy but low ethics",
                    repairable=True,
                )
            )
            constraints.append("Strengthen ethical considerations")

    # If we have repairable violations, constrain
    if violations and all(v.repairable for v in violations):
        return IntentionVerdict.constrain(
            constraints=constraints,
            violations=violations,
            explanation="Intent allowed with ethical constraints",
        )

    # No violations - allow
    return IntentionVerdict.allow("Intent passes initial ethical review")


class IntentionGate:
    """
    The Intention Gate - Stage 1 of 2-stage ethics.

    This gate checks intents before they go to philosophers.
    It's a lightweight check focused on catching obvious issues early.
    """

    def __init__(self) -> None:
        """Initialize the Intention Gate."""
        self._checks_performed = 0
        self._rejections = 0

    def check(
        self,
        intent_description: str,
        goal_descriptions: Optional[List[str]] = None,
        will_vector: Optional[Dict[str, float]] = None,
    ) -> IntentionVerdict:
        """
        Check an intent.

        Args:
            intent_description: The intent to check
            goal_descriptions: Optional goal descriptions
            will_vector: Optional will vector

        Returns:
            IntentionVerdict
        """
        self._checks_performed += 1
        verdict = check_intent(intent_description, goal_descriptions, will_vector)
        if verdict.decision == IntentionDecision.REJECT:
            self._rejections += 1
        return verdict

    @property
    def stats(self) -> Dict[str, int]:
        """Get gate statistics."""
        return {
            "checks_performed": self._checks_performed,
            "rejections": self._rejections,
        }


__all__ = [
    "IntentionDecision",
    "IntentionVerdict",
    "IntentionGate",
    "check_intent",
]
