"""Japanese tension detection tests for InteractionMatrix."""

from __future__ import annotations

from po_core.domain.proposal import Proposal
from po_core.tensors.interaction_tensor import InteractionMatrix


def _proposal(name: str, content: str) -> Proposal:
    return Proposal(
        proposal_id=f"test:{name}:0",
        action_type="answer",
        content=content,
        confidence=0.5,
        extra={
            "_po_core": {"author": name},
            "philosopher": name,
        },
    )


def test_japanese_opposition_generates_tension_and_interference():
    """Guarantee JA opposition keywords produce non-zero tension/interference."""
    proposals = [
        _proposal("哲学者A", "自由と個人の主観を重視する立場"),
        _proposal("哲学者B", "決定論と集団の客観を重視する立場"),
    ]

    matrix = InteractionMatrix.from_proposals(proposals)

    # PR-11 reason: without JA keyword support, tension often became 0 and
    # deliberation round2 could break early due to empty interference pairs.
    assert matrix.tension[0, 1] > 0.0

    pairs = matrix.high_interference_pairs(top_k=5)
    assert pairs
