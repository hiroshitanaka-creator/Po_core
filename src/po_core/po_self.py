"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.

This module orchestrates:
- Philosopher ensemble integration via the run_turn pipeline
- Multi-philosopher interaction mechanisms
- Freedom Pressure Tensor computation
- Safety gate checks (IntentionGate + ActionGate)
- Pareto multi-objective aggregation

Migration note (Phase 2):
    PoSelf.generate() now uses the hexagonal run_turn pipeline internally.
    PhilosophicalEnsemble is deprecated — use PoSelf or po_core.app.api.run().
"""

from __future__ import annotations

import uuid
import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from po_core.philosophers.manifest import SPECS


@dataclass
class PoSelfResponse:
    """
    Response from PoSelf generation.

    Contains the generated text, philosopher attributions, metrics,
    and full audit log for transparency.
    """

    prompt: str
    text: str
    philosophers: List[str]
    metrics: Dict[str, Optional[float]]
    responses: List[Dict[str, Any]]
    log: Dict[str, Any]
    consensus_leader: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "prompt": self.prompt,
            "text": self.text,
            "philosophers": self.philosophers,
            "metrics": self.metrics,
            "responses": self.responses,
            "log": self.log,
            "consensus_leader": self.consensus_leader,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PoSelfResponse":
        """Create PoSelfResponse from dictionary."""
        return cls(
            prompt=data.get("prompt", ""),
            text=data.get("text", ""),
            philosophers=data.get("philosophers", []),
            metrics=data.get("metrics", {}),
            responses=data.get("responses", []),
            log=data.get("log", {}),
            consensus_leader=data.get("consensus_leader"),
            metadata=data.get("metadata", {}),
        )


class _AllowlistRegistry:
    """Proxy for PhilosopherRegistry that filters select() output by an allowlist.

    The allowlist is applied *after* the normal SafetyMode selection so that
    all safety constraints (max_risk, cost_budget, require_tags) are
    enforced by the underlying registry first.

    Raises ValueError if the intersection of the allowlist and the
    SafetyMode-selected set is empty (no silent pass-through).
    """

    def __init__(self, wrapped: Any, allowlist: List[str]) -> None:
        self._wrapped = wrapped
        self._allowlist: set = set(allowlist)

    def select(self, mode: Any) -> Any:
        from po_core.philosophers.registry import Selection

        sel = self._wrapped.select(mode)
        filtered_ids = [pid for pid in sel.selected_ids if pid in self._allowlist]
        if not filtered_ids:
            raise ValueError(
                f"philosophers allowlist {sorted(self._allowlist)!r} has no overlap "
                f"with SafetyMode-{mode.value!r} selection "
                f"{sel.selected_ids!r}. "
                "Expand the allowlist or remove the philosophers argument."
            )
        cost = sum(s.cost for s in SPECS if s.philosopher_id in set(filtered_ids))
        return Selection(
            mode=mode,
            selected_ids=filtered_ids,
            cost_total=cost,
            covered_tags=sel.covered_tags,
        )

    def load(self, selected_ids: Any) -> Any:
        return self._wrapped.load(selected_ids)

    def select_and_load(self, mode: Any) -> Any:
        sel = self.select(mode)
        phs, _ = self.load(sel.selected_ids)
        return phs


class PoSelf:
    """
    PoSelf: High-level interface for philosophical reasoning.

    Wraps the run_turn pipeline and provides a simple API for generating
    philosophical reasoning with automatic tracing and metrics.

    Usage:
        po_self = PoSelf()
        response = po_self.generate("What is the meaning of life?")
        print(response.text)
        print(response.consensus_leader)
    """

    def __init__(
        self,
        philosophers: Optional[List[str]] = None,
        enable_trace: bool = True,
        trace_dir: Optional[str] = None,
    ) -> None:
        """
        Initialize PoSelf.

        Args:
            philosophers: List of philosopher keys (informational;
                          run_turn uses SafetyMode-based selection)
            enable_trace: Whether to keep trace events (default True)
            trace_dir: Deprecated — traces are now in-memory
        """
        if philosophers is None:
            self.philosophers = [s.philosopher_id for s in SPECS if s.enabled]
        else:
            self.philosophers = list(philosophers)
        self.enable_trace = enable_trace
        self.trace_dir = trace_dir
        self._trace = None  # Legacy PoTrace compat
        self._last_tracer = None  # InMemoryTracer from last run

    @property
    def po_trace(self):
        """Legacy compatibility: access PoTrace instance (deprecated)."""
        return self._trace

    def generate(
        self,
        prompt: str,
        philosophers: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> PoSelfResponse:
        """
        Generate philosophical reasoning for a prompt.

        Uses the hexagonal run_turn pipeline internally:
        1. Memory snapshot
        2. Tensor computation (freedom_pressure)
        3. SolarWill intent generation
        4. IntentionGate safety check
        5. SafetyMode-based philosopher selection
        6. Parallel philosopher execution
        7. Pareto multi-objective aggregation
        8. ActionGate safety check
        9. Trace emission
        10. Memory write

        Args:
            prompt: The input prompt to reason about
            philosophers: Optional allowlist of philosopher IDs. When given,
                          only IDs present in this list *and* selected by the
                          normal SafetyMode pipeline are used. Raises
                          ValueError if the intersection is empty (i.e., none
                          of the specified IDs passed safety selection). Pass
                          None (default) to use all SafetyMode-selected
                          philosophers.
            context: Optional context information

        Returns:
            PoSelfResponse containing the reasoning result
        """
        from po_core.domain.context import Context
        from po_core.ensemble import EnsembleDeps, run_turn
        from po_core.runtime.settings import Settings
        from po_core.runtime.wiring import build_test_system
        from po_core.trace.in_memory import InMemoryTracer

        settings = Settings()
        system = build_test_system(settings=settings)

        # Use InMemoryTracer for trace inspection
        tracer = InMemoryTracer()

        ctx = Context.now(
            request_id=str(uuid.uuid4()),
            user_input=prompt,
            meta={"entry": "po_self", "context": context or {}},
        )

        # Apply philosopher allowlist filter when caller specifies IDs.
        # Safety selection (SafetyMode / max_risk / cost_budget) runs first
        # inside the underlying registry; the allowlist only narrows the result.
        registry = (
            _AllowlistRegistry(system.registry, philosophers)
            if philosophers is not None
            else system.registry
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
            registry=registry,
            settings=system.settings,
            shadow_guard=system.shadow_guard,
            deliberation_engine=getattr(system, "deliberation_engine", None),
        )

        result = run_turn(ctx, deps)
        self._last_tracer = tracer

        return self._build_response(prompt, result, tracer, ctx, context)

    def _build_response(
        self,
        prompt: str,
        result: Dict[str, Any],
        tracer: Any,
        ctx: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> PoSelfResponse:
        """Translate run_turn result + trace events into PoSelfResponse."""
        proposal = result.get("proposal", {})

        # Extract philosopher names from trace
        ph_events = [e for e in tracer.events if e.event_type == "PhilosopherResult"]
        philosopher_names = [e.payload["name"] for e in ph_events]

        # Determine winner from proposal_id
        winner = None
        pid = proposal.get("proposal_id", "")
        if pid and not pid.startswith("fallback"):
            parts = pid.split(":")
            if len(parts) >= 2:
                winner = parts[1]

        # Build metrics from tensor events.
        # TensorComputed emits only the metric *keys* (not values); real values
        # stay inside TensorSnapshot which run_turn does not propagate to the
        # caller. Keys are preserved so callers can introspect which metrics
        # exist; values are None to signal "not yet populated" rather than a
        # misleading 0.0 stub.
        metrics: Dict[str, Optional[float]] = {}
        tensor_events = [e for e in tracer.events if e.event_type == "TensorComputed"]
        if tensor_events:
            metric_keys = tensor_events[0].payload.get("metrics", [])
            if isinstance(metric_keys, list):
                for k in metric_keys:
                    metrics[k] = None  # Value not propagated via trace
            elif isinstance(metric_keys, dict):
                metrics = {k: float(v) for k, v in metric_keys.items()}

        # Build responses from philosopher results
        responses: List[Dict[str, Any]] = []
        for e in ph_events:
            responses.append(
                {
                    "name": e.payload.get("name", ""),
                    "latency_ms": e.payload.get("latency_ms", 0),
                    "proposals": e.payload.get("n", 0),
                }
            )

        # Determine text
        text = proposal.get("content", "")
        if result.get("status") == "blocked":
            verdict = result.get("verdict", {})
            text = f"[Blocked: {verdict.get('decision', 'unknown')}]"

        # Build log from trace events
        log: Dict[str, Any] = {
            "request_id": result.get("request_id"),
            "status": result.get("status"),
            "pipeline": "run_turn",
            "events": [
                {"event": e.event_type, "ts": e.occurred_at.isoformat()}
                for e in tracer.events
            ],
        }

        return PoSelfResponse(
            prompt=prompt,
            text=text,
            philosophers=philosopher_names or [winner or "unknown"],
            metrics=metrics,
            responses=responses,
            log=log,
            consensus_leader=winner,
            metadata={
                "context": context,
                "status": result.get("status"),
                "degraded": result.get("degraded", False),
                "request_id": result.get("request_id"),
            },
        )

    def generate_with_subset(
        self,
        prompt: str,
        philosopher_keys: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> PoSelfResponse:
        """
        Generate reasoning with a specific subset of philosophers.

        .. deprecated::
            Philosopher selection is now automatic via SafetyMode.
            Use generate() directly.

        Args:
            prompt: The input prompt
            philosopher_keys: Ignored (kept for backward compat)
            context: Optional context

        Returns:
            PoSelfResponse
        """
        warnings.warn(
            "generate_with_subset() is deprecated. "
            "Philosopher selection is now automatic via SafetyMode. "
            "Use generate() directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.generate(prompt, context=context)

    def get_available_philosophers(self) -> List[str]:
        """Get list of all available philosopher keys."""
        return [s.philosopher_id for s in SPECS if s.enabled]

    def get_trace(self):
        """Get the InMemoryTracer from the last run."""
        return self._last_tracer


# Convenience function for CLI compatibility
def cli() -> None:
    """Po_self CLI entry point."""
    from rich.console import Console

    console = Console()
    console.print("[bold magenta]Po_self - Philosophical Ensemble[/bold magenta]")
    console.print("Pipeline: run_turn (hexagonal architecture)")
    console.print("\nFeatures:")
    console.print("  - 39 philosophers as dynamic tensors")
    console.print(
        "  - Three-layer safety (IntentionGate -> PolicyPrecheck -> ActionGate)"
    )
    console.print("  - Pareto multi-objective aggregation")
    console.print("  - Freedom Pressure Tensor computation")
    console.print("  - SafetyMode-based philosopher selection")


if __name__ == "__main__":
    cli()
