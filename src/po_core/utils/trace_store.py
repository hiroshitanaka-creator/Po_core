"""
Persistence utilities for Po_trace sessions.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from po_core.po_trace.models import TraceSession


class TraceStore:
    """JSONL-based persistence with lightweight rotation."""

    def __init__(
        self,
        base_path: Path | str | None = None,
        *,
        max_bytes: int = 1_000_000,
        max_files: int = 5,
    ) -> None:
        self.base_path = Path(base_path) if base_path else Path.cwd() / "trace_logs"
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_path / "traces.jsonl"
        self.max_bytes = max_bytes
        self.max_files = max_files

    def append(self, session: TraceSession) -> Path:
        """Append a session to the JSONL file and rotate if needed."""

        self._rotate_if_needed()
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(session.model_dump_json())
            f.write("\n")
        return self.file_path

    def load_all(self) -> List[TraceSession]:
        """Load all sessions from the primary JSONL file."""

        sessions: List[TraceSession] = []
        if not self.file_path.exists():
            return sessions

        with self.file_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    sessions.append(TraceSession.model_validate_json(line))
        return sessions

    def _rotate_if_needed(self) -> None:
        if self.file_path.exists() and self.file_path.stat().st_size > self.max_bytes:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            archived = self.base_path / f"traces_{timestamp}.jsonl"
            self.file_path.rename(archived)
            self._cleanup_archives()

    def _cleanup_archives(self) -> None:
        archives = sorted(self._archive_files(), key=lambda p: p.stat().st_mtime, reverse=True)
        for stale in archives[self.max_files - 1 :]:
            stale.unlink(missing_ok=True)

    def _archive_files(self) -> Iterable[Path]:
        return self.base_path.glob("traces_*.jsonl")


__all__ = ["TraceStore"]
