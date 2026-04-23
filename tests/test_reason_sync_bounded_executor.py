"""Regression tests for the bounded /v1/reason executor and semaphore.

Goal:  ensure that a burst of /v1/reason requests with a short request timeout
does NOT keep spawning background workers after the client has given up.

Historically the endpoint used ``run_in_executor(None, ...)`` which targets
the default asyncio thread pool (``min(32, cpu_count * 5)``).  Under load
with a 30s request timeout, that meant runaway thread growth even if the
HTTP caller hung up early.  We now gate through an explicit bounded
``ThreadPoolExecutor`` sized by ``settings.reason_sync_max_workers`` and an
``asyncio.Semaphore`` of the same size.
"""

from __future__ import annotations

import threading
import time

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings, set_api_settings
from po_core.app.rest.routers import reason as reason_mod
from po_core.app.rest.server import create_app


@pytest.fixture
def configured_client():
    settings = APISettings(
        skip_auth=True,
        api_key="",
        reason_sync_max_workers=2,
        rate_limit_per_minute=0,
    )
    set_api_settings(settings)
    app = create_app(settings=settings)
    with TestClient(app) as client:
        yield client


def test_sync_reason_uses_bounded_executor(configured_client: TestClient) -> None:
    """The sync endpoint MUST route through the configured bounded executor."""
    response = configured_client.post("/v1/reason", json={"input": "What is good?"})
    assert response.status_code == 200

    executor = reason_mod._sync_executor
    assert executor is not None
    # max_workers honours the configured setting.
    assert reason_mod._sync_max_workers == 2
    # Second request reuses the same singleton executor.
    second = configured_client.post("/v1/reason", json={"input": "What is truth?"})
    assert second.status_code == 200
    assert reason_mod._sync_executor is executor


def test_sync_active_worker_gauge_returns_to_zero_after_completion(
    configured_client: TestClient,
) -> None:
    """After a burst of successful requests the gauge collapses back to zero."""
    for _ in range(3):
        response = configured_client.post(
            "/v1/reason", json={"input": "What is justice?"}
        )
        assert response.status_code == 200

    # Allow any finalising background threads to return from _with_sync_worker_gauge.
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        if reason_mod._sync_active_worker_count() == 0:
            break
        time.sleep(0.02)

    assert reason_mod._sync_active_worker_count() == 0


def test_sync_active_workers_does_not_exceed_pool_size(
    configured_client: TestClient,
) -> None:
    """Concurrent submissions must be serialised by the semaphore + pool."""
    max_workers = reason_mod._sync_max_workers or 2
    observed_peak = 0
    peak_lock = threading.Lock()

    def _fire() -> None:
        configured_client.post("/v1/reason", json={"input": "What is wisdom?"})

    threads = [threading.Thread(target=_fire) for _ in range(max_workers + 4)]
    for t in threads:
        t.start()

    # Poll the active-worker gauge while the burst is in flight.
    end = time.monotonic() + 3.0
    while time.monotonic() < end and any(t.is_alive() for t in threads):
        with peak_lock:
            observed_peak = max(observed_peak, reason_mod._sync_active_worker_count())
        time.sleep(0.005)

    for t in threads:
        t.join(timeout=5.0)

    assert observed_peak <= max_workers, (
        f"active worker count peaked at {observed_peak} which exceeds the "
        f"bounded executor size {max_workers}"
    )
