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
from typing import Any, Sequence

from po_core.deliberation.roles import parse_roles_csv
from po_core.domain.safety_mode import SafetyMode
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


def _strict_philosopher_startup_enabled() -> bool:
    raw = os.getenv("PO_STRICT_PHILOSOPHER_STARTUP", "true").strip().lower()
    return raw not in {"0", "false", "no"}


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
    deliberation_engine: object | None = None  # DeliberationEngine (Phase 2)


def _maybe_preload_models(settings: Settings) -> None:
    if os.getenv("PO_PRELOAD_MODELS", "").strip() not in {
        "1",
        "true",
        "TRUE",
        "yes",
        "YES",
    }:
        return

    errors: list[str] = []
    try:
        from po_core.tensors.metrics.semantic_delta import (
            preload_models as preload_semantic,
        )

        preload_semantic()
    except Exception as exc:
        errors.append(f"semantic_delta preload failed: {exc}")

    if settings.use_freedom_pressure_v2:
        try:
            from po_core.tensors.freedom_pressure_v2 import (
                preload_model as preload_fpv2,
            )

            preload_fpv2()
        except Exception as exc:
            errors.append(f"freedom_pressure_v2 preload failed: {exc}")

    if errors:
        raise RuntimeError("; ".join(errors))


def _load_battalion_plans_from_env_or_package() -> Any:
    """Load battalion table with explicit env override validation."""

    from po_core.runtime.battalion_table import (
        load_battalion_table,
        load_packaged_battalion_table,
    )

    table_path = os.getenv("PO_CORE_BATTALION_TABLE", "").strip()
    if not table_path:
        return load_packaged_battalion_table()
    if not os.path.exists(table_path):
        raise FileNotFoundError(f"PO_CORE_BATTALION_TABLE not found: {table_path}")
    return load_battalion_table(table_path)


def _overlay_battalion_plans_with_settings(
    battalion_plans: Any, settings: Settings
) -> Any:
    """Overlay Settings/env-driven limit and budget values onto packaged battalion plans."""

    overlays = {
        SafetyMode.NORMAL: (
            settings.philosophers_max_normal,
            settings.philosopher_cost_budget_normal,
        ),
        SafetyMode.WARN: (
            settings.philosophers_max_warn,
            settings.philosopher_cost_budget_warn,
        ),
        SafetyMode.CRITICAL: (
            settings.philosophers_max_critical,
            settings.philosopher_cost_budget_critical,
        ),
        SafetyMode.UNKNOWN: (
            settings.philosophers_max_warn,
            settings.philosopher_cost_budget_warn,
        ),
    }

    out = {}
    for mode, plan in battalion_plans.items():
        limit, cost_budget = overlays.get(mode, (plan.limit, plan.cost_budget))
        out[mode] = type(plan)(
            limit=limit,
            max_risk=plan.max_risk,
            cost_budget=cost_budget,
            require_tags=plan.require_tags,
        )
    return out


def _load_pareto_cfg_from_env_or_package() -> Any:
    """Load pareto table with explicit env override validation."""

    from po_core.runtime.pareto_table import (
        load_packaged_pareto_table,
        load_pareto_table,
    )

    pareto_path = os.getenv("PO_CORE_PARETO_TABLE", "").strip()
    if not pareto_path:
        return load_packaged_pareto_table()
    if not os.path.exists(pareto_path):
        raise FileNotFoundError(f"PO_CORE_PARETO_TABLE not found: {pareto_path}")
    return load_pareto_table(pareto_path)


def _load_optional_shadow_pareto_cfg() -> Any:
    """Load optional shadow pareto table from explicit env path only."""

    from po_core.runtime.pareto_table import load_pareto_table

    shadow_path = os.getenv("PO_CORE_PARETO_SHADOW_TABLE", "").strip()
    if not shadow_path:
        return None
    if not os.path.exists(shadow_path):
        raise FileNotFoundError(
            f"PO_CORE_PARETO_SHADOW_TABLE points to missing file: {shadow_path}"
        )
    return load_pareto_table(shadow_path)


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
    from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
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
    _maybe_preload_models(settings)

    # SafetyModeConfig (単一真実 - Settingsから構築)
    safety_config = SafetyModeConfig(
        warn=settings.freedom_pressure_warn,
        critical=settings.freedom_pressure_critical,
        missing_mode=settings.freedom_pressure_missing_mode,
    )

    # Battalion/Pareto Table (packaged defaults + explicit env override)
    battalion_plans = _overlay_battalion_plans_with_settings(
        _load_battalion_plans_from_env_or_package(), settings
    )
    pareto_cfg = _load_pareto_cfg_from_env_or_package()

    # Shadow Pareto Table (A/B評価用 - オプショナル)
    aggregator_shadow = None
    shadow_cfg = None
    if settings.enable_pareto_shadow:
        shadow_cfg = _load_optional_shadow_pareto_cfg()
        if shadow_cfg is not None:
            aggregator_shadow = ParetoAggregator(
                mode_config=safety_config, config=shadow_cfg
            )

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

    selected_roles = settings.philosopher_roles
    if not selected_roles:
        roles_env = os.getenv("PO_ROLES", "").strip()
        if roles_env:
            selected_roles = tuple(
                sorted(parse_roles_csv(roles_env), key=lambda r: r.value)
            )

    # PhilosopherRegistry (SafetyModeに応じた編成制御 + cost budget)
    if getattr(settings, "enable_llm_philosophers", False):
        from po_core.adapters.llm_adapter import LLMAdapter
        from po_core.philosophers.llm_philosopher import build_llm_philosopher_registry

        llm_adapter = LLMAdapter.from_settings(settings)
        registry = build_llm_philosopher_registry(
            adapter=llm_adapter,
            max_normal=settings.philosophers_max_normal,
            max_warn=settings.philosophers_max_warn,
            max_critical=settings.philosophers_max_critical,
            budget_normal=settings.philosopher_cost_budget_normal,
            budget_warn=settings.philosopher_cost_budget_warn,
            budget_critical=settings.philosopher_cost_budget_critical,
            battalion_plans=battalion_plans,
            required_roles=selected_roles,
        )
    else:
        registry = PhilosopherRegistry(
            max_normal=settings.philosophers_max_normal,
            max_warn=settings.philosophers_max_warn,
            max_critical=settings.philosophers_max_critical,
            budget_normal=settings.philosopher_cost_budget_normal,
            budget_warn=settings.philosopher_cost_budget_warn,
            budget_critical=settings.philosopher_cost_budget_critical,
            battalion_plans=battalion_plans,
            required_roles=selected_roles,
        )

    strict_startup = _strict_philosopher_startup_enabled()
    normal_selection = registry.select(SafetyMode.NORMAL)
    loaded_philosophers, _load_errors = registry.load(
        normal_selection.selected_ids,
        strict_enabled=strict_startup,
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
        philosophers=loaded_philosophers,  # Backward compat
        aggregator=ParetoAggregator(mode_config=safety_config, config=pareto_cfg),
        aggregator_shadow=aggregator_shadow,
        settings=settings,
        registry=registry,
        shadow_guard=shadow_guard,
        deliberation_engine=_build_deliberation_engine(settings),
    )


def build_default_system(settings: Settings | None = None) -> WiredSystem:
    """
    Build the default in-process wired system (in-memory adapters).

    This is the public default for entrypoints that do not receive an external
    memory backend. Historically this function was exposed as
    ``build_test_system``; that alias remains for backward compatibility.

    Args:
        settings: Optional settings override

    Returns:
        WiredSystem with in-memory implementations
    """
    from po_core.adapters.memory_poself import InMemoryAdapter
    from po_core.aggregator.pareto import ParetoAggregator
    from po_core.autonomy.solarwill.engine import SolarWillEngine
    from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
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
    _maybe_preload_models(settings)

    # SafetyModeConfig (単一真実 - Settingsから構築)
    safety_config = SafetyModeConfig(
        warn=settings.freedom_pressure_warn,
        critical=settings.freedom_pressure_critical,
        missing_mode=settings.freedom_pressure_missing_mode,
    )

    # Battalion/Pareto Table (packaged defaults + explicit env override)
    battalion_plans = _overlay_battalion_plans_with_settings(
        _load_battalion_plans_from_env_or_package(), settings
    )
    pareto_cfg = _load_pareto_cfg_from_env_or_package()

    # Shadow Pareto Table (A/B評価用 - オプショナル)
    aggregator_shadow = None
    shadow_cfg = None
    if settings.enable_pareto_shadow:
        shadow_cfg = _load_optional_shadow_pareto_cfg()
        if shadow_cfg is not None:
            aggregator_shadow = ParetoAggregator(
                mode_config=safety_config, config=shadow_cfg
            )

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

    selected_roles = settings.philosopher_roles
    if not selected_roles:
        roles_env = os.getenv("PO_ROLES", "").strip()
        if roles_env:
            selected_roles = tuple(
                sorted(parse_roles_csv(roles_env), key=lambda r: r.value)
            )

    # PhilosopherRegistry (SafetyModeに応じた編成制御 + cost budget)
    if getattr(settings, "enable_llm_philosophers", False):
        from po_core.adapters.llm_adapter import LLMAdapter
        from po_core.philosophers.llm_philosopher import build_llm_philosopher_registry

        llm_adapter = LLMAdapter.from_settings(settings)
        registry = build_llm_philosopher_registry(
            adapter=llm_adapter,
            max_normal=settings.philosophers_max_normal,
            max_warn=settings.philosophers_max_warn,
            max_critical=settings.philosophers_max_critical,
            budget_normal=settings.philosopher_cost_budget_normal,
            budget_warn=settings.philosopher_cost_budget_warn,
            budget_critical=settings.philosopher_cost_budget_critical,
            battalion_plans=battalion_plans,
            required_roles=selected_roles,
        )
    else:
        registry = PhilosopherRegistry(
            max_normal=settings.philosophers_max_normal,
            max_warn=settings.philosophers_max_warn,
            max_critical=settings.philosophers_max_critical,
            budget_normal=settings.philosopher_cost_budget_normal,
            budget_warn=settings.philosopher_cost_budget_warn,
            budget_critical=settings.philosopher_cost_budget_critical,
            battalion_plans=battalion_plans,
            required_roles=selected_roles,
        )

    strict_startup = _strict_philosopher_startup_enabled()
    normal_selection = registry.select(SafetyMode.NORMAL)
    loaded_philosophers, _load_errors = registry.load(
        normal_selection.selected_ids,
        strict_enabled=strict_startup,
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
        philosophers=loaded_philosophers,  # Backward compat
        aggregator=ParetoAggregator(mode_config=safety_config, config=pareto_cfg),
        aggregator_shadow=aggregator_shadow,
        settings=settings,
        registry=registry,
        shadow_guard=shadow_guard,
        deliberation_engine=_build_deliberation_engine(settings),
    )


def _build_deliberation_engine(settings: Settings) -> Any:
    """Build deliberation engine if enabled in settings."""
    max_rounds = getattr(settings, "deliberation_max_rounds", 1)
    if max_rounds <= 1:
        return None
    from po_core.deliberation import DeliberationEngine

    return DeliberationEngine(
        max_rounds=max_rounds,
        top_k_pairs=getattr(settings, "deliberation_top_k_pairs", 5),
        prompt_mode=getattr(settings, "deliberation_prompt_mode", "debate"),
    )


def build_test_system(settings: Settings | None = None) -> WiredSystem:
    """Backward-compatible alias for :func:`build_default_system`."""
    return build_default_system(settings=settings)


__all__ = [
    "WiredSystem",
    "build_system",
    "build_default_system",
    "build_test_system",
]
