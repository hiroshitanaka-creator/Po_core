from __future__ import annotations

from pocore.engines import ethics_v1


def test_ethics_ruleset_fires_multiple_rules_from_features() -> None:
    rules = ethics_v1.rules_fired_for(
        short_id="case_777",
        features={
            "constraint_conflict": True,
            "unknowns_count": 2,
            "stakeholders_count": 3,
            "days_to_deadline": 5,
        },
    )

    assert rules == [
        "ETH_CONSTRAINT_CONFLICT_DISCLOSURE",
        "ETH_NO_OVERCLAIM_UNKNOWN",
        "ETH_STAKEHOLDER_CONSENT",
        "ETH_TIME_PRESSURE_SAFETY",
    ]


def test_ethics_ruleset_fires_only_applicable_rules() -> None:
    rules = ethics_v1.rules_fired_for(
        short_id="case_778",
        features={
            "constraint_conflict": False,
            "unknowns_count": 0,
            "stakeholders_count": 2,
            "days_to_deadline": None,
        },
    )

    assert rules == ["ETH_STAKEHOLDER_CONSENT"]
