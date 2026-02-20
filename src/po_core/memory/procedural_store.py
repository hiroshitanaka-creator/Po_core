"""
Procedural Memory Store  (Phase 6-E)
======================================

手続き記憶: 「このタイプの問いにはこのアプローチが有効」というパターン知識。

人間の哲学者が「倫理的ジレンマを議論するときは義務論と功利主義を対比する
と生産的だ」という暗黙知を持つように、Po_core が推論パターンを学習する。

Architecture:
  PhilosophicalProcedure  — 1つの手続き知識エントリ
  ProceduralMemoryStore   — エントリ群の管理・テンソル条件マッチング

Usage::

    store = ProceduralMemoryStore()
    proc = PhilosophicalProcedure(
        procedure_id="ethics_dilemma_v1",
        trigger_condition={"ethics": 0.7},
        recommended_philosophers=["Kant", "Mill", "Levinas"],
        aggregation_strategy="tension_first",
    )
    store.add(proc)
    matches = store.match({"ethics": 0.85, "choice": 0.4})
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# ── PhilosophicalProcedure ────────────────────────────────────────────


@dataclass
class PhilosophicalProcedure:
    """
    One procedural memory entry: a situation → action pattern.

    Attributes:
        procedure_id:             Unique identifier.
        trigger_condition:        Dict of {tensor_dimension: min_threshold}.
                                  Procedure matches when ALL conditions are met.
        recommended_philosophers: Philosopher names to prioritise in this context.
        aggregation_strategy:     "pareto" | "consensus_first" | "tension_first".
        success_rate:             Fraction of past uses that produced quality > 0.7.
        sample_size:              Total times this procedure was applied.
        last_used:                Timestamp of most recent application.
        description:              Optional human-readable rationale.
    """

    trigger_condition: Dict[str, float]
    recommended_philosophers: List[str] = field(default_factory=list)
    aggregation_strategy: str = "pareto"
    success_rate: float = 0.5
    sample_size: int = 0
    procedure_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    last_used: Optional[datetime] = None
    description: str = ""

    # ── Match ─────────────────────────────────────────────────────────

    def matches(self, metrics: Dict[str, float]) -> bool:
        """
        Return True if all trigger conditions are satisfied by metrics.

        A dimension that is absent in metrics is treated as 0.0.
        """
        for dim, threshold in self.trigger_condition.items():
            if metrics.get(dim, 0.0) < threshold:
                return False
        return True

    def match_score(self, metrics: Dict[str, float]) -> float:
        """
        Continuous match score: mean excess over threshold across all conditions.

        0.0 = exactly at threshold, 1.0 = all conditions exceeded by 1.0.
        Returns 0.0 if any condition is unmet (use matches() first).
        """
        if not self.trigger_condition:
            return 0.0
        excesses = []
        for dim, threshold in self.trigger_condition.items():
            val = metrics.get(dim, 0.0)
            if val < threshold:
                return 0.0
            excesses.append(val - threshold)
        return min(1.0, sum(excesses) / len(excesses))

    # ── Update ────────────────────────────────────────────────────────

    def record_outcome(self, success: bool) -> None:
        """Update success_rate with a new outcome using running average."""
        self.sample_size += 1
        # Incremental mean update
        self.success_rate = (
            self.success_rate * (self.sample_size - 1) + (1.0 if success else 0.0)
        ) / self.sample_size
        self.success_rate = round(self.success_rate, 4)
        self.last_used = datetime.now(timezone.utc)

    # ── Serialisation ─────────────────────────────────────────────────

    def to_dict(self) -> Dict:
        return {
            "procedure_id": self.procedure_id,
            "trigger_condition": dict(self.trigger_condition),
            "recommended_philosophers": list(self.recommended_philosophers),
            "aggregation_strategy": self.aggregation_strategy,
            "success_rate": round(self.success_rate, 4),
            "sample_size": self.sample_size,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "description": self.description,
        }


# ── ProceduralMemoryStore ─────────────────────────────────────────────


class ProceduralMemoryStore:
    """
    In-memory procedural knowledge store with tensor-condition matching.

    Stores philosopher approach patterns keyed by trigger conditions.
    Matched procedures are ranked by success_rate × match_score.
    """

    def __init__(self) -> None:
        self._procedures: Dict[str, PhilosophicalProcedure] = {}

    # ── Mutation ──────────────────────────────────────────────────────

    def add(self, procedure: PhilosophicalProcedure) -> None:
        """Add or replace a procedure by its procedure_id."""
        self._procedures[procedure.procedure_id] = procedure

    def record_outcome(self, procedure_id: str, success: bool) -> bool:
        """
        Update the outcome of a procedure.

        Returns:
            True if procedure was found and updated, False otherwise.
        """
        proc = self._procedures.get(procedure_id)
        if proc is None:
            return False
        proc.record_outcome(success)
        return True

    def upsert_from_run(
        self,
        metrics: Dict[str, float],
        winning_philosophers: List[str],
        quality: float,
        strategy: str = "pareto",
        min_threshold: float = 0.5,
    ) -> Optional[PhilosophicalProcedure]:
        """
        Create or reinforce a procedure from a pipeline run result.

        Extracts trigger conditions from metrics (dimensions > min_threshold),
        then looks for an existing matching procedure to reinforce or creates
        a new one.

        Args:
            metrics:               Tensor dimension scores from TensorSnapshot.
            winning_philosophers:  Philosophers whose proposals were selected.
            quality:               Overall EthicalQualityScore.overall.
            strategy:              Aggregation strategy used.
            min_threshold:         Minimum tensor score to include as trigger.

        Returns:
            The created or updated PhilosophicalProcedure.
        """
        trigger = {k: round(v, 2) for k, v in metrics.items() if v >= min_threshold}
        if not trigger:
            return None

        # Find the existing procedure with the highest match score
        matches = self.match(metrics)
        if matches:
            proc, _ = matches[0]
            proc.record_outcome(quality >= 0.7)
            # Reinforce philosopher recommendations
            for ph in winning_philosophers:
                if ph and ph not in proc.recommended_philosophers:
                    proc.recommended_philosophers.append(ph)
            return proc

        # Create new procedure
        new_proc = PhilosophicalProcedure(
            trigger_condition=trigger,
            recommended_philosophers=list(winning_philosophers),
            aggregation_strategy=strategy,
            success_rate=1.0 if quality >= 0.7 else 0.0,
            sample_size=1,
            last_used=datetime.now(timezone.utc),
        )
        self.add(new_proc)
        return new_proc

    # ── Query ─────────────────────────────────────────────────────────

    def match(
        self,
        metrics: Dict[str, float],
        min_success_rate: float = 0.0,
    ) -> List[Tuple[PhilosophicalProcedure, float]]:
        """
        Return all procedures whose trigger conditions are met by metrics,
        ranked by (success_rate × match_score) descending.

        Args:
            metrics:          Tensor dimension scores to match against.
            min_success_rate: Filter out procedures with success_rate below this.

        Returns:
            List of (procedure, composite_score) sorted descending.
        """
        results = []
        for proc in self._procedures.values():
            if proc.success_rate < min_success_rate:
                continue
            if not proc.matches(metrics):
                continue
            score = proc.success_rate * proc.match_score(metrics)
            results.append((proc, round(score, 4)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get(self, procedure_id: str) -> Optional[PhilosophicalProcedure]:
        return self._procedures.get(procedure_id)

    def top_procedures(self, n: int = 5) -> List[Tuple[PhilosophicalProcedure, float]]:
        """Return top-N procedures by success_rate × sample_size (reliability)."""
        ranked = [
            (p, p.success_rate * min(1.0, p.sample_size / 10))
            for p in self._procedures.values()
        ]
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:n]

    # ── Inspection ────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._procedures)

    def all_procedures(self) -> List[PhilosophicalProcedure]:
        return list(self._procedures.values())

    def to_dict(self) -> Dict:
        return {pid: p.to_dict() for pid, p in self._procedures.items()}

    def reset(self) -> None:
        self._procedures.clear()
