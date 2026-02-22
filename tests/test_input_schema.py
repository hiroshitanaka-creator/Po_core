"""
tests/test_input_schema.py

Validates all scenario YAML files against docs/spec/input_schema_v1.json.

Requirements validated:
    FR-OUT-001 (input side) — Case YAMLs conform to input_schema_v1.json
    NFR-GOV-001 — CI fails if any scenario violates the schema contract

Dependencies: pytest, PyYAML, jsonschema
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any, Iterable, List

import pytest

# ---- Optional but strict: fail fast if dependencies are missing ----
try:
    import yaml  # PyYAML
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for this test. Install with: pip install pyyaml"
    ) from e

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "jsonschema is required for this test. Install with: pip install jsonschema"
    ) from e


ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "docs" / "spec" / "input_schema_v1.json"
SCENARIOS_DIR = ROOT_DIR / "scenarios"


def _iter_yaml_files(directory: Path) -> List[Path]:
    if not directory.exists():
        return []
    files = list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))
    # Exclude expected output files
    files = [f for f in files if "_expected" not in f.name]
    return sorted(files)


def _to_json_compatible(obj: Any) -> Any:
    """
    YAML -> Python で発生しうる型（date/datetime等）を、
    JSON Schema検証しやすい形（主に文字列）に正規化する。

    方針:
    - date / datetime: ISO 8601文字列へ
    - dict / list: 再帰
    - その他: JSON互換であることを期待（str/int/float/bool/None）
    """
    if isinstance(obj, _dt.datetime):
        # datetimeはdateのサブクラスなので先に処理
        return obj.isoformat()
    if isinstance(obj, _dt.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        # JSON object keys are strings
        return {str(k): _to_json_compatible(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_json_compatible(v) for v in obj]
    if isinstance(obj, tuple):
        return [_to_json_compatible(v) for v in obj]

    # set 等はJSONに存在しないので、ここで落として入力の異常を可視化する
    if isinstance(obj, set):
        raise TypeError("YAML contains a 'set' which is not JSON-compatible.")

    return obj


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return _to_json_compatible(data)


def _load_schema(schema_path: Path) -> dict:
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _format_path(path_parts: Iterable[Any]) -> str:
    """
    jsonschemaの error.path を人間が読める JSONPath 風にする。
    """
    p = "$"
    for part in path_parts:
        if isinstance(part, int):
            p += f"[{part}]"
        else:
            # key
            p += f".{part}"
    return p


def _summarize_errors(errors, limit: int = 20) -> str:
    lines: List[str] = []
    for i, err in enumerate(errors[:limit], start=1):
        instance_path = _format_path(err.path)
        schema_path = "#/" + "/".join(str(x) for x in err.schema_path)
        lines.append(
            f"[{i}] {err.message}\n"
            f"    instance_path: {instance_path}\n"
            f"    schema_path:   {schema_path}"
        )
    if len(errors) > limit:
        lines.append(f"... and {len(errors) - limit} more error(s).")
    return "\n\n".join(lines)


def _get_validator() -> Draft202012Validator:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Input schema not found: {SCHEMA_PATH}. "
            "Expected at: docs/spec/input_schema_v1.json"
        )

    schema = _load_schema(SCHEMA_PATH)
    # FormatChecker を渡すと date/date-time の形式チェックが有効になる
    return Draft202012Validator(schema, format_checker=FormatChecker())


YAML_FILES = _iter_yaml_files(SCENARIOS_DIR)


def test_scenarios_directory_exists():
    assert SCENARIOS_DIR.exists(), f"scenarios directory does not exist: {SCENARIOS_DIR}"


def test_has_at_least_one_case_yaml():
    assert len(YAML_FILES) > 0, f"No .yaml/.yml case files found in: {SCENARIOS_DIR}"


def test_has_expected_ten_cases():
    """M0成功指標: 受け入れテスト10本がYAMLで定義済みであること"""
    assert len(YAML_FILES) >= 10, (
        f"Expected at least 10 case YAML files in {SCENARIOS_DIR}, "
        f"found {len(YAML_FILES)}: {[f.name for f in YAML_FILES]}"
    )


@pytest.mark.parametrize("yaml_path", YAML_FILES, ids=lambda p: p.name)
def test_case_yaml_conforms_to_input_schema(yaml_path: Path):
    """
    各シナリオYAMLがinput_schema_v1.jsonに適合することを確認する。

    Requirements:
        FR-OUT-001 (input side)
        NFR-GOV-001
    """
    validator = _get_validator()
    data = _load_yaml(yaml_path)

    assert isinstance(data, dict), (
        f"{yaml_path} must contain a single YAML mapping (object) at the top level, "
        f"but got: {type(data).__name__}"
    )

    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        details = _summarize_errors(errors, limit=30)
        pytest.fail(f"Schema validation failed for: {yaml_path}\n\n{details}")


@pytest.mark.parametrize("yaml_path", YAML_FILES, ids=lambda p: p.name)
def test_case_yaml_has_required_fields(yaml_path: Path):
    """
    case_id, title, problem, constraints, values が存在することを明示的に確認する。
    (スキーマ検証と重複するが、エラーメッセージを分かりやすくするため)
    """
    data = _load_yaml(yaml_path)
    required_fields = ["case_id", "title", "problem", "constraints", "values"]
    for field in required_fields:
        assert field in data, (
            f"{yaml_path.name} is missing required field: '{field}'"
        )


@pytest.mark.parametrize("yaml_path", YAML_FILES, ids=lambda p: p.name)
def test_case_yaml_values_empty_is_ok(yaml_path: Path):
    """
    values: [] は有効な入力（問いの層を発火させるケース）であることを確認する。
    (case_009 など)
    """
    validator = _get_validator()
    data = _load_yaml(yaml_path)
    # values が空配列でもスキーマ適合することを確認
    # (スキーマ上 minItems: 0 なので、この test はドキュメント兼保険)
    if "values" in data and data["values"] == []:
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            details = _summarize_errors(errors, limit=10)
            pytest.fail(
                f"{yaml_path.name} has empty values: [] but failed schema validation.\n\n{details}"
            )
