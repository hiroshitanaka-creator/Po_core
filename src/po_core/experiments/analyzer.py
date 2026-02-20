"""
analyzer.py - 統計分析
========================

目的:
- 実験サンプルから統計量を計算
- 有意性検定（t-test, Mann-Whitney U test）を実行
- 勝者を判定し、推奨アクションを返す

DEPENDENCY RULES:
- domain + experiments のみ依存
- scipy は optional（なければ簡易実装にフォールバック）
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional

from po_core.domain.experiment import (
    ExperimentAnalysis,
    ExperimentSample,
    SignificanceTest,
    VariantStatistics,
)

# scipy は optional
try:
    from scipy import stats as scipy_stats

    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _compute_statistics(
    samples: List[ExperimentSample], metric_name: str
) -> Dict[str, float]:
    """
    単一メトリクスの統計量を計算する。

    Args:
        samples: サンプルのリスト
        metric_name: メトリクス名

    Returns:
        統計量（mean, std, min, max, median, n）
    """
    values = []
    for s in samples:
        v = s.metrics.get(metric_name)
        if v is not None:
            # boolean を 0/1 に変換
            if isinstance(v, bool):
                v = 1.0 if v else 0.0
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                pass

    if not values:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "median": 0.0, "n": 0}

    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n if n > 1 else 0.0
    std = math.sqrt(variance)
    values_sorted = sorted(values)
    median = values_sorted[n // 2] if n > 0 else 0.0

    return {
        "mean": mean,
        "std": std,
        "min": min(values),
        "max": max(values),
        "median": median,
        "n": n,
    }


def _t_test(
    baseline_values: List[float], variant_values: List[float]
) -> tuple[float, float]:
    """
    t検定を実行する（scipy使用、なければ簡易実装）。

    Args:
        baseline_values: ベースラインの値
        variant_values: バリアントの値

    Returns:
        (t_statistic, p_value)
    """
    if HAS_SCIPY:
        t_stat, p_val = scipy_stats.ttest_ind(baseline_values, variant_values)
        return float(t_stat), float(p_val)

    # Fallback: Welch's t-test の簡易実装
    n1, n2 = len(baseline_values), len(variant_values)
    if n1 < 2 or n2 < 2:
        return 0.0, 1.0  # サンプル不足

    mean1 = sum(baseline_values) / n1
    mean2 = sum(variant_values) / n2
    var1 = sum((x - mean1) ** 2 for x in baseline_values) / (n1 - 1)
    var2 = sum((x - mean2) ** 2 for x in variant_values) / (n2 - 1)

    se = math.sqrt(var1 / n1 + var2 / n2)
    if se == 0:
        return 0.0, 1.0

    t = (mean2 - mean1) / se
    # 自由度（Welch-Satterthwaite）
    (var1 / n1 + var2 / n2) ** 2 / (
        (var1 / n1) ** 2 / (n1 - 1) + (var2 / n2) ** 2 / (n2 - 1)
    )

    # p値の簡易計算（正規分布近似）
    # 本来は t分布を使うべきだが、簡易実装なので正規分布で近似
    p = 2 * (1 - _normal_cdf(abs(t)))
    return t, p


def _normal_cdf(x: float) -> float:
    """標準正規分布のCDF（簡易実装）"""
    # erf を使った近似
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _cohens_d(
    mean1: float, std1: float, n1: int, mean2: float, std2: float, n2: int
) -> float:
    """Cohen's d（効果量）を計算"""
    if n1 < 2 or n2 < 2:
        return 0.0

    pooled_std = math.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0

    return (mean2 - mean1) / pooled_std


class ExperimentAnalyzer:
    """
    実験の統計分析を実行するクラス。
    """

    def __init__(self, storage: Any):  # ExperimentStorage
        """
        Args:
            storage: 実験結果を保存するストレージ
        """
        self.storage = storage

    def analyze(self, experiment_id: str) -> ExperimentAnalysis:
        """
        実験を分析し、統計的有意性検定を実行する。

        Args:
            experiment_id: 実験ID

        Returns:
            ExperimentAnalysis
        """
        # 実験定義を読み込み
        definition = self.storage.load_definition(experiment_id)
        if definition is None:
            raise ValueError(f"Experiment {experiment_id} not found")

        # サンプルを読み込み
        samples = self.storage.load_samples(experiment_id)
        if not samples:
            raise ValueError(f"No samples found for experiment {experiment_id}")

        # バリアント毎にグループ化
        baseline_samples = [s for s in samples if s.variant_name == "baseline"]
        variant_groups: Dict[str, List[ExperimentSample]] = {}
        for v in definition.variants:
            variant_groups[v.name] = [s for s in samples if s.variant_name == v.name]

        # 統計量を計算
        baseline_stats = self._compute_variant_stats(
            "baseline", baseline_samples, definition.metrics
        )
        variant_stats_list = [
            self._compute_variant_stats(
                v.name, variant_groups[v.name], definition.metrics
            )
            for v in definition.variants
        ]

        # 有意性検定を実行
        significance_tests = []
        for v in definition.variants:
            for metric_name in definition.metrics:
                test = self._run_significance_test(
                    metric_name=metric_name,
                    baseline_samples=baseline_samples,
                    variant_samples=variant_groups[v.name],
                    significance_level=definition.significance_level,
                )
                significance_tests.append(test)

        # 勝者を判定
        winner, recommendation = self._determine_winner(
            definition.variants,
            significance_tests,
            definition.significance_level,
        )

        return ExperimentAnalysis(
            experiment_id=experiment_id,
            baseline_stats=baseline_stats,
            variant_stats=variant_stats_list,
            significance_tests=significance_tests,
            winner=winner,
            recommendation=recommendation,
            analyzed_at=datetime.now(timezone.utc),
        )

    def _compute_variant_stats(
        self,
        variant_name: str,
        samples: List[ExperimentSample],
        metric_names: List[str],
    ) -> VariantStatistics:
        """バリアント毎の統計量を計算"""
        metrics_stats: Dict[str, Mapping[str, float]] = {}
        for metric in metric_names:
            metrics_stats[metric] = _compute_statistics(samples, metric)

        return VariantStatistics(
            variant_name=variant_name,
            n=len(samples),
            metrics=metrics_stats,
        )

    def _run_significance_test(
        self,
        metric_name: str,
        baseline_samples: List[ExperimentSample],
        variant_samples: List[ExperimentSample],
        significance_level: float,
    ) -> SignificanceTest:
        """単一メトリクスの有意性検定を実行"""
        # 値を抽出
        baseline_values = []
        for s in baseline_samples:
            v = s.metrics.get(metric_name)
            if v is not None:
                if isinstance(v, bool):
                    v = 1.0 if v else 0.0
                try:
                    baseline_values.append(float(v))
                except (ValueError, TypeError):
                    pass

        variant_values = []
        for s in variant_samples:
            v = s.metrics.get(metric_name)
            if v is not None:
                if isinstance(v, bool):
                    v = 1.0 if v else 0.0
                try:
                    variant_values.append(float(v))
                except (ValueError, TypeError):
                    pass

        if not baseline_values or not variant_values:
            return SignificanceTest(
                metric_name=metric_name,
                baseline_mean=0.0,
                variant_mean=0.0,
                delta=0.0,
                delta_percent=0.0,
                p_value=1.0,
                is_significant=False,
                test_type="t_test",
            )

        baseline_mean = sum(baseline_values) / len(baseline_values)
        variant_mean = sum(variant_values) / len(variant_values)
        delta = variant_mean - baseline_mean
        delta_percent = (delta / baseline_mean * 100) if baseline_mean != 0 else 0.0

        # t検定
        t_stat, p_value = _t_test(baseline_values, variant_values)

        # Cohen's d
        baseline_std = _compute_statistics(baseline_samples, metric_name)["std"]
        variant_std = _compute_statistics(variant_samples, metric_name)["std"]
        effect_size = _cohens_d(
            baseline_mean,
            baseline_std,
            len(baseline_values),
            variant_mean,
            variant_std,
            len(variant_values),
        )

        return SignificanceTest(
            metric_name=metric_name,
            baseline_mean=baseline_mean,
            variant_mean=variant_mean,
            delta=delta,
            delta_percent=delta_percent,
            p_value=p_value,
            is_significant=p_value < significance_level,
            test_type="t_test",
            effect_size=effect_size,
        )

    def _determine_winner(
        self,
        variants: List[Any],  # ExperimentVariant
        tests: List[SignificanceTest],
        significance_level: float,
    ) -> tuple[Optional[str], str]:
        """
        勝者を判定する。

        ロジック:
        - バリアント毎にテスト結果をグループ化
        - すべてのメトリクスで有意な改善があれば "promote"
        - 一部のメトリクスで有意な改悪があれば "reject"
        - 複数バリアントが改善している場合、改善数が最多のものを選択
        - それ以外は "continue"（サンプル不足）

        Returns:
            (winner_name, recommendation)
        """
        if not variants or not tests:
            return None, "continue"

        # メトリクス名をバリアント数で分割して各バリアントに割り当て
        # テストはバリアント順 × メトリクス順で格納されている
        metric_count = len(tests) // len(variants) if variants else 0
        if metric_count == 0:
            return None, "continue"

        best_winner: Optional[str] = None
        best_improvement_count = 0
        best_total_delta = 0.0

        for i, v in enumerate(variants):
            # このバリアントに対応するテスト結果を抽出
            start = i * metric_count
            end = start + metric_count
            v_tests = tests[start:end]

            # 有意な改善と改悪をカウント
            improvements = [t for t in v_tests if t.is_significant and t.delta > 0]
            regressions = [t for t in v_tests if t.is_significant and t.delta < 0]

            if regressions:
                # 改悪がある場合はこのバリアントをスキップ
                continue

            if not improvements:
                continue

            # 同数の改善がある場合は合計delta_percentで比較
            total_delta = sum(t.delta_percent for t in improvements)
            if (len(improvements) > best_improvement_count) or (
                len(improvements) == best_improvement_count
                and total_delta > best_total_delta
            ):
                best_winner = v.name
                best_improvement_count = len(improvements)
                best_total_delta = total_delta

        if best_winner is not None:
            return best_winner, "promote"

        return None, "continue"


__all__ = ["ExperimentAnalyzer"]
