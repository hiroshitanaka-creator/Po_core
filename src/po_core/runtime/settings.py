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

    # 実験→本番の切替
    use_experimental_solarwill: bool = False

    # SafetyMode（単一真実）- SolarWillとGateが同じ閾値を見る
    freedom_pressure_warn: float = 0.60
    freedom_pressure_critical: float = 0.85
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

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "enable_solarwill": self.enable_solarwill,
            "enable_intention_gate": self.enable_intention_gate,
            "enable_action_gate": self.enable_action_gate,
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
        }


__all__ = ["Settings"]
