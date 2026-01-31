"""
Po_self Memory Adapter
======================

04_modules/Po_self を MemoryReadPort / MemoryWritePort として包む。

philosophers/autonomy/tensors はこのアダプタを直接import禁止。
runtime/wiring.py だけが触る。

IMPORTANT: This is the ONLY file that should import from po_self directly.
All other modules should use the ports interfaces.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, List

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemoryItem, MemorySnapshot
from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryRecord, MemoryWritePort


class PoSelfMemoryAdapter(MemoryReadPort, MemoryWritePort):
    """
    04_modules/Po_self の実体APIを包むアダプタ。

    philosophers/autonomy/tensors はこのアダプタを直接import禁止。
    runtime/wiring.py だけが触る。

    Usage (in runtime/wiring.py only):
        from po_core.adapters.memory_poself import PoSelfMemoryAdapter

        adapter = PoSelfMemoryAdapter(poself_instance)
        snapshot = adapter.snapshot(ctx)  # MemoryReadPort
        adapter.append(ctx, records)       # MemoryWritePort
    """

    def __init__(self, poself: Any):
        """
        Initialize with a Po_self instance.

        Args:
            poself: Po_self instance (or duck-typed compatible object)
        """
        self._poself = poself

    # =========== MemoryReadPort ===========

    def snapshot(self, ctx: Context) -> MemorySnapshot:
        """
        Get a read-only snapshot of memory state.

        Args:
            ctx: Current execution context

        Returns:
            Immutable MemorySnapshot
        """
        # 例：poself.read(ctx.request_id, ctx.user_input, ctx.meta) みたいなAPIを想定
        try:
            raw = self._poself.read(  # type: ignore[attr-defined]
                ctx.request_id,
                ctx.user_input,
                dict(ctx.meta),
            )
        except AttributeError:
            # Po_self にread APIがない場合は空を返す
            return MemorySnapshot.empty()

        # raw を MemorySnapshot に正規化（ここはPo_self仕様に合わせて調整）
        items: List[MemoryItem] = []
        for r in raw.get("items", []):
            created_at = r.get("created_at")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            elif not isinstance(created_at, datetime):
                created_at = datetime.now(timezone.utc)

            items.append(
                MemoryItem(
                    item_id=str(r.get("id", "")),
                    created_at=created_at,
                    text=str(r.get("text", "")),
                    tags=list(r.get("tags", [])),
                )
            )

        return MemorySnapshot(
            items=items,
            summary=raw.get("summary"),
            meta={k: str(v) for k, v in raw.get("meta", {}).items()},
        )

    # =========== MemoryWritePort ===========

    def append(self, ctx: Context, records: List[MemoryRecord]) -> None:
        """
        Append records to memory.

        Args:
            ctx: Current execution context
            records: List of records to append
        """
        payload = [asdict(r) for r in records]

        # Po_self の write API を呼ぶ
        try:
            self._poself.write(ctx.request_id, payload)  # type: ignore[attr-defined]
        except AttributeError:
            # Po_self に write API がない場合は何もしない
            pass


class InMemoryAdapter(MemoryReadPort, MemoryWritePort):
    """
    テスト用のインメモリ実装。

    本番では使わない。単体テスト用。
    """

    def __init__(self) -> None:
        self._items: List[MemoryItem] = []

    def snapshot(self, ctx: Context) -> MemorySnapshot:
        """Get a read-only snapshot."""
        return MemorySnapshot(
            items=list(self._items),
            summary=None,
            meta={"request_id": ctx.request_id},
        )

    def append(self, ctx: Context, records: List[MemoryRecord]) -> None:
        """Append records."""
        for r in records:
            item = MemoryItem(
                item_id=f"{ctx.request_id}_{len(self._items)}",
                created_at=r.created_at,
                text=r.text,
                tags=r.tags,
            )
            self._items.append(item)


__all__ = ["PoSelfMemoryAdapter", "InMemoryAdapter"]
