from __future__ import annotations

import asyncio
from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import AsyncPartyMachine


@dataclass
class _AsyncSuccessPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return []

    async def propose_async(self, ctx, intent, tensors, memory):
        await asyncio.sleep(0)
        return [
            Proposal(
                proposal_id=f"{self.name}-p1",
                action_type="answer",
                content="success",
                confidence=0.8,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


@dataclass
class _AsyncTimeoutPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return []

    async def propose_async(self, ctx, intent, tensors, memory):
        await asyncio.sleep(0.2)
        return []


async def _run_machine(philosopher, timeout_s: float):
    async with AsyncPartyMachine(max_workers=1, timeout_s=timeout_s) as machine:
        return await machine.run(
            [philosopher],
            ctx=type("Ctx", (), {"request_id": "req-timeout-contract"})(),
            intent=None,
            tensors=None,
            memory=None,
        )


def test_async_timeout_reports_authoritative_timeout_without_string_parsing():
    async def _exercise():
        return await _run_machine(_AsyncTimeoutPhil(name="slow-async"), timeout_s=0.05)

    proposals, results = asyncio.run(_exercise())

    assert proposals == []
    assert len(results) == 1
    assert results[0].timed_out is True
    assert results[0].ok is False
    assert results[0].n == 0
    assert results[0].error is not None
    assert "TimeoutError" not in results[0].error


def test_async_success_reports_not_timed_out():
    proposals, results = asyncio.run(
        _run_machine(_AsyncSuccessPhil(name="fast-async"), timeout_s=0.05)
    )

    assert len(proposals) == 1
    assert len(results) == 1
    assert results[0].timed_out is False
    assert results[0].ok is True
    assert results[0].n == 1
