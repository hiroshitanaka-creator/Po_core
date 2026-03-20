"""
Runtime Settings
================

Configuration and feature flags for Po_core.

実験→本番の切替はここに閉じ込める（入口やcoreが分岐すると死ぬ）。

DEPENDENCY RULES:
- This file depends ONLY on: stdlib, domain layer
- No imports from ports/adapters/runtime
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, Protocol

from po_core.deliberation.roles import Role, parse_roles_csv
from po_core.domain.safety_mode import SafetyMode


class APISettingsLike(Protocol):
    enable_solarwill: bool
    enable_intention_gate: bool
    enable_action_gate: bool
    enable_pareto_shadow: bool
    use_freedom_pressure_v2: bool
    deliberation_max_rounds: int
    philosopher_roles: str
    enable_llm_philosophers: bool
    llm_provider: str
    llm_model: str
    llm_timeout_s: float
    philosopher_cost_budget_normal: int
    philosopher_cost_budget_warn: int
    philosopher_cost_budget_critical: int
    philosophers_max_normal: int
    philosophers_max_warn: int
    philosophers_max_critical: int
    philosopher_execution_mode: str


def _read_roles_from_env() -> tuple[Role, ...]:
    raw = os.getenv("PO_ROLES", "").strip()
    if not raw:
        return ()
    return tuple(sorted(parse_roles_csv(raw), key=lambda r: r.value))


def _env_first(*keys: str, default: str = "") -> str:
    """Return first non-empty env value from keys, else default."""
    for key in keys:
        value = os.getenv(key)
        if value is not None and value.strip() != "":
            return value
    return default


def _env_bool(*keys: str, default: bool) -> bool:
    raw = _env_first(*keys, default="")
    if raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(*keys: str, default: int) -> int:
    return int(_env_first(*keys, default=str(default)))


def _env_float(*keys: str, default: float) -> float:
    return float(_env_first(*keys, default=str(default)))


def _env_execution_mode(*keys: str, default: str) -> Literal["thread", "process"]:
    raw = _env_first(*keys, default=default).strip().lower()
    if raw not in {"thread", "process"}:
        return default  # type: ignore[return-value]
    return raw  # type: ignore[return-value]


@dataclass(frozen=True)
class Settings:
    """
    Po_core settings (immutable).

    実験→本番の切替はここに閉じ込める（入口やcoreが分岐すると死ぬ）
    """

    enable_solarwill: bool = True
    enable_intention_gate: bool = True
    enable_action_gate: bool = True
    enable_pareto_shadow: bool = False  # Shadow Pareto A/B評価

    # 実験→本番の切替
    use_experimental_solarwill: bool = False

    # ---- Phase 6-A: FreedomPressureV2 (ML-native テンソル) ----
    # False = FreedomPressureTensor v1 (keyword-based, 後退互換)
    # True  = FreedomPressureV2 (embedding-based, ML-native)
    # 環境変数: PO_FREEDOM_PRESSURE_V2=true
    use_freedom_pressure_v2: bool = False

    # ---- Shadow Guard (自律ブレーキ) ----
    enable_shadow_guard: bool = True
    shadow_guard_state_path: str = ".po_core/shadow_guard_state.json"

    shadow_guard_policy_score_drop_threshold: float = 0.15
    shadow_guard_min_shadow_policy_score: float = 0.0
    shadow_guard_max_bad_streak: int = 2
    shadow_guard_cooldown_s: float = 3600.0

    shadow_guard_disable_answer_to_refuse: bool = True
    shadow_guard_disable_on_override_increase: bool = True

    # SafetyMode（単一真実）- SolarWillとGateが同じ閾値を見る
    freedom_pressure_warn: float = 0.30
    freedom_pressure_critical: float = 0.50
    freedom_pressure_missing_mode: SafetyMode = SafetyMode.WARN

    # Philosopher Swarm 制御（増殖の蛇口）
    philosophers_max_normal: int = 42
    philosophers_max_warn: int = 5
    philosophers_max_critical: int = 1

    # Role-based filtering (voice names are labels; role is the operational unit)
    philosopher_roles: tuple[Role, ...] = ()

    philosopher_workers_normal: int = 12
    philosopher_workers_warn: int = 6
    philosopher_workers_critical: int = 2

    philosopher_timeout_s_normal: float = 1.2
    philosopher_timeout_s_warn: float = 0.8
    philosopher_timeout_s_critical: float = 0.5

    philosopher_cost_budget_normal: int = 80
    philosopher_cost_budget_warn: int = 12
    philosopher_cost_budget_critical: int = 3

    # Philosopher execution backend: thread (compat) | process (hard timeout)
    philosopher_execution_mode: Literal["thread", "process"] = "thread"

    # ---- LLM Philosopher Integration ----
    enable_llm_philosophers: bool = False
    llm_provider: str = "gemini"
    llm_model: str = ""
    llm_timeout_s: float = 10.0

    # ---- Deliberation Engine (Phase 2) ----
    deliberation_max_rounds: int = 2
    deliberation_top_k_pairs: int = 5
    deliberation_prompt_mode: str = "debate"
    deliberation_mode: str = "standard"
    deliberation_cluster_positions: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings with environment variable overrides."""
        return cls(
            enable_solarwill=_env_bool("PO_ENABLE_SOLARWILL", default=True),
            enable_intention_gate=_env_bool("PO_ENABLE_INTENTION_GATE", default=True),
            enable_action_gate=_env_bool("PO_ENABLE_ACTION_GATE", default=True),
            enable_pareto_shadow=_env_bool("PO_ENABLE_PARETO_SHADOW", default=False),
            use_freedom_pressure_v2=_env_bool("PO_FREEDOM_PRESSURE_V2", default=False),
            philosopher_roles=_read_roles_from_env(),
            philosophers_max_normal=_env_int("PO_PHILOSOPHERS_MAX_NORMAL", default=42),
            philosophers_max_warn=_env_int("PO_PHILOSOPHERS_MAX_WARN", default=5),
            philosophers_max_critical=_env_int(
                "PO_PHILOSOPHERS_MAX_CRITICAL", default=1
            ),
            philosopher_cost_budget_normal=_env_int(
                "PO_PHILOSOPHER_COST_BUDGET_NORMAL", default=80
            ),
            philosopher_cost_budget_warn=_env_int(
                "PO_PHILOSOPHER_COST_BUDGET_WARN", default=12
            ),
            philosopher_cost_budget_critical=_env_int(
                "PO_PHILOSOPHER_COST_BUDGET_CRITICAL", default=3
            ),
            philosopher_execution_mode=_env_execution_mode(
                "PO_PHILOSOPHER_EXECUTION_MODE", default="thread"
            ),
            enable_llm_philosophers=_env_bool(
                "PO_LLM_ENABLED", "PO_ENABLE_LLM_PHILOSOPHERS", default=False
            ),
            llm_provider=_env_first("PO_LLM_PROVIDER", default="gemini").strip(),
            llm_model=_env_first("PO_LLM_MODEL", default="").strip(),
            llm_timeout_s=_env_float(
                "PO_LLM_TIMEOUT", "PO_LLM_TIMEOUT_S", default=10.0
            ),
            deliberation_max_rounds=_env_int("PO_DELIBERATION_MAX_ROUNDS", default=2),
        )

    @classmethod
    def from_api_settings(cls, api_settings: APISettingsLike) -> "Settings":
        """Build core settings from REST/API-facing settings."""
        return cls(
            enable_solarwill=api_settings.enable_solarwill,
            enable_intention_gate=api_settings.enable_intention_gate,
            enable_action_gate=api_settings.enable_action_gate,
            enable_pareto_shadow=api_settings.enable_pareto_shadow,
            use_freedom_pressure_v2=api_settings.use_freedom_pressure_v2,
            philosopher_roles=(
                tuple(
                    sorted(
                        parse_roles_csv(api_settings.philosopher_roles),
                        key=lambda r: r.value,
                    )
                )
                if api_settings.philosopher_roles.strip()
                else ()
            ),
            philosophers_max_normal=api_settings.philosophers_max_normal,
            philosophers_max_warn=api_settings.philosophers_max_warn,
            philosophers_max_critical=api_settings.philosophers_max_critical,
            philosopher_cost_budget_normal=api_settings.philosopher_cost_budget_normal,
            philosopher_cost_budget_warn=api_settings.philosopher_cost_budget_warn,
            philosopher_cost_budget_critical=api_settings.philosopher_cost_budget_critical,
            philosopher_execution_mode=_env_execution_mode(
                default=getattr(api_settings, "philosopher_execution_mode", "thread")
            ),
            enable_llm_philosophers=api_settings.enable_llm_philosophers,
            llm_provider=api_settings.llm_provider,
            llm_model=api_settings.llm_model,
            llm_timeout_s=api_settings.llm_timeout_s,
            deliberation_max_rounds=api_settings.deliberation_max_rounds,
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "enable_solarwill": self.enable_solarwill,
            "enable_intention_gate": self.enable_intention_gate,
            "enable_action_gate": self.enable_action_gate,
            "enable_pareto_shadow": self.enable_pareto_shadow,
            "use_experimental_solarwill": self.use_experimental_solarwill,
            "freedom_pressure_warn": self.freedom_pressure_warn,
            "freedom_pressure_critical": self.freedom_pressure_critical,
            "freedom_pressure_missing_mode": self.freedom_pressure_missing_mode.value,
            "philosophers_max_normal": self.philosophers_max_normal,
            "philosophers_max_warn": self.philosophers_max_warn,
            "philosophers_max_critical": self.philosophers_max_critical,
            "philosopher_workers_normal": self.philosopher_workers_normal,
            "philosopher_workers_warn": self.philosopher_workers_warn,
            "philosopher_workers_critical": self.philosopher_workers_critical,
            "philosopher_timeout_s_normal": self.philosopher_timeout_s_normal,
            "philosopher_timeout_s_warn": self.philosopher_timeout_s_warn,
            "philosopher_timeout_s_critical": self.philosopher_timeout_s_critical,
            "philosopher_cost_budget_normal": self.philosopher_cost_budget_normal,
            "philosopher_cost_budget_warn": self.philosopher_cost_budget_warn,
            "philosopher_cost_budget_critical": self.philosopher_cost_budget_critical,
            "philosopher_roles": [r.value for r in self.philosopher_roles],
            "philosopher_execution_mode": self.philosopher_execution_mode,
            "enable_llm_philosophers": self.enable_llm_philosophers,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "llm_timeout_s": self.llm_timeout_s,
            "deliberation_max_rounds": self.deliberation_max_rounds,
            "deliberation_top_k_pairs": self.deliberation_top_k_pairs,
            "deliberation_prompt_mode": self.deliberation_prompt_mode,
            "deliberation_mode": self.deliberation_mode,
            "deliberation_cluster_positions": self.deliberation_cluster_positions,
            "use_freedom_pressure_v2": self.use_freedom_pressure_v2,
        }


__all__ = ["APISettingsLike", "Settings"]
