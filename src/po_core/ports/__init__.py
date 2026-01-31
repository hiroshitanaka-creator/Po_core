"""
Po_core Ports
=============

Abstract interfaces (ports) for external dependencies.

Ports define WHAT the system needs, not HOW it's provided.
Concrete implementations go in adapters/.

This follows the Hexagonal Architecture / Ports & Adapters pattern:
- Ports are abstract interfaces (this module)
- Adapters are concrete implementations (adapters/)

DEPENDENCY RULES:
- ports/ depends ONLY on: stdlib, domain/
- ports/ MUST NOT import from: philosophers/, tensors/, safety/, etc.

Memory Port Design (Read/Write分離):
- MemoryReadPort: philosophers/autonomy/tensors が参照するポート（読み取り専用）
- MemoryWritePort: runtime/wiring だけが使うポート（書き込み専用）

Usage:
    from po_core.ports import MemoryReadPort, MemoryWritePort

    # In runtime/wiring.py:
    class MyAdapter(MemoryReadPort, MemoryWritePort):
        ...
"""

from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryRecord, MemoryWritePort

__all__ = [
    # Read port (for philosophers/autonomy/tensors)
    "MemoryReadPort",
    # Write port (for runtime/wiring only)
    "MemoryWritePort",
    "MemoryRecord",
]
