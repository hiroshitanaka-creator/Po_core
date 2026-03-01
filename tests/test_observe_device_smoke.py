from __future__ import annotations

from po_core.po_self import PoSelf


def test_poself_metadata_has_synthesis_report_key(monkeypatch) -> None:
    monkeypatch.setenv("PO_STRUCTURED_OUTPUT", "1")

    response = PoSelf(enable_trace=True).generate("Is freedom important?")

    assert "synthesis_report" in response.metadata
