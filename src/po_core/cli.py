"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

import json
from pathlib import Path
from typing import Iterable, Optional

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__, run_ensemble
from po_core.po_self import PoSelfEnsemble
from po_core.po_trace import PoTraceLogger

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


def _format_prompt_output(data: dict, *, keys: Iterable[str]) -> str:
    """Render a compact text view for prompt results."""

    lines = []
    for key in keys:
        value = data.get(key, "")
        lines.append(f"{key.capitalize()}: {value}")
    return "\n".join(lines)


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
@click.argument("prompt")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="json",
    help="Choose between text or JSON output.",
)
def prompt(prompt: str, output_format: str) -> None:
    """Run the deterministic ensemble against a prompt."""

    result = run_ensemble(prompt)
    if output_format.lower() == "json":
        console.print(json.dumps(result, indent=2))
    else:
        console.print(
            _format_prompt_output(
                result,
                keys=["prompt", "philosophers"],
            )
        )


@main.command()
@click.argument("prompt")
def log(prompt: str) -> None:
    """Display the audit log for a deterministic ensemble run."""

    run_data = run_ensemble(prompt)
    console.print(json.dumps(run_data["log"], indent=2))


@main.command("po-self")
@click.argument("prompt")
@click.option(
    "--show-tensors",
    is_flag=True,
    help="Print philosopher tensor values instead of only the composite score.",
)
@click.option(
    "--log-file",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    default=None,
    help="Optional path to write Po_trace output.",
)
@click.option(
    "--ndjson/--json-log",
    "ndjson",
    default=True,
    help="Choose NDJSON (default) or JSON for trace output.",
)
def po_self(prompt: str, show_tensors: bool, log_file: Optional[str], ndjson: bool) -> None:
    """Run a three-philosopher Po_self inference and optional trace."""

    ensemble = PoSelfEnsemble()
    result = ensemble.infer(prompt)

    logger = PoTraceLogger(path=Path(log_file) if log_file else None, ndjson=ndjson)
    logger.record_prompt(prompt)
    logger.record_tensors(result)
    logger.record_contributions(
        f"{tensor.name} -> {tensor.value}" for tensor in result.philosopher_tensors
    )
    log_path = logger.save()

    if show_tensors:
        table = Table(title="Po_self Tensor Outputs")
        table.add_column("Philosopher", style="bold cyan")
        table.add_column("Value", justify="right")
        table.add_column("Weight", justify="right")
        table.add_column("Notes")
        focus_map = {tensor.name: tensor.description for tensor in result.philosopher_tensors}
        for tensor in result.philosopher_tensors:
            table.add_row(
                tensor.name,
                str(tensor.value),
                str(tensor.metadata.get("weight", "")),
                focus_map.get(tensor.name, ""),
            )
        console.print(table)

    composite = result.composite_tensor
    console.print(
        f"[bold green]Ensemble score:[/bold green] {composite.value}"
        if composite
        else "No composite tensor produced"
    )
    console.print(f"Trace log written to: [italic]{log_path}[/italic]")


if __name__ == "__main__":
    main()
