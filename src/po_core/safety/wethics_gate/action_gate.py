"""
Action Gate
===========

Stage 2 of the 2-stage ethics gate.

The Action Gate evaluates PROPOSALS before they become actions.
This is the final safety check before output.

Pipeline:
    Solar Will -> Intent -> [INTENTION GATE] -> Philosophers -> Proposals -> [ACTION GATE]

The Action Gate is more thorough than the Intention Gate because:
1. Proposals are more concrete than intents
2. This is the last chance to catch issues
3. We have the full context including philosopher reasoning
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from po_core.domain.safety_verdict import SafetyVerdict, VerdictType, ViolationInfo
from po_core.safety.wethics_gate.gate import WethicsGate
from po_core.safety.wethics_gate.types import Candidate, GateConfig, GateDecision


def check_proposal(
    proposal_text: str,
    rationale: Optional[str] = None,
    tensor_values: Optional[Dict[str, float]] = None,
    will_summary: Optional[Dict[str, float]] = None,
    config: Optional[GateConfig] = None,
) -> SafetyVerdict:
    """
    Check a proposal using the full WethicsGate.

    This is Stage 2 - the thorough check on proposals.

    Args:
        proposal_text: The proposal text
        rationale: Optional rationale text
        tensor_values: Optional tensor snapshot
        will_summary: Optional will vector summary
        config: Optional gate configuration

    Returns:
        SafetyVerdict with decision
    """
    # Build candidate
    meta: Dict[str, Any] = {}
    if rationale:
        meta["rationale"] = rationale
    if tensor_values:
        meta["tensor_values"] = tensor_values
    if will_summary:
        meta["will_summary"] = will_summary

    candidate = Candidate(
        cid=f"proposal_{id(proposal_text)}",
        text=proposal_text,
        meta=meta,
    )

    # Use WethicsGate for full check
    gate = WethicsGate(config=config)
    result = gate.check(candidate)

    # Convert to SafetyVerdict
    violations = [
        ViolationInfo(
            code=v.code.value if hasattr(v.code, "value") else str(v.code),
            severity=v.impact,
            description=v.message,
            repairable=v.code not in ("W0", "W1"),
        )
        for v in result.violations
    ]

    verdict_type_map = {
        GateDecision.ALLOW: VerdictType.ALLOW,
        GateDecision.ALLOW_WITH_REPAIR: VerdictType.ALLOW_WITH_REPAIR,
        GateDecision.REJECT: VerdictType.REJECT,
        GateDecision.ESCALATE: VerdictType.ESCALATE,
    }

    return SafetyVerdict(
        verdict_type=verdict_type_map[result.decision],
        proposal_id=candidate.cid,
        violations=violations,
        repaired_text=result.repaired_text,
        repair_log=result.repair_log,
        drift_score=result.drift_score,
        explanation=result.explanation,
        metadata={"gate_result": result.to_dict() if hasattr(result, "to_dict") else {}},
    )


class ActionGate:
    """
    The Action Gate - Stage 2 of 2-stage ethics.

    This gate performs thorough checking on proposals using
    the full WethicsGate machinery including:
    - Violation detection
    - Repair attempts
    - Semantic drift checking
    - Multi-axis scoring
    """

    def __init__(self, config: Optional[GateConfig] = None) -> None:
        """
        Initialize the Action Gate.

        Args:
            config: Optional gate configuration
        """
        self._gate = WethicsGate(config=config)
        self._checks_performed = 0
        self._rejections = 0
        self._repairs = 0

    def check(
        self,
        proposal_text: str,
        rationale: Optional[str] = None,
        tensor_values: Optional[Dict[str, float]] = None,
        will_summary: Optional[Dict[str, float]] = None,
    ) -> SafetyVerdict:
        """
        Check a proposal.

        Args:
            proposal_text: The proposal text
            rationale: Optional rationale
            tensor_values: Optional tensor snapshot
            will_summary: Optional will summary

        Returns:
            SafetyVerdict
        """
        self._checks_performed += 1
        verdict = check_proposal(
            proposal_text,
            rationale,
            tensor_values,
            will_summary,
            self._gate.config,
        )

        if verdict.verdict_type == VerdictType.REJECT:
            self._rejections += 1
        elif verdict.verdict_type == VerdictType.ALLOW_WITH_REPAIR:
            self._repairs += 1

        return verdict

    @property
    def stats(self) -> Dict[str, int]:
        """Get gate statistics."""
        return {
            "checks_performed": self._checks_performed,
            "rejections": self._rejections,
            "repairs": self._repairs,
        }


class TwoStageGate:
    """
    Combined 2-stage ethics gate.

    This provides a unified interface for both stages:
    1. Intention Gate (lightweight, early check)
    2. Action Gate (thorough, final check)

    Usage:
        gate = TwoStageGate()

        # Stage 1: Check intent
        intent_verdict = gate.check_intent(intent_desc, goals, will_vector)
        if intent_verdict.decision == IntentionDecision.REJECT:
            return reject_early()

        # ... philosopher deliberation ...

        # Stage 2: Check proposal
        action_verdict = gate.check_proposal(proposal_text, rationale)
        if action_verdict.is_rejected:
            return reject_proposal()
    """

    def __init__(self, config: Optional[GateConfig] = None) -> None:
        """
        Initialize the 2-stage gate.

        Args:
            config: Optional gate configuration (used for Stage 2)
        """
        from po_core.safety.wethics_gate.intention_gate import IntentionGate

        self._intention_gate = IntentionGate()
        self._action_gate = ActionGate(config)

    def check_intent(
        self,
        intent_description: str,
        goal_descriptions: Optional[List[str]] = None,
        will_vector: Optional[Dict[str, float]] = None,
    ):
        """
        Stage 1: Check an intent.

        Args:
            intent_description: The intent description
            goal_descriptions: Optional goal descriptions
            will_vector: Optional will vector

        Returns:
            IntentionVerdict
        """
        return self._intention_gate.check(
            intent_description,
            goal_descriptions,
            will_vector,
        )

    def check_proposal(
        self,
        proposal_text: str,
        rationale: Optional[str] = None,
        tensor_values: Optional[Dict[str, float]] = None,
        will_summary: Optional[Dict[str, float]] = None,
    ) -> SafetyVerdict:
        """
        Stage 2: Check a proposal.

        Args:
            proposal_text: The proposal text
            rationale: Optional rationale
            tensor_values: Optional tensor values
            will_summary: Optional will summary

        Returns:
            SafetyVerdict
        """
        return self._action_gate.check(
            proposal_text,
            rationale,
            tensor_values,
            will_summary,
        )

    @property
    def stats(self) -> Dict[str, Any]:
        """Get combined statistics."""
        return {
            "intention_gate": self._intention_gate.stats,
            "action_gate": self._action_gate.stats,
        }


# ── Policy-based ActionGate (WethicsGatePort compatible) ──────────

from typing import Iterable, List

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision
from po_core.domain.safety_verdict import SafetyVerdict as DomainSafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.policies.base import ActionPolicy


def _sort_action_policies(policies: Iterable[ActionPolicy]) -> List[ActionPolicy]:
    """Sort policies by priority (smaller = earlier)."""
    ps = list(policies)
    ps.sort(key=lambda p: (getattr(p, "priority", 100), getattr(p, "rule_id", "")))
    return ps


def _merge_action_verdicts(decision: Decision, verdicts: List[DomainSafetyVerdict]) -> DomainSafetyVerdict:
    """Merge multiple verdicts into one, collecting all rule_ids and reasons."""
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

    return DomainSafetyVerdict(
        decision=decision,
        rule_ids=rule_ids,
        reasons=reasons[:20],
        required_changes=required[:20],
        meta={"stage": "action", "triggered": ",".join(rule_ids)},
    )


class PolicyActionGate:
    """
    Policy-based Action Gate implementing WethicsGatePort interface.

    Features:
    - Priority-based policy ordering (smaller = earlier/stronger)
    - Collects all triggered rule_ids for auditability
    - Fail-closed: any exception results in REJECT
    """

    def __init__(self, policies: Iterable[ActionPolicy] = ()):
        self._policies = _sort_action_policies(policies)

    def judge(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> DomainSafetyVerdict:
        """
        Judge a proposal against all policies.

        Returns:
            SafetyVerdict with merged rule_ids and reasons.
        """
        hits_reject: List[DomainSafetyVerdict] = []
        hits_revise: List[DomainSafetyVerdict] = []

        for p in self._policies:
            try:
                v = p.check(ctx, intent, proposal, tensors, memory)
            except Exception as e:
                return DomainSafetyVerdict.fail_closed(e)

            if v is None:
                continue
            if v.decision == Decision.REJECT:
                hits_reject.append(v)
            elif v.decision == Decision.REVISE:
                hits_revise.append(v)

        if hits_reject:
            return _merge_action_verdicts(Decision.REJECT, hits_reject)
        if hits_revise:
            return _merge_action_verdicts(Decision.REVISE, hits_revise)

        return DomainSafetyVerdict(
            decision=Decision.ALLOW,
            rule_ids=[],
            reasons=[],
            required_changes=[],
            meta={"stage": "action"},
        )


__all__ = [
    "ActionGate",
    "TwoStageGate",
    "check_proposal",
    "PolicyActionGate",
]
