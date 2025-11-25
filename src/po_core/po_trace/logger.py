"""Structured Po_trace logger producing JSON/NDJSON outputs."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from po_core.po_self import TensorEnsembleResult


@dataclass
class TraceEvent:
    timestamp: str
    kind: str
    payload: Dict[str, Any]


class PoTraceLogger:
    """Persist ensemble traces to disk in JSON or NDJSON form."""

    def __init__(self, path: Optional[Path] = None, *, ndjson: bool = True) -> None:
        self.path = path or Path("po_trace_run.ndjson" if ndjson else "po_trace_run.json")
        self.ndjson = ndjson
        self.events: list[TraceEvent] = []

    def record_prompt(self, prompt: str) -> None:
        self._append("prompt", {"prompt": prompt})

    def record_tensors(self, result: TensorEnsembleResult) -> None:
        self._append(
            "tensor_states",
            {
                "base_tensor": result.base_tensor.to_dict(),
                "philosopher_tensors": [tensor.to_dict() for tensor in result.philosopher_tensors],
                "composite_tensor": result.composite_tensor.to_dict() if result.composite_tensor else None,
            },
        )

    def record_contributions(self, notes: Iterable[str]) -> None:
        self._append("contributions", {"notes": list(notes)})

    def save(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.ndjson:
            content = "\n".join(json.dumps(asdict(event)) for event in self.events)
            self.path.write_text(content + "\n", encoding="utf-8")
        else:
            self.path.write_text(json.dumps([asdict(event) for event in self.events], indent=2), encoding="utf-8")
        return self.path

    def _append(self, kind: str, payload: Dict[str, Any]) -> None:
        self.events.append(
            TraceEvent(
                timestamp=datetime.utcnow().isoformat() + "Z",
                kind=kind,
                payload=payload,
            )
        )
