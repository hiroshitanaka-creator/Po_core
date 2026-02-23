from pocore.engines.recommendation_v1 import recommend
from pocore.policy_v1 import TIME_PRESSURE_DAYS, UNKNOWN_BLOCK


def test_unknowns_at_or_above_unknown_block_returns_no_recommendation() -> None:
    result = recommend(
        case={},
        short_id="case_custom",
        features={"unknowns_count": UNKNOWN_BLOCK},
        options=[],
    )

    assert result["status"] == "no_recommendation"
    assert result["confidence"] == "high"


def test_deadline_pressure_with_unknowns_reduces_confidence() -> None:
    result = recommend(
        case={},
        short_id="case_custom",
        features={"unknowns_count": 1, "days_to_deadline": TIME_PRESSURE_DAYS},
        options=[],
    )

    assert result["status"] == "recommended"
    assert result["recommended_option_id"] == "opt_1"
    assert result["confidence"] == "low"


def test_unknowns_zero_uses_default_recommendation() -> None:
    result = recommend(
        case={},
        short_id="case_custom",
        features={"unknowns_count": 0, "days_to_deadline": 1},
        options=[],
    )

    assert result["status"] == "recommended"
    assert result["recommended_option_id"] == "opt_1"
    assert result["confidence"] == "medium"
