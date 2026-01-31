"""
MemorySnapshot - 読み取り専用。philosophers/autonomy/tensorsはこれ"だけ"を見る。

Memory items and snapshots for the memory layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Mapping, Optional


@dataclass(frozen=True)
class MemoryItem:
    """
    A single memory item.

    Attributes:
        item_id: Unique identifier for this item
        created_at: When this item was created
        text: Content of the memory item
        tags: Classification tags
    """

    item_id: str
    created_at: datetime
    text: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "item_id": self.item_id,
            "created_at": self.created_at.isoformat(),
            "text": self.text,
            "tags": list(self.tags),
        }


@dataclass(frozen=True)
class MemorySnapshot:
    """
    読み取り専用。philosophers/autonomy/tensorsはこれ"だけ"を見る。

    Attributes:
        items: List of memory items
        summary: Optional summary of the memory state
        meta: Additional metadata
    """

    items: List[MemoryItem] = field(default_factory=list)
    summary: Optional[str] = None
    meta: Mapping[str, str] = field(default_factory=dict)

    @staticmethod
    def empty() -> "MemorySnapshot":
        """Create an empty memory snapshot."""
        return MemorySnapshot(items=[], summary=None, meta={})

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result: dict = {
            "items": [item.to_dict() for item in self.items],
            "meta": dict(self.meta),
        }
        if self.summary is not None:
            result["summary"] = self.summary
        return result


__all__ = ["MemoryItem", "MemorySnapshot"]
