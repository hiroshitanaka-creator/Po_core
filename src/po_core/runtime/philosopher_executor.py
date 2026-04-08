from __future__ import annotations

import asyncio
import multiprocessing
import os
import queue as queue_module
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from dataclasses import dataclass
from time import perf_counter
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
)

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.philosopher_process import ExecOutcome, SerializedJob, run_one_philosopher

if TYPE_CHECKING:
    from po_core.domain.context import Context
    from po_core.domain.intent import Intent
    from po_core.domain.memory_snapshot import MemorySnapshot
    from po_core.domain.proposal import Proposal
    from po_core.domain.tensor_snapshot import TensorSnapshot
    from po_core.philosophers.base import PhilosopherProtocol


@dataclass(frozen=True)
class RunResult:
    philosopher_id: str
    ok: bool
    n: int = 0
    timed_out: bool = False
    error: Optional[str] = None
    latency_ms: Optional[int] = None


@dataclass(frozen=True)
class ExecutionResult:
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


@dataclass(frozen=True)
class ExecutorConfig:
    mode: str
    max_workers: int
    timeout_s: float
    limit_per_philosopher: int


class PhilosopherExecutor(Protocol):
    def run(
        self,
        philosophers: Sequence["PhilosopherProtocol"],
        ctx: "Context",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
    ) -> Tuple[List["Proposal"], List[RunResult]]: ...


def _soft_timeout_error(timeout_s: float, mode: str) -> str:
    return (
        f"Soft timeout after {timeout_s}s ({mode} fallback=empty_proposals; "
        "background work may still continue)"
    )


def _hard_timeout_error(timeout_s: float) -> str:
    return f"Hard timeout after {timeout_s}s"


def _child_crash_error(exit_code: int | None) -> str:
    return f"Child process crashed (exit_code={exit_code})"


def _bootstrap_failure_error(exc: Exception) -> str:
    return f"Worker bootstrap failure: {type(exc).__name__}: {exc}"


def _build_execution_result(
    *,
    philosopher_id: str,
    proposals: Optional[List["Proposal"]] = None,
    n: int,
    timed_out: bool,
    error: Optional[str],
    latency_ms: Optional[int],
) -> ExecutionResult:
    selected_proposals = list(proposals or [])
    return ExecutionResult(
        philosopher_id=philosopher_id,
        proposals=[] if timed_out else selected_proposals,
        ok=(error is None and not timed_out),
        n=(0 if timed_out else n),
        timed_out=timed_out,
        error=error,
        latency_ms=latency_ms,
    )


def _execution_result_from_outcome(outcome: ExecOutcome) -> ExecutionResult:
    return _build_execution_result(
        philosopher_id=outcome.philosopher_id,
        proposals=outcome.proposals,
        n=outcome.n,
        timed_out=outcome.timed_out,
        error=outcome.error,
        latency_ms=outcome.latency_ms,
    )


def _embed_author_proposal(
    p: "Proposal", author: str, proposal_index: int
) -> "Proposal":
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
        SerializedJob(
            ph, ctx, intent, tensors, memory, limit_per_philosopher, timeout_s
        )
    )
    elapsed_ms = int((perf_counter() - start) * 1000)
    if elapsed_ms > timeout_s * 1000 and outcome.error is None:
        # A thread future can time out while the underlying work keeps running,
        # so thread mode cannot guarantee production-safe cancellation.
        return ExecOutcome(
            [], 0, True, _soft_timeout_error(timeout_s, "thread"), elapsed_ms, pid
        )
    return outcome


def _process_worker(job: SerializedJob, queue: multiprocessing.queues.Queue) -> None:
    """Execute philosopher in a subprocess and put ExecOutcome into the queue.

    Wraps run_one_philosopher() to catch PicklingError from queue.put() — which
    can occur when a philosopher produces a Proposal with a non-picklable attribute
    (e.g. circular reference, custom TensorSnapshot).  In that case, an error
    ExecOutcome is queued instead of silently crashing the child process.
    """
    import pickle

    pid = getattr(job.philosopher, "name", job.philosopher.__class__.__name__)
    try:
        outcome = run_one_philosopher(job)
    except Exception as exc:
        queue.put(
            ExecOutcome(
                proposals=[],
                n=0,
                timed_out=False,
                error=_bootstrap_failure_error(exc),
                latency_ms=0,
                philosopher_id=pid,
            )
        )
        return
    try:
        queue.put(outcome)
    except (pickle.PicklingError, TypeError, AttributeError) as exc:
        # Outcome is not serializable — queue a stripped-down error outcome instead
        error_outcome = ExecOutcome(
            proposals=[],
            n=0,
            timed_out=False,
            error=f"IPC serialize error (PicklingError) for {pid}: {type(exc).__name__}: {exc}",
            latency_ms=outcome.latency_ms,
            philosopher_id=pid,
        )
        queue.put(error_outcome)


def _run_one_in_subprocess(job: SerializedJob) -> ExecOutcome:
    pid = getattr(job.philosopher, "name", job.philosopher.__class__.__name__)
    start = perf_counter()
    ctx = multiprocessing.get_context(
        "fork" if "fork" in multiprocessing.get_all_start_methods() else "spawn"
    )
    queue = ctx.Queue(maxsize=1)
    proc = ctx.Process(target=_process_worker, args=(job, queue))
    proc.start()
    bootstrap_grace_s = float(
        os.getenv("PO_PHILOSOPHER_PROCESS_BOOTSTRAP_GRACE_S", "0.05")
    )
    try:
        outcome = queue.get(timeout=job.timeout_s + bootstrap_grace_s)
    except queue_module.Empty:
        proc.join(timeout=0.01)
        exit_code = proc.exitcode
        proc.terminate()
        proc.join(timeout=1.0)
        if proc.is_alive():
            proc.kill()
            proc.join(timeout=1.0)
        elapsed_ms = int((perf_counter() - start) * 1000)
        queue.close()
        if exit_code not in (None, 0):
            return ExecOutcome(
                [], 0, False, _child_crash_error(exit_code), elapsed_ms, pid
            )
        return ExecOutcome(
            [], 0, True, _hard_timeout_error(job.timeout_s), elapsed_ms, pid
        )
    except (OSError, EOFError) as exc:
        proc.terminate()
        proc.join(timeout=1.0)
        elapsed_ms = int((perf_counter() - start) * 1000)
        queue.close()
        return ExecOutcome([], 0, False, _bootstrap_failure_error(exc), elapsed_ms, pid)

    proc.join(timeout=1.0)
    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=1.0)
    elapsed_ms = int((perf_counter() - start) * 1000)
    queue.close()
    if isinstance(outcome, ExecOutcome):
        if outcome.latency_ms > job.timeout_s * 1000:
            return ExecOutcome(
                [], 0, True, _hard_timeout_error(job.timeout_s), elapsed_ms, pid
            )
        return outcome
    return ExecOutcome([], 0, False, "Worker returned invalid outcome", elapsed_ms, pid)


class ThreadPhilosopherExecutor:
    def __init__(self, config: ExecutorConfig) -> None:
        self._config = config

    def run(self, philosophers, ctx, intent, tensors, memory):
        return _run_sync_jobs(
            philosophers=philosophers,
            ctx=ctx,
            intent=intent,
            tensors=tensors,
            memory=memory,
            config=self._config,
            runner="thread",
        )


class ProcessPhilosopherExecutor:
    def __init__(self, config: ExecutorConfig) -> None:
        self._config = config

    def run(self, philosophers, ctx, intent, tensors, memory):
        return _run_sync_jobs(
            philosophers=philosophers,
            ctx=ctx,
            intent=intent,
            tensors=tensors,
            memory=memory,
            config=self._config,
            runner="process",
        )


RunnerKind = str


def _run_sync_jobs(
    *,
    philosophers: Sequence["PhilosopherProtocol"],
    ctx: "Context",
    intent: "Intent",
    tensors: "TensorSnapshot",
    memory: "MemorySnapshot",
    config: ExecutorConfig,
    runner: RunnerKind,
) -> Tuple[List["Proposal"], List[RunResult]]:
    from po_core.domain.proposal import Proposal

    proposals: List[Proposal] = []
    if not philosophers:
        return proposals, []

    result_by_index: Dict[int, RunResult] = {}
    proposals_by_index: Dict[int, List[Proposal]] = {}
    executor = ThreadPoolExecutor(max_workers=config.max_workers)
    try:
        futures = {}
        for idx, ph in enumerate(philosophers):
            if runner == "process":
                job = SerializedJob(
                    ph,
                    ctx,
                    intent,
                    tensors,
                    memory,
                    config.limit_per_philosopher,
                    config.timeout_s,
                )
                futures[idx] = executor.submit(_run_one_in_subprocess, job)
            else:
                futures[idx] = executor.submit(
                    _run_one_in_thread,
                    ph,
                    ctx,
                    intent,
                    tensors,
                    memory,
                    config.limit_per_philosopher,
                    config.timeout_s,
                )

        for idx, ph in enumerate(philosophers):
            pid = getattr(ph, "name", ph.__class__.__name__)
            try:
                outcome = futures[idx].result(
                    timeout=None if runner == "process" else config.timeout_s + 0.05
                )
                execution_result = _execution_result_from_outcome(outcome)
            except FuturesTimeoutError:
                execution_result = _build_execution_result(
                    philosopher_id=pid,
                    n=0,
                    timed_out=True,
                    error=_soft_timeout_error(config.timeout_s, "thread"),
                    latency_ms=None,
                )
            except Exception as exc:
                execution_result = _build_execution_result(
                    philosopher_id=pid,
                    n=0,
                    timed_out=False,
                    error=f"{type(exc).__name__}: {exc}",
                    latency_ms=None,
                )

            result_by_index[idx] = execution_result.to_run_result()
            if execution_result.proposals:
                stable = [
                    _embed_author_proposal(
                        p, execution_result.philosopher_id, proposal_index
                    )
                    for proposal_index, p in enumerate(execution_result.proposals)
                ]
                proposals_by_index[idx] = stable
    finally:
        executor.shutdown(wait=False, cancel_futures=False)

    results = [result_by_index[idx] for idx in range(len(philosophers))]
    for idx in range(len(philosophers)):
        proposals.extend(proposals_by_index.get(idx, []))
    return proposals, results


def build_executor(config: ExecutorConfig) -> PhilosopherExecutor:
    if config.mode == "process":
        return ProcessPhilosopherExecutor(config)
    return ThreadPhilosopherExecutor(config)


async def run_in_process_async(
    job: SerializedJob,
    *,
    executor: ThreadPoolExecutor,
    semaphore: asyncio.Semaphore,
) -> ExecOutcome:
    async with semaphore:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, _run_one_in_subprocess, job)
