"""
PoViewer — High-level viewer for run_turn pipeline results.

Consumes TraceEvents from InMemoryTracer and produces reports
in Markdown, plain text, or dict format.

Usage::

    from po_core.po_self import PoSelf
    from po_core.po_viewer import PoViewer

    po = PoSelf()
    response = po.generate("What is truth?")
    tracer = po.get_trace()

    viewer = PoViewer(tracer.events)
    print(viewer.markdown())   # Full Markdown report
    print(viewer.summary())    # One-line summary
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.decision_report_md import render_markdown
from po_core.viewer.pipeline_view import render_pipeline_markdown, render_pipeline_text
from po_core.viewer.tensor_view import (
    render_tensor_markdown,
    render_tensor_text,
    extract_tensor_values,
)


class PoViewer:
    """
    High-level viewer for run_turn pipeline trace events.

    Combines pipeline progression, tensor metrics, decision report,
    and A/B comparison into a single unified view.
    """

    def __init__(self, events: Sequence[TraceEvent]) -> None:
        self._events = list(events)

    @property
    def events(self) -> List[TraceEvent]:
        return list(self._events)

    @property
    def event_types(self) -> List[str]:
        """Unique event types in order of occurrence."""
        seen: dict[str, None] = {}
        for e in self._events:
            seen.setdefault(e.event_type, None)
        return list(seen)

    @property
    def request_id(self) -> str:
        if self._events:
            return self._events[0].correlation_id
        return "unknown"

    def markdown(self) -> str:
        """
        Full Markdown report combining all views.

        Returns:
            Markdown string with pipeline + tensors + decision report
        """
        parts: List[str] = []
        parts.append(f"# Po_core Run Report")
        parts.append(f"- request_id: `{self.request_id}`")
        parts.append(f"- events: {len(self._events)}")
        parts.append("")

        # Pipeline progression
        parts.append(render_pipeline_markdown(self._events))

        # Tensor metrics
        parts.append(render_tensor_markdown(self._events))

        # Full decision report (includes Pareto, A/B, etc.)
        parts.append(render_markdown(self._events))

        return "\n".join(parts)

    def pipeline_text(self) -> str:
        """Plain-text pipeline progression view."""
        return render_pipeline_text(self._events)

    def tensor_text(self) -> str:
        """Plain-text tensor metrics view."""
        return render_tensor_text(self._events)

    def tensor_values(self) -> Dict[str, float]:
        """Extract tensor metric values as dict."""
        return extract_tensor_values(self._events)

    def summary(self) -> str:
        """
        One-line summary of the pipeline run.

        Returns:
            Summary string like "ok | 12 events | 8 philosophers | fp=0.12"
        """
        n_events = len(self._events)

        # Status
        decision_events = [e for e in self._events if e.event_type == "DecisionEmitted"]
        if decision_events:
            last = decision_events[-1]
            status = "degraded" if last.payload.get("degraded") else "ok"
        else:
            blocked = any(
                e.event_type == "SafetyJudged:Intention"
                and e.payload.get("decision") != "allow"
                for e in self._events
            )
            status = "blocked" if blocked else "unknown"

        # Philosopher count
        ph_events = [e for e in self._events if e.event_type == "PhilosopherResult"]
        n_ph = len(ph_events)

        # Freedom pressure
        tensors = extract_tensor_values(self._events)
        fp = tensors.get("freedom_pressure")
        fp_str = f"fp={fp:.2f}" if fp is not None else ""

        parts = [status, f"{n_events} events", f"{n_ph} philosophers"]
        if fp_str:
            parts.append(fp_str)
        return " | ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """
        Export viewer data as a dict (for JSON serialization).

        Returns:
            Dict with pipeline_steps, tensor_values, event_types, summary
        """
        return {
            "request_id": self.request_id,
            "n_events": len(self._events),
            "event_types": self.event_types,
            "tensor_values": self.tensor_values(),
            "summary": self.summary(),
        }


__all__ = ["PoViewer"]
