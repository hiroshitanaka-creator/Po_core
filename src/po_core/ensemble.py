"""
Ensemble module — run_turn pipeline + philosopher registry.

The legacy ``run_ensemble()`` function was removed in v0.3.
Use ``po_core.app.api.run()`` or ``PoSelf.generate()`` instead.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Union,
    cast,
)

from po_core import philosophers
from po_core.axis.scoring import score_text_with_debug
from po_core.axis.spec import load_axis_spec
from po_core.deliberation.protocol import run_deliberation
from po_core.domain.case_signals import CaseSignals
from po_core.domain.context import Context as DomainContext
from po_core.domain.keys import (
    AUTHOR,
    AUTHOR_RELIABILITY,
    EMERGENCE_NOVELTY,
    FREEDOM_PRESSURE,
    PO_CORE,
    POLICY,
    TRACEQ,
)
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.safety_verdict import Decision
from po_core.domain.trace_event import TraceEvent
from po_core.party_machine import RunResult, async_run_philosophers, run_philosophers
from po_core.philosophers.allowlist import AllowlistRegistry
from po_core.philosophers.base import Philosopher, PhilosopherProtocol
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.philosophers.tags import (
    TAG_CLARIFY,
    TAG_COMPLIANCE,
    TAG_CREATIVE,
    TAG_CRITIC,
    TAG_PLANNER,
    TAG_REDTEAM,
)
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
from po_core.safety.wethics_gate.explanation import build_explanation_from_verdict
from po_core.trace.decision_compare import emit_decision_comparison
from po_core.trace.decision_events import (
    emit_decision_emitted,
    emit_safety_override_applied,
)
from po_core.trace.pareto_events import emit_pareto_debug_events
from po_core.trace.synthesis_report_events import emit_synthesis_report_built

DEFAULT_PHILOSOPHERS: List[str] = ["aristotle", "confucius", "wittgenstein"]

# Scenario-sensitive routing table for non-default scenario types.
# Each entry maps scenario_type → (preferred_tags, scenario_limit).
#
# preferred_tags: overrides SelectionPlan.require_tags for the first-pass slot
#   fill, guaranteeing the right archetypes appear in the roster.
# scenario_limit: tighter roster cap needed because NORMAL mode's budget equals
#   the total cost of all 42 philosophers — without a limit the preferred_tags
#   would be absorbed and all 42 would still be selected.
#
# Tag semantics
# ─────────────
# values_clarification  → clarify + creative + compliance:
#   clarify     → confucius (risk=0, weight=1.5) — question-generating, values-
#                 exploring contemplative voice
#   creative    → zhuangzi (risk=1, weight=1.0) — analogical, divergent thinking
#   compliance  → kant (risk=0) fills the third slot — normative grounding
#
# conflicting_constraints → critic + redteam + planner:
#   critic      → kant (risk=0) — structural critique, contradiction detection
#   redteam     → nietzsche (risk=2) — adversarial revaluation, exposes hidden
#                 assumptions behind each constraint
#   planner     → marcus_aurelius (risk=0) fills the third slot — pragmatic
#                 decomposition
#
# With limit=3 the required-tag phase exhausts all slots.  In NORMAL mode
# (max_risk=2, budget=80) confucius is excluded from the conflicting_constraints
# roster because it carries no critic/redteam/planner tags, so the Pareto
# winner differs between scenarios.  In WARN/CRITICAL mode redteam philosophers
# (risk=2) are filtered out before selection; the roster will differ from the
# NORMAL prediction above, but the scenario_type signal and preferred_tags are
# still forwarded to the registry for whatever selection it can satisfy.
_EXPECTED_TENSOR_METRICS: tuple = (
    "freedom_pressure",
    "semantic_delta",
    "blocked_tensor",
    "interaction_tensor",
)


def _tensor_metric_status_entry(
    name: str,
    value: Any,
    tensor_values: Mapping[str, Any],
) -> Dict[str, Any]:
    """Return the metric_status entry for a single tensor metric."""
    if isinstance(value, (int, float)):
        tv = tensor_values.get(name)
        return {
            "status": "computed",
            "source": tv.source if tv is not None else "unknown",
        }
    return {"status": "missing", "source": None}


_SCENARIO_ROUTING: Dict[str, tuple] = {
    "values_clarification": (
        (TAG_CLARIFY, TAG_CREATIVE, TAG_COMPLIANCE),
        3,
    ),
    "conflicting_constraints": (
        (TAG_CRITIC, TAG_REDTEAM, TAG_PLANNER),
        3,
    ),
}
logger = logging.getLogger(__name__)


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
    "appiah": philosophers.Appiah,
    "fanon": philosophers.Fanon,
    "charles_taylor": philosophers.CharlesTaylor,
}


# ── Hexagonal Architecture: run_turn (vertical slice) ──────────────────


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
    registry: Union[
        PhilosopherRegistry, AllowlistRegistry
    ]  # SafetyMode-based selection
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


class _PhasePreResult(NamedTuple):
    """Carries state from pipeline phases 1-5 into the philosopher dispatch."""

    memory: Any
    tensors: Any
    intent: Any
    mode: SafetyMode
    philosophers: List[PhilosopherProtocol]
    max_workers: int
    timeout_s: float


def _debate_v1_enabled() -> bool:
    return os.getenv("PO_DEBATE_V1", "").lower() in ("1", "true", "yes")


def _run_deliberation_protocol_v1(
    *,
    ctx: DomainContext,
    philosophers: Sequence[PhilosopherProtocol],
    proposals: Sequence[Any],
    tracer: TracePort,
) -> None:
    settings = {"max_critiques_per_philosopher": 2}
    cards, critiques, report = run_deliberation(
        input={"prompt": ctx.user_input, "proposals": list(proposals)},
        philosophers=philosophers,
        axis_spec={"axes": ["ethics", "risk", "evidence"]},
        settings=settings,
    )
    tracer.emit(
        TraceEvent.now(
            "DebateProtocolV1Completed",
            ctx.request_id,
            {
                "cards": len(cards),
                "critiques": len(critiques),
                "report": report,
            },
        )
    )


def _proposal_author_key(proposal: Any) -> str:
    """Resolve proposal author key: _po_core.author → extra["philosopher"] → ""."""
    try:
        extra = getattr(proposal, "extra", None)
        extra = extra if isinstance(extra, Mapping) else {}
        pc = extra.get(PO_CORE) if isinstance(extra, Mapping) else None
        if isinstance(pc, Mapping):
            author = pc.get(AUTHOR)
            if isinstance(author, str) and author:
                return author
        philosopher = extra.get("philosopher") if isinstance(extra, Mapping) else None
        if isinstance(philosopher, str) and philosopher:
            return philosopher
    except Exception:
        pass
    return ""


def _normalize_primary_proposals(proposals: List[Any]) -> tuple[List[Any], List[Any]]:
    """Normalize to one primary proposal per author while preserving input order."""
    primaries: List[Any] = []
    secondaries: List[Any] = []
    seen_authors: set[str] = set()

    for proposal in proposals:
        author_key = _proposal_author_key(proposal)
        if author_key and author_key in seen_authors:
            secondaries.append(proposal)
            continue
        if author_key:
            seen_authors.add(author_key)
        primaries.append(proposal)
    return primaries, secondaries


def _build_safety_mode_inferred_payload(
    mode: SafetyMode,
    fp_value: "Optional[float]",
    config: SafetyModeConfig,
) -> dict:
    """Build the SafetyModeInferred trace payload.

    Pure function; called from _run_phase_pre and testable in isolation.
    """
    if fp_value is None:
        reason = "freedom_pressure_missing"
    elif fp_value >= config.critical:
        reason = "freedom_pressure >= critical_threshold"
    elif fp_value >= config.warn:
        reason = "warn_threshold <= freedom_pressure < critical_threshold"
    else:
        reason = "freedom_pressure < warn_threshold"
    return {
        "mode": mode.value,
        "freedom_pressure": fp_value,
        "warn_threshold": config.warn,
        "critical_threshold": config.critical,
        "missing_mode": config.missing_mode.value,
        "source_metric": "freedom_pressure",
        "reason": reason,
    }


def _run_phase_pre(
    ctx: DomainContext,
    deps: "EnsembleDeps",
    case_signals: Optional[CaseSignals] = None,
) -> Union["_PhasePreResult", Dict[str, Any]]:
    """
    Pipeline phases 1-5: memory → tensors → intent → intention gate →
    philosopher selection/loading.

    Returns:
        _PhasePreResult  on the happy path.
        dict             on early exit (intention gate blocked).
    """
    tracer = deps.tracer

    # 1. Memory snapshot
    memory = deps.memory_read.snapshot(ctx)
    tracer.emit(
        TraceEvent.now(
            "MemorySnapshotted", ctx.request_id, {"items": len(memory.items)}
        )
    )

    # 2. Tensor computation
    tensors = deps.tensors.compute(ctx, memory)
    _metric_status: Dict[str, Any] = {}
    for _mname in _EXPECTED_TENSOR_METRICS:
        _metric_status[_mname] = _tensor_metric_status_entry(
            _mname, tensors.metrics.get(_mname), tensors.values
        )
    for _mname in tensors.metrics:
        if _mname not in _metric_status:
            _metric_status[_mname] = _tensor_metric_status_entry(
                _mname, tensors.metrics[_mname], tensors.values
            )
    tracer.emit(
        TraceEvent.now(
            "TensorComputed",
            ctx.request_id,
            {
                "metrics": dict(tensors.metrics),
                "version": tensors.version,
                "metric_status": _metric_status,
            },
        )
    )

    # Determine SafetyMode from tensors
    safety_config = SafetyModeConfig(
        warn=deps.settings.freedom_pressure_warn,
        critical=deps.settings.freedom_pressure_critical,
        missing_mode=deps.settings.freedom_pressure_missing_mode,
    )
    mode, fp_value = infer_safety_mode(tensors, safety_config)

    tracer.emit(
        TraceEvent.now(
            "SafetyModeInferred",
            ctx.request_id,
            _build_safety_mode_inferred_payload(mode, fp_value, safety_config),
        )
    )

    # 3. SolarWill intent
    intent, will_meta = deps.solarwill.compute_intent(ctx, tensors, memory)
    tracer.emit(TraceEvent.now("IntentGenerated", ctx.request_id, dict(will_meta)))

    # 4. Intention Gate (Stage 1)
    v1 = deps.gate.judge_intent(ctx, intent, tensors, memory)
    tracer.emit(
        TraceEvent.now(
            "SafetyJudged:Intention",
            ctx.request_id,
            {"decision": v1.decision.value, "rule_ids": v1.rule_ids},
        )
    )

    # ExplanationChain for intention gate (Phase 3)
    if v1.decision != Decision.ALLOW:
        try:
            intent_explanation = build_explanation_from_verdict(v1, stage="intention")
            tracer.emit(
                TraceEvent.now(
                    "ExplanationEmitted",
                    ctx.request_id,
                    intent_explanation.to_dict(),
                )
            )
        except Exception as exc:
            logger.exception(
                "Failed to emit ExplanationEmitted for intention gate verdict",
                extra={
                    "request_id": ctx.request_id,
                    "stage": "intention",
                    "decision": v1.decision.value,
                    "error_type": type(exc).__name__,
                },
            )
            tracer.emit(
                TraceEvent.now(
                    "ExplanationEmitFailed",
                    ctx.request_id,
                    {
                        "stage": "intention",
                        "decision": v1.decision.value,
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    },
                )
            )

    if v1.decision != Decision.ALLOW:
        fallback = compose_fallback(ctx, v1, stage="intention")
        vfb = deps.gate.judge_action(ctx, intent, fallback, tensors, memory)
        tracer.emit(
            TraceEvent.now(
                "SafetyDegraded", ctx.request_id, {"from": "intention", **v1.meta}
            )
        )
        if vfb.decision == Decision.ALLOW:
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
    # When CaseSignals carries a non-default scenario_type, steer first-pass
    # tag requirements AND apply a tighter roster limit so that the preferred-tag
    # archetypes are not diluted by the full NORMAL budget (which equals the
    # total cost of all 42 philosophers and would otherwise admit everyone).
    scenario_type = (
        case_signals.scenario_type if case_signals is not None else "general"
    )
    _routing = _SCENARIO_ROUTING.get(scenario_type)
    preferred_tags: Optional[tuple] = _routing[0] if _routing else None
    limit_override: Optional[int] = _routing[1] if _routing else None
    sel = deps.registry.select(
        mode,
        preferred_tags=preferred_tags,
        limit_override=limit_override,
    )
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
                "scenario_type": scenario_type,
                "preferred_tags": (
                    list(sel.preferred_tags) if sel.preferred_tags else None
                ),
                "limit_override": sel.limit_override,
                "max_risk": sel.max_risk,
                "cost_budget": sel.cost_budget,
                "limit": sel.limit,
                "require_tags": list(sel.require_tags),
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

    return _PhasePreResult(
        memory=memory,
        tensors=tensors,
        intent=intent,
        mode=mode,
        philosophers=philosophers,
        max_workers=max_workers,
        timeout_s=timeout_s,
    )


def _run_phase_post(
    ctx: DomainContext,
    deps: "EnsembleDeps",
    pre: "_PhasePreResult",
    ph_proposals: List[Any],
    run_results: List[RunResult],
) -> Dict[str, Any]:
    """
    Pipeline phases 6.5-10: emit PhilosopherResult events, deliberation,
    policy enrichment, Pareto aggregation, Action Gate, memory write.
    """
    from po_core.domain.proposal import Proposal as DomainProposal

    tracer = deps.tracer
    memory, tensors, intent = pre.memory, pre.tensors, pre.intent
    timeout_s = pre.timeout_s

    raw_proposals: List[DomainProposal] = [p for p in ph_proposals if p is not None]
    synthesis_report: Optional[Dict[str, Any]] = None

    if _debate_v1_enabled() and raw_proposals:
        _run_deliberation_protocol_v1(
            ctx=ctx,
            philosophers=pre.philosophers,
            proposals=raw_proposals,
            tracer=tracer,
        )

    def _extract_llm_route(proposal: DomainProposal | None) -> Dict[str, Any]:
        if proposal is None:
            return {}

        extra = proposal.extra if isinstance(proposal.extra, Mapping) else {}
        normalized = extra.get("normalized_response")
        normalized_dict = normalized if isinstance(normalized, Mapping) else {}
        metadata = normalized_dict.get("metadata")
        metadata_dict = metadata if isinstance(metadata, Mapping) else {}

        route: Dict[str, Any] = {}
        provider = metadata_dict.get("llm_provider")
        model = metadata_dict.get("llm_model")
        llm_fallback = metadata_dict.get("llm_fallback")
        fallback_reason = metadata_dict.get("fallback_reason")

        if provider not in (None, ""):
            route["llm_provider"] = str(provider)
        if model not in (None, ""):
            route["llm_model"] = str(model)
        if llm_fallback is not None:
            route["llm_fallback"] = bool(llm_fallback)
        if fallback_reason not in (None, ""):
            route["fallback_reason"] = str(fallback_reason)
        return route

    # Emit trace events for each philosopher execution result
    for run_result in run_results:
        matched_proposal = next(
            (
                p
                for p in raw_proposals
                if isinstance(p, DomainProposal)
                and _proposal_author_key(p) == run_result.philosopher_id
            ),
            None,
        )
        _display_name: str
        if matched_proposal is not None:
            _mp_extra = getattr(matched_proposal, "extra", None)
            _mp_extra = _mp_extra if isinstance(_mp_extra, Mapping) else {}
            _display_name = _mp_extra.get("philosopher") or run_result.philosopher_id
        else:
            _display_name = run_result.philosopher_id
        payload: Dict[str, Any] = {
            "philosopher_id": run_result.philosopher_id,
            "name": _display_name,
            "n": run_result.n,
            "timed_out": run_result.timed_out,
            "error": "" if run_result.error is None else run_result.error[:200],
            "latency_ms": (
                -1 if run_result.latency_ms is None else run_result.latency_ms
            ),
        }
        payload.update(_extract_llm_route(matched_proposal))

        tracer.emit(TraceEvent.now("PhilosopherResult", ctx.request_id, payload))

    # 6.5 Deliberation Engine (multi-round philosopher dialogue)
    if deps.deliberation_engine is not None and hasattr(
        deps.deliberation_engine, "deliberate"
    ):
        primary_proposals, secondary_proposals = _normalize_primary_proposals(
            raw_proposals
        )
        delib_result = deps.deliberation_engine.deliberate(
            pre.philosophers, ctx, intent, tensors, memory, primary_proposals
        )
        raw_proposals = list(delib_result.proposals) + secondary_proposals
        tracer.emit(
            TraceEvent.now(
                "DeliberationCompleted", ctx.request_id, delib_result.summary()
            )
        )

        # Embed emergence novelty scores into proposals so Pareto can reward them.
        # EmergenceSignal.source_philosopher → author → proposal.extra[PO_CORE][EMERGENCE_NOVELTY]
        if delib_result.emergence_signals:
            author_novelty: Dict[str, float] = {}
            for sig in delib_result.emergence_signals:
                prev = author_novelty.get(sig.source_philosopher, 0.0)
                author_novelty[sig.source_philosopher] = max(prev, sig.novelty_score)

            tagged: List[DomainProposal] = []
            for p in raw_proposals:
                extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
                pc = dict(extra.get(PO_CORE, {}))
                author = str(pc.get(AUTHOR, ""))
                novelty = author_novelty.get(author, 0.0)
                if novelty > 0.0:
                    pc[EMERGENCE_NOVELTY] = f"{novelty:.4f}"
                    extra[PO_CORE] = pc
                    tagged.append(
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
                else:
                    tagged.append(p)
            raw_proposals = tagged

    # 6.6 Enrich proposals with policy/trace/freedom signals
    author_stat = {r.philosopher_id: r for r in run_results}
    fp_val = tensors.metrics.get("freedom_pressure")
    fp_str = "" if fp_val is None else f"{float(fp_val):.4f}"

    enriched: List[DomainProposal] = []
    precheck_counts: Dict[str, int] = {"allow": 0, "revise": 0, "reject": 0}
    axis_spec = load_axis_spec()

    for p in raw_proposals:
        extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
        pc = dict(extra.get(PO_CORE, {}))
        author = str(pc.get(AUTHOR, ""))

        r = author_stat.get(author)
        rel = _author_reliability(
            timed_out=(r.timed_out if r else False),
            error=(r.error if r else None),
            latency_ms=(r.latency_ms if r else None),
            timeout_s=timeout_s,
        )
        pc[TRACEQ] = {AUTHOR_RELIABILITY: f"{rel:.3f}"}

        v = deps.gate.judge_action(ctx, intent, p, tensors, memory)
        s = policy_score(v)
        pc[POLICY] = {
            "decision": v.decision.value,
            "score": f"{s:.3f}",
            "rule_ids": v.rule_ids[:8],
            "required_changes_n": str(len(v.required_changes)),
        }
        precheck_counts[v.decision.value] = precheck_counts.get(v.decision.value, 0) + 1
        pc[FREEDOM_PRESSURE] = fp_str
        axis_scores, axis_scoring_debug = score_text_with_debug(
            str(p.content), axis_spec
        )
        pc["axis_scores"] = axis_scores
        pc["axis_scoring_debug"] = axis_scoring_debug
        pc["axis_name"] = axis_spec.axis_name
        pc["axis_spec_version"] = axis_spec.spec_version
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

    # Internal structured synthesis (deterministic stats + enumeration).
    # Default behavior is unchanged; report is only surfaced when requested.
    try:
        synthesis_report = _build_synthesis_report(proposals)
    except Exception as exc:
        logger.exception(
            "Synthesis report construction failed",
            extra={
                "request_id": ctx.request_id,
                "error_type": type(exc).__name__,
            },
        )
        tracer.emit(
            TraceEvent.now(
                "SynthesisReportFailed",
                ctx.request_id,
                {
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
        )
        synthesis_report = {}

    emit_synthesis_report_built(
        tracer,
        ctx,
        synthesis_report,
        axis_name=axis_spec.axis_name,
        axis_spec_version=axis_spec.spec_version,
    )

    tracer.emit(
        TraceEvent.now("PolicyPrecheckSummary", ctx.request_id, precheck_counts)
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

    # 9. Shadow Pareto A/B evaluation (optional)
    if deps.aggregator_shadow is not None:
        try:
            if deps.shadow_guard is not None:
                _sg = cast(Any, deps.shadow_guard)
                run_shadow, ev = _sg.should_run_shadow(ctx)
                if ev is not None:
                    tracer.emit(ev)
                if run_shadow:
                    candidate_shadow = deps.aggregator_shadow.aggregate(
                        ctx, intent, tensors, proposals
                    )
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
                    ev2 = _sg.observe_comparison(
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
                    emit_decision_comparison(
                        tracer,
                        ctx,
                        main_candidate=candidate_main,
                        main_final=final_main,
                        shadow_candidate=candidate_shadow,
                        shadow_final=final_shadow,
                    )
            else:
                candidate_shadow = deps.aggregator_shadow.aggregate(
                    ctx, intent, tensors, proposals
                )
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
                emit_decision_comparison(
                    tracer,
                    ctx,
                    main_candidate=candidate_main,
                    main_final=final_main,
                    shadow_candidate=candidate_shadow,
                    shadow_final=final_shadow,
                )
        except Exception as exc:
            logger.exception(
                "Shadow Pareto A/B evaluation failed",
                extra={
                    "request_id": ctx.request_id,
                    "error_type": type(exc).__name__,
                },
            )
            tracer.emit(
                TraceEvent.now(
                    "ShadowParetoFailed",
                    ctx.request_id,
                    {
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    },
                )
            )

    # 10. Persist decision summary (main only)
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

    def _to_rest_proposal(p: DomainProposal) -> Dict[str, Any]:
        extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
        po_meta = extra.get(PO_CORE, {})
        po_meta_dict = dict(po_meta) if isinstance(po_meta, Mapping) else {}

        author_raw = po_meta_dict.get(AUTHOR) or extra.get("philosopher")
        author = str(author_raw) if author_raw is not None else "unknown"

        normalized_raw = extra.get("normalized_response")
        normalized = dict(normalized_raw) if isinstance(normalized_raw, Mapping) else {}
        metadata_raw = normalized.get("metadata")
        metadata = dict(metadata_raw) if isinstance(metadata_raw, Mapping) else {}

        return {
            "philosopher_id": author,
            "name": author,
            "content": str(getattr(p, "content", "")),
            "proposal": str(getattr(p, "content", "")),
            "weight": float(getattr(p, "confidence", 0.0)),
            "score": float(getattr(p, "confidence", 0.0)),
            "normalized_response": normalized,
            "metadata": metadata,
        }

    rest_proposals = [
        _to_rest_proposal(p)
        for p in sorted(
            proposals,
            key=lambda p: (
                -float(getattr(p, "confidence", 0.0)),
                str(getattr(p, "proposal_id", "")),
            ),
        )[:5]
    ]

    result: Dict[str, Any] = {
        "request_id": ctx.request_id,
        "status": "ok",
        "proposal": final_main.compact(),
        "proposals": rest_proposals,
    }

    if _structured_output_enabled() and synthesis_report:
        result["synthesis_report"] = synthesis_report

    return result


def _structured_output_enabled() -> bool:
    v = os.getenv("PO_STRUCTURED_OUTPUT", "").strip().lower()
    return v in {"1", "true", "yes", "on"}


def _build_synthesis_report(proposals: Sequence[Any]) -> Dict[str, Any]:
    from po_core.deliberation.synthesis import ArgumentCard, AxisSpec, SynthesisEngine

    cards: List[ArgumentCard] = []
    axis_vectors: List[Dict[str, Any]] = []
    axis_names: set[str] = set()
    total_hits_values: List[int] = []
    for p in proposals:
        extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
        po_core_meta = extra.get(PO_CORE, {})
        pc = dict(po_core_meta) if isinstance(po_core_meta, Mapping) else {}

        stance = str(pc.get("dialectic_role", p.action_type or "unknown"))
        claims = [str(p.content).strip()] if str(p.content).strip() else []

        axis_scores_raw = pc.get("axis_scores", {})
        axis_scores: Dict[str, float] = {}
        if isinstance(axis_scores_raw, Mapping):
            for k, v in axis_scores_raw.items():
                try:
                    axis_scores[str(k)] = float(v)
                except (TypeError, ValueError):
                    continue
        axis_names.update(axis_scores.keys())

        policy = pc.get(POLICY, {})
        policy_decision: Optional[str] = None
        if isinstance(policy, Mapping):
            decision = policy.get("decision")
            if decision is not None:
                policy_decision = str(decision)

        if axis_scores:
            author_raw = pc.get(AUTHOR)
            author = str(author_raw) if author_raw is not None else None
            axis_vectors.append(
                {
                    "author": author,
                    "proposal_id": str(getattr(p, "proposal_id", "")),
                    "confidence": float(getattr(p, "confidence", 0.5)),
                    "axis_scores": axis_scores,
                    "policy": policy_decision,
                }
            )

        axis_scoring_debug_raw = pc.get("axis_scoring_debug", {})
        axis_scoring_debug = (
            dict(axis_scoring_debug_raw)
            if isinstance(axis_scoring_debug_raw, Mapping)
            else {}
        )
        try:
            total_hits_values.append(int(axis_scoring_debug.get("total_hits", 0)))
        except (TypeError, ValueError):
            total_hits_values.append(0)

        questions = []
        qs = pc.get("open_questions", [])
        if isinstance(qs, Sequence) and not isinstance(qs, (str, bytes)):
            questions = [str(q).strip() for q in qs if str(q).strip()]

        cards.append(
            ArgumentCard(
                card_id=str(getattr(p, "proposal_id", "")),
                stance=stance,
                claims=claims,
                axis_scores=axis_scores,
                confidence=float(getattr(p, "confidence", 0.5)),
                questions=questions,
            )
        )

    axis_spec = AxisSpec(dimensions=sorted(axis_names))
    report = SynthesisEngine().synthesize(axis_spec=axis_spec, cards=cards)
    report_dict = report.to_dict()
    report_dict["axis_vectors"] = axis_vectors
    n_vectors = len(total_hits_values)
    hit_count = sum(1 for v in total_hits_values if v > 0)
    hit_rate = (float(hit_count) / float(n_vectors)) if n_vectors > 0 else 0.0
    mean_total_hits = (
        float(sum(total_hits_values)) / float(n_vectors) if n_vectors > 0 else 0.0
    )
    report_dict["axis_scoring_diagnostics"] = {
        "n_vectors": n_vectors,
        "hit_rate": hit_rate,
        "mean_total_hits": mean_total_hits,
        "warn_no_signal": hit_rate < 0.3,
    }
    return report_dict


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

    # Emit ExplanationChain for observability (Phase 3)
    if variant == "main":
        try:
            explanation = build_explanation_from_verdict(v, stage="action")
            tracer.emit(
                TraceEvent.now(
                    "ExplanationEmitted",
                    ctx.request_id,
                    explanation.to_dict(),
                )
            )
        except Exception as exc:
            # Explanation failure must not break the pipeline, but silent
            # swallowing hides observability gaps — emit a structured failure
            # event so downstream consumers can detect and alert on it.
            logger.exception(
                "Failed to emit ExplanationEmitted for action gate verdict",
                extra={
                    "request_id": ctx.request_id,
                    "stage": "action",
                    "variant": variant,
                    "decision": v.decision.value,
                    "error_type": type(exc).__name__,
                },
            )
            tracer.emit(
                TraceEvent.now(
                    "ExplanationEmitFailed",
                    ctx.request_id,
                    {
                        "stage": "action",
                        "variant": variant,
                        "decision": v.decision.value,
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    },
                )
            )

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


def _apply_case_signals(
    result: Dict[str, Any],
    signals: CaseSignals,
) -> tuple[Dict[str, Any], list[str]]:
    """Overlay CaseSignals semantics onto the run_turn result dict.

    Only modifies the result when signals indicate a non-default case:
    - values_present=False → primary proposal action_type overridden to 'clarify'
    - has_constraint_conflict=True → 'constraint_conflict': True added to result

    Returns:
        (modified_result, applied_changes) where applied_changes is a list of
        human-readable descriptions of mutations made (empty when no mutation).
    """
    changes: list[str] = []
    proposal = result.get("proposal")
    if isinstance(proposal, dict) and not signals.values_present:
        before = proposal.get("action_type", "")
        result = {**result, "proposal": {**proposal, "action_type": "clarify"}}
        changes.append(f"action_type:{before}->clarify")
    if signals.has_constraint_conflict:
        result = {**result, "constraint_conflict": True}
        changes.append("constraint_conflict:true")
    return result, changes


def run_turn(
    ctx: DomainContext,
    deps: EnsembleDeps,
    *,
    case_signals: Optional[CaseSignals] = None,
) -> Dict[str, Any]:
    """
    Run a single turn through the full pipeline (synchronous).

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
        case_signals: Optional structured semantic signals from the calling
            layer (e.g. StubComposer).  When provided, the result dict is
            post-processed to surface values-clarification and
            constraint-conflict signals that the pipeline cannot infer from
            plain-text user_input alone.

    Returns:
        Result dictionary with status, proposal, or verdict
    """
    pre = _run_phase_pre(ctx, deps, case_signals=case_signals)
    if isinstance(pre, dict):
        return pre  # Early exit (intention gate blocked)

    ph_proposals, run_results = run_philosophers(
        pre.philosophers,
        ctx,
        pre.intent,
        pre.tensors,
        pre.memory,
        max_workers=pre.max_workers,
        timeout_s=pre.timeout_s,
        execution_mode=deps.settings.philosopher_execution_mode,
    )
    result = _run_phase_post(ctx, deps, pre, ph_proposals, run_results)
    if case_signals is not None:
        _action_type_before = (result.get("proposal") or {}).get("action_type", "")
        result, _changes = _apply_case_signals(result, case_signals)
        if _changes:
            deps.tracer.emit(
                TraceEvent.now(
                    "CaseSignalsApplied",
                    ctx.request_id,
                    {
                        "values_present": case_signals.values_present,
                        "has_constraint_conflict": case_signals.has_constraint_conflict,
                        "scenario_type": case_signals.scenario_type,
                        "action_type_before": _action_type_before,
                        "action_type_after": (result.get("proposal") or {}).get(
                            "action_type", ""
                        ),
                        "constraint_conflict_added": case_signals.has_constraint_conflict,
                        "applied_changes": _changes,
                    },
                )
            )
    return result


async def async_run_turn(
    ctx: DomainContext,
    deps: EnsembleDeps,
    *,
    case_signals: Optional[CaseSignals] = None,
) -> Dict[str, Any]:
    """
    Async version of run_turn.

    Uses ``async_run_philosophers`` for step 6, which dispatches each
    philosopher's ``propose()`` via ``asyncio.gather`` + thread executors.
    The event loop is freed between philosopher completions, making this
    suitable for the FastAPI SSE endpoint.

    Phases 1-5 and 6.5-10 execute synchronously in the event loop; they are
    fast CPU-bound steps with no IO.

    Args:
        ctx: Request context
        deps: Injected dependencies
        case_signals: Optional structured semantic signals; see ``run_turn``.

    Returns:
        Result dictionary with status, proposal, or verdict
    """
    pre = _run_phase_pre(ctx, deps, case_signals=case_signals)
    if isinstance(pre, dict):
        return pre  # Early exit (intention gate blocked)

    ph_proposals, run_results = await async_run_philosophers(
        pre.philosophers,
        ctx,
        pre.intent,
        pre.tensors,
        pre.memory,
        max_workers=pre.max_workers,
        timeout_s=pre.timeout_s,
        tracer=deps.tracer,
        execution_mode=deps.settings.philosopher_execution_mode,
    )
    result = _run_phase_post(ctx, deps, pre, ph_proposals, run_results)
    if case_signals is not None:
        _action_type_before = (result.get("proposal") or {}).get("action_type", "")
        result, _changes = _apply_case_signals(result, case_signals)
        if _changes:
            deps.tracer.emit(
                TraceEvent.now(
                    "CaseSignalsApplied",
                    ctx.request_id,
                    {
                        "values_present": case_signals.values_present,
                        "has_constraint_conflict": case_signals.has_constraint_conflict,
                        "scenario_type": case_signals.scenario_type,
                        "action_type_before": _action_type_before,
                        "action_type_after": (result.get("proposal") or {}).get(
                            "action_type", ""
                        ),
                        "constraint_conflict_added": case_signals.has_constraint_conflict,
                        "applied_changes": _changes,
                    },
                )
            )
    return result


__all__ = [
    "PHILOSOPHER_REGISTRY",
    "DEFAULT_PHILOSOPHERS",
    # Hexagonal architecture
    "EnsembleDeps",
    "run_turn",
    "async_run_turn",
]
