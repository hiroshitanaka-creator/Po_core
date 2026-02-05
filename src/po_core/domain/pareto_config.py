"""
ParetoConfig - Pareto最適化の設定型
===================================

Paretoの重み・チューニングパラメータの"型"をdomainに置いて凍結する。
aggregator/runtime/viewer が同じ言語で握れる。

DEPENDENCY RULES:
- domain のみ依存（SafetyMode）
- 外部設定ファイルから読み込まれる前提
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from po_core.domain.safety_mode import SafetyMode


@dataclass(frozen=True)
class ParetoWeights:
    """Pareto目的関数の重み（SafetyMode毎に異なる）"""
    safety: float
    freedom: float
    explain: float
    brevity: float
    coherence: float

    def to_dict(self) -> dict:
        return {
            "safety": self.safety,
            "freedom": self.freedom,
            "explain": self.explain,
            "brevity": self.brevity,
            "coherence": self.coherence,
        }


@dataclass(frozen=True)
class ParetoTuning:
    """Pareto目的関数のチューニングパラメータ"""
    brevity_max_len: int = 2000
    explain_rationale_weight: float = 0.65
    explain_author_rel_weight: float = 0.35
    front_limit: int = 20


@dataclass(frozen=True)
class ParetoConfig:
    """
    Pareto最適化の完全な設定。

    Attributes:
        weights_by_mode: SafetyMode毎の重み
        tuning: チューニングパラメータ
        version: 設定バージョン（監査用）
        source: 設定ソース（監査用: "defaults" / "file:<path>" / "env"）
    """
    weights_by_mode: Mapping[SafetyMode, ParetoWeights]
    tuning: ParetoTuning = field(default_factory=ParetoTuning)
    version: int = 1
    source: str = "defaults"

    @staticmethod
    def defaults() -> "ParetoConfig":
        """デフォルト設定（外部ファイルがない場合のフォールバック）"""
        return ParetoConfig(
            weights_by_mode={
                SafetyMode.NORMAL: ParetoWeights(0.25, 0.30, 0.20, 0.10, 0.15),
                SafetyMode.WARN: ParetoWeights(0.40, 0.10, 0.20, 0.15, 0.25),
                SafetyMode.CRITICAL: ParetoWeights(0.55, 0.00, 0.20, 0.15, 0.30),
                SafetyMode.UNKNOWN: ParetoWeights(0.40, 0.10, 0.20, 0.15, 0.25),
            },
            tuning=ParetoTuning(),
            version=1,
            source="defaults",
        )


__all__ = ["ParetoWeights", "ParetoTuning", "ParetoConfig"]
