from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCK_FILE = ROOT / "docs/traceability/config_versions.lock.yaml"


def test_update_traceability_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/update_traceability.py", "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_traceability_lock_tracks_config_versions() -> None:
    payload = yaml.safe_load(LOCK_FILE.read_text(encoding="utf-8"))
    tracked = payload.get("tracked_configs", [])
    tracked_paths = {row["path"] for row in tracked}

    assert "02_architecture/philosophy/pareto_table.yaml" in tracked_paths
    assert "02_architecture/philosophy/battalion_table.yaml" in tracked_paths
    for row in tracked:
        assert str(row.get("config_version", ""))
        assert len(str(row.get("sha256", ""))) == 64
