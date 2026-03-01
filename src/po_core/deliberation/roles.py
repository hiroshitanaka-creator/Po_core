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
from typing import Dict, FrozenSet, Iterable, List, Mapping, Set

# Philosophers assigned to the Synthesis round in dialectic mode.
# These thinkers are known for integrating opposing views into higher-order propositions.
# Uses philosopher_id (lowercase, matches manifest.py) — NOT the full .name attribute.
SYNTHESIZER_PHILOSOPHERS: List[str] = [
    "hegel",  # Aufhebung: Negation → preservation → elevation
    "kant",  # Transcendental synthesis of opposing faculties
    "plato",  # Forms: the higher truth behind apparent opposites
    "dewey",  # Pragmatic integration of conflicting perspectives
]


class DebateRole(str, Enum):
    """Role assigned to a deliberation round in dialectic mode."""

    THESIS = "thesis"
    ANTITHESIS = "antithesis"
    SYNTHESIS = "synthesis"
    STANDARD = "standard"  # Non-dialectic rounds


class Role(str, Enum):
    """Execution role (voice-independent functional role)."""

    UTILITARIAN = "UTILITARIAN"
    DEONTOLOGIST = "DEONTOLOGIST"
    VIRTUE = "VIRTUE"
    CARE = "CARE"
    SYSTEMS = "SYSTEMS"
    PRAGMATIST = "PRAGMATIST"
    RED_TEAM = "RED_TEAM"


class RoleCoverage:
    """AxisSpec v1 role coverage helper."""

    AXIS_REQUIRED_ROLES: Mapping[str, FrozenSet[Role]] = {
        "A": frozenset({Role.DEONTOLOGIST, Role.CARE}),
        "B": frozenset({Role.UTILITARIAN, Role.DEONTOLOGIST}),
        "C": frozenset({Role.CARE, Role.SYSTEMS}),
        "D": frozenset({Role.VIRTUE, Role.PRAGMATIST}),
        "E": frozenset({Role.RED_TEAM, Role.SYSTEMS}),
    }

    @classmethod
    def covered_axes(cls, roles: Iterable[Role]) -> Set[str]:
        role_set = set(roles)
        return {
            axis
            for axis, required in cls.AXIS_REQUIRED_ROLES.items()
            if required.intersection(role_set)
        }

    @classmethod
    def is_axis_covered(cls, axis_id: str, roles: Iterable[Role]) -> bool:
        required = cls.AXIS_REQUIRED_ROLES.get(axis_id, frozenset())
        return bool(required.intersection(set(roles)))

    @classmethod
    def is_fully_covered(cls, roles: Iterable[Role]) -> bool:
        role_set = set(roles)
        return all(
            required.intersection(role_set)
            for required in cls.AXIS_REQUIRED_ROLES.values()
        )


DEFAULT_ROLES: FrozenSet[Role] = frozenset(
    {
        Role.UTILITARIAN,
        Role.DEONTOLOGIST,
        Role.VIRTUE,
        Role.CARE,
        Role.SYSTEMS,
        Role.PRAGMATIST,
        Role.RED_TEAM,
    }
)


PHILOSOPHER_ROLE_MAP: Mapping[str, Role] = {
    "dummy": Role.SYSTEMS,
    "kant": Role.DEONTOLOGIST,
    "confucius": Role.CARE,
    "marcus_aurelius": Role.VIRTUE,
    "jonas": Role.SYSTEMS,
    "weil": Role.CARE,
    "levinas": Role.CARE,
    "watsuji": Role.CARE,
    "dogen": Role.VIRTUE,
    "wabi_sabi": Role.VIRTUE,
    "aristotle": Role.VIRTUE,
    "plato": Role.DEONTOLOGIST,
    "descartes": Role.SYSTEMS,
    "spinoza": Role.SYSTEMS,
    "hegel": Role.SYSTEMS,
    "husserl": Role.SYSTEMS,
    "merleau_ponty": Role.CARE,
    "wittgenstein": Role.PRAGMATIST,
    "peirce": Role.PRAGMATIST,
    "dewey": Role.PRAGMATIST,
    "arendt": Role.SYSTEMS,
    "beauvoir": Role.CARE,
    "nishida": Role.SYSTEMS,
    "laozi": Role.VIRTUE,
    "zhuangzi": Role.VIRTUE,
    "nagarjuna": Role.RED_TEAM,
    "parmenides": Role.DEONTOLOGIST,
    "epicurus": Role.UTILITARIAN,
    "jung": Role.CARE,
    "nietzsche": Role.RED_TEAM,
    "heidegger": Role.RED_TEAM,
    "sartre": Role.RED_TEAM,
    "kierkegaard": Role.RED_TEAM,
    "schopenhauer": Role.RED_TEAM,
    "foucault": Role.RED_TEAM,
    "derrida": Role.RED_TEAM,
    "deleuze": Role.RED_TEAM,
    "lacan": Role.RED_TEAM,
    "badiou": Role.RED_TEAM,
    "butler": Role.CARE,
    "claude_anthropic": Role.DEONTOLOGIST,
    "grok_xai": Role.RED_TEAM,
    "gpt_chatgpt": Role.PRAGMATIST,
    "gemini_google": Role.SYSTEMS,
}


def parse_roles_csv(raw: str) -> FrozenSet[Role]:
    """Parse PO_ROLES style CSV into validated Role values."""
    roles: Set[Role] = set()
    for token in raw.split(","):
        value = token.strip().upper()
        if not value:
            continue
        roles.add(Role(value))
    return frozenset(roles)


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
    "DEFAULT_ROLES",
    "DebateRole",
    "Role",
    "RoleCoverage",
    "PHILOSOPHER_ROLE_MAP",
    "SYNTHESIZER_PHILOSOPHERS",
    "assign_role",
    "get_role_prompt_prefix",
    "parse_roles_csv",
]
