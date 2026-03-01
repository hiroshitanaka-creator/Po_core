from __future__ import annotations

import os

from po_core.po_self import PoSelf


def test_synthesis_report_invariants() -> None:
    old = os.environ.get("PO_STRUCTURED_OUTPUT")
    os.environ["PO_STRUCTURED_OUTPUT"] = "1"
    try:
        response = PoSelf(enable_trace=False).generate(
            "What should we prioritize first?"
        )
    finally:
        if old is None:
            os.environ.pop("PO_STRUCTURED_OUTPUT", None)
        else:
            os.environ["PO_STRUCTURED_OUTPUT"] = old

    report = response.metadata.get("synthesis_report")
    assert isinstance(report, dict)

    axis_scoreboard = report.get("axis_scoreboard")
    assert isinstance(axis_scoreboard, dict)

    open_questions = report.get("open_questions")
    assert isinstance(open_questions, list)
    assert all(isinstance(q, str) and q.strip() for q in open_questions)

    stance_distribution = report.get("stance_distribution")
    assert isinstance(stance_distribution, dict)
    total = sum(float(v) for v in stance_distribution.values())
    if total > 0:
        normalized = sum(float(v) / total for v in stance_distribution.values())
        assert abs(normalized - 1.0) < 1e-9
