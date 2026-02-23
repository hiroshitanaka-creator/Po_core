from pocore.tracer import build_trace


def _parse_step(trace: dict) -> dict:
    return next(step for step in trace["steps"] if step["name"] == "parse_input")


def test_build_trace_generic_parse_input_metrics_include_observability_values():
    trace = build_trace(
        short_id="case_123",
        created_at="2026-02-22T00:00:00Z",
        options_count=2,
        questions_count=1,
        features={
            "unknowns_count": 3,
            "stakeholders_count": 2,
            "days_to_deadline": 5,
            "constraint_conflict": True,
        },
        rules_fired=[
            "ETH_CONSTRAINT_CONFLICT_DISCLOSURE",
            "ETH_NO_OVERCLAIM_UNKNOWN",
        ],
    )

    metrics = _parse_step(trace)["metrics"]
    assert metrics["unknowns_count"] == 3
    assert metrics["stakeholders_count"] == 2
    assert metrics["days_to_deadline"] == 5
    assert metrics["constraint_conflict"] is True
    assert metrics["rules_fired"] == [
        "ETH_CONSTRAINT_CONFLICT_DISCLOSURE",
        "ETH_NO_OVERCLAIM_UNKNOWN",
    ]


def test_build_trace_generic_omits_days_to_deadline_when_unknown():
    trace = build_trace(
        short_id="case_124",
        created_at="2026-02-22T00:00:00Z",
        options_count=1,
        questions_count=0,
        features={"unknowns_count": 1, "stakeholders_count": 0, "days_to_deadline": None},
    )

    metrics = _parse_step(trace)["metrics"]
    assert metrics["unknowns_count"] == 1
    assert metrics["stakeholders_count"] == 0
    assert "days_to_deadline" not in metrics


def test_build_trace_generic_compose_output_metrics_include_rules_fired() -> None:
    trace = build_trace(
        short_id="case_125",
        created_at="2026-02-22T00:00:00Z",
        options_count=2,
        questions_count=0,
        features={"unknowns_count": 0, "stakeholders_count": 0},
        rules_fired=["ETH_STAKEHOLDER_CONSENT"],
        arbitration_code="REC_A",
    )

    compose_step = next(step for step in trace["steps"] if step["name"] == "compose_output")
    assert compose_step["metrics"]["rules_fired"] == ["ETH_STAKEHOLDER_CONSENT"]
    assert compose_step["metrics"]["arbitration_code"] == "REC_A"


def test_build_trace_frozen_case_001_and_009_steps_unchanged():
    created_at = "2026-02-22T00:00:00Z"

    trace_001 = build_trace(
        short_id="case_001",
        created_at=created_at,
        options_count=99,
        questions_count=99,
        features={
            "scenario_profile": "job_change_transition_v1",
            "unknowns_count": 999,
            "stakeholders_count": 999,
            "days_to_deadline": 999,
            "constraint_conflict": True,
        },
    )
    assert trace_001["steps"] == [
        {
            "name": "parse_input",
            "started_at": "2026-02-22T00:00:00Z",
            "ended_at": "2026-02-22T00:00:01Z",
            "summary": "入力を正規化し、不明点を抽出した",
        },
        {
            "name": "generate_options",
            "started_at": "2026-02-22T00:00:01Z",
            "ended_at": "2026-02-22T00:00:02Z",
            "summary": "2案を生成した",
            "metrics": {"options": 99},
        },
        {
            "name": "compose_output",
            "started_at": "2026-02-22T00:00:02Z",
            "ended_at": "2026-02-22T00:00:03Z",
            "summary": "推奨・反証・代替案を含む出力を組み立てた",
        },
    ]

    trace_009 = build_trace(
        short_id="case_009",
        created_at=created_at,
        options_count=99,
        questions_count=99,
        features={
            "scenario_profile": "values_clarification_v1",
            "unknowns_count": 999,
            "stakeholders_count": 999,
            "days_to_deadline": 999,
            "constraint_conflict": True,
        },
    )
    assert trace_009["steps"] == [
        {
            "name": "parse_input",
            "started_at": "2026-02-22T00:00:00Z",
            "ended_at": "2026-02-22T00:00:01Z",
            "summary": "valuesが空であることを検出した",
        },
        {
            "name": "question_layer",
            "started_at": "2026-02-22T00:00:01Z",
            "ended_at": "2026-02-22T00:00:02Z",
            "summary": "軸を作るための質問を生成した",
            "metrics": {"questions": 99},
        },
        {
            "name": "compose_output",
            "started_at": "2026-02-22T00:00:02Z",
            "ended_at": "2026-02-22T00:00:03Z",
            "summary": "推奨を保留し、次ステップを提示した",
        },
    ]
