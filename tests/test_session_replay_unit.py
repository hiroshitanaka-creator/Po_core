from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "session_replay.py"
CASE_PATH = ROOT / "scenarios" / "case_002.yaml"


def _run_replay(tmp_path: Path, out_name: str) -> dict:
    answers = {
        "patch": [
            {"op": "replace", "path": "/unknowns", "value": ["評価データはHR確認済み"]},
            {"op": "add", "path": "/extensions", "value": {"session_replay": "unit-test"}},
        ]
    }
    answers_path = tmp_path / f"answers_{out_name}.json"
    answers_path.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")

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
