"""
Phase 5-E: Pipeline Performance Benchmark Suite
================================================

Measures end-to-end pipeline latency and throughput across safety modes,
async philosopher execution, and concurrent REST-layer offloading.

Targets:
  NORMAL  (39 philosophers) p50 < 5 s
  WARN    ( 5 philosophers) p50 < 2 s
  CRITICAL( 1 philosopher ) p50 < 1 s

Usage:
    # Benchmark only (with Rich summary table printed to stdout)
    pytest tests/benchmarks/ -v -s -m benchmark

    # Skip slow benchmarks in CI
    pytest tests/ -m "not slow"

Markers: benchmark, slow, phase5
"""

from __future__ import annotations

import asyncio
import statistics
import time
from typing import Callable
from unittest.mock import MagicMock

import pytest
from rich.console import Console
from rich.table import Table

from po_core.app.api import run
from po_core.domain.safety_mode import SafetyMode
from po_core.runtime.settings import Settings

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPEAT_NORMAL = 5  # NORMAL is heavier — 5 samples keeps CI sane
REPEAT_FAST = 8  # WARN/CRITICAL are cheap — more samples = stable p90

TARGET_NORMAL_S = 5.0
TARGET_WARN_S = 2.0
TARGET_CRITICAL_S = 1.0

_BENCH_PROMPT = "What is justice, and how should a society pursue it?"

console = Console()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _settings(mode: SafetyMode) -> Settings:
    return Settings(freedom_pressure_missing_mode=mode)


def _timeit(fn: Callable[[], object], n: int) -> list[float]:
    """Run fn n times; return wall-clock seconds per call."""
    samples: list[float] = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - t0)
    return samples


def _pct(data: list[float], p: float) -> float:
    s = sorted(data)
    return s[min(int(len(s) * p / 100), len(s) - 1)]


def _stats(samples: list[float]) -> dict:
    return {
        "p50": statistics.median(samples),
        "p90": _pct(samples, 90),
        "p99": _pct(samples, 99),
        "min": min(samples),
        "max": max(samples),
        "n": len(samples),
    }


def _print_rich_row(label: str, st: dict, target: float) -> None:
    ok = st["p50"] < target
    badge = "[green]PASS[/green]" if ok else "[red]FAIL[/red]"
    console.print(
        f"  {badge}  [bold]{label:<24}[/bold]"
        f"  p50=[cyan]{st['p50']:.3f}s[/cyan]"
        f"  p90=[yellow]{st['p90']:.3f}s[/yellow]"
        f"  req/s=[magenta]{1/st['p50']:.2f}[/magenta]"
        f"  n={st['n']}"
    )


# ---------------------------------------------------------------------------
# NORMAL mode — 39 philosophers
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_normal_p50():
    """NORMAL mode (39 philosophers): p50 < 5 s."""
    samples = _timeit(
        lambda: run(_BENCH_PROMPT, settings=_settings(SafetyMode.NORMAL)),
        REPEAT_NORMAL,
    )
    st = _stats(samples)
    _print_rich_row("NORMAL (39 phil)", st, TARGET_NORMAL_S)
    assert (
        st["p50"] < TARGET_NORMAL_S
    ), f"NORMAL p50={st['p50']:.3f}s ≥ {TARGET_NORMAL_S}s"


# ---------------------------------------------------------------------------
# WARN mode — 5 philosophers
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_warn_p50():
    """WARN mode (5 philosophers): p50 < 2 s."""
    samples = _timeit(
        lambda: run(_BENCH_PROMPT, settings=_settings(SafetyMode.WARN)),
        REPEAT_FAST,
    )
    st = _stats(samples)
    _print_rich_row("WARN (5 phil)", st, TARGET_WARN_S)
    assert st["p50"] < TARGET_WARN_S, f"WARN p50={st['p50']:.3f}s ≥ {TARGET_WARN_S}s"


# ---------------------------------------------------------------------------
# CRITICAL mode — 1 philosopher
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_critical_p50():
    """CRITICAL mode (1 philosopher): p50 < 1 s."""
    samples = _timeit(
        lambda: run(_BENCH_PROMPT, settings=_settings(SafetyMode.CRITICAL)),
        REPEAT_FAST,
    )
    st = _stats(samples)
    _print_rich_row("CRITICAL (1 phil)", st, TARGET_CRITICAL_S)
    assert (
        st["p50"] < TARGET_CRITICAL_S
    ), f"CRITICAL p50={st['p50']:.3f}s ≥ {TARGET_CRITICAL_S}s"


# ---------------------------------------------------------------------------
# Cold-start vs warm-up (NORMAL)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_coldstart_vs_warmup():
    """Cold-start latency ≤ 3× warm median (no pathological init cost)."""
    samples = _timeit(
        lambda: run(_BENCH_PROMPT, settings=_settings(SafetyMode.NORMAL)),
        REPEAT_NORMAL,
    )
    cold = samples[0]
    warm = statistics.median(samples[1:]) if len(samples) > 1 else samples[0]
    console.print(
        f"\n  [bold]Cold-start[/bold] [cyan]{cold:.3f}s[/cyan]"
        f"  [bold]Warm-median[/bold] [green]{warm:.3f}s[/green]"
        f"  ratio=[yellow]{cold/warm:.2f}x[/yellow]"
    )
    assert (
        cold <= warm * 3.0
    ), f"Cold-start ({cold:.3f}s) > 3× warm median ({warm:.3f}s)"


# ---------------------------------------------------------------------------
# async_run_philosophers() — Phase 5-D async benchmark
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_bench_async_philosophers():
    """async_run_philosophers() completes 39-stub-philosophers in < 2 s."""
    from po_core.party_machine import async_run_philosophers

    class _QuickPhil:
        def __init__(self, i: int) -> None:
            self.name = f"bench_phil_{i:02d}"

        def propose(self, ctx, intent, tensors, memory):
            from po_core.domain.proposal import Proposal

            return [
                Proposal(
                    proposal_id=f"{self.name}_p",
                    action_type="respond",
                    content=f"Proposal from {self.name}",
                    confidence=0.9,
                )
            ]

    philosophers = [_QuickPhil(i) for i in range(39)]

    t0 = time.perf_counter()
    proposals, results = await async_run_philosophers(
        philosophers,
        MagicMock(),  # ctx
        MagicMock(),  # intent
        MagicMock(),  # tensors
        MagicMock(),  # memory
        max_workers=12,
        timeout_s=2.0,
    )
    elapsed = time.perf_counter() - t0

    ok_count = sum(1 for r in results if r.ok)
    console.print(
        f"\n  [bold]async 39 philosophers[/bold]"
        f"  elapsed=[cyan]{elapsed:.3f}s[/cyan]"
        f"  ok={ok_count}/39"
        f"  proposals={len(proposals)}"
    )

    assert elapsed < 2.0, f"async_run_philosophers 39-phil took {elapsed:.3f}s ≥ 2s"
    assert ok_count == 39, f"Expected 39 ok results, got {ok_count}"
    assert len(proposals) == 39


# ---------------------------------------------------------------------------
# Concurrency: 5 simultaneous WARN-mode requests
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_bench_concurrent_warn_requests():
    """5 concurrent WARN-mode run() calls finish in < 4 s total wall-clock."""
    settings = _settings(SafetyMode.WARN)
    loop = asyncio.get_event_loop()

    async def _one() -> float:
        t0 = time.perf_counter()
        await loop.run_in_executor(None, lambda: run(_BENCH_PROMPT, settings=settings))
        return time.perf_counter() - t0

    t_wall = time.perf_counter()
    latencies = await asyncio.gather(*[_one() for _ in range(5)])
    wall = time.perf_counter() - t_wall

    console.print(
        f"\n  [bold]5 concurrent WARN requests[/bold]"
        f"  wall=[cyan]{wall:.3f}s[/cyan]"
        f"  p50=[green]{statistics.median(latencies):.3f}s[/green]"
        f"  max=[yellow]{max(latencies):.3f}s[/yellow]"
    )

    assert wall < 4.0, f"5 concurrent WARN requests took {wall:.3f}s ≥ 4s"


# ---------------------------------------------------------------------------
# Rich summary table — always passes, purely informational
# ---------------------------------------------------------------------------


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.phase5
def test_bench_summary_table():
    """Print a Rich summary table for all safety modes (informational)."""
    modes: list[tuple[str, SafetyMode, int, float]] = [
        ("NORMAL (39 phil)", SafetyMode.NORMAL, REPEAT_NORMAL, TARGET_NORMAL_S),
        ("WARN (5 phil)", SafetyMode.WARN, REPEAT_FAST, TARGET_WARN_S),
        ("CRITICAL (1 phil)", SafetyMode.CRITICAL, REPEAT_FAST, TARGET_CRITICAL_S),
    ]

    table = Table(
        title="Po_core Pipeline — Phase 5-E Benchmark Summary",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Mode", style="bold", width=22)
    table.add_column("p50 (s)", justify="right")
    table.add_column("p90 (s)", justify="right")
    table.add_column("p99 (s)", justify="right")
    table.add_column("req/s", justify="right")
    table.add_column("Target", justify="center")
    table.add_column("Status", justify="center")

    all_pass = True
    for label, mode, n, target in modes:
        samples = _timeit(lambda s=_settings(mode): run(_BENCH_PROMPT, settings=s), n)
        st = _stats(samples)
        passed = st["p50"] < target
        all_pass = all_pass and passed
        status = "[green]✓ PASS[/green]" if passed else "[red]✗ FAIL[/red]"
        table.add_row(
            label,
            f"{st['p50']:.3f}",
            f"{st['p90']:.3f}",
            f"{st['p99']:.3f}",
            f"{1/st['p50']:.2f}",
            f"< {target:.0f}s",
            status,
        )

    console.print()
    console.print(table)
    console.print()
    # Summary assertion — the table test itself always passes (it's informational)
    # Individual assertions live in the per-mode tests above.
