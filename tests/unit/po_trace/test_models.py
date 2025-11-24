from pathlib import Path

from po_core.po_trace.models import TraceSession


def test_trace_session_roundtrip() -> None:
    fixture_path = Path("tests/fixtures/sample_trace.json")
    payload = fixture_path.read_text(encoding="utf-8")

    session = TraceSession.model_validate_json(payload)

    assert session.prompt == "What is freedom?"
    assert len(session.entries) == 1
    assert session.entries[0].tensors[0].shape == [3]

    serialized = session.model_dump_json()
    restored = TraceSession.model_validate_json(serialized)

    assert restored.summary_rows()[0][0] == "1"


def test_trace_session_summary_rows_display_strings() -> None:
    fixture_path = Path("tests/fixtures/sample_trace.json")
    payload = fixture_path.read_text(encoding="utf-8")
    session = TraceSession.model_validate_json(payload)

    step, freedom, semantic, spoken = session.summary_rows()[0]

    assert step == "1"
    assert freedom.startswith("0.")
    assert semantic.startswith("0.")
    assert "freedom" in spoken
