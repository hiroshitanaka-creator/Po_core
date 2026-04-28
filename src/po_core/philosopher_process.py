from __future__ import annotations

import inspect
import traceback
from dataclasses import dataclass
from time import perf_counter
from typing import TYPE_CHECKING, Mapping

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.philosophers.identity import resolve_philosopher_id
from po_core.runtime.execution_budget import ExecutionBudget, ExecutionBudgetExceeded

if TYPE_CHECKING:
    from po_core.domain.context import Context
    from po_core.domain.intent import Intent
    from po_core.domain.memory_snapshot import MemorySnapshot
    from po_core.domain.proposal import Proposal
    from po_core.domain.tensor_snapshot import TensorSnapshot
    from po_core.philosophers.base import PhilosopherProtocol


@dataclass(frozen=True)
class ExecOutcome:
    proposals: list["Proposal"]
    n: int
    timed_out: bool
    error: str | None
    latency_ms: int
    philosopher_id: str


@dataclass(frozen=True)
class SerializedJob:
    philosopher: "PhilosopherProtocol"
    ctx: "Context"
    intent: "Intent"
    tensors: "TensorSnapshot"
    memory: "MemorySnapshot"
    limit_per_philosopher: int
    timeout_s: float


def _supports_budget_kwarg(method: object) -> bool:
    try:
        signature = inspect.signature(method)
    except (TypeError, ValueError):
        return False
    budget_param = signature.parameters.get("budget")
    if budget_param is None:
        return False
    return budget_param.kind in {
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.KEYWORD_ONLY,
    }


def _budget_cancelled_error(mode: str) -> str:
    return f"Execution stopped cooperatively ({mode})"


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


def run_one_philosopher(job: SerializedJob) -> ExecOutcome:
    pid = resolve_philosopher_id(job.philosopher)
    t0 = perf_counter()
    budget = ExecutionBudget(timeout_s=job.timeout_s)
    supports_budget = _supports_budget_kwarg(getattr(job.philosopher, "propose"))
    try:
        budget.raise_if_cancelled_or_expired()
        if supports_budget:
            raw = job.philosopher.propose(
                job.ctx, job.intent, job.tensors, job.memory, budget=budget
            )
            budget.raise_if_cancelled_or_expired()
        else:
            raw = job.philosopher.propose(job.ctx, job.intent, job.tensors, job.memory)
        proposals_local = [p for p in raw if p is not None] if raw else []
        selected = proposals_local[: job.limit_per_philosopher]
        embedded = [
            _embed_author_proposal(p, pid, idx) for idx, p in enumerate(selected)
        ]
        dt = int((perf_counter() - t0) * 1000)
        return ExecOutcome(embedded, len(proposals_local), False, None, dt, pid)
    except ExecutionBudgetExceeded:
        dt = int((perf_counter() - t0) * 1000)
        return ExecOutcome(
            [], 0, False, _budget_cancelled_error("budget signalled"), dt, pid
        )
    except Exception as e:
        dt = int((perf_counter() - t0) * 1000)
        tb = traceback.format_exc()
        return ExecOutcome([], 0, False, f"{type(e).__name__}: {e}\n{tb}", dt, pid)
