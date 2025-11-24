"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__
from po_core.po_self import run_ensemble

console = Console()


@click.group()
@click.version_option(version="0.1.0-alpha", prog_name="po-core")
def main() -> None:
    """
    Po_core: Philosophy-Driven AI System 🐷🎈

    A system that integrates philosophers as dynamic tensors
    for responsible meaning generation.
    """
    pass


@main.command()
def hello() -> None:
    """Say hello from Po_core"""
    console.print("[bold blue]🐷🎈 Po_core へようこそ![/bold blue]")
    console.print("Philosophy-Driven AI System - Alpha v0.1.0")
    console.print("\n[italic]A frog in a well may not know the ocean, but it can know the sky.[/italic]")


@main.command()
def status() -> None:
    """Show project status"""
    console.print("[bold]📊 Po_core Project Status[/bold]\n")
    console.print("✅ Philosophical Framework: 100%")
    console.print("✅ Documentation: 100%")
    console.print("✅ Architecture Design: 100%")
    console.print("🔄 Implementation: 30%")
    console.print("⏳ Testing: 0%")
    console.print("⏳ Visualization: 0%")


@main.command()
def version() -> None:
    """Show version information"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()

    table.add_row("🐷🎈 Po_core", f"v{__version__}")
    table.add_row("Author", __author__)
    table.add_row("Email", __email__)
    table.add_row("Philosophy", "Flying Pig - When Pigs Fly")
    table.add_row("Motto", "井の中の蛙、大海は知らずとも、大空を知る")

    console.print("\n")
    console.print(table)
    console.print("\n[dim]A frog in a well may not know the ocean, but it can know the sky.[/dim]")


@main.command()
@click.option("--prompt", required=True, help="Prompt to run through the Po_self ensemble")
def self(prompt: str) -> None:
    """Run Po_self ensemble reasoning."""

    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    result = run_ensemble(prompt)

    console.print("\n[bold]Minimal Response[/bold]")
    console.print(result.response)

    console.print("\n[bold]Design Signals[/bold]")
    console.print(
        f"Freedom Pressure: {result.design_signals.freedom_pressure}\n"
        f"Ethical Resonance: {result.design_signals.ethical_resonance}\n"
        f"Responsibility Pressure: {result.design_signals.responsibility_pressure}\n"
        f"Meaning Profile: {result.design_signals.meaning_profile}"
    )

    console.print("\n[bold]Philosopher Log[/bold]")
    for signal in result.philosopher_signals:
        console.print(f"- {signal.name} (w={result.weights.get(signal.name, 0):.2f}): {signal.reasoning}")


if __name__ == "__main__":
    main()
