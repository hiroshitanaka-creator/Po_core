"""
tests/test_output_schema.py

Validates output_schema_v1.json itself and any golden/expected output JSON files
against that schema.

Requirements validated:
    FR-OUT-001 — Po_core JSON output must conform to output_schema_v1.json
    NFR-REP-001 — Output structure is deterministic and schema-constrained
    NFR-GOV-001 — CI fails if schema contract is broken

Dependencies: pytest, jsonschema
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

import pytest

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "jsonschema is required for this test. Install with: pip install jsonschema"
    ) from e


ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "docs" / "spec" / "output_schema_v1.json"
SCENARIOS_DIR = ROOT_DIR / "scenarios"
OUTPUTS_DIR = ROOT_DIR / "outputs"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _format_path(path_parts: Iterable[Any]) -> str:
    """jsonschema error.path を JSONPath 風に整形する。"""
    p = "$"
    for part in path_parts:
        if isinstance(part, int):
            p += f"[{part}]"
        else:
            p += f".{part}"
    return p


def _summarize_errors(errors, limit: int = 30) -> str:
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
            f"Output schema not found: {SCHEMA_PATH}. "
            "Expected at: docs/spec/output_schema_v1.json"
        )
    schema = _load_json(SCHEMA_PATH)
    # format: date-time の検証も有効化
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _iter_output_sample_files() -> List[Path]:
    """
    期待出力（golden files）置き場を複数許容する。
    - scenarios/*_expected.json  : ケースごとの期待出力
    - outputs/*_output.json      : 実行結果出力
    - outputs/*_result.json      : 実行結果出力（別命名）
    - outputs/*_expected.json    : 期待出力をoutputsに置く派への逃げ道
    """
    files: List[Path] = []

    if SCENARIOS_DIR.exists():
        files.extend(SCENARIOS_DIR.glob("*_expected.json"))

    if OUTPUTS_DIR.exists():
        files.extend(OUTPUTS_DIR.glob("*_output.json"))
        files.extend(OUTPUTS_DIR.glob("*_result.json"))
        files.extend(OUTPUTS_DIR.glob("*_expected.json"))

    # 重複排除 + ソート
    uniq = sorted({p.resolve() for p in files})
    return [Path(p) for p in uniq]


SAMPLE_FILES = _iter_output_sample_files()


def _smoke_minimal_valid_output() -> dict:
    """
    Schemaが矛盾していないことを保証するための最小スモーク出力。
    これが通らないなら schema 自体が壊れている。

    Requirements: FR-OUT-001
    """
    # 64 hex chars
    digest = "0" * 64

    option_1 = {
        "option_id": "opt_1",
        "title": "案A：段階的に進める",
        "description": "リスクを抑えつつ小さく試して前進する。",
        "action_plan": [{"step": "最小実験を設計する"}],
        "pros": ["失敗コストを抑えられる"],
        "cons": ["進行が遅く感じる可能性"],
        "risks": [
            {
                "risk": "検証が不十分になる",
                "severity": "medium",
                "mitigation": "検証項目を明文化する",
            }
        ],
        "ethics_review": {
            "principles_applied": ["integrity", "autonomy"],
            "tradeoffs": [
                {
                    "tension": "速度と安全の緊張",
                    "between": ["nonmaleficence", "accountability"],
                    "mitigation": "段階リリースと監視で両立を狙う",
                    "severity": "medium",
                }
            ],
            "concerns": ["情報不足のまま断言しない"],
            "confidence": "medium",
        },
        "responsibility_review": {
            "decision_owner": "user",
            "stakeholders": [
                {"name": "自分", "role": "意思決定主体", "impact": "結果責任を負う"}
            ],
            "accountability_notes": "最終判断はユーザーが行い、Po_coreは手続きを支援する。",
            "confidence": "high",
        },
        "feasibility": {
            "effort": "medium",
            "timeline": "1-2 weeks",
            "confidence": "medium",
        },
        "uncertainty": {
            "overall_level": "medium",
            "reasons": ["外部条件が未確定"],
            "assumptions": ["現状の制約が継続する"],
            "known_unknowns": ["関係者の同意状況"],
        },
    }

    option_2 = {
        "option_id": "opt_2",
        "title": "案B：いったん保留して情報収集",
        "description": "重要な不明点を埋めてから判断する。",
        "action_plan": [{"step": "不足情報を5項目に絞って集める"}],
        "pros": ["判断の精度が上がる"],
        "cons": ["機会損失が起きる可能性"],
        "risks": [
            {
                "risk": "先延ばし癖が発動する",
                "severity": "low",
                "mitigation": "期限と判断条件を設定する",
            }
        ],
        "ethics_review": {
            "principles_applied": ["integrity", "justice"],
            "tradeoffs": [],
            "concerns": ["情報収集が目的化しないよう注意"],
            "confidence": "medium",
        },
        "responsibility_review": {
            "decision_owner": "user",
            "stakeholders": [
                {
                    "name": "自分",
                    "role": "意思決定主体",
                    "impact": "機会損失と納得感に影響",
                }
            ],
            "accountability_notes": "保留の理由と追加で必要な条件を説明可能にする。",
            "confidence": "medium",
        },
        "feasibility": {"effort": "low", "timeline": "3-5 days", "confidence": "high"},
        "uncertainty": {
            "overall_level": "high",
            "reasons": ["情報が不足している"],
            "assumptions": ["情報収集ルートが存在する"],
            "known_unknowns": ["意思決定期限の柔軟性"],
        },
    }

    out = {
        "meta": {
            "schema_version": "1.0",
            "pocore_version": "0.1.0",
            "run_id": "smoke-run-0001",
            "created_at": "2026-02-22T00:00:00Z",
            "seed": 0,
            "deterministic": True,
            "generator": {"name": "generator_stub", "version": "0.1.0", "mode": "stub"},
        },
        "case_ref": {
            "case_id": "case_smoke",
            "title": "Smoke Test Case",
            "input_digest": digest,
        },
        "options": [option_1, option_2],
        "recommendation": {
            "status": "recommended",
            "recommended_option_id": "opt_1",
            "reason": "段階的に進めることで害を抑えつつ前進できるため。",
            "counter": "スピードが足りず機会損失になる可能性がある。",
            "alternatives": [
                {
                    "option_id": "opt_2",
                    "when_to_choose": "期限に余裕があり重要不明点が多い場合",
                }
            ],
            "confidence": "medium",
        },
        "ethics": {
            "principles_used": [
                "integrity",
                "autonomy",
                "nonmaleficence",
                "justice",
                "accountability",
            ],
            "tradeoffs": [
                {
                    "tension": "速度と安全の緊張",
                    "between": ["nonmaleficence", "accountability"],
                    "mitigation": "段階実行で安全側に倒しつつ、期限を設定する",
                    "severity": "medium",
                }
            ],
            "guardrails": [
                "不確実な事実を断言しない",
                "意思決定主体をユーザーから奪わない",
                "反証と代替案を必ず提示する",
            ],
            "notes": "倫理は単一最適化ではなく、トレードオフを開示する。",
        },
        "responsibility": {
            "decision_owner": "user",
            "stakeholders": [
                {"name": "自分", "role": "意思決定主体", "impact": "結果責任を負う"}
            ],
            "accountability_notes": "Po_coreは助言と構造化を提供し、最終判断はユーザーが行う。",
            "consent_considerations": [
                "関係者がいる場合は事前に影響説明と合意を検討する"
            ],
        },
        "questions": [
            {
                "question_id": "q1",
                "question": "あなたが最優先する価値は『安定』と『成長』のどちらに近い？",
                "priority": 1,
                "why_needed": "推奨の軸（価値関数）を固定しないと判断がぶれるため。",
                "assumption_if_unanswered": "安定と成長を同等に扱う",
                "optional": True,
            }
        ],
        "uncertainty": {
            "overall_level": "medium",
            "reasons": ["ケース情報が一部不足している"],
            "assumptions": ["提示された制約が正しい"],
            "known_unknowns": ["外部要因（他者の反応、将来状況）"],
        },
        "trace": {
            "version": "1.0",
            "steps": [
                {
                    "name": "parse_input",
                    "started_at": "2026-02-22T00:00:00Z",
                    "ended_at": "2026-02-22T00:00:01Z",
                    "summary": "入力を正規化して必須項目を抽出した",
                    "metrics": {"input_fields": 5},
                },
                {
                    "name": "generate_options",
                    "started_at": "2026-02-22T00:00:01Z",
                    "ended_at": "2026-02-22T00:00:02Z",
                    "summary": "スタブ生成器で2案を生成した",
                    "metrics": {"options": 2},
                },
                {
                    "name": "ethics_review",
                    "started_at": "2026-02-22T00:00:02Z",
                    "ended_at": "2026-02-22T00:00:03Z",
                    "summary": "倫理原則とトレードオフを評価した",
                },
                {
                    "name": "responsibility_review",
                    "started_at": "2026-02-22T00:00:03Z",
                    "ended_at": "2026-02-22T00:00:04Z",
                    "summary": "責任主体と利害関係者を整理した",
                },
                {
                    "name": "question_layer",
                    "started_at": "2026-02-22T00:00:04Z",
                    "ended_at": "2026-02-22T00:00:05Z",
                    "summary": "不足情報を補う問いを生成した",
                    "metrics": {"questions": 1},
                },
                {
                    "name": "compose_output",
                    "started_at": "2026-02-22T00:00:05Z",
                    "ended_at": "2026-02-22T00:00:06Z",
                    "summary": "最終出力（JSON/Markdown）を組み立てた",
                },
            ],
        },
        "rendered": {
            "markdown": "# Smoke Output\n\nこれはスキーマ検証用の最小出力です。"
        },
    }
    return out


def test_output_schema_file_exists():
    assert SCHEMA_PATH.exists(), f"output schema does not exist: {SCHEMA_PATH}"


def test_output_schema_is_valid_json_schema():
    """output_schema_v1.json 自体が有効なJSON Schemaであることを確認する。"""
    schema = _load_json(SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as e:
        pytest.fail(
            f"output_schema_v1.json is not a valid JSON Schema (Draft 2020-12).\n{e}"
        )


def test_smoke_output_conforms_to_output_schema():
    """
    最小スモーク出力がschemaに適合することを確認する。
    これが失敗する場合、schema自体に問題がある。

    Requirements: FR-OUT-001
    """
    validator = _get_validator()
    instance = _smoke_minimal_valid_output()

    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        details = _summarize_errors(errors, limit=50)
        pytest.fail(f"Smoke output does NOT conform to output schema.\n\n{details}")


def test_smoke_output_has_all_five_ethics_principles():
    """
    スモーク出力がFR-ETH-001を満たすことを確認する（5原則すべて含む）。

    Requirements: FR-ETH-001
    """
    instance = _smoke_minimal_valid_output()
    principles = set(instance["ethics"]["principles_used"])
    required = {"integrity", "autonomy", "nonmaleficence", "justice", "accountability"}
    assert (
        required == principles
    ), f"Smoke output missing ethics principles. Expected: {required}, got: {principles}"


def test_smoke_output_recommendation_has_counter_and_alternatives():
    """
    スモーク出力がFR-REC-001を満たすことを確認する（推奨+反証+代替）。

    Requirements: FR-REC-001
    """
    instance = _smoke_minimal_valid_output()
    rec = instance["recommendation"]
    assert rec["status"] == "recommended"
    assert rec.get("counter"), "recommendation.counter must be non-empty (FR-REC-001)"
    assert (
        len(rec.get("alternatives", [])) >= 1
    ), "recommendation.alternatives must have >=1 item (FR-REC-001)"


def test_smoke_output_uncertainty_exists():
    """
    スモーク出力がFR-UNC-001を満たすことを確認する。

    Requirements: FR-UNC-001
    """
    instance = _smoke_minimal_valid_output()
    unc = instance["uncertainty"]
    assert unc.get("overall_level") in ("low", "medium", "high")
    assert isinstance(unc.get("reasons"), list)


def test_smoke_output_trace_has_required_steps():
    """
    スモーク出力がFR-TR-001を満たすことを確認する（必須ステップの存在）。

    Requirements: FR-TR-001
    """
    instance = _smoke_minimal_valid_output()
    step_names = {s["name"] for s in instance["trace"]["steps"]}
    assert (
        "parse_input" in step_names
    ), "trace must include parse_input step (FR-TR-001)"
    assert (
        "compose_output" in step_names
    ), "trace must include compose_output step (FR-TR-001)"
    assert instance["trace"]["version"], "trace.version must be non-empty (FR-TR-001)"


@pytest.mark.parametrize("json_path", SAMPLE_FILES, ids=lambda p: p.name)
def test_output_json_samples_conform_to_output_schema(json_path: Path):
    """
    期待出力（golden files）がoutput_schema_v1.jsonに適合することを確認する。

    Requirements: FR-OUT-001, NFR-GOV-001
    """
    validator = _get_validator()
    data = _load_json(json_path)

    assert isinstance(data, dict), (
        f"{json_path} must contain a single JSON object at the top level, "
        f"but got: {type(data).__name__}"
    )

    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        details = _summarize_errors(errors, limit=50)
        pytest.fail(
            f"Schema validation failed for output sample: {json_path}\n\n{details}"
        )


@pytest.mark.parametrize("json_path", SAMPLE_FILES, ids=lambda p: p.name)
def test_golden_output_responsibility_decision_owner(json_path: Path):
    """
    golden fileが FR-RES-001 を満たすことを確認する（decision_owner非空）。

    Requirements: FR-RES-001
    """
    data = _load_json(json_path)
    owner = data.get("responsibility", {}).get("decision_owner", "")
    assert (
        owner
    ), f"{json_path.name}: responsibility.decision_owner must be non-empty (FR-RES-001)"


@pytest.mark.parametrize("json_path", SAMPLE_FILES, ids=lambda p: p.name)
def test_golden_output_ethics_principles_at_least_two(json_path: Path):
    """
    golden fileが FR-ETH-001 を満たすことを確認する（2原則以上）。

    Requirements: FR-ETH-001
    """
    data = _load_json(json_path)
    principles = data.get("ethics", {}).get("principles_used", [])
    assert len(principles) >= 2, (
        f"{json_path.name}: ethics.principles_used must have >=2 entries (FR-ETH-001), "
        f"got: {principles}"
    )


def test_note_on_output_samples_presence():
    """
    出力サンプルが0件でもsmokeが通るのでCIは通る。
    ただし「契約の殴り」を強くしたいなら、golden filesを追加すること。
    """
    if not SAMPLE_FILES:
        pytest.skip(
            "No output sample JSON files found. "
            "Add scenarios/*_expected.json or outputs/*_output.json to validate real outputs."
        )
