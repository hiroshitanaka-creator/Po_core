"""Trace persistence and retrieval helpers."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TraceEntry:
    """A single recorded reasoning run.

    Attributes:
        timestamp: UTC timestamp of the run.
        prompt: Original prompt provided to the ensemble engine.
        context: Optional contextual metadata provided by the caller.
        result: Structured output returned by :class:`po_core.po_self.PoSelf`.
    """

    timestamp: str
    prompt: str
    context: Dict[str, Any]
    result: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


class PoTrace:
    """Persist and retrieve reasoning traces in JSONL format."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path) if path else Path("config/traces.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, prompt: str, context: Dict[str, Any], result: Dict[str, Any]) -> TraceEntry:
        """Append a reasoning trace to disk.

        Writes are flushed and ``fsync``'d to avoid partial writes in most
        environments.
        """

        entry = TraceEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            prompt=prompt,
            context=context,
            result=result,
            metadata={"philosophers": result.get("metadata", {}).get("philosophers", [])},
        )
        serialized = json.dumps(entry.__dict__, ensure_ascii=False)
        with open(self.path, "a", encoding="utf-8") as fp:
            fp.write(serialized + "\n")
            fp.flush()
            os.fsync(fp.fileno())
        return entry

    def iter_traces(self) -> Iterable[TraceEntry]:
        """Yield traces from the persistent store."""

        if not self.path.exists():
            return iter(())
        with open(self.path, "r", encoding="utf-8") as fp:
            for line in fp:
                if not line.strip():
                    continue
                data = json.loads(line)
                yield TraceEntry(**data)

    def list_traces(self, limit: Optional[int] = None) -> List[TraceEntry]:
        """Return recent traces, newest last."""

        traces = list(self.iter_traces())
        if limit is None or limit >= len(traces):
            return traces
        return traces[-limit:]

    def latest(self) -> Optional[TraceEntry]:
        """Return the most recent trace if available."""

        traces = self.list_traces(limit=1)
        return traces[0] if traces else None

    def get(self, index: int) -> Optional[TraceEntry]:
        """Retrieve a trace by zero-based index."""

        traces = self.list_traces()
        if index < 0 or index >= len(traces):
            return None
        return traces[index]
