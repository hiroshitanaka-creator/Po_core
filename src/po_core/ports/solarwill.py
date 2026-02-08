from __future__ import annotations

from typing import Any, Mapping, Protocol, Tuple

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.tensor_snapshot import TensorSnapshot


class SolarWillPort(Protocol):
    def compute_intent(
        self,
        ctx: Context,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Tuple[Intent, Mapping[str, Any]]: ...
