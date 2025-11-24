"""Po_trace: Reasoning Audit Log Module.

Tracks and logs the complete reasoning process, including what was said and
what was not said.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

import click
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class TraceEvent:
    """An individual reasoning event in a trace log."""

    utterance: str
    philosophers: List[str]
    accepted: bool = True
    rejection_reason: Optional[str] = None
    comment: Optional[str] = None
    tension: Optional[float] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


def save_trace(
    events: Sequence[TraceEvent],
    path: Path | str,
    *,
    ndjson: bool = True,
) -> Path:
    """Save trace events to a JSON or NDJSON file."""

    trace_path = Path(path)
    trace_path.parent.mkdir(parents=True, exist_ok=True)

    if ndjson:
        trace_path.write_text(
            "\n".join(json.dumps(asdict(event), ensure_ascii=False) for event in events)
            + "\n",
            encoding="utf-8",
        )
    else:
        trace_path.write_text(
            json.dumps([asdict(event) for event in events], ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )

    return trace_path


def load_trace(path: Path | str) -> List[TraceEvent]:
    """Load trace events from a JSON or NDJSON file."""

    trace_path = Path(path)
    content = trace_path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    if content.startswith("["):
        data = json.loads(content)
    else:
        data = [json.loads(line) for line in content.splitlines() if line.strip()]

    events: List[TraceEvent] = []
    for item in data:
        events.append(
            TraceEvent(
                utterance=item.get("utterance", ""),
                philosophers=list(item.get("philosophers", [])),
                accepted=item.get("accepted", True),
                rejection_reason=item.get("rejection_reason"),
                comment=item.get("comment"),
                tension=item.get("tension"),
                timestamp=item.get("timestamp", datetime.now(timezone.utc).isoformat()),
            )
        )

    return events


def demo_trace_events() -> List[TraceEvent]:
    """Generate a short set of demo events for showcasing Po_trace."""

    return [
        TraceEvent(
            utterance="Prompt received: How do we balance freedom and responsibility?",
            philosophers=["System"],
            comment="Initial prompt",
            tension=0.1,
        ),
        TraceEvent(
            utterance="Authenticity emerges when choice meets responsibility.",
            philosophers=["Jean-Paul Sartre"],
            comment="Existential framing",
            tension=0.35,
        ),
        TraceEvent(
            utterance="The shadow reminds us that unowned duties return as projections.",
            philosophers=["Carl Jung"],
            comment="Depth psychology",
            tension=0.42,
        ),
        TraceEvent(
            utterance="Binary oppositions hide the play of différance.",
            philosophers=["Jacques Derrida"],
            accepted=False,
            rejection_reason="Too abstract for the user's immediate need",
            tension=0.55,
        ),
        TraceEvent(
            utterance="Synthesis: Freedom is lived as accountable improvisation.",
            philosophers=["Ensemble"],
            comment="Draft response",
            tension=0.28,
        ),
    ]


def render_trace(events: Sequence[TraceEvent]) -> None:
    """Render a trace log to the console."""

    table = Table(title="Po_trace Log", show_lines=True)
    table.add_column("Timestamp", style="dim", no_wrap=True)
    table.add_column("Philosophers")
    table.add_column("Utterance")
    table.add_column("Accepted", justify="center")
    table.add_column("Rejection Reason")
    table.add_column("Tension", justify="right")

    for event in events:
        table.add_row(
            event.timestamp,
            ", ".join(event.philosophers),
            event.utterance,
            "✅" if event.accepted else "❌",
            event.rejection_reason or "-",
            f"{event.tension:.2f}" if event.tension is not None else "-",
        )

    console.print(table)


@click.command()
@click.option(
    "--log",
    "log_path",
    default="po_trace_demo.jsonl",
    show_default=True,
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Path to save the trace log (JSONL).",
)
@click.option(
    "--json",
    "use_json",
    is_flag=True,
    default=False,
    help="Save as JSON array instead of NDJSON.",
)
def cli(log_path: Path, use_json: bool) -> None:
    """Generate and save a demo reasoning trace."""

    events = demo_trace_events()
    save_trace(events, log_path, ndjson=not use_json)
    console.print(
        f"[bold green]🔍 Po_trace[/bold green] wrote {len(events)} events to [cyan]{log_path}[/cyan]"
    )
    render_trace(events)


__all__ = [
    "TraceEvent",
    "save_trace",
    "load_trace",
    "demo_trace_events",
    "render_trace",
]

