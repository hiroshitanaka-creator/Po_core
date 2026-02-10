from __future__ import annotations

from typing import Protocol

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.tensor_snapshot import TensorSnapshot


class TensorEnginePort(Protocol):
    def compute(self, ctx: Context, memory: MemorySnapshot) -> TensorSnapshot: ...
