from __future__ import annotations

from pocore.engines import ethics_v1


def test_ethics_guardrails_v1_feature_reactions_for_generic_case() -> None:
    case = {"case_id": "case_777_generic"}
    features = {
        "constraint_conflict": False,
        "unknowns_count": 2,
        "stakeholders_count": 3,
        "days_to_deadline": 3,
    }
    options = [
        {"option_id": "opt_1", "label": "A"},
        {"option_id": "opt_2", "label": "B"},
    ]

    reviewed_options, summary = ethics_v1.apply(
        case,
        short_id="case_777",
        features=features,
        options=options,
    )

    assert "前提と不確実性を明示する" in summary["guardrails"]
    assert "関係者への影響と同意を考慮する" in summary["guardrails"]
    assert "時間圧力下でも検証を省略しない" in summary["guardrails"]

    tensions = {item["tension"] for item in summary["tradeoffs"]}
    assert "自己決定と外部性/公正の緊張" in tensions
    assert "速度と安全（nonmaleficence）の緊張" in tensions

    for option in reviewed_options:
        review = option["ethics_review"]
        assert "前提と不確実性を明示する" in review["concerns"]
        assert "justice" in review["principles_applied"]
        assert "autonomy" in review["principles_applied"]
        assert "nonmaleficence" in review["principles_applied"]


def test_ethics_guardrails_v1_only_applies_to_generic_path() -> None:
    options = [{"option_id": "opt_1"}, {"option_id": "opt_2"}]

    _, summary = ethics_v1.apply(
        {"case_id": "case_001_job_change"},
        short_id="case_001",
        features={
            "scenario_profile": "job_change_transition_v1",
            "unknowns_count": 9,
            "stakeholders_count": 9,
            "days_to_deadline": 1,
        },
        options=options,
    )

    assert "関係者への影響と同意を考慮する" not in summary["guardrails"]
    assert "時間圧力下でも検証を省略しない" not in summary["guardrails"]
