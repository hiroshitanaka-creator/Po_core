from __future__ import annotations

from po_core.axis.scoring import score_text
from po_core.axis.spec import load_axis_spec


def test_score_text_safety_emphasis() -> None:
    spec = load_axis_spec()
    text = "This plan has legal risk and potential harm; safety must come first."

    scores = score_text(text, spec)

    assert set(scores.keys()) == {"safety", "benefit", "feasibility"}
    assert scores["safety"] > scores["benefit"]
    assert scores["safety"] > scores["feasibility"]


def test_score_text_feasibility_emphasis() -> None:
    spec = load_axis_spec()
    text = "現実的な手順と実装計画を明示し、工数と予算の見積もりを出す。"

    scores = score_text(text, spec)

    assert set(scores.keys()) == {"safety", "benefit", "feasibility"}
    assert scores["feasibility"] > scores["safety"]
    assert scores["feasibility"] > scores["benefit"]
