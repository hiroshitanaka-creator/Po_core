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

    @property
    def storage_dir(self) -> Path:
        """Alias for trace_dir for backward compatibility."""
        return self.trace_dir

    def _session_file(self, session_id: str) -> Path:
        """Get the file path for a session."""
        return self.trace_dir / f"session_{session_id}.json"

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