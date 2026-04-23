"""Redaction helpers for trace and review responses.

Goals:
  * Strip PII-shaped strings (emails, phone numbers, API-key-like tokens) from
    trace payload values before they leave the server.
  * Drop internal traceback fields that may leak file paths, stack frames, or
    secrets.
  * Collapse human-review comments (which can contain freeform PII) to a
    length-preserved redacted placeholder for non-reviewer roles.

The implementation is intentionally conservative and non-recursive beyond the
first two levels; trace payloads are expected to be shallow dictionaries.  The
goal is defensive redaction, not perfect DLP.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

REDACTED_PLACEHOLDER = "[REDACTED]"

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\-\s().]{7,}\d)")
# Catch bearer/api-key-style long alphanumeric+symbol tokens.
_TOKEN_RE = re.compile(r"(?i)(?:bearer\s+|api[_-]?key[\s:=]+)[A-Za-z0-9._~+\-/]{12,}")

# Payload keys that are always dropped/redacted.  Paths, tracebacks, and raw
# error dumps tend to leak environment details.
_SENSITIVE_KEYS = {
    "traceback",
    "stack_trace",
    "stacktrace",
    "exception_traceback",
    "tb",
    "internal_error",
    "raw_error",
    "secret",
    "api_key",
    "authorization",
    "password",
    "token",
}

# Payload keys whose value is free text that may include PII.  We string-scrub
# them but do not drop them — keeping the key preserves schema compatibility.
_FREETEXT_KEYS = {
    "user_input",
    "input",
    "prompt",
    "response",
    "message",
    "detail",
    "content",
    "comment",
    "error_message",
}


def _scrub_string(value: str) -> str:
    scrubbed = _EMAIL_RE.sub(REDACTED_PLACEHOLDER, value)
    scrubbed = _PHONE_RE.sub(REDACTED_PLACEHOLDER, scrubbed)
    scrubbed = _TOKEN_RE.sub(REDACTED_PLACEHOLDER, scrubbed)
    return scrubbed


def _redact_value(key: str, value: Any, *, depth: int) -> Any:
    if depth > 4:
        return REDACTED_PLACEHOLDER

    key_lower = key.lower() if isinstance(key, str) else ""
    if key_lower in _SENSITIVE_KEYS:
        return REDACTED_PLACEHOLDER

    if isinstance(value, str):
        if key_lower in _FREETEXT_KEYS or len(value) > 80:
            return _scrub_string(value)
        return value

    if isinstance(value, Mapping):
        return redact_payload(value, depth=depth + 1)

    if isinstance(value, (list, tuple)):
        redacted: list[Any] = [
            _redact_value(key, item, depth=depth + 1) for item in value
        ]
        return redacted if isinstance(value, list) else tuple(redacted)

    return value


def redact_payload(payload: Mapping[str, Any], *, depth: int = 0) -> dict[str, Any]:
    """Return a redacted shallow copy of *payload*.

    The top-level shape is preserved; values are scrubbed in place.
    """
    result: dict[str, Any] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            result[str(key)] = _redact_value(str(key), value, depth=depth + 1)
            continue
        result[key] = _redact_value(key, value, depth=depth + 1)
    return result


def redact_trace_events(events: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Redact each event payload in *events* and return a plain list of dicts."""
    redacted: list[dict[str, Any]] = []
    for event in events:
        payload = event.get("payload")
        payload_map: Mapping[str, Any] = payload if isinstance(payload, Mapping) else {}
        redacted.append(
            {
                **{k: v for k, v in event.items() if k != "payload"},
                "payload": redact_payload(payload_map),
            }
        )
    return redacted


def redact_review_comment(comment: str | None) -> str | None:
    """Collapse a review comment into a length-preserved redacted placeholder.

    The raw comment is kept server-side (in storage and in audit trails) but
    not surfaced to general clients through the REST response.
    """
    if comment is None:
        return None
    if not comment.strip():
        return comment
    # Keep a size hint so that dashboards can still show that a comment exists.
    return f"{REDACTED_PLACEHOLDER} ({len(comment)} chars)"


__all__ = [
    "REDACTED_PLACEHOLDER",
    "redact_payload",
    "redact_review_comment",
    "redact_trace_events",
]
