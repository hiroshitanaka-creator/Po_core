from pocore.parse_input import extract_features
from pocore.utils import detect_constraint_conflict


def test_constraint_conflict_detects_contradictory_weekly_hours() -> None:
    case = {
        "constraints": [
            "副業に週20時間以上は必要",
            "副業は週5時間以内に抑える",
        ]
    }

    result = detect_constraint_conflict(case)

    assert result["constraint_conflict"] is True
    assert result["time_min_hours_per_week"] == 20
    assert result["time_max_hours_per_week"] == 5


def test_constraint_conflict_false_when_hours_are_consistent() -> None:
    case = {
        "constraints": [
            "副業に週5時間以上は確保する",
            "副業は週20時間以内に抑える",
        ]
    }

    result = detect_constraint_conflict(case)

    assert result["constraint_conflict"] is False
    assert result["time_min_hours_per_week"] == 5
    assert result["time_max_hours_per_week"] == 20


def test_constraint_conflict_false_with_only_one_sided_bound() -> None:
    case = {"constraints": ["副業は週8時間以内にする"]}

    result = detect_constraint_conflict(case)

    assert result["constraint_conflict"] is False
    assert result["time_min_hours_per_week"] is None
    assert result["time_max_hours_per_week"] == 8


def test_extract_features_exposes_constraint_conflict_flag() -> None:
    case = {
        "constraints": [
            "学習は週20時間以上",
            "学習は週5時間以内",
        ],
        "unknowns": ["A", "B"],
    }

    features = extract_features(case)

    assert features["constraint_conflict"] is True
    assert features["unknowns_count"] == 2
