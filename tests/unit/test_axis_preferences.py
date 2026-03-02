from __future__ import annotations

import math

from po_core.axis.preferences import alignment, normalize_weights, parse_weights_str


def test_parse_weights_str_parses_valid_pairs_and_skips_invalid_tokens() -> None:
    parsed = parse_weights_str("safety:0.5, benefit:0.3,invalid,feasibility:0.2,bad:x")

    assert parsed == {"safety": 0.5, "benefit": 0.3, "feasibility": 0.2}


def test_normalize_weights_fills_missing_dims_with_zero() -> None:
    normalized = normalize_weights({"safety": 2.0}, ["safety", "benefit"])

    assert normalized == {"safety": 1.0, "benefit": 0.0}


def test_normalize_weights_falls_back_to_uniform_on_invalid_values() -> None:
    normalized_negative = normalize_weights(
        {"safety": -1.0, "benefit": 1.0}, ["safety", "benefit"]
    )
    normalized_nan = normalize_weights(
        {"safety": math.nan, "benefit": 1.0}, ["safety", "benefit"]
    )
    normalized_inf = normalize_weights(
        {"safety": math.inf, "benefit": 1.0}, ["safety", "benefit"]
    )

    assert normalized_negative == {"safety": 0.5, "benefit": 0.5}
    assert normalized_nan == {"safety": 0.5, "benefit": 0.5}
    assert normalized_inf == {"safety": 0.5, "benefit": 0.5}


def test_normalize_weights_falls_back_to_uniform_on_non_positive_sum() -> None:
    normalized = normalize_weights({}, ["safety", "benefit", "feasibility"])

    assert normalized == {
        "safety": 1.0 / 3.0,
        "benefit": 1.0 / 3.0,
        "feasibility": 1.0 / 3.0,
    }


def test_alignment_returns_dot_product() -> None:
    score = alignment(
        {"safety": 0.9, "benefit": 0.4, "feasibility": 0.2},
        {"safety": 0.5, "benefit": 0.25, "feasibility": 0.25},
    )

    assert score == 0.9 * 0.5 + 0.4 * 0.25 + 0.2 * 0.25
