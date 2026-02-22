"""
src/po_core/runner.py
=====================

Po_core scenario runner — M1 stub implementation.

Public API
----------
    run_case_file(path, seed, now, deterministic) -> dict

Pipeline (executed in order):
    1. Load YAML
    2. Validate against input_schema_v1.json
    3. Compute input_digest  = sha256(canonical_json(case))
    4. Generate stub output  (deterministic given same inputs)
    5. Validate against output_schema_v1.json
    6. Return dict

Determinism contract (ADR-0002):
    Same path + same seed + same now + deterministic=True → identical JSON.

Dependencies: PyYAML, jsonschema (both in dev requirements)
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Optional, Union

try:
    import yaml
except ImportError as _e:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for po_core.runner. pip install pyyaml"
    ) from _e

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as _e:  # pragma: no cover
    raise ImportError(
        "jsonschema is required for po_core.runner. pip install jsonschema"
    ) from _e

# ── Paths ─────────────────────────────────────────────────────────────────

_ROOT = Path(__file__).resolve().parents[2]  # src/po_core → src → repo root
_INPUT_SCHEMA = _ROOT / "docs" / "spec" / "input_schema_v1.json"
_OUTPUT_SCHEMA = _ROOT / "docs" / "spec" / "output_schema_v1.json"

_DEFAULT_NOW = "2026-02-22T00:00:00Z"

# ── Helpers ───────────────────────────────────────────────────────────────


def _to_json_compat(obj: object) -> object:
    """Recursively convert PyYAML types (date/datetime) to JSON-safe types."""
    if isinstance(obj, dt.datetime):
        return obj.isoformat()
    if isinstance(obj, dt.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): _to_json_compat(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_json_compat(v) for v in obj]
    return obj


def _canonical_json(data: dict) -> str:
    """Canonical JSON: sorted keys, no whitespace, UTF-8 characters preserved."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(data: dict) -> str:
    """SHA-256 hex digest of canonical JSON."""
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def _load_schema(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate(data: dict, schema_path: Path, label: str) -> None:
    schema = _load_schema(schema_path)
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(v.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        msgs = [f"  [{i}] {e.message}" for i, e in enumerate(errors, 1)]
        raise ValueError(f"{label} schema validation failed:\n" + "\n".join(msgs))


def _ts(base: dt.datetime, offset_secs: int) -> str:
    """ISO-8601 UTC timestamp at base + offset_secs."""
    t = base + dt.timedelta(seconds=offset_secs)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Stub generator ────────────────────────────────────────────────────────


def _build_stub(
    case: dict,
    digest: str,
    seed: int,
    now: str,
    run_id: str,
    deterministic: bool,
) -> dict:
    """
    Build a minimal, schema-valid stub output for the given case.

    Content is derived entirely from the case data + injection parameters,
    ensuring determinism: same inputs → same output.
    """
    base = dt.datetime.fromisoformat(now.replace("Z", "+00:00"))
    values_empty = len(case.get("values", [])) == 0
    unknowns: list = case.get("unknowns", [])
    constraints: list = case.get("constraints", [])

    # Stakeholders (up to 3, minimum 1)
    raw_sh: list = case.get("stakeholders", [])
    stakeholders = [
        {"name": s["name"], "role": s["role"], "impact": s["impact"]}
        for s in raw_sh[:3]
    ]
    if not stakeholders:
        stakeholders = [
            {"name": "user", "role": "意思決定主体", "impact": "意思決定に影響"}
        ]

    # ── Options ──────────────────────────────────────────────────────────
    options = [
        {
            "option_id": "opt_1",
            "title": "情報収集して期限付きで決断",
            "description": "不明点を整理し、基準を決めて期限付きで判断する。",
            "action_plan": [{"step": "不明点をリストアップして解消する"}],
            "pros": ["情報に基づいた判断ができる"],
            "cons": ["時間がかかる"],
            "risks": [
                {
                    "risk": "先延ばしのリスク",
                    "severity": "medium",
                    "mitigation": "期限を設定する",
                }
            ],
            "ethics_review": {
                "principles_applied": ["integrity", "autonomy"],
                "tradeoffs": [],
                "concerns": ["不確実な事実を断言しない"],
                "confidence": "high",
            },
            "responsibility_review": {
                "decision_owner": "user",
                "stakeholders": stakeholders[:2],
                "accountability_notes": "最終判断はユーザー。",
                "confidence": "high",
            },
            "feasibility": {
                "effort": "low",
                "timeline": "1-2 weeks",
                "confidence": "high",
            },
            "uncertainty": {
                "overall_level": "medium",
                "reasons": unknowns[:1] if unknowns else ["重要情報が未確定"],
                "assumptions": [],
                "known_unknowns": unknowns[:2],
            },
        },
        {
            "option_id": "opt_2",
            "title": "現状維持で探索を続ける",
            "description": "安全を保ちつつ選択肢を広げる。",
            "action_plan": [{"step": "現状を維持しながら情報を集める"}],
            "pros": ["リスクが低い"],
            "cons": ["変化が遅い"],
            "risks": [
                {
                    "risk": "現状固定化",
                    "severity": "medium",
                    "mitigation": "定期的に判断条件を見直す",
                }
            ],
            "ethics_review": {
                "principles_applied": ["autonomy", "nonmaleficence"],
                "tradeoffs": [],
                "concerns": ["断言を避ける"],
                "confidence": "medium",
            },
            "responsibility_review": {
                "decision_owner": "user",
                "stakeholders": stakeholders[:1],
                "accountability_notes": "判断責任はユーザーにある。",
                "confidence": "high",
            },
            "feasibility": {
                "effort": "low",
                "timeline": "ongoing",
                "confidence": "high",
            },
            "uncertainty": {
                "overall_level": "high" if values_empty else "medium",
                "reasons": ["目的や優先順位が未確定"],
                "assumptions": [],
                "known_unknowns": unknowns[:1],
            },
        },
    ]

    # ── Recommendation ────────────────────────────────────────────────────
    if values_empty:
        recommendation: dict = {
            "status": "no_recommendation",
            "reason": "価値観と目的が未確定なため、推奨は恣意的になる。まず問いで軸を作る。",
            "missing_info": unknowns[:3] if unknowns else ["価値観", "目的"],
            "next_steps": ["質問に答えて価値の優先順位を仮決めする"],
            "confidence": "high",
        }
    else:
        recommendation = {
            "status": "recommended",
            "recommended_option_id": "opt_1",
            "reason": "重要不明点を整理してから判断する方が誠実で後悔を減らしやすい。",
            "counter": "期限を守れないと先延ばしになり、機会損失が増える。",
            "alternatives": [
                {"option_id": "opt_2", "when_to_choose": "安定を優先したい場合"}
            ],
            "confidence": "medium",
        }

    # ── Questions (from unknowns, up to 5) ────────────────────────────────
    questions = [
        {
            "question_id": f"q{i}",
            "question": f"{u}は？",
            "priority": min(i, 5),
            "why_needed": "判断の前提条件を確定するため。",
            "assumption_if_unanswered": "最も安全側の仮定を採用する",
            "optional": i > 2,
        }
        for i, u in enumerate(unknowns[:5], 1)
    ]
    if not questions:
        questions = [
            {
                "question_id": "q1",
                "question": "最も重要な不明点は何か？",
                "priority": 1,
                "why_needed": "判断基準を確定するため。",
                "assumption_if_unanswered": "安全側の仮定を採用する",
                "optional": False,
            }
        ]

    # ── Trace ─────────────────────────────────────────────────────────────
    trace_steps = [
        {
            "name": "parse_input",
            "started_at": _ts(base, 0),
            "ended_at": _ts(base, 1),
            "summary": "入力を正規化し、不明点を抽出した",
        },
        {
            "name": "generate_options",
            "started_at": _ts(base, 1),
            "ended_at": _ts(base, 2),
            "summary": f"{len(options)}案を生成した",
            "metrics": {"options": len(options)},
        },
        {
            "name": "ethics_review",
            "started_at": _ts(base, 2),
            "ended_at": _ts(base, 3),
            "summary": "倫理原則とトレードオフを評価した",
        },
        {
            "name": "responsibility_review",
            "started_at": _ts(base, 3),
            "ended_at": _ts(base, 4),
            "summary": "責任主体と利害関係者を整理した",
        },
        {
            "name": "question_layer",
            "started_at": _ts(base, 4),
            "ended_at": _ts(base, 5),
            "summary": f"質問を{len(questions)}件生成した",
            "metrics": {"questions": len(questions)},
        },
        {
            "name": "compose_output",
            "started_at": _ts(base, 5),
            "ended_at": _ts(base, 6),
            "summary": "推奨・反証・代替案を含む出力を組み立てた",
        },
    ]

    return {
        "meta": {
            "schema_version": "1.0",
            "pocore_version": "0.2.0b3",
            "run_id": run_id,
            "created_at": now,
            "seed": seed,
            "deterministic": deterministic,
            "generator": {
                "name": "generator_stub",
                "version": "0.1.0",
                "mode": "stub",
            },
        },
        "case_ref": {
            "case_id": case["case_id"],
            "title": case["title"],
            "input_digest": digest,
        },
        "options": options,
        "recommendation": recommendation,
        "ethics": {
            "principles_used": [
                "integrity",
                "autonomy",
                "nonmaleficence",
                "justice",
                "accountability",
            ],
            "tradeoffs": [],
            "guardrails": [
                "不確実な事実を断言しない",
                "意思決定主体をユーザーから奪わない",
                "推奨には反証と代替案を併記する",
            ],
            "notes": "価値の衝突を前提に、トレードオフを開示する。",
        },
        "responsibility": {
            "decision_owner": "user",
            "stakeholders": stakeholders,
            "accountability_notes": (
                "意思決定と結果責任はユーザー。Po_coreは問いと構造化を提供する。"
            ),
            "consent_considerations": [],
        },
        "questions": questions,
        "uncertainty": {
            "overall_level": "high" if values_empty else "medium",
            "reasons": unknowns[:2] if unknowns else ["重要情報が未確定"],
            "assumptions": constraints[:1],
            "known_unknowns": unknowns[:3],
        },
        "trace": {
            "version": "1.0",
            "steps": trace_steps,
        },
    }


# ── Public API ────────────────────────────────────────────────────────────


def run_case_file(
    path: Union[str, Path],
    seed: int = 0,
    now: Optional[str] = None,
    deterministic: bool = True,
) -> dict:
    """
    Run a scenario YAML file through the Po_core stub pipeline.

    Args:
        path:          Path to case YAML file (``scenarios/*.yaml``).
        seed:          Determinism seed (reserved; not yet used internally).
        now:           ISO-8601 UTC datetime for trace timestamps.
                       Defaults to ``"2026-02-22T00:00:00Z"``.
        deterministic: When True, ``run_id`` is derived from ``case_id``
                       (same input → same run_id).

    Returns:
        Output dict conforming to ``output_schema_v1.json``.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError:        If input or output schema validation fails.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Case file not found: {path}")

    if now is None:
        now = _DEFAULT_NOW

    # 1. Load YAML
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    case: dict = _to_json_compat(raw)  # type: ignore[assignment]

    # 2. Validate input
    _validate(case, _INPUT_SCHEMA, "Input")

    # 3. Compute input_digest
    digest = _digest(case)

    # 4. Generate stub output
    run_id = (
        f"{case['case_id']}_stub_v1"
        if deterministic
        else __import__("uuid").uuid4().hex
    )
    output = _build_stub(
        case,
        digest=digest,
        seed=seed,
        now=now,
        run_id=run_id,
        deterministic=deterministic,
    )

    # 5. Validate output
    _validate(output, _OUTPUT_SCHEMA, "Output")

    # 6. Return
    return output
