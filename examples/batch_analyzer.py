#!/usr/bin/env python3
"""
Po_core Batch Analyzer
======================

Batch processing tool for analyzing multiple questions and comparing philosopher responses.

複数の質問を一括処理し、哲学者の応答を比較分析するツール

Features:
- Batch process 10+ questions
- Export results to JSON/CSV formats
- Statistical analysis (average metrics, leader distribution)
- Progress tracking
- Customizable philosopher groups

Usage:
    python examples/batch_analyzer.py
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, asdict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from po_core import __version__
from po_core.po_self import PoSelf

console = Console()


@dataclass
class AnalysisResult:
    """
    Analysis result for a single prompt.

    単一プロンプトの分析結果
    """

    prompt: str
    consensus_leader: str
    metrics: Dict[str, float]
    philosopher_count: int
    response_length: int


@dataclass
class BatchAnalysisReport:
    """
    Comprehensive report for batch analysis.

    バッチ分析の包括的レポート
    """

    total_prompts: int
    total_philosophers_used: int
    average_metrics: Dict[str, float]
    leader_distribution: Dict[str, int]
    results: List[AnalysisResult]
    created_at: str


class BatchAnalyzer:
    """バッチ分析エンジン"""

    def __init__(self, philosophers: List[str] = None):
        """
        初期化

        Args:
            philosophers: 使用する哲学者のリスト
        """
        self.po = PoSelf(philosophers=philosophers)
        self.results: List[AnalysisResult] = []

    def analyze_prompt(self, prompt: str) -> AnalysisResult:
        """
        単一のプロンプトを分析

        Args:
            prompt: 質問

        Returns:
            分析結果
        """
        response = self.po.generate(prompt)

        result = AnalysisResult(
            prompt=prompt,
            consensus_leader=response.consensus_leader or "Unknown",
            metrics=response.metrics,
            philosopher_count=len(response.philosophers),
            response_length=len(response.text),
        )

        self.results.append(result)
        return result

    def analyze_batch(
        self, prompts: List[str], show_progress: bool = True
    ) -> List[AnalysisResult]:
        """
        複数のプロンプトをバッチ分析

        Args:
            prompts: 質問のリスト
            show_progress: 進捗を表示するか

        Returns:
            分析結果のリスト
        """
        results = []

        if show_progress:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    f"[cyan]Analyzing {len(prompts)} prompts...", total=len(prompts)
                )

                for prompt in prompts:
                    result = self.analyze_prompt(prompt)
                    results.append(result)
                    progress.update(task, advance=1)
        else:
            for prompt in prompts:
                result = self.analyze_prompt(prompt)
                results.append(result)

        return results

    def generate_report(self) -> BatchAnalysisReport:
        """
        分析レポートを生成

        Returns:
            バッチ分析レポート
        """
        if not self.results:
            return BatchAnalysisReport(
                total_prompts=0,
                total_philosophers_used=0,
                average_metrics={},
                leader_distribution={},
                results=[],
                created_at=datetime.utcnow().isoformat() + "Z",
            )

        # 平均メトリクスを計算
        total_metrics = {
            "freedom_pressure": 0.0,
            "semantic_delta": 0.0,
            "blocked_tensor": 0.0,
        }

        for result in self.results:
            for key in total_metrics:
                total_metrics[key] += result.metrics.get(key, 0.0)

        average_metrics = {
            key: round(value / len(self.results), 2)
            for key, value in total_metrics.items()
        }

        # リーダー分布を計算
        leader_distribution = {}
        for result in self.results:
            leader = result.consensus_leader
            leader_distribution[leader] = leader_distribution.get(leader, 0) + 1

        # ユニークな哲学者の数
        all_philosophers = set()
        for result in self.results:
            all_philosophers.add(result.consensus_leader)

        return BatchAnalysisReport(
            total_prompts=len(self.results),
            total_philosophers_used=len(all_philosophers),
            average_metrics=average_metrics,
            leader_distribution=leader_distribution,
            results=self.results,
            created_at=datetime.utcnow().isoformat() + "Z",
        )

    def print_summary(self):
        """サマリーを表示"""
        report = self.generate_report()

        console.print("\n")
        console.print(
            Panel(
                f"[bold cyan]Batch Analysis Summary[/bold cyan]\n\n"
                f"Total Prompts: {report.total_prompts}\n"
                f"Philosophers Used: {report.total_philosophers_used}\n"
                f"Created: {report.created_at}",
                border_style="cyan",
            )
        )

        # 平均メトリクス
        metrics_table = Table(title="Average Metrics")
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="magenta")

        for key, value in report.average_metrics.items():
            metrics_table.add_row(key, f"{value:.2f}")

        console.print(metrics_table)

        # リーダー分布
        console.print("\n")
        leader_table = Table(title="Consensus Leader Distribution")
        leader_table.add_column("Philosopher", style="cyan")
        leader_table.add_column("Count", style="magenta")
        leader_table.add_column("Percentage", style="green")

        for leader, count in sorted(
            report.leader_distribution.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / report.total_prompts) * 100
            leader_table.add_row(leader, str(count), f"{percentage:.1f}%")

        console.print(leader_table)

    def export_json(self, filepath: str):
        """
        結果をJSON形式でエクスポート

        Args:
            filepath: 出力ファイルパス
        """
        report = self.generate_report()

        # dataclassを辞書に変換
        report_dict = {
            "total_prompts": report.total_prompts,
            "total_philosophers_used": report.total_philosophers_used,
            "average_metrics": report.average_metrics,
            "leader_distribution": report.leader_distribution,
            "results": [asdict(r) for r in report.results],
            "created_at": report.created_at,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)

        console.print(f"\n[green]✓ Exported to {filepath}[/green]")

    def export_csv(self, filepath: str):
        """
        結果をCSV形式でエクスポート

        Args:
            filepath: 出力ファイルパス
        """
        import csv

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # ヘッダー
            writer.writerow(
                [
                    "Prompt",
                    "Consensus Leader",
                    "Freedom Pressure",
                    "Semantic Delta",
                    "Blocked Tensor",
                    "Philosopher Count",
                    "Response Length",
                ]
            )

            # データ
            for result in self.results:
                writer.writerow(
                    [
                        result.prompt,
                        result.consensus_leader,
                        result.metrics["freedom_pressure"],
                        result.metrics["semantic_delta"],
                        result.metrics["blocked_tensor"],
                        result.philosopher_count,
                        result.response_length,
                    ]
                )

        console.print(f"\n[green]✓ Exported to {filepath}[/green]")


def load_prompts_from_file(filepath: str) -> List[str]:
    """
    ファイルから質問を読み込む（1行1質問）

    Args:
        filepath: ファイルパス

    Returns:
        質問のリスト
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    """メイン実行関数"""
    console.print("\n" + "=" * 70, style="bold blue")
    console.print("🐷🎈 Po_core Batch Analyzer", style="bold blue", justify="center")
    console.print(f"Version: {__version__}", style="dim", justify="center")
    console.print("=" * 70 + "\n", style="bold blue")

    # デモ質問セット
    demo_prompts = [
        "真の自由とは何か？",
        "正義とは何か？",
        "美とは何か？",
        "愛とは何か？",
        "幸福とは何か？",
        "知識とは何か？",
        "道徳とは何か？",
        "真理とは何か？",
        "善とは何か？",
        "悪とは何か？",
    ]

    console.print("[bold]デモモード: 10個の哲学的問いを分析[/bold]\n")

    # バッチ分析を実行
    analyzer = BatchAnalyzer()
    analyzer.analyze_batch(demo_prompts, show_progress=True)

    # サマリーを表示
    analyzer.print_summary()

    # 結果をエクスポート
    output_dir = Path("batch_analysis_results")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"analysis_{timestamp}.json"
    csv_path = output_dir / f"analysis_{timestamp}.csv"

    analyzer.export_json(str(json_path))
    analyzer.export_csv(str(csv_path))

    console.print("\n" + "=" * 70 + "\n", style="bold blue")


if __name__ == "__main__":
    main()
