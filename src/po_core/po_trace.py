"""Po_trace: Reasoning Audit Log Module.

Tracks and logs the complete reasoning process, including what was said and
what was not said. Provides a CLI for inspecting the latest reasoning runs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


def _now() -> str:
    """Return an ISO-8601 timestamp with UTC timezone indicator."""

    return datetime.utcnow().isoformat() + "Z"


@dataclass
class TraceEvent:
    """Represents a single trace event within a reasoning run."""

    event: str
    timestamp: str
    philosopher: Optional[str] = None
    status: Optional[str] = None
    data: Dict[str, object] = field(default_factory=dict)


@dataclass
class TraceArtifact:
    """Captures intermediate reasoning artifacts produced during a run."""

    label: str
    content: str
    timestamp: str
    philosopher: Optional[str] = None


class PoTraceRecorder:
    """In-memory recorder for reasoning audit logs."""

    def __init__(self) -> None:
        self._runs: List[Dict[str, object]] = []
        self._next_id = 1

    # Public API -----------------------------------------------------------
    def reset(self) -> None:
        """Reset all stored runs (intended for tests)."""

        self._runs.clear()
        self._next_id = 1

    def start_run(self, prompt: str, philosophers: Iterable[str]) -> int:
        """Register a new run and return its identifier."""

        run = {
            "id": self._next_id,
            "prompt": prompt,
            "philosophers": list(philosophers),
            "status": "running",
            "started_at": _now(),
            "events": [],
            "artifacts": [],
        }
        self._next_id += 1
        self._runs.append(run)

        self.log_event(run["id"], "ensemble_started", philosophers=len(run["philosophers"]))
        return run["id"]

    def log_event(
        self,
        run_id: int,
        event: str,
        philosopher: Optional[str] = None,
        status: Optional[str] = None,
        **data: object,
    ) -> None:
        """Record an event within a run."""

        run = self._get_run(run_id)
        trace_event = TraceEvent(
            event=event,
            timestamp=_now(),
            philosopher=philosopher,
            status=status,
            data=data,
        )
        run["events"].append(self._event_to_dict(trace_event))

        if status:
            run["status"] = status

    def log_artifact(
        self,
        run_id: int,
        label: str,
        content: str,
        philosopher: Optional[str] = None,
    ) -> None:
        """Record an intermediate reasoning artifact for a run."""

        run = self._get_run(run_id)
        artifact = TraceArtifact(
            label=label,
            content=content,
            timestamp=_now(),
            philosopher=philosopher,
        )
        run["artifacts"].append(self._artifact_to_dict(artifact))

    def complete_run(self, run_id: int, status: str = "ok", **data: object) -> None:
        """Mark a run as completed and add a closing event."""

        run = self._get_run(run_id)
        run["completed_at"] = _now()
        run["status"] = status
        self.log_event(run_id, "ensemble_completed", status=status, **data)

    def snapshot(self, run_id: int) -> Dict[str, object]:
        """Return a deep-ish copy of a run suitable for export."""

        run = self._get_run(run_id)
        return json.loads(json.dumps(run))

    def recent_runs(
        self,
        *,
        limit: int = 5,
        prompt_filter: Optional[str] = None,
        philosopher_filter: Optional[Iterable[str]] = None,
        status_filter: Optional[str] = None,
    ) -> List[Dict[str, object]]:
        """Return the most recent runs filtered by prompt, philosopher, or status."""

        filtered: List[Dict[str, object]] = []
        philosopher_targets = None
        if philosopher_filter:
            philosopher_targets = {item.lower() for item in philosopher_filter}

        for run in reversed(self._runs):
            if prompt_filter and prompt_filter.lower() not in run["prompt"].lower():
                continue

            if status_filter and run.get("status", "").lower() != status_filter.lower():
                continue

            if philosopher_targets and not self._run_has_philosopher(run, philosopher_targets):
                continue

            filtered.append(self.snapshot(run["id"]))
            if len(filtered) >= limit:
                break

        return filtered

    # Internal helpers -----------------------------------------------------
    def _event_to_dict(self, event: TraceEvent) -> Dict[str, object]:
        payload = {
            "event": event.event,
            "timestamp": event.timestamp,
        }
        if event.philosopher:
            payload["philosopher"] = event.philosopher
        if event.status:
            payload["status"] = event.status
        if event.data:
            payload["data"] = event.data
            for key, value in event.data.items():
                payload.setdefault(key, value)
        return payload

    def _artifact_to_dict(self, artifact: TraceArtifact) -> Dict[str, object]:
        payload = {
            "label": artifact.label,
            "content": artifact.content,
            "timestamp": artifact.timestamp,
        }
        if artifact.philosopher:
            payload["philosopher"] = artifact.philosopher
        return payload

    def _get_run(self, run_id: int) -> Dict[str, object]:
        for run in reversed(self._runs):
            if run["id"] == run_id:
                return run
        raise KeyError(f"Run with id {run_id} not found")

    def _run_has_philosopher(self, run: Dict[str, object], targets: set[str]) -> bool:
        participants = {p.lower() for p in run.get("philosophers", [])}
        for event in run.get("events", []):
            philosopher = event.get("philosopher")
            if philosopher:
                participants.add(philosopher.lower())

        for artifact in run.get("artifacts", []):
            philosopher = artifact.get("philosopher")
            if philosopher:
                participants.add(philosopher.lower())

        return bool(participants & targets)


trace_recorder = PoTraceRecorder()


def _format_runs_text(runs: List[Dict[str, object]]) -> str:
    """Render a human-readable representation of recent runs."""

    if not runs:
        return "No reasoning logs found. Try running the ensemble first."

    blocks = []
    for run in runs:
        lines = [
            f"Run #{run['id']} — Status: {run.get('status', 'unknown')}",
            f"Prompt: {run['prompt']}",
            f"Philosophers: {', '.join(run.get('philosophers', []))}",
            f"Started: {run.get('started_at', 'n/a')}",
            f"Completed: {run.get('completed_at', 'incomplete')}",
            "Events:",
        ]

        for event in run.get("events", []):
            philosopher = event.get("philosopher")
            parts = [f"- [{event['timestamp']}] {event['event']}"]
            if philosopher:
                parts.append(f"({philosopher})")
            status = event.get("status")
            if status:
                parts.append(f"status={status}")
            data = event.get("data")
            if data:
                parts.append(f"data={data}")
            lines.append(" ".join(parts))

        if run.get("artifacts"):
            lines.append("Artifacts:")
            for artifact in run["artifacts"]:
                actor = artifact.get("philosopher", "n/a")
                lines.append(
                    f"- [{artifact['timestamp']}] {artifact['label']} by {actor}: {artifact['content']}"
                )

        blocks.append("\n".join(lines))

    return "\n\n".join(blocks)


@click.command()
@click.option("--limit", default=5, show_default=True, help="Number of runs to display")
@click.option("--prompt", "prompt_filter", default=None, help="Filter by prompt substring")
@click.option(
    "--philosopher",
    "philosopher_filter",
    multiple=True,
    help="Filter by philosopher involvement",
)
@click.option(
    "--status",
    "status_filter",
    type=click.Choice(["ok", "error", "running"], case_sensitive=False),
    default=None,
    help="Filter by run status",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    show_default=True,
    help="Choose between text or JSON output.",
)
def cli(
    *,
    limit: int,
    prompt_filter: Optional[str],
    philosopher_filter: Iterable[str],
    status_filter: Optional[str],
    output_format: str,
) -> None:
    """Po_trace CLI entry point."""

    runs = trace_recorder.recent_runs(
        limit=limit,
        prompt_filter=prompt_filter,
        philosopher_filter=philosopher_filter,
        status_filter=status_filter,
    )

    console.print("[bold green]🔍 Po_trace - Reasoning Audit Log[/bold green]")

    if output_format.lower() == "json":
        console.print(json.dumps(runs, indent=2))
        return

    console.print(Panel(_format_runs_text(runs), expand=False))


if __name__ == "__main__":
    cli()
