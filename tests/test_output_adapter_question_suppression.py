from po_core.app.output_adapter import adapt_to_schema


def _base_case() -> dict:
    return {
        "case_id": "case_test",
        "title": "問い抑制テスト",
        "problem": "A or B?",
        "constraints": ["budget"],
        "values": ["安全", "公平"],
        "stakeholders": [{"name": "本人", "role": "decision_owner", "impact": "high"}],
    }


def test_questions_are_suppressed_when_intention_gate_revises() -> None:
    case = {**_base_case(), "unknowns": ["コスト上限"]}
    run_result = {
        "status": "ok",
        "proposal": {"content": "fallback", "confidence": 0.3},
        "verdict": {"decision": "revise", "rule_ids": ["intention_mode_001"]},
    }

    output = adapt_to_schema(
        case,
        run_result,
        run_id="r-1",
        digest="0" * 64,
        now="2026-02-22T00:00:00Z",
    )

    assert output["questions"] == []


def test_questions_are_not_suppressed_when_unknowns_remain_and_intention_allows() -> (
    None
):
    case = {**_base_case(), "unknowns": ["意思決定期限"]}
    run_result = {
        "status": "ok",
        "proposal": {"content": "normal", "confidence": 0.8},
    }

    output = adapt_to_schema(
        case,
        run_result,
        run_id="r-2",
        digest="1" * 64,
        now="2026-02-22T00:00:00Z",
    )

    assert len(output["questions"]) >= 1
