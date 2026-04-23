from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from pocore.runner import run_session_replay

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "session_replay.py"
CASE_PATH = ROOT / "scenarios" / "case_002.yaml"


def _run_replay(tmp_path: Path, out_name: str) -> dict:
    answers = {
        "patch": [
            {"op": "replace", "path": "/unknowns", "value": ["評価データはHR確認済み"]},
            {
                "op": "add",
                "path": "/extensions",
                "value": {"session_replay": "unit-test"},
            },
        ]
    }
    answers_path = tmp_path / f"answers_{out_name}.json"
    answers_path.write_text(
        json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    out_dir = tmp_path / out_name
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--case",
        str(CASE_PATH),
        "--answers",
        str(answers_path),
        "--now",
        "2026-02-22T00:00:00Z",
        "--seed",
        "0",
        "--out-dir",
        str(out_dir),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)

    output_path = out_dir / "replay_output.json"
    decision_record_path = out_dir / "decision_record.md"
    assert output_path.exists()
    assert decision_record_path.exists()

    return json.loads(output_path.read_text(encoding="utf-8"))


def test_session_replay_is_deterministic(tmp_path: Path) -> None:
    first = _run_replay(tmp_path, "run1")
    second = _run_replay(tmp_path, "run2")

    assert first == second


def _write_case_and_answers(
    tmp_path: Path, *, patch_ops: list[dict[str, object]]
) -> tuple[Path, Path]:
    case = {
        "case_id": "case_replay_001",
        "title": "session replay invalid patch",
        "problem": "test",
        "constraints": [],
        "values": ["stability"],
    }
    answers = {"case_ref": "case_replay_001", "patch": patch_ops}
    answers.update(
        {
            "version": "1.0",
            "answers": [
                {
                    "question_id": "q1",
                    "answer_text": "stub",
                    "applied_patch_paths": [str(patch_ops[0]["path"])],
                }
            ],
        }
    )

    case_path = tmp_path / "case.yaml"
    answers_path = tmp_path / "answers.yaml"
    case_path.write_text(yaml.safe_dump(case, allow_unicode=True), encoding="utf-8")
    answers_path.write_text(
        yaml.safe_dump(answers, allow_unicode=True), encoding="utf-8"
    )
    return case_path, answers_path


def test_run_session_replay_rejects_unknown_patch_operation(tmp_path: Path) -> None:
    case_path, answers_path = _write_case_and_answers(
        tmp_path,
        patch_ops=[{"op": "copy", "path": "/values/0", "value": "x"}],
    )

    with pytest.raises(ValueError, match="Unsupported patch operation"):
        run_session_replay(case_path, answers_path)


def test_run_session_replay_rejects_out_of_range_list_index(tmp_path: Path) -> None:
    case_path, answers_path = _write_case_and_answers(
        tmp_path,
        patch_ops=[{"op": "replace", "path": "/values/9", "value": "x"}],
    )

    with pytest.raises(ValueError, match="List replace index out of range"):
        run_session_replay(case_path, answers_path)
