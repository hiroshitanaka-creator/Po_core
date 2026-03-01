"""Normalization and simple language detection utilities."""

from __future__ import annotations

import re
import unicodedata
from typing import Literal

_WHITESPACE_RE = re.compile(r"\s+")
_JA_CHAR_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]")
_LATIN_CHAR_RE = re.compile(r"[A-Za-z]")

Language = Literal["ja", "en", "mixed"]


def normalize_text(text: str) -> str:
    """
    Normalize text for deterministic keyword/anchor matching.

    - Unicode NFKC normalization
    - Collapse repeated spaces/newlines/tabs into single spaces
    - Lowercase English letters (Japanese characters are unchanged)
    """
    normalized = unicodedata.normalize("NFKC", text)
    normalized = _WHITESPACE_RE.sub(" ", normalized).strip()
    return normalized.lower()


def detect_language_simple(text: str) -> Language:
    """
    Detect text language with a lightweight heuristic.

    Returns:
        - "ja": Japanese scripts only (hiragana/katakana/kanji)
        - "en": Latin letters only
        - "mixed": both Japanese and Latin are present, or neither is clear
    """
    has_ja = bool(_JA_CHAR_RE.search(text))
    has_latin = bool(_LATIN_CHAR_RE.search(text))

    if has_ja and not has_latin:
        return "ja"
    if has_latin and not has_ja:
        return "en"
    return "mixed"


__all__ = ["normalize_text", "detect_language_simple", "Language"]
