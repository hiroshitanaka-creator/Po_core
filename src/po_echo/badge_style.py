from __future__ import annotations

from typing import Any

LABEL_CONFIG: dict[str, dict[str, str]] = {
    "ECHO_BLOCKED": {
        "display": "ECHO BLOCKED",
        "bg": "#3A1111",
        "fg": "#FFD9D9",
        "accent": "#FF5A5A",
    },
    "ECHO_CHECK": {
        "display": "ECHO CHECK",
        "bg": "#2F2910",
        "fg": "#FFF5CC",
        "accent": "#F6C343",
    },
    "ECHO_VERIFIED": {
        "display": "ECHO VERIFIED",
        "bg": "#102C1E",
        "fg": "#D8FFE9",
        "accent": "#45D483",
    },
}

PIG_STATE_BY_LABEL: dict[str, str] = {
    "ECHO_BLOCKED": "🐷💥",
    "ECHO_CHECK": "🐷⚠️",
    "ECHO_VERIFIED": "🐷🌈",
}

PIG_MESSAGE_BY_LABEL: dict[str, str] = {
    "ECHO_BLOCKED": "Risk signal detected. Stop execution.",
    "ECHO_CHECK": "Need human confirmation before acting.",
    "ECHO_VERIFIED": "Candidate set is ready with clear boundaries.",
}


def normalize_label(label: str) -> str:
    normalized = (label or "").strip().replace("-", "_").upper()
    if not normalized.startswith("ECHO_") and normalized in {"BLOCKED", "CHECK", "VERIFIED"}:
        normalized = f"ECHO_{normalized}"
    if normalized not in LABEL_CONFIG:
        raise ValueError(
            f"Unsupported label '{label}'. Expected one of: {', '.join(LABEL_CONFIG)}"
        )
    return normalized


def get_label_config(label: str) -> dict[str, Any]:
    key = normalize_label(label)
    return {
        "label": key,
        **LABEL_CONFIG[key],
        "pig_state": PIG_STATE_BY_LABEL[key],
        "pig_message": PIG_MESSAGE_BY_LABEL[key],
    }
