from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py<3.11
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DEV_FILE = ROOT / "tools" / "dev-requirements.txt"
PYPROJECT_FILE = ROOT / "pyproject.toml"


def _canonical_dev_dependencies() -> list[str]:
    lines = CANONICAL_DEV_FILE.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]


def main() -> None:
    canonical = _canonical_dev_dependencies()
    pyproject = tomllib.loads(PYPROJECT_FILE.read_text(encoding="utf-8"))
    optional_dev = pyproject["project"]["optional-dependencies"]["dev"]
    dependency_group_dev = pyproject["dependency-groups"]["dev"]

    mismatches: list[str] = []
    if optional_dev != canonical:
        mismatches.append(
            "project.optional-dependencies.dev does not match tools/dev-requirements.txt"
        )
    if dependency_group_dev != canonical:
        mismatches.append(
            "dependency-groups.dev does not match tools/dev-requirements.txt"
        )

    if mismatches:
        joined = "\n - ".join(["dev dependency drift detected", *mismatches])
        raise SystemExit(joined)
    print("dev dependency metadata matches tools/dev-requirements.txt")


if __name__ == "__main__":
    main()
