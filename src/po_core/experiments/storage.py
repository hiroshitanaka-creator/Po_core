"""
storage.py - 実験結果の永続化
================================

目的:
- 実験サンプルをJSON Lines形式で保存
- 実験定義と分析結果を保存
- ファイルベースの簡易ストレージ（SQLiteへの移行も容易）

DEPENDENCY RULES:
- domain のみ依存
- stdlib のみ使用（外部DBライブラリ不要）
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from po_core.domain.experiment import (
    ExperimentAnalysis,
    ExperimentDefinition,
    ExperimentSample,
    ExperimentStatus,
    ExperimentVariant,
    SignificanceTest,
    VariantStatistics,
)


class ExperimentStorage:
    """
    実験結果の永続化を担当するクラス。

    スレッドセーフ: 内部で threading.Lock を使用し、
    複数スレッドからの同時書き込みを保護する。

    ファイル構造:
        experiments/
          results/
            {experiment_id}/
              definition.json       # 実験定義
              samples.jsonl         # サンプル（JSON Lines）
              analysis.json         # 分析結果（最新）
              analysis_history/     # 分析履歴
                {timestamp}.json
    """

    def __init__(self, base_dir: str = "experiments/results"):
        """
        Args:
            base_dir: 実験結果の保存先ディレクトリ
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _exp_dir(self, experiment_id: str) -> Path:
        """実験IDに対応するディレクトリパスを返す"""
        return self.base_dir / experiment_id

    def _ensure_exp_dir(self, experiment_id: str) -> Path:
        """実験ディレクトリを作成（存在しなければ）"""
        d = self._exp_dir(experiment_id)
        d.mkdir(parents=True, exist_ok=True)
        (d / "analysis_history").mkdir(exist_ok=True)
        return d

    # ── ExperimentDefinition ────────────────────────────────────────────

    def save_definition(self, definition: ExperimentDefinition) -> None:
        """実験定義を保存（スレッドセーフ）"""
        d = self._ensure_exp_dir(definition.id)
        path = d / "definition.json"
        with self._lock:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(definition.to_dict(), f, indent=2, ensure_ascii=False)

    def load_definition(self, experiment_id: str) -> Optional[ExperimentDefinition]:
        """実験定義を読み込み"""
        path = self._exp_dir(experiment_id) / "definition.json"
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Reconstruct from dict
        baseline = ExperimentVariant(**data["baseline"])
        variants = [ExperimentVariant(**v) for v in data["variants"]]
        created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None

        return ExperimentDefinition(
            id=data["id"],
            description=data["description"],
            baseline=baseline,
            variants=variants,
            metrics=data["metrics"],
            sample_size=data.get("sample_size", 100),
            significance_level=data.get("significance_level", 0.05),
            status=ExperimentStatus(data.get("status", "pending")),
            created_at=created_at,
            metadata=data.get("metadata", {}),
        )

    def update_status(self, experiment_id: str, status: ExperimentStatus) -> None:
        """実験のステータスを更新"""
        defn = self.load_definition(experiment_id)
        if defn is None:
            raise ValueError(f"Experiment {experiment_id} not found")

        updated = ExperimentDefinition(
            id=defn.id,
            description=defn.description,
            baseline=defn.baseline,
            variants=defn.variants,
            metrics=defn.metrics,
            sample_size=defn.sample_size,
            significance_level=defn.significance_level,
            status=status,
            created_at=defn.created_at,
            metadata=defn.metadata,
        )
        self.save_definition(updated)

    # ── ExperimentSample ────────────────────────────────────────────────

    def append_sample(self, experiment_id: str, sample: ExperimentSample) -> None:
        """サンプルを追加（JSON Lines形式で追記、スレッドセーフ）"""
        d = self._ensure_exp_dir(experiment_id)
        path = d / "samples.jsonl"
        with self._lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(sample.to_dict(), ensure_ascii=False) + "\n")

    def append_samples(self, experiment_id: str, samples: Iterable[ExperimentSample]) -> None:
        """複数のサンプルを一括追加（スレッドセーフ）"""
        d = self._ensure_exp_dir(experiment_id)
        path = d / "samples.jsonl"
        with self._lock:
            with open(path, "a", encoding="utf-8") as f:
                for s in samples:
                    f.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")

    def load_samples(self, experiment_id: str) -> List[ExperimentSample]:
        """全サンプルを読み込み"""
        path = self._exp_dir(experiment_id) / "samples.jsonl"
        if not path.exists():
            return []

        samples = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                samples.append(ExperimentSample(
                    request_id=data["request_id"],
                    variant_name=data["variant_name"],
                    metrics=data["metrics"],
                    timestamp=datetime.fromisoformat(data["timestamp"]),
                    metadata=data.get("metadata", {}),
                ))
        return samples

    def count_samples(self, experiment_id: str, variant_name: Optional[str] = None) -> int:
        """サンプル数をカウント（variant指定可）"""
        samples = self.load_samples(experiment_id)
        if variant_name is None:
            return len(samples)
        return sum(1 for s in samples if s.variant_name == variant_name)

    # ── ExperimentAnalysis ──────────────────────────────────────────────

    def save_analysis(self, analysis: ExperimentAnalysis) -> None:
        """分析結果を保存（最新 + 履歴、スレッドセーフ）"""
        d = self._ensure_exp_dir(analysis.experiment_id)

        data = analysis.to_dict()
        with self._lock:
            # 最新の分析結果
            path_latest = d / "analysis.json"
            with open(path_latest, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # 履歴にも保存
            ts = analysis.analyzed_at or datetime.now()
            ts_str = ts.strftime("%Y%m%d_%H%M%S")
            path_history = d / "analysis_history" / f"{ts_str}.json"
            with open(path_history, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def load_analysis(self, experiment_id: str) -> Optional[ExperimentAnalysis]:
        """最新の分析結果を読み込み（完全なドメインオブジェクトを再構築）"""
        path = self._exp_dir(experiment_id) / "analysis.json"
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # VariantStatistics を再構築
        baseline_stats = _reconstruct_variant_statistics(data["baseline_stats"])
        variant_stats = [
            _reconstruct_variant_statistics(vs)
            for vs in data.get("variant_stats", [])
        ]

        # SignificanceTest を再構築
        significance_tests = [
            SignificanceTest(
                metric_name=t["metric_name"],
                baseline_mean=t["baseline_mean"],
                variant_mean=t["variant_mean"],
                delta=t["delta"],
                delta_percent=t["delta_percent"],
                p_value=t["p_value"],
                is_significant=t["is_significant"],
                test_type=t["test_type"],
                effect_size=t.get("effect_size"),
            )
            for t in data.get("significance_tests", [])
        ]

        # analyzed_at を再構築
        analyzed_at = None
        if data.get("analyzed_at"):
            analyzed_at = datetime.fromisoformat(data["analyzed_at"])

        return ExperimentAnalysis(
            experiment_id=data["experiment_id"],
            baseline_stats=baseline_stats,
            variant_stats=variant_stats,
            significance_tests=significance_tests,
            winner=data.get("winner"),
            recommendation=data.get("recommendation", "continue"),
            analyzed_at=analyzed_at,
            metadata=data.get("metadata", {}),
        )

    def list_experiments(self) -> List[str]:
        """実験IDの一覧を返す"""
        if not self.base_dir.exists():
            return []
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]


def _reconstruct_variant_statistics(data: Dict[str, Any]) -> VariantStatistics:
    """JSON dict から VariantStatistics を再構築する"""
    return VariantStatistics(
        variant_name=data["variant_name"],
        n=data["n"],
        metrics={k: dict(v) for k, v in data["metrics"].items()},
    )


__all__ = ["ExperimentStorage"]
