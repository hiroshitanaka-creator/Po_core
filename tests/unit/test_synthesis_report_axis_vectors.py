from __future__ import annotations

from po_core.domain.keys import AUTHOR, PO_CORE, POLICY
from po_core.domain.proposal import Proposal
from po_core.ensemble import _build_synthesis_report


def test_build_synthesis_report_includes_axis_vectors() -> None:
    proposals = [
        Proposal(
            proposal_id="p-1",
            action_type="answer",
            content="First",
            confidence=0.8,
            extra={
                PO_CORE: {
                    AUTHOR: "kant",
                    "axis_scores": {"safety": 0.7, "benefit": 0.6},
                    POLICY: {"decision": "allow"},
                }
            },
        ),
        Proposal(
            proposal_id="p-2",
            action_type="answer",
            content="Second",
            confidence=0.4,
            extra={PO_CORE: {AUTHOR: "nietzsche", "axis_scores": {"safety": 0.2}}},
        ),
    ]

    report = _build_synthesis_report(proposals)

    assert "axis_vectors" in report
    assert report["axis_vectors"] == [
        {
            "author": "kant",
            "proposal_id": "p-1",
            "confidence": 0.8,
            "axis_scores": {"safety": 0.7, "benefit": 0.6},
            "policy": "allow",
        },
        {
            "author": "nietzsche",
            "proposal_id": "p-2",
            "confidence": 0.4,
            "axis_scores": {"safety": 0.2},
            "policy": None,
        },
    ]
