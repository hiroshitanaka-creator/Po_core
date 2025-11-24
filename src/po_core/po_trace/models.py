"""
Data models for Po_trace entries and sessions.

These pydantic models describe the structured trace events emitted by
``Po_self`` during reasoning.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TensorSnapshot(BaseModel):
    """Lightweight view of a tensor-like structure."""

    name: str = Field(..., description="Identifier for the tensor")
    shape: List[int] = Field(..., description="Tensor dimensions")
    summary: List[float] = Field(..., description="Compact numeric summary")


class TraceEntry(BaseModel):
    """Single reasoning step captured in the trace."""

    step: int = Field(..., description="Ordinal step in the reasoning chain")
    spoken_text: str = Field(..., description="Text that was surfaced")
    suppressed_text: Optional[str] = Field(
        None, description="Text or ideas that were held back"
    )
    philosopher_weights: Dict[str, float] = Field(
        default_factory=dict,
        description="Relative influence of each philosopher at this step",
    )
    tensors: List[TensorSnapshot] = Field(
        default_factory=list, description="Tensor states relevant to this step"
    )
    freedom_pressure: float = Field(
        ..., description="Constraint pressure on generative freedom"
    )
    semantic_delta: float = Field(
        ..., description="Magnitude of meaning change between steps"
    )
    timestamp: datetime = Field(..., description="UTC timestamp of the event")


class TraceSession(BaseModel):
    """Full trace for a single prompt execution."""

    session_id: str = Field(..., description="Unique identifier for the session")
    prompt: str = Field(..., description="Original user prompt")
    spoken_summary: str = Field(..., description="Final surfaced text")
    created_at: datetime = Field(..., description="Session start time (UTC)")
    completed_at: datetime = Field(..., description="Session end time (UTC)")
    entries: List[TraceEntry] = Field(
        default_factory=list, description="Ordered trace entries"
    )

    def summary_rows(self) -> List[List[str]]:
        """Return concise summary rows for CLI presentation."""

        return [
            [
                str(entry.step),
                f"{entry.freedom_pressure:.2f}",
                f"{entry.semantic_delta:.2f}",
                entry.spoken_text,
            ]
            for entry in self.entries
        ]


__all__ = [
    "TensorSnapshot",
    "TraceEntry",
    "TraceSession",
]
