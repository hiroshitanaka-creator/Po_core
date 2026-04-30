"""Matrix tests for scope-based API key authorization.

Covers ``reason:write``, ``trace:read``, and ``review:write`` across:

- single-key mode (no per-scope env vars set): global ``PO_API_KEY`` works
  for every scope
- scope-key mode (any per-scope env var set): scope segmentation is enforced
  - the right scoped key is accepted
  - the global key is **rejected** unless explicitly listed under the scope
  - a key authorised for a *different* scope is rejected (no cross-scope
    leakage)

These tests guard the contract documented in
``po_core.app.rest.scopes`` after the redaction-auth-scope-fixes change
that removed the implicit "global key = super-key" behaviour in scope-key
mode.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.scopes import Scope, evaluate_scope_policy
from po_core.app.rest.server import create_app

GLOBAL_KEY = "global-key-xyz"
REASON_KEY = "reason-key-aaa"
TRACE_KEY = "trace-key-bbb"
REVIEW_KEY = "review-key-ccc"


# ---------------------------------------------------------------------------
# Unit-level matrix on evaluate_scope_policy
# ---------------------------------------------------------------------------


def _settings(**overrides: Any) -> APISettings:
    base = dict(
        skip_auth=False,
        api_key=GLOBAL_KEY,
        api_keys_reason_write="",
        api_keys_trace_read="",
        api_keys_review_write="",
    )
    base.update(overrides)
    return APISettings(**base)


@pytest.mark.parametrize(
    "scope",
    [Scope.REASON_WRITE, Scope.TRACE_READ, Scope.REVIEW_WRITE],
)
def test_single_key_mode_global_key_grants_every_scope(scope: str) -> None:
    """No scope env vars set → global key authorises every scope."""
    settings = _settings()
    decision = evaluate_scope_policy(
        settings=settings, presented_api_key=GLOBAL_KEY, scope=scope
    )
    assert decision.allowed is True


@pytest.mark.parametrize(
    "scope",
    [Scope.REASON_WRITE, Scope.TRACE_READ, Scope.REVIEW_WRITE],
)
def test_single_key_mode_wrong_key_rejected(scope: str) -> None:
    settings = _settings()
    decision = evaluate_scope_policy(
        settings=settings, presented_api_key="not-the-global-key", scope=scope
    )
    assert decision.allowed is False
    assert decision.is_misconfigured is False


@pytest.mark.parametrize(
    "scope, scope_key, key_setting",
    [
        (Scope.REASON_WRITE, REASON_KEY, "api_keys_reason_write"),
        (Scope.TRACE_READ, TRACE_KEY, "api_keys_trace_read"),
        (Scope.REVIEW_WRITE, REVIEW_KEY, "api_keys_review_write"),
    ],
)
def test_scope_mode_correct_scoped_key_allowed(
    scope: str, scope_key: str, key_setting: str
) -> None:
    """Scope-key mode: the key listed under the scope's env var is accepted."""
    settings = _settings(**{key_setting: scope_key})
    decision = evaluate_scope_policy(
        settings=settings, presented_api_key=scope_key, scope=scope
    )
    assert decision.allowed is True


@pytest.mark.parametrize(
    "scope, key_setting, scope_key",
    [
        (Scope.REASON_WRITE, "api_keys_reason_write", REASON_KEY),
        (Scope.TRACE_READ, "api_keys_trace_read", TRACE_KEY),
        (Scope.REVIEW_WRITE, "api_keys_review_write", REVIEW_KEY),
    ],
)
def test_scope_mode_global_key_no_longer_implicit_super_key(
    scope: str, key_setting: str, scope_key: str
) -> None:
    """Scope-key mode: the global key is rejected unless listed under the scope.

    This is the regression guard for the redaction-auth-scope-fixes change.
    Previously the global key authorised every scope even in scope-key mode,
    which silently defeated scope segmentation.
    """
    settings = _settings(**{key_setting: scope_key})
    decision = evaluate_scope_policy(
        settings=settings, presented_api_key=GLOBAL_KEY, scope=scope
    )
    assert decision.allowed is False


def test_scope_mode_global_key_works_when_explicitly_listed_under_scope() -> None:
    """If the operator lists the global key under a scope, it works for that scope."""
    settings = _settings(
        api_keys_reason_write=f"{GLOBAL_KEY},{REASON_KEY}",
    )
    decision = evaluate_scope_policy(
        settings=settings, presented_api_key=GLOBAL_KEY, scope=Scope.REASON_WRITE
    )
    assert decision.allowed is True


def test_scope_mode_no_cross_scope_leakage() -> None:
    """A reason:write-scoped key must not authorise trace:read or review:write."""
    settings = _settings(
        api_keys_reason_write=REASON_KEY,
        api_keys_trace_read=TRACE_KEY,
        api_keys_review_write=REVIEW_KEY,
    )

    for wrong_scope in (Scope.TRACE_READ, Scope.REVIEW_WRITE):
        decision = evaluate_scope_policy(
            settings=settings, presented_api_key=REASON_KEY, scope=wrong_scope
        )
        assert (
            decision.allowed is False
        ), f"reason key leaked into {wrong_scope} — scope segmentation broken"


def test_scope_mode_rejects_global_key_for_unconfigured_scope() -> None:
    """Once any scope env var is set, the global key alone never authorises an
    unconfigured scope — operators must explicitly list it under each scope
    they want it to grant.
    """
    settings = _settings(api_keys_reason_write=REASON_KEY)  # only reason configured

    decision = evaluate_scope_policy(
        settings=settings, presented_api_key=GLOBAL_KEY, scope=Scope.TRACE_READ
    )
    assert decision.allowed is False


# ---------------------------------------------------------------------------
# HTTP-level matrix via TestClient (covers reason:write + trace:read +
# review:write all the way through ``require_scope``)
# ---------------------------------------------------------------------------


def _build_client(tmp_path, **overrides: Any) -> TestClient:
    base = dict(
        skip_auth=False,
        api_key=GLOBAL_KEY,
        trace_store_backend="sqlite",
        trace_db_path=str(tmp_path / "trace_store.sqlite3"),
        review_store_backend="sqlite",
        review_db_path=str(tmp_path / "review_store.sqlite3"),
        api_keys_reason_write="",
        api_keys_trace_read="",
        api_keys_review_write="",
    )
    base.update(overrides)
    return TestClient(create_app(APISettings(**base)), raise_server_exceptions=True)


def _stub_reason_pipeline() -> Any:
    """Patch the heavy reasoning pipeline so HTTP auth tests stay fast."""
    return patch(
        "po_core.app.rest.routers.reason.po_run",
        return_value={
            "status": "ok",
            "proposal": {"content": "ok"},
            "proposals": [],
            "tensors": {},
            "safety_mode": "NORMAL",
            "request_id": "req-1",
        },
    )


def _async_stub_reason_pipeline() -> Any:
    return patch(
        "po_core.app.rest.routers.reason.po_async_run",
        new=AsyncMock(
            return_value={
                "status": "ok",
                "proposal": {"content": "ok"},
                "proposals": [],
                "tensors": {},
                "safety_mode": "NORMAL",
                "request_id": "req-1",
            }
        ),
    )


def test_http_single_key_mode_global_key_grants_every_endpoint(tmp_path) -> None:
    client = _build_client(tmp_path)

    with _stub_reason_pipeline():
        r = client.post(
            "/v1/reason",
            json={"input": "ping"},
            headers={"X-API-Key": GLOBAL_KEY},
        )
    assert r.status_code == 200, r.text

    r = client.get(
        "/v1/trace/history",
        headers={"X-API-Key": GLOBAL_KEY},
    )
    assert r.status_code == 200, r.text

    r = client.get(
        "/v1/review/pending",
        headers={"X-API-Key": GLOBAL_KEY},
    )
    assert r.status_code == 200, r.text


def test_http_scope_mode_scoped_key_grants_only_its_scope(tmp_path) -> None:
    client = _build_client(
        tmp_path,
        api_keys_reason_write=REASON_KEY,
        api_keys_trace_read=TRACE_KEY,
        api_keys_review_write=REVIEW_KEY,
    )

    # reason-scoped key works for /v1/reason …
    with _stub_reason_pipeline():
        r = client.post(
            "/v1/reason",
            json={"input": "ping"},
            headers={"X-API-Key": REASON_KEY},
        )
    assert r.status_code == 200, r.text

    # … but NOT for trace:read
    r = client.get("/v1/trace/history", headers={"X-API-Key": REASON_KEY})
    assert r.status_code == 403

    # … nor review:write
    r = client.get("/v1/review/pending", headers={"X-API-Key": REASON_KEY})
    assert r.status_code == 403

    # trace key works for trace:read
    r = client.get("/v1/trace/history", headers={"X-API-Key": TRACE_KEY})
    assert r.status_code == 200

    # review key works for review:write
    r = client.get("/v1/review/pending", headers={"X-API-Key": REVIEW_KEY})
    assert r.status_code == 200


def test_http_scope_mode_global_key_rejected_when_not_listed(tmp_path) -> None:
    """Global key alone must NOT authorise scoped endpoints in scope-key mode."""
    client = _build_client(
        tmp_path,
        api_keys_reason_write=REASON_KEY,
        api_keys_trace_read=TRACE_KEY,
        api_keys_review_write=REVIEW_KEY,
    )

    with _stub_reason_pipeline():
        r = client.post(
            "/v1/reason",
            json={"input": "ping"},
            headers={"X-API-Key": GLOBAL_KEY},
        )
    assert r.status_code == 403, r.text

    r = client.get("/v1/trace/history", headers={"X-API-Key": GLOBAL_KEY})
    assert r.status_code == 403

    r = client.get("/v1/review/pending", headers={"X-API-Key": GLOBAL_KEY})
    assert r.status_code == 403


def test_websocket_scope_mode_rejects_global_key_alone(tmp_path) -> None:
    """The /v1/ws/reason fallback no longer re-accepts the global key in
    scope-key mode.  Without explicit listing under reason:write, the
    handshake must be closed with 1008.
    """
    client = _build_client(
        tmp_path,
        api_keys_reason_write=REASON_KEY,
    )

    with _async_stub_reason_pipeline():
        with pytest.raises(Exception):  # starlette WebSocketDisconnect
            with client.websocket_connect(
                "/v1/ws/reason",
                headers={"X-API-Key": GLOBAL_KEY},
            ) as ws:
                ws.send_json({"input": "ping"})
                ws.receive_json()


def test_websocket_scope_mode_accepts_scoped_key(tmp_path) -> None:
    client = _build_client(
        tmp_path,
        api_keys_reason_write=REASON_KEY,
    )

    with _async_stub_reason_pipeline():
        with client.websocket_connect(
            "/v1/ws/reason",
            headers={"X-API-Key": REASON_KEY},
        ) as ws:
            ws.send_json({"input": "ping"})
            chunks: list[dict[str, Any]] = []
            while True:
                chunk = ws.receive_json()
                chunks.append(chunk)
                if chunk["chunk_type"] in {"done", "error"}:
                    break

    assert any(c["chunk_type"] == "done" for c in chunks)
