"""
tests/test_golden_e2e.py
========================

Golden diff E2E tests.

Contract (ADR-0002):
    run_case_file(yaml_path, seed=meta.seed, now=meta.created_at, deterministic=True)
    must produce JSON exactly equal (after canonicalization) to *_expected.json.

Canonicalization:
    Lists with known ordering semantics are sorted before comparison so that
    engine output-order changes don't cause spurious failures:
      - options         → sorted by option_id
      - questions       → sorted by (priority, question_id)
      - stakeholders    → sorted by (name, role)
      - trace.steps     → sorted by PIPELINE_ORDER enum
      - principles      → sorted alphabetically
    Scalar fields and other lists are compared as-is.

To regenerate goldens intentionally:
    python scripts/update_goldens.py
"""

from __future__ import annotations

import datetime as _dt
import difflib
import importlib
import json
from pathlib import Path
from typing import Any, Callable, Dict, List

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "scenarios"

PIPELINE_ORDER = [
    "parse_input",
    "generate_options",
    "ethics_review",
    "responsibility_review",
    "question_layer",
    "compose_output",
]

# ---------------------------------------------------------------------------
# Dynamic runner import
# ---------------------------------------------------------------------------


def _import_run_case_file() -> Callable:
    """Try pocore.runner → pocore.orchestrator → pocore in order."""
    candidates = [
        ("pocore.runner", "run_case_file"),
        ("pocore.orchestrator", "run_case_file"),
        ("pocore", "run_case_file"),
    ]
    for mod_name, fn_name in candidates:
        try:
            mod = importlib.import_module(mod_name)
            fn = getattr(mod, fn_name, None)
            if fn is not None and callable(fn):
                return fn
        except ImportError:
            continue
    raise ImportError(
        "Could not import run_case_file from any of: "
        + ", ".join(m for m, _ in candidates)
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def run_case_file_fn() -> Callable:
    return _import_run_case_file()


# ---------------------------------------------------------------------------
# Golden file discovery
# ---------------------------------------------------------------------------

EXPECTED_FILES: List[Path] = sorted(SCENARIOS.glob("*_expected.json"))


# ---------------------------------------------------------------------------
# Canonicalization
# ---------------------------------------------------------------------------


def _sort_key_step(step: Dict) -> int:
    try:
        return PIPELINE_ORDER.index(step.get("name", ""))
    except ValueError:
        return 999


def _canonicalize(obj: Any, *, parent_key: str = "") -> Any:  # noqa: C901
    """Recursively sort lists with known ordering semantics."""
    if isinstance(obj, dict):
        canon = {k: _canonicalize(v, parent_key=k) for k, v in obj.items()}
        # Sort lists that have stable sort keys
        if parent_key == "options" and isinstance(canon.get("options"), list):
            # handled below at list level
            pass
        return canon
    if isinstance(obj, list):
        items = [_canonicalize(i, parent_key=parent_key) for i in obj]
        if parent_key == "options":
            return sorted(items, key=lambda x: x.get("option_id", ""))
        if parent_key == "questions":
            return sorted(
                items,
                key=lambda x: (x.get("priority", 0), x.get("question_id", "")),
            )
        if parent_key == "stakeholders":
            return sorted(
                items,
                key=lambda x: (x.get("name", ""), x.get("role", "")),
            )
        if parent_key == "steps":
            return sorted(items, key=_sort_key_step)
        if parent_key in (
            "principles_used",
            "principles_applied",
            "guardrails",
            "concerns",
            "known_unknowns",
            "assumptions",
            "reasons",
        ):
            return sorted(items)
        return items
    return obj


# ---------------------------------------------------------------------------
# Path-level diff helpers
# ---------------------------------------------------------------------------


def _collect_path_diffs(
    actual: Any,
    expected: Any,
    path: str = "",
    diffs: List[str] | None = None,
    max_diffs: int = 20,
) -> List[str]:
    if diffs is None:
        diffs = []
    if len(diffs) >= max_diffs:
        return diffs

    if isinstance(expected, dict) and isinstance(actual, dict):
        for k in set(list(expected.keys()) + list(actual.keys())):
            sub = f"{path}.{k}" if path else k
            if k not in actual:
                diffs.append(f"MISSING key {sub!r} in actual")
            elif k not in expected:
                diffs.append(f"EXTRA key {sub!r} in actual")
            else:
                _collect_path_diffs(actual[k], expected[k], sub, diffs, max_diffs)
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(actual) != len(expected):
            diffs.append(
                f"LIST LENGTH at {path!r}: actual={len(actual)}, expected={len(expected)}"
            )
        for i, (a_item, e_item) in enumerate(zip(actual, expected)):
            _collect_path_diffs(a_item, e_item, f"{path}[{i}]", diffs, max_diffs)
    else:
        if actual != expected:
            diffs.append(
                f"VALUE at {path!r}:\n"
                f"  actual:   {actual!r}\n"
                f"  expected: {expected!r}"
            )
    return diffs


def _format_failure(actual: Dict, expected: Dict, name: str) -> str:
    a_canon = _canonicalize(actual)
    e_canon = _canonicalize(expected)

    path_diffs = _collect_path_diffs(a_canon, e_canon)
    a_str = json.dumps(a_canon, indent=2, ensure_ascii=False, sort_keys=True)
    e_str = json.dumps(e_canon, indent=2, ensure_ascii=False, sort_keys=True)
    udiff = list(
        difflib.unified_diff(
            e_str.splitlines(keepends=True),
            a_str.splitlines(keepends=True),
            fromfile=f"expected/{name}",
            tofile=f"actual/{name}",
            n=3,
        )
    )

    parts = [f"\n{'='*60}", f"GOLDEN MISMATCH: {name}", f"{'='*60}"]
    if path_diffs:
        parts.append("\n── Path diffs (first 20) ──")
        parts.extend(path_diffs)
    if udiff:
        parts.append("\n── Unified diff (expected → actual) ──")
        parts.extend(udiff[:120])  # cap at 120 diff lines
    parts.append("\nTo update goldens: python scripts/update_goldens.py")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Sanity: at least the required goldens exist
# ---------------------------------------------------------------------------


def test_required_expected_files_exist() -> None:
    """case_001, case_009, case_010 must all have expected files."""
    names = {p.name for p in EXPECTED_FILES}
    for required in (
        "case_001_expected.json",
        "case_009_expected.json",
        "case_010_expected.json",
    ):
        assert required in names, f"{required} is missing from scenarios/"


# ---------------------------------------------------------------------------
# Golden diff — parametrized over all *_expected.json
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "expected_path",
    EXPECTED_FILES,
    ids=lambda p: p.stem,
)
def test_golden_e2e_output_matches_expected(
    expected_path: Path, run_case_file_fn: Callable
) -> None:
    """
    Runner output (after canonicalization) must exactly match the frozen
    expected JSON.  Golden diff contract: ADR-0002.
    """
    # Load expected
    with expected_path.open("r", encoding="utf-8") as f:
        expected = json.load(f)

    # Derive yaml path
    stem = expected_path.stem  # e.g. "case_001_expected"
    yaml_name = stem.replace("_expected", "") + ".yaml"
    yaml_path = SCENARIOS / yaml_name
    if not yaml_path.exists():
        pytest.skip(f"{yaml_name} not found")

    # Use meta from expected file to drive determinism
    meta = expected.get("meta", {})
    now = meta.get("created_at", "2026-02-22T00:00:00Z")
    seed = meta.get("seed", 0)

    actual = run_case_file_fn(yaml_path, seed=seed, now=now, deterministic=True)

    a_canon = _canonicalize(actual)
    e_canon = _canonicalize(expected)

    assert a_canon == e_canon, _format_failure(actual, expected, expected_path.name)


# ---------------------------------------------------------------------------
# Determinism contract
# ---------------------------------------------------------------------------


def test_run_case_file_deterministic(run_case_file_fn: Callable) -> None:
    """Running the same case twice must produce identical output."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    now = "2026-02-22T00:00:00Z"
    out1 = run_case_file_fn(yaml_path, seed=0, now=now, deterministic=True)
    out2 = run_case_file_fn(yaml_path, seed=0, now=now, deterministic=True)
    assert out1 == out2, "run_case_file is not deterministic"


# ---------------------------------------------------------------------------
# Semantic contracts
# ---------------------------------------------------------------------------


def test_empty_values_triggers_no_recommendation(run_case_file_fn: Callable) -> None:
    """case_009 (values=[]) must produce status='no_recommendation'."""
    yaml_path = SCENARIOS / "case_009.yaml"
    if not yaml_path.exists():
        pytest.skip("case_009.yaml not found")

    result = run_case_file_fn(yaml_path, seed=0, now="2026-02-22T00:00:00Z")
    assert (
        result["recommendation"]["status"] == "no_recommendation"
    ), "case with empty values must not produce a recommendation"


def test_constraint_conflict_triggers_recommendation(
    run_case_file_fn: Callable,
) -> None:
    """case_010 (conflicting time constraints) must produce status='recommended'."""
    yaml_path = SCENARIOS / "case_010.yaml"
    if not yaml_path.exists():
        pytest.skip("case_010.yaml not found")

    result = run_case_file_fn(yaml_path, seed=0, now="2026-02-22T00:00:00Z")
    assert (
        result["recommendation"]["status"] == "recommended"
    ), "constraint_conflict case must produce a recommendation (to resolve the conflict)"


def test_nonempty_values_triggers_recommendation(run_case_file_fn: Callable) -> None:
    """case_001 (values non-empty) must produce status='recommended'."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    result = run_case_file_fn(yaml_path, seed=0, now="2026-02-22T00:00:00Z")
    assert (
        result["recommendation"]["status"] == "recommended"
    ), "case with non-empty values must produce a recommendation"


# ---------------------------------------------------------------------------
# Schema / structural contracts
# ---------------------------------------------------------------------------


def test_run_case_file_schema_valid(run_case_file_fn: Callable) -> None:
    """run_case_file must not raise (internal schema validation passes)."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    result = run_case_file_fn(yaml_path, seed=0, now="2026-02-22T00:00:00Z")
    assert isinstance(result, dict)
    assert result["meta"]["schema_version"] == "1.0"
    assert len(result["meta"]["run_id"]) > 0
    assert len(result["case_ref"]["input_digest"]) == 64


def test_input_digest_is_64_hex_chars(run_case_file_fn: Callable) -> None:
    """input_digest must be a 64-character hex string (SHA-256)."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    result = run_case_file_fn(yaml_path, seed=0, now="2026-02-22T00:00:00Z")
    digest = result["case_ref"]["input_digest"]
    assert len(digest) == 64
    assert all(c in "0123456789abcdef" for c in digest)


def test_run_case_file_missing_file_raises(run_case_file_fn: Callable) -> None:
    """run_case_file must raise FileNotFoundError for non-existent path."""
    with pytest.raises(FileNotFoundError):
        run_case_file_fn("/no/such/case_999.yaml")
