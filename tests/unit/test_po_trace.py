from pathlib import Path

from po_core.po_trace import PoTrace


def test_trace_record_and_list(tmp_path: Path):
    path = tmp_path / "traces.jsonl"
    tracer = PoTrace(path=path)

    result = tracer.record(prompt="hello", context={"a": 1}, result={"metadata": {"philosophers": ["One"]}})
    assert result.prompt == "hello"

    traces = tracer.list_traces()
    assert len(traces) == 1
    assert traces[0].prompt == "hello"
    assert traces[0].metadata["philosophers"] == ["One"]


def test_trace_get_invalid_index(tmp_path: Path):
    tracer = PoTrace(path=tmp_path / "traces.jsonl")
    assert tracer.get(0) is None
