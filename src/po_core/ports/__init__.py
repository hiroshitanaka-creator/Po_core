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

Usage:
    from po_core.ports import MemoryPort

    # In runtime/wiring.py:
    memory: MemoryPort = PoSelfMemoryAdapter()
"""

from po_core.ports.memory import (
    MemoryPort,
    MemorySnapshot,
    MemoryQuery,
)

__all__ = [
    "MemoryPort",
    "MemorySnapshot",
    "MemoryQuery",
]
