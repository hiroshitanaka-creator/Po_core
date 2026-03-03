#!/usr/bin/env python3
"""Machine-check v1.0.0 release readiness.

Checks:
1) Pytest gates relevant to acceptance / redteam / golden+schema / traceability.
2) `make paper-build` succeeds and `docs/paper/po_core_paper.pdf` exists.
3) `CHANGELOG.md` contains a `[1.0.0]` entry.
4) `docs/spec/` has v1.0 update markers based on explicit detection rules.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def _run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _tail(text: str, limit: int = 2000) -> str:
    content = text.strip()
    return content[-limit:] if content else "(no output)"


def check_pytest_gates() -> CheckResult:
    commands = [
        (
            "acceptance",
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/acceptance/",
                "-m",
                "acceptance",
                "-q",
            ],
        ),
        (
            "redteam",
            [sys.executable, "-m", "pytest", "tests/redteam/", "-m", "redteam", "-q"],
        ),
        (
            "golden+schema",
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_golden_e2e.py",
                "tests/test_golden_regression.py",
                "tests/test_input_schema.py",
                "tests/test_output_schema.py",
                "-q",
            ],
        ),
        (
            "traceability",
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_traceability.py",
                "tests/test_traceability_config_lock.py",
                "-q",
            ],
        ),
    ]

    failures: list[str] = []
    for label, command in commands:
        completed = _run(command)
        if completed.returncode != 0:
            output = _tail(f"{completed.stdout}\n{completed.stderr}")
            failures.append(f"{label}: command failed ({' '.join(command)})\n{output}")

    if failures:
        return CheckResult(
            name="pytest release gates",
            ok=False,
            detail="\n\n".join(failures),
        )

    return CheckResult(
        name="pytest release gates",
        ok=True,
        detail="acceptance/redteam/golden+schema/traceability passed",
    )


def check_paper_build() -> CheckResult:
    command = ["make", "paper-build"]
    completed = _run(command)
    pdf_path = ROOT / "docs" / "paper" / "po_core_paper.pdf"

    if completed.returncode != 0:
        build_output = _tail(completed.stdout + "\n" + completed.stderr)
        return CheckResult(
            name="paper build",
            ok=False,
            detail=(
                "make paper-build failed\n"
                f"command: {' '.join(command)}\n"
                f"{build_output}"
            ),
        )

    if not pdf_path.exists():
        return CheckResult(
            name="paper build",
            ok=False,
            detail=f"paper build succeeded but PDF missing: {pdf_path.relative_to(ROOT)}",
        )

    return CheckResult(
        name="paper build",
        ok=True,
        detail=f"generated {pdf_path.relative_to(ROOT)}",
    )


def check_changelog_v1() -> CheckResult:
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return CheckResult(
            name="CHANGELOG [1.0.0]",
            ok=False,
            detail="CHANGELOG.md not found",
        )

    content = changelog.read_text(encoding="utf-8")
    if "## [1.0.0]" in content or "[1.0.0] -" in content:
        return CheckResult(
            name="CHANGELOG [1.0.0]",
            ok=True,
            detail="found [1.0.0] entry",
        )

    return CheckResult(
        name="CHANGELOG [1.0.0]",
        ok=False,
        detail="missing [1.0.0] entry",
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_spec_v1_markers() -> CheckResult:
    spec_root = ROOT / "docs" / "spec"
    input_schema_path = spec_root / "input_schema_v1.json"
    output_schema_path = spec_root / "output_schema_v1.json"
    prd_path = spec_root / "prd.md"

    missing_files = [
        str(path.relative_to(ROOT))
        for path in (input_schema_path, output_schema_path, prd_path)
        if not path.exists()
    ]
    if missing_files:
        return CheckResult(
            name="docs/spec v1.0 markers",
            ok=False,
            detail=f"missing files: {', '.join(missing_files)}",
        )

    input_schema = _load_json(input_schema_path)
    output_schema = _load_json(output_schema_path)
    prd_text = prd_path.read_text(encoding="utf-8")

    input_title = str(input_schema.get("title", ""))
    input_meta_const = (
        input_schema.get("properties", {})
        .get("meta", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("const")
    )

    output_title = str(output_schema.get("title", ""))
    output_meta_const = (
        output_schema.get("properties", {})
        .get("meta", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("const")
    )

    failures: list[str] = []
    if "v1" not in input_title.lower() or str(input_meta_const) != "1.0":
        failures.append(
            "input schema marker failed "
            f"(title={input_title!r}, meta.schema_version.const={input_meta_const!r})"
        )
    if "v1" not in output_title.lower() or str(output_meta_const) != "1.0":
        failures.append(
            "output schema marker failed "
            f"(title={output_title!r}, meta.schema_version.const={output_meta_const!r})"
        )
    if "v1.0" not in prd_text.lower():
        failures.append("prd marker failed (docs/spec/prd.md does not mention v1.0)")

    if failures:
        return CheckResult(
            name="docs/spec v1.0 markers",
            ok=False,
            detail="; ".join(failures),
        )

    return CheckResult(
        name="docs/spec v1.0 markers",
        ok=True,
        detail="input/output schema + PRD markers indicate v1.0 updates",
    )


def main() -> int:
    checks = [
        check_pytest_gates(),
        check_paper_build(),
        check_changelog_v1(),
        check_spec_v1_markers(),
    ]

    failed = False
    for result in checks:
        prefix = "PASS" if result.ok else "FAIL"
        stream = sys.stdout if result.ok else sys.stderr
        print(f"[{prefix}] {result.name}: {result.detail}", file=stream)
        if not result.ok:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
