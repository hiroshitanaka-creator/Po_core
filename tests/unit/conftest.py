import json
import pytest


@pytest.fixture()
def sample_prompt() -> str:
    return "What does it mean to live authentically?"


@pytest.fixture()
def load_json_output():
    def _loader(result) -> dict:
        return json.loads(result.output.strip())

    return _loader


@pytest.fixture()
def trace_sink(tmp_path, monkeypatch):
    sink = tmp_path / "trace.ndjson"
    monkeypatch.setenv("PO_TRACE_PATH", str(sink))
    return sink
