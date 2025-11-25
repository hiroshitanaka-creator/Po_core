"""
Po_trace: Reasoning Audit Log Module.

Provides structured Reason Log entries that capture how Po_self made
decisions, what alternatives were suppressed, and when events occurred.
The format is intentionally deterministic to keep tests stable while
following the Reason Log design guidelines.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, List, Mapping, MutableMapping, TextIO

DEFAULT_TIME = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
TimeProvider = Callable[[], datetime]


def _format_timestamp(moment: datetime) -> str:
    """Return an ISO-8601 timestamp with a Z suffix."""

    return moment.isoformat().replace("+00:00", "Z")


@dataclass
class TraceEvent:
    """Individual event within the Reason Log."""

    event: str
    timestamp: str
    decision: str | None = None
    suppressed: List[str] = field(default_factory=list)
    metadata: Mapping[str, object] | None = None

    def to_dict(self) -> MutableMapping[str, object]:
        payload: MutableMapping[str, object] = {
            "event": self.event,
            "timestamp": self.timestamp,
            "suppressed": self.suppressed,
        }
        if self.decision:
            payload["decision"] = self.decision
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


class PoTrace:
    """Structured Reason Log builder and serializer."""

    def __init__(
        self,
        prompt: str,
        philosophers: Iterable[str],
        *,
        time_provider: TimeProvider | None = None,
    ) -> None:
        self.prompt = prompt
        self.philosophers = list(philosophers)
        self._now = time_provider or (lambda: DEFAULT_TIME)
        self.created_at = _format_timestamp(self._now())
        self._events: List[TraceEvent] = []

    def _timestamp(self) -> str:
        return _format_timestamp(self._now())

    def record_event(
        self,
        event: str,
        *,
        decision: str | None = None,
        suppressed: Iterable[str] | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> TraceEvent:
        """Add a Reason Log entry and return it."""

        entry = TraceEvent(
            event=event,
            timestamp=self._timestamp(),
            decision=decision,
            suppressed=list(suppressed or []),
            metadata=metadata,
        )
        self._events.append(entry)
        return entry

    def events(self) -> List[Mapping[str, object]]:
        """Return the recorded events as dictionaries."""

        return [event.to_dict() for event in self._events]

    def to_dict(self) -> MutableMapping[str, object]:
        """Serialize the Reason Log to a dictionary."""

        return {
            "prompt": self.prompt,
            "philosophers": self.philosophers,
            "created_at": self.created_at,
            "events": self.events(),
        }

    def to_json(self, *, indent: int = 2) -> str:
        """Render the Reason Log as JSON."""

        return json.dumps(self.to_dict(), indent=indent)

    def stream(self, target: str | Path | TextIO) -> None:
        """Write the Reason Log to a file path or file-like object."""

        payload = self.to_json()
        if isinstance(target, (str, Path)):
            Path(target).write_text(payload, encoding="utf-8")
        else:
            target.write(payload)
            target.write("\n")


__all__ = ["PoTrace", "TraceEvent", "DEFAULT_TIME"]
