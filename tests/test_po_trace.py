from po_core.po_trace import PoTrace, DEFAULT_TIME


def test_po_trace_records_events(sample_prompt):
    trace = PoTrace(sample_prompt, ["aristotle", "nietzsche"])
    trace.record_event("ensemble_started", decision="begin", metadata={"philosophers": 2})
    trace.record_event("ensemble_completed", decision="done", suppressed=["omitted"])

    data = trace.to_dict()

    assert data["prompt"] == sample_prompt
    assert data["created_at"] == "2024-01-01T00:00:00Z"
    assert len(data["events"]) == 2
    assert data["events"][0]["timestamp"] == "2024-01-01T00:00:00Z"
    assert data["events"][1]["suppressed"] == ["omitted"]


def test_po_trace_serialization_round_trip(sample_prompt):
    trace = PoTrace(sample_prompt, [])
    trace.record_event("noop")

    serialized = trace.to_json()
    assert "noop" in serialized
    assert "created_at" in serialized
    assert serialized.endswith("}\n") or serialized.endswith("}")
