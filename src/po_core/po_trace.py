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
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import click
from rich.console import Console
from rich.table import Table

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from po_core.po_self import PoSelf, PoSelfResponse

console = Console()

# デフォルトのログ保存先（必要なら設定で変えられるようにしてもよい）
DEFAULT_TRACE_DIR = Path("traces")


class EventType(str, Enum):
    """Types of events that can be logged."""

    ENSEMBLE_STARTED = "ensemble_started"
    PHILOSOPHER_REASONING = "philosopher_reasoning"
    AGGREGATE_COMPUTED = "aggregate_computed"
    CONSENSUS_REACHED = "consensus_reached"
    EXECUTION = "execution"
    STATE_CHANGE = "state_change"
    ERROR = "error"
    USER_ACTION = "user_action"
    SYSTEM = "system"


@dataclass
class Event:
    """A single event in a reasoning session."""

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
    def from_dict(cls, data: Dict[str, Any]) -> Event:
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
    """A reasoning session with events and metrics."""

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
    def from_dict(cls, data: Dict[str, Any]) -> Session:
        """Create Session from dictionary."""
        events = [Event.from_dict(e) for e in data.get("events", [])]
        return cls(
            session_id=data["session_id"],
            prompt=data["prompt"],
            philosophers=data["philosophers"],
            created_at=data["created_at"],
            events=events,
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

    def __init__(self, trace_dir: Path | str = DEFAULT_TRACE_DIR) -> None:
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)

    def build_trace(self, response: PoSelfResponse) -> TraceRecord:
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

    text_prompt = " ".join(prompt).strip()
    if not text_prompt:
        console.print(
            "[red]No prompt provided.[/red] "
            "Usage: po-core trace \"What is meaning?\""
        )
        raise SystemExit(1)

    console.print("[bold magenta]🧠 Po_self x Po_trace[/bold magenta]")
    console.print(f"[cyan]Prompt:[/cyan] {text_prompt}")

    # Import here to avoid circular dependency at module level
    from po_core.po_self import PoSelf

    # 1. Po_self を実行
    po_self = PoSelf()
    response = po_self.generate(text_prompt)

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