from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

DEFAULT_TIMESTAMP = "2026-02-22T00:00:00Z"
DEFAULT_SEED = 0


def _scenario_digest(paths: list[Path]) -> str:
    hasher = hashlib.sha256()
    for path in sorted(paths):
        hasher.update(path.name.encode("utf-8"))
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def _payload_digest(payload: dict) -> str:
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(normalized).hexdigest()


def build_snapshot(repo_root: Path, created_at: str, seed: int) -> dict:
    scenarios_dir = repo_root / "scenarios"
    scenario_files = sorted(scenarios_dir.glob("case_*.yaml"))
    expected_files = sorted(scenarios_dir.glob("case_*_expected.json"))

    payload = {
        "meta": {
            "pipeline": "paper_experiments_v1",
            "created_at": created_at,
            "deterministic": True,
            "seed": seed,
        },
        "stats": {
            "scenario_count": len(scenario_files),
            "golden_count": len(expected_files),
            "scenario_digest": _scenario_digest(scenario_files),
        },
    }
    payload["stats"]["snapshot_digest"] = _payload_digest(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate deterministic experiment snapshot"
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="docs/paper/experiments/results_latest.json"
    )
    parser.add_argument("--created-at", default=DEFAULT_TIMESTAMP)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output = (repo_root / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = build_snapshot(
        repo_root=repo_root, created_at=args.created_at, seed=args.seed
    )
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
