"""
VoiceLoader — Philosopher Voice Configuration
==============================================

Each philosopher has a voice YAML under src/po_core/config/voices/<id>.yaml
that defines their characteristic rhetoric, catchphrases, and tension-aware
response templates.

The voice layer is applied as a post-processor in Philosopher.reason_with_context()
so the technical pipeline (run_turn) is completely unchanged.

YAML schema (all keys optional except openings):
  name: str
  rhetorical_mode: aphoristic | dialectical | Socratic | meditative | ...
  openings: list[str]        # {topic} placeholder available
  conflict: list[str]        # high tension body — {topic} available
  question: list[str]        # moderate tension body
  insight: list[str]         # low tension body
  closings: list[str]
  signature_phrases: list[str]
  tensor_reactions:
    freedom_pressure_high: str
    blocked_tensor_high: str
    semantic_delta_high: str
"""

from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

_VOICE_DIR = Path(__file__).parent.parent / "config" / "voices"

# Module-level cache: philosopher_id → VoiceRenderer (or None if no YAML)
_CACHE: Dict[str, Optional["VoiceRenderer"]] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_topic(prompt: str) -> str:
    """Return a short topic phrase (≤5 words) from the prompt."""
    clean = re.sub(r"[^\w\s]", " ", prompt).strip()
    words = clean.split()
    return " ".join(words[:5]) if len(words) > 5 else clean or prompt


def _tension_category(tension_level: Optional[str]) -> str:
    """Map tension level string → YAML category key."""
    if not tension_level:
        return "question"
    lvl = tension_level.lower()
    if "very high" in lvl or ("high" in lvl and "low" not in lvl):
        return "conflict"
    if "low" in lvl:
        return "insight"
    return "question"


def _pick(items: list[str], topic: str, full_topic: str) -> str:
    """Pick a random item and substitute {topic}/{full_topic} placeholders."""
    if not items:
        return ""
    template = random.choice(items)
    return template.format(topic=topic, full_topic=full_topic)


# ---------------------------------------------------------------------------
# VoiceRenderer
# ---------------------------------------------------------------------------


class VoiceRenderer:
    """Renders a philosopher's response in their characteristic voice.

    Usage (internal — called from base.py)::

        renderer = get_voice("nietzsche")
        voiced = renderer.render(
            prompt="What is justice?",
            tension_level="High",
            tensor_snapshot={"freedom_pressure": 0.8, ...},
        )
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(
        self,
        prompt: str,
        tension_level: Optional[str] = None,
        tensor_snapshot: Optional[Dict[str, float]] = None,
    ) -> str:
        """Build the voiced reasoning string."""
        topic = _extract_topic(prompt)
        full_topic = prompt.strip().rstrip("?!. ")
        cat = _tension_category(tension_level)

        parts: list[str] = []

        # 1. Opening
        opening = _pick(self.config.get("openings", []), topic, full_topic)
        if opening:
            parts.append(opening)

        # 2. Body (tension-aware, fall back through categories)
        body_items = (
            self.config.get(cat)
            or self.config.get("question")
            or []
        )
        body = _pick(body_items, topic, full_topic)
        if body:
            parts.append(body)

        # 3. Tensor colour (optional)
        tensor_comment = self._tensor_reaction(tensor_snapshot or {})
        if tensor_comment:
            parts.append(tensor_comment)

        # 4. Closing
        closing = _pick(self.config.get("closings", []), topic, full_topic)
        if closing:
            parts.append(closing)

        # 5. Signature phrase (50 % chance — keeps responses fresh)
        sigs = self.config.get("signature_phrases", [])
        if sigs and random.random() > 0.5:
            parts.append(random.choice(sigs))

        return " ".join(p for p in parts if p)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _tensor_reaction(self, tensors: Dict[str, float]) -> str:
        reactions: Dict[str, str] = self.config.get("tensor_reactions", {})
        if not reactions:
            return ""

        fp = tensors.get("freedom_pressure", 0.0)
        bt = tensors.get("blocked_tensor", 0.0)
        sd = tensors.get("semantic_delta", 0.0)

        if fp > 0.7 and "freedom_pressure_high" in reactions:
            return reactions["freedom_pressure_high"]
        if bt > 0.6 and "blocked_tensor_high" in reactions:
            return reactions["blocked_tensor_high"]
        if sd > 0.7 and "semantic_delta_high" in reactions:
            return reactions["semantic_delta_high"]
        return ""


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------


def get_voice(philosopher_module_id: str) -> Optional[VoiceRenderer]:
    """Return a VoiceRenderer for the given philosopher module ID (e.g. 'nietzsche').

    Returns None if no voice YAML exists for this philosopher (graceful degradation).
    The result is cached for the lifetime of the process.
    """
    if philosopher_module_id in _CACHE:
        return _CACHE[philosopher_module_id]

    yaml_path = _VOICE_DIR / f"{philosopher_module_id}.yaml"
    if not yaml_path.exists():
        _CACHE[philosopher_module_id] = None
        return None

    with yaml_path.open(encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}

    renderer = VoiceRenderer(config)
    _CACHE[philosopher_module_id] = renderer
    return renderer


def clear_cache() -> None:
    """Clear the voice renderer cache (useful in tests)."""
    _CACHE.clear()
