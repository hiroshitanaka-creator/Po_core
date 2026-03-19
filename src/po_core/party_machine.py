"""
Philosopher Party Machine 🎉
============================

Interactive system that automatically suggests optimal philosopher combinations
based on research findings and executes engaging philosophical reasoning sessions.

Based on research data:
- RQ1: Best combinations (4-philosopher groups with 100% emergence)
- RQ3: Optimal group size (8-14 philosophers, peak at 15)
- RQ4: Dialectical tension correlation (+1975% emergence increase)

Usage:
    from po_core.party_machine import PhilosopherPartyMachine

    party = PhilosopherPartyMachine()
    config = party.suggest_party(
        theme="AI and responsibility",
        mood="balanced"  # calm, balanced, chaotic, critical
    )
    results = party.run_party(config)
    party.visualize_results(results)

Parallel Execution:
    from po_core.party_machine import run_philosophers

    proposals, results = run_philosophers(
        philosophers, ctx, intent, tensors, memory,
        max_workers=12, timeout_s=1.2
    )
"""

from __future__ import annotations

import asyncio
import inspect
import os
import pickle
import random
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from dataclasses import dataclass, field
from enum import Enum
from time import perf_counter
from typing import TYPE_CHECKING, Dict, List, Mapping, Optional, Sequence, Tuple

if TYPE_CHECKING:
    from po_core.domain.context import Context
    from po_core.domain.intent import Intent
    from po_core.domain.memory_snapshot import MemorySnapshot
    from po_core.domain.proposal import Proposal
    from po_core.domain.tensor_snapshot import TensorSnapshot
    from po_core.philosophers.base import PhilosopherProtocol
    from po_core.ports.trace import TracePort

from rich.console import Console
from rich.panel import Panel

from po_core.deliberation.protocol import run_deliberation
from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.philosopher_process import (
    ExecOutcome,
    SerializedJob,
    _supports_budget_kwarg,
    run_one_philosopher,
)
from po_core.runtime.execution_budget import ExecutionBudget, ExecutionBudgetExceeded

console = Console()


class PartyMood(str, Enum):
    """Mood/atmosphere for the philosophical party."""

    CALM = "calm"  # Low tension, harmonious discussion
    BALANCED = "balanced"  # Moderate tension, diverse perspectives
    CHAOTIC = "chaotic"  # High tension, maximum disagreement
    CRITICAL = "critical"  # Critical/skeptical emphasis


class PhilosophicalTheme(str, Enum):
    """Common philosophical themes."""

    ETHICS = "ethics"
    EXISTENCE = "existence"
    KNOWLEDGE = "knowledge"
    POLITICS = "politics"
    CONSCIOUSNESS = "consciousness"
    FREEDOM = "freedom"
    MEANING = "meaning"
    JUSTICE = "justice"
    TECHNOLOGY = "technology"
    DEATH = "death"


@dataclass
class PartyConfig:
    """Configuration for a philosopher party."""

    theme: str
    mood: PartyMood
    philosophers: List[str]
    expected_size: int
    expected_tension: float  # 0.0-1.0
    expected_emergence: float  # 0.0-1.0
    reasoning: str = ""  # Why this combination was chosen


@dataclass
class PartyResults:
    """Results from a philosopher party session."""

    config: PartyConfig
    responses: List[Dict]
    metrics: Dict[str, float]
    consensus: Dict
    emergence_detected: bool
    tension_level: float
    visualization_data: Dict = field(default_factory=dict)


# ============================================================================
# Parallel Execution Engine
# ============================================================================


@dataclass(frozen=True)
class RunResult:
    """Result of a single philosopher execution."""

    philosopher_id: str
    ok: bool
    n: int = 0  # Number of proposals generated
    timed_out: bool = False
    error: Optional[str] = None
    latency_ms: Optional[int] = None  # Execution time in milliseconds


@dataclass(frozen=True)
class _ExecutionResult:
    """Structured internal execution result with authoritative timeout state."""

    philosopher_id: str
    proposals: List["Proposal"]
    ok: bool
    n: int
    timed_out: bool
    error: Optional[str]
    latency_ms: Optional[int]

    def to_run_result(self) -> RunResult:
        return RunResult(
            philosopher_id=self.philosopher_id,
            ok=self.ok,
            n=self.n,
            timed_out=self.timed_out,
            error=self.error,
            latency_ms=self.latency_ms,
        )


def _build_execution_result(
    *,
    philosopher_id: str,
    proposals: Optional[List["Proposal"]] = None,
    n: int,
    timed_out: bool,
    error: Optional[str],
    latency_ms: Optional[int],
) -> _ExecutionResult:
    selected_proposals = list(proposals or [])
    return _ExecutionResult(
        philosopher_id=philosopher_id,
        proposals=[] if timed_out else selected_proposals,
        ok=(error is None and not timed_out),
        n=(0 if timed_out else n),
        timed_out=timed_out,
        error=error,
        latency_ms=latency_ms,
    )


def _execution_result_from_outcome(outcome: ExecOutcome) -> _ExecutionResult:
    return _build_execution_result(
        philosopher_id=outcome.philosopher_id,
        proposals=outcome.proposals,
        n=outcome.n,
        timed_out=outcome.timed_out,
        error=outcome.error,
        latency_ms=outcome.latency_ms,
    )


_LATENCY_EMA_BY_PHILOSOPHER: Dict[str, float] = {}


def _soft_timeout_error(timeout_s: float, mode: str) -> str:
    return (
        f"Soft timeout after {timeout_s}s ({mode} fallback=empty_proposals; "
        "background work may still continue)"
    )


def _cooperative_timeout_error(timeout_s: float, mode: str) -> str:
    return f"Cooperative timeout after {timeout_s}s ({mode} fallback=empty_proposals)"


def _hard_timeout_error(timeout_s: float) -> str:
    return f"Hard timeout after {timeout_s}s"


def _is_budget_stop_error(error: Optional[str]) -> bool:
    return bool(error and error.startswith("Execution stopped cooperatively"))


def _run_one_in_subprocess(job: SerializedJob) -> ExecOutcome:
    """Execute one philosopher in a dedicated Python subprocess."""
    pid = getattr(job.philosopher, "name", job.philosopher.__class__.__name__)
    start = perf_counter()
    env = dict(os.environ)
    src_path = os.path.dirname(os.path.dirname(__file__))
    repo_root = os.path.dirname(src_path)
    test_paths = [src_path, repo_root, os.path.join(repo_root, "tests"), os.path.join(repo_root, "tests", "unit")]
    existing_pythonpath = env.get("PYTHONPATH")
    pythonpath_parts = [p for p in test_paths if os.path.isdir(p)]
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    try:
        payload = pickle.dumps(job)
    except Exception as e:
        elapsed_ms = int((perf_counter() - start) * 1000)
        return ExecOutcome([], 0, False, f"{type(e).__name__}: {e}", elapsed_ms, pid)
    proc = subprocess.Popen(
        [sys.executable, "-m", "po_core.philosopher_worker"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=repo_root,
        env=env,
    )
    bootstrap_grace_s = float(os.getenv("PO_PHILOSOPHER_PROCESS_BOOTSTRAP_GRACE_S", "0.05"))
    try:
        stdout, stderr = proc.communicate(payload, timeout=job.timeout_s + bootstrap_grace_s)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        elapsed_ms = int((perf_counter() - start) * 1000)
        return ExecOutcome([], 0, True, _hard_timeout_error(job.timeout_s), elapsed_ms, pid)

    elapsed_ms = int((perf_counter() - start) * 1000)
    if proc.returncode != 0:
        err = stderr.decode("utf-8", errors="replace").strip()
        message = err or f"Worker exited without outcome (returncode={proc.returncode})"
        return ExecOutcome([], 0, False, message, elapsed_ms, pid)

    try:
        outcome = pickle.loads(stdout)
    except Exception as e:
        err = stderr.decode("utf-8", errors="replace").strip()
        message = err or f"Worker decode failed: {type(e).__name__}: {e}"
        return ExecOutcome([], 0, False, message, elapsed_ms, pid)

    if isinstance(outcome, ExecOutcome):
        if outcome.latency_ms > job.timeout_s * 1000:
            return ExecOutcome([], 0, True, _hard_timeout_error(job.timeout_s), elapsed_ms, pid)
        return outcome

    return ExecOutcome([], 0, False, "Worker returned invalid outcome", elapsed_ms, pid)


def _run_one_in_thread(
    ph: "PhilosopherProtocol",
    ctx: "Context",
    intent: "Intent",
    tensors: "TensorSnapshot",
    memory: "MemorySnapshot",
    limit_per_philosopher: int,
    timeout_s: float,
) -> ExecOutcome:
    pid = getattr(ph, "name", ph.__class__.__name__)
    start = perf_counter()
    outcome = run_one_philosopher(
        SerializedJob(ph, ctx, intent, tensors, memory, limit_per_philosopher, timeout_s)
    )
    elapsed_ms = int((perf_counter() - start) * 1000)
    if elapsed_ms > timeout_s * 1000:
        if _is_budget_stop_error(outcome.error):
            return ExecOutcome([], 0, True, _cooperative_timeout_error(timeout_s, "thread"), elapsed_ms, pid)
        if outcome.error is None:
            return ExecOutcome([], 0, True, _soft_timeout_error(timeout_s, "thread"), elapsed_ms, pid)
    return outcome


def run_philosophers(
    philosophers: Sequence["PhilosopherProtocol"],
    ctx: "Context",
    intent: "Intent",
    tensors: "TensorSnapshot",
    memory: "MemorySnapshot",
    *,
    max_workers: int,
    timeout_s: float,
    limit_per_philosopher: int = 1,
) -> Tuple[List["Proposal"], List[RunResult]]:
    """Execute philosophers with adaptive parallelism and deterministic ordering."""
    from po_core.domain.proposal import Proposal

    proposals: List[Proposal] = []
    results: List[RunResult] = []

    if not philosophers:
        return proposals, results

    limit = max(0, min(limit_per_philosopher, 5))
    hard_timeout_max_s = float(os.getenv("PO_PHILOSOPHER_HARD_TIMEOUT_MAX_S", "0.01"))
    use_process_isolation = timeout_s <= hard_timeout_max_s

    def _embed_author_and_index(
        p: "Proposal", author: str, proposal_index: int
    ) -> "Proposal":
        extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
        pc_src = extra.get(PO_CORE, {})
        pc = dict(pc_src) if isinstance(pc_src, Mapping) else {}
        pc[AUTHOR] = author
        pc["proposal_index"] = proposal_index
        extra[PO_CORE] = pc
        return Proposal(
            proposal_id=p.proposal_id,
            action_type=p.action_type,
            content=p.content,
            confidence=p.confidence,
            assumption_tags=list(p.assumption_tags),
            risk_tags=list(p.risk_tags),
            extra=extra,
        )


    ema_alpha = float(os.getenv("PO_PHILOSOPHER_LATENCY_EMA_ALPHA", "0.3"))
    seq_threshold_ms = float(os.getenv("PO_PHILOSOPHER_SEQUENTIAL_THRESHOLD_MS", "0.0"))

    def _update_ema(pid: str, dt: Optional[int]) -> None:
        if dt is None:
            return
        prev = _LATENCY_EMA_BY_PHILOSOPHER.get(pid)
        if prev is None:
            _LATENCY_EMA_BY_PHILOSOPHER[pid] = float(dt)
            return
        _LATENCY_EMA_BY_PHILOSOPHER[pid] = (
            ema_alpha * float(dt) + (1.0 - ema_alpha) * prev
        )

    result_by_index: Dict[int, RunResult] = {}
    proposals_by_index: Dict[int, List[Proposal]] = {}

    sequential_indices: list[int] = []
    parallel_indices: list[int] = []

    for idx, ph in enumerate(philosophers):
        pid = getattr(ph, "name", ph.__class__.__name__)
        ema = _LATENCY_EMA_BY_PHILOSOPHER.get(pid)
        if seq_threshold_ms > 0.0 and ema is not None and ema <= seq_threshold_ms:
            sequential_indices.append(idx)
        else:
            parallel_indices.append(idx)

    for idx in sequential_indices:
        ph = philosophers[idx]
        outcome = (
            _run_one_in_subprocess(
                SerializedJob(ph, ctx, intent, tensors, memory, limit, timeout_s)
            )
            if use_process_isolation
            else _run_one_in_thread(ph, ctx, intent, tensors, memory, limit, timeout_s)
        )
        _update_ema(outcome.philosopher_id, outcome.latency_ms)
        execution_result = _execution_result_from_outcome(outcome)
        result_by_index[idx] = execution_result.to_run_result()
        if execution_result.proposals:
            proposals_by_index[idx] = execution_result.proposals

    if parallel_indices:
        executor = ThreadPoolExecutor(max_workers=max_workers)
        try:
            futures = {
                idx: executor.submit(
                    _run_one_in_subprocess if use_process_isolation else _run_one_in_thread,
                    SerializedJob(
                        philosophers[idx],
                        ctx,
                        intent,
                        tensors,
                        memory,
                        limit,
                        timeout_s,
                    ) if use_process_isolation else philosophers[idx],
                    *( () if use_process_isolation else (ctx, intent, tensors, memory, limit, timeout_s) )
                )
                for idx in parallel_indices
            }
            for idx in parallel_indices:
                future = futures[idx]
                ph = philosophers[idx]
                pid = getattr(ph, "name", ph.__class__.__name__)
                try:
                    outcome = future.result(timeout=None if use_process_isolation else timeout_s + 0.05)
                    _update_ema(outcome.philosopher_id, outcome.latency_ms)
                    execution_result = _execution_result_from_outcome(outcome)
                    result_by_index[idx] = execution_result.to_run_result()
                    if execution_result.proposals:
                        proposals_by_index[idx] = execution_result.proposals
                except FuturesTimeoutError:
                    result_by_index[idx] = _build_execution_result(
                        philosopher_id=pid,
                        n=0,
                        timed_out=True,
                        error=_soft_timeout_error(timeout_s, "thread"),
                        latency_ms=None,
                    ).to_run_result()
                except Exception as e:
                    result_by_index[idx] = _build_execution_result(
                        philosopher_id=pid,
                        n=0,
                        timed_out=False,
                        error=f"{type(e).__name__}: {e}",
                        latency_ms=None,
                    ).to_run_result()
        finally:
            executor.shutdown(wait=False, cancel_futures=False)

    for idx in range(len(philosophers)):
        results.append(result_by_index[idx])
        proposals.extend(proposals_by_index.get(idx, []))

    if os.getenv("PO_DEBATE_V1", "").lower() in ("1", "true", "yes") and proposals:
        try:
            run_deliberation(
                input={
                    "prompt": getattr(ctx, "user_input", ""),
                    "proposals": list(proposals),
                },
                philosophers=philosophers,
                axis_spec={"axes": ["ethics", "risk", "evidence"]},
                settings={"max_critiques_per_philosopher": 2},
            )
        except Exception:
            pass

    return proposals, results


class AsyncPartyMachine:
    """True async philosopher execution engine (Phase 5.2).

    Dispatches philosopher execution using the most efficient available method:
    - If a philosopher exposes ``propose_async()`` with a native override,
      it is called directly on the event loop (zero thread overhead).
    - Otherwise the synchronous ``propose()`` is offloaded to a
      ``ThreadPoolExecutor``, keeping the FastAPI event loop unblocked.

    Lifecycle:
        The machine creates and owns an executor for thread fallback.
        Call ``async with AsyncPartyMachine(...) as machine`` or
        ``await machine.aclose()`` when done to ensure proper cleanup.

    Usage::

        machine = AsyncPartyMachine(max_workers=12, timeout_s=5.0)
        proposals, results = await machine.run(philosophers, ctx, intent, tensors, memory)
        await machine.aclose()
    """

    _NATIVE_ASYNC_SENTINEL = "propose_async"

    def __init__(self, *, max_workers: int = 8, timeout_s: float = 5.0) -> None:
        self._max_workers = max_workers
        self._timeout_s = timeout_s
        self._executor: Optional[ThreadPoolExecutor] = None

    # ── Context-manager support ───────────────────────────────────────

    async def __aenter__(self) -> "AsyncPartyMachine":
        self._executor = ThreadPoolExecutor(
            max_workers=self._max_workers,
            thread_name_prefix="po_phil",
        )
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Gracefully shut down the internal executor."""
        if self._executor is not None:
            self._executor.shutdown(wait=True, cancel_futures=False)
            self._executor = None

    # ── Execution ─────────────────────────────────────────────────────

    def _has_native_async(self, ph: "PhilosopherProtocol") -> bool:
        """Return True if the philosopher overrides propose_async() natively."""
        method = getattr(ph, self._NATIVE_ASYNC_SENTINEL, None)
        if method is None:
            return False
        # If the method's underlying function differs from Philosopher.propose_async,
        # it is a native override.
        from po_core.philosophers.base import Philosopher

        base_fn = Philosopher.propose_async
        return getattr(method, "__func__", None) is not base_fn

    async def _dispatch_one(
        self,
        ph: "PhilosopherProtocol",
        ctx: "Context",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
        tracer: Optional["TracePort"] = None,
        limit_per_philosopher: int = 1,
    ) -> _ExecutionResult:
        """Run a single philosopher and return structured execution metadata.

        If *tracer* is provided, a ``PhilosopherCompleted`` event is emitted
        immediately after the philosopher finishes (success or failure), enabling
        real-time SSE streaming of per-philosopher results.
        """
        pid = getattr(ph, "name", ph.__class__.__name__)
        t0 = perf_counter()
        budget = ExecutionBudget(timeout_s=self._timeout_s)
        supports_async_budget = _supports_budget_kwarg(getattr(ph, "propose_async", None))

        try:
            if self._has_native_async(ph):
                # Native async — runs on event loop directly
                if supports_async_budget:
                    ph_proposals = await asyncio.wait_for(
                        ph.propose_async(ctx, intent, tensors, memory, budget=budget),
                        timeout=self._timeout_s,
                    )
                else:
                    ph_proposals = await asyncio.wait_for(
                        ph.propose_async(ctx, intent, tensors, memory),
                        timeout=self._timeout_s,
                    )

                budget.raise_if_cancelled_or_expired()
                dt = int((perf_counter() - t0) * 1000)
                proposals = (
                    [p for p in ph_proposals if p is not None] if ph_proposals else []
                )
                selected = proposals[:limit_per_philosopher]
                embedded = [
                    _embed_author_proposal(p, pid, idx) for idx, p in enumerate(selected)
                ]
                result = _build_execution_result(
                    philosopher_id=pid,
                    proposals=embedded,
                    n=len(proposals),
                    timed_out=False,
                    error=None,
                    latency_ms=dt,
                )
            else:
                hard_timeout_max_s = float(os.getenv("PO_PHILOSOPHER_HARD_TIMEOUT_MAX_S", "0.01"))
                if self._timeout_s <= hard_timeout_max_s:
                    outcome = await asyncio.to_thread(
                        _run_one_in_subprocess,
                        SerializedJob(
                            ph,
                            ctx,
                            intent,
                            tensors,
                            memory,
                            limit_per_philosopher,
                            self._timeout_s,
                        ),
                    )
                else:
                    loop = asyncio.get_event_loop()
                    if self._executor is None:
                        self._executor = ThreadPoolExecutor(
                            max_workers=self._max_workers,
                            thread_name_prefix="po_phil",
                        )
                    outcome = await loop.run_in_executor(
                        self._executor,
                        _run_one_in_thread,
                        ph,
                        ctx,
                        intent,
                        tensors,
                        memory,
                        limit_per_philosopher,
                        self._timeout_s,
                    )
                result = _execution_result_from_outcome(outcome)

        except asyncio.TimeoutError:
            budget.cancel()
            dt = int((perf_counter() - t0) * 1000)
            result = _build_execution_result(
                philosopher_id=pid,
                n=0,
                timed_out=True,
                error=_cooperative_timeout_error(self._timeout_s, "async"),
                latency_ms=dt,
            )
        except ExecutionBudgetExceeded:
            budget.cancel()
            dt = int((perf_counter() - t0) * 1000)
            result = _build_execution_result(
                philosopher_id=pid,
                n=0,
                timed_out=True,
                error=_cooperative_timeout_error(self._timeout_s, "async"),
                latency_ms=dt,
            )
        except Exception as e:
            dt = int((perf_counter() - t0) * 1000)
            tb = traceback.format_exc()
            result = _build_execution_result(
                philosopher_id=pid,
                n=0,
                timed_out=False,
                error=f"{type(e).__name__}: {e}\n{tb}",
                latency_ms=dt,
            )

        # Emit per-philosopher completion event for real-time SSE streaming.
        # This fires as soon as the philosopher finishes, before other philosophers
        # complete, so SSE clients see results progressively.
        if tracer is not None:
            n_out = result.n
            err_out = result.error
            dt_out = result.latency_ms
            from po_core.domain.trace_event import TraceEvent

            tracer.emit(
                TraceEvent.now(
                    "PhilosopherCompleted",
                    ctx.request_id,
                    {
                        "name": pid,
                        "n": n_out,
                        "latency_ms": dt_out,
                        "ok": result.ok,
                    },
                )
            )

        return result

    async def run(
        self,
        philosophers: Sequence["PhilosopherProtocol"],
        ctx: "Context",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
        tracer: Optional["TracePort"] = None,
        limit_per_philosopher: int = 1,
    ) -> Tuple[List["Proposal"], List[RunResult]]:
        """Run all philosophers concurrently and collect results.

        If *tracer* is provided, a ``PhilosopherCompleted`` event is emitted
        for each philosopher as it finishes (not after all complete), enabling
        real-time progressive streaming via the SSE endpoint.

        Returns:
            Tuple of (proposals, run_results) — same shape as async_run_philosophers().
        """
        proposals: List["Proposal"] = []
        results: List[RunResult] = []

        if not philosophers:
            return proposals, results

        limit = max(0, min(limit_per_philosopher, 5))

        tasks = [
            asyncio.create_task(
                self._dispatch_one(ph, ctx, intent, tensors, memory, tracer, limit)
            )
            for ph in philosophers
        ]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        for ph, outcome in zip(philosophers, raw_results):
            pid = getattr(ph, "name", ph.__class__.__name__)
            if isinstance(outcome, Exception):
                results.append(
                    _build_execution_result(
                        philosopher_id=pid,
                        n=0,
                        timed_out=isinstance(outcome, asyncio.TimeoutError),
                        error=f"{type(outcome).__name__}: {outcome}",
                        latency_ms=None,
                    ).to_run_result()
                )
            else:
                execution_result = outcome
                results.append(execution_result.to_run_result())
                proposals.extend(execution_result.proposals)

        return proposals, results


def _embed_author_proposal(
    p: "Proposal", author: str, proposal_index: int
) -> "Proposal":
    """Embed philosopher author ID into Proposal.extra (shared helper)."""
    from po_core.domain.proposal import Proposal

    extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
    pc_src = extra.get(PO_CORE, {})
    pc = dict(pc_src) if isinstance(pc_src, Mapping) else {}
    pc[AUTHOR] = author
    pc["proposal_index"] = proposal_index
    extra[PO_CORE] = pc
    return Proposal(
        proposal_id=p.proposal_id,
        action_type=p.action_type,
        content=p.content,
        confidence=p.confidence,
        assumption_tags=list(p.assumption_tags),
        risk_tags=list(p.risk_tags),
        extra=extra,
    )


async def async_run_philosophers(
    philosophers: Sequence["PhilosopherProtocol"],
    ctx: "Context",
    intent: "Intent",
    tensors: "TensorSnapshot",
    memory: "MemorySnapshot",
    *,
    max_workers: int,
    timeout_s: float,
    limit_per_philosopher: int = 1,
    tracer: Optional["TracePort"] = None,
) -> Tuple[List["Proposal"], List[RunResult]]:
    """Async-native philosopher execution — delegates to AsyncPartyMachine.

    Backward-compatible wrapper around :class:`AsyncPartyMachine`.  New code
    should prefer ``async with AsyncPartyMachine(...)`` for explicit lifecycle
    management.  This function creates a machine, runs it, and shuts down the
    executor with ``wait=True`` to guarantee clean resource release.

    Args:
        philosophers: Sequence of philosopher instances to execute.
        ctx: Context for the current request.
        intent: Parsed intent from the intention stage.
        tensors: Current tensor snapshot (safety metrics).
        memory: Current memory snapshot.
        max_workers: Maximum number of parallel threads.
        timeout_s: Per-philosopher timeout in seconds.
        tracer: Optional tracer for real-time per-philosopher SSE events.
            When provided, a ``PhilosopherCompleted`` event is emitted as
            each philosopher finishes rather than after all complete.

    Returns:
        Tuple of:
        - List[Proposal]: Successfully generated proposals.
        - List[RunResult]: Execution results for each philosopher.
    """
    async with AsyncPartyMachine(
        max_workers=max_workers, timeout_s=timeout_s
    ) as machine:
        return await machine.run(
            philosophers,
            ctx,
            intent,
            tensors,
            memory,
            tracer,
            limit_per_philosopher=limit_per_philosopher,
        )


# ============================================================================
# Research-Based Knowledge Base
# ============================================================================

# Best 4-philosopher combinations (from RQ1)
OPTIMAL_4_COMBOS: Dict[PhilosophicalTheme, List[List[str]]] = {
    PhilosophicalTheme.ETHICS: [
        ["kant", "mill", "levinas", "confucius"],
        ["aristotle", "kant", "rawls", "levinas"],
        ["confucius", "dewey", "levinas", "arendt"],
    ],
    PhilosophicalTheme.EXISTENCE: [
        ["heidegger", "sartre", "kierkegaard", "levinas"],
        ["heidegger", "merleau_ponty", "levinas", "watsuji"],
        ["sartre", "kierkegaard", "dewey", "watsuji"],
    ],
    PhilosophicalTheme.KNOWLEDGE: [
        ["aristotle", "dewey", "peirce", "wittgenstein"],
        ["kant", "dewey", "peirce", "merleau_ponty"],
        ["confucius", "dewey", "wittgenstein", "derrida"],
    ],
    PhilosophicalTheme.POLITICS: [
        ["aristotle", "rawls", "arendt", "confucius"],
        ["mill", "rawls", "arendt", "dewey"],
        ["aristotle", "mill", "arendt", "levinas"],
    ],
    PhilosophicalTheme.FREEDOM: [
        ["sartre", "mill", "dewey", "nietzsche"],
        ["kierkegaard", "mill", "arendt", "dewey"],
        ["sartre", "rawls", "dewey", "levinas"],
    ],
    PhilosophicalTheme.CONSCIOUSNESS: [
        ["heidegger", "merleau_ponty", "jung", "lacan"],
        ["sartre", "merleau_ponty", "jung", "watsuji"],
        ["kierkegaard", "jung", "lacan", "levinas"],
    ],
}

# Philosopher tension pairs (high dialectical tension)
HIGH_TENSION_PAIRS: List[Tuple[str, str]] = [
    ("kant", "nietzsche"),  # Duty vs. Will-to-Power
    ("aristotle", "derrida"),  # Essentialism vs. Deconstruction
    ("confucius", "sartre"),  # Harmony vs. Radical Freedom
    ("heidegger", "dewey"),  # Being vs. Pragmatism
    ("mill", "kierkegaard"),  # Utilitarianism vs. Existentialism
    ("rawls", "deleuze"),  # Justice vs. Difference
    ("levinas", "nietzsche"),  # Ethics of Other vs. Self-Overcoming
]

# Philosopher compatibility clusters
HARMONIOUS_CLUSTERS: Dict[str, List[str]] = {
    "continental": ["heidegger", "sartre", "kierkegaard", "merleau_ponty", "levinas"],
    "analytic": ["wittgenstein", "dewey", "peirce", "mill"],
    "eastern": ["confucius", "zhuangzi", "watsuji", "wabi_sabi"],
    "political": ["aristotle", "rawls", "arendt", "mill", "dewey"],
    "psychoanalytic": ["jung", "lacan", "nietzsche"],
    "postmodern": ["derrida", "deleuze", "badiou", "lacan"],
}


# ============================================================================
# Philosopher Party Machine
# ============================================================================


class PhilosopherPartyMachine:
    """
    Automatically suggests and runs optimal philosopher combinations
    based on research findings.
    """

    def __init__(self, verbose: bool = True):
        """Initialize the party machine."""
        self.verbose = verbose
        self.available_philosophers = [
            "aristotle",
            "kant",
            "mill",
            "confucius",
            "dewey",
            "heidegger",
            "sartre",
            "kierkegaard",
            "merleau_ponty",
            "levinas",
            "rawls",
            "arendt",
            "peirce",
            "wittgenstein",
            "derrida",
            "deleuze",
            "badiou",
            "jung",
            "watsuji",
            "zhuangzi",
            "wabi_sabi",
            "lacan",
        ]

    def suggest_party(
        self,
        theme: str,
        mood: PartyMood = PartyMood.BALANCED,
        custom_prompt: Optional[str] = None,
    ) -> PartyConfig:
        """
        Suggest optimal philosopher party configuration.

        Args:
            theme: Philosophical theme (ethics, existence, etc.)
            mood: Desired atmosphere (calm, balanced, chaotic, critical)
            custom_prompt: Optional custom theme description

        Returns:
            PartyConfig with suggested philosophers and parameters
        """
        # Normalize theme
        theme_key = self._match_theme(theme)

        # Determine optimal size based on mood and research
        size = self._determine_size(mood)

        # Select philosophers based on theme and mood
        philosophers = self._select_philosophers(theme_key, mood, size)

        # Calculate expected metrics
        tension = self._estimate_tension(philosophers, mood)
        emergence = self._estimate_emergence(philosophers, tension)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            theme, mood, philosophers, tension, emergence
        )

        config = PartyConfig(
            theme=custom_prompt or theme,
            mood=mood,
            philosophers=philosophers,
            expected_size=len(philosophers),
            expected_tension=tension,
            expected_emergence=emergence,
            reasoning=reasoning,
        )

        if self.verbose:
            self._display_config(config)

        return config

    def _match_theme(self, theme: str) -> PhilosophicalTheme:
        """Match user theme to enum."""
        theme_lower = theme.lower()

        # Direct match
        for t in PhilosophicalTheme:
            if t.value in theme_lower:
                return t

        # Keyword matching
        keywords = {
            PhilosophicalTheme.ETHICS: [
                "moral",
                "right",
                "wrong",
                "responsibility",
                "duty",
            ],
            PhilosophicalTheme.EXISTENCE: ["being", "dasein", "ontology", "existence"],
            PhilosophicalTheme.KNOWLEDGE: [
                "epistemology",
                "truth",
                "knowledge",
                "certainty",
            ],
            PhilosophicalTheme.POLITICS: [
                "society",
                "democracy",
                "power",
                "government",
            ],
            PhilosophicalTheme.CONSCIOUSNESS: [
                "mind",
                "awareness",
                "subject",
                "psyche",
            ],
            PhilosophicalTheme.FREEDOM: ["liberty", "autonomy", "choice", "free will"],
            PhilosophicalTheme.MEANING: ["purpose", "significance", "life", "value"],
            PhilosophicalTheme.JUSTICE: ["fairness", "equality", "rights", "law"],
            PhilosophicalTheme.TECHNOLOGY: ["AI", "machine", "digital", "virtual"],
            PhilosophicalTheme.DEATH: ["mortality", "dying", "afterlife", "finitude"],
        }

        for theme_enum, words in keywords.items():
            if any(word in theme_lower for word in words):
                return theme_enum

        # Default to meaning
        return PhilosophicalTheme.MEANING

    def _determine_size(self, mood: PartyMood) -> int:
        """Determine optimal group size based on mood and research."""
        # Research findings: 8-14 optimal, peak at 15
        if mood == PartyMood.CALM:
            return random.choice([4, 5, 6])  # Smaller, harmonious groups
        elif mood == PartyMood.BALANCED:
            return random.choice([8, 10, 12, 15])  # Optimal range
        elif mood == PartyMood.CHAOTIC:
            return random.choice([15, 18, 20])  # Larger, more complex
        else:  # CRITICAL
            return random.choice([6, 8, 10])  # Medium with critical focus

    def _select_philosophers(
        self,
        theme: PhilosophicalTheme,
        mood: PartyMood,
        size: int,
    ) -> List[str]:
        """Select philosophers based on theme, mood, and desired size."""
        selected = []

        # Start with optimal combo if size <= 4
        if size <= 4 and theme in OPTIMAL_4_COMBOS:
            combo = random.choice(OPTIMAL_4_COMBOS[theme])
            return combo[:size]

        # For larger groups, build strategically
        if theme in OPTIMAL_4_COMBOS:
            # Start with a good base combo
            base = random.choice(OPTIMAL_4_COMBOS[theme])
            selected.extend(base)

        # Add philosophers based on mood
        if mood == PartyMood.CALM:
            # Add harmonious philosophers
            cluster = random.choice(list(HARMONIOUS_CLUSTERS.values()))
            for p in cluster:
                if p not in selected and len(selected) < size:
                    selected.append(p)

        elif mood == PartyMood.CHAOTIC:
            # Add tension-creating pairs
            for p1, p2 in HIGH_TENSION_PAIRS:
                if len(selected) >= size:
                    break
                if p1 not in selected:
                    selected.append(p1)
                if len(selected) < size and p2 not in selected:
                    selected.append(p2)

        elif mood == PartyMood.CRITICAL:
            # Add critical/skeptical philosophers
            critical_types = [
                "nietzsche",
                "wittgenstein",
                "derrida",
                "kierkegaard",
                "sartre",
            ]
            for p in critical_types:
                if p not in selected and len(selected) < size:
                    selected.append(p)

        # Fill remaining slots with diverse philosophers
        remaining = [p for p in self.available_philosophers if p not in selected]
        random.shuffle(remaining)

        while len(selected) < size and remaining:
            selected.append(remaining.pop())

        return selected[:size]

    def _estimate_tension(self, philosophers: List[str], mood: PartyMood) -> float:
        """Estimate dialectical tension level."""
        tension = 0.0

        # Count tension pairs
        tension_count = 0
        for p1, p2 in HIGH_TENSION_PAIRS:
            if p1 in philosophers and p2 in philosophers:
                tension_count += 1

        # Base tension from pairs
        tension = min(1.0, tension_count * 0.2)

        # Mood adjustment
        mood_multiplier = {
            PartyMood.CALM: 0.3,
            PartyMood.BALANCED: 0.7,
            PartyMood.CHAOTIC: 1.2,
            PartyMood.CRITICAL: 0.9,
        }
        tension *= mood_multiplier[mood]

        # Diversity bonus
        clusters_present = sum(
            1
            for cluster in HARMONIOUS_CLUSTERS.values()
            if any(p in philosophers for p in cluster)
        )
        diversity_factor = min(1.0, clusters_present / 4)
        tension += diversity_factor * 0.3

        return min(1.0, tension)

    def _estimate_emergence(self, philosophers: List[str], tension: float) -> float:
        """Estimate emergence probability based on research findings."""
        # Base from group size (research: 8-14 optimal)
        size = len(philosophers)
        if 8 <= size <= 14:
            size_factor = 1.0
        elif size == 15:
            size_factor = 1.1  # Peak performance
        elif 4 <= size < 8:
            size_factor = 0.7
        else:
            size_factor = 0.5

        # Research finding: Tension increases emergence by ~19.75x (1975%)
        # We model this as: emergence = base * (1 + tension * 19)
        base_emergence = 0.05  # 5% baseline
        emergence = base_emergence * (1 + tension * 19) * size_factor

        return min(1.0, emergence)

    def _generate_reasoning(
        self,
        theme: str,
        mood: PartyMood,
        philosophers: List[str],
        tension: float,
        emergence: float,
    ) -> str:
        """Generate human-readable reasoning for the configuration."""
        lines = [
            f"🎯 Theme: {theme}",
            f"🎭 Mood: {mood.value}",
            f"👥 Party size: {len(philosophers)} philosophers",
            "",
            f"⚡ Expected tension: {tension:.1%}",
            f"✨ Expected emergence: {emergence:.1%}",
            "",
            "📊 Research basis:",
        ]

        # Add research insights
        if len(philosophers) == 4:
            lines.append("  • Optimal 4-philosopher combo (100% emergence from RQ1)")
        elif 8 <= len(philosophers) <= 14:
            lines.append("  • Optimal group size range (RQ3: 8-14 philosophers)")
        elif len(philosophers) == 15:
            lines.append("  • Peak performance size (RQ3: 15 philosophers)")

        if tension > 0.6:
            lines.append(
                f"  • High dialectical tension → +{int(tension * 1975)}% emergence boost (RQ4)"
            )

        lines.append("")
        lines.append(f"🧠 Selected philosophers: {', '.join(philosophers)}")

        return "\n".join(lines)

    def _display_config(self, config: PartyConfig) -> None:
        """Display party configuration with Rich formatting."""
        console.print(
            Panel(
                config.reasoning,
                title="[bold magenta]🎉 Philosopher Party Configuration[/bold magenta]",
                border_style="magenta",
            )
        )


# ============================================================================
# Factory Functions
# ============================================================================


def create_party(theme: str, mood: str = "balanced") -> PartyConfig:
    """
    Quick factory function to create a party configuration.

    Args:
        theme: Philosophical theme
        mood: Party mood (calm, balanced, chaotic, critical)

    Returns:
        PartyConfig ready to run
    """
    machine = PhilosopherPartyMachine(verbose=False)
    mood_enum = PartyMood(mood)
    return machine.suggest_party(theme, mood_enum)


__all__ = [
    "PhilosopherPartyMachine",
    "PartyConfig",
    "PartyResults",
    "PartyMood",
    "PhilosophicalTheme",
    "create_party",
    # Parallel execution
    "run_philosophers",
    "RunResult",
    # Phase 5.2: Async execution
    "AsyncPartyMachine",
    "async_run_philosophers",
]
