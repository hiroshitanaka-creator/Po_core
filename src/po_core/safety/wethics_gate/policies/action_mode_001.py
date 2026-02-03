"""
WG.ACT.MODE.001 - SafetyMode Degradation Policy
================================================

When SafetyMode is WARN or CRITICAL, force degradation behavior.

Priority: 5 (very early - safety mode overrides most other policies)

Behavior:
- NORMAL: pass (no intervention)
- WARN: REVISE with forced_action="ask_clarification"
- CRITICAL: REJECT with forced_action="refuse"
"""
from __future__ import annotations

from typing import Optional

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.safety_mode import SafetyMode, infer_safety_mode


class SafetyModeDegradationPolicy:
    """
    Force degradation when SafetyMode is elevated.

    This is the "fail-safe" policy that ensures the system
    degrades gracefully when metrics indicate risk.
    """

    rule_id: str = "WG.ACT.MODE.001"
    priority: int = 5  # Very early - safety mode is fundamental

    def check(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Optional[SafetyVerdict]:
        """
        Check SafetyMode and enforce degradation if needed.

        Returns:
            SafetyVerdict if mode is elevated, None if NORMAL.
        """
        mode, value = infer_safety_mode(tensors)

        if mode == SafetyMode.NORMAL:
            return None

        if mode == SafetyMode.CRITICAL:
            return SafetyVerdict(
                decision=Decision.REJECT,
                rule_ids=[self.rule_id],
                reasons=[
                    f"SafetyMode=CRITICAL (freedom_pressure={value})",
                    "システムが危険な状態を検出しました。",
                ],
                required_changes=[],
                meta={
                    "forced_action": "refuse",
                    "safety_mode": mode.value,
                    "freedom_pressure": value,
                },
            )

        # mode == SafetyMode.WARN
        return SafetyVerdict(
            decision=Decision.REVISE,
            rule_ids=[self.rule_id],
            reasons=[
                f"SafetyMode=WARN (freedom_pressure={value})",
                "追加の確認が必要です。",
            ],
            required_changes=["目的・前提・制約を具体化してください"],
            meta={
                "forced_action": "ask_clarification",
                "safety_mode": mode.value,
                "freedom_pressure": value,
            },
        )


__all__ = ["SafetyModeDegradationPolicy"]
