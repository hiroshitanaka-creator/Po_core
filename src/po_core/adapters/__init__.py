"""
Po_core Adapters
================

Concrete implementations of port interfaces.

Adapters connect the abstract ports to real implementations:
- memory_poself.py: Wraps Po_self as a MemoryPort

DEPENDENCY RULES:
- adapters/ can import from: ports/, domain/, and external systems
- adapters/ is the ONLY place that can import concrete external modules
- Core modules (philosophers/, tensors/, safety/) must NOT import from adapters/

Usage:
    # Only in runtime/wiring.py:
    from po_core.adapters import PoSelfMemoryAdapter
    memory = PoSelfMemoryAdapter()
"""

from po_core.adapters.memory_poself import PoSelfMemoryAdapter

__all__ = [
    "PoSelfMemoryAdapter",
]
