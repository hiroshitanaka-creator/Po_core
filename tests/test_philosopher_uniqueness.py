"""
Philosopher Semantic Uniqueness Assessment
============================================

Phase 1, Task 5: Assess each philosopher's semantic uniqueness to
prevent homogenization when scaling to 39 philosophers.

Tests:
- All 39 produce distinct outputs (no duplicates)
- Vocabulary diversity across philosophers
- Philosophical tradition coverage (West, East, analytic, continental, etc.)
- Each philosopher produces consistent perspective across prompts
- No two philosophers share identical reasoning patterns
"""

from __future__ import annotations

import uuid
from collections import Counter
from typing import Dict, List, Set

import pytest

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_mode import SafetyMode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.base import Philosopher
from po_core.philosophers.manifest import SPECS
from po_core.philosophers.registry import PhilosopherRegistry

# ── Helpers ──


def _ctx(text: str = "What is the nature of consciousness?") -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text)


def _intent() -> Intent:
    return Intent.neutral()


def _tensors() -> TensorSnapshot:
    return TensorSnapshot.now({"freedom_pressure": 0.0})


def _memory() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


PHILOSOPHER_IDS = [
    s.philosopher_id for s in SPECS if s.enabled and s.philosopher_id != "dummy"
]


@pytest.fixture(scope="module")
def registry():
    return PhilosopherRegistry(cache_instances=True)


@pytest.fixture(scope="module")
def all_philosophers(registry):
    sel = registry.select(SafetyMode.NORMAL)
    philosophers, _ = registry.load(sel.selected_ids)
    return [p for p in philosophers if isinstance(p, Philosopher)]


@pytest.fixture(scope="module")
def all_proposals(all_philosophers):
    """Run all philosophers once and cache results."""
    results = {}
    ctx = _ctx()
    intent = _intent()
    tensors = _tensors()
    memory = _memory()
    for ph in all_philosophers:
        proposals = ph.propose(ctx, intent, tensors, memory)
        if proposals:
            results[ph.name] = proposals[0]
    return results


@pytest.fixture(scope="module")
def all_reason_results(all_philosophers):
    """Run reason() for all philosophers and cache results."""
    results = {}
    for ph in all_philosophers:
        result = ph.reason("What is the nature of consciousness?")
        results[ph.name] = result
    return results


# ══════════════════════════════════════════════════════════════════════════
# 1. Output Uniqueness
# ══════════════════════════════════════════════════════════════════════════


class TestOutputUniqueness:
    """Verify that all 39 philosophers produce distinct outputs."""

    def test_no_duplicate_content(self, all_proposals):
        """No two philosophers should produce identical proposal content."""
        contents = {}
        for name, proposal in all_proposals.items():
            content = proposal.content
            for other_name, other_content in contents.items():
                assert (
                    content != other_content
                ), f"{name} and {other_name} produced identical content"
            contents[name] = content

    def test_sufficient_philosopher_count(self, all_proposals):
        """Should have proposals from at least 30 philosophers."""
        assert (
            len(all_proposals) >= 30
        ), f"Only {len(all_proposals)} philosophers produced proposals (expected 30+)"

    def test_no_trivially_short_content(self, all_proposals):
        """Every philosopher should produce substantive content (>20 chars)."""
        for name, proposal in all_proposals.items():
            assert (
                len(proposal.content) > 20
            ), f"{name} produced trivially short content: '{proposal.content[:50]}'"


# ══════════════════════════════════════════════════════════════════════════
# 2. Vocabulary Diversity
# ══════════════════════════════════════════════════════════════════════════


class TestVocabularyDiversity:
    """Verify lexical diversity across philosophers."""

    @staticmethod
    def _extract_words(text: str) -> Set[str]:
        """Extract unique lowercase words from text."""
        return {
            w.strip(".,!?\"'()[]{}:;")
            for w in text.lower().split()
            if len(w.strip(".,!?\"'()[]{}:;")) > 2
        }

    def test_collective_vocabulary_size(self, all_proposals):
        """39 philosophers together should have a rich vocabulary."""
        all_words: Set[str] = set()
        for proposal in all_proposals.values():
            all_words |= self._extract_words(proposal.content)

        # 39 diverse philosophers should collectively use 200+ unique words
        assert (
            len(all_words) >= 200
        ), f"Collective vocabulary only {len(all_words)} words (expected 200+)"

    def test_each_philosopher_contributes_unique_words(self, all_proposals):
        """Each philosopher should contribute at least some unique vocabulary."""
        all_word_sets = {
            name: self._extract_words(p.content) for name, p in all_proposals.items()
        }

        # Count how many philosophers have at least 1 word unique to them
        unique_count = 0
        for name, words in all_word_sets.items():
            other_words = set()
            for other_name, other_ws in all_word_sets.items():
                if other_name != name:
                    other_words |= other_ws
            unique_to_philosopher = words - other_words
            if unique_to_philosopher:
                unique_count += 1

        # At least 50% of philosophers should have some unique vocabulary
        assert (
            unique_count >= len(all_proposals) * 0.5
        ), f"Only {unique_count}/{len(all_proposals)} philosophers have unique words"


# ══════════════════════════════════════════════════════════════════════════
# 3. Tradition Coverage
# ══════════════════════════════════════════════════════════════════════════


class TestTraditionCoverage:
    """Verify representation across philosophical traditions."""

    def test_multiple_traditions_represented(self, all_philosophers):
        """Should have philosophers from at least 5 distinct traditions."""
        traditions = set()
        for ph in all_philosophers:
            if hasattr(ph, "tradition") and ph.tradition:
                # Take the first word/phrase as tradition family
                traditions.add(ph.tradition.lower())

        assert len(traditions) >= 5, f"Only {len(traditions)} traditions: {traditions}"

    def test_eastern_traditions_present(self, all_philosophers):
        """Should include Eastern philosophical traditions."""
        eastern_keywords = {
            "confuci",
            "eastern",
            "zen",
            "buddhis",
            "daoism",
            "taoism",
            "japanese",
            "chinese",
            "wabi",
            "watsuji",
            "asian",
        }
        has_eastern = False
        for ph in all_philosophers:
            tradition = getattr(ph, "tradition", "").lower()
            if any(kw in tradition for kw in eastern_keywords):
                has_eastern = True
                break
        assert has_eastern, "No Eastern philosophical tradition found"

    def test_western_traditions_present(self, all_philosophers):
        """Should include Western philosophical traditions."""
        western_keywords = {
            "greek",
            "western",
            "german",
            "european",
            "french",
            "british",
            "continental",
            "analytic",
            "virtue",
            "enlightenment",
        }
        has_western = False
        for ph in all_philosophers:
            tradition = getattr(ph, "tradition", "").lower()
            if any(kw in tradition for kw in western_keywords):
                has_western = True
                break
        assert has_western, "No Western philosophical tradition found"

    def test_risk_level_distribution(self):
        """Risk levels should be distributed across all three levels."""
        risk_counts = Counter()
        for spec in SPECS:
            if spec.enabled and spec.philosopher_id != "dummy":
                risk_counts[spec.risk_level] += 1

        assert (
            risk_counts[0] >= 5
        ), f"Too few safe (risk=0) philosophers: {risk_counts[0]}"
        assert (
            risk_counts[1] >= 10
        ), f"Too few standard (risk=1) philosophers: {risk_counts[1]}"
        assert (
            risk_counts[2] >= 5
        ), f"Too few risky (risk=2) philosophers: {risk_counts[2]}"


# ══════════════════════════════════════════════════════════════════════════
# 4. Perspective Consistency
# ══════════════════════════════════════════════════════════════════════════


class TestPerspectiveConsistency:
    """Verify each philosopher maintains a consistent perspective."""

    def test_perspective_field_present(self, all_reason_results):
        """Each philosopher's reason() should include perspective-like content."""
        for name, result in all_reason_results.items():
            # Check for perspective or equivalent
            has_perspective = any(
                key in result
                for key in (
                    "perspective",
                    "approach",
                    "analysis",
                    "framework",
                    "summary",
                )
            )
            assert (
                has_perspective
            ), f"{name} reason() lacks perspective field. Keys: {list(result.keys())}"

    def test_philosopher_produces_different_outputs_for_different_prompts(self):
        """Same philosopher should produce meaningfully different outputs for different prompts.

        Uses prompts containing keywords that trigger distinct virtue-detection
        paths in Aristotle's template-based reason() (courage vs justice).
        """
        from po_core.philosophers.aristotle import Aristotle

        ph = Aristotle()
        r1 = ph.reason("We must show courage and bravely confront this challenge")
        r2 = ph.reason("Justice demands that we treat all people fairly and equally")

        # Should produce different reasoning (different virtue keywords detected)
        c1 = r1.get("reasoning", r1.get("analysis", ""))
        c2 = r2.get("reasoning", r2.get("analysis", ""))

        if isinstance(c1, str) and isinstance(c2, str) and c1 and c2:
            assert (
                c1 != c2
            ), "Aristotle produced identical reasoning for different prompts"


# ══════════════════════════════════════════════════════════════════════════
# 5. Anti-Homogenization
# ══════════════════════════════════════════════════════════════════════════


class TestAntiHomogenization:
    """Verify philosophers don't converge to similar outputs."""

    @staticmethod
    def _jaccard_similarity(a: Set[str], b: Set[str]) -> float:
        """Compute Jaccard similarity between two word sets."""
        if not a and not b:
            return 1.0
        intersection = len(a & b)
        union = len(a | b)
        return intersection / union if union > 0 else 0.0

    def test_no_pair_has_high_similarity(self, all_proposals):
        """No two philosophers should have Jaccard similarity > 0.8."""
        word_sets = {}
        for name, p in all_proposals.items():
            words = {
                w.strip(".,!?\"'()[]{}:;").lower()
                for w in p.content.split()
                if len(w.strip(".,!?\"'()[]{}:;")) > 3
            }
            word_sets[name] = words

        names = list(word_sets.keys())
        high_similarity_pairs = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                sim = self._jaccard_similarity(word_sets[names[i]], word_sets[names[j]])
                if sim > 0.8:
                    high_similarity_pairs.append((names[i], names[j], sim))

        assert (
            len(high_similarity_pairs) == 0
        ), f"Found {len(high_similarity_pairs)} highly similar pairs: " + ", ".join(
            f"{a} ↔ {b} ({s:.2f})" for a, b, s in high_similarity_pairs[:5]
        )

    def test_mean_pairwise_similarity_low(self, all_proposals):
        """Mean pairwise Jaccard similarity should be < 0.4 (low overlap)."""
        word_sets = {}
        for name, p in all_proposals.items():
            words = {
                w.strip(".,!?\"'()[]{}:;").lower()
                for w in p.content.split()
                if len(w.strip(".,!?\"'()[]{}:;")) > 3
            }
            word_sets[name] = words

        names = list(word_sets.keys())
        similarities = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                sim = self._jaccard_similarity(word_sets[names[i]], word_sets[names[j]])
                similarities.append(sim)

        if similarities:
            mean_sim = sum(similarities) / len(similarities)
            assert (
                mean_sim < 0.4
            ), f"Mean pairwise Jaccard similarity {mean_sim:.3f} is too high (> 0.4)"

    def test_key_concepts_diversity(self, all_philosophers):
        """Philosophers should have diverse key_concepts."""
        all_concepts: List[str] = []
        for ph in all_philosophers:
            concepts = getattr(ph, "key_concepts", [])
            all_concepts.extend(concepts)

        # Should have many unique concepts
        unique_concepts = set(c.lower() for c in all_concepts)
        assert (
            len(unique_concepts) >= 50
        ), f"Only {len(unique_concepts)} unique key_concepts across all philosophers (expected 50+)"
