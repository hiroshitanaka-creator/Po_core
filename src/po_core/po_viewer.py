"""Po_viewer: Visualization Module

Lightweight viewer utilities for Po_trace logs. The module focuses on two
responsibilities:

* Load a Po_trace JSON log from disk.
* Render a compact terminal visualization (tension map + philosopher
  contributions) and export the same data structure as JSON for future Web
  viewer integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Mapping

import click
import orjson
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass(frozen=True)
class Contribution:
    """A single philosopher contribution within a Po_trace step."""

    philosopher: str
    summary: str
    weight: float


@dataclass(frozen=True)
class TraceStep:
    """Individual step inside a Po_trace log."""

    step: int
    tension: Mapping[str, float]
    contributions: List[Contribution]
    note: str | None = None


@dataclass(frozen=True)
class TraceData:
    """Structured representation of a Po_trace log."""

    trace_id: str
    theme: str
    steps: List[TraceStep]


def _load_json(path: Path) -> Dict:
    return orjson.loads(path.read_bytes())


def load_po_trace(path: Path | str) -> TraceData:
    """Load a Po_trace JSON log from ``path`` into a typed structure.

    The expected schema is intentionally minimal for the initial viewer:

    ``trace_id`` (str), ``theme`` (str), and ``steps`` (list). Each step must
    contain ``step`` (int), ``tension`` (mapping of philosopher name to float
    between 0 and 1), and ``contributions`` (list of philosopher summaries with
    ``philosopher``, ``summary``, and ``weight`` fields).
    """

    trace_raw = _load_json(Path(path))
    steps: List[TraceStep] = []
    for entry in trace_raw.get("steps", []):
        contributions = [
            Contribution(
                philosopher=item["philosopher"],
                summary=item.get("summary", ""),
                weight=float(item.get("weight", 0.0)),
            )
            for item in entry.get("contributions", [])
        ]

        steps.append(
            TraceStep(
                step=int(entry["step"]),
                tension={k: float(v) for k, v in entry.get("tension", {}).items()},
                contributions=contributions,
                note=entry.get("note"),
            )
        )

    return TraceData(
        trace_id=str(trace_raw.get("trace_id", "unknown-trace")),
        theme=str(trace_raw.get("theme", "(untitled)")),
        steps=sorted(steps, key=lambda step: step.step),
    )


def _bar(value: float, size: int = 12) -> str:
    clamped = max(0.0, min(1.0, value))
    filled = int(round(clamped * size))
    return "█" * filled + "·" * (size - filled)


def _aggregate_contributions(steps: Iterable[TraceStep]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    for step in steps:
        for contribution in step.contributions:
            totals[contribution.philosopher] = totals.get(contribution.philosopher, 0) + contribution.weight
    return totals


def render_trace_summary(trace: TraceData) -> str:
    """Render a combined tension map and contribution overview as text."""

    record_console = Console(
        record=True, force_terminal=False, color_system=None, width=88, file=StringIO()
    )
    record_console.print(f"[bold cyan]🎨 Po_trace Viewer[/bold cyan] — [italic]{trace.theme}[/italic]")
    record_console.print(f"Trace ID: [bold]{trace.trace_id}[/bold]\n")

    tension_table = Table(title="Tension Map", show_edge=False, header_style="bold magenta")
    tension_table.add_column("Step", style="cyan", justify="right")
    tension_table.add_column("Philosopher", style="white")
    tension_table.add_column("Tension", style="green", justify="right")
    tension_table.add_column("Level", style="yellow")

    for step in trace.steps:
        for philosopher in sorted(step.tension):
            tension_value = step.tension[philosopher]
            tension_table.add_row(
                str(step.step),
                philosopher,
                f"{tension_value:0.2f}",
                _bar(tension_value),
            )
    record_console.print(tension_table)

    totals = _aggregate_contributions(trace.steps)
    total_weight = sum(totals.values()) or 1.0
    contribution_table = Table(
        title="Philosopher Contributions", show_edge=False, header_style="bold blue"
    )
    contribution_table.add_column("Philosopher", style="white")
    contribution_table.add_column("Weight", style="green", justify="right")
    contribution_table.add_column("Share", style="yellow")

    for philosopher in sorted(totals):
        weight = totals[philosopher]
        share = weight / total_weight
        contribution_table.add_row(
            philosopher,
            f"{weight:0.2f}",
            _bar(share),
        )

    record_console.print("\n")
    record_console.print(contribution_table)
    return record_console.export_text(clear=False)


def export_visualization_data(trace: TraceData) -> str:
    """Export visualization-ready data as JSON for a future Web viewer."""

    payload = {
        "trace_id": trace.trace_id,
        "theme": trace.theme,
        "tension_map": [
            {"step": step.step, "tension": dict(step.tension)} for step in trace.steps
        ],
        "contributions": _aggregate_contributions(trace.steps),
    }
    return orjson.dumps(payload, option=orjson.OPT_INDENT_2).decode()


@click.command()
@click.option(
    "trace_path",
    "--trace",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to a Po_trace JSON log (see examples/po_trace_sample.json)",
)
def cli(trace_path: Path) -> None:
    """Po_viewer CLI entry point."""

    trace = load_po_trace(trace_path)
    output = render_trace_summary(trace)
    console.print(output)


if __name__ == "__main__":
    cli()
