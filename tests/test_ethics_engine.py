from __future__ import annotations

from po_core.app.ethics_engine import build_ethics_summary


def test_ethics_summary_guarantees_minimum_principles() -> None:
    case = {
        "case_id": "case_ethics_001",
        "title": "価値観が未定義でも最低原則を満たす",
        "values": [],
    }

    ethics = build_ethics_summary(case)

    assert len(ethics["principles_used"]) >= 2


def test_ethics_summary_emits_tradeoff_for_multi_value_case() -> None:
    case = {
        "case_id": "case_ethics_002",
        "title": "価値衝突あり",
        "values": ["公平性", "スピード"],
    }

    ethics = build_ethics_summary(case)

    assert ethics["tradeoffs"], "複数価値がある場合、tradeoffs は非空であるべき"
    assert ethics["tradeoffs"][0]["between"] == ["公平性", "スピード"]


def test_ethics_summary_maps_revise_to_allow_with_repair() -> None:
    case = {
        "case_id": "case_ethics_003",
        "title": "判定マッピング",
        "values": ["自律", "安全"],
    }

    ethics = build_ethics_summary(case, run_result={"verdict": {"decision": "REVISE"}})

    assert ethics["wethics_verdict"] == "ALLOW_WITH_REPAIR"
