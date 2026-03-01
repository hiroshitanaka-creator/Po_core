from __future__ import annotations

from po_core.po_self import PoSelf


def test_synthesis_report_scoreboard_has_axis_samples(monkeypatch) -> None:
    monkeypatch.setenv("PO_STRUCTURED_OUTPUT", "1")

    response = PoSelf(enable_trace=True).generate(
        "Please propose a practical plan with explicit steps and budget."
    )

    report = response.metadata.get("synthesis_report")
    assert isinstance(report, dict)

    scoreboard = report.get("scoreboard")
    assert isinstance(scoreboard, dict)

    for axis in ("safety", "benefit", "feasibility"):
        assert axis in scoreboard
        assert int(scoreboard[axis]["samples"]) >= 1
