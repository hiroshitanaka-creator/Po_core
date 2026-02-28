from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRACEABILITY_PATH = ROOT / "docs/traceability/traceability_v1.yaml"
REQUIREMENTS_PATH = ROOT / "docs/spec/requirements_v1.md"


def _load_traceability() -> dict[str, Any]:
    with TRACEABILITY_PATH.open("r", encoding="utf-8") as f:
        payload = yaml.safe_load(f)
    assert isinstance(payload, dict)
    return payload


def _extract_rule_ids_from_repo() -> set[str]:
    pattern = re.compile(r'"((?:ETH|RESP)_[A-Z0-9_]+)"')
    rule_ids: set[str] = set()
    for py_file in (ROOT / "src/pocore").rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        rule_ids.update(pattern.findall(text))
    return rule_ids


def _extract_arbitration_codes_from_repo() -> set[str]:
    target = ROOT / "src/pocore/engines/recommendation_v1.py"
    module = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))

    codes: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Return) or not isinstance(node.value, ast.Tuple):
            continue
        if len(node.value.elts) != 2:
            continue
        code_node = node.value.elts[1]
        if isinstance(code_node, ast.Constant) and isinstance(code_node.value, str):
            if re.fullmatch(r"[A-Z][A-Z0-9_]+", code_node.value):
                codes.add(code_node.value)
    return codes


def _traceability_code_refs(payload: dict[str, Any], kind: str) -> set[str]:
    values: set[str] = set()
    for req in payload.get("requirements", []):
        for ref in req.get("code_refs", []):
            if ref.get("kind") == kind:
                values.add(ref.get("value"))
    return values


def test_traceability_covers_all_rule_ids() -> None:
    payload = _load_traceability()
    repo_rule_ids = _extract_rule_ids_from_repo()
    mapped_rule_ids = _traceability_code_refs(payload, "rule_id")
    assert repo_rule_ids <= mapped_rule_ids


def test_traceability_covers_all_arbitration_codes() -> None:
    payload = _load_traceability()
    repo_codes = _extract_arbitration_codes_from_repo()
    mapped_codes = _traceability_code_refs(payload, "arbitration_code")
    assert repo_codes <= mapped_codes


def test_traceability_adr_refs_exist() -> None:
    payload = _load_traceability()
    for req in payload.get("requirements", []):
        for adr_path in req.get("adrs", []):
            assert (ROOT / adr_path).is_file(), f"Missing ADR: {adr_path}"


def test_traceability_test_file_refs_exist() -> None:
    payload = _load_traceability()
    for req in payload.get("requirements", []):
        for test_ref in req.get("tests", []):
            rel_path = test_ref.split("::", 1)[0]
            assert (ROOT / rel_path).is_file(), f"Missing test file: {rel_path}"


def test_traceability_includes_all_requirements_ids_from_requirements_doc() -> None:
    payload = _load_traceability()
    md_text = REQUIREMENTS_PATH.read_text(encoding="utf-8")

    req_ids_in_doc = set(re.findall(r"\bREQ-[A-Z]+-\d{3}\b", md_text))
    req_ids_in_yaml = {req["id"] for req in payload.get("requirements", [])}

    assert req_ids_in_doc <= req_ids_in_yaml
