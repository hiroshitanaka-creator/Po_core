from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_run_comparative_benchmark_outputs_are_created(tmp_path: Path) -> None:
    output_dir = tmp_path / "bench"
    subprocess.run(
        [
            sys.executable,
            "scripts/paper/run_comparative_benchmark.py",
            "--repo-root",
            ".",
            "--output-dir",
            str(output_dir),
            "--created-at",
            "2026-02-22T00:00:00Z",
        ],
        check=True,
    )

    json_path = output_dir / "comparative_results.json"
    md_path = output_dir / "comparative_table.md"
    csv_path = output_dir / "comparative_table.csv"
    svg_path = output_dir / "comparative_overall.svg"

    assert json_path.exists()
    assert md_path.exists()
    assert csv_path.exists()
    assert svg_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["meta"]["benchmark"] == "phase_23_comparative_v1"
    assert payload["meta"]["deterministic"] is True
    assert payload["meta"]["created_at"] == "2026-02-22T00:00:00Z"

    assert payload["results"][0]["system_id"] == "po_core"
    assert set(payload["meta"]["axes"]) == {
        "diversity",
        "explainability",
        "safety",
        "emergence",
    }

    assert "| System | Diversity | Explainability | Safety | Emergence | Overall |" in md_path.read_text(
        encoding="utf-8"
    )
    assert "<svg" in svg_path.read_text(encoding="utf-8")


def test_run_comparative_benchmark_is_deterministic(tmp_path: Path) -> None:
    run1 = tmp_path / "run1"
    run2 = tmp_path / "run2"
    command = [
        sys.executable,
        "scripts/paper/run_comparative_benchmark.py",
        "--repo-root",
        ".",
        "--created-at",
        "2026-02-22T00:00:00Z",
    ]

    subprocess.run([*command, "--output-dir", str(run1)], check=True)
    subprocess.run([*command, "--output-dir", str(run2)], check=True)

    assert (run1 / "comparative_results.json").read_text(encoding="utf-8") == (
        run2 / "comparative_results.json"
    ).read_text(encoding="utf-8")
