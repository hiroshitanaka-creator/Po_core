from po_core.deliberation.synthesis import ArgumentCard, AxisSpec, SynthesisEngine


def test_synthesis_engine_scoreboard_and_open_questions() -> None:
    engine = SynthesisEngine(consensus_top_n=3)
    axis = AxisSpec(dimensions=["safety", "speed"])
    cards = [
        ArgumentCard(
            card_id="c1",
            stance="pro",
            claims=["Enable staged rollout", "Measure impact"],
            axis_scores={"safety": 0.2, "speed": 0.8},
            confidence=0.5,
            questions=["Who audits outcomes?", "What is rollback criteria?"],
        ),
        ArgumentCard(
            card_id="c2",
            stance="con",
            claims=["Enable staged rollout"],
            axis_scores={"safety": 0.8, "speed": 0.4},
            confidence=1.0,
            questions=["Who audits outcomes?"],
        ),
        ArgumentCard(
            card_id="c3",
            stance="pro",
            claims=["Enable staged rollout", "Need explicit guardrails"],
            axis_scores={"safety": 0.6, "speed": 0.5},
            confidence=1.5,
            questions=["How do we monitor drift?"],
        ),
    ]

    report = engine.synthesize(axis_spec=axis, cards=cards)

    assert report.stance_distribution == {"con": 1, "pro": 2}
    assert report.scoreboard["safety"].mean == 0.6
    assert report.scoreboard["safety"].variance == 0.04
    assert report.scoreboard["safety"].samples == 3

    assert report.open_questions == [
        "Who audits outcomes?",
        "What is rollback criteria?",
        "How do we monitor drift?",
    ]

    # Sample JSON (for future API shape discussion)
    sample_json = report.to_dict()
    assert sample_json["consensus_claims"][0] == {
        "claim": "Enable staged rollout",
        "count": 3,
    }
    assert sample_json["scoreboard"]["speed"] == {
        "mean": 0.516667,
        "variance": 0.018056,
        "samples": 3,
    }
