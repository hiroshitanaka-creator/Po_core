from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

module_path = Path(__file__).resolve().parents[2] / "scripts" / "check_pr_governance.py"
spec = spec_from_file_location("check_pr_governance", module_path)
assert spec and spec.loader
module = module_from_spec(spec)
spec.loader.exec_module(module)

extract_section = module.extract_section
has_checked_box = module.has_checked_box
is_placeholder = module.is_placeholder
requires_status_update = module.requires_status_update


def test_has_checked_box_detects_checked_variants() -> None:
    body = """
- [x] SSOT `docs/厳格固定ルール.md` を読んだ
- [X] 実行したテストコマンドと結果を下記に記載した
- [ ] 影響範囲とロールバック手順を下記に記載した
"""
    assert has_checked_box(body, "SSOT `docs/厳格固定ルール.md` を読んだ")
    assert has_checked_box(body, "実行したテストコマンドと結果を下記に記載した")
    assert not has_checked_box(body, "影響範囲とロールバック手順を下記に記載した")


def test_is_placeholder_detects_template_values() -> None:
    assert is_placeholder("")
    assert is_placeholder("-")
    assert is_placeholder("TBD")
    assert is_placeholder("n/a")
    assert is_placeholder("未記入")
    assert not is_placeholder("更新済み")


def test_requires_status_update_for_substantive_change() -> None:
    changed_files = ["src/pocore/runner.py", "CHANGELOG.md"]
    assert requires_status_update(changed_files)


def test_requires_status_update_relaxed_for_docs_or_template_only() -> None:
    changed_files = [
        ".github/pull_request_template.md",
        "CHANGELOG.md",
        "docs/status.md",
    ]
    assert not requires_status_update(changed_files)


def test_extract_section_returns_expected_block() -> None:
    body = """
## Status Update
- 更新箇所（Completed / Meta / Next など）: Meta
- 更新内容: governance workflow added

## Test Report
実行ログ（コマンドと結果）:
- pytest -q
"""
    section = extract_section(body, "Status Update")
    assert "更新箇所" in section
    assert "governance workflow added" in section
    assert "## Test Report" not in section
