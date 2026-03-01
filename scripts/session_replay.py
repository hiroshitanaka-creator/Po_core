#!/usr/bin/env python3
"""Session replay tool: apply answer patch, rerun pipeline, and record decision notes."""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pocore.orchestrator import run_case
from pocore.utils import to_json_compatible


DEFAULT_NOW = "2026-02-22T00:00:00Z"


def _repo_root() -> Path:
    return ROOT


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_case_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    normalized = to_json_compatible(data)
    if not isinstance(normalized, dict):
        raise TypeError(f"Case YAML must be an object at top-level: {path}")
    return normalized


def _load_validator(schema_name: str) -> Draft202012Validator:
    schema_path = _repo_root() / "docs" / "spec" / schema_name
    schema = _load_json(schema_path)
    if not isinstance(schema, dict):
        raise TypeError(f"Schema must be an object: {schema_path}")
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _validate_or_raise(
    validator: Draft202012Validator, instance: Any, *, label: str
) -> None:
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if not errors:
        return
    lines = [f"{label} failed schema validation ({len(errors)} error(s))."]
    for i, err in enumerate(errors[:10], start=1):
        path = "$" + "".join(
            f"[{p}]" if isinstance(p, int) else f".{p}" for p in err.path
        )
        lines.append(f"[{i}] {path}: {err.message}")
    raise ValueError("\n".join(lines))


def _decode_pointer_token(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def _split_pointer(path: str) -> List[str]:
    if path == "":
        return []
    if not path.startswith("/"):
        raise ValueError(f"JSON Pointer must start with '/': {path}")
    return [_decode_pointer_token(tok) for tok in path[1:].split("/")]


def _resolve_parent(doc: Any, path: str) -> tuple[Any, str]:
    tokens = _split_pointer(path)
    if not tokens:
        return None, ""

    cur = doc
    for token in tokens[:-1]:
        if isinstance(cur, list):
            if token == "-":
                raise ValueError("'-' is only valid for add at final list segment")
            idx = int(token)
            cur = cur[idx]
        elif isinstance(cur, dict):
            if token not in cur:
                raise KeyError(f"Missing object key in pointer path: {token}")
            cur = cur[token]
        else:
            raise TypeError("Cannot traverse non-container value")

    return cur, tokens[-1]


def _get_value(doc: Any, path: str) -> Any:
    if path == "":
        return doc
    cur = doc
    for token in _split_pointer(path):
        if isinstance(cur, list):
            if token == "-":
                raise ValueError("'-' is invalid outside add operation")
            cur = cur[int(token)]
        elif isinstance(cur, dict):
            cur = cur[token]
        else:
            raise TypeError("Cannot traverse non-container value")
    return cur


def _add_op(doc: Any, path: str, value: Any) -> Any:
    if path == "":
        return copy.deepcopy(value)

    parent, token = _resolve_parent(doc, path)
    if isinstance(parent, list):
        if token == "-":
            parent.append(copy.deepcopy(value))
        else:
            parent.insert(int(token), copy.deepcopy(value))
    elif isinstance(parent, dict):
        parent[token] = copy.deepcopy(value)
    else:
        raise TypeError("add target parent is not container")
    return doc


def _replace_op(doc: Any, path: str, value: Any) -> Any:
    if path == "":
        return copy.deepcopy(value)

    parent, token = _resolve_parent(doc, path)
    if isinstance(parent, list):
        parent[int(token)] = copy.deepcopy(value)
    elif isinstance(parent, dict):
        if token not in parent:
            raise KeyError(f"replace target does not exist: {path}")
        parent[token] = copy.deepcopy(value)
    else:
        raise TypeError("replace target parent is not container")
    return doc


def _remove_op(doc: Any, path: str) -> Any:
    if path == "":
        raise ValueError("remove cannot target document root")

    parent, token = _resolve_parent(doc, path)
    if isinstance(parent, list):
        del parent[int(token)]
    elif isinstance(parent, dict):
        del parent[token]
    else:
        raise TypeError("remove target parent is not container")
    return doc


def apply_rfc6902_patch(document: Dict[str, Any], patch_ops: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Apply RFC6902 patch operations to document and return patched copy."""
    doc: Any = copy.deepcopy(document)

    for i, op in enumerate(patch_ops, start=1):
        op_name = str(op.get("op", "")).strip()
        path = str(op.get("path", ""))

        if op_name == "add":
            doc = _add_op(doc, path, op.get("value"))
        elif op_name == "replace":
            doc = _replace_op(doc, path, op.get("value"))
        elif op_name == "remove":
            doc = _remove_op(doc, path)
        elif op_name == "copy":
            from_path = str(op.get("from", ""))
            doc = _add_op(doc, path, _get_value(doc, from_path))
        elif op_name == "move":
            from_path = str(op.get("from", ""))
            moved = _get_value(doc, from_path)
            doc = _remove_op(doc, from_path)
            doc = _add_op(doc, path, moved)
        elif op_name == "test":
            current = _get_value(doc, path)
            if current != op.get("value"):
                raise ValueError(f"Patch op #{i} test failed at path={path}")
        else:
            raise ValueError(f"Unsupported patch op at index {i}: {op_name}")

    if not isinstance(doc, dict):
        raise TypeError("Patched case must remain a JSON object")
    return doc




def _coerce_answers_payload(payload: Any, *, case_path: Path) -> Any:
    """Backward-compatible coercion for legacy patch-only answers payload."""
    if not isinstance(payload, dict):
        return payload
    has_required = all(k in payload for k in ("version", "case_ref", "answers", "patch"))
    if has_required:
        return payload
    if isinstance(payload.get("patch"), list):
        patch_paths = [
            str(op.get("path", ""))
            for op in payload["patch"]
            if isinstance(op, dict) and str(op.get("path", ""))
        ]
        return {
            "version": "1.0",
            "case_ref": case_path.name,
            "answers": [
                {
                    "question_id": "legacy.patch",
                    "answer_text": "legacy patch payload",
                    "applied_patch_paths": patch_paths,
                }
            ],
            "patch": payload["patch"],
        }
    return payload

def _normalize_answers_payload(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        patch = payload
    elif isinstance(payload, dict):
        if isinstance(payload.get("patch"), list):
            patch = payload["patch"]
        elif isinstance(payload.get("operations"), list):
            patch = payload["operations"]
        else:
            raise ValueError("answers JSON must include list field 'patch' or 'operations'")
    else:
        raise TypeError("answers JSON must be an object or an array")

    normalized: List[Dict[str, Any]] = []
    for op in patch:
        if not isinstance(op, dict):
            raise TypeError("Each patch operation must be an object")
        normalized.append(op)
    return normalized


def _coerce_answers_envelope(payload: Any, *, case_path: Path) -> Any:
    """Backward-compatible shim: allow patch-only payloads in local tooling.

    Canonical format remains session_answers_schema_v1, but unit/integration
    utilities may provide only `{ "patch": [...] }`.
    """
    if not isinstance(payload, dict):
        return payload

    if {"version", "case_ref", "answers", "patch"}.issubset(payload.keys()):
        return payload

    patch_ops = payload.get("patch") or payload.get("operations")
    if not isinstance(patch_ops, list):
        return payload

    return {
        "version": "1.0",
        "case_ref": case_path.name,
        "answers": [
            {
                "question_id": "session_replay_legacy",
                "answer_text": "Auto-coerced legacy patch payload.",
                "applied_patch_paths": [
                    str(op.get("path", ""))
                    for op in patch_ops
                    if isinstance(op, dict)
                    and isinstance(op.get("path"), str)
                    and str(op.get("path")).startswith("/")
                ],
            }
        ],
        "patch": patch_ops,
    }


def _json_text(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _render_key_points(before: Dict[str, Any], after: Dict[str, Any]) -> str:
    rec_before = before.get("recommendation")
    rec_after = after.get("recommendation")
    q_before = len(before.get("questions", [])) if isinstance(before.get("questions"), list) else 0
    q_after = len(after.get("questions", [])) if isinstance(after.get("questions"), list) else 0

    return "\n".join(
        [
            f"- recommendation changed: {'yes' if rec_before != rec_after else 'no'}",
            f"- questions count: {q_before} -> {q_after}",
            f"- options count: {len(before.get('options', []))} -> {len(after.get('options', []))}",
            f"- input digest changed: {before.get('case_ref', {}).get('input_digest') != after.get('case_ref', {}).get('input_digest')}",
        ]
    )


def _build_decision_record(
    *,
    case_path: Path,
    answers_path: Path,
    now: str,
    seed: int,
    patch_ops: Sequence[Dict[str, Any]],
    original_case: Dict[str, Any],
    patched_case: Dict[str, Any],
    before_output: Dict[str, Any],
    after_output: Dict[str, Any],
) -> str:
    patch_paths = [str(op.get("path", "")) for op in patch_ops]
    case_diff = "".join(
        difflib.unified_diff(
            _json_text(original_case).splitlines(keepends=True),
            _json_text(patched_case).splitlines(keepends=True),
            fromfile="case_before.json",
            tofile="case_after.json",
            n=3,
        )
    )
    output_diff = "".join(
        difflib.unified_diff(
            _json_text(before_output).splitlines(keepends=True),
            _json_text(after_output).splitlines(keepends=True),
            fromfile="output_before.json",
            tofile="output_after.json",
            n=3,
        )
    )

    return f"""# Decision Record (session replay)

## Replay metadata
- case: `{case_path}`
- answers: `{answers_path}`
- now: `{now}`
- seed: `{seed}`
- patch operations: {len(patch_ops)}
- patched paths: {", ".join(patch_paths) if patch_paths else "(none)"}

## Key points
{_render_key_points(before_output, after_output)}

## Input patch diff
```diff
{case_diff.rstrip()}
```

## Output diff (before vs replay)
```diff
{output_diff.rstrip()}
```
"""


def replay_session(
    *,
    case_path: Path,
    answers_path: Path,
    out_dir: Path,
    now: str = DEFAULT_NOW,
    seed: int = 0,
) -> Dict[str, Path]:
    case = _load_case_yaml(case_path)
    answers_payload = _load_json(answers_path)
    answers_payload = _coerce_answers_envelope(answers_payload, case_path=case_path)

    input_validator = _load_validator("input_schema_v1.json")
    output_validator = _load_validator("output_schema_v1.json")

    _validate_or_raise(input_validator, case, label=f"Input case {case_path.name}")

    answers_schema_path = _repo_root() / "docs" / "spec" / "session_answers_schema_v1.json"
    # Backward compatibility: replay accepted patch-only payloads before the
    # session_answers_v1 envelope was introduced. Keep supporting that legacy
    # shape to avoid breaking existing tooling/tests.
    if answers_schema_path.exists() and isinstance(answers_payload, dict):
        has_v1_envelope = all(
            key in answers_payload for key in ("version", "case_ref", "answers")
        )
        if has_v1_envelope:
            answers_validator = _load_validator("session_answers_schema_v1.json")
            _validate_or_raise(
                answers_validator,
                answers_payload,
                label=f"Session answers {answers_path.name}",
            )

    patch_ops = _normalize_answers_payload(answers_payload)
    patched_case = apply_rfc6902_patch(case, patch_ops)
    _validate_or_raise(input_validator, patched_case, label="Patched input case")

    before_output = run_case(case, case_path=case_path, seed=seed, now=now, deterministic=True)
    replay_output = run_case(
        patched_case,
        case_path=case_path,
        seed=seed,
        now=now,
        deterministic=True,
    )
    _validate_or_raise(output_validator, replay_output, label="Replay output")

    out_dir.mkdir(parents=True, exist_ok=True)
    patched_case_path = out_dir / "replay_case.json"
    output_path = out_dir / "replay_output.json"
    decision_record_path = out_dir / "decision_record.md"

    patched_case_path.write_text(_json_text(patched_case), encoding="utf-8")
    output_path.write_text(_json_text(replay_output), encoding="utf-8")

    decision_record = _build_decision_record(
        case_path=case_path,
        answers_path=answers_path,
        now=now,
        seed=seed,
        patch_ops=patch_ops,
        original_case=case,
        patched_case=patched_case,
        before_output=before_output,
        after_output=replay_output,
    )
    decision_record_path.write_text(decision_record, encoding="utf-8")

    return {
        "patched_case": patched_case_path,
        "output": output_path,
        "decision_record": decision_record_path,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply session answers (RFC6902 patch) to a case and rerun deterministic pipeline."
    )
    parser.add_argument("--case", required=True, help="Path to case YAML file.")
    parser.add_argument("--answers", required=True, help="Path to answers JSON file.")
    parser.add_argument("--now", default=DEFAULT_NOW, help="Injected deterministic timestamp.")
    parser.add_argument("--seed", type=int, default=0, help="Deterministic seed.")
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Directory to write replay_case.json, replay_output.json, decision_record.md.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    outputs = replay_session(
        case_path=Path(args.case),
        answers_path=Path(args.answers),
        out_dir=Path(args.out_dir),
        now=args.now,
        seed=args.seed,
    )
    print(f"[OK] patched case   : {outputs['patched_case']}")
    print(f"[OK] replay output  : {outputs['output']}")
    print(f"[OK] decision record: {outputs['decision_record']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
