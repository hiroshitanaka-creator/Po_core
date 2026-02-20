"""
Phase 6-D/E: Philosophical Memory System — Unit Tests
======================================================

Tests for:
  - SemanticMemoryEntry (creation, mutation, serialisation)
  - SemanticMemoryStore (add, consolidate, search, high_confidence)
  - PhilosophicalProcedure (creation, matches, match_score, record_outcome)
  - ProceduralMemoryStore (add, match, upsert_from_run, top_procedures)
  - PhilosophicalMemoryBundle (accessors, to_dict)
  - PhilosophicalMemorySystem (read_bundle, consolidate_from_run, stats, reset)

Embedding strategy:
  Search tests monkeypatch po_core.memory.semantic_store._encode with
  _keyword_embed for deterministic behaviour regardless of sbert.
"""

from __future__ import annotations

import pytest

import po_core.memory.semantic_store as semantic_mod
from po_core.memory import (
    PhilosophicalMemoryBundle,
    PhilosophicalMemorySystem,
    PhilosophicalProcedure,
    ProceduralMemoryStore,
    SemanticMemoryEntry,
    SemanticMemoryStore,
)

# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture
def keyword_encode(monkeypatch):
    """Force keyword-bag encoder in semantic_store module."""
    monkeypatch.setattr(semantic_mod, "_encode", semantic_mod._keyword_embed)


@pytest.fixture
def store() -> SemanticMemoryStore:
    return SemanticMemoryStore()


@pytest.fixture
def proc_store() -> ProceduralMemoryStore:
    return ProceduralMemoryStore()


@pytest.fixture
def mem() -> PhilosophicalMemorySystem:
    return PhilosophicalMemorySystem.create()


# ── SemanticMemoryEntry ───────────────────────────────────────────────


class TestSemanticMemoryEntry:
    def test_creation_defaults(self):
        e = SemanticMemoryEntry(concept="justice")
        assert e.concept == "justice"
        assert e.formation_count == 1
        assert e.confidence == 0.5
        assert e.associated_philosophers == []
        assert e.typical_tensions == []
        assert e.entry_id != ""

    def test_unique_entry_ids(self):
        a = SemanticMemoryEntry(concept="a")
        b = SemanticMemoryEntry(concept="b")
        assert a.entry_id != b.entry_id

    def test_reinforce_increments_count(self):
        e = SemanticMemoryEntry(concept="duty")
        e.reinforce()
        assert e.formation_count == 2

    def test_reinforce_adds_philosophers(self):
        e = SemanticMemoryEntry(concept="duty", associated_philosophers=["Kant"])
        e.reinforce(["Mill", "Hegel"])
        assert "Mill" in e.associated_philosophers
        assert "Hegel" in e.associated_philosophers
        assert "Kant" in e.associated_philosophers

    def test_reinforce_no_duplicate_philosophers(self):
        e = SemanticMemoryEntry(concept="duty", associated_philosophers=["Kant"])
        e.reinforce(["Kant"])
        assert e.associated_philosophers.count("Kant") == 1

    def test_reinforce_boosts_confidence(self):
        e = SemanticMemoryEntry(concept="justice", confidence=0.5)
        e.reinforce(confidence_boost=0.1)
        assert abs(e.confidence - 0.6) < 0.001

    def test_reinforce_clamps_confidence_at_one(self):
        e = SemanticMemoryEntry(concept="justice", confidence=0.99)
        e.reinforce(confidence_boost=0.1)
        assert e.confidence <= 1.0

    def test_add_tension(self):
        e = SemanticMemoryEntry(concept="ethics")
        e.add_tension("Kant", "Nietzsche", 0.82)
        assert len(e.typical_tensions) == 1
        assert e.typical_tensions[0][2] == 0.82

    def test_add_tension_updates_existing(self):
        e = SemanticMemoryEntry(concept="ethics")
        e.add_tension("Kant", "Nietzsche", 0.82)
        e.add_tension("Kant", "Nietzsche", 0.91)
        # Latest value wins; no duplicate pair
        assert len(e.typical_tensions) == 1
        assert abs(e.typical_tensions[0][2] - 0.91) < 0.001

    def test_to_dict_keys(self):
        e = SemanticMemoryEntry(concept="truth")
        d = e.to_dict()
        for k in (
            "concept",
            "entry_id",
            "associated_philosophers",
            "typical_tensions",
            "formation_count",
            "last_activated",
            "confidence",
        ):
            assert k in d

    def test_to_dict_no_embedding(self):
        e = SemanticMemoryEntry(concept="beauty")
        d = e.to_dict()
        assert "_embedding" not in d


# ── SemanticMemoryStore ───────────────────────────────────────────────


class TestSemanticMemoryStore:
    def test_initially_empty(self, store):
        assert len(store) == 0
        assert store.all_entries() == []

    def test_add_single_entry(self, store):
        e = SemanticMemoryEntry(concept="virtue")
        store.add(e)
        assert len(store) == 1
        assert store.get("virtue") is e

    def test_add_reinforce_existing(self, store):
        store.add(
            SemanticMemoryEntry(concept="justice", associated_philosophers=["Rawls"])
        )
        store.add(
            SemanticMemoryEntry(
                concept="justice", associated_philosophers=["Aristotle"]
            )
        )
        # Only one entry; formation_count incremented
        assert len(store) == 1
        rec = store.get("justice")
        assert rec.formation_count == 2
        assert "Aristotle" in rec.associated_philosophers
        assert "Rawls" in rec.associated_philosophers

    def test_get_unknown_returns_none(self, store):
        assert store.get("nonexistent") is None

    def test_consolidate_creates_new(self, store):
        entry = store.consolidate("freedom", philosophers=["Sartre"])
        assert len(store) == 1
        assert entry.concept == "freedom"
        assert "Sartre" in entry.associated_philosophers

    def test_consolidate_reinforces_existing(self, store):
        store.consolidate("freedom", philosophers=["Sartre"])
        store.consolidate("freedom", philosophers=["Hegel"])
        assert len(store) == 1
        assert store.get("freedom").formation_count == 2

    def test_consolidate_adds_tension(self, store):
        store.consolidate("freedom", tension=("Sartre", "Kant", 0.75))
        e = store.get("freedom")
        assert any(t[0] in ("Sartre", "Kant") for t in e.typical_tensions)

    def test_search_empty_returns_empty(self, store, keyword_encode):
        results = store.search_by_text("justice", top_k=5)
        assert results == []

    def test_search_returns_results(self, store, keyword_encode):
        store.add(SemanticMemoryEntry(concept="justice duty moral"))
        store.add(SemanticMemoryEntry(concept="freedom choice autonomy"))
        results = store.search_by_text("justice moral duty", top_k=2)
        assert len(results) == 2
        # Most similar concept should be "justice duty moral"
        assert results[0][0].concept == "justice duty moral"

    def test_search_similarity_in_range(self, store, keyword_encode):
        store.add(SemanticMemoryEntry(concept="virtue ethics"))
        results = store.search_by_text("ethics virtue good", top_k=1)
        assert 0.0 <= results[0][1] <= 1.0

    def test_search_top_k_limits_results(self, store, keyword_encode):
        for i in range(10):
            store.add(SemanticMemoryEntry(concept=f"concept_{i}"))
        results = store.search_by_text("test", top_k=3)
        assert len(results) == 3

    def test_high_confidence_entries(self, store):
        store.add(SemanticMemoryEntry(concept="high", confidence=0.9))
        store.add(SemanticMemoryEntry(concept="low", confidence=0.3))
        high = store.high_confidence_entries(threshold=0.7)
        assert any(e.concept == "high" for e in high)
        assert not any(e.concept == "low" for e in high)

    def test_to_dict(self, store):
        store.add(SemanticMemoryEntry(concept="ethics"))
        d = store.to_dict()
        assert "ethics" in d

    def test_reset(self, store):
        store.add(SemanticMemoryEntry(concept="ethics"))
        store.reset()
        assert len(store) == 0


# ── PhilosophicalProcedure ────────────────────────────────────────────


class TestPhilosophicalProcedure:
    def test_creation_defaults(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.7})
        assert p.success_rate == 0.5
        assert p.sample_size == 0
        assert p.aggregation_strategy == "pareto"
        assert p.procedure_id != ""

    def test_unique_ids(self):
        a = PhilosophicalProcedure(trigger_condition={"ethics": 0.7})
        b = PhilosophicalProcedure(trigger_condition={"ethics": 0.7})
        assert a.procedure_id != b.procedure_id

    def test_matches_all_conditions_met(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.7, "choice": 0.5})
        assert p.matches({"ethics": 0.8, "choice": 0.6}) is True

    def test_matches_one_condition_unmet(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.7, "choice": 0.5})
        assert p.matches({"ethics": 0.8, "choice": 0.3}) is False

    def test_matches_missing_dimension_is_zero(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.5})
        assert p.matches({"choice": 0.9}) is False  # ethics missing → 0.0 < 0.5

    def test_matches_empty_condition_always_true(self):
        p = PhilosophicalProcedure(trigger_condition={})
        assert p.matches({"ethics": 0.5}) is True

    def test_match_score_all_met(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.5})
        score = p.match_score({"ethics": 1.0})
        assert score == 0.5  # excess = 1.0 - 0.5 = 0.5

    def test_match_score_unmet_returns_zero(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.7})
        assert p.match_score({"ethics": 0.3}) == 0.0

    def test_match_score_empty_condition(self):
        p = PhilosophicalProcedure(trigger_condition={})
        assert p.match_score({"ethics": 0.9}) == 0.0

    def test_record_outcome_success(self):
        p = PhilosophicalProcedure(
            trigger_condition={"ethics": 0.5}, success_rate=0.5, sample_size=2
        )
        p.record_outcome(True)
        assert p.sample_size == 3
        assert p.success_rate > 0.5  # moved toward 1.0

    def test_record_outcome_failure(self):
        p = PhilosophicalProcedure(
            trigger_condition={"ethics": 0.5}, success_rate=0.8, sample_size=4
        )
        p.record_outcome(False)
        assert p.success_rate < 0.8  # moved toward 0.0

    def test_record_outcome_updates_last_used(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.5})
        assert p.last_used is None
        p.record_outcome(True)
        assert p.last_used is not None

    def test_to_dict_keys(self):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.7})
        d = p.to_dict()
        for k in (
            "procedure_id",
            "trigger_condition",
            "recommended_philosophers",
            "aggregation_strategy",
            "success_rate",
            "sample_size",
            "last_used",
        ):
            assert k in d


# ── ProceduralMemoryStore ─────────────────────────────────────────────


class TestProceduralMemoryStore:
    def test_initially_empty(self, proc_store):
        assert len(proc_store) == 0

    def test_add_and_get(self, proc_store):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.7})
        proc_store.add(p)
        assert proc_store.get(p.procedure_id) is p

    def test_match_returns_matching(self, proc_store):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.6})
        proc_store.add(p)
        results = proc_store.match({"ethics": 0.9})
        assert len(results) == 1
        assert results[0][0] is p

    def test_match_excludes_nonmatching(self, proc_store):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.8})
        proc_store.add(p)
        results = proc_store.match({"ethics": 0.5})
        assert len(results) == 0

    def test_match_sorted_by_score(self, proc_store):
        # Two matching procedures with different conditions (different excess)
        p1 = PhilosophicalProcedure(trigger_condition={"ethics": 0.3}, success_rate=0.9)
        p2 = PhilosophicalProcedure(trigger_condition={"ethics": 0.7}, success_rate=0.9)
        proc_store.add(p1)
        proc_store.add(p2)
        results = proc_store.match({"ethics": 0.9})
        assert len(results) == 2
        scores = [s for _, s in results]
        assert scores == sorted(scores, reverse=True)

    def test_match_min_success_filter(self, proc_store):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.5}, success_rate=0.2)
        proc_store.add(p)
        results = proc_store.match({"ethics": 0.9}, min_success_rate=0.5)
        assert len(results) == 0

    def test_record_outcome(self, proc_store):
        p = PhilosophicalProcedure(trigger_condition={"ethics": 0.5})
        proc_store.add(p)
        success = proc_store.record_outcome(p.procedure_id, True)
        assert success is True
        assert proc_store.get(p.procedure_id).sample_size == 1

    def test_record_outcome_unknown_returns_false(self, proc_store):
        assert proc_store.record_outcome("nonexistent", True) is False

    def test_upsert_creates_new_procedure(self, proc_store):
        proc = proc_store.upsert_from_run(
            metrics={"ethics": 0.8},
            winning_philosophers=["Kant"],
            quality=0.85,
        )
        assert proc is not None
        assert len(proc_store) == 1
        assert "Kant" in proc.recommended_philosophers

    def test_upsert_reinforces_existing(self, proc_store):
        proc_store.upsert_from_run(
            metrics={"ethics": 0.8},
            winning_philosophers=["Kant"],
            quality=0.85,
        )
        proc_store.upsert_from_run(
            metrics={"ethics": 0.85},
            winning_philosophers=["Mill"],
            quality=0.80,
        )
        # Should reinforce existing procedure, not create new one
        assert len(proc_store) == 1

    def test_upsert_empty_metrics_returns_none(self, proc_store):
        result = proc_store.upsert_from_run(
            metrics={},
            winning_philosophers=["Kant"],
            quality=0.85,
        )
        assert result is None

    def test_top_procedures_sorted(self, proc_store):
        p1 = PhilosophicalProcedure(
            trigger_condition={"a": 0.5}, success_rate=0.9, sample_size=10
        )
        p2 = PhilosophicalProcedure(
            trigger_condition={"b": 0.5}, success_rate=0.5, sample_size=10
        )
        proc_store.add(p1)
        proc_store.add(p2)
        top = proc_store.top_procedures(n=2)
        assert top[0][0] is p1  # higher success_rate

    def test_reset(self, proc_store):
        proc_store.add(PhilosophicalProcedure(trigger_condition={"ethics": 0.5}))
        proc_store.reset()
        assert len(proc_store) == 0


# ── PhilosophicalMemoryBundle ─────────────────────────────────────────


class TestPhilosophicalMemoryBundle:
    def test_empty_bundle(self):
        b = PhilosophicalMemoryBundle()
        assert b.has_memory() is False
        assert b.top_concept is None
        assert b.top_procedure is None
        assert b.recommended_philosophers == []

    def test_top_concept_from_semantic(self):
        e = SemanticMemoryEntry(concept="justice", associated_philosophers=["Rawls"])
        b = PhilosophicalMemoryBundle(relevant_concepts=[(e, 0.9)])
        assert b.top_concept is e

    def test_top_procedure_from_procedural(self):
        p = PhilosophicalProcedure(
            trigger_condition={"ethics": 0.7},
            recommended_philosophers=["Kant"],
        )
        b = PhilosophicalMemoryBundle(matched_procedures=[(p, 0.8)])
        assert b.top_procedure is p

    def test_recommended_philosophers_from_procedure(self):
        p = PhilosophicalProcedure(
            trigger_condition={},
            recommended_philosophers=["Kant", "Mill"],
        )
        b = PhilosophicalMemoryBundle(matched_procedures=[(p, 0.8)])
        assert b.recommended_philosophers == ["Kant", "Mill"]

    def test_recommended_philosophers_fallback_to_concept(self):
        e = SemanticMemoryEntry(concept="justice", associated_philosophers=["Rawls"])
        b = PhilosophicalMemoryBundle(relevant_concepts=[(e, 0.9)])
        assert "Rawls" in b.recommended_philosophers

    def test_has_memory_with_episodic(self):
        b = PhilosophicalMemoryBundle(episodic_summary="previous justice debate")
        assert b.has_memory() is True

    def test_to_dict_keys(self):
        b = PhilosophicalMemoryBundle()
        d = b.to_dict()
        for k in (
            "retrieved_at",
            "has_memory",
            "relevant_concepts",
            "matched_procedures",
            "episodic_summary",
        ):
            assert k in d


# ── PhilosophicalMemorySystem ─────────────────────────────────────────


class TestPhilosophicalMemorySystem:
    def test_create_fresh(self, mem):
        assert mem.episodic_count() == 0
        assert len(mem.semantic) == 0
        assert len(mem.procedural) == 0

    def test_stats_empty(self, mem):
        s = mem.stats()
        assert s["episodic_count"] == 0
        assert s["semantic_concepts"] == 0
        assert s["procedural_count"] == 0

    def test_consolidate_updates_episodic(self, mem):
        mem.consolidate_from_run(concept="justice", quality=0.8)
        assert mem.episodic_count() == 1

    def test_consolidate_updates_semantic(self, mem):
        mem.consolidate_from_run(
            concept="justice",
            winning_philosophers=["Rawls"],
            quality=0.8,
        )
        assert len(mem.semantic) == 1
        assert mem.semantic.get("justice") is not None

    def test_consolidate_updates_procedural(self, mem):
        mem.consolidate_from_run(
            metrics={"ethics": 0.9},
            winning_philosophers=["Kant"],
            quality=0.85,
        )
        assert len(mem.procedural) == 1

    def test_consolidate_no_concept_no_semantic_entry(self, mem):
        mem.consolidate_from_run(
            metrics={"ethics": 0.9},
            quality=0.85,
        )
        assert len(mem.semantic) == 0

    def test_read_bundle_returns_bundle(self, mem, keyword_encode):
        mem.consolidate_from_run(
            concept="justice duty moral",
            winning_philosophers=["Rawls"],
            quality=0.8,
        )
        bundle = mem.read_bundle(user_input="justice duty")
        assert isinstance(bundle, PhilosophicalMemoryBundle)

    def test_read_bundle_semantic_results(self, mem, keyword_encode):
        mem.consolidate_from_run(
            concept="justice duty moral",
            winning_philosophers=["Rawls"],
            quality=0.8,
        )
        bundle = mem.read_bundle(user_input="justice moral duty")
        # The "justice duty moral" concept should be found
        assert bundle.top_concept is not None
        assert bundle.top_concept.concept == "justice duty moral"

    def test_read_bundle_procedural_results(self, mem):
        mem.consolidate_from_run(
            metrics={"ethics": 0.9},
            winning_philosophers=["Kant"],
            quality=0.85,
        )
        bundle = mem.read_bundle(metrics={"ethics": 0.95})
        assert bundle.top_procedure is not None

    def test_read_bundle_episodic_summary(self, mem, keyword_encode):
        mem.consolidate_from_run(concept="justice", quality=0.8)
        bundle = mem.read_bundle(user_input="justice")
        assert bundle.episodic_summary is not None

    def test_read_bundle_empty_system(self, mem, keyword_encode):
        bundle = mem.read_bundle(user_input="justice", metrics={"ethics": 0.9})
        assert bundle.has_memory() is False

    def test_multiple_consolidations_accumulate(self, mem):
        for concept in ["justice", "freedom", "virtue"]:
            mem.consolidate_from_run(concept=concept, quality=0.8)
        assert mem.episodic_count() == 3
        assert len(mem.semantic) == 3

    def test_reset_clears_all(self, mem):
        mem.consolidate_from_run(
            concept="justice", metrics={"ethics": 0.8}, quality=0.8
        )
        mem.reset()
        assert mem.episodic_count() == 0
        assert len(mem.semantic) == 0
        assert len(mem.procedural) == 0
