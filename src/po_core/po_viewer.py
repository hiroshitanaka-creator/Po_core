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

Phase 3 — WebUI integration::

    viewer = PoViewer.from_run("What is justice?")
    viewer.serve()  # Opens browser dashboard on localhost:8050
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.decision_report_md import render_markdown
from po_core.viewer.philosopher_view import (
    extract_battalion_info,
    extract_philosopher_data,
    render_philosopher_markdown,
    render_philosopher_text,
)
from po_core.viewer.pipeline_view import render_pipeline_markdown, render_pipeline_text
from po_core.viewer.tensor_view import (
    extract_tensor_values,
    render_tensor_markdown,
    render_tensor_text,
)


class PoViewer:
    """
    High-level viewer for run_turn pipeline trace events.

    Combines pipeline progression, tensor metrics, decision report,
    and A/B comparison into a single unified view.
    """

    def __init__(self, events: Sequence[TraceEvent]) -> None:
        self._events = list(events)

    @staticmethod
    def from_run(user_input: str) -> "PoViewer":
        """
        Run the pipeline and create a PoViewer from the trace.

        Convenience method for Phase 3 observability:
            viewer = PoViewer.from_run("What is justice?")
            print(viewer.markdown())

        Args:
            user_input: The prompt to run through the pipeline.

        Returns:
            PoViewer populated with trace events from the run.
        """
        import uuid

        from po_core.domain.context import Context
        from po_core.ensemble import EnsembleDeps, run_turn
        from po_core.runtime.settings import Settings
        from po_core.runtime.wiring import build_test_system
        from po_core.trace.in_memory import InMemoryTracer

        settings = Settings()
        system = build_test_system(settings=settings)
        tracer = InMemoryTracer()

        ctx = Context.now(
            request_id=str(uuid.uuid4()),
            user_input=user_input,
            meta={"entry": "po_viewer.from_run"},
        )

        deps = EnsembleDeps(
            memory_read=system.memory_read,
            memory_write=system.memory_write,
            tracer=tracer,
            tensors=system.tensor_engine,
            solarwill=system.solarwill,
            gate=system.gate,
            philosophers=system.philosophers,
            aggregator=system.aggregator,
            aggregator_shadow=system.aggregator_shadow,
            registry=system.registry,
            settings=system.settings,
            shadow_guard=system.shadow_guard,
            deliberation_engine=getattr(system, "deliberation_engine", None),
        )

        run_turn(ctx, deps)
        return PoViewer(tracer.events)

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

        # Philosopher participation
        parts.append(render_philosopher_markdown(self._events))

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

    def philosopher_text(self) -> str:
        """Plain-text philosopher participation view."""
        return render_philosopher_text(self._events)

    def philosopher_data(self) -> List[Dict[str, Any]]:
        """Extract per-philosopher participation data."""
        return extract_philosopher_data(self._events)

    def battalion_info(self) -> Dict[str, Any]:
        """Extract battalion (selection) information."""
        return extract_battalion_info(self._events)

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
            "philosophers": self.philosopher_data(),
            "battalion": self.battalion_info(),
            "summary": self.summary(),
        }

    def serve(
        self,
        explanation: Optional["ExplanationChain"] = None,
        port: int = 8050,
        debug: bool = False,
    ) -> None:
        """
        Launch the Viewer WebUI dashboard in the browser.

        Args:
            explanation: Optional ExplanationChain for W_Ethics tab.
            port: HTTP port to serve on.
            debug: Enable Dash debug mode.
        """
        from po_core.viewer.web import create_app

        app = create_app(
            events=self._events,
            explanation=explanation,
            debug=debug,
        )
        app.run(port=port, debug=debug)


# Lazy import for type hint
ExplanationChain = Any

__all__ = ["PoViewer"]
