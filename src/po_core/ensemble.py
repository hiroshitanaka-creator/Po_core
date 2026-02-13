"""
Ensemble module — run_turn pipeline + philosopher registry.

The legacy ``run_ensemble()`` function was removed in v0.3.
Use ``po_core.app.api.run()`` or ``PoSelf.generate()`` instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from po_core import philosophers
from po_core.philosophers.base import Philosopher

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


# ── Hexagonal Architecture: run_turn (vertical slice) ──────────────────

from typing import Mapping, Sequence

from po_core.domain.context import Context as DomainContext
from po_core.domain.keys import (
    AUTHOR,
    AUTHOR_RELIABILITY,
    FREEDOM_PRESSURE,
    PO_CORE,
    POLICY,
    TRACEQ,
)
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.safety_verdict import Decision
from po_core.domain.trace_event import TraceEvent
from po_core.party_machine import RunResult, run_philosophers
from po_core.philosophers.base import PhilosopherProtocol
from po_core.philosophers.registry import LoadError, PhilosopherRegistry
from po_core.ports.aggregator import AggregatorPort
from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryRecord, MemoryWritePort
from po_core.ports.solarwill import SolarWillPort
from po_core.ports.tensor_engine import TensorEnginePort
from po_core.ports.trace import TracePort
from po_core.ports.wethics_gate import WethicsGatePort
from po_core.runtime.settings import Settings
from po_core.safety.fallback import compose_fallback
from po_core.safety.policy_scoring import policy_score
from po_core.trace.decision_compare import emit_decision_comparison
from po_core.trace.decision_events import (
    emit_decision_emitted,
    emit_safety_override_applied,
    emit_wethics_gate_explained,
)
from po_core.trace.pareto_events import emit_pareto_debug_events


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
    aggregator_shadow: Optional[AggregatorPort]  # Shadow Pareto A/B評価用
    registry: PhilosopherRegistry  # SafetyMode-based selection
    settings: Settings  # Worker/timeout settings
    shadow_guard: Optional[object]  # ShadowGuard (自律ブレーキ)
    deliberation_engine: Optional[object] = None  # DeliberationEngine (Phase 2)


def _get_swarm_params(mode: SafetyMode, settings: Settings) -> tuple[int, float]:
    """Get worker count and timeout based on SafetyMode."""
    if mode == SafetyMode.CRITICAL:
        return (
            settings.philosopher_workers_critical,
            settings.philosopher_timeout_s_critical,
        )
    elif mode == SafetyMode.WARN:
        return settings.philosopher_workers_warn, settings.philosopher_timeout_s_warn
    else:  # NORMAL or UNKNOWN
        return (
            settings.philosopher_workers_normal,
            settings.philosopher_timeout_s_normal,
        )


def _evaluate_candidate(
    *,
    ctx: DomainContext,
    deps: EnsembleDeps,
    intent: Any,
    tensors: Any,
    memory: Any,
    candidate: Any,
    variant: str,
    origin: str,
) -> tuple[Any, bool]:
    """
    候補（Pareto選択結果）をAction Gateで評価し、最終決定を返す。

    Shadow評価とmain評価で共通のロジックを抽出。

    Args:
        ctx: Request context
        deps: Dependencies
        intent: Solar Will intent
        tensors: Tensor snapshot
        memory: Memory snapshot
        candidate: Aggregatorが返した候補Proposal
        variant: "main" or "shadow"
        origin: "pareto" or "pareto_shadow"

    Returns:
        (最終Proposal, degraded: bool)
        - ALLOWならcandidate (degraded=False)
        - それ以外ならfallback (degraded=True)
    """
    tracer = deps.tracer

    # Pareto debug（候補時点）
    emit_pareto_debug_events(tracer, ctx, candidate, variant=variant)

    # Action Gate evaluation
    v = deps.gate.judge_action(ctx, intent, candidate, tensors, memory)

    if v.decision == Decision.ALLOW:
        # 正常経路：候補がそのまま最終
        emit_decision_emitted(
            tracer,
            ctx,
            variant=variant,
            stage="action",
            origin=origin,
            final=candidate,
            candidate=candidate,
            gate_verdict=v,
            degraded=False,
        )
        return candidate, False

    # 安全上書き：fallbackへ縮退
    fb = compose_fallback(ctx, v, stage="action")

    emit_safety_override_applied(
        tracer,
        ctx,
        variant=variant,
        stage="action",
        reason=f"gate_{v.decision.value}",
        from_proposal=candidate,
        to_proposal=fb,
        verdict=v,
    )

    # Fallback自体もAction Gateで検証
    vfb = deps.gate.judge_action(ctx, intent, fb, tensors, memory)

    emit_decision_emitted(
        tracer,
        ctx,
        variant=variant,
        stage="action",
        origin=f"{origin}_fallback",
        final=fb,
        candidate=candidate,
        gate_verdict=vfb,
        degraded=True,
    )

    return fb, True


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
    tracer.emit(
        TraceEvent.now(
            "MemorySnapshotted",
            ctx.request_id,
            {"items": len(memory.items)},
        )
    )

    # 2. Tensor computation
    tensors = deps.tensors.compute(ctx, memory)
    tracer.emit(
        TraceEvent.now(
            "TensorComputed",
            ctx.request_id,
            {"metrics": list(tensors.metrics.keys()), "version": tensors.version},
        )
    )

    # Determine SafetyMode from tensors
    safety_config = SafetyModeConfig(
        warn=deps.settings.freedom_pressure_warn,
        critical=deps.settings.freedom_pressure_critical,
        missing_mode=deps.settings.freedom_pressure_missing_mode,
    )
    mode, _ = infer_safety_mode(tensors, safety_config)

    # 3. SolarWill intent
    intent, will_meta = deps.solarwill.compute_intent(ctx, tensors, memory)
    tracer.emit(
        TraceEvent.now(
            "IntentGenerated",
            ctx.request_id,
            dict(will_meta),
        )
    )

    # 4. Intention Gate (Stage 1)
    v1 = deps.gate.judge_intent(ctx, intent, tensors, memory)
    tracer.emit(
        TraceEvent.now(
            "SafetyJudged:Intention",
            ctx.request_id,
            {"decision": v1.decision.value, "rule_ids": v1.rule_ids},
        )
    )
    if v1.decision != Decision.ALLOW:
        fallback = compose_fallback(ctx, v1, stage="intention")
        # Pass fallback through action gate to verify it's safe
        vfb = deps.gate.judge_action(ctx, intent, fallback, tensors, memory)
        tracer.emit(
            TraceEvent.now(
                "SafetyDegraded",
                ctx.request_id,
                {"from": "intention", **v1.meta},
            )
        )
        if vfb.decision == Decision.ALLOW:
            # 意図段階で縮退（候補なし）
            emit_decision_emitted(
                tracer,
                ctx,
                stage="intent",
                origin="intent_gate_fallback",
                final=fallback,
                candidate=None,
                gate_verdict=vfb,
                degraded=True,
            )
            return {
                "request_id": ctx.request_id,
                "status": "ok",
                "degraded": True,
                "proposal": fallback.compact(),
                "verdict": v1.to_dict(),
            }
        # Fallback itself was rejected - hard block
        emit_decision_emitted(
            tracer,
            ctx,
            stage="intent",
            origin="intent_gate_blocked",
            final=fallback,
            candidate=None,
            gate_verdict=vfb,
            degraded=True,
        )
        return {
            "request_id": ctx.request_id,
            "status": "blocked",
            "stage": "intention",
            "verdict": v1.to_dict(),
        }

    # 5. Select philosophers based on SafetyMode (編成)
    sel = deps.registry.select(mode)
    max_workers, timeout_s = _get_swarm_params(mode, deps.settings)
    tracer.emit(
        TraceEvent.now(
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
        )
    )

    # Load philosophers (with error recovery)
    philosophers, load_errors = deps.registry.load(sel.selected_ids)
    for e in load_errors:
        tracer.emit(
            TraceEvent.now(
                "PhilosopherLoadError",
                ctx.request_id,
                {
                    "id": e.philosopher_id,
                    "module": e.module,
                    "symbol": e.symbol,
                    "error": e.error,
                },
            )
        )

    # 6. Parallel philosopher execution with timeout
    from po_core.domain.proposal import Proposal as DomainProposal

    raw_proposals: List[DomainProposal] = []
    ph_proposals, run_results = run_philosophers(
        philosophers,
        ctx,
        intent,
        tensors,
        memory,
        max_workers=max_workers,
        timeout_s=timeout_s,
    )
    raw_proposals.extend(ph_proposals)

    # Emit trace events for each result (with latency)
    for result in run_results:
        tracer.emit(
            TraceEvent.now(
                "PhilosopherResult",
                ctx.request_id,
                {
                    "name": result.philosopher_id,
                    "n": result.n,
                    "timed_out": result.timed_out,
                    "error": "" if result.error is None else result.error[:200],
                    "latency_ms": (
                        -1 if result.latency_ms is None else result.latency_ms
                    ),
                },
            )
        )

    # 6.5 Deliberation Engine (multi-round philosopher dialogue)
    if deps.deliberation_engine is not None and hasattr(
        deps.deliberation_engine, "deliberate"
    ):
        delib_result = deps.deliberation_engine.deliberate(
            philosophers, ctx, intent, tensors, memory, raw_proposals
        )
        raw_proposals = delib_result.proposals
        tracer.emit(
            TraceEvent.now(
                "DeliberationCompleted",
                ctx.request_id,
                delib_result.summary(),
            )
        )

    # 6.6 Enrich proposals with policy/trace/freedom signals
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
        enriched.append(
            DomainProposal(
                proposal_id=p.proposal_id,
                action_type=p.action_type,
                content=p.content,
                confidence=p.confidence,
                assumption_tags=list(p.assumption_tags),
                risk_tags=list(p.risk_tags),
                extra=extra,
            )
        )

    proposals = enriched
    tracer.emit(
        TraceEvent.now(
            "PolicyPrecheckSummary",
            ctx.request_id,
            precheck_counts,
        )
    )

    # 7. Main Pareto Aggregation
    candidate_main = deps.aggregator.aggregate(ctx, intent, tensors, proposals)
    tracer.emit(
        TraceEvent.now(
            "AggregateCompleted",
            ctx.request_id,
            {
                "proposal_id": candidate_main.proposal_id,
                "action_type": candidate_main.action_type,
            },
        )
    )

    # 8. Main evaluation (Pareto debug + Action Gate)
    final_main, main_degraded = _evaluate_candidate(
        ctx=ctx,
        deps=deps,
        intent=intent,
        tensors=tensors,
        memory=memory,
        candidate=candidate_main,
        variant="main",
        origin="pareto",
    )

    # 8.5 Observability: emit WethicsGateExplained (Phase 3)
    try:
        from po_core.safety.wethics_gate.explanation import (
            build_explanation_from_verdict,
        )

        _final_verdict = deps.gate.judge_action(
            ctx, intent, final_main, tensors, memory
        )
        _explanation = build_explanation_from_verdict(_final_verdict)
        emit_wethics_gate_explained(tracer, ctx, explanation_chain=_explanation)
    except Exception:
        pass  # observability must never break the pipeline

    # 9. Shadow Pareto A/B evaluation（オプショナル）
    if deps.aggregator_shadow is not None:
        try:
            # Pre-check: should run shadow? (ShadowGuard autonomous brake)
            if deps.shadow_guard is not None:
                run_shadow, ev = deps.shadow_guard.should_run_shadow(ctx)
                if ev is not None:
                    tracer.emit(ev)
                if not run_shadow:
                    # Shadow is disabled (cooldown) - skip shadow block
                    # Don't emit DecisionComparisonComputed (no comparison happened)
                    pass  # Exit shadow block
                else:
                    # Shadow Guard允許：実行
                    # Shadow Pareto aggregation（同じproposals集合）
                    candidate_shadow = deps.aggregator_shadow.aggregate(
                        ctx, intent, tensors, proposals
                    )

                    # Shadow evaluation
                    final_shadow, shadow_degraded = _evaluate_candidate(
                        ctx=ctx,
                        deps=deps,
                        intent=intent,
                        tensors=tensors,
                        memory=memory,
                        candidate=candidate_shadow,
                        variant="shadow",
                        origin="pareto_shadow",
                    )

                    # Post-check: observe & maybe disable (ShadowGuard autonomous brake)
                    ev2 = deps.shadow_guard.observe_comparison(
                        ctx,
                        main_candidate=candidate_main,
                        main_final=final_main,
                        shadow_candidate=candidate_shadow,
                        shadow_final=final_shadow,
                        main_degraded=main_degraded,
                        shadow_degraded=shadow_degraded,
                    )
                    if ev2 is not None:
                        tracer.emit(ev2)

                    # Comparison event（監査ログに差分を残す）
                    emit_decision_comparison(
                        tracer,
                        ctx,
                        main_candidate=candidate_main,
                        main_final=final_main,
                        shadow_candidate=candidate_shadow,
                        shadow_final=final_shadow,
                    )
            else:
                # No guard - run shadow normally
                # Shadow Pareto aggregation（同じproposals集合）
                candidate_shadow = deps.aggregator_shadow.aggregate(
                    ctx, intent, tensors, proposals
                )

                # Shadow evaluation
                final_shadow, shadow_degraded = _evaluate_candidate(
                    ctx=ctx,
                    deps=deps,
                    intent=intent,
                    tensors=tensors,
                    memory=memory,
                    candidate=candidate_shadow,
                    variant="shadow",
                    origin="pareto_shadow",
                )

                # Comparison event（監査ログに差分を残す）
                emit_decision_comparison(
                    tracer,
                    ctx,
                    main_candidate=candidate_main,
                    main_final=final_main,
                    shadow_candidate=candidate_shadow,
                    shadow_final=final_shadow,
                )
        except Exception:
            # Shadow失敗は無視（main は必ず返す）
            pass

    # 10. Persist decision summary (main のみ)
    deps.memory_write.append(
        ctx,
        [
            MemoryRecord(
                created_at=ctx.created_at,
                kind="decision",
                text=f"{final_main.action_type}:{final_main.content[:200]}",
                tags=["vertex", "allowed"],
            )
        ],
    )

    # 11. Return (main のみ)
    return {
        "request_id": ctx.request_id,
        "status": "ok",
        "proposal": final_main.compact(),
    }


__all__ = [
    "PHILOSOPHER_REGISTRY",
    "DEFAULT_PHILOSOPHERS",
    # Hexagonal architecture
    "EnsembleDeps",
    "run_turn",
]
