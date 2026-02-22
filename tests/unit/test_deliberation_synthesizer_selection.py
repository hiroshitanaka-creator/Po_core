"""
PR-4: deliberation synthesizer selection — name/ID mismatch fix
================================================================

Verifies that the synthesis round in dialectic_mode correctly finds
synthesizer philosophers even when their ``.name`` attribute is a full
historical name (e.g. "Georg Wilhelm Friedrich Hegel") that does not
match the short-name entry previously stored in SYNTHESIZER_PHILOSOPHERS.

These tests require **no external LLM** and no real philosopher modules:
stub philosophers with realistic full names are sufficient.

Marker: phase4  (reuses existing CI bucket)
"""

from __future__ import annotations

import uuid
from typing import List

import pytest

from po_core.deliberation.engine import (
    _build_philosopher_lookup,
    _collect_synthesis_counterarguments,
)
from po_core.deliberation.roles import SYNTHESIZER_PHILOSOPHERS
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot

pytestmark = pytest.mark.phase4


# ── Minimal stubs ────────────────────────────────────────────────────────────


def _make_proposal(author: str, content: str = "some content") -> Proposal:
    return Proposal(
        proposal_id=f"test:{author}:0",
        action_type="answer",
        content=content,
        confidence=0.5,
        extra={"_po_core": {"author": author}, "philosopher": author},
    )


class _StubPhilosopher:
    """Minimal philosopher stub — only name and propose() are needed."""

    def __init__(self, name: str, response: str = "stub response") -> None:
        self.name = name
        self._response = response

    def propose(self, ctx, intent, tensors, memory) -> List[Proposal]:
        return [
            Proposal(
                proposal_id=f"{ctx.request_id}:{self.name}:0",
                action_type="answer",
                content=self._response,
                confidence=0.7,
                extra={"_po_core": {"author": self.name}},
            )
        ]


# Stubs that mimic the real philosopher class names and full .name values
class Hegel(_StubPhilosopher):
    def __init__(self) -> None:
        super().__init__("Georg Wilhelm Friedrich Hegel")


class Kant(_StubPhilosopher):
    def __init__(self) -> None:
        super().__init__("Immanuel Kant")


class Plato(_StubPhilosopher):
    def __init__(self) -> None:
        super().__init__("Plato (\u03a0\u03bb\u03ac\u03c4\u03c9\u03bd)")


class Dewey(_StubPhilosopher):
    def __init__(self) -> None:
        super().__init__("John Dewey")


class Aristotle(_StubPhilosopher):
    def __init__(self) -> None:
        super().__init__("Aristotle")


# ── Tests: SYNTHESIZER_PHILOSOPHERS uses IDs, not full names ─────────────────


class TestSynthesizerPhilosophersList:
    def test_synthesizer_ids_are_lowercase(self):
        for sid in SYNTHESIZER_PHILOSOPHERS:
            assert (
                sid == sid.lower()
            ), f"SYNTHESIZER_PHILOSOPHERS entry {sid!r} must be a lowercase ID"

    def test_synthesizer_ids_match_known_manifest_ids(self):
        expected = {"hegel", "kant", "plato", "dewey"}
        assert set(SYNTHESIZER_PHILOSOPHERS) == expected

    def test_synthesizer_ids_do_not_contain_full_names(self):
        full_names = [
            "Georg Wilhelm Friedrich Hegel",
            "Immanuel Kant",
            "Plato (Πλάτων)",
            "John Dewey",
        ]
        for full_name in full_names:
            assert (
                full_name not in SYNTHESIZER_PHILOSOPHERS
            ), f"Full name {full_name!r} should not appear in SYNTHESIZER_PHILOSOPHERS"


# ── Tests: _build_philosopher_lookup secondary key ───────────────────────────


class TestBuildPhilosopherLookup:
    def test_lookup_contains_full_name_key(self):
        hegel = Hegel()
        lookup = _build_philosopher_lookup([hegel])
        assert "Georg Wilhelm Friedrich Hegel" in lookup

    def test_lookup_contains_class_id_key(self):
        """Secondary key must be lowercase class name (= manifest philosopher_id)."""
        hegel = Hegel()
        lookup = _build_philosopher_lookup([hegel])
        assert "hegel" in lookup

    def test_lookup_class_id_and_name_resolve_same_instance(self):
        hegel = Hegel()
        lookup = _build_philosopher_lookup([hegel])
        assert lookup["hegel"] is lookup["Georg Wilhelm Friedrich Hegel"]

    def test_lookup_all_four_synthesizers_by_id(self):
        philosophers = [Hegel(), Kant(), Plato(), Dewey()]
        lookup = _build_philosopher_lookup(philosophers)
        for sid in SYNTHESIZER_PHILOSOPHERS:
            assert sid in lookup, f"philosopher_id {sid!r} not found in lookup"

    def test_lookup_non_synthesizer_by_class_id(self):
        aristotle = Aristotle()
        lookup = _build_philosopher_lookup([aristotle])
        assert "aristotle" in lookup

    def test_full_name_key_not_clobbered_by_secondary(self):
        """setdefault means the secondary key never overwrites an existing entry."""
        hegel = Hegel()
        kant = Kant()
        lookup = _build_philosopher_lookup([hegel, kant])
        assert lookup["Georg Wilhelm Friedrich Hegel"] is hegel
        assert lookup["Immanuel Kant"] is kant


# ── Tests: _collect_synthesis_counterarguments resolves via ID ───────────────


class TestCollectSynthesisCounterarguments:
    def _proposals(self) -> List[Proposal]:
        return [
            _make_proposal("Aristotle", "Virtue is a mean between extremes."),
            _make_proposal("Nietzsche", "Virtue is slave morality."),
        ]

    def test_synthesizer_found_when_using_id_keys(self):
        """Core regression: synthesis round must NOT return empty dict."""
        philosophers = [Hegel(), Kant(), Plato(), Dewey(), Aristotle()]
        lookup = _build_philosopher_lookup(philosophers)
        proposals = self._proposals()

        result = _collect_synthesis_counterarguments(
            proposals, SYNTHESIZER_PHILOSOPHERS, lookup
        )

        assert result, (
            "_collect_synthesis_counterarguments returned empty dict — "
            "synthesizer lookup by ID is broken"
        )

    def test_all_four_synthesizers_receive_combined_text(self):
        philosophers = [Hegel(), Kant(), Plato(), Dewey()]
        lookup = _build_philosopher_lookup(philosophers)
        proposals = self._proposals()

        result = _collect_synthesis_counterarguments(
            proposals, SYNTHESIZER_PHILOSOPHERS, lookup
        )

        assert set(result.keys()) == set(SYNTHESIZER_PHILOSOPHERS)

    def test_combined_text_contains_both_proposals(self):
        philosophers = [Hegel(), Kant(), Plato(), Dewey()]
        lookup = _build_philosopher_lookup(philosophers)
        proposals = self._proposals()

        result = _collect_synthesis_counterarguments(
            proposals, SYNTHESIZER_PHILOSOPHERS, lookup
        )

        for text in result.values():
            assert "Virtue is a mean" in text or "slave morality" in text

    def test_absent_synthesizer_excluded(self):
        """Only synthesizers that are actually in the lookup should appear."""
        philosophers = [Hegel()]  # only Hegel present
        lookup = _build_philosopher_lookup(philosophers)
        proposals = self._proposals()

        result = _collect_synthesis_counterarguments(
            proposals, SYNTHESIZER_PHILOSOPHERS, lookup
        )

        assert set(result.keys()) == {"hegel"}

    def test_empty_proposals_still_returns_entry(self):
        """Even with no proposals, synthesizers in lookup get an entry (empty combined)."""
        philosophers = [Hegel()]
        lookup = _build_philosopher_lookup(philosophers)
        result = _collect_synthesis_counterarguments(
            [], SYNTHESIZER_PHILOSOPHERS, lookup
        )
        # combined is "", but the key is present because Hegel is in lookup
        assert "hegel" in result


# ── Integration-style: synthesis path resolves synthesizers via ID ────────────


class TestSynthesisPathRePropose:
    """
    Directly exercise the synthesis path without going through InteractionMatrix
    (which may short-circuit via hi_pairs in round 2 before reaching round 3).

    The goal: given a lookup built with _build_philosopher_lookup and
    SYNTHESIZER_PHILOSOPHERS as ID keys, _re_propose must produce proposals.
    """

    def _ctx(self) -> Context:
        return Context.now(request_id=str(uuid.uuid4()), user_input="What is justice?")

    def test_re_propose_finds_synthesizers_by_id(self):
        """_re_propose resolves synthesizer instances from the ID-keyed lookup."""
        from po_core.deliberation.engine import _re_propose

        philosophers = [Hegel(), Kant(), Plato(), Dewey()]
        lookup = _build_philosopher_lookup(philosophers)

        current_proposals = [
            _make_proposal("Aristotle", "Justice is giving each their due."),
            _make_proposal("Nietzsche", "Justice is power in disguise."),
        ]
        combined = "\n\n".join(
            f"[{a}]: {p.content}"
            for p in current_proposals
            for a in [p.extra.get("_po_core", {}).get("author", "")]
            if p.content
        )
        counterarguments = {
            sid: combined for sid in SYNTHESIZER_PHILOSOPHERS if sid in lookup
        }

        ctx = self._ctx()
        intent = Intent.neutral()
        tensors = TensorSnapshot.now({"freedom_pressure": 0.0})
        memory = MemorySnapshot(items=[], summary=None, meta={})

        from po_core.deliberation.roles import DebateRole

        revised = _re_propose(
            lookup,
            counterarguments,
            ctx,
            intent,
            tensors,
            memory,
            round_num=3,
            role=DebateRole.SYNTHESIS,
        )

        assert revised, (
            "_re_propose returned no proposals for synthesis round — "
            "synthesizer philosophers were not found in the lookup"
        )
        assert len(revised) == len(
            SYNTHESIZER_PHILOSOPHERS
        ), f"Expected {len(SYNTHESIZER_PHILOSOPHERS)} synthesis proposals, got {len(revised)}"

    def test_re_propose_synthesis_proposals_carry_dialectic_role(self):
        """Synthesis proposals must have dialectic_role='synthesis' in extra."""
        from po_core.deliberation.engine import _re_propose
        from po_core.deliberation.roles import DebateRole

        philosophers = [Hegel()]
        lookup = _build_philosopher_lookup(philosophers)
        counterarguments = {"hegel": "debate content"}

        ctx = self._ctx()
        intent = Intent.neutral()
        tensors = TensorSnapshot.now({"freedom_pressure": 0.0})
        memory = MemorySnapshot(items=[], summary=None, meta={})

        revised = _re_propose(
            lookup,
            counterarguments,
            ctx,
            intent,
            tensors,
            memory,
            round_num=3,
            role=DebateRole.SYNTHESIS,
        )

        assert revised
        for p in revised:
            assert (
                p.extra.get("dialectic_role") == "synthesis"
            ), f"Expected dialectic_role='synthesis', got {p.extra.get('dialectic_role')!r}"
