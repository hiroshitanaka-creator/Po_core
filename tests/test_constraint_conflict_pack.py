from __future__ import annotations

from pocore.engines import generator_stub, question_v1


CONFLICT_FEATURES = {
    "constraint_conflict": True,
    "time_min_hours_per_week": 20,
    "time_max_hours_per_week": 5,
    "unknowns_count": 0,
    "unknowns_items": [],
    "stakeholders_count": 1,
}


def test_constraint_conflict_questions_are_deterministic_and_capped() -> None:
    questions = question_v1.generate({}, short_id="case_custom", features=CONFLICT_FEATURES)

    assert [q["question_id"] for q in questions] == [
        "q_conflict_1",
        "q_conflict_2",
        "q_conflict_3",
        "q_conflict_4",
        "q_conflict_5",
    ]
    assert [q["priority"] for q in questions] == [1, 1, 2, 2, 3]
    assert len(questions) == 5


def test_constraint_conflict_plan_protocol_order_and_cap() -> None:
    options = generator_stub.generate_options({}, short_id="case_custom", features=CONFLICT_FEATURES)

    plan = options[0]["action_plan"]
    assert len(plan) == 5
    assert plan[0]["step"].startswith("制約矛盾サマリ")
    assert "要求は週20h以上" in plan[0]["step"]
    assert "絶対制約" in plan[1]["step"]
    assert "可逆な最小スコープ" in plan[2]["step"]


def test_constraint_conflict_plan_rule_id_fired() -> None:
    fired = generator_stub.rules_fired_for(features=CONFLICT_FEATURES)

    assert fired == [generator_stub.PLAN_CONSTRAINT_CONFLICT_PROTOCOL_V1]
