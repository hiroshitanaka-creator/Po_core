from po_core.app.responsibility_engine import (
    build_responsibility_summary,
    sanitize_decision_owner,
)


def test_decision_owner_is_required_with_fallback() -> None:
    summary = build_responsibility_summary({"stakeholders": []}, values=[])
    assert summary["decision_owner"] == "意思決定者"
    assert summary["decision_owner"]


def test_forbidden_subjects_are_rejected() -> None:
    assert sanitize_decision_owner("Po_core") == "意思決定者"
    assert sanitize_decision_owner("ai") == "意思決定者"
    assert sanitize_decision_owner("the system") == "意思決定者"


def test_valid_human_owner_is_preserved() -> None:
    case = {
        "stakeholders": [
            {"name": "山田 太郎", "role": "申請者", "impact": "決定の実行責任を負う"}
        ]
    }
    summary = build_responsibility_summary(case, values=["安全"])
    assert summary["decision_owner"] == "山田 太郎"
