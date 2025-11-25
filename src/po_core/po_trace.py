"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process,
including what was said and what was not said.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import json

import click
from rich.console import Console
from rich.table import Table

console = Console()


class TraceLevel(str, Enum):
    """Levels of trace detail supported by the audit log."""

    CONCISE = "concise"
    VERBOSE = "verbose"
    DEBUG = "debug"


@dataclass
class ReasonLog:
    """Explanation for why a piece of content was emitted."""

    philosopher: str
    reason: str
    channel: str = "analysis"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "philosopher": self.philosopher,
            "reason": self.reason,
            "channel": self.channel,
        }


@dataclass
class RejectionLog:
    """Record of content that was suppressed or rejected."""

    philosopher: str
    content: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "philosopher": self.philosopher,
            "content": self.content,
            "rationale": self.rationale,
        }


@dataclass
class PhilosopherAttribution:
    """Contribution weight for a philosopher."""

    philosopher: str
    weight: float
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "philosopher": self.philosopher,
            "weight": round(self.weight, 2),
            "note": self.note,
        }


@dataclass
class TraceEvent:
    """Generic trace event with timestamped metadata."""

    event: str
    metadata: Dict[str, Any]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event": self.event,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class PoTrace:
    """Audit log container capturing emitted and suppressed reasoning."""

    prompt: str
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z"
    )
    events: List[TraceEvent] = field(default_factory=list)
    reasons: List[ReasonLog] = field(default_factory=list)
    rejections: List[RejectionLog] = field(default_factory=list)
    attributions: List[PhilosopherAttribution] = field(default_factory=list)
    emissions: List[Dict[str, Any]] = field(default_factory=list)

    def record_event(self, event: str, **metadata: Any) -> None:
        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        self.events.append(TraceEvent(event=event, metadata=metadata, timestamp=timestamp))

    def log_reason(self, philosopher: str, reason: str, *, channel: str = "analysis") -> None:
        self.reasons.append(ReasonLog(philosopher=philosopher, reason=reason, channel=channel))

    def log_rejection(self, philosopher: str, content: str, rationale: str) -> None:
        self.rejections.append(
            RejectionLog(philosopher=philosopher, content=content, rationale=rationale)
        )

    def attribute(self, philosopher: str, weight: float, note: str) -> None:
        self.attributions.append(
            PhilosopherAttribution(philosopher=philosopher, weight=weight, note=note)
        )

    def record_emission(self, philosopher: str, content: str, *, channel: str = "analysis") -> None:
        self.emissions.append(
            {
                "philosopher": philosopher,
                "channel": channel,
                "content": content,
            }
        )

    def to_dict(self, level: TraceLevel = TraceLevel.CONCISE) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "prompt": self.prompt,
            "created_at": self.created_at,
            "level": level.value,
            "events": [event.to_dict() for event in self.events],
            "attributions": [attr.to_dict() for attr in self.attributions],
        }

        if level in {TraceLevel.VERBOSE, TraceLevel.DEBUG}:
            base.update(
                {
                    "emissions": list(self.emissions),
                    "reasons": [reason.to_dict() for reason in self.reasons],
                }
            )

        if level == TraceLevel.DEBUG:
            base.update({"rejections": [rej.to_dict() for rej in self.rejections]})

        return base

    def export(self, destination: Optional[str], level: TraceLevel = TraceLevel.CONCISE) -> None:
        """Persist the trace to a file if a destination is provided."""

        if not destination:
            return

        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(level=level), indent=2))


@click.command()
@click.option(
    "--trace-level",
    type=click.Choice([member.value for member in TraceLevel]),
    default=TraceLevel.CONCISE.value,
    show_default=True,
    help="Level of detail to show (concise, verbose, debug).",
)
@click.option(
    "--from-file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Inspect a saved Po_trace JSON file instead of running a trace.",
)
@click.option(
    "--summary/--no-summary",
    default=True,
    show_default=True,
    help="Show the attribution summary table.",
)
@click.argument("prompt", required=False)
def cli(trace_level: str, from_file: Optional[Path], summary: bool, prompt: Optional[str]) -> None:
    """Po_trace CLI entry point.

    When given a PROMPT, a placeholder deterministic trace is generated. If
    --from-file is supplied, the CLI will render the stored trace instead.
    """

    selected_level = TraceLevel(trace_level)

    if from_file:
        trace_data = json.loads(from_file.read_text())
    else:
        demo_trace = PoTrace(prompt or "demo")
        demo_trace.record_event("trace_preview_started", source="cli")
        demo_trace.attribute("preview_philosopher", 1.0, "Full contribution")
        demo_trace.record_emission("preview_philosopher", f"Reflection on '{prompt or 'demo'}'.")
        demo_trace.log_rejection(
            "preview_philosopher",
            content="Omitted speculative aside.",
            rationale="Kept the preview concise.",
        )
        demo_trace.record_event("trace_preview_finished", status="ok")
        trace_data = demo_trace.to_dict(level=selected_level)

    console.print("[bold green]\n🔍 Po_trace - Reasoning Audit Log\n")
    console.print(f"Level: [bold]{selected_level.value}[/bold]")

    if summary:
        _render_summary(trace_data)

    console.print("\n[dim]Full trace JSON:[/dim]")
    console.print_json(data=trace_data)


def _render_summary(trace_data: Dict[str, Any]) -> None:
    """Render a compact summary of attributions."""

    table = Table(title="Philosopher Attribution", show_lines=True)
    table.add_column("Philosopher", justify="left")
    table.add_column("Weight", justify="center")
    table.add_column("Note", justify="left")

    for attribution in trace_data.get("attributions", []):
        table.add_row(
            attribution.get("philosopher", ""),
            str(attribution.get("weight", "")),
            attribution.get("note", ""),
        )

    console.print(table)


if __name__ == "__main__":
    cli()
