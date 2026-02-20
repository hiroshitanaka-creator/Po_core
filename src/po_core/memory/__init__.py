"""
Po_core Philosophical Memory  (Phase 6-D/E)
============================================

三層哲学的記憶システム:

  Layer 1 — Episodic:   MemorySnapshot (既存) — 会話履歴
  Layer 2 — Semantic:   SemanticMemoryStore   — 概念知識 (Phase 6-D)
  Layer 3 — Procedural: ProceduralMemoryStore — 行動パターン (Phase 6-E)

Usage::

    from po_core.memory import (
        PhilosophicalMemorySystem,
        PhilosophicalMemoryBundle,
        SemanticMemoryEntry,
        SemanticMemoryStore,
        PhilosophicalProcedure,
        ProceduralMemoryStore,
    )

    mem = PhilosophicalMemorySystem.create()
    mem.consolidate_from_run(
        concept="justice",
        winning_philosophers=["Rawls", "Aristotle"],
        metrics={"ethics": 0.9},
        quality=0.85,
    )
    bundle = mem.read_bundle(user_input="What is justice?", metrics={"ethics": 0.9})
    print(bundle.top_concept.concept)        # "justice"
    print(bundle.recommended_philosophers)   # ["Rawls", "Aristotle"]
"""

from po_core.memory.philosophical_memory import (
    PhilosophicalMemoryBundle,
    PhilosophicalMemorySystem,
)
from po_core.memory.procedural_store import (
    PhilosophicalProcedure,
    ProceduralMemoryStore,
)
from po_core.memory.semantic_store import SemanticMemoryEntry, SemanticMemoryStore

__all__ = [
    "PhilosophicalMemoryBundle",
    "PhilosophicalMemorySystem",
    "PhilosophicalProcedure",
    "ProceduralMemoryStore",
    "SemanticMemoryEntry",
    "SemanticMemoryStore",
]
