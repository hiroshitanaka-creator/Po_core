from __future__ import annotations

import importlib
from typing import Any

from po_core.philosophers.aristotle import Aristotle
from po_core.philosophers.base import ArgumentCard, Context
from po_core.philosophers.manifest import SPECS


TEST_PROMPT = "I need a fair and practical plan for a risky team decision."


def _load_philosopher(spec: Any) -> Any:
    module = importlib.import_module(spec.module)
    cls = getattr(module, spec.symbol)
    return cls()


def test_propose_card_has_required_fields() -> None:
    phil = Aristotle()
    card = phil.propose_card(Context.from_prompt(TEST_PROMPT))

    assert isinstance(card, ArgumentCard)
    assert isinstance(card.philosopher, str) and card.philosopher
    assert isinstance(card.perspective, str) and card.perspective
    assert isinstance(card.stance, str) and card.stance
    assert isinstance(card.claims, list)
    assert isinstance(card.assumptions, list)
    assert isinstance(card.risks, list)
    assert isinstance(card.questions, list)
    assert isinstance(card.actions, list)
    assert isinstance(card.axis_scores_self, dict)
    assert isinstance(card.confidence, float)


def test_aristotle_axis_scores_self_populated_from_axis_spec() -> None:
    phil = Aristotle()
    axis_spec = {
        "version": "v1",
        "dimensions": [
            {"id": "prudence"},
            {"id": "ethical_balance"},
            {"id": "practical_actionability"},
        ],
    }

    card = phil.propose_card(Context.from_prompt(TEST_PROMPT), axis_spec=axis_spec)

    assert len(card.axis_scores_self) >= 1
    assert "prudence" in card.axis_scores_self


def test_all_reason_based_philosophers_can_propose_card() -> None:
    for spec in SPECS:
        philosopher = _load_philosopher(spec)
        if not hasattr(philosopher, "reason"):
            continue

        card = philosopher.propose_card(Context.from_prompt("What is wisdom?"))
        assert isinstance(card, ArgumentCard)
        assert isinstance(card.claims, list)
