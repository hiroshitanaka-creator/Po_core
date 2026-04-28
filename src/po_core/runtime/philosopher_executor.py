from __future__ import annotations

import asyncio
import logging
import multiprocessing
import os
import pickle
import queue as queue_mod
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from dataclasses import dataclass
from time import perf_counter
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    cast,
)

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.philosopher_process import ExecOutcome, SerializedJob, run_one_philosopher
from po_core.philosophers.identity import resolve_philosopher_id

logger = logging.getLogger(__name__)

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


# Distinct error codes for subprocess failure classification.  These are
# deliberately kept free of the word "timeout" so that downstream consumers
# (observability, tests, alerting) can distinguish bootstrap / IPC / exit
# failures from genuine timeouts.  The shape is
# ``{code}: {detail}`` so both a machine-readable prefix and a human-readable
# tail are retained for logs and traces.
ERROR_CODE_CHILD_BOOTSTRAP_FAILED = "child_bootstrap_failed"
ERROR_CODE_CHILD_EXITED = "child_exited_before_result"
ERROR_CODE_IPC_QUEUE_EOF = "ipc_queue_eof"
ERROR_CODE_IPC_SERIALIZATION_FAILED = "ipc_serialization_failed"
ERROR_CODE_IPC_UNKNOWN = "ipc_unknown_failure"


def _format_subprocess_error(code: str, detail: str) -> str:
    return f"{code}: {detail}"


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
    pid = resolve_philosopher_id(ph)
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
    pid = resolve_philosopher_id(job.philosopher)
    outcome = run_one_philosopher(job)
    try:
        queue.put(outcome)
    except (pickle.PicklingError, TypeError, AttributeError) as exc:
        # Outcome is not serializable — queue a stripped-down error outcome instead.
        error_outcome = ExecOutcome(
            proposals=[],
            n=0,
            timed_out=False,
            error=_format_subprocess_error(
                ERROR_CODE_IPC_SERIALIZATION_FAILED,
                f"failed to serialize outcome for {pid}: "
                f"{type(exc).__name__}: {exc}",
            ),
            latency_ms=outcome.latency_ms,
            philosopher_id=pid,
        )
        queue.put(error_outcome)


def _terminate_process(proc: object) -> None:
    """Best-effort cooperative then forceful termination of a subprocess handle."""
    try:
        proc.terminate()  # type: ignore[attr-defined]
    except Exception as exc:
        logger.debug("terminate() failed on subprocess handle: %s", exc)
    try:
        proc.join(timeout=1.0)  # type: ignore[attr-defined]
    except Exception as exc:
        logger.debug("join() failed on subprocess handle: %s", exc)
    try:
        if proc.is_alive():  # type: ignore[attr-defined]
            proc.kill()  # type: ignore[attr-defined]
            proc.join(timeout=1.0)  # type: ignore[attr-defined]
    except Exception as exc:
        logger.debug("kill() failed on subprocess handle: %s", exc)


def _close_queue(queue: object) -> None:
    try:
        queue.close()  # type: ignore[attr-defined]
    except Exception as exc:
        logger.debug("queue.close() failed: %s", exc)


def _classify_subprocess_get_failure(
    exc: BaseException, proc: object
) -> tuple[str, str]:
    """Classify a failure raised by ``queue.get`` into (error_code, detail).

    - ``queue.Empty``            → hard timeout (caller supplies timeout string).
    - ``EOFError``/``BrokenPipeError`` + dead process with exitcode !=0
                                  → child exited before posting (bootstrap / crash).
    - ``EOFError``/``BrokenPipeError`` otherwise
                                  → ipc queue EOF.
    - ``pickle.UnpicklingError``  → IPC deserialization failure.
    - anything else               → unknown IPC failure.
    """
    if isinstance(exc, queue_mod.Empty):
        # The caller is responsible for turning this into a hard-timeout
        # message; we return a sentinel here.
        return ("__timeout__", str(exc))

    exitcode = getattr(proc, "exitcode", None)
    alive = False
    try:
        alive = bool(proc.is_alive())  # type: ignore[attr-defined]
    except Exception:
        alive = False

    if isinstance(exc, (EOFError, BrokenPipeError)):
        if not alive and exitcode not in (None, 0):
            detail = (
                f"child exited with code {exitcode} before posting outcome "
                f"({type(exc).__name__}: {exc})"
            )
            return (ERROR_CODE_CHILD_BOOTSTRAP_FAILED, detail)
        if not alive and exitcode == 0:
            detail = (
                f"child exited cleanly without posting outcome "
                f"({type(exc).__name__}: {exc})"
            )
            return (ERROR_CODE_CHILD_EXITED, detail)
        return (
            ERROR_CODE_IPC_QUEUE_EOF,
            f"queue closed before outcome arrived ({type(exc).__name__}: {exc})",
        )

    if isinstance(exc, pickle.UnpicklingError):
        return (
            ERROR_CODE_IPC_SERIALIZATION_FAILED,
            f"failed to deserialize outcome from child ({type(exc).__name__}: {exc})",
        )

    # OSError (closed pipes, spawn failures) — treat as child crash if dead.
    if isinstance(exc, OSError):
        if not alive and exitcode not in (None, 0):
            return (
                ERROR_CODE_CHILD_BOOTSTRAP_FAILED,
                f"child exited with code {exitcode} before posting outcome "
                f"({type(exc).__name__}: {exc})",
            )
        return (
            ERROR_CODE_IPC_UNKNOWN,
            f"os-level IPC failure ({type(exc).__name__}: {exc})",
        )

    return (
        ERROR_CODE_IPC_UNKNOWN,
        f"unexpected IPC failure ({type(exc).__name__}: {exc})",
    )


def _run_one_in_subprocess(job: SerializedJob) -> ExecOutcome:
    pid = resolve_philosopher_id(job.philosopher)
    start = perf_counter()
    method = "fork" if "fork" in multiprocessing.get_all_start_methods() else "spawn"
    # ``get_context`` returns ``BaseContext`` whose type stubs do not expose
    # ``Process``/``Queue`` despite the concrete contexts (Spawn/ForkContext)
    # defining them.  Cast through Any so mypy accepts the factory calls.
    ctx = cast(Any, multiprocessing.get_context(method))
    queue = ctx.Queue(maxsize=1)
    proc = ctx.Process(target=_process_worker, args=(job, queue))
    proc.start()
    bootstrap_grace_s = float(
        os.getenv("PO_PHILOSOPHER_PROCESS_BOOTSTRAP_GRACE_S", "0.05")
    )
    try:
        outcome = queue.get(timeout=job.timeout_s + bootstrap_grace_s)
    except queue_mod.Empty:
        # Genuine timeout: child is still running (or has not yet posted).
        _terminate_process(proc)
        elapsed_ms = int((perf_counter() - start) * 1000)
        _close_queue(queue)
        return ExecOutcome(
            [], 0, True, _hard_timeout_error(job.timeout_s), elapsed_ms, pid
        )
    except (
        EOFError,
        BrokenPipeError,
        OSError,
        pickle.UnpicklingError,
    ) as exc:
        # Child crash / bootstrap failure / IPC serialization failure — NOT a
        # timeout.  Classify with a distinct error code so observability does
        # not collapse these into the timeout bucket.
        code, detail = _classify_subprocess_get_failure(exc, proc)
        _terminate_process(proc)
        elapsed_ms = int((perf_counter() - start) * 1000)
        _close_queue(queue)
        if code == "__timeout__":
            return ExecOutcome(
                [], 0, True, _hard_timeout_error(job.timeout_s), elapsed_ms, pid
            )
        logger.warning(
            "Subprocess philosopher execution failed without timeout",
            extra={
                "philosopher_id": pid,
                "error_code": code,
                "detail": detail,
            },
        )
        return ExecOutcome(
            [], 0, False, _format_subprocess_error(code, detail), elapsed_ms, pid
        )
    except Exception as exc:
        # Unknown IPC-level failure: surface as structured error, not timeout.
        code, detail = _classify_subprocess_get_failure(exc, proc)
        _terminate_process(proc)
        elapsed_ms = int((perf_counter() - start) * 1000)
        _close_queue(queue)
        logger.warning(
            "Subprocess philosopher execution failed with unknown IPC error",
            extra={
                "philosopher_id": pid,
                "error_code": code,
                "detail": detail,
            },
        )
        return ExecOutcome(
            [], 0, False, _format_subprocess_error(code, detail), elapsed_ms, pid
        )

    proc.join(timeout=1.0)
    if proc.is_alive():
        _terminate_process(proc)
    elapsed_ms = int((perf_counter() - start) * 1000)
    _close_queue(queue)
    if isinstance(outcome, ExecOutcome):
        return outcome
    return ExecOutcome(
        [],
        0,
        False,
        _format_subprocess_error(
            ERROR_CODE_IPC_UNKNOWN,
            f"worker returned invalid outcome type: {type(outcome).__name__}",
        ),
        elapsed_ms,
        pid,
    )


class ThreadPhilosopherExecutor:
    def __init__(self, config: ExecutorConfig) -> None:
        self._config = config

    def run(
        self,
        philosophers: Sequence["PhilosopherProtocol"],
        ctx: "Context",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
    ) -> Tuple[List["Proposal"], List[RunResult]]:
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

    def run(
        self,
        philosophers: Sequence["PhilosopherProtocol"],
        ctx: "Context",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
    ) -> Tuple[List["Proposal"], List[RunResult]]:
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
            pid = resolve_philosopher_id(ph)
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


_VALID_EXECUTOR_MODES = frozenset({"process", "thread"})


def build_executor(config: ExecutorConfig) -> PhilosopherExecutor:
    """Build the philosopher executor for the given ``config.mode``.

    Unknown modes are rejected with ``ValueError`` (fail-closed) — previously
    any unrecognised mode silently fell back to the cooperative thread
    executor, which hides deployment misconfiguration.
    """
    mode = config.mode
    if mode == "process":
        return ProcessPhilosopherExecutor(config)
    if mode == "thread":
        return ThreadPhilosopherExecutor(config)
    raise ValueError(
        f"Unknown philosopher execution mode: {mode!r}. "
        f"Expected one of {sorted(_VALID_EXECUTOR_MODES)}."
    )


async def run_in_process_async(
    job: SerializedJob,
    *,
    executor: ThreadPoolExecutor,
    semaphore: asyncio.Semaphore,
) -> ExecOutcome:
    async with semaphore:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, _run_one_in_subprocess, job)
