"""
Phase 5-D: True Async PartyMachine — unit tests.

Covers:
- async_run_philosophers(): normal execution, timeout, exception isolation
- REST reason endpoint: run_in_executor offload (event loop not blocked)

Markers: unit, phase5
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Mapping
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers / stubs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _FakeProposal:
    proposal_id: str = "p1"
    action_type: str = "respond"
    content: str = "stub content"
    confidence: float = 0.8
    assumption_tags: tuple = field(default_factory=tuple)
    risk_tags: tuple = field(default_factory=tuple)
    extra: Mapping = field(default_factory=dict)


class _OKPhilosopher:
    name = "ok_phil"

    def propose(self, ctx, intent, tensors, memory) -> List[_FakeProposal]:
        return [_FakeProposal()]


class _ErrorPhilosopher:
    name = "err_phil"

    def propose(self, ctx, intent, tensors, memory):
        raise RuntimeError("deliberate error")


class _SlowPhilosopher:
    name = "slow_phil"

    def propose(self, ctx, intent, tensors, memory):
        import time

        time.sleep(5)  # will trigger timeout
        return [_FakeProposal()]


# ---------------------------------------------------------------------------
# async_run_philosophers tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_run_philosophers_success():
    """Successful philosopher returns a proposal and RunResult.ok=True."""
    from po_core.party_machine import async_run_philosophers

    proposals, results = await async_run_philosophers(
        [_OKPhilosopher()],
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        max_workers=2,
        timeout_s=2.0,
    )

    assert len(results) == 1
    assert results[0].ok is True
    assert results[0].philosopher_id == "ok_phil"
    assert results[0].timed_out is False
    assert len(proposals) == 1


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_run_philosophers_empty():
    """Empty philosophers list returns empty results immediately."""
    from po_core.party_machine import async_run_philosophers

    proposals, results = await async_run_philosophers(
        [],
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        max_workers=2,
        timeout_s=1.0,
    )

    assert proposals == []
    assert results == []


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_run_philosophers_exception_isolated():
    """Exception in one philosopher is captured; others still return."""
    from po_core.party_machine import async_run_philosophers

    proposals, results = await async_run_philosophers(
        [_OKPhilosopher(), _ErrorPhilosopher()],
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        max_workers=2,
        timeout_s=2.0,
    )

    ids = {r.philosopher_id: r for r in results}
    assert ids["ok_phil"].ok is True
    assert ids["err_phil"].ok is False
    assert "RuntimeError" in (ids["err_phil"].error or "")
    assert len(proposals) == 1  # only ok_phil contributed


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_run_philosophers_timeout():
    """Slow philosopher is marked timed_out; not counted in proposals."""
    from po_core.party_machine import async_run_philosophers

    proposals, results = await async_run_philosophers(
        [_SlowPhilosopher()],
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        max_workers=2,
        timeout_s=0.1,  # 100 ms timeout → _SlowPhilosopher (5 s) will time out
    )

    assert len(results) == 1
    assert results[0].timed_out is True
    assert results[0].ok is False
    assert proposals == []


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_run_philosophers_mixed():
    """Mixed OK + error + timeout: results correctly classified."""
    from po_core.party_machine import async_run_philosophers

    proposals, results = await async_run_philosophers(
        [_OKPhilosopher(), _ErrorPhilosopher(), _SlowPhilosopher()],
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        max_workers=4,
        timeout_s=0.1,
    )

    ids = {r.philosopher_id: r for r in results}
    assert ids["ok_phil"].ok is True
    assert ids["err_phil"].ok is False
    assert ids["slow_phil"].timed_out is True
    assert len(proposals) == 1


# ---------------------------------------------------------------------------
# REST layer: run_in_executor offload
# ---------------------------------------------------------------------------

_MOCK_RESULT: dict[str, Any] = {
    "status": "ok",
    "request_id": "req-async-test",
    "proposal": {"content": "async offload works"},
    "proposals": [],
    "tensors": {},
    "safety_mode": "NORMAL",
}


@pytest.fixture()
def _client_no_auth():
    from fastapi.testclient import TestClient

    from po_core.app.rest import auth, config
    from po_core.app.rest.config import APISettings
    from po_core.app.rest.server import create_app

    app = create_app()
    app.dependency_overrides[config.get_api_settings] = lambda: APISettings(
        skip_auth=True, api_key=""
    )
    app.dependency_overrides[auth.require_api_key] = lambda: None
    return TestClient(app, raise_server_exceptions=True)


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_endpoint_uses_run_in_executor(_client_no_auth):
    """POST /v1/reason runs _run_reasoning via run_in_executor (async offload)."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = _client_no_auth.post("/v1/reason", json={"input": "Is async safe?"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "approved"
    assert "async offload works" in data["response"]


@pytest.mark.unit
@pytest.mark.phase5
def test_reason_stream_endpoint_non_blocking(_client_no_auth):
    """POST /v1/reason/stream SSE generator runs po_run via run_in_executor."""
    with patch("po_core.app.rest.routers.reason.po_run", return_value=_MOCK_RESULT):
        resp = _client_no_auth.post(
            "/v1/reason/stream",
            json={"input": "Stream async?"},
            headers={"Accept": "text/event-stream"},
        )

    assert resp.status_code == 200
    body = resp.text
    assert "started" in body
    assert "result" in body
    assert "done" in body


# ---------------------------------------------------------------------------
# AsyncPartyMachine — Phase 5.2 native async engine tests
# ---------------------------------------------------------------------------


class _NativeAsyncPhilosopher:
    """Philosopher with a real native propose_async() override (no thread)."""

    name = "native_async_phil"

    def propose(self, ctx, intent, tensors, memory):
        return [_FakeProposal(proposal_id="sync_fallback")]

    async def propose_async(self, ctx, intent, tensors, memory):
        # Native async — does NOT call propose() / no thread overhead
        return [_FakeProposal(proposal_id="native_async")]


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_party_machine_context_manager():
    """AsyncPartyMachine can be used as an async context manager."""
    from po_core.party_machine import AsyncPartyMachine

    async with AsyncPartyMachine(max_workers=2, timeout_s=2.0) as machine:
        proposals, results = await machine.run(
            [_OKPhilosopher()],
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

    assert len(results) == 1
    assert results[0].ok is True
    assert len(proposals) == 1


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_party_machine_native_async_dispatch():
    """Native propose_async() is called directly without thread overhead."""
    from po_core.party_machine import AsyncPartyMachine

    native = _NativeAsyncPhilosopher()
    async with AsyncPartyMachine(max_workers=2, timeout_s=2.0) as machine:
        assert machine._has_native_async(native), "Should detect native override"
        proposals, results = await machine.run(
            [native],
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

    assert results[0].ok is True
    # Verify the native async path was used (proposal_id differs from sync fallback)
    assert proposals[0].proposal_id == "native_async"


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_party_machine_thread_fallback():
    """Philosopher without propose_async override uses thread fallback."""
    from po_core.party_machine import AsyncPartyMachine

    ok_phil = _OKPhilosopher()
    async with AsyncPartyMachine(max_workers=2, timeout_s=2.0) as machine:
        assert not machine._has_native_async(ok_phil), "Should use thread fallback"
        proposals, results = await machine.run(
            [ok_phil],
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

    assert results[0].ok is True
    assert len(proposals) == 1


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_party_machine_mixed_sync_and_native():
    """Mix of native-async and sync-thread philosophers works correctly."""
    from po_core.party_machine import AsyncPartyMachine

    philosophers = [_OKPhilosopher(), _NativeAsyncPhilosopher(), _ErrorPhilosopher()]
    async with AsyncPartyMachine(max_workers=4, timeout_s=2.0) as machine:
        proposals, results = await machine.run(
            philosophers,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

    ids = {r.philosopher_id: r for r in results}
    assert ids["ok_phil"].ok is True
    assert ids["native_async_phil"].ok is True
    assert ids["err_phil"].ok is False
    assert len(proposals) == 2  # ok_phil + native_async_phil


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_async_party_machine_aclose():
    """aclose() can be called explicitly instead of context manager."""
    from po_core.party_machine import AsyncPartyMachine

    machine = AsyncPartyMachine(max_workers=2, timeout_s=1.0)
    proposals, results = await machine.run(
        [_OKPhilosopher()],
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    await machine.aclose()

    assert results[0].ok is True
    assert machine._executor is None  # executor has been shut down


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_propose_async_default_runs_in_thread():
    """Philosopher.propose_async() default wraps propose() in a thread."""
    from datetime import datetime, timezone

    from po_core.domain.context import Context
    from po_core.domain.tensor_snapshot import TensorSnapshot
    from po_core.philosophers.aristotle import Aristotle

    aristotle = Aristotle()
    ctx = Context(
        user_input="What is virtue?",
        request_id="test-async-propose",
        created_at=datetime.now(timezone.utc),
    )
    tensors = TensorSnapshot.now({"freedom_pressure": 0.5})
    # propose_async() should return the same result type as propose()
    async_result = await aristotle.propose_async(ctx, MagicMock(), tensors, MagicMock())

    assert len(async_result) == 1
    assert isinstance(async_result[0].content, str)
    assert len(async_result[0].content) > 0
