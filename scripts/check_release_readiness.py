#!/usr/bin/env python3
"""Release readiness checker for v1.0.0.

Checks:
1) AT-001 to AT-010 acceptance tests pass.
2) Required CI jobs are green.
3) CHANGELOG has an Unreleased entry.
4) docs/spec is updated for v1.0 (minimum detection rules).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def _run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, capture_output=True, text=True)


def check_acceptance_tests(
    runner: Callable[[Sequence[str]], subprocess.CompletedProcess[str]] = _run_command,
) -> CheckResult:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "tests/acceptance/",
        "-m",
        "acceptance",
        "-q",
    ]
    completed = runner(command)
    if completed.returncode == 0:
        return CheckResult(
            name="AT-001〜AT-010 pass",
            ok=True,
            detail="acceptance suite passed",
        )

    detail = (completed.stdout + "\n" + completed.stderr).strip()
    return CheckResult(
        name="AT-001〜AT-010 pass",
        ok=False,
        detail=f"acceptance suite failed\n{detail[-1000:]}",
    )


def _extract_ci_statuses(ci_data: dict) -> dict[str, str]:
    if isinstance(ci_data.get("required_jobs"), dict):
        return {
            str(name): str(status).lower()
            for name, status in ci_data["required_jobs"].items()
        }

    statuses: dict[str, str] = {}
    check_runs = ci_data.get("check_runs")
    if isinstance(check_runs, list):
        for run in check_runs:
            name = run.get("name")
            conclusion = run.get("conclusion")
            if name and conclusion:
                statuses[str(name)] = str(conclusion).lower()
    return statuses


def check_ci_required_jobs_green(ci_status_file: Path | None) -> CheckResult:
    if ci_status_file is None:
        return CheckResult(
            name="CI required jobs green",
            ok=False,
            detail="ci status file is required (--ci-status-file)",
        )

    if not ci_status_file.exists():
        return CheckResult(
            name="CI required jobs green",
            ok=False,
            detail=f"ci status file not found: {ci_status_file}",
        )

    ci_data = json.loads(ci_status_file.read_text(encoding="utf-8"))
    statuses = _extract_ci_statuses(ci_data)
    required_jobs = ["lint", "test", "security", "build"]

    missing = [job for job in required_jobs if job not in statuses]
    failed = [job for job in required_jobs if statuses.get(job) != "success"]

    if not missing and not failed:
        return CheckResult(
            name="CI required jobs green",
            ok=True,
            detail="all required jobs are success",
        )

    parts: list[str] = []
    if missing:
        parts.append(f"missing jobs: {', '.join(missing)}")
    if failed:
        states = ", ".join(f"{job}={statuses.get(job)}" for job in failed)
        parts.append(f"non-success jobs: {states}")
    return CheckResult(name="CI required jobs green", ok=False, detail="; ".join(parts))


def check_changelog_has_entry(changelog_path: Path) -> CheckResult:
    if not changelog_path.exists():
        return CheckResult(
            name="CHANGELOG has entry",
            ok=False,
            detail=f"missing changelog: {changelog_path}",
        )

    lines = changelog_path.read_text(encoding="utf-8").splitlines()

    start = None
    end = len(lines)
    for idx, line in enumerate(lines):
        if line.strip().startswith("## [Unreleased]"):
            start = idx + 1
            continue
        if start is not None and line.startswith("## "):
            end = idx
            break

    if start is None:
        return CheckResult(
            name="CHANGELOG has entry",
            ok=False,
            detail="missing [Unreleased] section",
        )

    unreleased_lines = lines[start:end]
    has_bullet = any(line.lstrip().startswith("-") for line in unreleased_lines)
    if has_bullet:
        return CheckResult(
            name="CHANGELOG has entry",
            ok=True,
            detail="[Unreleased] section contains entries",
        )

    return CheckResult(
        name="CHANGELOG has entry",
        ok=False,
        detail="[Unreleased] section has no bullet entries",
    )


def check_docs_spec_v1(spec_path: Path) -> CheckResult:
    if not spec_path.exists():
        return CheckResult(
            name="docs/spec updated to v1.0",
            ok=False,
            detail=f"missing spec file: {spec_path}",
        )

    schema = json.loads(spec_path.read_text(encoding="utf-8"))
    title = str(schema.get("title", ""))
    schema_version_const = (
        schema.get("properties", {})
        .get("meta", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("const")
    )

    if "v1" in title.lower() and str(schema_version_const) == "1.0":
        return CheckResult(
            name="docs/spec updated to v1.0",
            ok=True,
            detail="output_schema_v1.json title/schema_version indicate v1.0",
        )

    return CheckResult(
        name="docs/spec updated to v1.0",
        ok=False,
        detail=(
            "v1.0 detection failed: "
            f"title={title!r}, meta.schema_version.const={schema_version_const!r}"
        ),
    )


def run_release_readiness(ci_status_file: Path | None) -> list[CheckResult]:
    return [
        check_acceptance_tests(),
        check_ci_required_jobs_green(ci_status_file),
        check_changelog_has_entry(ROOT / "CHANGELOG.md"),
        check_docs_spec_v1(ROOT / "docs/spec/output_schema_v1.json"),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check v1.0.0 release readiness")
    parser.add_argument(
        "--ci-status-file",
        type=Path,
        default=None,
        help="Path to CI status JSON with required_jobs or check_runs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = run_release_readiness(ci_status_file=args.ci_status_file)

    for result in results:
        prefix = "PASS" if result.ok else "FAIL"
        print(f"[{prefix}] {result.name}: {result.detail}")

    return 0 if all(item.ok for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
