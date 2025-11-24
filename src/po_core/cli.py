"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

from pathlib import Path
from typing import Iterable, List

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__
from po_core.po_self import available_philosophers, render_po_self_summary, run_po_self
from po_core.po_trace import log_trace

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="po-core")
def main() -> None:
    """
    Po_core: Philosophy-Driven AI System 🐷🎈

    Orchestrates philosophical ensembles (Po_self) and trace logging (Po_trace)
    for responsible meaning generation.
    """
    pass


@main.command()
def hello() -> None:
    """Say hello from Po_core"""
    console.print("[bold blue]🐷🎈 Po_core へようこそ![/bold blue]")
    console.print("Philosophy-Driven AI System - Alpha v0.1.0")
    console.print("\n[italic]A frog in a well may not know the ocean, but it can know the sky.[/italic]")


def _default_philosophers() -> List[str]:
    """Return the default philosopher selection for the CLI."""

    defaults = ["confucius", "nietzsche", "wittgenstein"]
    return [name for name in defaults if name in available_philosophers()]


@main.command()
@click.option(
    "--prompt",
    "-p",
    required=True,
    help="Prompt to route through the Po_self ensemble.",
)
@click.option(
    "--philosopher",
    "-f",
    multiple=True,
    help="Philosophers to activate (e.g., nietzsche, confucius). Defaults to a curated trio.",
)
@click.option(
    "--log-path",
    "-l",
    type=click.Path(path_type=Path, dir_okay=False),
    default=Path("po_trace.log"),
    show_default=True,
    help="Where to store the Po_trace JSONL log.",
)
def status(prompt: str, philosopher: Iterable[str], log_path: Path) -> None:
    """Route a prompt through Po_self and persist its Po_trace audit."""

    selection = list(philosopher) or _default_philosophers()
    try:
        results = run_po_self(prompt, selection)
    except (KeyError, ValueError) as exc:
        raise click.BadParameter(str(exc)) from exc

    render_po_self_summary(prompt, results)

    trace_path = log_trace(prompt, results, log_path)
    console.print(f"\n[green]🔍 Trace saved to[/green] {trace_path}")


@main.command()
def version() -> None:
    """Show version information"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()

    table.add_row("🐷🎈 Po_core", f"v{__version__} (with Po_self & Po_trace)")
    table.add_row("Author", __author__)
    table.add_row("Email", __email__)
    table.add_row("Philosophy", "Flying Pig - When Pigs Fly")
    table.add_row("Motto", "井の中の蛙、大海は知らずとも、大空を知る")

    console.print("\n")
    console.print(table)
    console.print("\n[dim]A frog in a well may not know the ocean, but it can know the sky.[/dim]")


if __name__ == "__main__":
    main()
