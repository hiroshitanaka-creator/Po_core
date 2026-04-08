from po_core import __version__
from po_core.app.output_adapter import adapt_to_schema


def test_output_metadata_version_uses_package_version() -> None:
    output = adapt_to_schema(
        case={
            "case_id": "c1",
            "title": "t",
            "values": [],
            "constraints": [],
            "unknowns": [],
        },
        run_result={"proposal": {"content": "ok", "risk_tags": []}},
        run_id="r1",
        digest="d1",
        now="2026-02-22T00:00:00Z",
        seed=0,
        deterministic=True,
    )

    assert output["meta"]["pocore_version"] == __version__
    assert output["meta"]["generator"]["version"] == __version__
