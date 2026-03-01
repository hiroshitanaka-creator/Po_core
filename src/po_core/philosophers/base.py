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
from typing import Any, Dict, List, Optional
from typing import Protocol as TypingProtocol
from typing import TypedDict

from po_core.domain.context import Context as DomainContext
from po_core.domain.intent import Intent
from po_core.domain.keys import CITATIONS, PO_CORE, RATIONALE
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot

# Valid action types that philosophers may declare.
# Values outside this set are silently normalised to "answer".
VALID_ACTION_TYPES: frozenset = frozenset(
    {"answer", "refuse", "ask_clarification", "tool_call", "defer"}
)


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

    Optional keys (normalised automatically by normalize_response()):
        tension: Any - Identified tensions (str, dict, or None)
        metadata: Dict[str, Any] - Additional structured data
        rationale: str - Short one-sentence justification; derived from the
            first sentence of *reasoning* when absent.
        confidence: float - Self-reported confidence in [0, 1]; defaults to
            0.5 when absent or non-numeric.
        action_type: str - Proposed action class; must be one of
            VALID_ACTION_TYPES.  Unknown values fall back to "answer".
        citations: List[str] - Philosophical references / works cited;
            defaults to [] when absent.

    Philosophers may include additional custom keys specific to their
    philosophical framework (e.g., virtue_assessment for Aristotle,
    will_to_power for Nietzsche).
    """

    tension: Any
    metadata: Dict[str, Any]
    rationale: str
    confidence: float
    action_type: str
    citations: List[str]


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
    - rationale: from 'rationale', else first sentence (≤150 chars) of reasoning
    - confidence: from 'confidence' clamped to [0.0, 1.0], else 0.5
    - action_type: from 'action_type' if in VALID_ACTION_TYPES, else "answer"
    - citations: from 'citations' if list[str], else []
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
    # This allows philosopher-specific extensions (e.g., virtue_assessment).
    # The four new fields are excluded here because they go through explicit
    # normalisation logic below (type coercion, clamping, allow-list checks).
    preserved_keys = {
        "reasoning",
        "perspective",
        "tension",
        "metadata",
        "rationale",
        "confidence",
        "action_type",
        "citations",
    }
    for key, value in raw_response.items():
        if key not in preserved_keys:
            normalized[key] = value  # type: ignore

    # ── New fields ────────────────────────────────────────────────────

    # rationale: explicit field preferred; fall back to first sentence of reasoning
    raw_rationale = raw_response.get("rationale")
    if isinstance(raw_rationale, str) and raw_rationale.strip():
        rationale: str = raw_rationale.strip()
    else:
        reasoning_text: str = normalized["reasoning"]
        dot_idx = reasoning_text.find(". ")
        rationale = (
            reasoning_text[: dot_idx + 1] if dot_idx > 0 else reasoning_text[:150]
        ).strip()

    # confidence: must be a float in [0.0, 1.0]
    raw_conf = raw_response.get("confidence")
    if raw_conf is None:
        confidence: float = 0.5
    else:
        try:
            confidence = float(raw_conf)
            confidence = max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            confidence = 0.5

    # action_type: must be one of VALID_ACTION_TYPES; unknown values → "answer"
    raw_action = raw_response.get("action_type", "answer")
    action_type: str = raw_action if raw_action in VALID_ACTION_TYPES else "answer"

    # citations: must be a list; non-list values → []
    raw_citations = raw_response.get("citations")
    if isinstance(raw_citations, list):
        citations: List[str] = [str(c) for c in raw_citations if c]
    else:
        citations = []

    normalized["rationale"] = rationale
    normalized["confidence"] = confidence
    normalized["action_type"] = action_type
    normalized["citations"] = citations

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
        # Subclasses should override these in their __init__
        if not hasattr(self, "tradition"):
            self.tradition: str = ""
        if not hasattr(self, "key_concepts"):
            self.key_concepts: list = []

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
        - Voice layer application (characteristic philosopher rhetoric)
        - Future extensibility

        Args:
            ctx: A Context object containing the prompt and metadata

        Returns:
            A normalized PhilosopherResponse with guaranteed keys
        """
        from po_core.runtime.voice_loader import get_voice

        # Call the legacy reason() method
        raw = self.reason(ctx.prompt, ctx.metadata if ctx.metadata else None)

        # Normalize the response
        normalized = normalize_response(raw, self.name, self.description)

        # Apply voice layer — replaces template-string reasoning with
        # the philosopher's characteristic rhetoric.  Falls back gracefully
        # if no YAML exists for this philosopher.
        module_id = self.__class__.__module__.split(".")[-1]
        voice = get_voice(module_id)
        if voice:
            tension_level: Optional[str] = None
            tension = normalized.get("tension")
            if isinstance(tension, dict):
                tension_level = tension.get("level")
            normalized["reasoning"] = voice.render(
                prompt=ctx.prompt,
                tension_level=tension_level,
                tensor_snapshot=ctx.tensor_snapshot,
            )

        return normalized

    def __repr__(self) -> str:
        """String representation of the philosopher."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name}: {self.description}"

    # ── PhilosopherProtocol conformance ─────────────────────────────
    # All Philosopher subclasses implement PhilosopherProtocol natively.

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

        Calls reason(), normalizes the result, and wraps it as a Proposal.
        """
        from po_core.runtime.voice_loader import get_voice

        # Build lightweight context for legacy reason() interface.
        # Tensor values are now forwarded so philosophers can react to them.
        legacy_context = {
            "intent": intent.goals[0] if intent.goals else "",
            "constraints": intent.constraints,
            "freedom_pressure": tensors.freedom_pressure,
            "semantic_delta": tensors.semantic_delta,
            "blocked_tensor": tensors.blocked_tensor,
        }

        # Call legacy reason()
        raw = self.reason(ctx.user_input, legacy_context)

        # Normalize response
        normalized = normalize_response(raw, self.name, self.description)

        # Apply voice layer — gives each philosopher their characteristic rhetoric.
        # Voice is stored as a *stylistic wrapper* in extra["voiced_reasoning"] so
        # that Proposal.content keeps the original analytical text.  This ensures
        # InteractionMatrix._compute_tension and counterargument assembly in the
        # deliberation engine operate on the full philosophical reasoning payload
        # (with opposition keywords intact) rather than on the template-rendered
        # voice output, which would produce zero-tension pairs and collapse
        # multi-round deliberation into a no-op.
        module_id = self.__class__.__module__.split(".")[-1]
        voice = get_voice(module_id)
        if voice:
            tension_level_v: Optional[str] = None
            tension_v = normalized.get("tension")
            if isinstance(tension_v, dict):
                tension_level_v = tension_v.get("level")
            tensor_snapshot_dict = {
                "freedom_pressure": tensors.freedom_pressure,
                "semantic_delta": tensors.semantic_delta,
                "blocked_tensor": tensors.blocked_tensor,
            }
            normalized["voiced_reasoning"] = voice.render(
                prompt=ctx.user_input,
                tension_level=tension_level_v,
                tensor_snapshot=tensor_snapshot_dict,
            )

        # Convert to Proposal
        reasoning = normalized.get("reasoning", "")
        perspective = normalized.get("perspective", "")
        tension = normalized.get("tension")

        # --- Fields extracted / normalised by normalize_response() ---
        confidence: float = float(normalized.get("confidence", 0.5))
        action_type: str = str(normalized.get("action_type", "answer"))
        rationale: str = str(normalized.get("rationale", ""))
        citations: List[str] = list(normalized.get("citations", []))

        content = reasoning

        assumption_tags = [f"perspective:{perspective}"]
        if tension:
            assumption_tags.append("has_tension")
        if citations:
            assumption_tags.append("has_citations")

        # PO_CORE provenance block — AUTHOR is added later by _embed_author()
        # in party_machine, which merges into this dict rather than replacing it.
        po_core_meta: Dict[str, Any] = {
            RATIONALE: rationale,
            CITATIONS: citations,
        }

        proposal = Proposal(
            proposal_id=f"{ctx.request_id}:{self.name}:0",
            action_type=action_type,
            content=content,
            confidence=confidence,
            assumption_tags=assumption_tags,
            risk_tags=[],
            extra={
                "philosopher": self.name,
                "perspective": perspective,
                "tension": tension,
                "voiced_reasoning": normalized.get("voiced_reasoning"),
                "normalized_response": {
                    k: v
                    for k, v in normalized.items()
                    if k not in ("reasoning", "voiced_reasoning")
                },
                PO_CORE: po_core_meta,
            },
        )

        return [proposal]

    async def propose_async(
        self,
        ctx: "DomainContext",
        intent: "Intent",
        tensors: "TensorSnapshot",
        memory: "MemorySnapshot",
    ) -> "List[Proposal]":
        """Async interface for PhilosopherProtocol.propose().

        Default implementation runs the synchronous ``propose()`` in a thread
        via the event-loop's default executor, ensuring the FastAPI event loop
        is never blocked even for CPU-bound philosophers.

        Subclasses that have native async capability (e.g., AI philosophers that
        call external APIs) may override this method to skip the thread entirely.

        Returns:
            Same as ``propose()``: a list of Proposal objects.
        """
        import asyncio
        import functools

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            functools.partial(self.propose, ctx, intent, tensors, memory),
        )


# ── New Protocol-based interface for hexagonal architecture ──────────


@dataclass(frozen=True)
class PhilosopherInfo:
    """Metadata about a philosopher (new format)."""

    name: str
    version: str


class PhilosopherProtocol(TypingProtocol):
    """
    Protocol for philosopher implementations (hexagonal architecture).

    Every conforming implementation must satisfy:

    1. ``info`` — a :class:`PhilosopherInfo` instance.

    2. ``propose()`` / ``propose_async()`` — return ``List[Proposal]`` where
       every Proposal guarantees the following in its ``extra`` mapping:

       * ``extra[PO_CORE][RATIONALE]`` (:class:`str`) — one-sentence
         justification derived from the philosopher's reasoning.  Empty string
         when the reasoning itself is empty.
       * ``extra[PO_CORE][CITATIONS]`` (:class:`List[str]`) — philosophical
         references returned by ``reason()``.  Empty list when none are given.
       * ``extra[PO_CORE][AUTHOR]`` (:class:`str`) — philosopher identifier,
         embedded by ``party_machine._embed_author()`` after ``propose()``
         returns (not set inside ``propose()`` itself).

    3. ``Proposal.confidence`` — float in ``[0.0, 1.0]`` sourced from the
       ``confidence`` key in ``reason()``'s return dict (default ``0.5``).

    4. ``Proposal.action_type`` — one of :data:`VALID_ACTION_TYPES` sourced
       from the ``action_type`` key in ``reason()``'s return dict (default
       ``"answer"``).

    The base :class:`Philosopher` class satisfies all four guarantees through
    :func:`normalize_response` + the ``propose()`` implementation in
    ``base.py``.  Custom protocol implementations must replicate this
    behaviour explicitly.
    """

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
            List of Proposal objects.  Each Proposal must carry
            ``extra[PO_CORE][RATIONALE]`` and ``extra[PO_CORE][CITATIONS]``
            (see class docstring).
        """
        ...

    async def propose_async(
        self,
        ctx: DomainContext,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> List[Proposal]:
        """
        Async variant of propose().

        Implementations that override this may use native async IO without
        blocking the event loop.  The default (on ``Philosopher`` subclasses)
        wraps the synchronous ``propose()`` in a thread executor.

        Returns:
            Same as ``propose()``: a list of Proposal objects.
        """
        ...


__all__ = [
    # Legacy
    "Philosopher",
    "PhilosopherResponse",
    "PhilosopherResponseRequired",
    "Context",
    "normalize_response",
    "VALID_ACTION_TYPES",
    # New hexagonal architecture
    "PhilosopherInfo",
    "PhilosopherProtocol",
]
