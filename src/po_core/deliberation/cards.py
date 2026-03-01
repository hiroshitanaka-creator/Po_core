"""Card schema for deliberation outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ArgumentCard:
    card_id: str
    claim: str
    rationale: str
    confidence: float
    evidence: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_id": self.card_id,
            "claim": self.claim,
            "rationale": self.rationale,
            "confidence": self.confidence,
            "evidence": list(self.evidence),
        }

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "ArgumentCard":
        evidence = data.get("evidence", [])
        return ArgumentCard(
            card_id=str(data["card_id"]),
            claim=str(data["claim"]),
            rationale=str(data.get("rationale", "")),
            confidence=float(data["confidence"]),
            evidence=tuple(str(item) for item in evidence),
        )


@dataclass(frozen=True)
class CritiqueCard:
    card_id: str
    target_argument_id: str
    concern: str
    severity: str
    suggestion: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_id": self.card_id,
            "target_argument_id": self.target_argument_id,
            "concern": self.concern,
            "severity": self.severity,
            "suggestion": self.suggestion,
        }

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "CritiqueCard":
        return CritiqueCard(
            card_id=str(data["card_id"]),
            target_argument_id=str(data["target_argument_id"]),
            concern=str(data["concern"]),
            severity=str(data["severity"]),
            suggestion=str(data.get("suggestion", "")),
        )


@dataclass(frozen=True)
class SynthesisReport:
    report_id: str
    summary: str
    recommended_option_id: str
    argument_cards: tuple[ArgumentCard, ...] = field(default_factory=tuple)
    critique_cards: tuple[CritiqueCard, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "summary": self.summary,
            "recommended_option_id": self.recommended_option_id,
            "argument_cards": [card.to_dict() for card in self.argument_cards],
            "critique_cards": [card.to_dict() for card in self.critique_cards],
        }

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "SynthesisReport":
        arg_raw = data.get("argument_cards", [])
        critique_raw = data.get("critique_cards", [])
        return SynthesisReport(
            report_id=str(data["report_id"]),
            summary=str(data["summary"]),
            recommended_option_id=str(data["recommended_option_id"]),
            argument_cards=tuple(
                ArgumentCard.from_dict(item) for item in arg_raw if isinstance(item, Mapping)
            ),
            critique_cards=tuple(
                CritiqueCard.from_dict(item)
                for item in critique_raw
                if isinstance(item, Mapping)
            ),
        )


__all__ = ["ArgumentCard", "CritiqueCard", "SynthesisReport"]
