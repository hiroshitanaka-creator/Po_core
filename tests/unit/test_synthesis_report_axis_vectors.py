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
                    "axis_scoring_debug": {"total_hits": 3},
                }
            },
        ),
        Proposal(
            proposal_id="p-2",
            action_type="answer",
            content="Second",
            confidence=0.4,
            extra={
                PO_CORE: {
                    AUTHOR: "nietzsche",
                    "axis_scores": {"safety": 0.2},
                    "axis_scoring_debug": {"total_hits": 0},
                }
            },
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


def test_build_synthesis_report_includes_axis_scoring_diagnostics() -> None:
    proposals = [
        Proposal(
            proposal_id="p-1",
            action_type="answer",
            content="First",
            confidence=0.8,
            extra={
                PO_CORE: {
                    AUTHOR: "kant",
                    "axis_scores": {"safety": 0.7},
                    "axis_scoring_debug": {"total_hits": 2},
                }
            },
        ),
        Proposal(
            proposal_id="p-2",
            action_type="answer",
            content="Second",
            confidence=0.4,
            extra={
                PO_CORE: {
                    AUTHOR: "nietzsche",
                    "axis_scores": {"safety": 0.2},
                    "axis_scoring_debug": {"total_hits": 0},
                }
            },
        ),
    ]

    report = _build_synthesis_report(proposals)

    assert report["axis_scoring_diagnostics"] == {
        "n_vectors": 2,
        "hit_rate": 0.5,
        "mean_total_hits": 1.0,
        "warn_no_signal": False,
    }
