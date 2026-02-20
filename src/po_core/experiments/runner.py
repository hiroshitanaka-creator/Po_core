"""
runner.py - 実験実行エンジン
==============================

目的:
- 実験定義に基づいて複数のバリアントを評価
- 各バリアントで同一の入力に対してParetoを実行
- メトリクスを収集してストレージに保存

DEPENDENCY RULES:
- domain + experiments のみ依存
- ensemble / runtime は外部から注入
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Protocol

from po_core.domain.experiment import (
    ExperimentDefinition,
    ExperimentSample,
    ExperimentStatus,
)
from po_core.domain.trace_event import TraceEvent
from po_core.experiments.storage import ExperimentStorage


class RunFn(Protocol):
    """実験実行関数のプロトコル。

    config_path を引数として受け取り、結果辞書を返す。
    結果には request_id と events を含むことが期待される。
    """

    def __call__(self, user_input: str, *, config_path: str) -> Dict[str, Any]: ...


def _extract_metrics_from_events(
    events: List[TraceEvent],
    metric_names: List[str],
) -> Dict[str, Any]:
    """
    TraceEvent からメトリクスを抽出する。

    対応メトリクス例:
    - final_action_changed_rate: DecisionComparisonComputed から
    - final_policy_score_delta_avg: DecisionComparisonComputed から
    - gate_override_rate: DecisionEmitted から
    - pareto_front_size: ParetoFrontComputed から
    """
    metrics: Dict[str, Any] = {}

    # DecisionComparisonComputed から差分情報を取得
    cmp_events = [e for e in events if e.event_type == "DecisionComparisonComputed"]
    if cmp_events:
        cmp = cmp_events[-1]  # 最新のみ
        diff = cmp.payload.get("diff", {})

        if "final_action_changed" in metric_names:
            metrics["final_action_changed"] = diff.get("final_action_changed", False)

        if "final_content_changed" in metric_names:
            metrics["final_content_changed"] = diff.get("final_content_changed", False)

        if "final_policy_score_delta" in metric_names:
            metrics["final_policy_score_delta"] = diff.get(
                "final_policy_score_delta", 0.0
            )

    # DecisionEmitted から degraded 情報を取得
    de_events = [e for e in events if e.event_type == "DecisionEmitted"]
    if de_events:
        de = de_events[-1]
        if "degraded" in metric_names:
            metrics["degraded"] = de.payload.get("degraded", False)

    # ParetoFrontComputed からフロントサイズを取得
    pf_events = [e for e in events if e.event_type == "ParetoFrontComputed"]
    if pf_events:
        pf = pf_events[-1]
        if "pareto_front_size" in metric_names:
            metrics["pareto_front_size"] = pf.payload.get("front_size", 0)

    return metrics


class ExperimentRunner:
    """
    実験を実行し、サンプルを収集するクラス。

    スレッドセーフ: config_path は run_fn にキーワード引数として渡される。
    os.environ による切り替えは使用しない。

    使い方:
        runner = ExperimentRunner(storage)
        runner.run_experiment(
            definition,
            run_fn=lambda user_input, *, config_path: run_turn(user_input, config_path=config_path),
            inputs=[...],
        )
    """

    def __init__(self, storage: ExperimentStorage) -> None:
        """
        Args:
            storage: 実験結果を保存するストレージ
        """
        self.storage = storage

    def run_experiment(
        self,
        definition: ExperimentDefinition,
        run_fn: Callable[..., Dict[str, Any]],
        inputs: List[str],
        *,
        save_interval: int = 10,
    ) -> None:
        """
        実験を実行する。

        Args:
            definition: 実験定義
            run_fn: 単一リクエストを実行する関数。
                     シグネチャ: (user_input: str, *, config_path: str) -> dict
            inputs: 入力のリスト（user_input文字列）
            save_interval: 進捗表示の間隔

        実装の流れ:
        1. 実験定義を保存
        2. ステータスを RUNNING に更新
        3. 各入力に対して:
           a. baseline を実行
           b. 各 variant を実行
           c. メトリクスを抽出
           d. サンプルを保存
        4. ステータスを COMPLETED に更新
        """
        # 1. 実験定義を保存
        defn_with_timestamp = ExperimentDefinition(
            id=definition.id,
            description=definition.description,
            baseline=definition.baseline,
            variants=definition.variants,
            metrics=definition.metrics,
            sample_size=definition.sample_size,
            significance_level=definition.significance_level,
            status=ExperimentStatus.RUNNING,
            created_at=datetime.now(timezone.utc),
            metadata=definition.metadata,
        )
        self.storage.save_definition(defn_with_timestamp)

        samples_collected = 0
        target_samples = min(definition.sample_size, len(inputs))

        try:
            for i, user_input in enumerate(inputs[:target_samples]):
                # Baseline 実行
                baseline_sample = self._run_single_variant(
                    experiment_id=definition.id,
                    variant_name="baseline",
                    config_path=definition.baseline.config_path,
                    user_input=user_input,
                    run_fn=run_fn,
                    metric_names=definition.metrics,
                )
                self.storage.append_sample(definition.id, baseline_sample)

                # Variants 実行
                for variant in definition.variants:
                    variant_sample = self._run_single_variant(
                        experiment_id=definition.id,
                        variant_name=variant.name,
                        config_path=variant.config_path,
                        user_input=user_input,
                        run_fn=run_fn,
                        metric_names=definition.metrics,
                    )
                    self.storage.append_sample(definition.id, variant_sample)

                samples_collected += 1

                # 定期的に進捗を表示
                if (i + 1) % save_interval == 0:
                    print(
                        f"[{definition.id}] {i + 1}/{target_samples} samples collected"
                    )

            # 4. ステータスを COMPLETED に更新
            self.storage.update_status(definition.id, ExperimentStatus.COMPLETED)
            print(
                f"[{definition.id}] Experiment completed: {samples_collected} samples"
            )

        except Exception as e:
            # 失敗時はステータスを FAILED に更新
            self.storage.update_status(definition.id, ExperimentStatus.FAILED)
            raise RuntimeError(f"Experiment {definition.id} failed: {e}") from e

    def _run_single_variant(
        self,
        *,
        experiment_id: str,
        variant_name: str,
        config_path: str,
        user_input: str,
        run_fn: Callable[..., Dict[str, Any]],
        metric_names: List[str],
    ) -> ExperimentSample:
        """
        単一バリアントで1回実行し、サンプルを生成する。

        config_path は run_fn にキーワード引数として渡す（スレッドセーフ）。
        """
        # config_path を run_fn にキーワード引数として渡す
        result = run_fn(user_input, config_path=config_path)

        # TraceEvent からメトリクスを抽出
        events = result.get("events", [])
        metrics = _extract_metrics_from_events(events, metric_names)

        return ExperimentSample(
            request_id=result.get(
                "request_id",
                f"{experiment_id}_{variant_name}_{datetime.now().timestamp()}",
            ),
            variant_name=variant_name,
            metrics=metrics,
            timestamp=datetime.now(timezone.utc),
            metadata={"user_input": user_input, "config_path": config_path},
        )


__all__ = ["ExperimentRunner"]
