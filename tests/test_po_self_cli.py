from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_po_self_synthesize_to_file(tmp_path: Path) -> None:
    output_path = tmp_path / "response.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "po_core.po_self",
            "synthesize",
            "--prompt",
            "What is responsibility?",
            "--mode",
            "demo",
            "--seed",
            "123",
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), **os.environ},
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert set(payload).issuperset({"prompt", "response", "confidence"})
