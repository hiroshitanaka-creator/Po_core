from __future__ import annotations

from pocore.engines import question_v1


def test_questions_v2_prioritizes_deadline_and_unknowns_with_cap() -> None:
    case = {"unknowns": [f"u{i}" for i in range(1, 8)]}
    features = {
        "unknowns_count": 7,
        "unknowns_items": [f"u{i}" for i in range(1, 8)],
        "days_to_deadline": 1,
        "stakeholders_count": 3,
    }

    questions = question_v1.generate(case, short_id="case_custom", features=features)

    assert len(questions) == 5
    assert [q["question_id"] for q in questions] == [
        "q_deadline_flex_1",
        "q_temporary_scope_1",
        "q_stakeholder_1",
        "q_unknown_1",
        "q_stakeholder_2",
    ]
    assert [q["priority"] for q in questions] == [1, 1, 2, 2, 3]


def test_questions_v2_converts_unknown_items_deterministically() -> None:
    case = {
        "unknowns": ["法務確認", "費用見積", "運用体制"],
    }
    features = {
        "unknowns_count": 3,
        "unknowns_items": ["法務確認", "費用見積", "運用体制"],
        "days_to_deadline": 10,
        "stakeholders_count": 1,
    }

    questions = question_v1.generate(case, short_id="case_custom", features=features)

    assert [q["question_id"] for q in questions] == [
        "q_unknown_1",
        "q_unknown_2",
        "q_unknown_3",
        "q_unknowns_bundle_1",
    ]
    assert questions[0]["question"] == (
        "不明点『法務確認』を検証するため、最短で確認できる事実は何か？"
    )
    assert questions[3]["priority"] == 2
