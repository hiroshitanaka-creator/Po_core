"""
Po_viewer: Visualization Module

Visualizes the reasoning process, tension maps,
and philosophical interactions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence

import click
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class TraceEvent:
    """Single Po_trace event captured in the log."""

    step: int
    philosopher: str
    tension: float
    summary: str


@dataclass
class PhilosopherContribution:
    """Aggregated statistics for each philosopher."""

    name: str
    turns: int
    average_tension: float
    latest_summary: str


@dataclass
class PoTraceLog:
    """Structured representation of a Po_trace log."""

    session: str
    events: List[TraceEvent]

    @property
    def philosopher_contributions(self) -> List[PhilosopherContribution]:
        contributions: Dict[str, List[TraceEvent]] = {}
        for event in self.events:
            contributions.setdefault(event.philosopher, []).append(event)

        aggregated: List[PhilosopherContribution] = []
        for name, events in contributions.items():
            turns = len(events)
            average = sum(event.tension for event in events) / max(turns, 1)
            latest_summary = events[-1].summary
            aggregated.append(
                PhilosopherContribution(
                    name=name,
                    turns=turns,
                    average_tension=round(average, 3),
                    latest_summary=latest_summary,
                )
            )

        return sorted(aggregated, key=lambda item: item.name)


def _tension_bar(tension: float, width: int = 12) -> str:
    clamped = min(max(tension, 0.0), 1.0)
    filled = int(round(clamped * width))
    bar = "█" * filled
    padding = "░" * (width - filled)
    return f"{bar}{padding} {clamped:.2f}"


def load_trace(trace_path: str | Path) -> PoTraceLog:
    """Load a Po_trace JSON log from disk and validate its structure."""

    try:
        data = json.loads(Path(trace_path).read_text(encoding="utf-8"))
    except FileNotFoundError as error:  # pragma: no cover - click handles path option
        raise click.ClickException(f"Trace file not found: {trace_path}") from error
    except json.JSONDecodeError as error:
        raise click.ClickException("Trace file is not valid JSON") from error

    events_data = data.get("events")
    if not isinstance(events_data, Sequence) or not events_data:
        raise click.ClickException("Trace file must include a non-empty 'events' list")

    events: List[TraceEvent] = []
    for raw in events_data:
        try:
            step = int(raw["step"])
            philosopher = str(raw["philosopher"])
            tension = float(raw.get("tension", 0.0))
            summary = str(raw.get("summary", ""))
        except (TypeError, KeyError, ValueError) as error:
            raise click.ClickException(
                "Each event must include 'step', 'philosopher', and numeric 'tension'"
            ) from error
        events.append(
            TraceEvent(
                step=step,
                philosopher=philosopher,
                tension=tension,
                summary=summary,
            )
        )

    session = str(data.get("session", "Unnamed Po_trace Session"))
    return PoTraceLog(session=session, events=sorted(events, key=lambda item: item.step))


def export_visualization(log: PoTraceLog) -> Dict[str, Any]:
    """Export the visualization-friendly JSON payload."""

    return {
        "session": log.session,
        "timeline": [
            {
                "step": event.step,
                "philosopher": event.philosopher,
                "tension": event.tension,
                "summary": event.summary,
            }
            for event in log.events
        ],
        "philosophers": [
            {
                "name": contribution.name,
                "turns": contribution.turns,
                "average_tension": contribution.average_tension,
                "latest_summary": contribution.latest_summary,
            }
            for contribution in log.philosopher_contributions
        ],
    }


def render_tension_map(log: PoTraceLog, *, console: Console = console) -> None:
    """Render a step-by-step tension map to the provided console."""

    table = Table(title=f"Tension Map ▸ {log.session}", show_lines=True)
    table.add_column("Step", justify="right", style="cyan")
    table.add_column("Philosopher", style="magenta")
    table.add_column("Tension", style="yellow")
    table.add_column("Summary", overflow="fold")

    for event in log.events:
        table.add_row(
            str(event.step),
            event.philosopher,
            _tension_bar(event.tension),
            event.summary,
        )

    console.print(table)


def render_philosopher_contributions(
    log: PoTraceLog, *, console: Console = console
) -> None:
    """Render per-philosopher contribution statistics."""

    table = Table(title="Philosopher Contributions", show_lines=True)
    table.add_column("Philosopher", style="magenta")
    table.add_column("Turns", justify="right", style="cyan")
    table.add_column("Avg Tension", justify="right", style="yellow")
    table.add_column("Latest Summary", overflow="fold")

    for contribution in log.philosopher_contributions:
        table.add_row(
            contribution.name,
            str(contribution.turns),
            f"{contribution.average_tension:.3f}",
            contribution.latest_summary,
        )

    console.print(table)


def render_trace(log: PoTraceLog, *, console: Console = console) -> None:
    """Render all available Po_trace visualizations."""

    console.rule(f"🎨 Po_trace Viewer • {log.session}")
    render_tension_map(log, console=console)
    render_philosopher_contributions(log, console=console)


@click.command()
@click.option(
    "trace_path",
    "--trace",
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Path to a Po_trace JSON log",
)
def cli(trace_path: Path) -> None:
    """Po_viewer CLI entry point"""

    log = load_trace(trace_path)
    render_trace(log, console=console)


if __name__ == "__main__":  # pragma: no cover - manual entry point
    cli()
