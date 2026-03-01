from __future__ import annotations

from po_core.deliberation.cards import ArgumentCard, CritiqueCard, SynthesisReport


def test_argument_card_roundtrip() -> None:
    card = ArgumentCard(
        card_id="arg-1",
        claim="Option A is safer",
        rationale="Lower downside risk",
        confidence=0.82,
        evidence=("historical data", "policy constraint"),
    )

    restored = ArgumentCard.from_dict(card.to_dict())
    assert restored == card


def test_critique_card_roundtrip() -> None:
    card = CritiqueCard(
        card_id="crt-1",
        target_argument_id="arg-1",
        concern="Benefit is under-estimated",
        severity="medium",
        suggestion="Include upside scenario analysis",
    )

    restored = CritiqueCard.from_dict(card.to_dict())
    assert restored == card


def test_synthesis_report_roundtrip() -> None:
    report = SynthesisReport(
        report_id="rep-1",
        summary="Option A currently dominates under defined constraints.",
        recommended_option_id="option_a",
        argument_cards=(
            ArgumentCard(
                card_id="arg-1",
                claim="Option A is safer",
                rationale="Lower downside risk",
                confidence=0.82,
                evidence=("historical data",),
            ),
        ),
        critique_cards=(
            CritiqueCard(
                card_id="crt-1",
                target_argument_id="arg-1",
                concern="Benefit is under-estimated",
                severity="medium",
                suggestion="Include upside scenario analysis",
            ),
        ),
    )

    restored = SynthesisReport.from_dict(report.to_dict())
    assert restored == report
