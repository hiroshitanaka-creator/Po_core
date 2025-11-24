"""
Helpers for presenting trace summaries in the CLI.
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from po_core.po_trace.models import TraceSession


def render_summary(console: Console, session: TraceSession) -> None:
    """Render a compact summary of a trace session."""

    console.print("[bold green]\n🔍 Po_trace - Reasoning Audit Log[/bold green]")
    console.print(f"Session: [bold]{session.session_id}[/bold]")
    console.print(f"Prompt: [italic]{session.prompt}[/italic]\n")

    table = Table(title="Trace Steps", show_lines=True)
    table.add_column("Step", justify="center", style="cyan", no_wrap=True)
    table.add_column("Freedom", justify="center")
    table.add_column("Δ Semantic", justify="center")
    table.add_column("Spoken", overflow="fold")

    for row in session.summary_rows():
        table.add_row(*row)

    console.print(table)
    console.print("\n[dim]Stored a fully structured trace for inspection.[/dim]")


__all__ = ["render_summary"]
