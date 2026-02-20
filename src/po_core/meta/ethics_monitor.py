"""
MetaEthicsMonitor
=================

Po_core の倫理的自己反省モジュール。

各推論サイクルの倫理品質を定量化し、CUSUM アルゴリズムで品質ドリフトを
検出する。ドリフト検出時は TraceEvent を発火し、SafetyMode 引き上げを推奨
する。

Architecture:
  EthicalQualityScore — 1サイクル分のスコア (4指標 + 総合)
  MetaEthicsMonitor   — CUSUM ドリフト監視 + PhilosopherLedger 連携

Usage::

    from po_core.meta import EthicalQualityScore, MetaEthicsMonitor
    from po_core.meta.philosopher_ledger import PhilosopherQualityLedger

    ledger  = PhilosopherQualityLedger()
    monitor = MetaEthicsMonitor(ledger)
    score   = EthicalQualityScore.compute(
        request_id=ctx.request_id,
        proposals=proposals,
        winner=winner,
        verdict=verdict,
        tensors=tensors,
    )
    escalation = monitor.record(score, tracer)
    if escalation:
        print(f"SafetyMode escalated to {escalation}")
"""

from __future__ import annotations

import re
import statistics
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.trace_event import TraceEvent
from po_core.ports.trace import TracePort
from po_core.runtime.settings import SafetyMode

if TYPE_CHECKING:
    from po_core.meta.philosopher_ledger import PhilosopherQualityLedger

# ── Constants ─────────────────────────────────────────────────────────

_TOTAL_PHILOSOPHERS = 39  # canonical philosopher pool size

# Coherence signals: logical connectors boost coherence
_CONNECTORS = frozenset(
    {
        "therefore",
        "thus",
        "because",
        "since",
        "hence",
        "consequently",
        "given",
        "follows",
        "entails",
        "implies",
    }
)
# Contradiction markers reduce coherence
_CONTRADICTIONS = frozenset(
    {
        "but",
        "however",
        "nevertheless",
        "on the other hand",
        "contradicts",
        "refutes",
        "inconsistent",
        "paradox",
        "conflicting",
    }
)

# FP dimension → representative keyword stems
_FP_KEYWORDS: Dict[str, List[str]] = {
    "choice": ["choice", "choose", "decide", "option", "freedom", "will"],
    "responsibility": [
        "responsible",
        "duty",
        "obligation",
        "accountability",
        "ought",
    ],
    "urgency": ["urgent", "immediate", "crisis", "emergency", "now", "pressing"],
    "ethics": ["ethical", "moral", "right", "wrong", "virtue", "justice"],
    "social": ["social", "society", "community", "collective", "public", "common"],
    "authenticity": [
        "authentic",
        "genuine",
        "true",
        "self",
        "identity",
        "real",
    ],
}


# ── EthicalQualityScore ───────────────────────────────────────────────


@dataclass(frozen=True)
class EthicalQualityScore:
    """
    One-cycle ethical quality snapshot.

    Attributes:
        request_id:                  Unique identifier for this reasoning cycle.
        timestamp:                   When the score was computed.
        safety_compliance:           1.0 if ALLOW, 0.6 if REVISE, 0.0 if REJECT.
        philosophical_diversity:     Unique philosopher authors / 39.
        coherence:                   Internal consistency of the winning proposal.
        freedom_pressure_alignment:  How well the winner aligns with FP tensors.
        overall:                     Weighted composite (safety×0.4 + diversity×0.2
                                     + coherence×0.2 + fp_align×0.2).
        winning_author:              Author of the winning proposal (empty if unknown).
    """

    request_id: str
    timestamp: datetime
    safety_compliance: float
    philosophical_diversity: float
    coherence: float
    freedom_pressure_alignment: float
    overall: float
    winning_author: str = ""

    # ── Factory ───────────────────────────────────────────────────────

    @classmethod
    def compute(
        cls,
        request_id: str,
        proposals: Sequence[Proposal],
        winner: Proposal,
        verdict: SafetyVerdict,
        tensors: TensorSnapshot,
    ) -> "EthicalQualityScore":
        """
        Compute a quality score from pipeline artefacts.

        Args:
            request_id: From Context.request_id.
            proposals:  All proposals considered this cycle.
            winner:     The selected / winning proposal.
            verdict:    SafetyVerdict from W_Ethics Gate.
            tensors:    Current TensorSnapshot.
        """
        safety = _safety_score(verdict)
        diversity = _diversity_score(proposals)
        coherence = _coherence_score(winner.content)
        fp_align = _fp_alignment_score(winner.content, tensors)
        overall = _weighted_overall(safety, diversity, coherence, fp_align)
        author = _get_author(winner)
        return cls(
            request_id=request_id,
            timestamp=datetime.now(timezone.utc),
            safety_compliance=round(safety, 4),
            philosophical_diversity=round(diversity, 4),
            coherence=round(coherence, 4),
            freedom_pressure_alignment=round(fp_align, 4),
            overall=round(overall, 4),
            winning_author=author,
        )

    # ── Serialisation ─────────────────────────────────────────────────

    def to_dict(self) -> Dict:
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "safety_compliance": self.safety_compliance,
            "philosophical_diversity": self.philosophical_diversity,
            "coherence": self.coherence,
            "freedom_pressure_alignment": self.freedom_pressure_alignment,
            "overall": self.overall,
            "winning_author": self.winning_author,
        }


# ── DriftState ────────────────────────────────────────────────────────


@dataclass
class DriftState:
    """
    CUSUM cumulative sum state for drift detection.

    Attributes:
        cusum_pos:   Positive CUSUM (detects upward shift = quality improvement).
        cusum_neg:   Negative CUSUM (detects downward shift = quality degradation).
        is_drifting: True when either statistic exceeds the threshold.
        n_scores:    Total number of scores processed.
    """

    cusum_pos: float = 0.0
    cusum_neg: float = 0.0
    is_drifting: bool = False
    n_scores: int = 0

    def to_dict(self) -> Dict:
        return {
            "cusum_pos": round(self.cusum_pos, 6),
            "cusum_neg": round(self.cusum_neg, 6),
            "is_drifting": self.is_drifting,
            "n_scores": self.n_scores,
        }


# ── MetaEthicsMonitor ─────────────────────────────────────────────────


class MetaEthicsMonitor:
    """
    Ethical self-reflection monitor for Po_core.

    Roles:
      1. Record each cycle's EthicalQualityScore.
      2. Detect quality drift via CUSUM algorithm.
      3. On drift: emit EthicalDriftDetected TraceEvent.
      4. Return recommended SafetyMode escalation to caller.
      5. Update PhilosopherQualityLedger per cycle.

    Args:
        ledger:           PhilosopherQualityLedger instance.
        drift_threshold:  CUSUM threshold for alerting (default 0.15).
        window_size:      Rolling window size for baseline estimation (default 20).
        slack:            CUSUM slack parameter k (default 0.01).
        min_baseline:     Minimum scores before CUSUM activates (default 10).
    """

    def __init__(
        self,
        ledger: "PhilosopherQualityLedger",
        drift_threshold: float = 0.15,
        window_size: int = 20,
        slack: float = 0.01,
        min_baseline: int = 10,
    ) -> None:
        self._ledger = ledger
        self._threshold = drift_threshold
        self._window: deque[float] = deque(maxlen=window_size)
        self._slack = slack
        self._min_baseline = min_baseline
        self._cusum_pos: float = 0.0
        self._cusum_neg: float = 0.0
        self._all_scores: List[EthicalQualityScore] = []

    # ── Public API ────────────────────────────────────────────────────

    def record(
        self,
        score: EthicalQualityScore,
        tracer: Optional[TracePort] = None,
    ) -> Optional[SafetyMode]:
        """
        Record a quality score, update CUSUM, and emit TraceEvent if drifting.

        Args:
            score:  EthicalQualityScore for this cycle.
            tracer: Optional TracePort for emitting drift events.

        Returns:
            SafetyMode.WARN if quality degradation drift detected,
            SafetyMode.CRITICAL if CUSUM exceeds 2× threshold,
            None otherwise.
        """
        self._all_scores.append(score)
        self._window.append(score.overall)
        self._ledger.update_from_score(score)

        # CUSUM requires at least min_baseline samples
        if len(self._window) < self._min_baseline:
            return None

        # Estimate baseline from first half of window
        half = max(1, len(self._window) // 2)
        baseline = statistics.mean(list(self._window)[:half])

        deviation = score.overall - baseline
        self._cusum_pos = max(0.0, self._cusum_pos + deviation - self._slack)
        self._cusum_neg = min(0.0, self._cusum_neg + deviation + self._slack)

        # Check if either statistic signals drift
        # Only NEGATIVE drift (quality degradation) triggers SafetyMode escalation.
        # Positive drift (quality improvement) is tracked but not escalated.
        neg_exceeded = self._cusum_neg < -self._threshold

        if neg_exceeded:
            escalation = (
                SafetyMode.CRITICAL
                if abs(self._cusum_neg) > 2 * self._threshold
                else SafetyMode.WARN
            )

            if tracer is not None:
                tracer.emit(
                    TraceEvent.now(
                        "EthicalDriftDetected",
                        score.request_id,
                        {
                            "cusum_pos": round(self._cusum_pos, 6),
                            "cusum_neg": round(self._cusum_neg, 6),
                            "baseline": round(baseline, 4),
                            "latest_score": score.overall,
                            "recommended_safety_mode": escalation.value,
                        },
                    )
                )
            return escalation

        return None

    # ── Inspection ────────────────────────────────────────────────────

    def cusum_state(self) -> DriftState:
        """Return current CUSUM state snapshot."""
        # Only negative CUSUM (quality degradation) is considered "drifting"
        # for escalation purposes. Positive drift is tracked but not alerted.
        is_drifting = self._cusum_neg < -self._threshold
        return DriftState(
            cusum_pos=self._cusum_pos,
            cusum_neg=self._cusum_neg,
            is_drifting=is_drifting,
            n_scores=len(self._all_scores),
        )

    def is_drifting(self) -> bool:
        """True if CUSUM currently signals drift."""
        return self.cusum_state().is_drifting

    def mean_quality(self) -> float:
        """Rolling mean quality over the current window."""
        if not self._window:
            return 0.0
        return round(statistics.mean(self._window), 4)

    def scores(self) -> List[EthicalQualityScore]:
        """Return a copy of all recorded scores."""
        return list(self._all_scores)

    def reset(self) -> None:
        """Reset CUSUM state and score history (keep ledger)."""
        self._cusum_pos = 0.0
        self._cusum_neg = 0.0
        self._window.clear()
        self._all_scores.clear()


# ── Internal metric helpers ───────────────────────────────────────────


def _get_author(proposal: Proposal) -> str:
    """Extract author name from proposal metadata."""
    extra = proposal.extra if isinstance(proposal.extra, dict) else {}
    pc = extra.get(PO_CORE, {})
    return pc.get(AUTHOR, "") or extra.get("philosopher", "") or extra.get(AUTHOR, "")


def _safety_score(verdict: SafetyVerdict) -> float:
    """Map SafetyVerdict decision to a compliance score."""
    mapping = {
        Decision.ALLOW: 1.0,
        Decision.REVISE: 0.6,
        Decision.REJECT: 0.0,
    }
    return mapping.get(verdict.decision, 0.5)


def _diversity_score(proposals: Sequence[Proposal]) -> float:
    """
    Unique philosopher authors / 39.

    Uses the PO_CORE author metadata key; falls back to 'philosopher' field.
    Clamped to [0, 1].
    """
    authors: set = set()
    for p in proposals:
        extra = p.extra if isinstance(p.extra, dict) else {}
        pc = extra.get(PO_CORE, {})
        author = (
            pc.get(AUTHOR, "") or extra.get("philosopher", "") or extra.get(AUTHOR, "")
        )
        if author:
            authors.add(author)
    return min(1.0, len(authors) / _TOTAL_PHILOSOPHERS)


def _coherence_score(content: str) -> float:
    """
    Heuristic coherence score for proposal content.

    Score = connector_ratio - contradiction_penalty, clamped to [0, 1].
    """
    if not content:
        return 0.5  # neutral for empty content

    words = re.findall(r"[a-z]+", content.lower())
    if not words:
        return 0.5

    connector_count = sum(1 for w in words if w in _CONNECTORS)
    contradiction_count = sum(1 for w in words if w in _CONTRADICTIONS)
    total = len(words)

    # Connector density boosts; contradiction density reduces
    connector_ratio = connector_count / total
    contradiction_ratio = contradiction_count / total

    # Base score: more connectors → structured → coherent
    raw = 0.5 + 4.0 * connector_ratio - 2.0 * contradiction_ratio
    return float(min(1.0, max(0.0, raw)))


def _fp_alignment_score(content: str, tensors: TensorSnapshot) -> float:
    """
    Alignment between winning proposal content and FP tensor dimensions.

    Uses `metrics` or `aggregate_metrics` from TensorSnapshot.
    Returns 0.5 if tensor data unavailable.
    """
    if not content:
        return 0.5

    # Get the dominant FP dimension from tensors
    metrics = dict(tensors.metrics) if tensors.metrics else {}
    if tensors.aggregate_metrics:
        metrics.update(tensors.aggregate_metrics)

    if not metrics:
        return 0.5

    # Find the highest-scored FP dimension
    fp_dims = {k: v for k, v in metrics.items() if k in _FP_KEYWORDS}
    if not fp_dims:
        return 0.5

    top_dim = max(fp_dims, key=lambda k: fp_dims[k])
    top_score = fp_dims[top_dim]

    # How many relevant keywords appear in the proposal?
    words = re.findall(r"[a-z]+", content.lower())
    kws = _FP_KEYWORDS.get(top_dim, [])
    hits = sum(1 for w in words if w in kws)

    # Normalise: expect at least 1 hit per 30 words for full alignment
    expected = max(1, len(words) // 30)
    hit_ratio = min(1.0, hits / expected)

    # Weight by tensor score so high-FP cycles get stronger alignment signal
    return round(float(hit_ratio * top_score + (1 - top_score) * 0.5), 4)


def _weighted_overall(
    safety: float,
    diversity: float,
    coherence: float,
    fp_align: float,
) -> float:
    """Weighted composite: safety×0.4 + diversity×0.2 + coherence×0.2 + fp_align×0.2"""
    return safety * 0.4 + diversity * 0.2 + coherence * 0.2 + fp_align * 0.2
