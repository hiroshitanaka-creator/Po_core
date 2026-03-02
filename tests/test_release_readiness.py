from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_release_readiness.py"
SPEC = importlib.util.spec_from_file_location("check_release_readiness", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Failed to load check_release_readiness.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


check_acceptance_tests = MODULE.check_acceptance_tests
check_changelog_has_entry = MODULE.check_changelog_has_entry
check_ci_required_jobs_green = MODULE.check_ci_required_jobs_green
check_docs_spec_v1 = MODULE.check_docs_spec_v1


def _completed(
    returncode: int,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[sys.executable],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_check_acceptance_tests_passes() -> None:
    result = check_acceptance_tests(runner=lambda _cmd: _completed(0, "ok"))
    assert result.ok is True


def test_check_acceptance_tests_fails() -> None:
    result = check_acceptance_tests(runner=lambda _cmd: _completed(1, "", "boom"))
    assert result.ok is False
    assert "failed" in result.detail


def test_check_ci_required_jobs_green_required_jobs_format(tmp_path: Path) -> None:
    payload = {
        "required_jobs": {
            "lint": "success",
            "test": "success",
            "security": "success",
            "build": "success",
        }
    }
    status_file = tmp_path / "ci.json"
    status_file.write_text(json.dumps(payload), encoding="utf-8")

    result = check_ci_required_jobs_green(status_file)
    assert result.ok is True


def test_check_ci_required_jobs_green_check_runs_format(tmp_path: Path) -> None:
    payload = {
        "check_runs": [
            {"name": "lint", "conclusion": "success"},
            {"name": "test", "conclusion": "success"},
            {"name": "security", "conclusion": "failure"},
            {"name": "build", "conclusion": "success"},
        ]
    }
    status_file = tmp_path / "ci.json"
    status_file.write_text(json.dumps(payload), encoding="utf-8")

    result = check_ci_required_jobs_green(status_file)
    assert result.ok is False
    assert "non-success" in result.detail


def test_check_changelog_has_entry(tmp_path: Path) -> None:
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        """# Changelog\n\n## [Unreleased]\n\n### Added\n- New check\n\n## [0.1.0]\n""",
        encoding="utf-8",
    )

    result = check_changelog_has_entry(changelog)
    assert result.ok is True


def test_check_docs_spec_v1(tmp_path: Path) -> None:
    schema = {
        "title": "Po_core Output Schema v1",
        "properties": {
            "meta": {
                "properties": {
                    "schema_version": {
                        "const": "1.0",
                    }
                }
            }
        },
    }
    schema_path = tmp_path / "output_schema_v1.json"
    schema_path.write_text(json.dumps(schema), encoding="utf-8")

    result = check_docs_spec_v1(schema_path)
    assert result.ok is True
