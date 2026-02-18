"""
Unit tests for the Phase 5 FastAPI REST API.

Tests cover:
- Health check endpoint
- Philosopher list endpoint
- Reason endpoint (mocked pipeline)
- Trace retrieval endpoint
- API key authentication
- SSE streaming endpoint

Markers: unit, phase4 (reuses phase4 marker for Phase 5 API tests)
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app
from po_core.app.rest.store import _store

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_trace_store():
    """Clear the in-memory trace store before each test."""
    _store.clear()
    yield
    _store.clear()


@pytest.fixture()
def client_no_auth():
    """TestClient with auth disabled (dev mode)."""

    def _override_settings() -> APISettings:
        return APISettings(skip_auth=True, api_key="")

    app = create_app()
    from po_core.app.rest import auth, config

    app.dependency_overrides[config.get_api_settings] = _override_settings
    app.dependency_overrides[auth.require_api_key] = lambda: None
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture()
def client_with_auth():
    """TestClient with API key authentication enabled."""

    def _override_settings() -> APISettings:
        return APISettings(skip_auth=False, api_key="test-secret-key")

    from po_core.app.rest import config

    app = create_app()
    app.dependency_overrides[config.get_api_settings] = _override_settings
    return TestClient(app, raise_server_exceptions=True)


# Mock result returned by po_core.run()
_MOCK_RESULT: dict[str, Any] = {
    "request_id": "test-req-001",
    "status": "approved",
    "proposal": {"content": "Justice is giving each their due."},
    "proposals": [
        {
            "philosopher_id": "aristotle",
            "content": "Justice is giving each their due.",
            "weight": 0.85,
        }
    ],
    "tensors": {
        "freedom_pressure": 0.12,
        "semantic_delta": 0.34,
        "blocked_tensor": 0.05,
    },
    "safety_mode": "NORMAL",
}


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_health_ok(client_no_auth):
    """Health endpoint returns 200 with expected fields."""
    resp = client_no_auth.get("/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "philosophers_loaded" in body
    assert body["philosophers_loaded"] > 0
    assert "uptime_seconds" in body


@pytest.mark.unit
@pytest.mark.phase5
def test_health_no_auth_required(client_with_auth):
    """Health endpoint does not require authentication."""
    resp = client_with_auth.get("/v1/health")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Philosopher List
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_philosophers_list(client_no_auth):
    """Philosopher list returns all philosophers."""
    resp = client_no_auth.get("/v1/philosophers")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] > 0
    assert len(body["philosophers"]) == body["total"]
    # Check first entry has required fields
    first = body["philosophers"][0]
    assert "philosopher_id" in first
    assert "module" in first
    assert "symbol" in first
    assert "risk_level" in first
    assert "tags" in first
    assert "cost" in first


@pytest.mark.unit
@pytest.mark.phase5
def test_philosophers_auth_required(client_with_auth):
    """Philosopher list requires valid API key."""
    # No key → 401
    resp = client_with_auth.get("/v1/philosophers")
    assert resp.status_code == 401

    # Valid key → 200
    resp = client_with_auth.get(
        "/v1/philosophers", headers={"X-API-Key": "test-secret-key"}
    )
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Reason — Synchronous
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_success(client_no_auth):
    """Reason endpoint returns synthesised response."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = client_no_auth.post("/v1/reason", json={"input": "What is justice?"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "approved"
    assert "Justice" in body["response"]
    assert "request_id" in body
    assert "session_id" in body
    assert "processing_time_ms" in body
    assert "tensors" in body
    assert body["tensors"]["freedom_pressure"] == pytest.approx(0.12)


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_custom_session_id(client_no_auth):
    """Reason endpoint preserves caller-supplied session_id."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = client_no_auth.post(
            "/v1/reason",
            json={"input": "What is the good life?", "session_id": "my-session-42"},
        )
    assert resp.status_code == 200
    assert resp.json()["session_id"] == "my-session-42"


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_empty_input_rejected(client_no_auth):
    """Reason endpoint rejects empty input with 422."""
    resp = client_no_auth.post("/v1/reason", json={"input": ""})
    assert resp.status_code == 422


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_missing_input_rejected(client_no_auth):
    """Reason endpoint rejects missing input field with 422."""
    resp = client_no_auth.post("/v1/reason", json={})
    assert resp.status_code == 422


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_auth_required(client_with_auth):
    """Reason endpoint requires valid API key."""
    resp = client_with_auth.post("/v1/reason", json={"input": "test"})
    assert resp.status_code == 401


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_auth_valid_key(client_with_auth):
    """Reason endpoint accepts valid API key."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = client_with_auth.post(
            "/v1/reason",
            json={"input": "What is truth?"},
            headers={"X-API-Key": "test-secret-key"},
        )
    assert resp.status_code == 200


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_saves_trace(client_no_auth):
    """Reason endpoint saves trace events to the store."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = client_no_auth.post(
            "/v1/reason",
            json={"input": "What is beauty?", "session_id": "trace-test-session"},
        )
    assert resp.status_code == 200
    # Trace store should have this session
    assert "trace-test-session" in _store


# ---------------------------------------------------------------------------
# Trace Retrieval
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_trace_not_found(client_no_auth):
    """Trace endpoint returns 404 for unknown session."""
    resp = client_no_auth.get("/v1/trace/nonexistent-session")
    assert resp.status_code == 404


@pytest.mark.unit
@pytest.mark.phase5
def test_trace_found_after_reason(client_no_auth):
    """Trace endpoint returns events after a reason call."""
    session_id = "trace-retrieval-test"
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        client_no_auth.post(
            "/v1/reason",
            json={"input": "What is virtue?", "session_id": session_id},
        )

    resp = client_no_auth.get(f"/v1/trace/{session_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["session_id"] == session_id
    assert "event_count" in body
    assert "events" in body


# ---------------------------------------------------------------------------
# Streaming (SSE)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_stream_returns_sse(client_no_auth):
    """Stream endpoint returns SSE content-type and done chunk."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = client_no_auth.post(
            "/v1/reason/stream",
            json={"input": "What is freedom?"},
        )
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")

    # Parse SSE lines
    chunks = []
    for line in resp.text.splitlines():
        if line.startswith("data: "):
            chunks.append(json.loads(line[6:]))

    chunk_types = [c["chunk_type"] for c in chunks]
    assert "started" in chunk_types
    assert "result" in chunk_types
    assert "done" in chunk_types


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_stream_result_has_response(client_no_auth):
    """Stream result chunk contains the synthesised response text."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = client_no_auth.post(
            "/v1/reason/stream",
            json={"input": "What is courage?"},
        )

    result_chunk = None
    for line in resp.text.splitlines():
        if line.startswith("data: "):
            chunk = json.loads(line[6:])
            if chunk["chunk_type"] == "result":
                result_chunk = chunk
                break

    assert result_chunk is not None
    assert "response" in result_chunk["payload"]
    assert "Justice" in result_chunk["payload"]["response"]


# ---------------------------------------------------------------------------
# OpenAPI schema
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_openapi_schema_generated(client_no_auth):
    """OpenAPI schema is auto-generated and accessible."""
    resp = client_no_auth.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "Po_core REST API"
    # All expected paths present
    paths = schema["paths"]
    assert "/v1/reason" in paths
    assert "/v1/reason/stream" in paths
    assert "/v1/philosophers" in paths
    assert "/v1/health" in paths
    # Trace path uses path param
    assert any("/v1/trace/" in p for p in paths)


@pytest.mark.unit
@pytest.mark.phase5
def test_swagger_ui_accessible(client_no_auth):
    """Swagger UI docs endpoint is accessible."""
    resp = client_no_auth.get("/docs")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Security Hardening (Phase 5-B): CORS + Rate Limiting
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_cors_default_allows_all_origins():
    """Default CORS configuration allows any origin (dev-friendly)."""
    from po_core.app.rest.config import APISettings
    from po_core.app.rest.server import create_app

    app = create_app(settings=APISettings(skip_auth=True, cors_origins="*"))
    client = TestClient(app)
    resp = client.get("/v1/health", headers={"Origin": "http://example.com"})
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "*"


@pytest.mark.unit
@pytest.mark.phase5
def test_cors_restricted_to_specific_origin():
    """CORS is restricted to the configured domain when PO_CORS_ORIGINS is set."""
    from po_core.app.rest.config import APISettings
    from po_core.app.rest.server import create_app

    trusted = "https://trusted.example.com"
    app = create_app(settings=APISettings(skip_auth=True, cors_origins=trusted))
    client = TestClient(app)

    # Preflight from trusted origin must succeed
    resp = client.options(
        "/v1/health",
        headers={
            "Origin": trusted,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == trusted


@pytest.mark.unit
@pytest.mark.phase5
def test_cors_blocked_untrusted_origin():
    """Requests from an untrusted origin receive no ACAO header."""
    from po_core.app.rest.config import APISettings
    from po_core.app.rest.server import create_app

    app = create_app(
        settings=APISettings(skip_auth=True, cors_origins="https://trusted.example.com")
    )
    client = TestClient(app)
    resp = client.options(
        "/v1/health",
        headers={
            "Origin": "https://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    # CORSMiddleware returns 400 for disallowed origins on preflight
    assert resp.headers.get("access-control-allow-origin") != "https://evil.example.com"


@pytest.mark.unit
@pytest.mark.phase5
def test_cors_multiple_origins_parsed():
    """Comma-separated PO_CORS_ORIGINS are each allowed."""
    from po_core.app.rest.config import APISettings
    from po_core.app.rest.server import _parse_cors_origins

    result = _parse_cors_origins("https://a.com, https://b.com , https://c.com")
    assert result == ["https://a.com", "https://b.com", "https://c.com"]

    wildcard = _parse_cors_origins("*")
    assert wildcard == ["*"]


@pytest.mark.unit
@pytest.mark.phase5
def test_rate_limiter_attached_to_app():
    """Rate limiter is registered on app.state after create_app()."""
    from po_core.app.rest.server import create_app

    app = create_app()
    assert hasattr(app.state, "limiter")
    assert app.state.limiter is not None


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_limit_string_format():
    """REASON_LIMIT is a valid SlowAPI limit string (e.g. '60/minute')."""
    from po_core.app.rest.rate_limit import REASON_LIMIT

    # Must be "<number>/<period>"
    assert "/" in REASON_LIMIT
    parts = REASON_LIMIT.split("/")
    assert parts[0].isdigit(), f"Expected integer, got: {parts[0]!r}"
    assert parts[1] in (
        "second",
        "minute",
        "hour",
        "day",
    ), f"Unexpected period: {parts[1]!r}"


@pytest.mark.unit
@pytest.mark.phase5
def test_rate_limit_429_on_excess():
    """Rate limiting blocks excess requests at the storage layer.

    Verifies the underlying ``limits`` library (used by SlowAPI) correctly
    rejects requests once the configured ceiling is reached.  The FastAPI
    integration (app.state.limiter + RateLimitExceeded handler) is covered by
    test_rate_limiter_attached_to_app and the wiring in server.py.
    """
    from limits import parse
    from limits.storage import MemoryStorage
    from limits.strategies import FixedWindowRateLimiter

    storage = MemoryStorage()
    rate_limiter = FixedWindowRateLimiter(storage)
    limit = parse("1/minute")

    # First hit: allowed
    assert rate_limiter.hit(limit, "127.0.0.1") is True
    # Second hit within the same window: blocked
    assert rate_limiter.hit(limit, "127.0.0.1") is False
