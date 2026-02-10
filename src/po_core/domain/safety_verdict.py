"""
SafetyVerdict - Gateの判定結果。

This is what the safety/wethics_gate/ module OUTPUTS.
It represents the judgment of the safety gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Mapping


class Decision(str, Enum):
    """Safety gate decision types."""

    ALLOW = "allow"
    REJECT = "reject"
    REVISE = "revise"  # 要修正（修正案は"生成しない"。要求だけ返す）


@dataclass(frozen=True)
class SafetyVerdict:
    """
    Gateの判定結果。

    Attributes:
        decision: The judgment (ALLOW, REJECT, REVISE)
        rule_ids: List of triggered rule identifiers
        reasons: Human-readable reasons
        required_changes: Required changes for REVISE decision
        meta: Additional metadata
    """

    decision: Decision
    rule_ids: List[str] = field(default_factory=list)  # 発火したルール識別子
    reasons: List[str] = field(default_factory=list)  # 人間が読める理由
    required_changes: List[str] = field(default_factory=list)  # revise時の要求
    meta: Mapping[str, str] = field(default_factory=dict)

    @staticmethod
    def fail_closed(error: Exception) -> "SafetyVerdict":
        """
        Create a fail-closed verdict when the gate encounters an error.

        重要：ゲートが壊れたら"拒否"する（fail-closed）
        """
        return SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=["gate_exception"],
            reasons=[f"wethics_gate exception: {type(error).__name__}"],
            required_changes=[],
            meta={},
        )

    @staticmethod
    def allow(rule_ids: List[str] | None = None) -> "SafetyVerdict":
        """Create an ALLOW verdict."""
        return SafetyVerdict(
            decision=Decision.ALLOW,
            rule_ids=rule_ids or [],
            reasons=[],
        )

    @staticmethod
    def reject(rule_ids: List[str], reasons: List[str]) -> "SafetyVerdict":
        """Create a REJECT verdict."""
        return SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=rule_ids,
            reasons=reasons,
        )

    @staticmethod
    def revise(
        rule_ids: List[str],
        reasons: List[str],
        required_changes: List[str],
    ) -> "SafetyVerdict":
        """Create a REVISE verdict."""
        return SafetyVerdict(
            decision=Decision.REVISE,
            rule_ids=rule_ids,
            reasons=reasons,
            required_changes=required_changes,
        )

    @property
    def is_allowed(self) -> bool:
        """Check if the decision is ALLOW."""
        return self.decision == Decision.ALLOW

    @property
    def is_rejected(self) -> bool:
        """Check if the decision is REJECT."""
        return self.decision == Decision.REJECT

    @property
    def needs_revision(self) -> bool:
        """Check if the decision is REVISE."""
        return self.decision == Decision.REVISE

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "decision": self.decision.value,
            "rule_ids": list(self.rule_ids),
            "reasons": list(self.reasons),
            "required_changes": list(self.required_changes),
            "meta": dict(self.meta),
        }


# ── Backward compatibility types (for legacy code) ──────────────────


class VerdictType(str, Enum):
    """Legacy verdict type enum (backward compat with action_gate.py)."""

    ALLOW = "allow"
    ALLOW_WITH_REPAIR = "allow_with_repair"
    REJECT = "reject"
    ESCALATE = "escalate"


@dataclass
class ViolationInfo:
    """
    Legacy violation info (backward compat with intention_gate.py).

    Used by the existing gate implementations.
    """

    code: str
    severity: float
    description: str
    repairable: bool = True


__all__ = ["SafetyVerdict", "Decision", "VerdictType", "ViolationInfo"]
