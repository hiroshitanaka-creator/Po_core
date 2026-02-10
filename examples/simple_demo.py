#!/usr/bin/env python3
"""
Po_core Simple Prototype Demo
==============================

このデモは、Po_coreの哲学的AIシステムの基本的な動作を示します。
複数の哲学者が問いに対して推論し、アンサンブルとして回答を生成します。
"""

import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from po_core import __version__
from po_core.po_self import PoSelf

console = Console()


def print_header():
    """ヘッダーを表示"""
    console.print("\n" + "=" * 70, style="bold blue")
    console.print(
        "🐷🎈 Po_core - Philosophy-Driven AI Prototype Demo",
        style="bold blue",
        justify="center",
    )
    console.print(f"Version: {__version__}", style="dim", justify="center")
    console.print("=" * 70 + "\n", style="bold blue")
    console.print(
        "[italic]「井の中の蛙、大海は知らずとも、大空を知る」[/italic]\n",
        justify="center",
    )


def demo_single_question(prompt: str, philosophers=None):
    """単一の質問に対する哲学的推論を実行"""

    console.print(Panel(f"[bold cyan]質問:[/bold cyan] {prompt}", border_style="cyan"))

    # Po_selfインスタンスを作成
    po_self = PoSelf(philosophers=philosophers) if philosophers else PoSelf()

    console.print("\n[dim]哲学者たちが推論中...[/dim]\n")

    # 推論を実行
    response = po_self.generate(prompt)

    # 結果を表示
    console.print(
        Panel(
            f"[bold green]コンセンサスリーダー:[/bold green] {response.consensus_leader}\n\n"
            f"[bold yellow]回答:[/bold yellow]\n{response.text[:300]}...",
            title="推論結果",
            border_style="green",
        )
    )

    # メトリクスを表形式で表示
    metrics_table = Table(title="哲学的テンソル・メトリクス")
    metrics_table.add_column("メトリクス", style="cyan")
    metrics_table.add_column("値", style="magenta")

    for key, value in response.metrics.items():
        metrics_table.add_row(key, f"{value:.2f}")

    console.print("\n")
    console.print(metrics_table)

    # 参加哲学者を表示
    console.print(f"\n[bold]参加哲学者:[/bold] {', '.join(response.philosophers)}\n")

    return response


def demo_philosopher_comparison():
    """複数の哲学者の視点を比較するデモ"""

    console.print("\n" + "=" * 70, style="bold magenta")
    console.print(
        "哲学者比較デモ - 異なる視点からの推論", style="bold magenta", justify="center"
    )
    console.print("=" * 70 + "\n", style="bold magenta")

    prompt = "人生の意味とは何か？"

    # 西洋哲学者グループ
    console.print("[bold blue]1. 西洋実存主義グループ[/bold blue]")
    response1 = demo_single_question(
        prompt, philosophers=["sartre", "heidegger", "kierkegaard"]
    )

    console.print("\n" + "-" * 70 + "\n")

    # 東洋哲学者グループ
    console.print("[bold blue]2. 東洋哲学グループ[/bold blue]")
    response2 = demo_single_question(
        prompt, philosophers=["confucius", "zhuangzi", "wabi_sabi"]
    )

    console.print("\n" + "-" * 70 + "\n")

    # 古典哲学者グループ
    console.print("[bold blue]3. 古典哲学グループ[/bold blue]")
    response3 = demo_single_question(
        prompt, philosophers=["aristotle", "nietzsche", "wittgenstein"]
    )

    # メトリクス比較
    console.print("\n" + "=" * 70 + "\n", style="bold magenta")
    console.print("[bold magenta]メトリクス比較[/bold magenta]\n")

    comparison_table = Table(title="Freedom Pressure Tensor 比較")
    comparison_table.add_column("グループ", style="cyan")
    comparison_table.add_column("Freedom Pressure", style="green")
    comparison_table.add_column("Semantic Delta", style="yellow")
    comparison_table.add_column("Blocked Tensor", style="red")

    comparison_table.add_row(
        "西洋実存主義",
        f"{response1.metrics['freedom_pressure']:.2f}",
        f"{response1.metrics['semantic_delta']:.2f}",
        f"{response1.metrics['blocked_tensor']:.2f}",
    )
    comparison_table.add_row(
        "東洋哲学",
        f"{response2.metrics['freedom_pressure']:.2f}",
        f"{response2.metrics['semantic_delta']:.2f}",
        f"{response2.metrics['blocked_tensor']:.2f}",
    )
    comparison_table.add_row(
        "古典哲学",
        f"{response3.metrics['freedom_pressure']:.2f}",
        f"{response3.metrics['semantic_delta']:.2f}",
        f"{response3.metrics['blocked_tensor']:.2f}",
    )

    console.print(comparison_table)


def demo_interactive_mode():
    """対話型モードのデモ"""

    console.print("\n" + "=" * 70, style="bold green")
    console.print("対話型モード", style="bold green", justify="center")
    console.print("=" * 70 + "\n", style="bold green")

    console.print(
        "[italic]質問を入力してください（終了するには 'quit' または 'exit' を入力）[/italic]\n"
    )

    po_self = PoSelf()

    while True:
        try:
            prompt = console.input("[bold cyan]あなた:[/bold cyan] ")

            if prompt.lower() in ["quit", "exit", "q", "終了"]:
                console.print(
                    "\n[bold blue]🐷🎈 Po_coreをご利用いただきありがとうございました！[/bold blue]\n"
                )
                break

            if not prompt.strip():
                continue

            console.print("\n[dim]推論中...[/dim]\n")
            response = po_self.generate(prompt)

            console.print(
                f"[bold green]Po_core ({response.consensus_leader}):[/bold green]"
            )
            console.print(response.text[:500] + "...\n")
            console.print(
                f"[dim]メトリクス: FP={response.metrics['freedom_pressure']:.2f}, "
                f"SD={response.metrics['semantic_delta']:.2f}, "
                f"BT={response.metrics['blocked_tensor']:.2f}[/dim]\n"
            )

        except KeyboardInterrupt:
            console.print(
                "\n\n[bold blue]🐷🎈 Po_coreをご利用いただきありがとうございました！[/bold blue]\n"
            )
            break
        except Exception as e:
            console.print(f"\n[bold red]エラー:[/bold red] {str(e)}\n")


def main():
    """メインデモ関数"""

    print_header()

    console.print("[bold]デモモードを選択してください:[/bold]\n")
    console.print("1. 基本デモ - 単一の質問")
    console.print("2. 哲学者比較デモ - 複数の視点")
    console.print("3. 対話型モード")
    console.print("4. すべて実行\n")

    try:
        choice = console.input("[bold cyan]選択 (1-4):[/bold cyan] ")

        if choice == "1":
            console.print("\n")
            demo_single_question("真の自由とは何か？")
        elif choice == "2":
            demo_philosopher_comparison()
        elif choice == "3":
            demo_interactive_mode()
        elif choice == "4":
            # 基本デモ
            console.print("\n")
            demo_single_question("真の自由とは何か？")

            # 哲学者比較デモ
            console.print("\n\n")
            demo_philosopher_comparison()

            # 対話型モードは最後に
            console.print("\n\n")
            demo_interactive_mode()
        else:
            console.print("\n[bold red]無効な選択です。[/bold red]\n")

    except KeyboardInterrupt:
        console.print("\n\n[bold blue]🐷🎈 デモを終了しました。[/bold blue]\n")
    except Exception as e:
        console.print(f"\n[bold red]エラーが発生しました:[/bold red] {str(e)}\n")


if __name__ == "__main__":
    main()
