"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process,
including what was said and what was not said.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.table import Table

console = Console()


class EventType(str, Enum):
    """Types of events that can be logged."""

    EXECUTION = "execution"
    STATE_CHANGE = "state_change"
    ERROR = "error"
    USER_ACTION = "user_action"
    SYSTEM = "system"


@dataclass
class Event:
    """Represents a single event in the reasoning trace."""

    event_id: str
    session_id: str
    timestamp: str
    event_type: EventType
    source: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type.value,
            "source": self.source,
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Event:
        """Create event from dictionary."""
        return cls(
            event_id=data["event_id"],
            session_id=data["session_id"],
            timestamp=data["timestamp"],
            event_type=EventType(data["event_type"]),
            source=data["source"],
            data=data["data"],
            metadata=data.get("metadata", {}),
        )


@dataclass
class Session:
    """Represents a complete reasoning session."""

    session_id: str
    prompt: str
    philosophers: List[str]
    created_at: str
    events: List[Event] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "prompt": self.prompt,
            "philosophers": self.philosophers,
            "created_at": self.created_at,
            "events": [event.to_dict() for event in self.events],
            "metrics": self.metrics,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Session:
        """Create session from dictionary."""
        return cls(
            session_id=data["session_id"],
            prompt=data["prompt"],
            philosophers=data["philosophers"],
            created_at=data["created_at"],
            events=[Event.from_dict(e) for e in data.get("events", [])],
            metrics=data.get("metrics", {}),
            metadata=data.get("metadata", {}),
        )


class PoTrace:
    """Po_trace audit logging system."""

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize Po_trace with optional custom storage directory."""
        if storage_dir is None:
            self.storage_dir = Path.home() / ".po_core" / "traces"
        else:
            self.storage_dir = storage_dir

        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._index_file = self.storage_dir / "index.json"
        self._ensure_index()

    def _ensure_index(self) -> None:
        """Ensure index file exists."""
        if not self._index_file.exists():
            self._index_file.write_text(json.dumps({"sessions": []}, indent=2))

    def _load_index(self) -> Dict[str, Any]:
        """Load index file."""
        return json.loads(self._index_file.read_text())

    def _save_index(self, index: Dict[str, Any]) -> None:
        """Save index file."""
        self._index_file.write_text(json.dumps(index, indent=2, ensure_ascii=False))

    def _session_file(self, session_id: str) -> Path:
        """Get path to session file."""
        return self.storage_dir / f"{session_id}.json"

    def create_session(
        self,
        prompt: str,
        philosophers: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a new reasoning session.

        Args:
            prompt: The prompt for this session
            philosophers: List of philosopher names
            metadata: Optional metadata

        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        session = Session(
            session_id=session_id,
            prompt=prompt,
            philosophers=philosophers,
            created_at=timestamp,
            metadata=metadata or {},
        )

        # Save session
        session_file = self._session_file(session_id)
        session_file.write_text(json.dumps(session.to_dict(), indent=2, ensure_ascii=False))

        # Update index
        index = self._load_index()
        index["sessions"].append(
            {
                "session_id": session_id,
                "prompt": prompt[:100],  # Truncate for index
                "created_at": timestamp,
                "philosophers_count": len(philosophers),
            }
        )
        self._save_index(index)

        return session_id

    def log_event(
        self,
        session_id: str,
        event_type: EventType,
        source: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log an event to a session.

        Args:
            session_id: Session identifier
            event_type: Type of event
            source: Source module/component
            data: Event data
            metadata: Optional event metadata

        Returns:
            event_id: Unique event identifier
        """
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        event = Event(
            event_id=event_id,
            session_id=session_id,
            timestamp=timestamp,
            event_type=event_type,
            source=source,
            data=data,
            metadata=metadata or {},
        )

        # Load session
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        # Add event
        session.events.append(event)

        # Save session
        session_file = self._session_file(session_id)
        session_file.write_text(json.dumps(session.to_dict(), indent=2, ensure_ascii=False))

        return event_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session object or None if not found
        """
        session_file = self._session_file(session_id)
        if not session_file.exists():
            return None

        data = json.loads(session_file.read_text())
        return Session.from_dict(data)

    def list_sessions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all sessions.

        Args:
            limit: Optional limit on number of sessions to return

        Returns:
            List of session metadata
        """
        index = self._load_index()
        sessions = index.get("sessions", [])

        # Sort by created_at descending (most recent first)
        sessions.sort(key=lambda s: s["created_at"], reverse=True)

        if limit:
            sessions = sessions[:limit]

        return sessions

    def update_metrics(self, session_id: str, metrics: Dict[str, float]) -> None:
        """
        Update session metrics.

        Args:
            session_id: Session identifier
            metrics: Metrics to update
        """
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        session.metrics.update(metrics)

        # Save session
        session_file = self._session_file(session_id)
        session_file.write_text(json.dumps(session.to_dict(), indent=2, ensure_ascii=False))

    def export_session(self, session_id: str, format: str = "json") -> str:
        """
        Export a session to a specific format.

        Args:
            session_id: Session identifier
            format: Export format ('json' or 'text')

        Returns:
            Exported content as string
        """
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        if format == "json":
            return json.dumps(session.to_dict(), indent=2, ensure_ascii=False)
        elif format == "text":
            lines = []
            lines.append(f"Session: {session.session_id}")
            lines.append(f"Created: {session.created_at}")
            lines.append(f"Prompt: {session.prompt}")
            lines.append(f"Philosophers: {', '.join(session.philosophers)}")
            lines.append(f"\nMetrics:")
            for key, value in session.metrics.items():
                lines.append(f"  {key}: {value}")
            lines.append(f"\nEvents ({len(session.events)}):")
            for event in session.events:
                lines.append(f"  [{event.timestamp}] {event.event_type.value} - {event.source}")
                if "message" in event.data:
                    lines.append(f"    {event.data['message']}")
            return "\n".join(lines)
        else:
            raise ValueError(f"Unknown format: {format}")


# CLI Commands
@click.group()
def cli() -> None:
    """Po_trace - Reasoning Audit Log System"""
    pass


@cli.command()
@click.option("--limit", type=int, default=10, help="Limit number of sessions to show")
def list(limit: int) -> None:
    """List recent reasoning sessions."""
    trace = PoTrace()
    sessions = trace.list_sessions(limit=limit)

    if not sessions:
        console.print("[yellow]No sessions found[/yellow]")
        return

    table = Table(title="Po_trace Sessions", show_header=True, header_style="bold magenta")
    table.add_column("Session ID", style="cyan", no_wrap=True)
    table.add_column("Created", style="green")
    table.add_column("Philosophers", style="yellow", justify="right")
    table.add_column("Prompt", style="white")

    for session in sessions:
        table.add_row(
            session["session_id"][:8],
            session["created_at"],
            str(session["philosophers_count"]),
            session["prompt"][:60] + "..." if len(session["prompt"]) > 60 else session["prompt"],
        )

    console.print(table)


@cli.command()
@click.argument("session_id")
def show(session_id: str) -> None:
    """Show detailed information about a session."""
    trace = PoTrace()
    session = trace.get_session(session_id)

    if session is None:
        console.print(f"[red]Session {session_id} not found[/red]")
        return

    console.print(f"\n[bold magenta]Session: {session.session_id}[/bold magenta]")
    console.print(f"[green]Created:[/green] {session.created_at}")
    console.print(f"[green]Prompt:[/green] {session.prompt}")
    console.print(f"[green]Philosophers:[/green] {', '.join(session.philosophers)}")

    if session.metrics:
        console.print(f"\n[bold cyan]Metrics:[/bold cyan]")
        for key, value in session.metrics.items():
            console.print(f"  {key}: {value:.3f}")

    console.print(f"\n[bold yellow]Events ({len(session.events)}):[/bold yellow]")
    for event in session.events:
        console.print(f"\n[cyan]{event.timestamp}[/cyan] - [{event.event_type.value}] {event.source}")
        if "message" in event.data:
            console.print(f"  {event.data['message']}")
        if "philosopher" in event.data:
            console.print(f"  Philosopher: {event.data['philosopher']}")


@cli.command()
@click.argument("session_id")
@click.option("--format", "output_format", type=click.Choice(["json", "text"]), default="json", help="Export format")
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
def export(session_id: str, output_format: str, output: Optional[str]) -> None:
    """Export a session to a file."""
    trace = PoTrace()

    try:
        content = trace.export_session(session_id, format=output_format)

        if output:
            Path(output).write_text(content)
            console.print(f"[green]Session exported to {output}[/green]")
        else:
            console.print(content)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    cli()
