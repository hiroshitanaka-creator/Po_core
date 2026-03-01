"""Structured synthesis for deliberation outputs.

This module intentionally keeps synthesis deterministic and explainable:
- aggregate simple statistics first
- enumerate artifacts (claims/questions) without heuristic-heavy inference
- avoid model-dependent "magic" transformations
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Dict, Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class AxisSpec:
    """Axis schema used for scoreboard aggregation."""

    dimensions: List[str]


@dataclass(frozen=True)
class ArgumentCard:
    """Minimal argument unit produced by a philosopher/proposal."""

    card_id: str
    stance: str
    claims: List[str] = field(default_factory=list)
    axis_scores: Mapping[str, float] = field(default_factory=dict)
    confidence: float = 1.0
    questions: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CritiqueCard:
    """Optional critique unit that can contribute questions."""

    card_id: str
    target_card_id: str
    questions: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ScoreboardEntry:
    """Weighted statistics for a single axis dimension."""

    mean: float
    variance: float
    samples: int


@dataclass(frozen=True)
class SynthesisReport:
    """Deterministic synthesis product for future structured APIs."""

    stance_distribution: Dict[str, int]
    consensus_claims: List[Dict[str, int | str]]
    disagreements: List[Dict[str, float | str | int]]
    open_questions: List[str]
    scoreboard: Dict[str, ScoreboardEntry]

    def to_dict(self) -> Dict[str, object]:
        """JSON-friendly form for logging/debugging."""
        scoreboard = {axis: asdict(entry) for axis, entry in self.scoreboard.items()}
        return {
            "stance_distribution": dict(self.stance_distribution),
            "consensus_claims": list(self.consensus_claims),
            "disagreements": list(self.disagreements),
            "open_questions": list(self.open_questions),
            "scoreboard": scoreboard,
            "axis_scoreboard": scoreboard,
        }


class SynthesisEngine:
    """Aggregate multiple cards into a deterministic synthesis report."""

    def __init__(
        self,
        *,
        consensus_top_n: int = 5,
        disagreement_top_n: int = 3,
        variance_alert_threshold: float = 0.04,
    ):
        self.consensus_top_n = max(1, consensus_top_n)
        self.disagreement_top_n = max(1, disagreement_top_n)
        self.variance_alert_threshold = max(0.0, variance_alert_threshold)

    def synthesize(
        self,
        axis_spec: AxisSpec,
        cards: list[ArgumentCard],
        critiques: list[CritiqueCard] | None = None,
    ) -> SynthesisReport:
        stance_distribution = self._stance_distribution(cards)
        scoreboard = self._scoreboard(axis_spec, cards)
        consensus_claims = self._consensus_claims(cards)
        disagreements = self._disagreements(stance_distribution, scoreboard)
        open_questions = self._open_questions(cards, critiques or [])

        return SynthesisReport(
            stance_distribution=stance_distribution,
            consensus_claims=consensus_claims,
            disagreements=disagreements,
            open_questions=open_questions,
            scoreboard=scoreboard,
        )

    def _stance_distribution(self, cards: Sequence[ArgumentCard]) -> Dict[str, int]:
        counts = Counter((c.stance or "unknown") for c in cards)
        return dict(sorted(counts.items(), key=lambda x: x[0]))

    def _consensus_claims(
        self, cards: Sequence[ArgumentCard]
    ) -> List[Dict[str, int | str]]:
        claim_counts: Counter[str] = Counter()
        for card in cards:
            # per-card duplicate claims are collapsed to avoid accidental over-weighting
            unique_claims = {claim.strip() for claim in card.claims if claim.strip()}
            claim_counts.update(unique_claims)

        ranked = sorted(claim_counts.items(), key=lambda x: (-x[1], x[0]))
        return [
            {"claim": claim, "count": count}
            for claim, count in ranked[: self.consensus_top_n]
        ]

    def _scoreboard(
        self,
        axis_spec: AxisSpec,
        cards: Sequence[ArgumentCard],
    ) -> Dict[str, ScoreboardEntry]:
        rows: Dict[str, List[tuple[float, float]]] = {
            axis: [] for axis in axis_spec.dimensions
        }

        for card in cards:
            weight = max(0.0, float(card.confidence))
            for axis in axis_spec.dimensions:
                if axis not in card.axis_scores:
                    continue
                rows[axis].append((float(card.axis_scores[axis]), weight))

        board: Dict[str, ScoreboardEntry] = {}
        for axis in axis_spec.dimensions:
            values = rows.get(axis, [])
            if not values:
                board[axis] = ScoreboardEntry(mean=0.0, variance=0.0, samples=0)
                continue

            w_sum = sum(w for _, w in values)
            if w_sum <= 0:
                mean = sum(v for v, _ in values) / len(values)
                variance = sum((v - mean) ** 2 for v, _ in values) / len(values)
            else:
                mean = sum(v * w for v, w in values) / w_sum
                variance = sum(w * (v - mean) ** 2 for v, w in values) / w_sum

            board[axis] = ScoreboardEntry(
                mean=round(mean, 6),
                variance=round(variance, 6),
                samples=len(values),
            )

        return board

    def _disagreements(
        self,
        stance_distribution: Mapping[str, int],
        scoreboard: Mapping[str, ScoreboardEntry],
    ) -> List[Dict[str, float | str | int]]:
        rows: List[Dict[str, float | str | int]] = []
        if len([k for k, v in stance_distribution.items() if v > 0]) > 1:
            rows.append(
                {
                    "type": "stance_split",
                    "n_stances": len(stance_distribution),
                    "largest_group": (
                        max(stance_distribution.values()) if stance_distribution else 0
                    ),
                }
            )

        sorted_axis = sorted(scoreboard.items(), key=lambda x: (-x[1].variance, x[0]))
        for axis, entry in sorted_axis[: self.disagreement_top_n]:
            if entry.samples >= 2 and entry.variance >= self.variance_alert_threshold:
                rows.append(
                    {
                        "type": "axis_variance",
                        "axis": axis,
                        "variance": entry.variance,
                        "samples": entry.samples,
                    }
                )
        return rows

    def _open_questions(
        self,
        cards: Sequence[ArgumentCard],
        critiques: Sequence[CritiqueCard],
    ) -> List[str]:
        return list(
            self._dedupe_preserve_order(
                list(self._iter_questions_from_cards(cards))
                + list(self._iter_questions_from_critiques(critiques))
            )
        )

    def _iter_questions_from_cards(
        self, cards: Sequence[ArgumentCard]
    ) -> Iterable[str]:
        for card in cards:
            for q in card.questions:
                clean = q.strip()
                if clean:
                    yield clean

    def _iter_questions_from_critiques(
        self, critiques: Sequence[CritiqueCard]
    ) -> Iterable[str]:
        for critique in critiques:
            for q in critique.questions:
                clean = q.strip()
                if clean:
                    yield clean

    def _dedupe_preserve_order(self, values: Sequence[str]) -> Iterable[str]:
        seen: set[str] = set()
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            yield value


__all__ = [
    "ArgumentCard",
    "AxisSpec",
    "CritiqueCard",
    "ScoreboardEntry",
    "SynthesisEngine",
    "SynthesisReport",
]
