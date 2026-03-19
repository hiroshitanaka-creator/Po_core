"""
Rate Limiting
=============

SlowAPI-based per-IP rate limiting for the Po_core REST API.

The ``limiter`` instance is a module-level singleton imported by routers.
The FastAPI app must attach it to ``app.state.limiter`` and register the
RateLimitExceeded exception handler — both are done in server.py.

The per-endpoint limit is derived at request time from
``request.app.state.settings.rate_limit_per_minute`` so that
``create_app(settings=...)`` overrides and .env configuration are honoured.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fastapi import Request
from slowapi import Limiter


def _extract_forwarded_ip(headers: Mapping[str, str]) -> str | None:
    """Return the first non-empty X-Forwarded-For hop when present."""
    forwarded_for = headers.get("x-forwarded-for", "")
    for candidate in forwarded_for.split(","):
        normalized = candidate.strip()
        if normalized:
            return normalized
    return None


def get_rate_limit_key(request: Request) -> str:
    """Return a deterministic rate-limit key for the incoming request."""
    settings: Any = getattr(request.app.state, "settings", None)
    trust_proxy_headers = bool(getattr(settings, "trust_proxy_headers", False))

    if trust_proxy_headers:
        forwarded_ip = _extract_forwarded_ip(request.headers)
        if forwarded_ip:
            return forwarded_ip

    client = request.client
    if client is not None and client.host:
        return client.host
    return "unknown"


# Shared limiter instance — imported by all routers
limiter: Limiter = Limiter(key_func=get_rate_limit_key)

__all__ = ["get_rate_limit_key", "limiter"]
