"""
Base Philosopher Class (Constitution)
=====================================

This is the CONSTITUTIONAL CONTRACT for all philosophical reasoning modules.
All 39 philosophers must conform to this interface.

IMPORTANT: This file defines the INVIOLABLE CONTRACT between philosophers
and the ensemble system. Any changes here affect all 39 philosophers.

Contract:
- Input: prompt (str) + optional context (Dict)
- Output: PhilosopherResponse with REQUIRED keys
- Philosophers may add extra keys, but required keys must exist

The ensemble system depends on:
1. reasoning: str - The core philosophical analysis
2. perspective: str - The philosopher's viewpoint name
3. tension: Any - Identified tensions (optional, can be None)
4. metadata: Dict - Additional structured data (optional, can be {})

NOTE: Some philosophers currently return non-conformant keys.
The normalize_response() function provides backward compatibility.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, TypedDict, Union


class PhilosopherResponseRequired(TypedDict):
    """Required keys for philosopher response."""

    reasoning: str
    perspective: str


class PhilosopherResponse(PhilosopherResponseRequired, total=False):
    """
    Full philosopher response contract.

    Required keys:
        reasoning: str - The philosophical analysis text
        perspective: str - Name of the philosophical viewpoint

    Optional keys:
        tension: Any - Identified tensions (str, dict, or None)
        metadata: Dict[str, Any] - Additional structured data

    Philosophers may include additional custom keys specific to their
    philosophical framework (e.g., virtue_assessment for Aristotle,
    will_to_power for Nietzsche).
    """

    tension: Any
    metadata: Dict[str, Any]


@dataclass
class Context:
    """
    Standardized context passed to philosophers.

    This is the INPUT contract - what philosophers receive.
    Using a dataclass allows future extension without breaking signatures.
    """

    prompt: str
    session_id: Optional[str] = None
    tensor_snapshot: Optional[Dict[str, float]] = None
    intent: Optional[str] = None
    previous_responses: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_prompt(cls, prompt: str) -> "Context":
        """Create a minimal context from just a prompt."""
        return cls(prompt=prompt)


def normalize_response(
    raw_response: Dict[str, Any],
    philosopher_name: str,
    philosopher_description: str,
) -> PhilosopherResponse:
    """
    Normalize a philosopher's response to the standard contract.

    This function provides backward compatibility for philosophers
    that return non-conformant keys (e.g., Arendt returns 'analysis'
    instead of 'reasoning').

    Args:
        raw_response: The raw response from philosopher.reason()
        philosopher_name: The philosopher's name (for fallback)
        philosopher_description: The philosopher's description (for fallback)

    Returns:
        A normalized PhilosopherResponse with guaranteed keys

    Mapping rules:
    - reasoning: from 'reasoning', 'analysis', 'summary', or synthesize from content
    - perspective: from 'perspective', 'description', or use philosopher description
    - tension: from 'tension' or None
    - metadata: from 'metadata' or construct from extra keys
    """
    # Try to extract reasoning
    reasoning = raw_response.get("reasoning")
    if reasoning is None:
        # Try alternative keys
        if "analysis" in raw_response:
            analysis = raw_response["analysis"]
            if isinstance(analysis, dict):
                # Arendt-style: analysis is a dict of sub-analyses
                reasoning = raw_response.get("summary", str(analysis))
            else:
                reasoning = str(analysis)
        elif "summary" in raw_response:
            reasoning = raw_response["summary"]
        else:
            # Last resort: concatenate all string values
            reasoning = " ".join(
                str(v) for v in raw_response.values() if isinstance(v, str)
            )

    # Try to extract perspective
    perspective = raw_response.get("perspective")
    if perspective is None:
        perspective = raw_response.get("description", philosopher_description)

    # Extract tension (optional)
    tension = raw_response.get("tension")

    # Extract or construct metadata
    metadata = raw_response.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    # Add philosopher info to metadata
    metadata.setdefault("philosopher", philosopher_name)

    # Build normalized response
    normalized: PhilosopherResponse = {
        "reasoning": str(reasoning) if reasoning else "",
        "perspective": str(perspective) if perspective else philosopher_description,
    }

    if tension is not None:
        normalized["tension"] = tension

    if metadata:
        normalized["metadata"] = metadata

    # Preserve additional custom keys from original response
    # This allows philosopher-specific extensions (e.g., virtue_assessment)
    preserved_keys = {"reasoning", "perspective", "tension", "metadata"}
    for key, value in raw_response.items():
        if key not in preserved_keys:
            normalized[key] = value  # type: ignore

    return normalized


class Philosopher(ABC):
    """
    Abstract base class for all philosophers.

    CONSTITUTIONAL CONTRACT:
    - Each philosopher must implement reason() returning a dict
    - The dict SHOULD have 'reasoning' and 'perspective' keys
    - If not, normalize_response() will attempt to extract them
    - The ensemble system relies on this contract

    Recommended return format:
        {
            "reasoning": "...",  # REQUIRED: The philosophical analysis
            "perspective": "...",  # REQUIRED: Viewpoint name
            "tension": {...},  # OPTIONAL: Identified tensions
            "metadata": {...},  # OPTIONAL: Additional data
            # ... additional philosopher-specific keys allowed
        }
    """

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize a philosopher.

        Args:
            name: The philosopher's name
            description: A brief description of their philosophical approach
        """
        self.name = name
        self.description = description
        self._context: Dict[str, Any] = {}

    @abstractmethod
    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate philosophical reasoning for the given prompt.

        Args:
            prompt: The input text to reason about
            context: Optional context information (legacy Dict format)

        Returns:
            A dictionary that SHOULD contain:
                - reasoning: The philosophical analysis (REQUIRED)
                - perspective: The philosopher's unique viewpoint (REQUIRED)
                - tension: Identified tensions or contradictions (optional)
                - metadata: Additional reasoning metadata (optional)

            Note: If required keys are missing, normalize_response() will
            attempt to extract them from alternative keys.
        """
        pass

    def reason_with_context(self, ctx: Context) -> PhilosopherResponse:
        """
        Generate philosophical reasoning using the new Context format.

        This is the PREFERRED method for new code. It provides:
        - Type-safe context passing
        - Guaranteed normalized response
        - Future extensibility

        Args:
            ctx: A Context object containing the prompt and metadata

        Returns:
            A normalized PhilosopherResponse with guaranteed keys
        """
        # Call the legacy reason() method
        raw = self.reason(ctx.prompt, ctx.metadata if ctx.metadata else None)

        # Normalize the response
        return normalize_response(raw, self.name, self.description)

    def __repr__(self) -> str:
        """String representation of the philosopher."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name}: {self.description}"

    # ── PhilosopherProtocol conformance ─────────────────────────────
    # These methods allow Philosopher subclasses to be used directly
    # as PhilosopherProtocol without needing PhilosopherBridge.

    @property
    def info(self) -> "PhilosopherInfo":
        """PhilosopherProtocol.info: metadata about this philosopher."""
        return PhilosopherInfo(name=self.name, version="v0")

    def propose(
        self,
        ctx: "DomainContext",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
    ) -> "List[Proposal]":
        """
        PhilosopherProtocol.propose(): generate proposals from this philosopher.

        Calls legacy reason(), normalizes the result, and wraps it as a Proposal.
        This replaces the need for PhilosopherBridge for all Philosopher subclasses.
        """
        # Build lightweight context for legacy reason() interface
        legacy_context = {
            "intent": intent.goals[0] if intent.goals else "",
            "constraints": intent.constraints,
        }

        # Call legacy reason()
        raw = self.reason(ctx.user_input, legacy_context)

        # Normalize response
        normalized = normalize_response(raw, self.name, self.description)

        # Convert to Proposal
        reasoning = normalized.get("reasoning", "")
        perspective = normalized.get("perspective", "")
        tension = normalized.get("tension")

        content = reasoning
        action_type = "answer"

        assumption_tags = [f"perspective:{perspective}"]
        if tension:
            assumption_tags.append("has_tension")

        proposal = Proposal(
            proposal_id=f"{ctx.request_id}:{self.name}:0",
            action_type=action_type,
            content=content,
            confidence=0.5,
            assumption_tags=assumption_tags,
            risk_tags=[],
            extra={
                "philosopher": self.name,
                "perspective": perspective,
                "tension": tension,
                "normalized_response": {
                    k: v for k, v in normalized.items() if k not in ("reasoning",)
                },
            },
        )

        return [proposal]


# ── New Protocol-based interface for hexagonal architecture ──────────

from typing import List
from typing import Protocol as TypingProtocol

from po_core.domain.context import Context as DomainContext
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot


@dataclass(frozen=True)
class PhilosopherInfo:
    """Metadata about a philosopher (new format)."""

    name: str
    version: str


class PhilosopherProtocol(TypingProtocol):
    """Protocol for philosopher implementations (hexagonal architecture)."""

    info: PhilosopherInfo

    def propose(
        self,
        ctx: DomainContext,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> List[Proposal]:
        """
        Generate proposals based on context, intent, tensors, and memory.

        Args:
            ctx: Request context (domain type)
            intent: Current intent from SolarWill
            tensors: Tensor snapshot
            memory: Memory snapshot

        Returns:
            List of proposals
        """
        ...


__all__ = [
    # Legacy
    "Philosopher",
    "PhilosopherResponse",
    "PhilosopherResponseRequired",
    "Context",
    "normalize_response",
    # New hexagonal architecture
    "PhilosopherInfo",
    "PhilosopherProtocol",
]
