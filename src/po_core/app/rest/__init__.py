"""
Po_core REST API (Phase 5)
==========================

FastAPI application exposing po_core.run() as a production REST API.

Endpoints:
    POST /v1/reason              — synchronous reasoning
    POST /v1/reason/stream       — streaming via SSE
    WS   /v1/ws/reason           — bidirectional streaming via WebSocket
    GET  /v1/philosophers        — philosopher list
    GET  /v1/trace/{session_id}  — trace retrieval
    GET  /v1/health              — health check
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI


def create_app(*args: Any, **kwargs: Any) -> FastAPI:
    """Lazily import the FastAPI app factory to avoid import cycles."""
    from po_core.app.rest.server import create_app as _create_app

    return _create_app(*args, **kwargs)


__all__ = ["create_app"]
