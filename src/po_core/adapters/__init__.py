"""
Po_core Adapters
================

Concrete implementations of port interfaces.

Adapters connect the abstract ports to real implementations:
- PoSelfMemoryAdapter: Wraps Po_self as MemoryReadPort / MemoryWritePort
- InMemoryAdapter: In-memory implementation for testing

DEPENDENCY RULES:
- adapters/ can import from: ports/, domain/, and external systems
- adapters/ is the ONLY place that can import concrete external modules
- Core modules (philosophers/, tensors/, safety/) must NOT import from adapters/

Usage:
    # Only in runtime/wiring.py:
    from po_core.adapters import PoSelfMemoryAdapter, InMemoryAdapter

    adapter = PoSelfMemoryAdapter(poself_instance)
    # or for testing:
    adapter = InMemoryAdapter()
"""

from po_core.adapters.memory_poself import InMemoryAdapter, PoSelfMemoryAdapter

__all__ = [
    "PoSelfMemoryAdapter",
    "InMemoryAdapter",
]
