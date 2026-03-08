#!/usr/bin/env python3
"""Lightweight PR governance checks for pull_request events."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

REQUIRED_HEADINGS = [
    "必須チェック（SSOT / 進捗 / テスト報告）",
    "Status Update",
    "Test Report",
    "Impact / Rollback",
]

REQUIRED_CHECKBOXES = {
    "SSOT acknowledgment": "SSOT `docs/厳格固定ルール.md` を読んだ",
    "docs/status.md update": "`docs/status.md` を更新した（どこを動かしたかを記載）",
    "test report": "実行したテストコマンドと結果を下記に記載した",
    "impact/rollback": "影響範囲とロールバック手順を下記に記載した",
}

# Matches requirement IDs like REQ-ARB-001, NFR-GOV-001, FR-ETH-002
REQ_ID_PATTERN = re.compile(r"\b(?:REQ|NFR|FR)-[A-Z0-9]+-\d{3}\b")

SUBSTANTIVE_PREFIXES = (
    "src/",
    "tests/",
    "scripts/",
    "scenarios/",
    ".github/workflows/",
    "docs/spec/",
)
SUBSTANTIVE_FILES = {"pyproject.toml"}

# Explicit exemptions for docs/governance-only PRs where status updates may be relaxed.
STATUS_UPDATE_EXEMPT_FILES = {
    ".github/pull_request_template.md",
    "CHANGELOG.md",
    "docs/status.md",
}

PLACEHOLDER_VALUES = {"", "-", "tbd", "n/a", "未記入"}


def extract_section(body: str, heading: str) -> str:
    pattern = rf"(?ms)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, body)
    return match.group(1).strip() if match else ""


def is_placeholder(text: str) -> bool:
    normalized = text.strip()
    if normalized.lower() in PLACEHOLDER_VALUES:
        return True
    return normalized == ""


def has_checked_box(body: str, label_fragment: str) -> bool:
    pattern = rf"(?im)^-\s*\[[xX]\]\s*.*{re.escape(label_fragment)}"
    return re.search(pattern, body) is not None


def requires_status_update(changed_files: list[str]) -> bool:
    if not changed_files:
        return False

    def _is_exempt(path: str) -> bool:
        return path in STATUS_UPDATE_EXEMPT_FILES or path.startswith("docs/")

    if all(_is_exempt(path) for path in changed_files):
        return False

    return any(
        path.startswith(SUBSTANTIVE_PREFIXES)
        or path in SUBSTANTIVE_FILES
        or re.match(r"^requirements[^/]*\.txt$", path)
        for path in changed_files
    )


def _extract_field(section: str, field_name: str) -> str:
    for line in section.splitlines():
        if field_name in line:
            _, _, value = line.partition(":")
            return value.strip()
    return ""


def _has_non_placeholder_line(text: str) -> bool:
    for line in text.splitlines():
        candidate = line.strip()
        if candidate.startswith("- ["):
            continue
        if not is_placeholder(candidate):
            return True
    return False


def validate_body(body: str, changed_files: list[str]) -> list[str]:
    failures: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if f"## {heading}" not in body:
            failures.append(f"Missing section heading: {heading}")

    for label, fragment in REQUIRED_CHECKBOXES.items():
        if not has_checked_box(body, fragment):
            failures.append(f"Missing checked box: {label}")

    status_section = extract_section(body, "Status Update")
    if not status_section:
        failures.append("Missing section content: Status Update")
    else:
        updated_area = _extract_field(status_section, "更新箇所")
        updated_content = _extract_field(status_section, "更新内容")
        if is_placeholder(updated_area):
            failures.append("Missing section content: Status Update / 更新箇所")
        if is_placeholder(updated_content):
            failures.append("Missing section content: Status Update / 更新内容")

    test_section = extract_section(body, "Test Report")
    if not test_section:
        failures.append("Missing section content: Test Report")
    else:
        marker = "実行ログ（コマンドと結果）:"
        log_text = test_section.split(marker, 1)[1] if marker in test_section else ""
        if not _has_non_placeholder_line(log_text):
            failures.append("Missing section content: Test Report / 実行ログ（コマンドと結果）")

    impact_section = extract_section(body, "Impact / Rollback")
    if not impact_section:
        failures.append("Missing section content: Impact / Rollback")
    else:
        impact_scope = _extract_field(impact_section, "影響範囲")
        rollback = _extract_field(impact_section, "ロールバック手順")
        if is_placeholder(impact_scope):
            failures.append("Missing section content: Impact / Rollback / 影響範囲")
        if is_placeholder(rollback):
            failures.append("Missing section content: Impact / Rollback / ロールバック手順")

    if requires_status_update(changed_files) and "docs/status.md" not in changed_files:
        failures.append("docs/status.md must be updated for code-affecting changes")

    # M4ゲート: 実質的な変更PRは要件IDを少なくとも1つ参照すること
    if requires_status_update(changed_files) and not REQ_ID_PATTERN.search(body):
        failures.append(
            "Substantive PRs must reference at least one requirement ID "
            "(e.g. REQ-xxx-001, NFR-GOV-001, FR-ETH-001) — M4 gate"
        )

    return failures


def _changed_files(base_sha: str, head_sha: str) -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}..{head_sha}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _load_event(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH is not set; skipping PR governance check.")
        return 0

    event_file = Path(event_path)
    if not event_file.exists():
        print(f"Event payload not found: {event_file}; skipping.")
        return 0

    payload = _load_event(event_file)
    pull_request = payload.get("pull_request")
    if not isinstance(pull_request, dict):
        print("No pull_request payload; skipping PR governance check.")
        return 0

    body = str(pull_request.get("body") or "")
    base_sha = str((pull_request.get("base") or {}).get("sha") or "")
    head_sha = str((pull_request.get("head") or {}).get("sha") or "")
    changed_files = _changed_files(base_sha, head_sha) if base_sha and head_sha else []

    failures = validate_body(body=body, changed_files=changed_files)
    if failures:
        print("PR governance check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PR governance check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
