from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_po_viewer_renders_ascii(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "sample_trace.log"
    trace_path = tmp_path / "trace.log"
    trace_path.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "po_core.po_viewer", "render", "--source", str(trace_path), "--format", "ascii", "--top", "5"],
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), **os.environ},
    )

    assert result.returncode == 0, result.stderr

    expected = Path(__file__).parent / "fixtures" / "expected_viewer_output.txt"
    for line in expected.read_text(encoding="utf-8").splitlines():
        assert line in result.stdout
