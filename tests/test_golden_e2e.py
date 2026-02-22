"""
tests/test_golden_e2e.py
========================

Golden diff E2E tests — M1 success criterion.

Contract (ADR-0002):
    run_case_file(yaml_path, seed=0, now=FIXED_NOW, deterministic=True)
    must produce JSON that is **exactly equal** to the corresponding
    ``scenarios/*_expected.json`` file.

Why this matters:
    - Proves the pipeline produces actual output (not just schema-valid stubs)
    - Same input + same seed + same now → identical JSON (no flakes)
    - Any silent regression in output structure is caught immediately

To update goldens intentionally:
    python scripts/update_goldens.py

Requirements:
    M1-1: E2EでactualをOut す
    M1-2: input_digest が実計算値と一致する
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from po_core.runner import run_case_file

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "scenarios"

# Determinism anchor: all golden runs use this fixed timestamp
FIXED_NOW = "2026-02-22T00:00:00Z"

# ── Test discovery ────────────────────────────────────────────────────────


def _golden_pairs() -> list[tuple[Path, Path]]:
    """Collect (yaml_path, expected_path) pairs that both exist."""
    pairs = []
    for yaml_path in sorted(SCENARIOS.glob("*.yaml")):
        if "_expected" in yaml_path.name:
            continue
        expected_path = SCENARIOS / yaml_path.name.replace(".yaml", "_expected.json")
        if expected_path.exists():
            pairs.append((yaml_path, expected_path))
    return pairs


GOLDEN_PAIRS = _golden_pairs()


# ── Sanity ────────────────────────────────────────────────────────────────


def test_golden_pairs_exist() -> None:
    """At minimum case_001 and case_009 must have golden expected files."""
    names = {p[0].name for p in GOLDEN_PAIRS}
    assert "case_001.yaml" in names, "case_001_expected.json is missing"
    assert "case_009.yaml" in names, "case_009_expected.json is missing"


# ── Golden diff ───────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "yaml_path,expected_path",
    GOLDEN_PAIRS,
    ids=lambda p: p.name,
)
def test_golden_exact_match(yaml_path: Path, expected_path: Path) -> None:
    """
    Runner output must exactly equal the frozen expected JSON.

    Golden diff contract (ADR-0002):
    - Complete equality — not partial / subset matching
    - Timestamps are deterministic (injected via ``now=``)
    - ``run_id`` is derived from ``case_id`` (``deterministic=True``)
    """
    actual = run_case_file(yaml_path, seed=0, now=FIXED_NOW, deterministic=True)
    with expected_path.open("r", encoding="utf-8") as f:
        expected = json.load(f)

    assert actual == expected, _diff_hint(actual, expected, yaml_path.name)


# ── Determinism ───────────────────────────────────────────────────────────


def test_run_case_file_deterministic() -> None:
    """Running the same case twice must produce identical output."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    out1 = run_case_file(yaml_path, seed=0, now=FIXED_NOW)
    out2 = run_case_file(yaml_path, seed=0, now=FIXED_NOW)
    assert out1 == out2, "run_case_file is not deterministic"


# ── Schema ────────────────────────────────────────────────────────────────


def test_run_case_file_schema_valid() -> None:
    """run_case_file must not raise (internal schema validation passes)."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    result = run_case_file(yaml_path, seed=0, now=FIXED_NOW)
    assert isinstance(result, dict)
    assert result["meta"]["schema_version"] == "1.0"
    assert len(result["meta"]["run_id"]) > 0
    assert len(result["case_ref"]["input_digest"]) == 64


# ── Semantic contracts ────────────────────────────────────────────────────


def test_empty_values_triggers_no_recommendation() -> None:
    """case_009 (values=[]) must produce status='no_recommendation'."""
    yaml_path = SCENARIOS / "case_009.yaml"
    if not yaml_path.exists():
        pytest.skip("case_009.yaml not found")

    result = run_case_file(yaml_path, seed=0, now=FIXED_NOW)
    assert (
        result["recommendation"]["status"] == "no_recommendation"
    ), "case with empty values must not produce a recommendation"


def test_nonempty_values_triggers_recommendation() -> None:
    """case_001 (values non-empty) must produce status='recommended'."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    result = run_case_file(yaml_path, seed=0, now=FIXED_NOW)
    assert (
        result["recommendation"]["status"] == "recommended"
    ), "case with non-empty values must produce a recommendation"


def test_input_digest_is_64_hex_chars() -> None:
    """input_digest must be a 64-character hex string (SHA-256)."""
    yaml_path = SCENARIOS / "case_001.yaml"
    if not yaml_path.exists():
        pytest.skip("case_001.yaml not found")

    result = run_case_file(yaml_path, seed=0, now=FIXED_NOW)
    digest = result["case_ref"]["input_digest"]
    assert len(digest) == 64
    assert all(c in "0123456789abcdef" for c in digest)


def test_run_case_file_missing_file_raises() -> None:
    """run_case_file must raise FileNotFoundError for non-existent path."""
    with pytest.raises(FileNotFoundError):
        run_case_file("/no/such/case_999.yaml")


# ── Helpers ───────────────────────────────────────────────────────────────


def _diff_hint(actual: dict, expected: dict, name: str) -> str:
    """Build a concise diff hint for assertion failures."""
    a_str = json.dumps(actual, indent=2, ensure_ascii=False, sort_keys=True)
    e_str = json.dumps(expected, indent=2, ensure_ascii=False, sort_keys=True)
    if a_str == e_str:
        return f"{name}: dicts are equal but == failed (type mismatch?)"
    lines_a = a_str.splitlines()
    lines_e = e_str.splitlines()
    for i, (la, le) in enumerate(zip(lines_a, lines_e)):
        if la != le:
            return (
                f"{name}: first diff at line {i + 1}:\n"
                f"  actual:   {la.strip()}\n"
                f"  expected: {le.strip()}\n"
                f"  To update: python scripts/update_goldens.py"
            )
    return (
        f"{name}: line count differs "
        f"(actual {len(lines_a)} vs expected {len(lines_e)})"
    )
