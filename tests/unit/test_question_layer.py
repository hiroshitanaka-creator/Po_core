from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from po_core.app.question_layer import build_questions


def test_question_layer_emits_questions_when_unknowns_exist() -> None:
    questions = build_questions(["法務確認", "費用見積"])

    assert len(questions) == 2
    assert [q["question_id"] for q in questions] == ["q_001", "q_002"]
    assert questions[0]["priority"] == 1


def test_question_layer_returns_empty_when_unknowns_absent() -> None:
    assert build_questions([]) == []


def test_question_layer_output_conforms_to_schema() -> None:
    schema = json.loads(Path("docs/spec/output_schema_v1.json").read_text())
    question_schema = schema["$defs"]["question"]

    questions = build_questions(["データ鮮度"])
    validator = jsonschema.Draft202012Validator(question_schema)
    for item in questions:
        validator.validate(item)
