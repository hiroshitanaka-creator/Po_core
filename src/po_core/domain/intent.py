"""
Intent - SolarWillの出力（意図・目標候補）。

philosophersが参照してよい"上位制御"。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Mapping


@dataclass(frozen=True)
class Intent:
    """
    SolarWillの出力（意図・目標候補）。philosophersが参照してよい"上位制御"。

    Attributes:
        goals: List of goal descriptions
        constraints: List of constraints to respect
        weights: Weight mapping for prioritization
    """

    goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

    # 目的の重み（例：autonomyが決める）
    weights: Mapping[str, float] = field(default_factory=dict)

    @staticmethod
    def neutral() -> "Intent":
        """Create a neutral intent with no goals or constraints."""
        return Intent(goals=[], constraints=[], weights={})

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "goals": list(self.goals),
            "constraints": list(self.constraints),
            "weights": dict(self.weights),
        }


__all__ = ["Intent"]
