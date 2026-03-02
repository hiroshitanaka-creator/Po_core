from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence

from po_core.adapters.memory_poself import InMemoryAdapter
from po_core.aggregator.pareto import ParetoAggregator
from po_core.autonomy.solarwill.engine import SolarWillEngine
from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.pareto_config import ParetoConfig
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ensemble import EnsembleDeps, run_turn
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.runtime.settings import Settings
from po_core.safety.wethics_gate.action_gate import PolicyActionGate
from po_core.safety.wethics_gate.intention_gate import PolicyIntentionGate
from po_core.safety.wethics_gate.policies.presets import (
    default_action_policies,
    default_intention_policies,
)
from po_core.safety.wethics_gate.policy_gate import PolicyWethicsGate
from po_core.trace.in_memory import InMemoryTracer


class FixedTensorEngine:
    def __init__(self, freedom_pressure: float):
        self._fp = freedom_pressure

    def compute(self, ctx: Context, memory: MemorySnapshot) -> TensorSnapshot:
        return TensorSnapshot.now({"freedom_pressure": self._fp})


def _build_deps(
    *, freedom_pressure: float = 0.0
) -> tuple[EnsembleDeps, InMemoryTracer]:
    settings = Settings()
    mem = InMemoryAdapter()
    tracer = InMemoryTracer()
    safety_config = SafetyModeConfig(
        warn=settings.freedom_pressure_warn,
        critical=settings.freedom_pressure_critical,
        missing_mode=settings.freedom_pressure_missing_mode,
    )
    registry = PhilosopherRegistry(
        max_normal=settings.philosophers_max_normal,
        max_warn=settings.philosophers_max_warn,
        max_critical=settings.philosophers_max_critical,
        budget_normal=settings.philosopher_cost_budget_normal,
        budget_warn=settings.philosopher_cost_budget_warn,
        budget_critical=settings.philosopher_cost_budget_critical,
    )

    deps = EnsembleDeps(
        memory_read=mem,
        memory_write=mem,
        tracer=tracer,
        tensors=FixedTensorEngine(freedom_pressure),
        solarwill=SolarWillEngine(config=safety_config),
        gate=PolicyWethicsGate(
            intention=PolicyIntentionGate(policies=default_intention_policies()),
            action=PolicyActionGate(policies=default_action_policies()),
        ),
        philosophers=registry.select_and_load(SafetyMode.NORMAL),
        aggregator=ParetoAggregator(
            mode_config=safety_config,
            config=ParetoConfig.defaults(),
        ),
        aggregator_shadow=None,
        registry=registry,
        settings=settings,
        shadow_guard=None,
    )
    return deps, tracer


def _make_ctx(user_input: str = "What is justice?") -> Context:
    return Context.now(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        meta={"entry": "test"},
    )


def _walk(obj):
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            yield k, v
            yield from _walk(v)
    elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
        for v in obj:
            yield from _walk(v)


def test_synthesis_report_built_event_is_emitted() -> None:
    deps, tracer = _build_deps(freedom_pressure=0.1)
    run_turn(_make_ctx("Explain tradeoffs for a difficult choice"), deps)

    events = [e for e in tracer.events if e.event_type == "SynthesisReportBuilt"]
    assert len(events) == 1


def test_synthesis_report_built_payload_is_sanitized() -> None:
    deps, tracer = _build_deps(freedom_pressure=0.1)
    run_turn(_make_ctx("Give guidance for an ethical decision"), deps)

    event = next(e for e in tracer.events if e.event_type == "SynthesisReportBuilt")
    payload = event.payload

    allowed_top_level_keys = {
        "axis_name",
        "axis_spec_version",
        "scoreboard",
        "disagreements",
        "stance_distribution",
        "axis_vectors",
    }
    assert set(payload.keys()).issubset(allowed_top_level_keys)

    banned_keys = {"content", "claims", "reasoning", "rationale", "analysis", "text"}
    for k, v in _walk(payload):
        assert k not in banned_keys
        if isinstance(v, str):
            assert len(v) <= 200
