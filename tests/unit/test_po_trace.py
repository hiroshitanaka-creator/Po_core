import json

from po_core.po_trace import PoTrace, filter_trace_data


def test_po_trace_persists_to_disk(trace_sink):
    trace = PoTrace("hello", sink_path=trace_sink)
    trace.record_input({"philosophers": ["aristotle"]})
    trace.add_philosopher_step("aristotle", {"summary": "analysis"}, freedom_pressure=0.25)
    trace.block_tensor("aristotle_tensor", "Manual block")
    trace.set_outputs({"result": "ok"})

    payload = trace.persist()

    assert trace_sink.exists()
    saved_lines = trace_sink.read_text().strip().splitlines()
    assert len(saved_lines) == 1
    stored = json.loads(saved_lines[0])
    assert stored == payload
    assert stored["blocked_tensors"]
    assert stored["freedom_pressure"]


def test_po_trace_filters_steps_by_philosopher(trace_sink):
    trace = PoTrace("prompt", sink_path=trace_sink)
    trace.add_philosopher_step("aristotle", {"summary": "first"}, freedom_pressure=0.2)
    trace.add_philosopher_step("nietzsche", {"summary": "second"}, freedom_pressure=0.4)
    trace.set_outputs({"result": "ok"})
    persisted = trace.persist()

    filtered = filter_trace_data(persisted, philosopher="aristotle")

    assert len(filtered["steps"]) == 1
    assert filtered["steps"][0]["philosopher"] == "aristotle"
    assert all(entry["philosopher"] == "aristotle" for entry in filtered["freedom_pressure"])


