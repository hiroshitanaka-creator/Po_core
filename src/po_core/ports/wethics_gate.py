from __future__ import annotations

from typing import Protocol

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot


class WethicsGatePort(Protocol):
    def judge_intent(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> SafetyVerdict: ...

    def judge_action(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> SafetyVerdict: ...
