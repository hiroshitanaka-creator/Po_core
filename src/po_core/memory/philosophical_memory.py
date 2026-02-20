"""
Philosophical Memory System  (Phase 6-D/E integration)
=======================================================

三層哲学的記憶の統合インターフェース。

  エピソード記憶: MemorySnapshot (既存) — 過去の会話履歴
  意味記憶:      SemanticMemoryStore   — 抽象化された概念知識 (Phase 6-D)
  手続き記憶:    ProceduralMemoryStore — 「どう考えるか」のパターン (Phase 6-E)

hexagonal アーキテクチャを保ちつつ、既存の MemoryReadPort / MemoryWritePort
インターフェースと互換な read/write メソッドを提供する。

Usage::

    from po_core.memory import PhilosophicalMemorySystem

    mem = PhilosophicalMemorySystem.create()

    # Read: consolidated memory bundle for current context
    bundle = mem.read_bundle(user_input="What is justice?", metrics={"ethics": 0.9})

    # Write: learn from pipeline run
    mem.consolidate_from_run(
        user_input="What is justice?",
        concept="justice",
        winning_philosophers=["Rawls", "Aristotle"],
        tensions=[("Kant", "Nietzsche", 0.8)],
        metrics={"ethics": 0.9},
        quality=0.85,
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from po_core.memory.procedural_store import (
    PhilosophicalProcedure,
    ProceduralMemoryStore,
)
from po_core.memory.semantic_store import SemanticMemoryEntry, SemanticMemoryStore

# ── PhilosophicalMemoryBundle ─────────────────────────────────────────


@dataclass
class PhilosophicalMemoryBundle:
    """
    Consolidated memory bundle returned by PhilosophicalMemorySystem.read_bundle().

    Contains entries from all three memory layers.

    Attributes:
        relevant_concepts:  Semantically similar concepts from SemanticMemoryStore.
        matched_procedures: Trigger-matching procedures from ProceduralMemoryStore.
        episodic_summary:   Optional plain-text summary of recent episodic memory.
        retrieved_at:       Timestamp of bundle creation.
    """

    relevant_concepts: List[Tuple[SemanticMemoryEntry, float]] = field(
        default_factory=list
    )
    matched_procedures: List[Tuple[PhilosophicalProcedure, float]] = field(
        default_factory=list
    )
    episodic_summary: Optional[str] = None
    retrieved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # ── Convenience accessors ─────────────────────────────────────────

    @property
    def top_concept(self) -> Optional[SemanticMemoryEntry]:
        """Highest-similarity semantic concept, or None."""
        return self.relevant_concepts[0][0] if self.relevant_concepts else None

    @property
    def top_procedure(self) -> Optional[PhilosophicalProcedure]:
        """Best-matching procedure, or None."""
        return self.matched_procedures[0][0] if self.matched_procedures else None

    @property
    def recommended_philosophers(self) -> List[str]:
        """
        Recommended philosophers from the best-matching procedure.

        Falls back to associated philosophers from the top concept.
        """
        if self.top_procedure:
            return list(self.top_procedure.recommended_philosophers)
        if self.top_concept:
            return list(self.top_concept.associated_philosophers)
        return []

    def has_memory(self) -> bool:
        """True if any memory layer returned results."""
        return bool(
            self.relevant_concepts or self.matched_procedures or self.episodic_summary
        )

    def to_dict(self) -> Dict:
        return {
            "retrieved_at": self.retrieved_at.isoformat(),
            "has_memory": self.has_memory(),
            "relevant_concepts": [
                {
                    "concept": e.concept,
                    "similarity": round(s, 4),
                    "confidence": e.confidence,
                }
                for e, s in self.relevant_concepts
            ],
            "matched_procedures": [
                {
                    "procedure_id": p.procedure_id,
                    "score": round(s, 4),
                    "recommended": p.recommended_philosophers,
                    "strategy": p.aggregation_strategy,
                }
                for p, s in self.matched_procedures
            ],
            "episodic_summary": self.episodic_summary,
        }


# ── PhilosophicalMemorySystem ─────────────────────────────────────────


class PhilosophicalMemorySystem:
    """
    三層哲学的記憶システムの統合インターフェース。

    Episodic memory is represented as a simple list of text summaries
    (lightweight stand-in; production systems can wire a full EpisodicStore).
    Semantic and procedural memory are held in dedicated stores.

    Args:
        semantic:    SemanticMemoryStore instance.
        procedural:  ProceduralMemoryStore instance.
        max_episodic: Maximum episodic items to retain.
    """

    def __init__(
        self,
        semantic: Optional[SemanticMemoryStore] = None,
        procedural: Optional[ProceduralMemoryStore] = None,
        max_episodic: int = 100,
    ) -> None:
        self.semantic = semantic or SemanticMemoryStore()
        self.procedural = procedural or ProceduralMemoryStore()
        self._episodic: List[Dict] = []  # lightweight episodic log
        self._max_episodic = max_episodic

    # ── Factory ───────────────────────────────────────────────────────

    @classmethod
    def create(cls) -> "PhilosophicalMemorySystem":
        """Create a fresh PhilosophicalMemorySystem with empty stores."""
        return cls()

    # ── Read (MemoryReadPort-compatible) ──────────────────────────────

    def read_bundle(
        self,
        user_input: str = "",
        metrics: Optional[Dict[str, float]] = None,
        top_k_concepts: int = 5,
        min_procedure_success: float = 0.0,
    ) -> PhilosophicalMemoryBundle:
        """
        Retrieve a consolidated memory bundle for the current context.

        Args:
            user_input:            Current user query (for semantic search).
            metrics:               Tensor dimension scores (for procedure matching).
            top_k_concepts:        How many semantic concepts to return.
            min_procedure_success: Filter procedures below this success rate.

        Returns:
            PhilosophicalMemoryBundle with all three memory layers populated.
        """
        # Semantic layer
        concepts = (
            self.semantic.search_by_text(user_input, top_k=top_k_concepts)
            if user_input
            else []
        )

        # Procedural layer
        procedures = (
            self.procedural.match(metrics, min_success_rate=min_procedure_success)
            if metrics
            else []
        )

        # Episodic summary (last few items)
        episodic_summary = None
        if self._episodic:
            recent = self._episodic[-3:]
            episodic_summary = "; ".join(
                e.get("summary", e.get("concept", "")) for e in recent if e
            )

        return PhilosophicalMemoryBundle(
            relevant_concepts=concepts,
            matched_procedures=procedures,
            episodic_summary=episodic_summary or None,
        )

    # ── Write (MemoryWritePort-compatible) ────────────────────────────

    def consolidate_from_run(
        self,
        user_input: str = "",
        concept: str = "",
        winning_philosophers: Optional[List[str]] = None,
        tensions: Optional[List[Tuple[str, str, float]]] = None,
        metrics: Optional[Dict[str, float]] = None,
        quality: float = 0.5,
        aggregation_strategy: str = "pareto",
    ) -> None:
        """
        Extract and store knowledge from a completed pipeline run.

        Updates all three memory layers:
          1. Episodic: append a summary of this run.
          2. Semantic: consolidate concept with new philosopher/tension info.
          3. Procedural: upsert a procedure from the observed metrics + outcome.

        Args:
            user_input:             User's query text.
            concept:                Central concept extracted from this run.
            winning_philosophers:   Philosophers whose proposals were selected.
            tensions:               Observed philosopher tension pairs.
            metrics:                Tensor dimension scores for this run.
            quality:                EthicalQualityScore.overall for this run.
            aggregation_strategy:   Strategy used in Pareto aggregation.
        """
        phs = list(winning_philosophers or [])
        ts = list(tensions or [])
        mets = dict(metrics or {})

        # 1. Episodic update
        self._episodic.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": concept or user_input[:80],
                "quality": round(quality, 4),
                "philosophers": phs[:5],
            }
        )
        if len(self._episodic) > self._max_episodic:
            self._episodic = self._episodic[-self._max_episodic :]

        # 2. Semantic update
        if concept:
            entry = self.semantic.consolidate(
                concept=concept,
                philosophers=phs,
                confidence_boost=0.05 + 0.1 * quality,
            )
            for t in ts:
                if len(t) == 3:
                    entry.add_tension(t[0], t[1], float(t[2]))

        # 3. Procedural update
        if mets:
            self.procedural.upsert_from_run(
                metrics=mets,
                winning_philosophers=phs,
                quality=quality,
                strategy=aggregation_strategy,
            )

    # ── Inspection ────────────────────────────────────────────────────

    def episodic_count(self) -> int:
        """Number of stored episodic items."""
        return len(self._episodic)

    def reset(self) -> None:
        """Clear all memory stores."""
        self.semantic.reset()
        self.procedural.reset()
        self._episodic.clear()

    def stats(self) -> Dict:
        """Summary statistics for all three layers."""
        return {
            "episodic_count": self.episodic_count(),
            "semantic_concepts": len(self.semantic),
            "procedural_count": len(self.procedural),
        }
