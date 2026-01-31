from __future__ import annotations

from typing import Protocol, Sequence

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot


class AggregatorPort(Protocol):
    def aggregate(self, ctx: Context, intent: Intent, tensors: TensorSnapshot, proposals: Sequence[Proposal]) -> Proposal:
        ...
