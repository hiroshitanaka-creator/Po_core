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

from dataclasses import dataclass

from po_core.domain.safety_mode import SafetyMode


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
    # Calibrated for normalized FP range [0.0, ~0.44]:
    #   NORMAL < 0.30 → 39 philosophers (most prompts)
    #   WARN 0.30-0.50 → 5 philosophers (ethically dense prompts)
    #   CRITICAL > 0.50 → 1 philosopher (extreme + memory boost)
    freedom_pressure_warn: float = 0.30
    freedom_pressure_critical: float = 0.50
    freedom_pressure_missing_mode: SafetyMode = SafetyMode.WARN

    # Philosopher Swarm 制御（増殖の蛇口）
    # 動員数: mode別の最大哲学者数
    philosophers_max_normal: int = 39
    philosophers_max_warn: int = 5
    philosophers_max_critical: int = 1

    # 並列数: mode別のworker数
    philosopher_workers_normal: int = 12
    philosopher_workers_warn: int = 6
    philosopher_workers_critical: int = 2

    # タイムアウト: mode別の秒数
    philosopher_timeout_s_normal: float = 1.2
    philosopher_timeout_s_warn: float = 0.8
    philosopher_timeout_s_critical: float = 0.5

    # コスト予算: mode別の総コスト上限（重い哲学者混入防止）
    philosopher_cost_budget_normal: int = 80
    philosopher_cost_budget_warn: int = 12
    philosopher_cost_budget_critical: int = 3

    # ---- Deliberation Engine (Phase 2) ----
    # 1 = no deliberation (backward compatible), 2+ = multi-round
    deliberation_max_rounds: int = 2
    deliberation_top_k_pairs: int = 5
    # "basic" = legacy soft counterargument
    # "debate" = structured rebuttal with steelman + flaw + defense (Phase 6-A)
    deliberation_prompt_mode: str = "debate"
    # "standard" = current multi-round deliberation (rounds are homogeneous)
    # "dialectic" = Hegelian 3-round: Thesis → Antithesis → Synthesis (Phase 6-B)
    deliberation_mode: str = "standard"
    # Phase 6-C1: cluster philosophers by position after round 1
    # False = off (default, backward compatible)
    # True  = PositionClusterer runs; result in DeliberationResult.cluster_result
    deliberation_cluster_positions: bool = False

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
            "deliberation_max_rounds": self.deliberation_max_rounds,
            "deliberation_top_k_pairs": self.deliberation_top_k_pairs,
            "deliberation_prompt_mode": self.deliberation_prompt_mode,
            "deliberation_mode": self.deliberation_mode,
            "deliberation_cluster_positions": self.deliberation_cluster_positions,
            "use_freedom_pressure_v2": self.use_freedom_pressure_v2,
        }


__all__ = ["Settings"]
