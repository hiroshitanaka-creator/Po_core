"""
Po_viewer: Visualization Module

Visualizes Reason Logs using Rich tables and progress bars.
"""
from __future__ import annotations

import json
from typing import Iterable, Mapping, MutableMapping, Sequence

import click
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

DEFAULT_CONSOLE = Console()


def _extract_log(data: Mapping[str, object]) -> Mapping[str, object]:
    if "log" in data:
        return data["log"]  # type: ignore[return-value]
    return data


def _extract_results(data: Mapping[str, object]) -> Sequence[Mapping[str, object]]:
    results = data.get("results", [])
    if isinstance(results, Sequence):
        return results  # type: ignore[return-value]
    return []


def render_reason_log(payload: Mapping[str, object], *, console: Console | None = None) -> None:
    """Render a textual MVP of the Reason Log."""

    console = console or DEFAULT_CONSOLE
    log = _extract_log(payload)
    results = _extract_results(payload)

    table = Table(title="Philosopher Scores", show_header=True, header_style="bold magenta")
    table.add_column("Philosopher")
    table.add_column("Weight", justify="right")
    table.add_column("Confidence", justify="right")
    table.add_column("Summary", overflow="fold")

    if results:
        for result in results:
            table.add_row(
                str(result.get("name", "")),
                f"{result.get('weight', 0):.2f}",
                f"{result.get('confidence', 0):.2f}",
                str(result.get("summary", "")),
            )
    else:
        table.add_row("(no results)", "-", "-", "Log-only payload")

    console.print(table)

    console.print("\n[bold]Event Timeline[/bold]")
    events: Iterable[MutableMapping[str, object]] = list(log.get("events", []))  # type: ignore[assignment]
    with Progress(console=console) as progress:
        task = progress.add_task("Events", total=len(events))
        for entry in events:  # type: ignore[assignment]
            progress.console.print(
                f"• {entry.get('timestamp', '')} — {entry.get('event', '')}",
                highlight=False,
            )
            if entry.get("decision"):
                progress.console.print(f"  decision: {entry['decision']}")
            suppressed = entry.get("suppressed") or []
            if suppressed:
                progress.console.print(f"  suppressed: {', '.join(suppressed)}")
            progress.update(task, advance=1)


@click.command()
@click.argument("log_path")
def cli(log_path: str) -> None:
    """Standalone entry point for Po_viewer."""

    data = json.loads(log_path)
    render_reason_log(data)


if __name__ == "__main__":
    cli()
