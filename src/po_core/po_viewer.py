"""
Po_viewer: Visualization Module

Visualizes the reasoning process, tension maps,
and philosophical interactions.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import click

from po_core.utils.logging import echo_error, echo_info, echo_success


@click.group()
def cli() -> None:
    """Po_viewer CLI entry point."""
    echo_info("🎨 Po_viewer - Reasoning Visualization")


@cli.command()
@click.option(
    "source",
    "--source",
    "-s",
    required=True,
    type=click.Path(path_type=Path),
    help="Path to a trace log file (JSON lines).",
)
@click.option(
    "fmt",
    "--format",
    "-f",
    type=click.Choice(["ascii"], case_sensitive=False),
    default="ascii",
    show_default=True,
    help="Render format.",
)
@click.option(
    "top",
    "--top",
    "-t",
    default=5,
    show_default=True,
    help="Number of top events to display.",
)
def render(source: Path, fmt: str, top: int) -> None:
    """Render a summary of the trace log."""
    if not source.exists():
        echo_error(f"Trace log not found: {source}")
        sys.exit(1)

    events = _load_events(source)
    if not events:
        echo_error("Trace log is empty. Nothing to render.")
        sys.exit(1)

    summary = _summarize(events, limit=top)
    if fmt.lower() == "ascii":
        _render_ascii(summary)
    else:
        echo_error(f"Unsupported format: {fmt}")
        sys.exit(1)


def _load_events(path: Path) -> List[Dict[str, str]]:
    events: List[Dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
            if isinstance(payload, dict) and "event" in payload:
                events.append({"event": str(payload.get("event"))})
        except json.JSONDecodeError:
            continue
    return events


def _summarize(events: List[Dict[str, str]], limit: int) -> List[Tuple[str, int]]:
    counts = Counter(event["event"] for event in events)
    return counts.most_common(limit)


def _render_ascii(summary: List[Tuple[str, int]]) -> None:
    echo_success("Event Summary")
    for name, count in summary:
        bar = "#" * count
        click.echo(f"{name}: {bar} ({count})")


if __name__ == "__main__":
    cli()
