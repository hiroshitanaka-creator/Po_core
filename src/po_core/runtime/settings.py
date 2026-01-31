"""
Runtime Settings
================

Configuration and feature flags for Po_core.

実験→本番の切替はここに閉じ込める（入口やcoreが分岐すると死ぬ）。

DEPENDENCY RULES:
- This file depends ONLY on: stdlib
- No imports from other po_core modules
"""

from __future__ import annotations

from dataclasses import dataclass


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

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "enable_solarwill": self.enable_solarwill,
            "enable_intention_gate": self.enable_intention_gate,
            "enable_action_gate": self.enable_action_gate,
            "use_experimental_solarwill": self.use_experimental_solarwill,
        }


__all__ = ["Settings"]
