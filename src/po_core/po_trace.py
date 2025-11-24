"""
Po_trace: Reasoning Audit Log Module

Provides data models and persistence for reasoning traces, along with
CLI utilities to inspect them. Traces capture prompts, responses,
participating philosophers, refusal reasons, and arbitrary metadata.
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import click
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_FILE_PATH = Path("po_trace.log")
DEFAULT_SQLITE_PATH = Path("po_trace.db")


@dataclass
class TraceEvent:
    """A single reasoning trace event."""

    event_id: str
    timestamp: datetime
    input_text: str
    response_text: str
    philosophers: List[str]
    refusal_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "input_text": self.input_text,
            "response_text": self.response_text,
            "philosophers": self.philosophers,
            "refusal_reason": self.refusal_reason,
            "metadata": self.metadata,
        }

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "TraceEvent":
        timestamp = record.get("timestamp")
        ts_value = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else datetime.utcnow()
        return cls(
            event_id=record.get("event_id", str(uuid.uuid4())),
            timestamp=ts_value,
            input_text=record.get("input_text", ""),
            response_text=record.get("response_text", ""),
            philosophers=list(record.get("philosophers", [])),
            refusal_reason=record.get("refusal_reason"),
            metadata=record.get("metadata", {}),
        )


class TraceStore:
    """Abstract storage for trace events."""

    def append(self, event: TraceEvent) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    def tail(
        self,
        limit: int = 10,
        philosophers: Optional[Sequence[str]] = None,
        refused_only: bool = False,
        contains: Optional[str] = None,
    ) -> List[TraceEvent]:  # pragma: no cover - interface
        raise NotImplementedError


class FileTraceStore(TraceStore):
    """Persist trace events as newline-delimited JSON."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def append(self, event: TraceEvent) -> None:
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event.to_record(), ensure_ascii=False) + "\n")

    def _load_events(self) -> List[TraceEvent]:
        events: List[TraceEvent] = []
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                events.append(TraceEvent.from_record(record))
        return events

    def tail(
        self,
        limit: int = 10,
        philosophers: Optional[Sequence[str]] = None,
        refused_only: bool = False,
        contains: Optional[str] = None,
    ) -> List[TraceEvent]:
        events = self._load_events()
        filtered = _apply_filters(events, philosophers, refused_only, contains)
        return filtered[-limit:] if limit else filtered


class SQLiteTraceStore(TraceStore):
    """Persist trace events in SQLite."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trace_events (
                    event_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    philosophers TEXT NOT NULL,
                    refusal_reason TEXT,
                    metadata TEXT
                )
                """
            )
            conn.commit()

    def append(self, event: TraceEvent) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO trace_events (
                    event_id, timestamp, input_text, response_text,
                    philosophers, refusal_reason, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.timestamp.isoformat(),
                    event.input_text,
                    event.response_text,
                    json.dumps(event.philosophers, ensure_ascii=False),
                    event.refusal_reason,
                    json.dumps(event.metadata, ensure_ascii=False),
                ),
            )
            conn.commit()

    def _fetch_events(self) -> List[TraceEvent]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT event_id, timestamp, input_text, response_text, philosophers, refusal_reason, metadata FROM trace_events ORDER BY rowid"
            ).fetchall()
        events: List[TraceEvent] = []
        for row in rows:
            record = {
                "event_id": row[0],
                "timestamp": row[1],
                "input_text": row[2],
                "response_text": row[3],
                "philosophers": json.loads(row[4]) if row[4] else [],
                "refusal_reason": row[5],
                "metadata": json.loads(row[6]) if row[6] else {},
            }
            events.append(TraceEvent.from_record(record))
        return events

    def tail(
        self,
        limit: int = 10,
        philosophers: Optional[Sequence[str]] = None,
        refused_only: bool = False,
        contains: Optional[str] = None,
    ) -> List[TraceEvent]:
        events = self._fetch_events()
        filtered = _apply_filters(events, philosophers, refused_only, contains)
        return filtered[-limit:] if limit else filtered


def _apply_filters(
    events: Iterable[TraceEvent],
    philosophers: Optional[Sequence[str]],
    refused_only: bool,
    contains: Optional[str],
) -> List[TraceEvent]:
    def _matches(event: TraceEvent) -> bool:
        if philosophers:
            ph_set = {p.lower() for p in event.philosophers}
            if not any(ph.lower() in ph_set for ph in philosophers):
                return False
        if refused_only and event.refusal_reason is None:
            return False
        if contains:
            needle = contains.lower()
            if needle not in event.input_text.lower() and needle not in event.response_text.lower():
                return False
        return True

    return [event for event in events if _matches(event)]


def get_trace_store(backend: str, location: Optional[str]) -> TraceStore:
    if backend == "sqlite":
        path = Path(location) if location else DEFAULT_SQLITE_PATH
        return SQLiteTraceStore(path)
    path = Path(location) if location else DEFAULT_FILE_PATH
    return FileTraceStore(path)


class TraceRecorder:
    """Interface for recording and reading trace events."""

    def __init__(self, backend: str = "file", location: Optional[str] = None) -> None:
        self.store = get_trace_store(backend, location)

    def record(
        self,
        input_text: str,
        response_text: str,
        philosophers: Sequence[str],
        refusal_reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> TraceEvent:
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=timestamp or datetime.utcnow(),
            input_text=input_text,
            response_text=response_text,
            philosophers=list(philosophers),
            refusal_reason=refusal_reason,
            metadata=metadata or {},
        )
        self.store.append(event)
        return event

    def tail(
        self,
        limit: int = 10,
        philosophers: Optional[Sequence[str]] = None,
        refused_only: bool = False,
        contains: Optional[str] = None,
    ) -> List[TraceEvent]:
        return self.store.tail(limit, philosophers, refused_only, contains)


def record_trace_event(
    input_text: str,
    response_text: str,
    philosophers: Sequence[str],
    refusal_reason: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    backend: str = "file",
    location: Optional[str] = None,
) -> TraceEvent:
    """Convenience hook for generation pipelines to persist trace events."""
    recorder = TraceRecorder(backend=backend, location=location)
    return recorder.record(
        input_text=input_text,
        response_text=response_text,
        philosophers=philosophers,
        refusal_reason=refusal_reason,
        metadata=metadata,
    )


def _render_events(events: Sequence[TraceEvent]) -> None:
    if not events:
        console.print("[dim]No trace events found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="cyan")
    table.add_column("Philosophers", style="green")
    table.add_column("Input", style="white")
    table.add_column("Response", style="yellow")
    table.add_column("Refusal", style="red")

    for event in events:
        table.add_row(
            event.timestamp.isoformat(timespec="seconds"),
            ", ".join(event.philosophers),
            event.input_text,
            event.response_text,
            event.refusal_reason or "-",
        )
    console.print(table)


def _cli_common_options(function):
    function = click.option(
        "--backend",
        type=click.Choice(["file", "sqlite"], case_sensitive=False),
        default="file",
        show_default=True,
        help="Trace persistence backend.",
    )(function)
    function = click.option(
        "--location",
        type=click.Path(dir_okay=False, path_type=Path),
        help="Path to the log file or SQLite database.",
    )(function)
    function = click.option("--tail", "tail_count", type=int, default=10, show_default=True, help="Number of events to display.")(function)
    function = click.option(
        "--philosopher",
        "philosophers",
        multiple=True,
        help="Filter events to those involving the given philosopher(s).",
    )(function)
    function = click.option(
        "--refused",
        is_flag=True,
        default=False,
        help="Show only refused events (where a refusal_reason is present).",
    )(function)
    function = click.option(
        "--contains",
        help="Filter events whose input or response contains the given text (case-insensitive).",
    )(function)
    return function


@click.command()
@_cli_common_options
def cli(
    tail_count: int,
    philosophers: Sequence[str],
    refused: bool,
    contains: Optional[str],
    backend: str,
    location: Optional[Path],
) -> None:
    """Inspect reasoning traces from the CLI."""

    recorder = TraceRecorder(backend=backend, location=str(location) if location else None)
    events = recorder.tail(
        limit=tail_count,
        philosophers=philosophers,
        refused_only=refused,
        contains=contains,
    )
    console.print("[bold green]🔍 Po_trace - Reasoning Audit Log[/bold green]")
    _render_events(events)


if __name__ == "__main__":
    cli()
