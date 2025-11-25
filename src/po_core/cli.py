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
from po_core.po_trace import PoTrace
from po_core.po_viewer import render_reason_log

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


@main.command(name="po-trace")
@click.argument("prompt")
@click.option(
    "--output",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Write the Reason Log to a file instead of stdout.",
)
def po_trace(prompt: str, output_path: Optional[Path]) -> None:
    """Generate a Reason Log using Po_trace."""

    run_data = run_ensemble(prompt)
    trace = PoTrace(prompt, run_data.get("philosophers", []))
    for event in run_data["log"].get("events", []):
        trace.record_event(
            event=event.get("event", ""),
            decision=event.get("decision"),
            suppressed=event.get("suppressed", []),
            metadata=event.get("metadata"),
        )

    if output_path:
        trace.stream(output_path)
        console.print(f"Reason Log written to {output_path}")
    else:
        console.print(trace.to_json(indent=2))


@main.command(name="view-log")
@click.option(
    "--file",
    "file_path",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Path to a file containing run data or a Reason Log.",
)
@click.option(
    "--json-input",
    "json_input",
    help="Raw JSON string representing run data or a Reason Log.",
)
def view_log(file_path: Optional[Path], json_input: Optional[str]) -> None:
    """Visualize Reason Log content using Po_viewer."""

    if file_path:
        payload = json.loads(file_path.read_text())
    elif json_input:
        payload = json.loads(json_input)
    else:
        raise click.UsageError("Provide --file or --json-input for view-log")

    render_reason_log(payload, console=console)


if __name__ == "__main__":
    main()
