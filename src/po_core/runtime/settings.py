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
        }


__all__ = ["Settings"]
