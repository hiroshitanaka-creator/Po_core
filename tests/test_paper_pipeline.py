from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_generate_experiment_snapshot(tmp_path: Path) -> None:
    output = tmp_path / "results.json"
    cmd = [
        sys.executable,
        "scripts/paper/generate_experiment_snapshot.py",
        "--repo-root",
        ".",
        "--output",
        str(output),
        "--created-at",
        "2026-02-22T00:00:00Z",
    ]
    subprocess.run(cmd, check=True)

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["meta"]["deterministic"] is True
    assert payload["meta"]["created_at"] == "2026-02-22T00:00:00Z"
    assert payload["stats"]["scenario_count"] >= 1
    assert payload["stats"]["golden_count"] >= 1
    assert len(payload["stats"]["scenario_digest"]) == 64


def test_build_paper_pdf(tmp_path: Path) -> None:
    experiments = tmp_path / "results.json"
    compiled = tmp_path / "paper_compiled.md"
    pdf = tmp_path / "paper.pdf"

    subprocess.run(
        [
            sys.executable,
            "scripts/paper/generate_experiment_snapshot.py",
            "--repo-root",
            ".",
            "--output",
            str(experiments),
        ],
        check=True,
    )

    subprocess.run(
        [
            sys.executable,
            "scripts/paper/build_paper_pdf.py",
            "--repo-root",
            ".",
            "--experiments",
            str(experiments),
            "--compiled",
            str(compiled),
            "--pdf",
            str(pdf),
        ],
        check=True,
    )

    assert compiled.exists()
    assert "Embedded Experiment Snapshot" in compiled.read_text(encoding="utf-8")

    data = pdf.read_bytes()
    assert data.startswith(b"%PDF-1.4")
    assert b"startxref" in data
