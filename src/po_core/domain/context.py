"""
Context - 意思決定1回分のコンテキスト（監査の単位）。

This is what all layers receive as input.
It's immutable once created to ensure consistent reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class Context:
    """
    意思決定1回分のコンテキスト（監査の単位）。

    Attributes:
        request_id: Unique request identifier for tracing
        created_at: When this context was created (UTC)
        user_input: The user's input prompt (required)
        meta: Additional metadata (API/CLI/experiment differences isolated here)
    """

    request_id: str
    created_at: datetime
    user_input: str

    # 入口側が詰める任意メタ（API/CLI/実験などの差異はここに隔離）
    meta: Mapping[str, Any] = field(default_factory=dict)

    @staticmethod
    def now(
        request_id: str,
        user_input: str,
        meta: Optional[Mapping[str, Any]] = None,
    ) -> "Context":
        """Create a context with current timestamp."""
        return Context(
            request_id=request_id,
            created_at=datetime.now(timezone.utc),
            user_input=user_input,
            meta=dict(meta or {}),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "request_id": self.request_id,
            "created_at": self.created_at.isoformat(),
            "user_input": self.user_input,
            "meta": dict(self.meta),
        }


__all__ = ["Context"]
