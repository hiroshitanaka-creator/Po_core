"""
Po_trace: Reasoning Audit Log Module

Complete tracking and logging of the philosophical reasoning process.

The legacy ``ReasoningTracer`` class was removed in v0.3.
Use ``InMemoryTracer`` (via ``PoSelf.get_trace()``) or the
``TraceEvent`` schema for all tracing needs.
"""

from po_core.trace.annotator import PhilosophicalAnnotator

__all__ = [
    "PhilosophicalAnnotator",
]
