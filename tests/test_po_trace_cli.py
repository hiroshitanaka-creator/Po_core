from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_po_trace_logs_events(tmp_path: Path) -> None:
    input_path = tmp_path / "events.json"
    fixture = Path(__file__).parent / "fixtures" / "sample_events.json"
    input_path.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    output_path = tmp_path / "trace.log"
    result = subprocess.run(
        [sys.executable, "-m", "po_core.po_trace", "log", "--input", str(input_path), "--output", str(output_path)],
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), **os.environ},
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()

    lines = output_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3
    for line in lines:
        payload = json.loads(line)
        assert set(payload).issuperset({"event", "timestamp", "metadata", "recorded_at"})
