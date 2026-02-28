from __future__ import annotations

from pocore.engines import generator_stub, question_v1


def test_values_clarification_questions_are_capped_and_deterministic() -> None:
    questions = question_v1.generate(
        {},
        short_id="case_custom",
        features={
            "values_empty": True,
            "unknowns_count": 0,
            "stakeholders_count": 0,
            "days_to_deadline": None,
        },
    )

    assert len(questions) == 5
    assert [q["question_id"] for q in questions] == [
        "q_values_1",
        "q_values_axis_1",
        "q_values_axis_2",
        "q_values_axis_3",
        "q_values_axis_4",
    ]
    assert [q["priority"] for q in questions] == [1, 1, 2, 2, 3]


def test_values_clarification_plan_is_emitted_with_fixed_steps() -> None:
    options = generator_stub.generate_options(
        {},
        short_id="case_custom",
        features={"values_empty": True},
    )

    steps = [item["step"] for item in options[0]["action_plan"]]
    assert len(steps) == 5
    assert steps[0].startswith("10分タイマーをセット")
    assert "上位3つ" in steps[1]
    assert "再評価する時刻" in steps[4]


def test_values_clarification_planning_rule_is_observable() -> None:
    assert generator_stub.rules_fired_for(features={"values_empty": True}) == [
        "PLAN_VALUES_CLARIFICATION_PACK_V1"
    ]
