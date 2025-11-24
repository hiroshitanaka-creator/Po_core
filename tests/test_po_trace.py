from datetime import datetime
from pathlib import Path

from click.testing import CliRunner

from po_core import po_trace


def test_file_store_roundtrip(tmp_path: Path) -> None:
    log_path = tmp_path / "trace.log"
    store = po_trace.FileTraceStore(log_path)

    event = po_trace.TraceEvent(
        event_id="abc",
        timestamp=datetime(2024, 1, 1),
        input_text="hello",
        response_text="world",
        philosophers=["Socrates"],
    )

    store.append(event)
    loaded = store.tail(limit=1)

    assert loaded[0].event_id == "abc"
    assert loaded[0].input_text == "hello"
    assert loaded[0].response_text == "world"
    assert loaded[0].philosophers == ["Socrates"]


def test_sqlite_store_filters(tmp_path: Path) -> None:
    db_path = tmp_path / "trace.db"
    store = po_trace.SQLiteTraceStore(db_path)

    store.append(
        po_trace.TraceEvent(
            event_id="1",
            timestamp=datetime(2024, 1, 1),
            input_text="prompt one",
            response_text="response one",
            philosophers=["Plato"],
        )
    )
    store.append(
        po_trace.TraceEvent(
            event_id="2",
            timestamp=datetime(2024, 1, 2),
            input_text="prompt two",
            response_text="response two",
            philosophers=["Kant"],
            refusal_reason="safety",
        )
    )

    only_kant = store.tail(philosophers=["Kant"], limit=5)
    assert len(only_kant) == 1
    assert only_kant[0].event_id == "2"

    refused = store.tail(refused_only=True, limit=5)
    assert len(refused) == 1
    assert refused[0].event_id == "2"


def test_cli_tail_filters(tmp_path: Path) -> None:
    fixture_path = Path("tests/fixtures/trace_events.jsonl").resolve()
    tmp_log = tmp_path / "fixture_copy.jsonl"
    tmp_log.write_text(fixture_path.read_text())

    runner = CliRunner()
    result = runner.invoke(
        po_trace.cli,
        [
            "--backend",
            "file",
            "--location",
            str(tmp_log),
            "--tail",
            "2",
            "--philosopher",
            "Socrates",
        ],
    )

    assert result.exit_code == 0
    assert "What is virtue?" in result.output
    assert "Virtue is a practiced habit." in result.output
