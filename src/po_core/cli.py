"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

import json
from typing import Any, Dict, Iterable, Tuple

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__
from po_core.po_self import PoSelf

console = Console()


def _parse_key_value_pairs(entries: Iterable[str]) -> Dict[str, Any]:
    context: Dict[str, Any] = {}
    for entry in entries:
        if "=" not in entry:
            continue
        key, value = entry.split("=", 1)
        context[key.strip()] = value.strip()
    return context


@click.group()
@click.version_option(version=__version__, prog_name="po-core")
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    Po_core: Philosophy-Driven AI System 🐷🎈

    A system that integrates philosophers as dynamic tensors
    for responsible meaning generation.
    """
    ctx.ensure_object(dict)
    ctx.obj["engine"] = PoSelf()


@main.command()
@click.pass_context
def hello(ctx: click.Context) -> None:
    """Say hello from Po_core."""

    engine: PoSelf = ctx.obj["engine"]
    console.print("[bold blue]🐷🎈 Po_core へようこそ![/bold blue]")
    console.print(f"Philosophy-Driven AI System - v{__version__}")
    console.print(
        f"\n[italic]Currently hosting {len(engine.philosophers)} philosophers ready to reason.[/italic]"
    )
    console.print("[dim]A frog in a well may not know the ocean, but it can know the sky.[/dim]")


@main.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show project status."""

    engine: PoSelf = ctx.obj["engine"]
    table = Table(title="📊 Po_core Project Status", show_header=False, box=None)
    table.add_row("Philosophers loaded", str(len(engine.philosophers)))
    table.add_row("Available", ", ".join(engine.available_names()))
    table.add_row("Pipeline", "Reasoning orchestrator active")
    table.add_row("Testing", "Ensemble and CLI smoke tests ready")

    console.print(table)


@main.command()
@click.argument("prompt")
@click.option(
    "--philosopher",
    "philosophers",
    multiple=True,
    help="Limit execution to a specific philosopher name. Can be passed multiple times.",
)
@click.option(
    "--context",
    "context_items",
    multiple=True,
    help="Optional context key=value pairs to pass into the ensemble.",
)
@click.option(
    "--output",
    "output_format",
    type=click.Choice(["rich", "json"], case_sensitive=False),
    default="rich",
    show_default=True,
    help="Format to display ensemble results.",
)
@click.pass_context
def run(
    ctx: click.Context,
    prompt: str,
    philosophers: Tuple[str, ...],
    context_items: Tuple[str, ...],
    output_format: str,
) -> None:
    """Run the philosopher ensemble on a prompt."""

    engine: PoSelf = ctx.obj["engine"]
    context = _parse_key_value_pairs(context_items)
    result = engine.run_prompt(prompt, context=context, selected=list(philosophers))

    if output_format.lower() == "json":
        console.print_json(json.dumps(result, default=lambda o: o.__dict__))
        return

    console.print(f"\n[bold]Prompt:[/bold] {prompt}\n")
    console.print(f"[bold cyan]Ensemble summary[/bold cyan]\n{result.summary}\n")

    influence_table = Table(title="Influence Weights", show_header=True, header_style="bold")
    influence_table.add_column("Philosopher")
    influence_table.add_column("Perspective")
    influence_table.add_column("Weight")
    for influence in result.influences:
        influence_table.add_row(
            influence["name"], influence.get("perspective", ""), str(influence["weight"])
        )
    console.print(influence_table)

    for output in result.outputs:
        console.rule(output.name)
        console.print(f"[bold]Perspective:[/bold] {output.perspective}")
        console.print(output.reasoning)

    if result.failed:
        console.print(
            f"\n[bold red]The following philosophers failed to respond:[/bold red] {', '.join(result.failed)}"
        )


@main.command()
def version() -> None:
    """Show version information."""
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


if __name__ == "__main__":
    main()
