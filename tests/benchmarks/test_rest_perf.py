"""
Phase 5-E: REST API Performance Benchmark Suite
================================================

Measures latency and overhead of the Po_core REST API layer (FastAPI /
TestClient) for each endpoint category.

Targets:
  GET  /v1/health          p50 < 50 ms
  GET  /v1/philosophers    p50 < 200 ms
  POST /v1/reason (smoke)  single run < 3 s   (CI-safe)
  POST /v1/reason          p50 < 3 s           (NORMAL mode, slow)
  REST overhead            delta vs direct run < 100 ms

Usage:
    # REST benchmarks only
    pytest tests/benchmarks/test_rest_perf.py -v -s -m benchmark

    # Skip slow benchmarks in CI
    pytest tests/ -m "not slow"

Markers: benchmark, slow, phase5
"""

from __future__ import annotations

import statistics
import time
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from po_core.app.api import run as po_run
from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app
from po_core.app.rest.store import _store
from po_core.runtime.settings import Settings

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPEAT_LIGHT = 15  # lightweight endpoints (health, philosophers)
REPEAT_REASON = 5  # reason endpoint — pipeline is heavier

TARGET_HEALTH_MS = 50.0
TARGET_PHILOSOPHERS_MS = 200.0
TARGET_REASON_S = 3.0
TARGET_OVERHEAD_MS = 100.0

_BENCH_PROMPT = "What is justice, and how should a society pursue it?"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ms(t: float) -> float:
    return t * 1000.0


def _pct(data: list[float], p: float) -> float:
    s = sorted(data)
    return s[min(int(len(s) * p / 100), len(s) - 1)]


def _stats(samples: list[float]) -> dict:
    return {
        "p50": statistics.median(samples),
        "p90": _pct(samples, 90),
        "min": min(samples),
        "max": max(samples),
        "n": len(samples),
    }


def _timeit(fn: Callable[[], object], n: int) -> list[float]:
    """Run fn n times; return wall-clock seconds per call."""
    results: list[float] = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        results.append(time.perf_counter() - t0)
    return results


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def bench_client():
    """
    Module-scoped TestClient — created once for the entire benchmark module.

    Auth and rate limiting are disabled so repeated calls don't hit
    the 60 req/min cap and each request isn't penalised by key lookup.
    """
    from po_core.app.rest import auth, config

    def _settings() -> APISettings:
        return APISettings(
            skip_auth=True,
            api_key="",
            rate_limit_per_minute=10_000,
        )

    app = create_app()
    app.dependency_overrides[config.get_api_settings] = _settings
    app.dependency_overrides[auth.require_api_key] = lambda: None

    with TestClient(app, raise_server_exceptions=True) as client:
        yield client

    _store.clear()


# ---------------------------------------------------------------------------
# GET /v1/health — CI-safe smoke + p50 assertion
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.phase5
def test_bench_rest_health_smoke(bench_client: TestClient):
    """CI smoke: /v1/health must respond in < 50 ms."""
    t0 = time.perf_counter()
    resp = bench_client.get("/v1/health")
    elapsed_ms = _ms(time.perf_counter() - t0)

    assert resp.status_code == 200
    assert (
        elapsed_ms < TARGET_HEALTH_MS
    ), f"/v1/health took {elapsed_ms:.1f} ms ≥ {TARGET_HEALTH_MS} ms"


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_rest_health_p50(bench_client: TestClient):
    """GET /v1/health: p50 < 50 ms over {n} samples."""
    samples = _timeit(lambda: bench_client.get("/v1/health"), REPEAT_LIGHT)
    st = _stats(samples)
    p50_ms = _ms(st["p50"])
    p90_ms = _ms(st["p90"])
    print(
        f"\n  /v1/health  " f"p50={p50_ms:.1f}ms  p90={p90_ms:.1f}ms  " f"n={st['n']}"
    )
    assert (
        p50_ms < TARGET_HEALTH_MS
    ), f"/v1/health p50={p50_ms:.1f}ms ≥ {TARGET_HEALTH_MS}ms"


# ---------------------------------------------------------------------------
# GET /v1/philosophers — manifest retrieval
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_rest_philosophers_p50(bench_client: TestClient):
    """GET /v1/philosophers: p50 < 200 ms (loads full 39-philosopher manifest)."""
    samples = _timeit(lambda: bench_client.get("/v1/philosophers"), REPEAT_LIGHT)
    st = _stats(samples)
    p50_ms = _ms(st["p50"])
    p90_ms = _ms(st["p90"])
    print(
        f"\n  /v1/philosophers  "
        f"p50={p50_ms:.1f}ms  p90={p90_ms:.1f}ms  "
        f"n={st['n']}"
    )
    assert (
        p50_ms < TARGET_PHILOSOPHERS_MS
    ), f"/v1/philosophers p50={p50_ms:.1f}ms ≥ {TARGET_PHILOSOPHERS_MS}ms"


# ---------------------------------------------------------------------------
# POST /v1/reason — pipeline latency through REST layer
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.phase5
def test_bench_rest_reason_smoke(bench_client: TestClient):
    """CI smoke: POST /v1/reason single call must complete in < 3 s."""
    t0 = time.perf_counter()
    resp = bench_client.post("/v1/reason", json={"input": _BENCH_PROMPT})
    elapsed = time.perf_counter() - t0

    assert resp.status_code == 200, f"Unexpected status {resp.status_code}: {resp.text}"
    assert (
        elapsed < TARGET_REASON_S
    ), f"POST /v1/reason took {elapsed:.3f}s ≥ {TARGET_REASON_S}s"


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_rest_reason_p50(bench_client: TestClient):
    """POST /v1/reason: p50 < 3 s (full pipeline via REST layer)."""
    samples = _timeit(
        lambda: bench_client.post("/v1/reason", json={"input": _BENCH_PROMPT}),
        REPEAT_REASON,
    )
    st = _stats(samples)
    print(
        f"\n  POST /v1/reason  "
        f"p50={st['p50']:.3f}s  p90={st['p90']:.3f}s  "
        f"req/s={1/st['p50']:.2f}  n={st['n']}"
    )
    assert (
        st["p50"] < TARGET_REASON_S
    ), f"POST /v1/reason p50={st['p50']:.3f}s ≥ {TARGET_REASON_S}s"


# ---------------------------------------------------------------------------
# REST overhead: direct run() vs POST /v1/reason
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_rest_overhead(bench_client: TestClient):
    """
    REST overhead (HTTP + serialisation) must be < 100 ms above direct run().

    Methodology:
    - Collect median latency for direct po_run() calls (no HTTP)
    - Collect median latency for POST /v1/reason (same prompt, HTTP overhead)
    - Assert delta < 100 ms to confirm the REST layer is not a bottleneck
    """
    settings = Settings()

    direct_samples = _timeit(
        lambda: po_run(_BENCH_PROMPT, settings=settings),
        REPEAT_REASON,
    )
    rest_samples = _timeit(
        lambda: bench_client.post("/v1/reason", json={"input": _BENCH_PROMPT}),
        REPEAT_REASON,
    )

    direct_p50 = statistics.median(direct_samples)
    rest_p50 = statistics.median(rest_samples)
    overhead_ms = _ms(rest_p50 - direct_p50)

    print(
        f"\n  direct run()     p50={direct_p50:.3f}s\n"
        f"  POST /v1/reason  p50={rest_p50:.3f}s\n"
        f"  overhead         {overhead_ms:+.1f}ms  (target < {TARGET_OVERHEAD_MS}ms)"
    )

    assert overhead_ms < TARGET_OVERHEAD_MS, (
        f"REST overhead {overhead_ms:.1f}ms ≥ {TARGET_OVERHEAD_MS}ms "
        f"(direct={direct_p50:.3f}s, rest={rest_p50:.3f}s)"
    )
