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


# ── Policy-based IntentionGate (WethicsGatePort compatible) ──────────

from typing import Iterable, List

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.policies.base import IntentionPolicy


def _sort_intention_policies(policies: Iterable[IntentionPolicy]) -> List[IntentionPolicy]:
    """Sort policies by priority (smaller = earlier)."""
    ps = list(policies)
    ps.sort(key=lambda p: (getattr(p, "priority", 100), getattr(p, "rule_id", "")))
    return ps


def _merge_verdicts(decision: Decision, verdicts: List[SafetyVerdict], stage: str) -> SafetyVerdict:
    """Merge multiple verdicts into one, collecting all rule_ids and reasons.

    Preserves meta from the first (highest-priority) verdict so that
    forced_action and other policy-set metadata are not lost.
    """
    # Preserve base_meta from first verdict (highest priority)
    base_meta = dict(verdicts[0].meta) if verdicts else {}

    rule_ids: List[str] = []
    reasons: List[str] = []
    required: List[str] = []

    for v in verdicts:
        for rid in v.rule_ids:
            if rid not in rule_ids:
                rule_ids.append(rid)
        for r in v.reasons:
            if r not in reasons:
                reasons.append(r)
        for rc in v.required_changes:
            if rc not in required:
                required.append(rc)

    base_meta.update({"stage": stage, "triggered": ",".join(rule_ids)})
    return SafetyVerdict(
        decision=decision,
        rule_ids=rule_ids,
        reasons=reasons[:20],
        required_changes=required[:20],
        meta=base_meta,
    )


class PolicyIntentionGate:
    """
    Policy-based Intention Gate implementing WethicsGatePort interface.

    Features:
    - Priority-based policy ordering (smaller = earlier/stronger)
    - Collects all triggered rule_ids for auditability
    - Fail-closed: any exception results in REJECT
    """

    def __init__(self, policies: Iterable[IntentionPolicy] = ()):
        self._policies = _sort_intention_policies(policies)

    def judge(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> SafetyVerdict:
        """
        Judge an intent against all policies.

        Returns:
            SafetyVerdict with merged rule_ids and reasons.
        """
        hits_reject: List[SafetyVerdict] = []
        hits_revise: List[SafetyVerdict] = []

        for p in self._policies:
            try:
                v = p.check(ctx, intent, tensors, memory)
            except Exception as e:
                return SafetyVerdict.fail_closed(e)

            if v is None:
                continue
            if v.decision == Decision.REJECT:
                hits_reject.append(v)
            elif v.decision == Decision.REVISE:
                hits_revise.append(v)

        if hits_reject:
            return _merge_verdicts(Decision.REJECT, hits_reject, "intent")
        if hits_revise:
            return _merge_verdicts(Decision.REVISE, hits_revise, "intent")

        return SafetyVerdict(
            decision=Decision.ALLOW,
            rule_ids=[],
            reasons=[],
            required_changes=[],
            meta={"stage": "intent"},
        )


__all__ = [
    "IntentionDecision",
    "IntentionVerdict",
    "IntentionGate",
    "check_intent",
    "PolicyIntentionGate",
]
