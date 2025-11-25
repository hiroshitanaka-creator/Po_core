"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process,
including what was said and what was not said.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Dict, Iterable, List, Optional

import click
from rich.console import Console

console = Console()

DEFAULT_TRACE_PATH = Path("po_trace.ndjson")


def _iso_now() -> str:
    """Return an ISO 8601 timestamp with UTC marker."""

    return datetime.utcnow().isoformat() + "Z"


def _parse_timestamp(timestamp: str) -> datetime:
    """Parse ISO 8601 timestamps that may end with a Z suffix."""

    cleaned = timestamp.replace("Z", "+00:00")
    return datetime.fromisoformat(cleaned)


@dataclass
class PoTrace:
    """Runtime reasoning trace for Po_core executions."""

    prompt: str
    sink_path: Path = field(default_factory=lambda: Path(os.getenv("PO_TRACE_PATH", DEFAULT_TRACE_PATH)))
    created_at: str = field(default_factory=_iso_now)
    inputs: Dict[str, Any] = field(default_factory=dict)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    blocked_tensors: List[Dict[str, Any]] = field(default_factory=list)
    outputs: Dict[str, Any] = field(default_factory=dict)
    freedom_pressure: List[Dict[str, Any]] = field(default_factory=list)

    _memory_sink: ClassVar[List[Dict[str, Any]]] = []

    def __post_init__(self) -> None:
        if self.sink_path is None:
            self.sink_path = Path(os.getenv("PO_TRACE_PATH", DEFAULT_TRACE_PATH))
        else:
            self.sink_path = Path(self.sink_path)

    def record_input(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record initial input metadata."""

        if metadata:
            self.inputs.update(metadata)

    def add_philosopher_step(
        self,
        name: str,
        contribution: Dict[str, Any],
        *,
        freedom_pressure: Optional[float] = None,
        blocked_tensors: Optional[Iterable[str]] = None,
    ) -> None:
        """Add a philosopher reasoning step."""

        step = {
            "philosopher": name,
            "contribution": contribution,
            "timestamp": _iso_now(),
        }
        if freedom_pressure is not None:
            step["freedom_pressure"] = freedom_pressure
            self.freedom_pressure.append({"philosopher": name, "value": freedom_pressure})

        blocked_entries = list(blocked_tensors or [])
        if blocked_entries:
            step["blocked_tensors"] = blocked_entries
            for tensor in blocked_entries:
                self.block_tensor(tensor, f"Blocked within step for {name}")

        self.steps.append(step)

    def block_tensor(self, tensor: str, reason: str) -> None:
        """Record a blocked tensor event."""

        self.blocked_tensors.append(
            {
                "tensor": tensor,
                "reason": reason,
                "timestamp": _iso_now(),
            }
        )

    def set_outputs(self, outputs: Dict[str, Any]) -> None:
        """Record final outputs for the trace."""

        self.outputs = outputs

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable dictionary representation of the trace."""

        return {
            "prompt": self.prompt,
            "created_at": self.created_at,
            "inputs": self.inputs,
            "steps": self.steps,
            "blocked_tensors": self.blocked_tensors,
            "freedom_pressure": self.freedom_pressure,
            "outputs": self.outputs,
            "sink_path": str(self.sink_path),
        }

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        """Return a JSON string representation."""

        return json.dumps(self.to_dict(), indent=indent)

    def to_ndjson(self) -> str:
        """Return an NDJSON line for the trace."""

        return json.dumps(self.to_dict())

    def persist(self) -> Dict[str, Any]:
        """Persist the trace to the configured sink and in-memory cache."""

        payload = self.to_dict()
        type(self)._memory_sink.append(payload)
        self.sink_path.parent.mkdir(parents=True, exist_ok=True)
        with self.sink_path.open("a", encoding="utf-8") as sink:
            sink.write(self.to_ndjson() + "\n")
        return payload

    @classmethod
    def latest(cls, sink_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """Load the most recent trace from memory or disk."""

        if cls._memory_sink:
            return cls._memory_sink[-1]

        path = Path(sink_path) if sink_path is not None else Path(os.getenv("PO_TRACE_PATH", DEFAULT_TRACE_PATH))
        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as source:
            lines = [line.strip() for line in source if line.strip()]
        if not lines:
            return None
        return json.loads(lines[-1])


def filter_trace_data(
    trace: Dict[str, Any], *, philosopher: Optional[str] = None, since: Optional[str] = None
) -> Dict[str, Any]:
    """Return a filtered copy of a trace based on philosopher and timestamp."""

    since_dt = _parse_timestamp(since) if since else None

    def _passes_time(timestamp: Optional[str]) -> bool:
        if not since_dt or not timestamp:
            return True
        try:
            return _parse_timestamp(timestamp) >= since_dt
        except ValueError:
            return False

    filtered = dict(trace)
    filtered_steps = []
    for step in trace.get("steps", []):
        if philosopher and step.get("philosopher") != philosopher:
            continue
        if not _passes_time(step.get("timestamp")):
            continue
        filtered_steps.append(step)

    filtered_blocked = []
    for event in trace.get("blocked_tensors", []):
        if philosopher and philosopher not in event.get("tensor", ""):
            # If tensor name embeds philosopher, respect filter; otherwise include when no philosopher filter
            continue
        if not _passes_time(event.get("timestamp")):
            continue
        filtered_blocked.append(event)

    filtered_pressure = []
    for entry in trace.get("freedom_pressure", []):
        if philosopher and entry.get("philosopher") != philosopher:
            continue
        filtered_pressure.append(entry)

    filtered["steps"] = filtered_steps
    filtered["blocked_tensors"] = filtered_blocked
    filtered["freedom_pressure"] = filtered_pressure
    return filtered


def cli() -> None:
    """Po_trace CLI entry point"""

    console.print("[bold green]🔍 Po_trace - Reasoning Audit Log[/bold green]")
    latest_trace = PoTrace.latest()
    if not latest_trace:
        console.print("No traces recorded yet.")
        return

    console.print(latest_trace)


if __name__ == "__main__":
    cli()
