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

from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared limiter instance — imported by all routers
limiter: Limiter = Limiter(key_func=get_remote_address)

__all__ = ["limiter"]
