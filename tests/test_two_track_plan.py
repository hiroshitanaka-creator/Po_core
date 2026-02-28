from __future__ import annotations

from pocore.engines import generator_stub


def test_two_track_plan_emitted_under_time_pressure_with_unknowns() -> None:
    options = generator_stub.generate_options(
        {},
        short_id="case_900",
        features={
            "unknowns_count": 2,
            "unknowns_items": ["法令確認の未完了", "運用体制の担当未確定"],
            "days_to_deadline": -4,
        },
    )

    plan = options[0]["action_plan"]
    steps = [item["step"] for item in plan]

    assert steps[0].startswith("[Track A]")
    assert any(step.startswith("[Track B]") for step in steps)



def test_two_track_plan_reflects_unknown_items_in_track_b_with_deterministic_order() -> None:
    unknowns = ["監査ログの欠落範囲", "通知対象ユーザー数", "契約上の通知期限"]
    options = generator_stub.generate_options(
        {},
        short_id="case_901",
        features={
            "unknowns_count": len(unknowns),
            "unknowns_items": unknowns,
            "days_to_deadline": -5,
        },
    )

    plan = options[0]["action_plan"]
    track_a = [item["step"] for item in plan if item["step"].startswith("[Track A]")]
    track_b = [item["step"] for item in plan if item["step"].startswith("[Track B]")]

    assert track_a
    assert track_b
    assert plan[len(track_a)]["step"].startswith("[Track B]")

    for item in unknowns:
        assert any(item in step for step in track_b)
