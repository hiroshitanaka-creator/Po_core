"""
Dependency Wiring
=================

Assembles concrete implementations and provides dependency injection.

This is the ONLY file that should:
1. Import concrete implementations from adapters/
2. Create instances with specific configurations
3. Wire dependencies together

Core modules receive dependencies as parameters, not through imports.

IMPORTANT: wiring.py 以外で adapter/具象を import し始めたら、即スパゲッティ再発。

Usage:
    from po_core.runtime.wiring import build_system

    system = build_system(memory=poself_instance, settings=Settings())
    result = system.memory_read.snapshot(ctx)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Sequence

from po_core.philosophers.base import PhilosopherProtocol
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.ports.aggregator import AggregatorPort
from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryWritePort
from po_core.ports.solarwill import SolarWillPort
from po_core.ports.tensor_engine import TensorEnginePort
from po_core.ports.trace import TracePort
from po_core.ports.wethics_gate import WethicsGatePort
from po_core.runtime.settings import Settings


@dataclass(frozen=True)
class WiredSystem:
    """
    Wired dependency container.

    Contains all dependencies needed for the vertical slice pipeline.
    """

    memory_read: MemoryReadPort
    memory_write: MemoryWritePort
    tracer: TracePort
    tensor_engine: TensorEnginePort
    solarwill: SolarWillPort
    gate: WethicsGatePort
    philosophers: Sequence[PhilosopherProtocol]  # Backward compat
    aggregator: AggregatorPort
    aggregator_shadow: AggregatorPort | None  # Shadow Pareto A/B評価用
    settings: Settings
    registry: PhilosopherRegistry  # SafetyMode-based selection
    shadow_guard: object | None  # ShadowGuard (自律ブレーキ)


def build_system(*, memory: object, settings: Settings) -> WiredSystem:
    """
    Build a wired system with all dependencies.

    Args:
        memory: Po_self などの具象（adapterで包む）
        settings: Application settings

    Returns:
        WiredSystem with all dependencies wired
    """
    from po_core.adapters.memory_poself import PoSelfMemoryAdapter
    from po_core.aggregator.pareto import ParetoAggregator
    from po_core.autonomy.solarwill.engine import SolarWillEngine
    from po_core.domain.pareto_config import ParetoConfig
    from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
    from po_core.runtime.battalion_table import load_battalion_table
    from po_core.runtime.pareto_table import load_pareto_table
    from po_core.safety.wethics_gate.action_gate import PolicyActionGate
    from po_core.safety.wethics_gate.intention_gate import PolicyIntentionGate
    from po_core.safety.wethics_gate.policies.presets import (
        default_action_policies,
        default_intention_policies,
    )
    from po_core.safety.wethics_gate.policy_gate import PolicyWethicsGate
    from po_core.tensors.engine import TensorEngine
    from po_core.tensors.metrics.blocked_tensor import metric_blocked_tensor
    from po_core.tensors.metrics.freedom_pressure import metric_freedom_pressure
    from po_core.tensors.metrics.interaction_tensor import metric_interaction_tensor
    from po_core.tensors.metrics.semantic_delta import metric_semantic_delta
    from po_core.trace.noop import NoopTracer

    mem = PoSelfMemoryAdapter(memory)

    # SafetyModeConfig (単一真実 - Settingsから構築)
    safety_config = SafetyModeConfig(
        warn=settings.freedom_pressure_warn,
        critical=settings.freedom_pressure_critical,
        missing_mode=settings.freedom_pressure_missing_mode,
    )

    # Battalion Table (外部設定 - 優先)
    table_path = os.getenv(
        "PO_CORE_BATTALION_TABLE", "02_architecture/philosophy/battalion_table.yaml"
    )
    battalion_plans = None
    if os.path.exists(table_path):
        try:
            battalion_plans = load_battalion_table(table_path)
        except Exception:
            pass  # フォールバックで内蔵デフォルトを使う

    # Pareto Table (外部設定 - 優先)
    pareto_path = os.getenv(
        "PO_CORE_PARETO_TABLE", "02_architecture/philosophy/pareto_table.yaml"
    )
    pareto_cfg = ParetoConfig.defaults()
    if os.path.exists(pareto_path):
        try:
            pareto_cfg = load_pareto_table(pareto_path)
        except Exception:
            pass  # フォールバックでデフォルトを使う

    # Shadow Pareto Table (A/B評価用 - オプショナル)
    aggregator_shadow = None
    shadow_cfg = None
    if settings.enable_pareto_shadow:
        shadow_path = os.getenv("PO_CORE_PARETO_SHADOW_TABLE", "")
        if shadow_path and os.path.exists(shadow_path):
            try:
                shadow_cfg = load_pareto_table(shadow_path)
                aggregator_shadow = ParetoAggregator(
                    mode_config=safety_config, config=shadow_cfg
                )
            except Exception:
                pass  # Shadow失敗は無視（main だけで動く）

    # Shadow Guard (自律ブレーキ)
    shadow_guard = None
    if (
        settings.enable_pareto_shadow
        and aggregator_shadow is not None
        and settings.enable_shadow_guard
    ):
        from po_core.runtime.shadow_guard import (
            FileShadowGuardStore,
            ShadowGuard,
            ShadowGuardConfig,
        )

        store = FileShadowGuardStore(settings.shadow_guard_state_path)
        disable_pairs = (
            (("answer", "refuse"),)
            if settings.shadow_guard_disable_answer_to_refuse
            else ()
        )

        guard_cfg = ShadowGuardConfig(
            enabled=True,
            policy_score_drop_threshold=settings.shadow_guard_policy_score_drop_threshold,
            min_shadow_policy_score=settings.shadow_guard_min_shadow_policy_score,
            max_bad_streak=settings.shadow_guard_max_bad_streak,
            cooldown_s=settings.shadow_guard_cooldown_s,
            disable_action_pairs=disable_pairs,
            disable_on_override_increase=settings.shadow_guard_disable_on_override_increase,
        )

        shadow_guard = ShadowGuard(
            guard_cfg,
            store,
            shadow_config_version=str(shadow_cfg.version) if shadow_cfg else "0",
            shadow_config_source=str(shadow_cfg.source) if shadow_cfg else "unknown",
        )

    # PhilosopherRegistry (SafetyModeに応じた編成制御 + cost budget)
    registry = PhilosopherRegistry(
        max_normal=settings.philosophers_max_normal,
        max_warn=settings.philosophers_max_warn,
        max_critical=settings.philosophers_max_critical,
        budget_normal=settings.philosopher_cost_budget_normal,
        budget_warn=settings.philosopher_cost_budget_warn,
        budget_critical=settings.philosopher_cost_budget_critical,
        battalion_plans=battalion_plans,
    )

    return WiredSystem(
        memory_read=mem,
        memory_write=mem,
        tracer=NoopTracer(),
        tensor_engine=TensorEngine(
            metrics=(
                metric_freedom_pressure,
                metric_semantic_delta,
                metric_blocked_tensor,
                metric_interaction_tensor,
            )
        ),
        solarwill=SolarWillEngine(config=safety_config),
        gate=PolicyWethicsGate(
            intention=PolicyIntentionGate(policies=default_intention_policies()),
            action=PolicyActionGate(policies=default_action_policies()),
        ),
        philosophers=registry.select_and_load(SafetyMode.NORMAL),  # Backward compat
        aggregator=ParetoAggregator(mode_config=safety_config, config=pareto_cfg),
        aggregator_shadow=aggregator_shadow,
        settings=settings,
        registry=registry,
        shadow_guard=shadow_guard,
    )


def build_test_system(settings: Settings | None = None) -> WiredSystem:
    """
    Build a wired system for testing (uses in-memory adapters).

    Args:
        settings: Optional settings override

    Returns:
        WiredSystem with in-memory implementations
    """
    from po_core.adapters.memory_poself import InMemoryAdapter
    from po_core.aggregator.pareto import ParetoAggregator
    from po_core.autonomy.solarwill.engine import SolarWillEngine
    from po_core.domain.pareto_config import ParetoConfig
    from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
    from po_core.runtime.battalion_table import load_battalion_table
    from po_core.runtime.pareto_table import load_pareto_table
    from po_core.safety.wethics_gate.action_gate import PolicyActionGate
    from po_core.safety.wethics_gate.intention_gate import PolicyIntentionGate
    from po_core.safety.wethics_gate.policies.presets import (
        default_action_policies,
        default_intention_policies,
    )
    from po_core.safety.wethics_gate.policy_gate import PolicyWethicsGate
    from po_core.tensors.engine import TensorEngine
    from po_core.tensors.metrics.blocked_tensor import metric_blocked_tensor
    from po_core.tensors.metrics.freedom_pressure import metric_freedom_pressure
    from po_core.tensors.metrics.interaction_tensor import metric_interaction_tensor
    from po_core.tensors.metrics.semantic_delta import metric_semantic_delta
    from po_core.trace.in_memory import InMemoryTracer

    settings = settings or Settings()
    mem = InMemoryAdapter()

    # SafetyModeConfig (単一真実 - Settingsから構築)
    safety_config = SafetyModeConfig(
        warn=settings.freedom_pressure_warn,
        critical=settings.freedom_pressure_critical,
        missing_mode=settings.freedom_pressure_missing_mode,
    )

    # Battalion Table (外部設定 - 優先)
    table_path = os.getenv(
        "PO_CORE_BATTALION_TABLE", "02_architecture/philosophy/battalion_table.yaml"
    )
    battalion_plans = None
    if os.path.exists(table_path):
        try:
            battalion_plans = load_battalion_table(table_path)
        except Exception:
            pass  # フォールバックで内蔵デフォルトを使う

    # Pareto Table (外部設定 - 優先)
    pareto_path = os.getenv(
        "PO_CORE_PARETO_TABLE", "02_architecture/philosophy/pareto_table.yaml"
    )
    pareto_cfg = ParetoConfig.defaults()
    if os.path.exists(pareto_path):
        try:
            pareto_cfg = load_pareto_table(pareto_path)
        except Exception:
            pass  # フォールバックでデフォルトを使う

    # Shadow Pareto Table (A/B評価用 - オプショナル)
    aggregator_shadow = None
    shadow_cfg = None
    if settings.enable_pareto_shadow:
        shadow_path = os.getenv("PO_CORE_PARETO_SHADOW_TABLE", "")
        if shadow_path and os.path.exists(shadow_path):
            try:
                shadow_cfg = load_pareto_table(shadow_path)
                aggregator_shadow = ParetoAggregator(
                    mode_config=safety_config, config=shadow_cfg
                )
            except Exception:
                pass  # Shadow失敗は無視（main だけで動く）

    # Shadow Guard (自律ブレーキ) - テスト用はInMemoryStore
    shadow_guard = None
    if (
        settings.enable_pareto_shadow
        and aggregator_shadow is not None
        and settings.enable_shadow_guard
    ):
        from po_core.runtime.shadow_guard import (
            InMemoryShadowGuardStore,
            ShadowGuard,
            ShadowGuardConfig,
        )

        store = InMemoryShadowGuardStore()
        disable_pairs = (
            (("answer", "refuse"),)
            if settings.shadow_guard_disable_answer_to_refuse
            else ()
        )

        guard_cfg = ShadowGuardConfig(
            enabled=True,
            policy_score_drop_threshold=settings.shadow_guard_policy_score_drop_threshold,
            min_shadow_policy_score=settings.shadow_guard_min_shadow_policy_score,
            max_bad_streak=settings.shadow_guard_max_bad_streak,
            cooldown_s=settings.shadow_guard_cooldown_s,
            disable_action_pairs=disable_pairs,
            disable_on_override_increase=settings.shadow_guard_disable_on_override_increase,
        )

        shadow_guard = ShadowGuard(
            guard_cfg,
            store,
            shadow_config_version=str(shadow_cfg.version) if shadow_cfg else "0",
            shadow_config_source=str(shadow_cfg.source) if shadow_cfg else "unknown",
        )

    # PhilosopherRegistry (SafetyModeに応じた編成制御 + cost budget)
    registry = PhilosopherRegistry(
        max_normal=settings.philosophers_max_normal,
        max_warn=settings.philosophers_max_warn,
        max_critical=settings.philosophers_max_critical,
        budget_normal=settings.philosopher_cost_budget_normal,
        budget_warn=settings.philosopher_cost_budget_warn,
        budget_critical=settings.philosopher_cost_budget_critical,
        battalion_plans=battalion_plans,
    )

    return WiredSystem(
        memory_read=mem,
        memory_write=mem,
        tracer=InMemoryTracer(),
        tensor_engine=TensorEngine(
            metrics=(
                metric_freedom_pressure,
                metric_semantic_delta,
                metric_blocked_tensor,
                metric_interaction_tensor,
            )
        ),
        solarwill=SolarWillEngine(config=safety_config),
        gate=PolicyWethicsGate(
            intention=PolicyIntentionGate(policies=default_intention_policies()),
            action=PolicyActionGate(policies=default_action_policies()),
        ),
        philosophers=registry.select_and_load(SafetyMode.NORMAL),  # Backward compat
        aggregator=ParetoAggregator(mode_config=safety_config, config=pareto_cfg),
        aggregator_shadow=aggregator_shadow,
        settings=settings,
        registry=registry,
        shadow_guard=shadow_guard,
    )


__all__ = [
    "WiredSystem",
    "build_system",
    "build_test_system",
]
