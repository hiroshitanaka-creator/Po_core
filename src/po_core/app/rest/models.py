"""
API Request/Response Models
============================

Pydantic v2 models for all REST API endpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# POST /v1/reason
# ---------------------------------------------------------------------------


class ReasonRequest(BaseModel):
    """Request body for the reasoning endpoint."""

    input: str = Field(
        ...,
        min_length=1,
        max_length=8192,
        description="The philosophical question or prompt to reason about.",
        examples=["What is justice?"],
    )
    session_id: Optional[str] = Field(
        default=None,
        description=(
            "Optional session identifier for memory continuity. "
            "A new UUID is generated if omitted."
        ),
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary key-value metadata attached to this request.",
    )


class PhilosopherContribution(BaseModel):
    """A single philosopher's contribution to the deliberation."""

    name: str
    proposal: str
    weight: float = Field(ge=0.0, le=1.0)


class TensorSnapshot(BaseModel):
    """Snapshot of tensor metrics computed during reasoning."""

    freedom_pressure: Optional[float] = None
    semantic_delta: Optional[float] = None
    blocked_tensor: Optional[float] = None


class ReasonResponse(BaseModel):
    """Response body from the reasoning endpoint."""

    request_id: str = Field(description="Unique ID for this request (UUID).")
    session_id: str = Field(description="Session ID used for this request.")
    status: str = Field(description="'approved' | 'blocked' | 'fallback'")
    response: str = Field(description="The synthesised philosophical response.")
    philosophers: List[PhilosopherContribution] = Field(
        default_factory=list,
        description="Top philosopher contributions.",
    )
    tensors: TensorSnapshot = Field(
        default_factory=TensorSnapshot,
        description="Tensor metrics computed during this turn.",
    )
    safety_mode: str = Field(
        default="NORMAL",
        description="SafetyMode active during this turn (NORMAL/WARN/CRITICAL).",
    )
    processing_time_ms: float = Field(
        description="Wall-clock time for this request in milliseconds."
    )
    created_at: datetime = Field(description="UTC timestamp of the response.")


# ---------------------------------------------------------------------------
# POST /v1/reason/stream  (SSE chunks)
# ---------------------------------------------------------------------------


class StreamChunk(BaseModel):
    """A single SSE chunk emitted during streaming reasoning."""

    chunk_type: str = Field(
        description="'event' | 'result' | 'error' | 'done'",
    )
    event_type: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# GET /v1/philosophers
# ---------------------------------------------------------------------------


class PhilosopherInfo(BaseModel):
    """Metadata about a single philosopher."""

    philosopher_id: str
    module: str
    symbol: str
    risk_level: int = Field(ge=0, le=2)
    weight: float
    enabled: bool
    tags: List[str]
    cost: int


class PhilosophersResponse(BaseModel):
    """Response body for the philosophers list endpoint."""

    total: int
    philosophers: List[PhilosopherInfo]


# ---------------------------------------------------------------------------
# GET /v1/trace/{session_id}
# ---------------------------------------------------------------------------


class TraceEventOut(BaseModel):
    """A single serialized TraceEvent."""

    event_type: str
    occurred_at: datetime
    correlation_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class TraceResponse(BaseModel):
    """Response body for the trace retrieval endpoint."""

    session_id: str
    event_count: int
    events: List[TraceEventOut]


# ---------------------------------------------------------------------------
# GET /v1/health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    """Response body for the health check endpoint."""

    status: str = Field(description="'ok' or 'degraded'")
    version: str
    philosophers_loaded: int
    uptime_seconds: float
