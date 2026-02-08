"""
PhilosopherBridge - Legacy→Protocol Adapter
============================================

Legacy Philosopher (reason()) を PhilosopherProtocol (propose()) に変換する。

39人の哲学者は全員 Philosopher.reason(prompt, context) → Dict を持つが、
新パイプライン (run_turn) は PhilosopherProtocol.propose(ctx, intent, tensors, memory) → List[Proposal] を必要とする。

このブリッジが間を埋める:
1. reason() を呼び出し
2. 結果を normalize_response() で正規化
3. Proposal に変換して返す

DEPENDENCY RULES:
- domain, philosophers.base のみ依存
- ensemble.py や runtime は見ない
"""
from __future__ import annotations

from typing import List

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.base import (
    Philosopher,
    PhilosopherInfo,
    PhilosopherProtocol,
    normalize_response,
)


class PhilosopherBridge:
    """
    Legacy Philosopher → PhilosopherProtocol adapter.

    Wraps a legacy Philosopher instance so it conforms to PhilosopherProtocol.
    - info: PhilosopherInfo built from legacy name
    - propose(): calls legacy reason(), normalizes, converts to Proposal

    Usage:
        legacy = Aristotle()
        bridged = PhilosopherBridge(legacy)
        proposals = bridged.propose(ctx, intent, tensors, memory)
    """

    def __init__(self, legacy: Philosopher, *, version: str = "v0") -> None:
        self._legacy = legacy
        self.info = PhilosopherInfo(name=legacy.name, version=version)

    @property
    def name(self) -> str:
        """Backward compat: expose name for run_philosophers()."""
        return self._legacy.name

    def propose(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> List[Proposal]:
        """
        Call legacy reason() and convert to Proposal list.

        Mapping:
        - prompt = ctx.user_input
        - context = intent/tensors/memory summary (lightweight)
        - reason() result → normalize_response() → Proposal
        """
        # Build a lightweight context dict for the legacy interface
        legacy_context = {
            "intent": intent.goals[0] if intent.goals else "",
            "constraints": intent.constraints,
        }

        # Call legacy reason()
        raw = self._legacy.reason(ctx.user_input, legacy_context)

        # Normalize response
        normalized = normalize_response(raw, self._legacy.name, self._legacy.description)

        # Convert to Proposal
        reasoning = normalized.get("reasoning", "")
        perspective = normalized.get("perspective", "")
        tension = normalized.get("tension")

        # Build content from reasoning
        content = reasoning

        # Determine action_type based on content heuristics
        action_type = "answer"

        # Build assumption_tags from philosopher metadata
        assumption_tags = [f"perspective:{perspective}"]
        if tension:
            assumption_tags.append("has_tension")

        proposal = Proposal(
            proposal_id=f"{ctx.request_id}:{self._legacy.name}:0",
            action_type=action_type,
            content=content,
            confidence=0.5,
            assumption_tags=assumption_tags,
            risk_tags=[],
            extra={
                "philosopher": self._legacy.name,
                "perspective": perspective,
                "tension": tension,
                "normalized_response": {
                    k: v for k, v in normalized.items()
                    if k not in ("reasoning",)
                },
            },
        )

        return [proposal]


def bridge(legacy: Philosopher, *, version: str = "v0") -> PhilosopherBridge:
    """Factory function to create a PhilosopherBridge."""
    return PhilosopherBridge(legacy, version=version)


__all__ = ["PhilosopherBridge", "bridge"]
