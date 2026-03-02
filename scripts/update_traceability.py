from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CONFIG_FILES = (
    "02_architecture/philosophy/pareto_table.yaml",
    "02_architecture/philosophy/battalion_table.yaml",
)
DEFAULT_LOCK_FILE = "docs/traceability/config_versions.lock.yaml"


@dataclass(frozen=True)
class ConfigFingerprint:
    path: str
    config_version: str
    sha256: str

    def to_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "config_version": self.config_version,
            "sha256": self.sha256,
        }


def _load_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    try:
        payload: Any = json.loads(text)
    except json.JSONDecodeError:
        payload = yaml.safe_load(text)

    if not isinstance(payload, dict):
        raise ValueError(f"Config must be mapping: {path}")
    if "version" not in payload:
        raise ValueError(f"Missing 'version' in config: {path}")
    return str(payload["version"])


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_fingerprints(repo_root: Path) -> list[ConfigFingerprint]:
    rows: list[ConfigFingerprint] = []
    for rel_path in CONFIG_FILES:
        full_path = repo_root / rel_path
        rows.append(
            ConfigFingerprint(
                path=rel_path,
                config_version=_load_version(full_path),
                sha256=_sha256(full_path),
            )
        )
    return rows


def _render_yaml(rows: list[ConfigFingerprint]) -> str:
    payload = {
        "version": 1,
        "tracked_configs": [row.to_dict() for row in rows],
    }
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def write_lock(lock_file: Path, rows: list[ConfigFingerprint]) -> None:
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    lock_file.write_text(_render_yaml(rows), encoding="utf-8")


def check_lock(lock_file: Path, rows: list[ConfigFingerprint]) -> bool:
    expected = _render_yaml(rows)
    if not lock_file.exists():
        print(f"Traceability lock file missing: {lock_file}")
        return False

    current = lock_file.read_text(encoding="utf-8")
    if current != expected:
        print("Traceability lock file is stale.")
        print("Run: python scripts/update_traceability.py")
        return False

    print("Traceability lock file is up to date.")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update/check config_version traceability lock file."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root path",
    )
    parser.add_argument(
        "--lock-file",
        type=Path,
        default=Path(DEFAULT_LOCK_FILE),
        help="Lock file path (relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate lock file only (non-zero exit if stale)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    lock_file = args.lock_file
    if not lock_file.is_absolute():
        lock_file = repo_root / lock_file

    rows = collect_fingerprints(repo_root)
    if args.check:
        return 0 if check_lock(lock_file, rows) else 1

    write_lock(lock_file, rows)
    print(f"Updated traceability lock file: {lock_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
