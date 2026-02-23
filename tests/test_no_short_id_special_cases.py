from pathlib import Path


def test_no_short_id_special_cases_for_case_001_009() -> None:
    root = Path(__file__).resolve().parents[1]
    disallowed = (
        'short_id == "case_001"',
        "short_id == 'case_001'",
        'short_id == "case_009"',
        "short_id == 'case_009'",
        'short_id in ("case_001", "case_009")',
        "short_id in ('case_001', 'case_009')",
    )

    violations: list[str] = []
    for path in (root / "src" / "pocore").rglob("*.py"):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        for pattern in disallowed:
            if pattern in text:
                violations.append(f"{rel}: contains {pattern}")

    assert violations == []
