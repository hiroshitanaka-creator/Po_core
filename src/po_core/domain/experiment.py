"""
experiment.py - 実験管理のドメインモデル
========================================

目的:
- 実験の定義（manifest）とデータモデル
- 実験結果の型安全な表現
- 統計分析の入力・出力モデル

DEPENDENCY RULES:
- domain のみ依存（stdlib以外は禁止）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Mapping, Optional


class ExperimentStatus(Enum):
    """実験のステータス"""

    PENDING = "pending"  # 未実行
    RUNNING = "running"  # 実行中
    COMPLETED = "completed"  # 完了
    FAILED = "failed"  # 失敗
    ANALYZING = "analyzing"  # 分析中
    PROMOTED = "promoted"  # 勝者が昇格済み


@dataclass(frozen=True)
class ExperimentVariant:
    """実験のバリアント（baseline または treatment）"""

    name: str
    config_path: str
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "config_path": self.config_path,
            "description": self.description,
        }


@dataclass(frozen=True)
class ExperimentDefinition:
    """
    実験の定義（manifest.yaml から読み込まれる）

    Attributes:
        id: 実験ID（一意）
        description: 実験の説明
        baseline: ベースライン設定
        variants: テストするバリアント（複数可）
        metrics: 評価指標のリスト
        sample_size: 必要なサンプル数
        significance_level: 有意水準（デフォルト 0.05）
        status: 実験のステータス
        created_at: 実験作成日時
    """

    id: str
    description: str
    baseline: ExperimentVariant
    variants: List[ExperimentVariant]
    metrics: List[str]
    sample_size: int = 100
    significance_level: float = 0.05
    status: ExperimentStatus = ExperimentStatus.PENDING
    created_at: Optional[datetime] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "baseline": self.baseline.to_dict(),
            "variants": [v.to_dict() for v in self.variants],
            "metrics": list(self.metrics),
            "sample_size": self.sample_size,
            "significance_level": self.significance_level,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ExperimentSample:
    """
    単一リクエストの実験結果

    Attributes:
        request_id: リクエストID
        variant_name: バリアント名（"baseline" or variant名）
        metrics: メトリクス値（metric_name -> value）
        timestamp: サンプル取得時刻
        metadata: その他のメタデータ
    """

    request_id: str
    variant_name: str
    metrics: Mapping[str, Any]
    timestamp: datetime
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "variant_name": self.variant_name,
            "metrics": dict(self.metrics),
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class VariantStatistics:
    """
    バリアント毎の統計量

    Attributes:
        variant_name: バリアント名
        n: サンプル数
        metrics: メトリクス毎の統計（mean, std, min, max, median）
    """

    variant_name: str
    n: int
    metrics: Mapping[str, Mapping[str, float]]

    def to_dict(self) -> dict:
        return {
            "variant_name": self.variant_name,
            "n": self.n,
            "metrics": {k: dict(v) for k, v in self.metrics.items()},
        }


@dataclass(frozen=True)
class SignificanceTest:
    """
    統計的有意性検定の結果

    Attributes:
        metric_name: メトリクス名
        baseline_mean: ベースラインの平均値
        variant_mean: バリアントの平均値
        delta: 差分（variant - baseline）
        delta_percent: 差分の割合（%）
        p_value: p値
        is_significant: 有意かどうか（p < significance_level）
        test_type: 検定の種類（"t_test", "mann_whitney"等）
        effect_size: 効果量（Cohen's d等）
    """

    metric_name: str
    baseline_mean: float
    variant_mean: float
    delta: float
    delta_percent: float
    p_value: float
    is_significant: bool
    test_type: str
    effect_size: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "baseline_mean": self.baseline_mean,
            "variant_mean": self.variant_mean,
            "delta": self.delta,
            "delta_percent": self.delta_percent,
            "p_value": self.p_value,
            "is_significant": self.is_significant,
            "test_type": self.test_type,
            "effect_size": self.effect_size,
        }


@dataclass(frozen=True)
class ExperimentAnalysis:
    """
    実験の分析結果

    Attributes:
        experiment_id: 実験ID
        baseline_stats: ベースラインの統計量
        variant_stats: バリアント毎の統計量
        significance_tests: 有意性検定の結果
        winner: 勝者のバリアント名（有意な改善があれば）
        recommendation: 推奨アクション（"promote", "reject", "continue"）
        analyzed_at: 分析実行時刻
    """

    experiment_id: str
    baseline_stats: VariantStatistics
    variant_stats: List[VariantStatistics]
    significance_tests: List[SignificanceTest]
    winner: Optional[str] = None
    recommendation: str = "continue"  # "promote", "reject", "continue"
    analyzed_at: Optional[datetime] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "experiment_id": self.experiment_id,
            "baseline_stats": self.baseline_stats.to_dict(),
            "variant_stats": [v.to_dict() for v in self.variant_stats],
            "significance_tests": [t.to_dict() for t in self.significance_tests],
            "winner": self.winner,
            "recommendation": self.recommendation,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "metadata": dict(self.metadata),
        }


__all__ = [
    "ExperimentStatus",
    "ExperimentVariant",
    "ExperimentDefinition",
    "ExperimentSample",
    "VariantStatistics",
    "SignificanceTest",
    "ExperimentAnalysis",
]
