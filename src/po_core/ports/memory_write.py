"""
MemoryWritePort - Memory書き込みインターフェース。

runtime/wiring.py だけがこれを触る。
philosophers/autonomy/tensors は直接importしてはいけない。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Protocol

from po_core.domain.context import Context


@dataclass(frozen=True)
class MemoryRecord:
    """
    Memory に書き込むレコード。

    Attributes:
        created_at: When this record was created
        kind: Type of record (e.g., "decision", "fact", "observation")
        text: Content of the record
        tags: Classification tags
    """

    created_at: datetime
    kind: str  # 例: "decision", "fact", "observation"
    text: str
    tags: List[str]

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "created_at": self.created_at.isoformat(),
            "kind": self.kind,
            "text": self.text,
            "tags": list(self.tags),
        }


class MemoryWritePort(Protocol):
    """
    Write-only memory access protocol.

    runtime/wiring.py だけがこのポートを使う。
    philosophers/autonomy/tensors はこれを受け取らない。

    Usage (in runtime/wiring.py only):
        def record_decision(ctx: Context, memory: MemoryWritePort, decision: str):
            record = MemoryRecord(
                created_at=datetime.now(timezone.utc),
                kind="decision",
                text=decision,
                tags=["final"],
            )
            memory.append(ctx, [record])
    """

    def append(self, ctx: Context, records: List[MemoryRecord]) -> None:
        """
        Append records to memory.

        Args:
            ctx: Current execution context
            records: List of records to append
        """
        ...


__all__ = ["MemoryWritePort", "MemoryRecord"]
