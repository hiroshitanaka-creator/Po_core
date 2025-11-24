"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

import json
from typing import Any, Dict, Optional

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__
from po_core.po_self import PoSelf
from po_core.po_trace import PoTrace

console = Console()


def _build_services() -> Dict[str, Any]:
    tracer = PoTrace()
    engine = PoSelf(tracer=tracer)
    return {"tracer": tracer, "engine": engine}


@click.group()
@click.pass_context
@click.version_option(version="0.1.0-alpha", prog_name="po-core")
def main(ctx: click.Context) -> None:
    """Po_core: Philosophy-Driven AI System 🐷🎈"""

    ctx.ensure_object(dict)
    if not ctx.obj:
        ctx.obj.update(_build_services())


@main.command()
def hello() -> None:
    """Say hello from Po_core"""
    console.print("[bold blue]🐷🎈 Po_core へようこそ![/bold blue]")
    console.print("Philosophy-Driven AI System - Alpha v0.1.0")
    console.print("\n[italic]A frog in a well may not know the ocean, but it can know the sky.[/italic]")


@main.command()
def status() -> None:
    """Show project status"""
    tracer = PoTrace()
    philosopher_count = len(PoSelf._default_philosophers())
    trace_count = len(tracer.list_traces())
    table = Table(title="📊 Po_core Project Status", show_lines=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value")
    table.add_row("Philosophers implemented", str(philosopher_count))
    table.add_row("Recorded traces", str(trace_count))
    table.add_row("CLI commands", str(len(main.commands)))
    table.add_row("Trace store", str(tracer.path))
    console.print(table)


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
@click.option("--context", "context_input", default=None, help="JSON payload providing additional context")
@click.pass_context
def run(ctx: click.Context, prompt: str, context_input: Optional[str]) -> None:
    """Execute the PoSelf ensemble on PROMPT."""

    context: Dict[str, Any] = {}
    if context_input:
        try:
            context = json.loads(context_input)
            if not isinstance(context, dict):
                raise ValueError
        except Exception as exc:  # noqa: BLE001
            raise click.BadParameter("--context must be valid JSON object") from exc

    engine: PoSelf = ctx.obj["engine"]
    result = engine.run(prompt, context)

    console.print(f"[bold magenta]Prompt:[/bold magenta] {prompt}\n")
    console.print("[bold]Aggregate reasoning[/bold]")
    console.print(result["reasoning"])

    table = Table(title="Perspectives", show_lines=True)
    table.add_column("Philosopher", style="cyan")
    table.add_column("Perspective")
    table.add_column("Reasoning")
    for perspective in result["perspectives"]:
        table.add_row(perspective["name"], perspective["perspective"], perspective["reasoning"])
    console.print(table)

    if result["tensions"]:
        tensions_table = Table(title="Tensions", show_lines=True)
        tensions_table.add_column("Source")
        tensions_table.add_column("Tension")
        for tension in result["tensions"]:
            tensions_table.add_row(tension["source"], tension["tension"])
        console.print(tensions_table)


@main.group(name="trace")
@click.pass_context
def trace_group(ctx: click.Context) -> None:
    """Trace inspection commands."""

    ctx.ensure_object(dict)


@trace_group.command(name="list")
@click.option("--limit", type=int, default=10, show_default=True, help="Number of traces to display")
@click.pass_context
def trace_list(ctx: click.Context, limit: int) -> None:
    """List recent traces."""

    tracer: PoTrace = ctx.obj.get("tracer") or PoTrace()
    traces = tracer.list_traces(limit=limit)
    if not traces:
        console.print("No traces recorded yet.")
        return

    table = Table(title="Recent traces", show_lines=True)
    table.add_column("Index", justify="right")
    table.add_column("Timestamp")
    table.add_column("Prompt")
    for idx, trace in enumerate(traces):
        table.add_row(str(idx), trace.timestamp, trace.prompt)
    console.print(table)


@trace_group.command(name="show")
@click.argument("index", type=int)
@click.pass_context
def trace_show(ctx: click.Context, index: int) -> None:
    """Show a recorded trace by INDEX."""

    tracer: PoTrace = ctx.obj.get("tracer") or PoTrace()
    trace = tracer.get(index)
    if not trace:
        raise click.BadParameter("Trace not found")

    console.print(f"[bold]Prompt:[/bold] {trace.prompt}")
    console.print(f"[dim]{trace.timestamp}[/dim]\n")
    console.print(trace.result.get("reasoning", ""))


if __name__ == "__main__":
    main()
