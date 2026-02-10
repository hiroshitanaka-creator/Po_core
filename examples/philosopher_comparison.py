#!/usr/bin/env python3
"""
Po_core Philosopher Comparison Tool
====================================

同じ質問に対する異なる哲学者の視点を比較するツール
"""

import sys
import os
from typing import List, Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

from po_core import __version__
from po_core.po_self import PoSelf

console = Console()


class PhilosopherComparison:
    """哲学者比較ツール"""

    # 哲学者グループの定義
    PHILOSOPHER_GROUPS = {
        "実存主義": ["sartre", "heidegger", "kierkegaard"],
        "古典哲学": ["aristotle", "confucius", "wabi_sabi"],
        "現代哲学": ["wittgenstein", "derrida", "deleuze"],
        "倫理学": ["aristotle", "levinas", "confucius"],
        "現象学": ["heidegger", "merleau_ponty", "sartre"],
        "プラグマティズム": ["dewey", "peirce", "wittgenstein"],
        "精神分析": ["jung", "lacan", "nietzsche"],
        "東洋哲学": ["confucius", "zhuangzi", "watsuji", "wabi_sabi"],
        "西洋哲学": ["aristotle", "nietzsche", "sartre", "wittgenstein"],
        "政治哲学": ["arendt", "confucius", "aristotle"],
    }

    def __init__(self):
        """初期化"""
        self.responses = {}

    def compare_groups(self, prompt: str, groups: List[str] = None):
        """
        複数の哲学者グループの視点を比較

        Args:
            prompt: 質問
            groups: 比較するグループ名のリスト（Noneなら全グループ）
        """
        if groups is None:
            groups = list(self.PHILOSOPHER_GROUPS.keys())

        console.print(
            Panel(f"[bold cyan]Question:[/bold cyan] {prompt}", border_style="cyan")
        )

        self.responses = {}

        # 各グループの応答を取得
        for group_name in groups:
            if group_name not in self.PHILOSOPHER_GROUPS:
                console.print(f"[yellow]Warning: Unknown group '{group_name}'[/yellow]")
                continue

            philosophers = self.PHILOSOPHER_GROUPS[group_name]

            console.print(f"\n[dim]Analyzing from {group_name} perspective...[/dim]")

            po = PoSelf(philosophers=philosophers)
            response = po.generate(prompt)

            self.responses[group_name] = {
                "response": response,
                "philosophers": philosophers,
            }

        # 比較結果を表示
        self._display_comparison_results(prompt)

    def compare_philosophers(self, prompt: str, philosophers: List[str]):
        """
        特定の哲学者の視点を個別比較

        Args:
            prompt: 質問
            philosophers: 哲学者のリスト
        """
        console.print(
            Panel(f"[bold cyan]Question:[/bold cyan] {prompt}", border_style="cyan")
        )

        self.responses = {}

        # 各哲学者の応答を取得
        for philosopher in philosophers:
            console.print(f"\n[dim]Getting {philosopher}'s perspective...[/dim]")

            po = PoSelf(philosophers=[philosopher])
            response = po.generate(prompt)

            self.responses[philosopher] = {
                "response": response,
                "philosophers": [philosopher],
            }

        # 比較結果を表示
        self._display_individual_comparison(prompt)

    def _display_comparison_results(self, prompt: str):
        """グループ比較結果を表示"""
        console.print("\n" + "=" * 70 + "\n")
        console.print("[bold magenta]Comparison Results[/bold magenta]\n")

        # メトリクス比較テーブル
        metrics_table = Table(title="Metrics Comparison")
        metrics_table.add_column("Group", style="cyan")
        metrics_table.add_column("Leader", style="green")
        metrics_table.add_column("FP", style="yellow")
        metrics_table.add_column("SD", style="yellow")
        metrics_table.add_column("BT", style="yellow")

        for group_name, data in self.responses.items():
            response = data["response"]
            metrics = response.metrics

            metrics_table.add_row(
                group_name,
                response.consensus_leader or "Unknown",
                f"{metrics['freedom_pressure']:.2f}",
                f"{metrics['semantic_delta']:.2f}",
                f"{metrics['blocked_tensor']:.2f}",
            )

        console.print(metrics_table)

        # 各グループの応答サマリー
        console.print("\n[bold magenta]Response Summaries[/bold magenta]\n")

        for group_name, data in self.responses.items():
            response = data["response"]
            philosophers = ", ".join(data["philosophers"])

            panel = Panel(
                f"[bold]{response.consensus_leader}[/bold]\n\n"
                f"{response.text[:200]}...\n\n"
                f"[dim]Philosophers: {philosophers}[/dim]",
                title=f"[cyan]{group_name}[/cyan]",
                border_style="blue",
            )
            console.print(panel)

    def _display_individual_comparison(self, prompt: str):
        """個別哲学者比較結果を表示"""
        console.print("\n" + "=" * 70 + "\n")
        console.print(
            "[bold magenta]Individual Philosopher Comparison[/bold magenta]\n"
        )

        # メトリクス比較
        metrics_table = Table(title="Metrics Comparison")
        metrics_table.add_column("Philosopher", style="cyan")
        metrics_table.add_column("FP", style="yellow")
        metrics_table.add_column("SD", style="yellow")
        metrics_table.add_column("BT", style="yellow")
        metrics_table.add_column("Response Length", style="green")

        for philosopher, data in self.responses.items():
            response = data["response"]
            metrics = response.metrics

            metrics_table.add_row(
                philosopher,
                f"{metrics['freedom_pressure']:.2f}",
                f"{metrics['semantic_delta']:.2f}",
                f"{metrics['blocked_tensor']:.2f}",
                str(len(response.text)),
            )

        console.print(metrics_table)

        # 各哲学者の詳細応答
        console.print("\n[bold magenta]Detailed Responses[/bold magenta]\n")

        for philosopher, data in self.responses.items():
            response = data["response"]

            # 哲学者ごとの応答から最初の応答を取得
            if response.responses:
                first_response = response.responses[0]
                reasoning = first_response.get("reasoning", "")
                perspective = first_response.get("perspective", "")

                panel = Panel(
                    f"[bold green]Perspective:[/bold green] {perspective}\n\n"
                    f"[bold yellow]Reasoning:[/bold yellow]\n{reasoning[:300]}...",
                    title=f"[cyan]{philosopher}[/cyan]",
                    border_style="blue",
                )
                console.print(panel)

    def show_available_groups(self):
        """利用可能なグループを表示"""
        console.print("\n[bold cyan]Available Philosopher Groups:[/bold cyan]\n")

        for group_name, philosophers in self.PHILOSOPHER_GROUPS.items():
            console.print(f"  • [green]{group_name}[/green]: {', '.join(philosophers)}")


def demo_group_comparison():
    """グループ比較のデモ"""
    console.print("\n" + "=" * 70, style="bold blue")
    console.print(
        "Demo 1: Philosopher Group Comparison", style="bold blue", justify="center"
    )
    console.print("=" * 70 + "\n", style="bold blue")

    comparison = PhilosopherComparison()

    prompt = "人生の意味とは何か？"
    groups = ["実存主義", "古典哲学", "東洋哲学"]

    comparison.compare_groups(prompt, groups)


def demo_individual_comparison():
    """個別哲学者比較のデモ"""
    console.print("\n" + "=" * 70, style="bold blue")
    console.print(
        "Demo 2: Individual Philosopher Comparison", style="bold blue", justify="center"
    )
    console.print("=" * 70 + "\n", style="bold blue")

    comparison = PhilosopherComparison()

    prompt = "真の自由とは何か？"
    philosophers = ["sartre", "aristotle", "confucius", "nietzsche"]

    comparison.compare_philosophers(prompt, philosophers)


def main():
    """メイン実行関数"""
    console.print("\n" + "=" * 70, style="bold blue")
    console.print(
        "🐷🎈 Po_core Philosopher Comparison Tool", style="bold blue", justify="center"
    )
    console.print(f"Version: {__version__}", style="dim", justify="center")
    console.print("=" * 70 + "\n", style="bold blue")

    console.print("[bold]Select demo mode:[/bold]\n")
    console.print("1. Group Comparison - Compare philosopher groups")
    console.print("2. Individual Comparison - Compare individual philosophers")
    console.print("3. Show Available Groups")
    console.print("4. Run All Demos\n")

    try:
        choice = console.input("[bold cyan]Choice (1-4):[/bold cyan] ")

        if choice == "1":
            demo_group_comparison()
        elif choice == "2":
            demo_individual_comparison()
        elif choice == "3":
            comparison = PhilosopherComparison()
            comparison.show_available_groups()
        elif choice == "4":
            demo_group_comparison()
            console.print("\n\n")
            demo_individual_comparison()

            console.print("\n\n")
            comparison = PhilosopherComparison()
            comparison.show_available_groups()
        else:
            console.print("\n[bold red]Invalid choice.[/bold red]\n")

    except KeyboardInterrupt:
        console.print("\n\n[bold blue]🐷🎈 Comparison tool closed.[/bold blue]\n")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
