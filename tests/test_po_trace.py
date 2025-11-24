from pathlib import Path

from click.testing import CliRunner

from po_core.po_trace import ReasonLog, cli as trace_cli


FIXTURE = Path(__file__).parent / "fixtures" / "reason_log_sample.json"


def test_reason_log_matches_spec_fields() -> None:
    data = ReasonLog.load(FIXTURE)
    spec_keys = {
        "id",
        "version",
        "created_at",
        "actor",
        "prompt",
        "conclusion",
        "rationale",
        "influences",
        "evidence",
        "confidence",
        "tags",
        "metadata",
    }
    assert set(data.to_dict().keys()) == spec_keys
    assert data.created_at.isoformat() == "2024-01-01T00:00:00"
    assert data.tags == sorted(data.tags)


def test_reason_log_markdown_roundtrip(tmp_path: Path) -> None:
    log = ReasonLog.new(
        prompt="Test prompt",
        conclusion="Test conclusion",
        rationale="Because tests demand it.",
        actor="tester",
        tags=["demo"],
        evidence=["unit"],
        influences=["spec"],
        confidence=0.9,
    )
    markdown_path = tmp_path / "log.md"
    log.save(markdown_path, fmt="markdown")
    assert markdown_path.exists()
    assert "## Prompt" in markdown_path.read_text(encoding="utf-8")


def test_po_trace_cli_create_and_load(tmp_path: Path) -> None:
    runner = CliRunner()
    output_path = tmp_path / "log.json"
    result_create = runner.invoke(
        trace_cli,
        [
            "log",
            "--prompt",
            "CLI prompt",
            "--conclusion",
            "Answer",
            "--rationale",
            "Reasoning",
            "--tag",
            "cli",
            "--save",
            str(output_path),
        ],
    )
    assert result_create.exit_code == 0
    assert output_path.exists()

    result_load = runner.invoke(trace_cli, ["log", "--load", str(output_path)])
    assert result_load.exit_code == 0
    assert "Reason Log" in result_load.output
