from __future__ import annotations

from po_core.viewer.preference_view import apply_preference_view


def test_apply_preference_view_returns_deep_copy_and_overlay() -> None:
    original = {
        "axis": {
            "scoreboard": {
                "safety": {"mean": 0.8},
                "benefit": {"mean": 0.6},
                "feasibility": {"mean": 0.4},
            },
            "axis_vectors": [
                {
                    "author": "kant",
                    "axis_scores": {
                        "safety": 0.9,
                        "benefit": 0.4,
                        "feasibility": 0.6,
                    },
                },
                {
                    "author": "mill",
                    "axis_scores": {
                        "safety": 0.5,
                        "benefit": 0.8,
                        "feasibility": 0.7,
                    },
                },
            ],
        }
    }

    updated = apply_preference_view(
        original,
        weights={"safety": 0.5, "benefit": 0.3, "feasibility": 0.2},
    )

    assert "preference_view" not in original["axis"]
    preference_view = updated["axis"]["preference_view"]
    assert preference_view["weights_used"] == {
        "benefit": 0.3,
        "feasibility": 0.2,
        "safety": 0.5,
    }
    assert preference_view["ranked_authors"] == ["kant", "mill"]
    assert (
        preference_view["alignment_by_author"]["kant"]
        > preference_view["alignment_by_author"]["mill"]
    )


def test_apply_preference_view_infers_dims_from_axis_vectors() -> None:
    updated = apply_preference_view(
        {
            "axis": {
                "axis_vectors": [
                    {"author": "a", "axis_scores": {"x": 1.0, "y": 0.0}},
                    {"author": "b", "axis_scores": {"x": 0.0, "y": 1.0}},
                ]
            }
        },
        weights={"x": 1.0},
    )

    assert updated["axis"]["preference_view"]["weights_used"] == {"x": 1.0, "y": 0.0}
    assert updated["axis"]["preference_view"]["ranked_authors"] == ["a", "b"]
