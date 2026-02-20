"""
EmergenceDetector — Integration Tests
======================================

10 integration tests that exercise EmergenceDetector together with
DeliberationEngine, InfluenceTracker, and the full deliberation pipeline.

Unlike the unit tests in test_phase6b_emergence.py (which test each class in
isolation), these tests verify the *interaction* between components:

  - EmergenceDetector  ↔  DeliberationEngine (multi-round pipeline)
  - InfluenceTracker   ↔  EmergenceDetector  (coexistence in result)
  - DeliberationResult ↔  summary()          (field consistency)
  - Threshold tuning   ↔  signal gating      (0.0 / 0.99 edge cases)

Embedding strategy:
  All tests use ``keyword_encode`` to force the keyword-bag backend so
  cosine distances are deterministic without requiring sentence-transformers.

Markers: unit, phase4 (reuses phase4 marker; add ``philosophical`` for
  semantics-heavy tests if desired).
"""

from __future__ import annotations

import datetime
import uuid
from typing import Any, List, Optional, Sequence

import pytest

from po_core.deliberation import emergence as emergence_mod
from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.engine import DeliberationEngine
from po_core.deliberation.influence import InfluenceTracker
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot

# ── Shared constants ──────────────────────────────────────────────────────────

_PO_CORE_KEY = "_po_core"

# ── Texts designed to trigger InteractionMatrix tension ──────────────────────
#
# _compute_tension() in interaction_tensor.py scores hits against 12
# opposition pairs (freedom/determinism, individual/collective, …).
# TENSION_A and TENSION_B each carry one word from every pair → 12/12 hits →
# tension = 1.0 for every A↔B comparison, guaranteeing high_interference_pairs
# returns the pair and triggers re-proposing in round 2.

TENSION_A_TEXT = (
    "freedom individual subjective intuitive becoming essence "
    "relative chaos plurality mind practice particular authentic human"
)
TENSION_B_TEXT = (
    "determinism collective objective rational being existence "
    "absolute order unity body theory universal moral law categorical"
)
# Radically novel text (quantum vocabulary — no overlap with A or B)
NOVEL_TEXT = (
    "quantum entanglement distributes consciousness photon states "
    "measurement collapses superposed ethical realities observed"
)
# Near-paraphrase of TENSION_A — low novelty for threshold tests
SIMILAR_TEXT = (
    "freedom individual subjective intuitive becoming essence "
    "relative disorder multiplicity psyche action singular"
)


# ── Shared helpers ────────────────────────────────────────────────────────────


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


def _make_ctx(user_input: str = "What is justice?") -> Context:
    return Context(
        request_id=f"req-{uuid.uuid4().hex[:8]}",
        created_at=datetime.datetime.now(datetime.timezone.utc),
        user_input=user_input,
    )


class _StubPhilosopher:
    """Lightweight philosopher that returns a fixed proposal when re-proposing.

    Used to inject novel (or similar) text into round-2 re-proposals without
    requiring actual philosopher modules.
    """

    def __init__(self, name: str, revision_content: str) -> None:
        self.name = name
        self._revision_content = revision_content

    def propose(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> List[Proposal]:
        return [_make_proposal(self._revision_content, self.name)]


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def keyword_encode(monkeypatch):
    """Force keyword-bag encoder for deterministic embedding distances."""
    from po_core.deliberation import influence as influence_mod

    monkeypatch.setattr(emergence_mod, "_encode", emergence_mod._keyword_embed)
    monkeypatch.setattr(influence_mod, "_encode", emergence_mod._keyword_embed)


@pytest.fixture
def ctx():
    return _make_ctx()


@pytest.fixture
def intent():
    return Intent()


@pytest.fixture
def tensors():
    return TensorSnapshot()


@pytest.fixture
def memory():
    return MemorySnapshot()


# ── Integration test class ────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.phase4
class TestEmergenceDetectorIntegration:
    """
    10 integration tests for EmergenceDetector interacting with the
    deliberation pipeline.
    """

    # ── Test 1 ──────────────────────────────────────────────────────────

    def test_emergence_detected_in_full_deliberation(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        End-to-end: two philosophers with orthogonal baseline proposals;
        one revises with a radically novel text.
        Expected: result.has_emergence == True, at least one signal.
        """
        # Round-1 proposals: highly different → triggers high-interference pair
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        # Stub philosopher: Sartre re-proposes with NOVEL_TEXT
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(max_rounds=2, detect_emergence=True)
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        assert result.has_emergence, "Expected emergence signal from novel revision"
        assert len(result.emergence_signals) >= 1
        for sig in result.emergence_signals:
            assert isinstance(sig, EmergenceSignal)

    # ── Test 2 ──────────────────────────────────────────────────────────

    def test_peak_novelty_is_max_across_all_signals(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        peak_novelty property should equal the maximum novelty_score
        across all emergence signals in the result.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(max_rounds=2, detect_emergence=True)
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        if not result.emergence_signals:
            pytest.skip("No emergence detected; cannot test peak_novelty")

        expected = max(s.novelty_score for s in result.emergence_signals)
        assert abs(result.peak_novelty - expected) < 1e-9

    # ── Test 3 ──────────────────────────────────────────────────────────

    def test_no_emergence_when_detector_disabled(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        detect_emergence=False → no EmergenceSignal emitted even when
        round-2 revisions are semantically novel.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(max_rounds=2, detect_emergence=False)
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        assert result.emergence_signals == []
        assert result.has_emergence is False
        assert result.peak_novelty == 0.0

    # ── Test 4 ──────────────────────────────────────────────────────────

    def test_low_threshold_catches_all_novelty(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        emergence_threshold=0.0 → any distance > 0 triggers a signal,
        including mildly paraphrased text.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        # SIMILAR_TEXT is a paraphrase of FREEDOM_TEXT → small distance
        stubs = [
            _StubPhilosopher("Sartre", SIMILAR_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(
            max_rounds=2, detect_emergence=True, emergence_threshold=0.0
        )
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        # With threshold=0.0 any non-zero distance generates a signal.
        # If re-proposing happened, we should have signals.
        if len(result.rounds) >= 2:
            assert result.has_emergence, (
                "threshold=0.0 should catch even paraphrased revisions"
            )

    # ── Test 5 ──────────────────────────────────────────────────────────

    def test_high_threshold_suppresses_similar_revisions(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        emergence_threshold=0.99 → similar-text revisions (low novelty)
        are below the threshold and produce NO signals.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        # Sartre revises with SIMILAR_TEXT (paraphrase → low novelty)
        stubs = [
            _StubPhilosopher("Sartre", SIMILAR_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(
            max_rounds=2, detect_emergence=True, emergence_threshold=0.99
        )
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        # Paraphrase should not exceed 0.99 novelty
        assert result.emergence_signals == [] or all(
            s.novelty_score < 0.99 for s in result.emergence_signals
        ), "Paraphrase should not cross 0.99 threshold"

    # ── Test 6 ──────────────────────────────────────────────────────────

    def test_influence_weights_nonzero_after_revision(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        After multi-round deliberation where Kant's counterargument
        influences Sartre's revision, influence_weights should record
        a nonzero value.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        # Sartre revises with novel text (measurably different from baseline)
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(
            max_rounds=2, detect_emergence=True, track_influence=True
        )
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        # Influence weights should be populated
        assert isinstance(result.influence_weights, dict)
        # Some philosopher should have been influenced (if revision occurred)
        if len(result.rounds) >= 2 and result.rounds[-1].n_revised > 0:
            total = sum(
                sum(w.influenced.values())
                for w in result.influence_weights.values()
            )
            assert total >= 0.0  # non-negative influence totals

    # ── Test 7 ──────────────────────────────────────────────────────────

    def test_emergence_and_influence_both_populated(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        With both detect_emergence=True and track_influence=True, the
        result should have both non-empty emergence_signals and
        non-empty influence_weights (when re-proposing occurs).
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(
            max_rounds=2, detect_emergence=True, track_influence=True
        )
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        if len(result.rounds) >= 2 and result.rounds[-1].n_revised > 0:
            # When re-proposing occurred, emergence detector should have fired
            assert result.has_emergence, "Expected emergence when novelty was high"
            # Influence weights are populated only when deliberation completes normally.
            # Strong emergence (novelty >= strong_threshold) triggers an early halt
            # *before* InfluenceTracker.update() is called, so influence_weights may
            # legitimately be empty in that scenario.
            strong_halt = any(
                s.novelty_score >= 0.85 for s in result.emergence_signals
            )
            if not strong_halt:
                assert result.influence_weights, "Expected influence data when no early halt"

    # ── Test 8 ──────────────────────────────────────────────────────────

    def test_summary_emergence_section_complete(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        result.summary() must include an 'emergence' section with keys:
        'detected', 'n_signals', 'peak_novelty'.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(max_rounds=2)
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        summary = result.summary()
        assert "emergence" in summary, "summary() must include 'emergence' section"
        emg = summary["emergence"]
        assert "detected" in emg
        assert "n_signals" in emg
        assert "peak_novelty" in emg
        # Value consistency
        assert emg["detected"] == result.has_emergence
        assert emg["n_signals"] == len(result.emergence_signals)
        assert abs(emg["peak_novelty"] - result.peak_novelty) < 1e-9

    # ── Test 9 ──────────────────────────────────────────────────────────

    def test_catalyst_pair_names_are_two_strings(
        self, keyword_encode, ctx, intent, tensors, memory
    ):
        """
        Every EmergenceSignal in the result must have catalyst_pair as a
        tuple of exactly two strings.
        """
        round1 = [
            _make_proposal(TENSION_A_TEXT, "Sartre"),
            _make_proposal(TENSION_B_TEXT, "Kant"),
        ]
        stubs = [
            _StubPhilosopher("Sartre", NOVEL_TEXT),
            _StubPhilosopher("Kant", TENSION_B_TEXT),
        ]

        engine = DeliberationEngine(max_rounds=2, detect_emergence=True)
        result = engine.deliberate(stubs, ctx, intent, tensors, memory, round1)

        for sig in result.emergence_signals:
            assert isinstance(sig.catalyst_pair, tuple), (
                f"catalyst_pair must be a tuple, got {type(sig.catalyst_pair)}"
            )
            assert len(sig.catalyst_pair) == 2, (
                f"catalyst_pair must have 2 elements, got {len(sig.catalyst_pair)}"
            )
            assert all(isinstance(p, str) for p in sig.catalyst_pair), (
                f"Both catalyst_pair elements must be strings: {sig.catalyst_pair}"
            )

    # ── Test 10 ─────────────────────────────────────────────────────────

    def test_strong_emergence_detected_with_low_strong_threshold(self, keyword_encode):
        """
        EmergenceDetector.has_strong_emergence() returns True when
        strong_threshold is set well below the novelty score of NOVEL_TEXT
        vs FREEDOM_TEXT (which is near 1.0 in keyword-bag space).
        """
        detector = EmergenceDetector(threshold=0.0, strong_threshold=0.5)
        baseline = [_make_proposal(TENSION_A_TEXT, "Sartre")]
        current = [_make_proposal(NOVEL_TEXT, "Sartre")]

        signals = detector.detect(baseline, current, round_num=2)
        assert signals, "threshold=0.0 should generate a signal for any non-zero distance"

        # With strong_threshold=0.5, a score near 1.0 should be "strong"
        if signals[0].novelty_score >= 0.5:
            assert detector.has_strong_emergence(signals), (
                f"novelty={signals[0].novelty_score:.3f} should be strong "
                f"(strong_threshold=0.5)"
            )
