from __future__ import annotations

import asyncio
import threading
import time
from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import async_run_philosophers
from po_core.philosopher_process import ExecOutcome


@dataclass
class _SyncPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return []


def test_async_process_executor_respects_max_workers(monkeypatch):
    import po_core.runtime.philosopher_executor as executor_mod

    state = {"current": 0, "peak": 0}
    lock = threading.Lock()

    def _fake_run_one_in_subprocess(job):
        with lock:
            state["current"] += 1
            state["peak"] = max(state["peak"], state["current"])
        try:
            time.sleep(0.05)
            proposal = Proposal(
                proposal_id=f"{job.philosopher.name}-proposal",
                action_type="answer",
                content=job.philosopher.name,
                confidence=0.8,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
            return ExecOutcome(
                proposals=[proposal],
                n=1,
                timed_out=False,
                error=None,
                latency_ms=50,
                philosopher_id=job.philosopher.name,
            )
        finally:
            with lock:
                state["current"] -= 1

    monkeypatch.setattr(executor_mod, "_run_one_in_subprocess", _fake_run_one_in_subprocess)

    async def _exercise():
        return await async_run_philosophers(
            [_SyncPhil(name=f"phil-{idx}") for idx in range(5)],
            ctx=type("Ctx", (), {"request_id": "req-async-process"})(),
            intent=None,
            tensors=None,
            memory=None,
            max_workers=2,
            timeout_s=1.0,
            limit_per_philosopher=1,
            execution_mode="process",
        )

    proposals, results = asyncio.run(_exercise())

    assert state["peak"] <= 2
    assert [result.philosopher_id for result in results] == [
        "phil-0",
        "phil-1",
        "phil-2",
        "phil-3",
        "phil-4",
    ]
    assert [proposal.proposal_id for proposal in proposals] == [
        "phil-0-proposal",
        "phil-1-proposal",
        "phil-2-proposal",
        "phil-3-proposal",
        "phil-4-proposal",
    ]
