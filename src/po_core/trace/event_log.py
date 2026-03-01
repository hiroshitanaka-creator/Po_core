from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

_EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\-()\s]{8,}\d)")
_ADDRESS_RE = re.compile(
    r"\b(?:\d{1,4}\s+)?(?:[A-Za-z0-9\-]+\s)+(?:st|street|ave|avenue|rd|road|blvd|boulevard|city|ward|prefecture)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Event:
    """Single replayable audit event."""

    run_id: str
    timestamp: str
    stage: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "stage": self.stage,
            "payload": self.payload,
        }

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "Event":
        return Event(
            run_id=str(data.get("run_id", "")),
            timestamp=str(data.get("timestamp", "")),
            stage=str(data.get("stage", "")),
            payload=dict(data.get("payload", {})),
        )


def mask_sensitive_payload(payload: Any) -> Any:
    """Best-effort masking for common PII patterns in nested payloads."""
    if isinstance(payload, Mapping):
        return {str(k): mask_sensitive_payload(v) for k, v in payload.items()}
    if isinstance(payload, list):
        return [mask_sensitive_payload(v) for v in payload]
    if isinstance(payload, tuple):
        return [mask_sensitive_payload(v) for v in payload]
    if isinstance(payload, str):
        masked = _EMAIL_RE.sub("[MASKED_EMAIL]", payload)
        masked = _PHONE_RE.sub("[MASKED_PHONE]", masked)
        masked = _ADDRESS_RE.sub("[MASKED_ADDRESS]", masked)
        return masked
    return payload


class JsonlEventLogger:
    """Append-only JSONL logger for propose/critique/synthesize stages."""

    def __init__(self, base_dir: str | Path | None = None) -> None:
        self.base_dir = Path(base_dir or ".po_core_runs")

    def _event_path(self, run_id: str) -> Path:
        return self.base_dir / f"{run_id}.jsonl"

    def emit(self, run_id: str, stage: str, payload: Mapping[str, Any]) -> Event:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        event = Event(
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            stage=stage,
            payload=dict(mask_sensitive_payload(payload)),
        )

        path = self._event_path(run_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        return event

    def load(self, run_id: str) -> list[Event]:
        path = self._event_path(run_id)
        if not path.exists():
            return []

        events: list[Event] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                events.append(Event.from_dict(json.loads(line)))
        return events

    def iter_run_ids(self) -> Iterable[str]:
        if not self.base_dir.exists():
            return []
        return sorted(p.stem for p in self.base_dir.glob("*.jsonl"))
