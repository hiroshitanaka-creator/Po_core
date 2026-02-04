"""Deterministic ensemble runner used by CLI smoke tests."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional, TYPE_CHECKING, Any

from po_core import philosophers
from po_core.philosophers.base import Philosopher
from po_core.trace.tracer import ReasoningTracer, TraceLevel

if TYPE_CHECKING:
    from po_core.po_trace import PoTrace, EventType

# Flag to enable advanced tensor metrics (can be set via environment or config)
USE_ADVANCED_METRICS = False

DEFAULT_PHILOSOPHERS: List[str] = ["aristotle", "confucius", "wittgenstein"]


PHILOSOPHER_REGISTRY: Dict[str, type[Philosopher]] = {
    "arendt": philosophers.Arendt,
    "aristotle": philosophers.Aristotle,
    "badiou": philosophers.Badiou,
    "beauvoir": philosophers.Beauvoir,
    "butler": philosophers.Butler,
    "confucius": philosophers.Confucius,
    "deleuze": philosophers.Deleuze,
    "derrida": philosophers.Derrida,
    "descartes": philosophers.Descartes,
    "dewey": philosophers.Dewey,
    "dogen": philosophers.Dogen,
    "epicurus": philosophers.Epicurus,
    "foucault": philosophers.Foucault,
    "hegel": philosophers.Hegel,
    "heidegger": philosophers.Heidegger,
    "husserl": philosophers.Husserl,
    "jonas": philosophers.Jonas,
    "jung": philosophers.Jung,
    "kant": philosophers.Kant,
    "kierkegaard": philosophers.Kierkegaard,
    "lacan": philosophers.Lacan,
    "laozi": philosophers.Laozi,
    "levinas": philosophers.Levinas,
    "marcus_aurelius": philosophers.MarcusAurelius,
    "merleau_ponty": philosophers.MerleauPonty,
    "nagarjuna": philosophers.Nagarjuna,
    "nietzsche": philosophers.Nietzsche,
    "nishida": philosophers.Nishida,
    "parmenides": philosophers.Parmenides,
    "peirce": philosophers.Peirce,
    "plato": philosophers.Plato,
    "sartre": philosophers.Sartre,
    "schopenhauer": philosophers.Schopenhauer,
    "spinoza": philosophers.Spinoza,
    "wabi_sabi": philosophers.WabiSabi,
    "watsuji": philosophers.Watsuji,
    "weil": philosophers.Weil,
    "wittgenstein": philosophers.Wittgenstein,
    "zhuangzi": philosophers.Zhuangzi,
}


@dataclass
class PhilosopherTensor:
    """Structured view of a philosopher's contribution."""

    name: str
    reasoning: str
    perspective: str
    freedom_pressure: float
    semantic_delta: float
    blocked_tensor: float
    tension: str | None = None
    # Advanced metrics (optional, only when USE_ADVANCED_METRICS=True)
    advanced_metrics: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, object]:
        result = {
            "name": self.name,
            "reasoning": self.reasoning,
            "perspective": self.perspective,
            "tension": self.tension,
            "freedom_pressure": self.freedom_pressure,
            "semantic_delta": self.semantic_delta,
            "blocked_tensor": self.blocked_tensor,
        }
        if self.advanced_metrics:
            result["advanced_metrics"] = self.advanced_metrics
        return result


@dataclass
class EnsembleMetrics:
    """Aggregate ensemble metrics."""

    freedom_pressure: float
    semantic_delta: float
    blocked_tensor: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "freedom_pressure": self.freedom_pressure,
            "semantic_delta": self.semantic_delta,
            "blocked_tensor": self.blocked_tensor,
        }


def _tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _compute_freedom_pressure(reasoning: str) -> float:
    tokens = _tokenize(reasoning)
    if not tokens:
        return 0.35
    unique_ratio = len(set(tokens)) / len(tokens)
    return round(0.35 + 0.65 * unique_ratio, 2)


def _compute_semantic_delta(prompt: str, reasoning: str) -> float:
    prompt_tokens = set(_tokenize(prompt))
    reasoning_tokens = set(_tokenize(reasoning))
    if not prompt_tokens or not reasoning_tokens:
        return 1.0
    overlap = len(prompt_tokens & reasoning_tokens)
    coverage = overlap / len(prompt_tokens)
    return round(1 - coverage, 2)


def _compute_blocked_tensor(freedom_pressure: float, semantic_delta: float) -> float:
    return round(max(0.0, (1 - freedom_pressure) * 0.5 + semantic_delta * 0.5), 2)


def _compute_advanced_metrics(prompt: str, reasoning: str, philosopher_name: str) -> Dict[str, Any]:
    """
    Compute advanced tensor-based metrics.

    Uses the tensor_metrics module for sophisticated calculations.
    Falls back to simple metrics if tensor_metrics is unavailable.
    """
    try:
        from po_core.tensor_metrics import compute_all_metrics
        return compute_all_metrics(prompt, reasoning, philosopher_name)
    except Exception as e:
        # Fallback to simple metrics if advanced metrics fail
        print(f"Warning: Advanced metrics failed for {philosopher_name}: {e}")
        print("Falling back to simple metrics")
        freedom_pressure = _compute_freedom_pressure(reasoning)
        semantic_delta = _compute_semantic_delta(prompt, reasoning)
        blocked_tensor = _compute_blocked_tensor(freedom_pressure, semantic_delta)
        return {
            "freedom_pressure_value": freedom_pressure,
            "semantic_delta": semantic_delta,
            "blocked_tensor_value": blocked_tensor,
        }


def _load_philosophers(names: Iterable[str]) -> List[Philosopher]:
    loaded: List[Philosopher] = []
    for name in names:
        key = name.lower()
        if key not in PHILOSOPHER_REGISTRY:
            raise ValueError(f"Unknown philosopher: {name}")
        loaded.append(PHILOSOPHER_REGISTRY[key]())
    return loaded


def _aggregate_metrics(tensors: List[PhilosopherTensor]) -> EnsembleMetrics:
    if not tensors:
        return EnsembleMetrics(0.0, 0.0, 0.0)

    freedom_avg = round(sum(t.freedom_pressure for t in tensors) / len(tensors), 2)
    delta_avg = round(sum(t.semantic_delta for t in tensors) / len(tensors), 2)
    blocked_avg = round(sum(t.blocked_tensor for t in tensors) / len(tensors), 2)
    return EnsembleMetrics(freedom_avg, delta_avg, blocked_avg)


def run_ensemble(
    prompt: str,
    *,
    philosophers: Optional[Iterable[str]] = None,
    po_trace: Optional["PoTrace"] = None,
    session_id: Optional[str] = None,
    enable_tracer: bool = True,
) -> Dict:
    """
    Return a structured ensemble response for a given prompt.

    Args:
        prompt: The input prompt to reason about
        philosophers: Optional list of philosopher names to use
        po_trace: Optional PoTrace instance for persistent logging
        session_id: Session ID for PoTrace
        enable_tracer: Whether to enable ReasoningTracer (default: True)

    Returns:
        Dictionary with ensemble response
    """

    selected = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
    thinkers = _load_philosophers(selected)

    # Create ReasoningTracer with PoTrace integration
    tracer: Optional[ReasoningTracer] = None
    if enable_tracer:
        tracer = ReasoningTracer(
            prompt=prompt,
            metadata={"philosophers": selected, "session_id": session_id},
            po_trace=po_trace,
            session_id=session_id,
        )

    # Log ensemble start
    if tracer:
        tracer.log_event(
            level=TraceLevel.INFO,
            event="ensemble_started",
            message=f"Ensemble reasoning started with {len(selected)} philosophers",
            data={"philosophers_count": len(selected), "philosophers": selected},
        )
    elif po_trace and session_id:
        from po_core.po_trace import EventType

        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="ensemble",
            data={
                "message": "Ensemble reasoning started",
                "philosophers_count": len(selected),
                "philosophers": selected,
            },
        )

    tensors: List[PhilosopherTensor] = []
    for thinker in thinkers:
        reasoning_result = thinker.reason(prompt)
        reasoning_text = str(reasoning_result.get("reasoning", ""))
        perspective = str(reasoning_result.get("perspective", ""))
        tension = reasoning_result.get("tension")

        # Compute metrics (simple or advanced)
        if USE_ADVANCED_METRICS:
            advanced_metrics = _compute_advanced_metrics(prompt, reasoning_text, thinker.name)
            freedom_pressure = advanced_metrics["freedom_pressure_value"]
            semantic_delta = advanced_metrics["semantic_delta"]
            blocked_tensor = advanced_metrics["blocked_tensor_value"]
        else:
            advanced_metrics = None
            freedom_pressure = _compute_freedom_pressure(reasoning_text)
            semantic_delta = _compute_semantic_delta(prompt, reasoning_text)
            blocked_tensor = _compute_blocked_tensor(freedom_pressure, semantic_delta)

        tensor = PhilosopherTensor(
            name=thinker.name,
            reasoning=reasoning_text,
            perspective=perspective,
            tension=tension,
            freedom_pressure=freedom_pressure,
            semantic_delta=semantic_delta,
            blocked_tensor=blocked_tensor,
            advanced_metrics=advanced_metrics,
        )
        tensors.append(tensor)

        # Log philosopher reasoning via tracer
        if tracer:
            tracer.log_philosopher_reasoning(
                philosopher=thinker.name,
                reasoning={
                    "perspective": perspective,
                    "tension": tension,
                    "reasoning_length": len(reasoning_text),
                },
                metadata={
                    "freedom_pressure": freedom_pressure,
                    "semantic_delta": semantic_delta,
                    "blocked_tensor": blocked_tensor,
                },
            )

            # Log tensor computation
            tracer.log_tensor_computation(
                tensor_name=f"{thinker.name}_tensor",
                tensor_data={
                    "freedom_pressure": freedom_pressure,
                    "semantic_delta": semantic_delta,
                    "blocked_tensor": blocked_tensor,
                },
            )
        elif po_trace and session_id:
            from po_core.po_trace import EventType

            po_trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source=f"philosopher.{thinker.name}",
                data={
                    "message": f"{thinker.name} completed reasoning",
                    "philosopher": thinker.name,
                    "perspective": perspective,
                    "freedom_pressure": freedom_pressure,
                    "semantic_delta": semantic_delta,
                    "blocked_tensor": blocked_tensor,
                    "reasoning_length": len(reasoning_text),
                },
            )

    aggregate = _aggregate_metrics(tensors)
    ranked = sorted(tensors, key=lambda tensor: tensor.freedom_pressure, reverse=True)

    # Log ensemble completion
    if tracer:
        tracer.log_decision(
            decision=f"Consensus leader: {ranked[0].name}" if ranked else "No consensus",
            reasoning="Selected philosopher with highest freedom pressure",
            alternatives=[t.name for t in ranked[1:3]] if len(ranked) > 1 else [],
        )
        tracer.complete(result={"consensus_leader": ranked[0].name if ranked else None})
    elif po_trace and session_id:
        from po_core.po_trace import EventType

        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="ensemble",
            data={
                "message": "Ensemble reasoning completed",
                "results_recorded": len(tensors),
                "consensus_leader": ranked[0].name if ranked else None,
                "status": "ok" if tensors else "empty",
            },
        )

        # Update session metrics
        po_trace.update_metrics(session_id, aggregate.to_dict())

    log = {
        "prompt": prompt,
        "philosophers": selected,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "events": [
            {"event": "ensemble_started", "philosophers": len(selected)},
            {
                "event": "ensemble_completed",
                "results_recorded": len(tensors),
                "status": "ok" if tensors else "empty",
            },
        ],
    }

    # Include tracer timeline in log if available
    if tracer:
        log["trace"] = {
            "trace_id": tracer.trace_id,
            "statistics": tracer.stats,
            "timeline": tracer.get_timeline(),
        }

    consensus_text = ranked[0].reasoning if ranked else ""

    return {
        "prompt": prompt,
        "philosophers": selected,
        "responses": [tensor.to_dict() for tensor in tensors],
        "aggregate": aggregate.to_dict(),
        "consensus": {
            "leader": ranked[0].name if ranked else None,
            "text": consensus_text,
        },
        "log": log,
    }


# ── Hexagonal Architecture: run_turn (vertical slice) ──────────────────

from typing import Mapping, Sequence

from po_core.domain.context import Context as DomainContext
from po_core.domain.trace_event import TraceEvent
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.safety_verdict import Decision
from po_core.domain.keys import (
    PO_CORE, POLICY, TRACEQ, FREEDOM_PRESSURE, AUTHOR, AUTHOR_RELIABILITY, PARETO_DEBUG,
)
from po_core.ports.aggregator import AggregatorPort
from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryRecord, MemoryWritePort
from po_core.ports.solarwill import SolarWillPort
from po_core.ports.tensor_engine import TensorEnginePort
from po_core.ports.trace import TracePort
from po_core.ports.wethics_gate import WethicsGatePort
from po_core.philosophers.base import PhilosopherProtocol
from po_core.philosophers.registry import PhilosopherRegistry, LoadError
from po_core.party_machine import run_philosophers, RunResult
from po_core.runtime.settings import Settings
from po_core.safety.fallback import compose_fallback
from po_core.safety.policy_scoring import policy_score


def _author_reliability(
    *,
    timed_out: bool,
    error: Optional[str],
    latency_ms: Optional[int],
    timeout_s: float,
) -> float:
    """
    Compute author reliability from execution trace.

    Returns:
        0.0〜1.0: 高いほど信頼性が高い
    """
    if timed_out:
        return 0.0
    if error is not None:
        return 0.2
    if latency_ms is None:
        return 0.6
    t = timeout_s * 1000.0
    # 速いほど高い：0ms→1.0, timeout→0.4
    r = 1.0 - 0.6 * min(1.0, float(latency_ms) / max(1.0, t))
    return max(0.0, min(1.0, r))


@dataclass(frozen=True)
class EnsembleDeps:
    """Dependencies for run_turn (injected via wiring)."""

    memory_read: MemoryReadPort
    memory_write: MemoryWritePort
    tracer: TracePort
    tensors: TensorEnginePort
    solarwill: SolarWillPort
    gate: WethicsGatePort
    philosophers: Sequence[PhilosopherProtocol]  # Backward compat
    aggregator: AggregatorPort
    registry: PhilosopherRegistry  # SafetyMode-based selection
    settings: Settings  # Worker/timeout settings


def _get_swarm_params(mode: SafetyMode, settings: Settings) -> tuple[int, float]:
    """Get worker count and timeout based on SafetyMode."""
    if mode == SafetyMode.CRITICAL:
        return settings.philosopher_workers_critical, settings.philosopher_timeout_s_critical
    elif mode == SafetyMode.WARN:
        return settings.philosopher_workers_warn, settings.philosopher_timeout_s_warn
    else:  # NORMAL or UNKNOWN
        return settings.philosopher_workers_normal, settings.philosopher_timeout_s_normal


def run_turn(ctx: DomainContext, deps: EnsembleDeps) -> Dict[str, Any]:
    """
    Run a single turn through the full pipeline.

    Pipeline:
    1. memory_read.snapshot()
    2. tensors.compute() → TensorSnapshot
    3. solarwill.compute_intent() → Intent
    4. IntentionGate (fail-closed)
    5. registry.select_and_load() → SafetyMode-based philosopher selection
    6. run_philosophers() → parallel execution with timeout
    7. aggregator.aggregate() → Proposal
    8. ActionGate (fail-closed)
    9. trace.emit() (>=5 events)
    10. memory_write.append()

    Args:
        ctx: Request context
        deps: Injected dependencies

    Returns:
        Result dictionary with status, proposal, or verdict
    """
    tracer = deps.tracer

    # 1. Memory snapshot
    memory = deps.memory_read.snapshot(ctx)
    tracer.emit(TraceEvent.now(
        "MemorySnapshotted",
        ctx.request_id,
        {"items": len(memory.items)},
    ))

    # 2. Tensor computation
    tensors = deps.tensors.compute(ctx, memory)
    tracer.emit(TraceEvent.now(
        "TensorComputed",
        ctx.request_id,
        {"metrics": list(tensors.metrics.keys()), "version": tensors.version},
    ))

    # Determine SafetyMode from tensors
    safety_config = SafetyModeConfig(
        warn=deps.settings.freedom_pressure_warn,
        critical=deps.settings.freedom_pressure_critical,
        missing_mode=deps.settings.freedom_pressure_missing_mode,
    )
    mode, _ = infer_safety_mode(tensors, safety_config)

    # 3. SolarWill intent
    intent, will_meta = deps.solarwill.compute_intent(ctx, tensors, memory)
    tracer.emit(TraceEvent.now(
        "IntentGenerated",
        ctx.request_id,
        dict(will_meta),
    ))

    # 4. Intention Gate (Stage 1)
    v1 = deps.gate.judge_intent(ctx, intent, tensors, memory)
    tracer.emit(TraceEvent.now(
        "SafetyJudged:Intention",
        ctx.request_id,
        {"decision": v1.decision.value, "rule_ids": v1.rule_ids},
    ))
    if v1.decision != Decision.ALLOW:
        fallback = compose_fallback(ctx, v1, stage="intention")
        # Pass fallback through action gate to verify it's safe
        vfb = deps.gate.judge_action(ctx, intent, fallback, tensors, memory)
        tracer.emit(TraceEvent.now(
            "SafetyDegraded",
            ctx.request_id,
            {"from": "intention", **v1.meta},
        ))
        if vfb.decision == Decision.ALLOW:
            return {
                "request_id": ctx.request_id,
                "status": "ok",
                "degraded": True,
                "proposal": fallback.compact(),
                "verdict": v1.to_dict(),
            }
        # Fallback itself was rejected - hard block
        return {
            "request_id": ctx.request_id,
            "status": "blocked",
            "stage": "intention",
            "verdict": v1.to_dict(),
        }

    # 5. Select philosophers based on SafetyMode (編成)
    sel = deps.registry.select(mode)
    max_workers, timeout_s = _get_swarm_params(mode, deps.settings)
    tracer.emit(TraceEvent.now(
        "PhilosophersSelected",
        ctx.request_id,
        {
            "mode": mode.value,
            "n": len(sel.selected_ids),
            "cost_total": sel.cost_total,
            "covered_tags": sel.covered_tags,
            "ids": sel.selected_ids,
            "workers": max_workers,
        },
    ))

    # Load philosophers (with error recovery)
    philosophers, load_errors = deps.registry.load(sel.selected_ids)
    for e in load_errors:
        tracer.emit(TraceEvent.now(
            "PhilosopherLoadError",
            ctx.request_id,
            {"id": e.philosopher_id, "module": e.module, "symbol": e.symbol, "error": e.error},
        ))

    # 6. Parallel philosopher execution with timeout
    from po_core.domain.proposal import Proposal as DomainProposal
    raw_proposals: List[DomainProposal] = []
    ph_proposals, run_results = run_philosophers(
        philosophers, ctx, intent, tensors, memory,
        max_workers=max_workers, timeout_s=timeout_s,
    )
    raw_proposals.extend(ph_proposals)

    # Emit trace events for each result (with latency)
    for result in run_results:
        tracer.emit(TraceEvent.now(
            "PhilosopherResult",
            ctx.request_id,
            {
                "name": result.philosopher_id,
                "n": result.n,
                "timed_out": result.timed_out,
                "error": "" if result.error is None else result.error[:200],
                "latency_ms": -1 if result.latency_ms is None else result.latency_ms,
            },
        ))

    # 6.5 Enrich proposals with policy/trace/freedom signals
    author_stat = {r.philosopher_id: r for r in run_results}
    fp_val = tensors.metrics.get("freedom_pressure")
    fp_str = "" if fp_val is None else f"{float(fp_val):.4f}"

    enriched: List[DomainProposal] = []
    precheck_counts: Dict[str, int] = {"allow": 0, "revise": 0, "reject": 0}

    for p in raw_proposals:
        extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
        pc = dict(extra.get(PO_CORE, {}))
        author = str(pc.get(AUTHOR, ""))

        # Trace quality (author reliability)
        r = author_stat.get(author)
        rel = _author_reliability(
            timed_out=(r.timed_out if r else False),
            error=(r.error if r else None),
            latency_ms=(r.latency_ms if r else None),
            timeout_s=timeout_s,
        )
        pc[TRACEQ] = {AUTHOR_RELIABILITY: f"{rel:.3f}"}

        # Policy precheck (action gate evaluation for each candidate)
        v = deps.gate.judge_action(ctx, intent, p, tensors, memory)
        s = policy_score(v)
        pc[POLICY] = {
            "decision": v.decision.value,
            "score": f"{s:.3f}",
            "rule_ids": v.rule_ids[:8],
            "required_changes_n": str(len(v.required_changes)),
        }
        precheck_counts[v.decision.value] = precheck_counts.get(v.decision.value, 0) + 1

        # FreedomPressure embed
        pc[FREEDOM_PRESSURE] = fp_str

        extra[PO_CORE] = pc
        enriched.append(DomainProposal(
            proposal_id=p.proposal_id,
            action_type=p.action_type,
            content=p.content,
            confidence=p.confidence,
            assumption_tags=list(p.assumption_tags),
            risk_tags=list(p.risk_tags),
            extra=extra,
        ))

    proposals = enriched
    tracer.emit(TraceEvent.now(
        "PolicyPrecheckSummary",
        ctx.request_id,
        precheck_counts,
    ))

    # 7. Aggregate
    final = deps.aggregator.aggregate(ctx, intent, tensors, proposals)
    tracer.emit(TraceEvent.now(
        "AggregateCompleted",
        ctx.request_id,
        {"proposal_id": final.proposal_id, "action_type": final.action_type},
    ))

    # 7.5 Emit Pareto debug trace events (if aggregator embedded them)
    final_extra = dict(final.extra) if isinstance(final.extra, Mapping) else {}
    final_pc = final_extra.get(PO_CORE, {})
    dbg = final_pc.get(PARETO_DEBUG, {})
    if dbg:
        tracer.emit(TraceEvent.now(
            "ConflictSummaryComputed",
            ctx.request_id,
            dict(dbg.get("conflicts", {})),
        ))
        tracer.emit(TraceEvent.now(
            "ParetoFrontComputed",
            ctx.request_id,
            {"weights": dbg.get("weights", {}), "front": dbg.get("front", [])},
        ))
        tracer.emit(TraceEvent.now(
            "ParetoWinnerSelected",
            ctx.request_id,
            {"winner": dbg.get("winner", {})},
        ))

    # 8. Action Gate (Stage 2)
    v2 = deps.gate.judge_action(ctx, intent, final, tensors, memory)
    tracer.emit(TraceEvent.now(
        "SafetyJudged:Action",
        ctx.request_id,
        {"decision": v2.decision.value, "rule_ids": v2.rule_ids},
    ))
    if v2.decision != Decision.ALLOW:
        fallback = compose_fallback(ctx, v2, stage="action")
        # Pass fallback through action gate to verify it's safe
        vfb = deps.gate.judge_action(ctx, intent, fallback, tensors, memory)
        tracer.emit(TraceEvent.now(
            "SafetyDegraded",
            ctx.request_id,
            {"from": "action", **v2.meta},
        ))
        if vfb.decision == Decision.ALLOW:
            return {
                "request_id": ctx.request_id,
                "status": "ok",
                "degraded": True,
                "proposal": fallback.compact(),
                "verdict": v2.to_dict(),
            }
        # Fallback itself was rejected - hard block
        return {
            "request_id": ctx.request_id,
            "status": "blocked",
            "stage": "action",
            "verdict": v2.to_dict(),
        }

    # 9. Persist decision summary (minimal)
    deps.memory_write.append(ctx, [
        MemoryRecord(
            created_at=ctx.created_at,
            kind="decision",
            text=f"{final.action_type}:{final.content[:200]}",
            tags=["vertex", "allowed"],
        )
    ])

    # 10. Final trace
    tracer.emit(TraceEvent.now(
        "DecisionEmitted",
        ctx.request_id,
        {"proposal_id": final.proposal_id},
    ))

    return {
        "request_id": ctx.request_id,
        "status": "ok",
        "proposal": final.compact(),
    }


__all__ = [
    # Legacy
    "run_ensemble",
    "PHILOSOPHER_REGISTRY",
    "DEFAULT_PHILOSOPHERS",
    "PhilosopherTensor",
    "EnsembleMetrics",
    # Hexagonal architecture
    "EnsembleDeps",
    "run_turn",
]
