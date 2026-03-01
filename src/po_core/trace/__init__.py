"""
Po_trace: Reasoning Audit Log Module

Complete tracking and logging of the philosophical reasoning process.

The legacy ``ReasoningTracer`` class was removed in v0.3.
Use ``InMemoryTracer`` (via ``PoSelf.get_trace()``) or the
``TraceEvent`` schema for all tracing needs.
"""

from po_core.trace.annotator import PhilosophicalAnnotator
from po_core.trace.event_log import Event, JsonlEventLogger, mask_sensitive_payload
from po_core.trace.replay import replay_run

__all__ = [
    "PhilosophicalAnnotator",
    "Event",
    "JsonlEventLogger",
    "mask_sensitive_payload",
    "replay_run",
]
