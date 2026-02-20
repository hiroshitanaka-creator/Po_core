"""
Phase 6-B: EmergenceDetector + InfluenceTracker — Unit Tests
=============================================================

Tests for:
  - EmergenceSignal dataclass
  - EmergenceDetector (novelty-based emergence detection)
  - InfluenceWeight dataclass
  - InfluenceTracker (inter-philosopher influence measurement)
  - DeliberationResult new fields (has_emergence, peak_novelty, summary)
  - DeliberationEngine integration flags

Embedding strategy:
  Tests that validate "similar text ↔ low distance" or "different text ↔ high
  distance" use `monkeypatch` to force the keyword-bag backend so results are
  deterministic regardless of whether sentence-transformers is installed.
  Tests that only need "some signal exists" or "no signal" use threshold tricks
  (0.0 = catch-all, 1.1 = nothing).
"""

from __future__ import annotations

import datetime
import uuid

import pytest

from po_core.deliberation import emergence as emergence_mod
from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.engine import DeliberationEngine, DeliberationResult
from po_core.deliberation.influence import InfluenceTracker, InfluenceWeight
from po_core.domain.proposal import Proposal

# ── Fixtures ──────────────────────────────────────────────────────────

# PO_CORE key = "_po_core", AUTHOR key = "author"
_PO_CORE_KEY = "_po_core"


def _make_proposal(content: str, author: str) -> Proposal:
    """Build a minimal Proposal with author metadata."""
    return Proposal(
        proposal_id=f"test-{uuid.uuid4().hex[:8]}",
        action_type="respond",
        content=content,
        confidence=0.8,
        assumption_tags=[],
        risk_tags=[],
        extra={_PO_CORE_KEY: {"author": author}},
    )


# Semantically different texts for high-novelty scenarios (keyword backend)
FREEDOM_TEXT = (
    "freedom fundamental condition human existence "
    "choosing authentically defines existential beings"
)
DUTY_TEXT = (
    "duty moral law transcend personal desire "
    "categorical imperative binds rational agents unconditionally"
)
NOVEL_TEXT = (
    "quantum entanglement distributes consciousness photon states "
    "measurement collapses superposed ethical realities observed"
)
SIMILAR_TEXT = (
    "freedom core condition human existence "
    "authentic choices determine existential subjects"
)


@pytest.fixture
def keyword_encode(monkeypatch):
    """Force the keyword-bag encoder in both deliberation modules for determinism."""
    from po_core.deliberation import influence as influence_mod

    monkeypatch.setattr(emergence_mod, "_encode", emergence_mod._keyword_embed)
    monkeypatch.setattr(influence_mod, "_encode", emergence_mod._keyword_embed)


# ── EmergenceSignal ───────────────────────────────────────────────────


class TestEmergenceSignal:
    def test_creation(self):
        sig = EmergenceSignal(
            novelty_score=0.72,
            source_philosopher="Sartre",
            catalyst_pair=("Sartre", "Kant"),
            round_detected=2,
        )
        assert sig.novelty_score == 0.72
        assert sig.source_philosopher == "Sartre"
        assert sig.catalyst_pair == ("Sartre", "Kant")
        assert sig.round_detected == 2

    def test_is_strong_above_threshold(self):
        sig = EmergenceSignal(0.90, "Nietzsche", ("Nietzsche", "Hegel"), 2)
        assert sig.is_strong(strong_threshold=0.85) is True

    def test_is_strong_below_threshold(self):
        sig = EmergenceSignal(0.70, "Nietzsche", ("Nietzsche", "Hegel"), 2)
        assert sig.is_strong(strong_threshold=0.85) is False

    def test_is_strong_at_threshold(self):
        sig = EmergenceSignal(0.85, "Kant", ("Kant", "Hume"), 2)
        assert sig.is_strong(strong_threshold=0.85) is True

    def test_frozen(self):
        sig = EmergenceSignal(0.72, "Sartre", ("Sartre", "Kant"), 2)
        with pytest.raises(Exception):
            sig.novelty_score = 0.99  # type: ignore[misc]


# ── EmergenceDetector ─────────────────────────────────────────────────


class TestEmergenceDetector:
    def test_empty_baseline_returns_empty(self):
        detector = EmergenceDetector(threshold=0.5)
        assert detector.detect([], [_make_proposal(NOVEL_TEXT, "N")], 2) == []

    def test_empty_current_returns_empty(self):
        detector = EmergenceDetector(threshold=0.5)
        assert detector.detect([_make_proposal(FREEDOM_TEXT, "S")], [], 2) == []

    def test_identical_text_no_emergence(self, keyword_encode):
        """Identical text → min-distance = 0 → no emergence signal."""
        detector = EmergenceDetector(threshold=0.3)
        text = "justice equal treatment rational beings"
        baseline = [_make_proposal(text, "Rawls")]
        current = [_make_proposal(text, "Rawls")]
        signals = detector.detect(baseline, current, round_num=2)
        assert len(signals) == 0

    def test_very_similar_text_below_threshold(self, keyword_encode):
        """Paraphrase shares many keywords → low distance → below threshold."""
        detector = EmergenceDetector(threshold=0.5)
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        current = [_make_proposal(SIMILAR_TEXT, "Beauvoir")]
        signals = detector.detect(baseline, current, round_num=2)
        assert len(signals) == 0

    def test_very_different_text_above_threshold(self, keyword_encode):
        """Completely different vocabulary → high distance → emergent."""
        detector = EmergenceDetector(threshold=0.5)
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        current = [_make_proposal(NOVEL_TEXT, "Nietzsche")]
        signals = detector.detect(baseline, current, round_num=2)
        assert len(signals) >= 1
        assert signals[0].novelty_score >= 0.5

    def test_signals_sorted_by_novelty_descending(self, keyword_encode):
        detector = EmergenceDetector(threshold=0.0)
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        current = [
            _make_proposal(NOVEL_TEXT, "Nietzsche"),
            _make_proposal(DUTY_TEXT, "Kant"),
        ]
        signals = detector.detect(baseline, current, round_num=2)
        for i in range(len(signals) - 1):
            assert signals[i].novelty_score >= signals[i + 1].novelty_score

    def test_round_num_recorded(self, keyword_encode):
        detector = EmergenceDetector(threshold=0.0)
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        current = [_make_proposal(NOVEL_TEXT, "Nietzsche")]
        signals = detector.detect(baseline, current, round_num=3)
        if signals:
            assert signals[0].round_detected == 3

    def test_source_philosopher_extracted(self, keyword_encode):
        detector = EmergenceDetector(threshold=0.0)
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        current = [_make_proposal(DUTY_TEXT, "Kant")]
        signals = detector.detect(baseline, current, round_num=2)
        if signals:
            assert signals[0].source_philosopher == "Kant"

    def test_catalyst_pair_is_tuple_of_two(self, keyword_encode):
        detector = EmergenceDetector(threshold=0.0)
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        current = [_make_proposal(NOVEL_TEXT, "Nietzsche")]
        signals = detector.detect(baseline, current, round_num=2)
        if signals:
            assert len(signals[0].catalyst_pair) == 2

    def test_has_strong_emergence_true(self):
        """strong_threshold=0 → any signal is strong."""
        detector = EmergenceDetector(threshold=0.0, strong_threshold=0.0)
        sig = EmergenceSignal(0.01, "N", ("N", "K"), 2)
        assert detector.has_strong_emergence([sig]) is True

    def test_has_strong_emergence_empty(self):
        detector = EmergenceDetector(threshold=0.99)
        assert detector.has_strong_emergence([]) is False

    def test_novelty_score_in_range(self, keyword_encode):
        detector = EmergenceDetector(threshold=0.0)
        baseline = [
            _make_proposal(FREEDOM_TEXT, "Sartre"),
            _make_proposal(DUTY_TEXT, "Kant"),
        ]
        current = [
            _make_proposal(NOVEL_TEXT, "Nietzsche"),
            _make_proposal(SIMILAR_TEXT, "Beauvoir"),
        ]
        signals = detector.detect(baseline, current, round_num=2)
        for sig in signals:
            assert 0.0 <= sig.novelty_score <= 1.0

    def test_multiple_baseline_nearest_used(self, keyword_encode):
        """
        A proposal identical to one baseline has min_dist ≈ 0 → not novel.
        """
        detector = EmergenceDetector(threshold=0.0)
        baseline = [
            _make_proposal(FREEDOM_TEXT, "Sartre"),
            _make_proposal(NOVEL_TEXT, "Nietzsche"),  # same as current
        ]
        # Current identical to Nietzsche's baseline → min_dist ≈ 0
        current = [_make_proposal(NOVEL_TEXT, "Camus")]
        signals = detector.detect(baseline, current, round_num=2)
        assert len(signals) >= 1
        # novelty ≈ 0 because current matches Nietzsche baseline exactly
        assert signals[0].novelty_score < 0.01


# ── InfluenceWeight ───────────────────────────────────────────────────


class TestInfluenceWeight:
    def test_creation(self):
        iw = InfluenceWeight(philosopher_id="Hegel")
        assert iw.philosopher_id == "Hegel"
        assert iw.influenced == {}

    def test_total_influence_empty(self):
        iw = InfluenceWeight(philosopher_id="Hegel")
        assert iw.total_influence() == 0.0

    def test_total_influence_sum(self):
        iw = InfluenceWeight(
            philosopher_id="Hegel",
            influenced={"Marx": 0.4, "Engels": 0.3},
        )
        assert abs(iw.total_influence() - 0.7) < 1e-9

    def test_to_dict_keys(self):
        iw = InfluenceWeight(philosopher_id="Hegel", influenced={"Marx": 0.4})
        d = iw.to_dict()
        assert "philosopher_id" in d
        assert "influenced" in d
        assert "total_influence" in d

    def test_to_dict_values(self):
        iw = InfluenceWeight(
            philosopher_id="Nietzsche",
            influenced={"Heidegger": 0.55},
        )
        d = iw.to_dict()
        assert d["philosopher_id"] == "Nietzsche"
        assert d["influenced"]["Heidegger"] == 0.55
        assert abs(d["total_influence"] - 0.55) < 1e-3


# ── InfluenceTracker ──────────────────────────────────────────────────


class TestInfluenceTracker:
    def test_initial_state(self):
        tracker = InfluenceTracker()
        assert tracker.weights() == {}
        assert tracker.top_influencers() == []

    def test_set_baseline_stores_texts(self):
        tracker = InfluenceTracker()
        proposals = [
            _make_proposal(FREEDOM_TEXT, "Sartre"),
            _make_proposal(DUTY_TEXT, "Kant"),
        ]
        tracker.set_baseline(proposals)
        assert "Sartre" in tracker._baseline_texts
        assert "Kant" in tracker._baseline_texts

    def test_empty_baseline_no_crash(self):
        tracker = InfluenceTracker()
        tracker.set_baseline([])
        assert tracker.weights() == {}

    def test_update_without_baseline_no_crash(self):
        tracker = InfluenceTracker()
        revised = [_make_proposal(NOVEL_TEXT, "Nietzsche")]
        tracker.update(revised, {"Nietzsche": "Kant"})
        assert tracker.weights() == {}

    def test_update_records_influence(self, keyword_encode):
        tracker = InfluenceTracker()
        baseline = [
            _make_proposal(FREEDOM_TEXT, "Sartre"),
            _make_proposal(DUTY_TEXT, "Kant"),
        ]
        tracker.set_baseline(baseline)
        # Kant sent Sartre a counterargument → Sartre revised with novel text
        revised = [_make_proposal(NOVEL_TEXT, "Sartre")]
        tracker.update(revised, {"Sartre": "Kant"})
        weights = tracker.weights()
        assert "Kant" in weights
        assert "Sartre" in weights["Kant"].influenced

    def test_influence_delta_nonzero_for_different_text(self, keyword_encode):
        tracker = InfluenceTracker()
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        tracker.set_baseline(baseline)
        revised = [_make_proposal(NOVEL_TEXT, "Sartre")]
        tracker.update(revised, {"Sartre": "Kant"})
        weights = tracker.weights()
        assert weights["Kant"].influenced["Sartre"] > 0.0

    def test_influence_delta_near_zero_for_same_text(self, keyword_encode):
        tracker = InfluenceTracker()
        baseline = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        tracker.set_baseline(baseline)
        revised = [_make_proposal(FREEDOM_TEXT, "Sartre")]
        tracker.update(revised, {"Sartre": "Kant"})
        weights = tracker.weights()
        assert weights["Kant"].influenced["Sartre"] < 0.05

    def test_top_influencers_sorted(self):
        tracker = InfluenceTracker()
        tracker._weights = {
            "Hegel": InfluenceWeight("Hegel", {"Marx": 0.8, "Engels": 0.6}),
            "Kant": InfluenceWeight("Kant", {"Fichte": 0.3}),
        }
        top = tracker.top_influencers(n=2)
        assert len(top) == 2
        assert top[0][0] == "Hegel"
        assert top[1][0] == "Kant"

    def test_top_influencers_n_limit(self):
        tracker = InfluenceTracker()
        for i in range(5):
            tracker._weights[f"ph_{i}"] = InfluenceWeight(
                f"ph_{i}", {"other": float(i) * 0.1}
            )
        top = tracker.top_influencers(n=3)
        assert len(top) == 3

    def test_reset_clears_all_state(self):
        tracker = InfluenceTracker()
        tracker.set_baseline([_make_proposal(FREEDOM_TEXT, "Sartre")])
        tracker._weights["Kant"] = InfluenceWeight("Kant", {"Sartre": 0.5})
        tracker.reset()
        assert tracker._baseline_texts == {}
        assert tracker._weights == {}

    def test_to_dict(self):
        tracker = InfluenceTracker()
        tracker._weights["Hegel"] = InfluenceWeight("Hegel", {"Marx": 0.7})
        d = tracker.to_dict()
        assert "Hegel" in d
        assert d["Hegel"]["influenced"]["Marx"] == 0.7


# ── DeliberationResult new fields ─────────────────────────────────────


class TestDeliberationResultNewFields:
    def _make_result(
        self,
        signals: list,
        weights: dict,
    ) -> DeliberationResult:
        from po_core.deliberation.engine import RoundTrace

        return DeliberationResult(
            proposals=[_make_proposal(FREEDOM_TEXT, "Sartre")],
            rounds=[RoundTrace(round_number=1, n_proposals=1, n_revised=0)],
            emergence_signals=signals,
            influence_weights=weights,
        )

    def test_has_emergence_false_when_empty(self):
        assert self._make_result([], {}).has_emergence is False

    def test_has_emergence_true_when_signals_present(self):
        sig = EmergenceSignal(0.72, "Sartre", ("Sartre", "Kant"), 2)
        assert self._make_result([sig], {}).has_emergence is True

    def test_peak_novelty_empty(self):
        assert self._make_result([], {}).peak_novelty == 0.0

    def test_peak_novelty_max(self):
        sigs = [
            EmergenceSignal(0.72, "Sartre", ("Sartre", "Kant"), 2),
            EmergenceSignal(0.88, "Nietzsche", ("Nietzsche", "Hegel"), 2),
            EmergenceSignal(0.65, "Hume", ("Hume", "Locke"), 3),
        ]
        assert self._make_result(sigs, {}).peak_novelty == 0.88

    def test_summary_includes_emergence_section(self):
        sig = EmergenceSignal(0.75, "Sartre", ("Sartre", "Kant"), 2)
        summary = self._make_result([sig], {}).summary()
        assert "emergence" in summary
        assert summary["emergence"]["detected"] is True
        assert summary["emergence"]["n_signals"] == 1
        assert summary["emergence"]["peak_novelty"] == 0.75

    def test_summary_includes_top_influencers(self):
        weights = {"Hegel": InfluenceWeight("Hegel", {"Marx": 0.8})}
        summary = self._make_result([], weights).summary()
        assert "top_influencers" in summary
        assert any(e["philosopher"] == "Hegel" for e in summary["top_influencers"])

    def test_default_fields_backward_compat(self):
        from po_core.deliberation.engine import RoundTrace

        result = DeliberationResult(
            proposals=[],
            rounds=[RoundTrace(round_number=1, n_proposals=0, n_revised=0)],
        )
        assert result.emergence_signals == []
        assert result.influence_weights == {}
        assert result.has_emergence is False
        assert result.peak_novelty == 0.0


# ── DeliberationEngine flags ──────────────────────────────────────────


class TestDeliberationEngineFlags:
    def test_detect_emergence_false_disables_detector(self):
        engine = DeliberationEngine(detect_emergence=False)
        assert engine._emergence_detector is None

    def test_detect_emergence_true_enables_detector(self):
        engine = DeliberationEngine(detect_emergence=True)
        assert isinstance(engine._emergence_detector, EmergenceDetector)

    def test_track_influence_false_disables_tracker(self):
        engine = DeliberationEngine(track_influence=False)
        assert engine._influence_tracker is None

    def test_track_influence_true_enables_tracker(self):
        engine = DeliberationEngine(track_influence=True)
        assert isinstance(engine._influence_tracker, InfluenceTracker)

    def test_default_engine_has_both_enabled(self):
        engine = DeliberationEngine()
        assert engine._emergence_detector is not None
        assert engine._influence_tracker is not None

    def test_max_rounds_1_returns_empty_signals(self):
        """Single-round deliberation produces no emergence signals."""
        from po_core.domain.context import Context
        from po_core.domain.intent import Intent
        from po_core.domain.memory_snapshot import MemorySnapshot
        from po_core.domain.tensor_snapshot import TensorSnapshot

        engine = DeliberationEngine(max_rounds=1)
        proposals = [
            _make_proposal(FREEDOM_TEXT, "Sartre"),
            _make_proposal(DUTY_TEXT, "Kant"),
        ]
        ctx = Context(
            request_id="test-001",
            created_at=datetime.datetime.now(datetime.timezone.utc),
            user_input="What is freedom?",
        )
        intent = Intent()
        tensors = TensorSnapshot()
        memory = MemorySnapshot()
        result = engine.deliberate([], ctx, intent, tensors, memory, proposals)
        assert result.emergence_signals == []
        assert result.influence_weights == {}
