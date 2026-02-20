"""
Philosopher Quality Ledger
==========================

哲学者別の品質履歴を管理するledger。

各哲学者について以下を追跡する:
  - 参加回数 (total_proposals)
  - 勝利回数 (提案が採用された回数)
  - 平均倫理品質スコア (overall from EthicalQualityScore)
  - 創発貢献度 (EmergenceSignal.source_philosopher として検出された回数)
  - 最終活動日時

Usage::

    from po_core.meta.philosopher_ledger import PhilosopherQualityLedger

    ledger = PhilosopherQualityLedger()
    ledger.update_from_score(score)          # called by MetaEthicsMonitor
    ledger.record_win("Kant")               # Kant's proposal selected
    ledger.record_emergence("Nietzsche")    # Nietzsche produced novel emergence
    underperformers = ledger.get_underperformers(threshold=0.3)
    top3 = ledger.rankings(n=3)
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from po_core.meta.ethics_monitor import EthicalQualityScore

# ── PhilosopherRecord ─────────────────────────────────────────────────


@dataclass
class PhilosopherRecord:
    """
    Per-philosopher quality record.

    Attributes:
        name:                    Philosopher identifier string.
        total_proposals:         Times this philosopher contributed a proposal.
        total_wins:              Times their proposal was selected as winner.
        quality_scores:          History of overall EthicalQualityScore values
                                 for cycles where this philosopher won.
        emergence_contributions: Times detected as source of a novel EmergenceSignal.
        last_active:             Timestamp of most recent activity.
    """

    name: str
    total_proposals: int = 0
    total_wins: int = 0
    quality_scores: List[float] = field(default_factory=list)
    emergence_contributions: int = 0
    last_active: Optional[datetime] = None

    # ── Derived stats ──────────────────────────────────────────────────

    @property
    def win_rate(self) -> float:
        """Fraction of participation cycles where this philosopher's proposal won."""
        if self.total_proposals == 0:
            return 0.0
        return self.total_wins / self.total_proposals

    @property
    def mean_quality(self) -> float:
        """Mean quality score of cycles won by this philosopher."""
        if not self.quality_scores:
            return 0.0
        return statistics.mean(self.quality_scores)

    @property
    def composite_score(self) -> float:
        """
        Composite ranking score combining win rate, quality, and emergence.

        composite = 0.5 × mean_quality + 0.3 × win_rate + 0.2 × emergence_ratio
        emergence_ratio = min(1.0, emergence_contributions / max(1, total_wins))
        """
        emergence_ratio = min(
            1.0,
            self.emergence_contributions / max(1, self.total_wins),
        )
        return 0.5 * self.mean_quality + 0.3 * self.win_rate + 0.2 * emergence_ratio

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "total_proposals": self.total_proposals,
            "total_wins": self.total_wins,
            "win_rate": round(self.win_rate, 4),
            "mean_quality": round(self.mean_quality, 4),
            "emergence_contributions": self.emergence_contributions,
            "composite_score": round(self.composite_score, 4),
            "last_active": (self.last_active.isoformat() if self.last_active else None),
        }


# ── PhilosopherQualityLedger ──────────────────────────────────────────


class PhilosopherQualityLedger:
    """
    Ledger tracking per-philosopher performance across reasoning cycles.

    Designed to be updated by MetaEthicsMonitor.record() and by the pipeline
    whenever a winning philosopher is identified or emergence is detected.
    """

    def __init__(self) -> None:
        self._records: Dict[str, PhilosopherRecord] = {}

    # ── Mutation API ──────────────────────────────────────────────────

    def update_from_score(self, score: EthicalQualityScore) -> None:
        """
        Record a quality cycle.

        Increments total_proposals for the winning philosopher, records
        their win, and appends the overall score to their history.
        If winning_author is empty, the cycle is still counted but not
        attributed to any philosopher.
        """
        author = score.winning_author
        if not author:
            return
        record = self._ensure(author)
        record.total_proposals += 1
        record.total_wins += 1
        record.quality_scores.append(score.overall)
        record.last_active = score.timestamp

    def record_participation(self, philosopher_name: str) -> None:
        """
        Record that a philosopher participated in a cycle (even if not selected).

        Call this for every philosopher that proposed, before calling
        update_from_score for the winner.
        """
        if not philosopher_name:
            return
        record = self._ensure(philosopher_name)
        record.total_proposals += 1
        record.last_active = datetime.now(timezone.utc)

    def record_win(
        self,
        philosopher_name: str,
        quality_score: Optional[float] = None,
    ) -> None:
        """
        Record a win for a philosopher (separate from update_from_score).

        Useful when calling from pipeline code that tracks the winner
        independently.
        """
        if not philosopher_name:
            return
        record = self._ensure(philosopher_name)
        record.total_wins += 1
        if quality_score is not None:
            record.quality_scores.append(quality_score)
        record.last_active = datetime.now(timezone.utc)

    def record_emergence(self, philosopher_name: str) -> None:
        """
        Increment emergence contribution count for a philosopher.

        Call this when EmergenceDetector reports a signal with
        source_philosopher == philosopher_name.
        """
        if not philosopher_name:
            return
        record = self._ensure(philosopher_name)
        record.emergence_contributions += 1
        record.last_active = datetime.now(timezone.utc)

    # ── Query API ─────────────────────────────────────────────────────

    def get_record(self, name: str) -> Optional[PhilosopherRecord]:
        """Return the record for a philosopher, or None if not tracked."""
        return self._records.get(name)

    def get_underperformers(self, threshold: float = 0.3) -> List[str]:
        """
        Return names of philosophers whose composite_score < threshold.

        Philosophers with no wins are excluded (they may never have been
        selected, so there's no quality signal).
        """
        return [
            name
            for name, rec in self._records.items()
            if rec.total_wins > 0 and rec.composite_score < threshold
        ]

    def rankings(self, n: Optional[int] = None) -> List[Tuple[str, float]]:
        """
        Return philosophers ranked by composite_score, descending.

        Args:
            n: Limit to top-N results (None = all).

        Returns:
            List of (philosopher_name, composite_score).
        """
        ranked = sorted(
            [(name, rec.composite_score) for name, rec in self._records.items()],
            key=lambda x: x[1],
            reverse=True,
        )
        return ranked[:n] if n is not None else ranked

    def all_records(self) -> Dict[str, PhilosopherRecord]:
        """Return a copy of all records, keyed by philosopher name."""
        return dict(self._records)

    def to_dict(self) -> Dict:
        """Serialise all records to a plain dict."""
        return {name: rec.to_dict() for name, rec in self._records.items()}

    def reset(self) -> None:
        """Clear all records."""
        self._records.clear()

    # ── Internal ──────────────────────────────────────────────────────

    def _ensure(self, name: str) -> PhilosopherRecord:
        """Get or create a record for the given philosopher name."""
        if name not in self._records:
            self._records[name] = PhilosopherRecord(name=name)
        return self._records[name]
