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


def test_unknowns_items_normalization_order_and_limit() -> None:
    case = {
        "unknowns": [
            "  first  ",
            "",
            "   ",
            42,
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "ninth",
            "tenth",
            "eleventh",
            "twelfth",
        ]
    }

    features = extract_features(case)

    assert features["unknowns_items"] == [
        "first",
        "42",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
        "eleventh",
        "twelfth",
    ]


def test_stakeholder_roles_normalization_dedup_and_limit() -> None:
    case = {
        "stakeholders": [
            {"role": "  owner "},
            {"role": ""},
            {"role": "owner"},
            {"role": "developer"},
            {"name": "missing-role"},
            "not-dict",
            {"role": "qa"},
            {"role": 99},
            {"role": "support"},
            {"role": "legal"},
            {"role": "ops"},
            {"role": "sales"},
            {"role": "finance"},
            {"role": "marketing"},
            {"role": "security"},
            {"role": "extra"},
        ]
    }

    features = extract_features(case)

    assert features["stakeholder_roles"] == [
        "owner",
        "developer",
        "qa",
        "99",
        "support",
        "legal",
        "ops",
        "sales",
        "finance",
        "marketing",
    ]


def test_days_to_deadline_with_date_string() -> None:
    case = {"deadline": "2026-03-01"}

    features = extract_features(case, now="2026-02-22T00:00:00Z")

    assert features["deadline_present"] is True
    assert features["deadline_iso"] == "2026-03-01"
    assert features["days_to_deadline"] == 7


def test_days_to_deadline_with_datetime_string() -> None:
    case = {"deadline": "2026-03-01T23:59:59Z"}

    features = extract_features(case, now="2026-02-22T09:30:00Z")

    assert features["deadline_present"] is True
    assert features["deadline_iso"] == "2026-03-01T23:59:59Z"
    assert features["days_to_deadline"] == 7


def test_days_to_deadline_invalid_deadline_returns_none_values() -> None:
    case = {"deadline": "2026/03/01"}

    features = extract_features(case, now="2026-02-22T00:00:00Z")

    assert features["deadline_present"] is True
    assert features["deadline_iso"] is None
    assert features["days_to_deadline"] is None


def test_extract_features_reads_scenario_profile_from_extensions() -> None:
    case = {"extensions": {"scenario_profile": "job_change_transition_v1"}}

    features = extract_features(case)

    assert features["scenario_profile"] == "job_change_transition_v1"
