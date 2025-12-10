"""
Po_trace: Reasoning Audit Log Module

Tracks and persists the reasoning process of Po_self,
including aggregate metrics and per-philosopher responses.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import click
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from po_core.po_self import PoSelf, PoSelfResponse

console = Console()

# デフォルトのログ保存先（必要なら設定で変えられるようにしてもよい）
DEFAULT_TRACE_DIR = Path("traces")


class EventType(str, Enum):
    """Event types for reasoning traces."""

    PHILOSOPHER_RESPONSE = "philosopher_response"
    PHILOSOPHER_REASONING = "philosopher_reasoning"
    CONSENSUS_FORMED = "consensus_formed"
    METRIC_UPDATE = "metric_update"
    EXECUTION = "execution"
    STATE_CHANGE = "state_change"
    ERROR = "error"
    USER_ACTION = "user_action"
    SYSTEM = "system"
    INFO = "info"
    # Phase 4: New event types for rejection tracking
    REJECTION = "rejection"
    BLOCKING = "blocking"
    SAFETY_VIOLATION = "safety_violation"
    ETHICAL_CONCERN = "ethical_concern"


@dataclass
class Event:
    """Individual event within a reasoning session."""

    event_id: str
    session_id: str
    timestamp: str
    event_type: EventType
    source: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
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
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create Event from dictionary."""
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
    """Complete reasoning session with events and metrics."""

    session_id: str
    prompt: str
    philosophers: List[str]
    created_at: str
    events: List[Event] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
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
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """Create Session from dictionary."""
        return cls(
            session_id=data["session_id"],
            prompt=data["prompt"],
            philosophers=data["philosophers"],
            created_at=data["created_at"],
            events=[Event.from_dict(e) for e in data.get("events", [])],
            metrics=data.get("metrics", {}),
            metadata=data.get("metadata", {}),
        )


@dataclass
class RejectionLog:
    """
    Log entry for rejected or blocked philosophical reasoning.

    Tracks cases where reasoning was rejected due to safety concerns,
    ethical violations, or blocking constraints.
    """

    rejection_id: str
    session_id: str
    timestamp: str
    rejection_type: str  # "safety", "ethical", "blocked", "restricted"
    philosopher: str
    prompt: str
    reasoning_attempt: Optional[str] = None
    reason: str = ""
    blocked_tensor_value: Optional[float] = None
    freedom_pressure_value: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "rejection_id": self.rejection_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "rejection_type": self.rejection_type,
            "philosopher": self.philosopher,
            "prompt": self.prompt,
            "reasoning_attempt": self.reasoning_attempt,
            "reason": self.reason,
            "blocked_tensor_value": self.blocked_tensor_value,
            "freedom_pressure_value": self.freedom_pressure_value,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RejectionLog":
        """Create RejectionLog from dictionary."""
        return cls(
            rejection_id=data["rejection_id"],
            session_id=data["session_id"],
            timestamp=data["timestamp"],
            rejection_type=data["rejection_type"],
            philosopher=data["philosopher"],
            prompt=data["prompt"],
            reasoning_attempt=data.get("reasoning_attempt"),
            reason=data.get("reason", ""),
            blocked_tensor_value=data.get("blocked_tensor_value"),
            freedom_pressure_value=data.get("freedom_pressure_value"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class TraceHeader:
    """メタ情報：トレースの概要"""

    trace_id: str
    created_at: str
    prompt: str
    philosophers: List[str]
    consensus_leader: Optional[str]
    metrics: Dict[str, float]


@dataclass
class TraceRecord:
    """1つの Po_self 実行結果に対応する完全なトレース"""

    header: TraceHeader
    text: str
    responses: List[Dict[str, Any]]
    log: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        # JSON にそのまま書ける形に落とす
        return {
            "header": asdict(self.header),
            "text": self.text,
            "responses": self.responses,
            "log": self.log,
        }


class PoTrace:
    """Po_self の実行結果をトレースとして保存する責務を持つクラス"""

    def __init__(
        self,
        trace_dir: Path | str = DEFAULT_TRACE_DIR,
        storage_dir: Optional[Path | str] = None,
    ) -> None:
        # Support both trace_dir and storage_dir for backward compatibility
        dir_path = storage_dir if storage_dir is not None else trace_dir
        self.trace_dir = Path(dir_path)
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.sessions: Dict[str, Session] = {}

        # Phase 4: Rejection log tracking
        self.rejections: Dict[str, RejectionLog] = {}

        # Initialize index.json if it doesn't exist
        self._index_file = self.trace_dir / "index.json"
        if not self._index_file.exists():
            self._save_index([])

    @property
    def storage_dir(self) -> Path:
        """Alias for trace_dir for backward compatibility."""
        return self.trace_dir

    def _session_file(self, session_id: str) -> Path:
        """Get the file path for a session."""
        return self.trace_dir / f"session_{session_id}.json"

    def _save_index(self, session_summaries: List[Dict[str, Any]]) -> None:
        """Save the index file with session summaries."""
        with self._index_file.open("w", encoding="utf-8") as f:
            json.dump({"sessions": session_summaries}, f, ensure_ascii=False, indent=2)

    def _update_index(self, session: Session) -> None:
        """Update the index file with a new or updated session."""
        # Load existing index
        if self._index_file.exists():
            with self._index_file.open("r", encoding="utf-8") as f:
                index_data = json.load(f)
                sessions = index_data.get("sessions", [])
        else:
            sessions = []

        # Create session summary
        summary = {
            "session_id": session.session_id,
            "prompt": session.prompt,
            "philosophers": session.philosophers,
            "created_at": session.created_at,
            "event_count": len(session.events),
            "metrics": session.metrics,
        }

        # Update or append
        existing_index = next(
            (i for i, s in enumerate(sessions) if s["session_id"] == session.session_id),
            None
        )
        if existing_index is not None:
            sessions[existing_index] = summary
        else:
            sessions.append(summary)

        # Save updated index
        self._save_index(sessions)

    def create_session(
        self,
        prompt: str,
        philosophers: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new reasoning session and return its ID."""
        session_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat() + "Z"

        session = Session(
            session_id=session_id,
            prompt=prompt,
            philosophers=philosophers,
            created_at=created_at,
            metadata=metadata or {},
        )
        self.sessions[session_id] = session

        # Auto-save session to disk
        self.save_session(session_id)

        # Update index
        self._update_index(session)

        return session_id

    def log_event(
        self,
        session_id: str,
        event_type: EventType,
        source: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an event to a session."""
        if session_id not in self.sessions:
            console.print(f"[yellow]Warning: Session {session_id} not found[/yellow]")
            return

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

        self.sessions[session_id].events.append(event)

    def update_metrics(
        self,
        session_id: str,
        metrics: Dict[str, float],
    ) -> None:
        """Update session metrics."""
        if session_id not in self.sessions:
            console.print(f"[yellow]Warning: Session {session_id} not found[/yellow]")
            return

        self.sessions[session_id].metrics.update(metrics)

    def log_rejection(
        self,
        session_id: str,
        philosopher: str,
        prompt: str,
        rejection_type: str,
        reason: str = "",
        reasoning_attempt: Optional[str] = None,
        blocked_tensor_value: Optional[float] = None,
        freedom_pressure_value: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log a rejected or blocked philosophical reasoning attempt.

        Args:
            session_id: The session ID
            philosopher: Name of the philosopher
            prompt: The prompt that was attempted
            rejection_type: Type of rejection ("safety", "ethical", "blocked", "restricted")
            reason: Reason for rejection
            reasoning_attempt: The attempted reasoning (if available)
            blocked_tensor_value: Blocked tensor metric value
            freedom_pressure_value: Freedom pressure metric value
            metadata: Additional metadata

        Returns:
            rejection_id: Unique ID for this rejection log
        """
        rejection_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        rejection_log = RejectionLog(
            rejection_id=rejection_id,
            session_id=session_id,
            timestamp=timestamp,
            rejection_type=rejection_type,
            philosopher=philosopher,
            prompt=prompt,
            reasoning_attempt=reasoning_attempt,
            reason=reason,
            blocked_tensor_value=blocked_tensor_value,
            freedom_pressure_value=freedom_pressure_value,
            metadata=metadata or {},
        )

        self.rejections[rejection_id] = rejection_log

        # Also log as an event in the session
        if session_id in self.sessions:
            self.log_event(
                session_id=session_id,
                event_type=EventType.REJECTION,
                source=f"philosopher.{philosopher}",
                data={
                    "rejection_id": rejection_id,
                    "rejection_type": rejection_type,
                    "philosopher": philosopher,
                    "reason": reason,
                    "blocked_tensor_value": blocked_tensor_value,
                    "freedom_pressure_value": freedom_pressure_value,
                },
                metadata=metadata,
            )

        # Save rejection to disk
        self._save_rejection(rejection_log)

        return rejection_id

    def _save_rejection(self, rejection_log: RejectionLog) -> None:
        """Save a rejection log to disk."""
        rejection_file = self.trace_dir / f"rejection_{rejection_log.rejection_id}.json"
        with rejection_file.open("w", encoding="utf-8") as f:
            json.dump(rejection_log.to_dict(), f, ensure_ascii=False, indent=2)

    def get_session_rejections(self, session_id: str) -> List[RejectionLog]:
        """Get all rejections for a specific session."""
        return [
            rejection
            for rejection in self.rejections.values()
            if rejection.session_id == session_id
        ]

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        return self.sessions.get(session_id)

    def list_sessions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """List sessions, most recent first, with optional limit."""
        # Sort sessions by created_at in descending order (most recent first)
        sorted_sessions = sorted(
            self.sessions.values(),
            key=lambda s: s.created_at,
            reverse=True
        )

        # Apply limit if specified
        if limit is not None:
            sorted_sessions = sorted_sessions[:limit]

        # Convert to dictionaries
        return [session.to_dict() for session in sorted_sessions]

    def save_session(self, session_id: str) -> Optional[Path]:
        """Save a session to disk."""
        if session_id not in self.sessions:
            console.print(f"[yellow]Warning: Session {session_id} not found[/yellow]")
            return None

        session = self.sessions[session_id]
        path = self._session_file(session_id)

        with path.open("w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)

        return path

    def export_session(self, session_id: str, format: str = "json") -> Optional[str]:
        """Export a session in the specified format."""
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        if format == "json":
            return json.dumps(session.to_dict(), ensure_ascii=False, indent=2)
        elif format == "text":
            # Create human-readable text format
            lines = [
                f"Session: {session.session_id}",
                f"Prompt: {session.prompt}",
                f"Philosophers: {', '.join(session.philosophers)}",
                f"Created: {session.created_at}",
                "",
                "Metrics:",
            ]
            for key, value in session.metrics.items():
                lines.append(f"  {key}: {value}")

            lines.append("")
            lines.append(f"Events ({len(session.events)}):")
            for event in session.events:
                lines.append(f"  [{event.timestamp}] {event.event_type.value} from {event.source}")
                if event.data:
                    lines.append(f"    Data: {json.dumps(event.data, ensure_ascii=False)}")

            return "\n".join(lines)
        else:
            raise ValueError(f"Unknown format: {format}")

    def build_trace(self, response: "PoSelfResponse") -> TraceRecord:
        """PoSelfResponse から TraceRecord を構築する"""

        # trace_id はとりあえずタイムスタンプ＋簡易カウンタみたいなものにしておく
        now = datetime.utcnow()
        trace_id = now.strftime("%Y%m%dT%H%M%S%fZ")
        created_at = now.isoformat() + "Z"

        header = TraceHeader(
            trace_id=trace_id,
            created_at=created_at,
            prompt=response.prompt,
            philosophers=response.philosophers,
            consensus_leader=response.consensus_leader,
            metrics=response.metrics,
        )

        return TraceRecord(
            header=header,
            text=response.text,
            responses=response.responses,
            log=response.log,
        )

    def save_trace(self, record: TraceRecord) -> Path:
        """TraceRecord を JSON ファイルとして保存して、パスを返す"""

        path = self.trace_dir / f"{record.header.trace_id}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)
        return path


@click.command()
@click.argument("prompt", nargs=-1)
@click.option(
    "--trace-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=DEFAULT_TRACE_DIR,
    help="Directory to store trace JSON files.",
)
def cli(prompt: List[str], trace_dir: Path) -> None:
    """Run the Po_self ensemble and persist a reasoning trace."""
    # Import at runtime to avoid circular import
    from po_core.po_self import PoSelf, PoSelfResponse

    text_prompt = " ".join(prompt).strip()
    if not text_prompt:
        console.print(
            "[red]No prompt provided.[/red] "
            "Usage: po-core trace \"What is meaning?\""
        )
        raise SystemExit(1)

    console.print("[bold magenta]🧠 Po_self x Po_trace[/bold magenta]")
    console.print(f"[cyan]Prompt:[/cyan] {text_prompt}")

    # 1. Po_self を実行
    po_self = PoSelf()
    response: PoSelfResponse = po_self.generate(text_prompt)

    # 2. トレースを構築・保存
    tracer = PoTrace(trace_dir=trace_dir)
    record = tracer.build_trace(response)
    path = tracer.save_trace(record)

    console.print(
        f"[green]Trace saved:[/green] {path} "
        f"(trace_id={record.header.trace_id})"
    )

    # 3. ついでに要約だけ標準出力に出す
    console.print("\n[bold]Final text:[/bold]")
    console.print(response.text)
    console.print("\n[bold]Metrics:[/bold] " + repr(response.metrics))


if __name__ == "__main__":
    cli()