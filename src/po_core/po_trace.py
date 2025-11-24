"""Po_trace: Reasoning Audit Log Module.

Provides a lightweight audit log for reasoning events and a CLI to
append new entries or inspect recent history. The implementation keeps
the structure intentionally simple so it can evolve alongside the
design documents without locking in a heavy storage layer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence

import click
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class TraceEvent:
    """Represents a single reasoning event in Po_trace."""

    title: str
    detail: str
    step: int | None = None
    tags: Sequence[str] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z"
    )

    def to_dict(self) -> dict:
        """Convert event to a JSON-serializable dict."""

        payload = asdict(self)
        # Convert tuple to list for JSON compatibility
        payload["tags"] = list(self.tags)
        return payload

    @classmethod
    def from_dict(cls, data: dict) -> "TraceEvent":
        """Create an event from a dictionary, gracefully handling missing fields."""

        return cls(
            title=data.get("title", "(untitled)"),
            detail=data.get("detail", ""),
            step=data.get("step"),
            tags=data.get("tags", []),
            timestamp=data.get("timestamp")
            or datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )


class PoTraceLogger:
    """In-memory Po_trace logger with optional JSON persistence."""

    def __init__(self, log_path: Path | str | None = None) -> None:
        self.log_path = Path(log_path) if log_path else None
        self.events: List[TraceEvent] = []
        if self.log_path and self.log_path.exists():
            self.events = self._load(self.log_path)

    def add_event(
        self,
        title: str,
        detail: str,
        step: int | None = None,
        tags: Iterable[str] | None = None,
    ) -> TraceEvent:
        """Append a new event to the log and persist if configured."""

        event = TraceEvent(title=title, detail=detail, step=step, tags=tags or [])
        self.events.append(event)
        if self.log_path:
            self._save(self.log_path)
        return event

    def summary(self) -> dict:
        """Return a basic summary of the log for quick inspection."""

        tag_counter: dict[str, int] = {}
        for event in self.events:
            for tag in event.tags:
                tag_counter[tag] = tag_counter.get(tag, 0) + 1

        return {
            "total_events": len(self.events),
            "tags": tag_counter,
            "most_recent": self.events[-1] if self.events else None,
        }

    def _load(self, path: Path) -> List[TraceEvent]:
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError:
            return []

        return [TraceEvent.from_dict(item) for item in payload]

    def _save(self, path: Path) -> None:
        path.write_text(json.dumps([event.to_dict() for event in self.events], indent=2))


def _build_logger(log_file: Path) -> PoTraceLogger:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    return PoTraceLogger(log_file)


@click.group()
def cli() -> None:
    """Po_trace CLI entry point."""


@cli.command("log")
@click.option("--title", required=True, help="Short label for the event")
@click.option("--detail", required=False, default="", help="Detailed description")
@click.option("--step", type=int, required=False, help="Optional reasoning step index")
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="Apply one or more tags (use multiple --tag flags)",
)
@click.option(
    "--log-file",
    type=click.Path(path_type=Path, dir_okay=False, resolve_path=True),
    default=Path("po_trace_log.json"),
    help="File path where the audit log is stored",
)
def log_command(
    title: str, detail: str, step: int | None, tags: Sequence[str], log_file: Path
) -> None:
    """Append a new Po_trace event and persist it to a JSON log file."""

    logger = _build_logger(log_file)
    event = logger.add_event(title=title, detail=detail, step=step, tags=tags)

    console.print("[bold green]🔍 Event recorded in Po_trace[/bold green]")
    console.print(f"Log file: {log_file}")
    console.print(f"Title   : {event.title}")
    if event.step is not None:
        console.print(f"Step    : {event.step}")
    if event.tags:
        console.print(f"Tags    : {', '.join(event.tags)}")
    if event.detail:
        console.print(f"Detail  : {event.detail}")


@cli.command("show")
@click.option(
    "--log-file",
    type=click.Path(path_type=Path, dir_okay=False, resolve_path=True),
    default=Path("po_trace_log.json"),
    help="File path where the audit log is stored",
)
@click.option("--limit", type=int, default=5, help="Number of latest events to display")
def show_command(log_file: Path, limit: int) -> None:
    """Display a summary and the most recent Po_trace events."""

    logger = _build_logger(log_file)
    summary = logger.summary()

    console.print("[bold blue]📜 Po_trace Audit Log[/bold blue]")
    console.print(f"Log file     : {log_file}")
    console.print(f"Total events : {summary['total_events']}")
    if summary["tags"]:
        tag_repr = ", ".join(f"{tag} ({count})" for tag, count in summary["tags"].items())
        console.print(f"Tags         : {tag_repr}")

    if not logger.events:
        console.print("\n[dim]No events recorded yet.[/dim]")
        return

    table = Table(title=f"Latest {min(limit, len(logger.events))} events", show_lines=True)
    table.add_column("Timestamp", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Step", justify="right")
    table.add_column("Tags")
    table.add_column("Detail")

    for event in list(logger.events)[-limit:][::-1]:
        table.add_row(
            event.timestamp,
            event.title,
            "-" if event.step is None else str(event.step),
            ", ".join(event.tags) if event.tags else "-",
            event.detail or "-",
        )

    console.print("\n")
    console.print(table)


if __name__ == "__main__":
    cli()
