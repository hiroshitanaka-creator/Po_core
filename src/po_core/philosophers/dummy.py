"""
Dummy Philosopher
=================

Minimal philosopher for vertical slice testing.
"""

from __future__ import annotations

from typing import List

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.base import PhilosopherInfo, PhilosopherProtocol


class DummyPhilosopher(PhilosopherProtocol):
    """Minimal philosopher that produces stub proposals."""

    info = PhilosopherInfo(name="dummy", version="v0")

    def propose(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> List[Proposal]:
        """Generate a single stub proposal."""
        return [
            Proposal(
                proposal_id=f"{ctx.request_id}:dummy:0",
                action_type="answer",
                content=f"[dummy] {ctx.user_input}",
                confidence=0.1,
                assumption_tags=["stub"],
                risk_tags=[],
            )
        ]


__all__ = ["DummyPhilosopher"]
