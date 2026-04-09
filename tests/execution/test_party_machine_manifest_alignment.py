from __future__ import annotations

from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers
from po_core.philosophers.manifest import get_enabled_specs


@dataclass
class _NamedPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return [
            Proposal(
                proposal_id=f"{self.name}-p1",
                action_type="answer",
                content="ok",
                confidence=0.7,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_party_machine_results_are_aligned_with_manifest_ids() -> None:
    canonical_ids = {s.philosopher_id for s in get_enabled_specs()}

    _, results = run_philosophers(
        [_NamedPhil(name="not-in-manifest")],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=0.2,
        execution_mode="thread",
    )

    assert results
    assert all(result.philosopher_id in canonical_ids for result in results)
