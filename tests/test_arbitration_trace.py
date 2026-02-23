from pocore.orchestrator import run_case


def _compose_metrics(output: dict) -> dict:
    compose_step = next(step for step in output["trace"]["steps"] if step["name"] == "compose_output")
    return compose_step.get("metrics", {})


def test_trace_compose_output_includes_arbitration_code_and_policy_snapshot_for_generic_case() -> None:
    case = {
        "case_id": "case_custom_arbitration",
        "title": "arbitration trace check",
        "dilemma": "test",
        "values": ["safety"],
        "unknowns": ["要件未確定", "工数見積もり不足", "依存先SLA不明", "運用体制未定"],
        "stakeholders": [{"role": "team"}],
        "deadline": "2026-03-01",
        "constraints": [],
    }

    output = run_case(
        case,
        now="2026-02-22T00:00:00Z",
        seed=0,
        deterministic=True,
    )

    metrics = _compose_metrics(output)
    assert metrics["arbitration_code"] == "BLOCK_UNKNOWN"
    assert metrics["policy_snapshot"] == {
        "UNKNOWN_BLOCK": 4,
        "TIME_PRESSURE_DAYS": 7,
    }


def test_trace_compose_output_arbitration_metrics_not_added_to_frozen_case() -> None:
    case = {
        "case_id": "case_001",
        "title": "frozen",
        "dilemma": "frozen",
        "values": ["v"],
        "context": {},
    }

    output = run_case(
        case,
        now="2026-02-22T00:00:00Z",
        seed=0,
        deterministic=True,
    )

    compose_step = next(step for step in output["trace"]["steps"] if step["name"] == "compose_output")
    assert "metrics" not in compose_step
