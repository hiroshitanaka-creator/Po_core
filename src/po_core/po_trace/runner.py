"""
Simple runner that executes a Po_self inference with tracing enabled.
"""

from __future__ import annotations

from typing import Optional

from po_core.po_self import execute_prompt
from po_core.po_trace.logger import TraceLogger
from po_core.po_trace.models import TraceSession
from po_core.utils.trace_store import TraceStore


def run_trace(
    prompt: str, *, steps: int = 3, store: Optional[TraceStore] = None
) -> TraceSession:
    """Run a traced Po_self execution for the given prompt."""

    active_store = store or TraceStore()
    logger = TraceLogger(store=active_store)
    return execute_prompt(prompt=prompt, steps=steps, trace_logger=logger)


__all__ = ["run_trace"]
