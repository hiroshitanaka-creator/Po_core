from __future__ import annotations

from dataclasses import dataclass

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers


@dataclass
class _MultiProposalPhil:
    name: str
    prefix: str

    def propose(self, ctx, intent, tensors, memory):
        return [
            Proposal(
                proposal_id=f"{self.prefix}-0",
                action_type="answer",
                content="first",
                confidence=0.6,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            ),
            Proposal(
                proposal_id=f"{self.prefix}-1",
                action_type="answer",
                content="second",
                confidence=0.7,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            ),
        ]


def test_process_executor_preserves_input_order():
    philosophers = [
        _MultiProposalPhil(name="alpha", prefix="a"),
        _MultiProposalPhil(name="beta", prefix="b"),
        _MultiProposalPhil(name="gamma", prefix="c"),
    ]

    proposals, results = run_philosophers(
        philosophers,
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=3,
        timeout_s=0.5,
        limit_per_philosopher=2,
        execution_mode="process",
    )

    assert [result.philosopher_id for result in results] == ["alpha", "beta", "gamma"]
    assert [proposal.proposal_id for proposal in proposals] == [
        "a-0",
        "a-1",
        "b-0",
        "b-1",
        "c-0",
        "c-1",
    ]
    assert [proposal.extra[PO_CORE][AUTHOR] for proposal in proposals] == [
        "alpha",
        "alpha",
        "beta",
        "beta",
        "gamma",
        "gamma",
    ]
