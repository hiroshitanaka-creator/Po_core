"""
Po_core REST API (Phase 5)
==========================

FastAPI application exposing po_core.run() as a production REST API.

Endpoints:
    POST /v1/reason              — synchronous reasoning
    POST /v1/reason/stream       — streaming via SSE
    GET  /v1/philosophers        — philosopher list
    GET  /v1/trace/{session_id}  — trace retrieval
    GET  /v1/health              — health check
"""

from po_core.app.rest.server import create_app

__all__ = ["create_app"]
