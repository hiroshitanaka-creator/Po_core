"""
MemoryReadPort - Memory読み取り専用インターフェース。

philosophers/autonomy/tensors が触るのはこれだけ。
直接memoryを操作することは型で禁止する。
"""

from __future__ import annotations

from typing import Protocol

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot


class MemoryReadPort(Protocol):
    """
    Read-only memory access protocol.

    philosophers/autonomy/tensors はこのポートだけを受け取る。
    書き込み操作は MemoryWritePort で分離。

    Usage:
        def process(ctx: Context, memory: MemoryReadPort) -> Proposal:
            snapshot = memory.snapshot(ctx)
            # Only read access available
            return create_proposal(snapshot)
    """

    def snapshot(self, ctx: Context) -> MemorySnapshot:
        """
        Get a read-only snapshot of memory state.

        Args:
            ctx: Current execution context

        Returns:
            Immutable MemorySnapshot (philosophers/autonomy/tensors はこれだけを見る)
        """
        ...


__all__ = ["MemoryReadPort"]
