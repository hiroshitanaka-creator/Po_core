from __future__ import annotations

from pocore.engines import question_v1, responsibility_v1

BASE_CASE = {
    "case_id": "case_externality_unit",
    "title": "外部性がある意思決定",
    "problem": "複数関係者への影響がある意思決定をどう進めるか",
    "constraints": ["法令は順守する"],
    "values": ["公正", "説明責任"],
    "stakeholders": [
        {"name": "自分", "role": "企画責任者", "impact": "意思決定の説明責任を負う"},
        {"name": "顧客", "role": "利用者", "impact": "運用変更の影響を受ける"},
        {"name": "現場チーム", "role": "実行担当", "impact": "運用負荷が増減する"},
    ],
}


def test_responsibility_adds_externality_checklist_for_many_stakeholders() -> None:
    options = [
        {
            "option_id": "opt_1",
            "responsibility_review": {},
        }
    ]

    _, summary = responsibility_v1.apply(
        BASE_CASE,
        short_id="case_custom",
        features={"stakeholders_count": 3},
        options=options,
    )

    assert summary["decision_owner"] == "未確定（要確認）"
    assert any(
        "RESP_STAKEHOLDER_CONSENT_CHECK" in item
        for item in summary["consent_considerations"]
    )
    assert any(
        "RESP_IMPACT_SCOPE" in item for item in summary["consent_considerations"]
    )
    assert "決裁者/意思決定者" in summary["accountability_notes"]


def test_questions_add_high_priority_stakeholder_prompts() -> None:
    questions = question_v1.generate(
        BASE_CASE,
        short_id="case_custom",
        features={"stakeholders_count": 3},
    )

    question_ids = [q["question_id"] for q in questions]

    assert question_ids == [
        "q_stakeholder_1",
        "q_stakeholder_2",
        "q_stakeholder_3",
        "q_stakeholder_4",
    ]
    assert all(q["priority"] == 1 for q in questions)
