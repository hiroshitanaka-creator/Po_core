from __future__ import annotations

import os
import time
from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers


@dataclass
class _BlockingPhil:
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


@dataclass
class _FastPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return [
            Proposal(
                proposal_id=f"{self.name}-ok",
                action_type="answer",
                content="ok",
                confidence=0.9,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_process_executor_timeout_is_authoritative(monkeypatch):
    monkeypatch.setenv("PO_PHILOSOPHER_EXECUTION_MODE", "process")

    proposals, results = run_philosophers(
        [_BlockingPhil(name="slow", sleep_s=0.6), _FastPhil(name="fast")],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=2,
        timeout_s=0.2,
    )

    assert [result.philosopher_id for result in results] == ["slow", "fast"]
    assert results[0].timed_out is True
    assert results[0].ok is False
    assert results[0].n == 0
    assert results[0].error == "Hard timeout after 0.2s"
    assert results[1].timed_out is False
    assert results[1].ok is True
    assert [proposal.proposal_id for proposal in proposals] == ["fast-ok"]

    time.sleep(0.7)
    assert [proposal.proposal_id for proposal in proposals] == ["fast-ok"]
    assert os.getenv("PO_PHILOSOPHER_EXECUTION_MODE") == "process"
