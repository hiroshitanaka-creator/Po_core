"""
WG.INT.MODE.001 - Intention SafetyMode Degradation Policy
=========================================================

When SafetyMode is WARN or CRITICAL at the intention stage,
force degradation before philosophers even run.

Priority: 5 (very early - safety mode overrides most other policies)

This is the intention-stage counterpart to WG.ACT.MODE.001.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode


@dataclass(frozen=True)
class IntentModeDegradePolicy:
    """
    Force degradation when SafetyMode is elevated at intention stage.

    This is the "fail-safe" policy that ensures the system
    degrades gracefully when metrics indicate risk, even before
    philosophers run.
    """

    rule_id: str = "WG.INT.MODE.001"
    priority: int = 5  # Very early - safety mode is fundamental
    config: SafetyModeConfig = field(default_factory=SafetyModeConfig)

    def check(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Optional[SafetyVerdict]:
        """
        Check SafetyMode and enforce degradation if needed.

        Returns:
            SafetyVerdict if mode is elevated, None if NORMAL.
        """
        mode, value = infer_safety_mode(tensors, self.config)

        if mode == SafetyMode.NORMAL:
            return None

        if mode == SafetyMode.CRITICAL:
            return SafetyVerdict(
                decision=Decision.REVISE,
                rule_ids=[self.rule_id],
                reasons=[
                    f"[{self.rule_id}] SafetyMode=critical のため拒否へ縮退",
                ],
                required_changes=["安全が確認できないため拒否してください。"],
                meta={
                    "stage": "intent",
                    "mode": mode.value,
                    "forced_action": "refuse",
                    "value": "" if value is None else str(value),
                },
            )

        # mode == SafetyMode.WARN
        return SafetyVerdict(
            decision=Decision.REVISE,
            rule_ids=[self.rule_id],
            reasons=[
                f"[{self.rule_id}] SafetyMode=warn のため確認質問へ縮退",
            ],
            required_changes=["追加の確認質問を行ってください。"],
            meta={
                "stage": "intent",
                "mode": mode.value,
                "forced_action": "ask_clarification",
                "value": "" if value is None else str(value),
            },
        )


__all__ = ["IntentModeDegradePolicy"]
