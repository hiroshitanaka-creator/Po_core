"""
Proposal - Philosopher proposals for action or reasoning.

This is what philosophers OUTPUT after reasoning.
Proposals can be aggregated, compared, and passed through safety gates.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ProposalSource(str, Enum):
    """Source of a proposal."""

    PHILOSOPHER = "philosopher"  # From a philosopher module
    AGGREGATOR = "aggregator"  # Aggregated from multiple proposals
    SOLAR_WILL = "solar_will"  # From the Solar Will autonomy system
    REPAIRED = "repaired"  # After safety gate repair
    USER = "user"  # Direct from user input


@dataclass
class Rationale:
    """
    Structured rationale for a proposal.

    Separates the "what" (proposal text) from the "why" (rationale).
    """

    summary: str
    """One-sentence summary of the rationale."""

    reasoning: str
    """Full reasoning text."""

    perspective: str
    """The philosophical perspective applied."""

    key_concepts: List[str] = field(default_factory=list)
    """Key philosophical concepts invoked."""

    tensions: List[str] = field(default_factory=list)
    """Identified tensions or contradictions."""

    confidence: float = 0.5
    """Confidence level in [0, 1]."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "summary": self.summary,
            "reasoning": self.reasoning,
            "perspective": self.perspective,
            "key_concepts": self.key_concepts,
            "tensions": self.tensions,
            "confidence": self.confidence,
        }


@dataclass
class Proposal:
    """
    A proposal from a philosopher or aggregation process.

    This is the core output type that flows through the system:
    philosopher -> aggregator -> safety gate -> output

    Attributes:
        proposal_id: Unique identifier for this proposal
        text: The proposal text (action, response, reasoning)
        rationale: Structured rationale explaining the proposal
        source: Where this proposal came from
        source_id: Identifier of the specific source (e.g., philosopher name)
        created_at: When this proposal was created
        context_id: ID of the Context that produced this proposal
        parent_ids: IDs of proposals this was derived from (for aggregation)
        scores: Multi-axis scores from evaluation
        metadata: Additional unstructured metadata
    """

    text: str
    """The proposal text."""

    rationale: Rationale
    """Structured rationale for the proposal."""

    source: ProposalSource
    """Source type of the proposal."""

    source_id: str
    """Specific source identifier (e.g., 'aristotle', 'weighted_vote')."""

    proposal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """Unique proposal identifier."""

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    """Creation timestamp."""

    context_id: Optional[str] = None
    """ID of the context that produced this proposal."""

    parent_ids: List[str] = field(default_factory=list)
    """Parent proposal IDs (for aggregated proposals)."""

    scores: Dict[str, float] = field(default_factory=dict)
    """Multi-axis scores (e.g., {"A": 0.8, "B": 0.7})."""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata."""

    @classmethod
    def from_philosopher(
        cls,
        text: str,
        reasoning: str,
        perspective: str,
        philosopher_name: str,
        context_id: Optional[str] = None,
        tension: Optional[Any] = None,
        confidence: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Proposal":
        """
        Create a proposal from a philosopher's reasoning output.

        This is a convenience factory for converting philosopher output
        to the standardized Proposal format.
        """
        tensions = []
        if tension:
            if isinstance(tension, dict) and "elements" in tension:
                tensions = tension.get("elements", [])
            elif isinstance(tension, str):
                tensions = [tension]
            elif isinstance(tension, list):
                tensions = [str(t) for t in tension]

        rationale = Rationale(
            summary=f"Analysis from {perspective}",
            reasoning=reasoning,
            perspective=perspective,
            tensions=tensions,
            confidence=confidence,
        )

        return cls(
            text=text if text else reasoning[:500],  # Use reasoning if no separate text
            rationale=rationale,
            source=ProposalSource.PHILOSOPHER,
            source_id=philosopher_name.lower().replace(" ", "_"),
            context_id=context_id,
            metadata=metadata or {},
        )

    @classmethod
    def aggregate(
        cls,
        proposals: List["Proposal"],
        aggregated_text: str,
        aggregator_id: str = "weighted_vote",
        scores: Optional[Dict[str, float]] = None,
    ) -> "Proposal":
        """
        Create an aggregated proposal from multiple source proposals.
        """
        # Combine perspectives
        perspectives = list(set(p.rationale.perspective for p in proposals))
        all_tensions = []
        for p in proposals:
            all_tensions.extend(p.rationale.tensions)

        # Calculate average confidence
        avg_confidence = (
            sum(p.rationale.confidence for p in proposals) / len(proposals)
            if proposals
            else 0.5
        )

        rationale = Rationale(
            summary=f"Aggregated from {len(proposals)} proposals",
            reasoning=aggregated_text,
            perspective=f"Multi-perspective ({', '.join(perspectives[:3])}...)",
            tensions=list(set(all_tensions)),
            confidence=avg_confidence,
        )

        return cls(
            text=aggregated_text,
            rationale=rationale,
            source=ProposalSource.AGGREGATOR,
            source_id=aggregator_id,
            parent_ids=[p.proposal_id for p in proposals],
            scores=scores or {},
        )

    def with_repair(self, repaired_text: str, repair_log: List[str]) -> "Proposal":
        """Create a repaired version of this proposal."""
        return Proposal(
            text=repaired_text,
            rationale=Rationale(
                summary=f"Repaired: {self.rationale.summary}",
                reasoning=self.rationale.reasoning,
                perspective=self.rationale.perspective,
                key_concepts=self.rationale.key_concepts,
                tensions=self.rationale.tensions,
                confidence=self.rationale.confidence * 0.9,  # Slight confidence reduction
            ),
            source=ProposalSource.REPAIRED,
            source_id=f"repaired_{self.source_id}",
            context_id=self.context_id,
            parent_ids=[self.proposal_id],
            scores=self.scores.copy(),
            metadata={
                **self.metadata,
                "original_proposal_id": self.proposal_id,
                "repair_log": repair_log,
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "proposal_id": self.proposal_id,
            "text": self.text,
            "rationale": self.rationale.to_dict(),
            "source": self.source.value,
            "source_id": self.source_id,
            "created_at": self.created_at,
            "context_id": self.context_id,
            "parent_ids": self.parent_ids,
            "scores": self.scores,
            "metadata": self.metadata,
        }


__all__ = ["Proposal", "ProposalSource", "Rationale"]
