"""Po_viewer: Visualization Module.

Visualizes Po_trace output and summarizes philosopher contributions.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import click
from rich.console import Console
from rich.table import Table

from po_core.po_trace import TraceEvent, load_trace

console = Console()


def summarize_contributions(events: Sequence[TraceEvent]) -> Counter:
    """Summarize how many times each philosopher contributed."""

    counter: Counter[str] = Counter()
    for event in events:
        for philosopher in event.philosophers:
            counter[philosopher] += 1
    return counter


def render_trace_table(events: Sequence[TraceEvent]) -> None:
    """Render a table of individual events."""

    table = Table(title="Trace Events", show_lines=True)
    table.add_column("Philosophers")
    table.add_column("Utterance")
    table.add_column("Accepted", justify="center")
    table.add_column("Rejection Reason")
    table.add_column("Tension", justify="right")

    for event in events:
        table.add_row(
            ", ".join(event.philosophers),
            event.utterance,
            "✅" if event.accepted else "❌",
            event.rejection_reason or "-",
            f"{event.tension:.2f}" if event.tension is not None else "-",
        )

    console.print(table)


def render_summary(counter: Counter, tensions: Iterable[float]) -> None:
    """Render summary tables and a simple sparkline."""

    summary = Table(title="Philosopher Contributions")
    summary.add_column("Philosopher")
    summary.add_column("Events", justify="right")

    for philosopher, count in counter.most_common():
        summary.add_row(philosopher, str(count))

    sparkline = "".join(_spark_char(value) for value in tensions)
    console.print(summary)
    console.print(f"Tension trend: [bold blue]{sparkline}[/bold blue]\n")


def _spark_char(value: float) -> str:
    """Convert a numeric tension into a simple sparkline character."""

    if value < 0.2:
        return "▁"
    if value < 0.4:
        return "▂"
    if value < 0.6:
        return "▃"
    if value < 0.8:
        return "▄"
    return "▅"


@click.command()
@click.option(
    "--trace",
    "trace_path",
    required=True,
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
    help="Path to a Po_trace JSON/JSONL file.",
)
def cli(trace_path: Path) -> None:
    """Visualize a Po_trace file in the terminal."""

    events = load_trace(trace_path)
    if not events:
        console.print("[yellow]No events found in trace.[/yellow]")
        return

    counter = summarize_contributions(events)
    tensions = [event.tension or 0.0 for event in events]

    console.print(f"[bold cyan]🎨 Po_viewer[/bold cyan] loading [cyan]{trace_path}[/cyan]\n")
    render_summary(counter, tensions)
    render_trace_table(events)


__all__ = ["render_trace_table", "render_summary", "summarize_contributions"]

