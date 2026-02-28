"""Decision Session v1 replay golden diff E2E."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = ROOT / "sessions"


def _import_run_session_replay() -> Callable[..., dict[str, Any]]:
    candidates = [
        ("pocore.runner", "run_session_replay"),
        ("pocore", "run_session_replay"),
    ]
    for mod_name, fn_name in candidates:
        try:
            mod = importlib.import_module(mod_name)
        except ImportError:
            continue
        fn = getattr(mod, fn_name, None)
        if callable(fn):
            return fn
    raise ImportError("Could not import run_session_replay")


def _canonicalize(obj: Any, *, parent_key: str = "") -> Any:
    if isinstance(obj, dict):
        return {k: _canonicalize(v, parent_key=k) for k, v in obj.items()}
    if isinstance(obj, list):
        items = [_canonicalize(i, parent_key=parent_key) for i in obj]
        if parent_key == "options":
            return sorted(items, key=lambda x: x.get("option_id", ""))
        if parent_key == "questions":
            return sorted(items, key=lambda x: (x.get("priority", 0), x.get("question_id", "")))
        if parent_key == "stakeholders":
            return sorted(items, key=lambda x: (x.get("name", ""), x.get("role", "")))
        return items
    return obj


def test_session_replay_matches_expected_json() -> None:
    run_session_replay = _import_run_session_replay()

    case_path = SESSIONS_DIR / "session_001_case.yaml"
    answers_path = SESSIONS_DIR / "session_001_answers.yaml"
    expected_path = SESSIONS_DIR / "session_001_expected.json"

    actual = run_session_replay(
        case_path,
        answers_path,
        seed=0,
        now="2026-02-22T00:00:00Z",
        deterministic=True,
    )

    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    assert _canonicalize(actual) == _canonicalize(expected)
