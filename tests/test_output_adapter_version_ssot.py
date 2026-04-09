from __future__ import annotations

from po_core import __version__
from po_core.app.output_adapter import adapt_to_schema


def test_output_meta_pocore_version_matches_package_version() -> None:
    case = {
        "case_id": "case_version",
        "title": "version check",
        "problem": "p",
        "constraints": [],
        "values": [],
        "stakeholders": [],
        "unknowns": [],
    }
    run_result = {"status": "ok", "proposal": {"content": "x", "confidence": 0.5}}
    output = adapt_to_schema(
        case,
        run_result,
        run_id="run-version",
        digest="0" * 64,
        now="2026-02-22T00:00:00Z",
    )

    assert output["meta"]["pocore_version"] == __version__
