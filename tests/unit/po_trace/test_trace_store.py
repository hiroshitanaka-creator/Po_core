from pathlib import Path

from po_core.po_trace.models import TraceSession
from po_core.utils.trace_store import TraceStore


def _fake_session(tmp_path: Path) -> TraceSession:
    return TraceSession(
        session_id="demo",
        prompt="test",
        spoken_summary="demo text",
        created_at="2024-01-01T00:00:00Z",
        completed_at="2024-01-01T00:00:01Z",
        entries=[],
    )


def test_trace_store_append_and_load(tmp_path: Path) -> None:
    store = TraceStore(base_path=tmp_path, max_bytes=10_000)
    session = _fake_session(tmp_path)

    store.append(session)

    loaded = store.load_all()

    assert len(loaded) == 1
    assert loaded[0].prompt == "test"
