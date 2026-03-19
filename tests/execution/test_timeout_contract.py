from __future__ import annotations

import time
from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers


@dataclass
class _SuccessPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return [
            Proposal(
                proposal_id=f"{self.name}-p1",
                action_type="answer",
                content="success",
                confidence=0.7,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


@dataclass
class _TimeoutPhil:
    name: str
    sleep_s: float

    def propose(self, ctx, intent, tensors, memory):
        time.sleep(self.sleep_s)
        return [
            Proposal(
                proposal_id=f"{self.name}-late",
                action_type="answer",
                content="late",
                confidence=0.1,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_sync_timeout_reports_authoritative_timeout_and_zero_proposals():
    proposals, results = run_philosophers(
        [_TimeoutPhil(name="slow-sync", sleep_s=0.2)],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=0.05,
    )

    assert proposals == []
    assert len(results) == 1
    assert results[0].timed_out is True
    assert results[0].ok is False
    assert results[0].n == 0


def test_sync_success_reports_not_timed_out():
    proposals, results = run_philosophers(
        [_SuccessPhil(name="fast-sync")],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=0.05,
    )

    assert len(proposals) == 1
    assert len(results) == 1
    assert results[0].timed_out is False
    assert results[0].ok is True
    assert results[0].n == 1
