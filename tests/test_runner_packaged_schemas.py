from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_runner_loads_packaged_schemas_from_installed_package(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    install_dir = tmp_path / "installed-package"
    case_copy = tmp_path / "case_002.yaml"
    case_copy.write_text(
        (repo_root / "scenarios" / "case_002.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--target",
            str(install_dir),
            "--no-build-isolation",
            str(repo_root),
        ],
        check=True,
        cwd=tmp_path,
    )

    runner_script = """
from pathlib import Path
import json
from po_core import runner

result = runner.run_case_file(
    Path('case_002.yaml'),
    seed=0,
    now='2026-02-22T00:00:00Z',
    deterministic=True,
)
print(json.dumps({
    'case_id': result['case_ref']['case_id'],
    'schema_version': result['meta']['schema_version'],
    'cwd': str(Path.cwd()),
}))
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(install_dir)
    completed = subprocess.run(
        [sys.executable, "-c", runner_script],
        check=True,
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout.strip())
    assert payload["case_id"] == "case_002_headcount_reduction"
    assert payload["schema_version"] == "1.0"
    assert Path(payload["cwd"]) == tmp_path
