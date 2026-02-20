"""
Phase 6-C: MetaEthicsMonitor + PhilosopherQualityLedger — Unit Tests
=====================================================================

Tests for:
  - EthicalQualityScore (computation + serialisation)
  - MetaEthicsMonitor (CUSUM drift detection + SafetyMode escalation)
  - DriftState (CUSUM state snapshot)
  - PhilosopherRecord (per-philosopher stats)
  - PhilosopherQualityLedger (aggregated ledger operations)
"""

from __future__ import annotations

import datetime
import uuid
from unittest.mock import MagicMock

import pytest

from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.meta import (
    DriftState,
    EthicalQualityScore,
    MetaEthicsMonitor,
    PhilosopherQualityLedger,
    PhilosopherRecord,
)
from po_core.runtime.settings import SafetyMode

# ── Helpers ───────────────────────────────────────────────────────────

_PO_CORE = "_po_core"


def _make_proposal(content: str, author: str) -> Proposal:
    return Proposal(
        proposal_id=f"p-{uuid.uuid4().hex[:8]}",
        action_type="respond",
        content=content,
        confidence=0.8,
        assumption_tags=[],
        risk_tags=[],
        extra={_PO_CORE: {"author": author}},
    )


def _allow_verdict() -> SafetyVerdict:
    return SafetyVerdict(decision=Decision.ALLOW)


def _reject_verdict() -> SafetyVerdict:
    return SafetyVerdict(decision=Decision.REJECT)


def _revise_verdict() -> SafetyVerdict:
    return SafetyVerdict(decision=Decision.REVISE)


def _tensors_with(metrics: dict) -> TensorSnapshot:
    """Build a TensorSnapshot with custom metrics dict."""
    return TensorSnapshot(metrics=metrics)


def _make_score(
    overall: float = 0.75,
    winning_author: str = "Kant",
    request_id: str | None = None,
) -> EthicalQualityScore:
    """Build an EthicalQualityScore directly (without compute())."""
    return EthicalQualityScore(
        request_id=request_id or uuid.uuid4().hex,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        safety_compliance=overall,
        philosophical_diversity=0.5,
        coherence=0.6,
        freedom_pressure_alignment=0.5,
        overall=overall,
        winning_author=winning_author,
    )


# ── EthicalQualityScore ───────────────────────────────────────────────


class TestEthicalQualityScore:
    def test_direct_creation(self):
        score = _make_score(overall=0.8, winning_author="Sartre")
        assert score.overall == 0.8
        assert score.winning_author == "Sartre"

    def test_frozen(self):
        score = _make_score()
        with pytest.raises(Exception):
            score.overall = 0.99  # type: ignore[misc]

    # ── compute() safety_compliance ───────────────────────────────────

    def test_compute_allow_verdict(self):
        proposal = _make_proposal("freedom is good", "Sartre")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.safety_compliance == 1.0

    def test_compute_reject_verdict(self):
        proposal = _make_proposal("harm is acceptable", "Machiavelli")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_reject_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.safety_compliance == 0.0

    def test_compute_revise_verdict(self):
        proposal = _make_proposal("needs refinement", "Hegel")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_revise_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.safety_compliance == 0.6

    # ── compute() diversity ───────────────────────────────────────────

    def test_compute_diversity_multiple_authors(self):
        proposals = [_make_proposal("text a", f"ph_{i}") for i in range(10)]
        winner = proposals[0]
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=proposals,
            winner=winner,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        # 10 unique / 39 ≈ 0.2564
        assert 0.25 < score.philosophical_diversity < 0.27

    def test_compute_diversity_single_author(self):
        proposal = _make_proposal("text", "Kant")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        # 1/39 ≈ 0.0256
        assert score.philosophical_diversity < 0.03

    def test_compute_diversity_max_clamped_at_one(self):
        proposals = [_make_proposal("x", f"ph_{i}") for i in range(100)]
        winner = proposals[0]
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=proposals,
            winner=winner,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.philosophical_diversity <= 1.0

    # ── compute() coherence ───────────────────────────────────────────

    def test_compute_coherence_connector_rich_content(self):
        content = (
            "therefore justice follows from reason "
            "because virtue entails duty thus we act"
        )
        proposal = _make_proposal(content, "Kant")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.coherence > 0.5

    def test_compute_coherence_contradiction_heavy_content(self):
        content = "but however nevertheless on the other hand inconsistent conflicting"
        proposal = _make_proposal(content, "Hegel")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.coherence < 0.5

    def test_compute_coherence_empty_content(self):
        proposal = _make_proposal("", "Kant")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.coherence == 0.5

    def test_compute_coherence_in_range(self):
        proposal = _make_proposal("justice therefore follows", "Rawls")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert 0.0 <= score.coherence <= 1.0

    # ── compute() FP alignment ────────────────────────────────────────

    def test_compute_fp_alignment_no_metrics(self):
        proposal = _make_proposal("freedom choice decide", "Sartre")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        # No FP metrics → neutral 0.5
        assert score.freedom_pressure_alignment == 0.5

    def test_compute_fp_alignment_matching_content(self):
        proposal = _make_proposal("choose choice freedom will decide option", "Sartre")
        tensors = _tensors_with({"choice": 0.9, "responsibility": 0.1})
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=tensors,
        )
        assert score.freedom_pressure_alignment > 0.5

    # ── compute() overall ─────────────────────────────────────────────

    def test_compute_overall_in_range(self):
        proposal = _make_proposal("justice", "Rawls")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert 0.0 <= score.overall <= 1.0

    def test_compute_winning_author_extracted(self):
        proposal = _make_proposal("text", "Aristotle")
        score = EthicalQualityScore.compute(
            request_id="r1",
            proposals=[proposal],
            winner=proposal,
            verdict=_allow_verdict(),
            tensors=TensorSnapshot(),
        )
        assert score.winning_author == "Aristotle"

    # ── to_dict ───────────────────────────────────────────────────────

    def test_to_dict_has_all_keys(self):
        score = _make_score()
        d = score.to_dict()
        for key in (
            "request_id",
            "timestamp",
            "safety_compliance",
            "philosophical_diversity",
            "coherence",
            "freedom_pressure_alignment",
            "overall",
            "winning_author",
        ):
            assert key in d

    def test_to_dict_types(self):
        score = _make_score(overall=0.75, winning_author="Kant")
        d = score.to_dict()
        assert isinstance(d["overall"], float)
        assert isinstance(d["timestamp"], str)
        assert isinstance(d["winning_author"], str)


# ── DriftState ────────────────────────────────────────────────────────


class TestDriftState:
    def test_default_not_drifting(self):
        ds = DriftState()
        assert ds.is_drifting is False
        assert ds.cusum_pos == 0.0
        assert ds.cusum_neg == 0.0
        assert ds.n_scores == 0

    def test_to_dict_keys(self):
        ds = DriftState(cusum_pos=0.1, cusum_neg=-0.05, is_drifting=False, n_scores=5)
        d = ds.to_dict()
        assert "cusum_pos" in d
        assert "cusum_neg" in d
        assert "is_drifting" in d
        assert "n_scores" in d

    def test_to_dict_values(self):
        ds = DriftState(
            cusum_pos=0.123456, cusum_neg=-0.05, is_drifting=True, n_scores=15
        )
        d = ds.to_dict()
        assert d["is_drifting"] is True
        assert d["n_scores"] == 15


# ── MetaEthicsMonitor ─────────────────────────────────────────────────


class TestMetaEthicsMonitor:
    def _make_monitor(self, threshold=0.15, window_size=20, min_baseline=10):
        ledger = PhilosopherQualityLedger()
        return MetaEthicsMonitor(
            ledger,
            drift_threshold=threshold,
            window_size=window_size,
            min_baseline=min_baseline,
        )

    def test_initial_cusum_state(self):
        monitor = self._make_monitor()
        state = monitor.cusum_state()
        assert state.cusum_pos == 0.0
        assert state.cusum_neg == 0.0
        assert state.is_drifting is False
        assert state.n_scores == 0

    def test_initial_not_drifting(self):
        monitor = self._make_monitor()
        assert monitor.is_drifting() is False

    def test_initial_mean_quality_zero(self):
        monitor = self._make_monitor()
        assert monitor.mean_quality() == 0.0

    def test_record_before_min_baseline_returns_none(self):
        monitor = self._make_monitor(min_baseline=10)
        for _ in range(9):
            result = monitor.record(_make_score(overall=0.8))
            assert result is None

    def test_record_stable_quality_no_drift(self):
        """Stable quality around 0.8 → no drift."""
        monitor = self._make_monitor(min_baseline=5, window_size=10)
        for _ in range(15):
            result = monitor.record(_make_score(overall=0.8))
        assert result is None
        assert monitor.is_drifting() is False

    def test_record_quality_drop_returns_warn(self):
        """Drop from 0.8 → 0.3 should trigger WARN."""
        monitor = self._make_monitor(threshold=0.05, min_baseline=5, window_size=10)
        # Establish baseline
        for _ in range(5):
            monitor.record(_make_score(overall=0.8))
        # Sudden drop
        result = None
        for _ in range(10):
            result = monitor.record(_make_score(overall=0.3))
            if result is not None:
                break
        assert result in (SafetyMode.WARN, SafetyMode.CRITICAL)

    def test_record_severe_quality_drop_returns_critical(self):
        """Sustained severe drop should eventually trigger CRITICAL."""
        monitor = self._make_monitor(threshold=0.05, min_baseline=3, window_size=10)
        for _ in range(3):
            monitor.record(_make_score(overall=1.0))
        result = None
        for _ in range(20):
            result = monitor.record(_make_score(overall=0.0))
            if result == SafetyMode.CRITICAL:
                break
        assert result == SafetyMode.CRITICAL

    def test_record_quality_improvement_no_escalation(self):
        """Quality improvement should not return escalation."""
        monitor = self._make_monitor(min_baseline=5, window_size=10)
        for _ in range(5):
            monitor.record(_make_score(overall=0.5))
        results = [monitor.record(_make_score(overall=0.9)) for _ in range(5)]
        # Improvement should not trigger negative drift
        assert not any(
            r in (SafetyMode.WARN, SafetyMode.CRITICAL)
            for r in results
            if r is not None
        )

    def test_tracer_emits_on_drift(self):
        """TracePort.emit() should be called when drift is detected."""
        monitor = self._make_monitor(threshold=0.05, min_baseline=3, window_size=10)
        tracer = MagicMock()
        tracer.emit = MagicMock()

        for _ in range(3):
            monitor.record(_make_score(overall=0.9), tracer)
        for _ in range(10):
            monitor.record(_make_score(overall=0.0), tracer)

        assert tracer.emit.called

    def test_tracer_not_called_before_drift(self):
        """TracePort.emit() should NOT be called before min_baseline."""
        monitor = self._make_monitor(min_baseline=10)
        tracer = MagicMock()
        for _ in range(9):
            monitor.record(_make_score(overall=0.8), tracer)
        assert not tracer.emit.called

    def test_mean_quality_after_records(self):
        monitor = self._make_monitor()
        for _ in range(5):
            monitor.record(_make_score(overall=0.6))
        assert abs(monitor.mean_quality() - 0.6) < 0.01

    def test_scores_accumulate(self):
        monitor = self._make_monitor()
        monitor.record(_make_score(overall=0.7))
        monitor.record(_make_score(overall=0.8))
        assert len(monitor.scores()) == 2

    def test_reset_clears_state(self):
        monitor = self._make_monitor()
        for _ in range(5):
            monitor.record(_make_score(overall=0.7))
        monitor.reset()
        assert len(monitor.scores()) == 0
        assert monitor.mean_quality() == 0.0
        assert monitor.cusum_state().cusum_pos == 0.0

    def test_ledger_updated_on_record(self):
        ledger = PhilosopherQualityLedger()
        monitor = MetaEthicsMonitor(ledger)
        score = _make_score(overall=0.8, winning_author="Aristotle")
        monitor.record(score)
        record = ledger.get_record("Aristotle")
        assert record is not None
        assert record.total_wins == 1


# ── PhilosopherRecord ─────────────────────────────────────────────────


class TestPhilosopherRecord:
    def test_creation_defaults(self):
        rec = PhilosopherRecord(name="Kant")
        assert rec.name == "Kant"
        assert rec.total_proposals == 0
        assert rec.total_wins == 0
        assert rec.quality_scores == []
        assert rec.emergence_contributions == 0
        assert rec.last_active is None

    def test_win_rate_zero_proposals(self):
        rec = PhilosopherRecord(name="Plato")
        assert rec.win_rate == 0.0

    def test_win_rate_half(self):
        rec = PhilosopherRecord(name="Plato", total_proposals=10, total_wins=5)
        assert rec.win_rate == 0.5

    def test_mean_quality_empty(self):
        rec = PhilosopherRecord(name="Plato")
        assert rec.mean_quality == 0.0

    def test_mean_quality_computed(self):
        rec = PhilosopherRecord(name="Plato", quality_scores=[0.6, 0.8, 1.0])
        assert abs(rec.mean_quality - 0.8) < 0.001

    def test_composite_score_range(self):
        rec = PhilosopherRecord(
            name="Nietzsche",
            total_proposals=10,
            total_wins=5,
            quality_scores=[0.7, 0.8],
            emergence_contributions=2,
        )
        assert 0.0 <= rec.composite_score <= 1.0

    def test_composite_score_better_for_higher_quality(self):
        low = PhilosopherRecord(
            name="A", total_proposals=10, total_wins=5, quality_scores=[0.3, 0.3]
        )
        high = PhilosopherRecord(
            name="B", total_proposals=10, total_wins=5, quality_scores=[0.9, 0.9]
        )
        assert high.composite_score > low.composite_score

    def test_to_dict_keys(self):
        rec = PhilosopherRecord(name="Hegel")
        d = rec.to_dict()
        for key in (
            "name",
            "total_proposals",
            "total_wins",
            "win_rate",
            "mean_quality",
            "emergence_contributions",
            "composite_score",
            "last_active",
        ):
            assert key in d

    def test_to_dict_last_active_none(self):
        rec = PhilosopherRecord(name="Hegel")
        assert rec.to_dict()["last_active"] is None


# ── PhilosopherQualityLedger ──────────────────────────────────────────


class TestPhilosopherQualityLedger:
    def test_initial_empty(self):
        ledger = PhilosopherQualityLedger()
        assert ledger.all_records() == {}
        assert ledger.rankings() == []

    def test_get_record_unknown_returns_none(self):
        ledger = PhilosopherQualityLedger()
        assert ledger.get_record("Descartes") is None

    def test_update_from_score_creates_record(self):
        ledger = PhilosopherQualityLedger()
        ledger.update_from_score(_make_score(winning_author="Kant"))
        assert ledger.get_record("Kant") is not None

    def test_update_from_score_increments_wins(self):
        ledger = PhilosopherQualityLedger()
        for _ in range(3):
            ledger.update_from_score(_make_score(winning_author="Kant", overall=0.8))
        assert ledger.get_record("Kant").total_wins == 3

    def test_update_from_score_empty_author_ignored(self):
        ledger = PhilosopherQualityLedger()
        ledger.update_from_score(_make_score(winning_author=""))
        assert ledger.all_records() == {}

    def test_record_win(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_win("Aristotle", quality_score=0.75)
        rec = ledger.get_record("Aristotle")
        assert rec.total_wins == 1
        assert rec.quality_scores == [0.75]

    def test_record_participation(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_participation("Hume")
        ledger.record_participation("Hume")
        rec = ledger.get_record("Hume")
        assert rec.total_proposals == 2

    def test_record_participation_empty_ignored(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_participation("")
        assert ledger.all_records() == {}

    def test_record_emergence(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_emergence("Nietzsche")
        ledger.record_emergence("Nietzsche")
        rec = ledger.get_record("Nietzsche")
        assert rec.emergence_contributions == 2

    def test_record_emergence_empty_ignored(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_emergence("")
        assert ledger.all_records() == {}

    def test_get_underperformers_finds_low_scorers(self):
        ledger = PhilosopherQualityLedger()
        # High performer
        ledger.record_win("Kant", quality_score=0.9)
        # Low performer
        ledger.record_win("Sophist", quality_score=0.1)
        underperformers = ledger.get_underperformers(threshold=0.3)
        assert "Sophist" in underperformers
        assert "Kant" not in underperformers

    def test_get_underperformers_excludes_no_wins(self):
        """Philosophers with 0 wins have no quality signal → excluded."""
        ledger = PhilosopherQualityLedger()
        ledger.record_participation("NoWins")
        assert "NoWins" not in ledger.get_underperformers()

    def test_rankings_sorted_descending(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_win("High", quality_score=0.9)
        ledger.record_win("Low", quality_score=0.2)
        rankings = ledger.rankings()
        scores = [s for _, s in rankings]
        assert scores == sorted(scores, reverse=True)

    def test_rankings_n_limit(self):
        ledger = PhilosopherQualityLedger()
        for i in range(5):
            ledger.record_win(f"ph_{i}", quality_score=float(i) * 0.1)
        top3 = ledger.rankings(n=3)
        assert len(top3) == 3

    def test_all_records_returns_copy(self):
        ledger = PhilosopherQualityLedger()
        ledger.update_from_score(_make_score(winning_author="Plato"))
        records = ledger.all_records()
        assert "Plato" in records

    def test_to_dict_serialises_all(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_win("Rawls", quality_score=0.8)
        d = ledger.to_dict()
        assert "Rawls" in d
        assert "win_rate" in d["Rawls"]

    def test_reset_clears_all(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_win("Hegel", quality_score=0.7)
        ledger.reset()
        assert ledger.all_records() == {}

    def test_multiple_philosophers_independent(self):
        ledger = PhilosopherQualityLedger()
        ledger.record_win("Kant", quality_score=0.9)
        ledger.record_win("Kant", quality_score=0.8)
        ledger.record_win("Hume", quality_score=0.5)
        assert ledger.get_record("Kant").total_wins == 2
        assert ledger.get_record("Hume").total_wins == 1
