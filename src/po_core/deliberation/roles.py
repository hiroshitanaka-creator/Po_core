"""
Dialectic Roles
===============

Hegel 弁証法的ラウンド役割システム (Phase 6-B).

Round 1 → Thesis    : 全哲学者が独自立場を提案  [現状と同じ]
Round 2 → Antithesis: 高干渉ペアが「否定・論駁」を構築
Round 3 → Synthesis : Synthesizer 哲学者群が対立を統合し上位命題を生成
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List

# Philosophers assigned to the Synthesis round in dialectic mode.
# These thinkers are known for integrating opposing views into higher-order propositions.
SYNTHESIZER_PHILOSOPHERS: List[str] = [
    "Hegel",  # Aufhebung: Negation → preservation → elevation
    "Kant",  # Transcendental synthesis of opposing faculties
    "Plato",  # Forms: the higher truth behind apparent opposites
    "Dewey",  # Pragmatic integration of conflicting perspectives
]


class DebateRole(str, Enum):
    """Role assigned to a deliberation round in dialectic mode."""

    THESIS = "thesis"
    ANTITHESIS = "antithesis"
    SYNTHESIS = "synthesis"
    STANDARD = "standard"  # Non-dialectic rounds


# Role-specific prompt instructions prepended to the debate prompt.
ROLE_PROMPT_PREFIX: Dict[str, str] = {
    DebateRole.THESIS: "",  # Round 1 is a normal proposal — no extra instruction
    DebateRole.ANTITHESIS: (
        "[ROLE: ANTITHESIS]\n"
        "Your task is to REFUTE, not merely rebut. "
        "You must actively negate and undermine the opposing position. "
        "Identify its deepest contradiction, expose its hidden assumptions, "
        "and demonstrate why it fails on its own terms.\n"
    ),
    DebateRole.SYNTHESIS: (
        "[ROLE: SYNTHESIS — Aufhebung]\n"
        "As a synthesizer, your task is to transcend the debate. "
        "Draw upon the opposing positions to articulate a higher-order proposition "
        "that preserves the valid insights of each while resolving their central contradiction. "
        "This is not a compromise — it is an Aufhebung: negate, preserve, and elevate.\n"
    ),
    DebateRole.STANDARD: "",
}


def assign_role(round_num: int, dialectic_mode: bool) -> DebateRole:
    """Assign a DebateRole based on round number and mode.

    In standard mode, all rounds use DebateRole.STANDARD.

    In dialectic mode:
      Round 1  → THESIS
      Round 2  → ANTITHESIS
      Round 3+ → SYNTHESIS
    """
    if not dialectic_mode:
        return DebateRole.STANDARD
    if round_num == 1:
        return DebateRole.THESIS
    if round_num == 2:
        return DebateRole.ANTITHESIS
    return DebateRole.SYNTHESIS


def get_role_prompt_prefix(role: DebateRole) -> str:
    """Return the prompt instruction prefix for a given role."""
    return ROLE_PROMPT_PREFIX.get(role, "")


__all__ = [
    "DebateRole",
    "SYNTHESIZER_PHILOSOPHERS",
    "assign_role",
    "get_role_prompt_prefix",
]
