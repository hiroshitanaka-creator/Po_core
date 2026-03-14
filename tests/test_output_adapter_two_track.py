from po_core.app.output_adapter import adapt_to_schema


def _base_run_result() -> dict:
    return {
        "status": "ok",
        "proposal": {"content": "主要案", "confidence": 0.7},
    }


def test_urgent_case_uses_two_track_plan_from_case_now() -> None:
    """REQ-PLAN-001: urgent case routes opt_001.action_plan to Two-Track."""
    case = {
        "case_id": "case_two_track_routing",
        "title": "二系統テスト",
        "problem": "迅速な意思決定が必要",
        "constraints": ["コスト最小化"],
        "values": ["自律", "安全"],
        "unknowns": ["予算上限", "法的リスク"],
        "deadline": "2026-04-03",
        # Business-time reference for urgency judgement (20 days to deadline)
        "now": "2026-03-14T00:00:00Z",
    }

    output = adapt_to_schema(
        case,
        _base_run_result(),
        run_id="r-two-track",
        digest="2" * 64,
        # Metadata timestamp intentionally different from case.now.
        now="2026-03-03T00:00:00Z",
    )

    steps = [item["step"] for item in output["options"][0]["action_plan"]]
    assert any("Track A" in step for step in steps)
    assert any("Track B" in step for step in steps)


def test_values_clarification_keeps_higher_priority_than_two_track() -> None:
    """REQ-VALUES-001 precedence: values-empty uses VC action plan first."""
    case = {
        "case_id": "case_vc_priority",
        "title": "価値観未定義の緊急ケース",
        "problem": "価値観が未整理",
        "constraints": ["迅速対応"],
        "values": [],
        "unknowns": ["影響範囲", "関係者合意"],
        "deadline": "2026-04-03",
        "now": "2026-03-14T00:00:00Z",
    }

    output = adapt_to_schema(
        case,
        _base_run_result(),
        run_id="r-vc-priority",
        digest="3" * 64,
        now="2026-03-03T00:00:00Z",
    )

    steps = [item["step"] for item in output["options"][0]["action_plan"]]
    assert steps
    assert all("Track " not in step for step in steps)
    assert any("ステップ" in step for step in steps)
