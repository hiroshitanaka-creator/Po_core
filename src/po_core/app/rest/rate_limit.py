"""
Rate Limiting
=============

SlowAPI-based per-IP rate limiting for the Po_core REST API.

The limit string is read from the environment at module import time so it
can be customised without code changes:

    PO_RATE_LIMIT_PER_MINUTE=30   # override at runtime

The ``limiter`` instance is a module-level singleton imported by routers.
The FastAPI app must attach it to ``app.state.limiter`` and register the
RateLimitExceeded exception handler — both are done in server.py.
"""

from __future__ import annotations

import os

from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared limiter instance — imported by all routers
limiter: Limiter = Limiter(key_func=get_remote_address)

# Rate limit string evaluated at import time from environment.
# Falls back to 60 requests/minute when the env var is absent.
REASON_LIMIT: str = f"{os.environ.get('PO_RATE_LIMIT_PER_MINUTE', '60')}/minute"

__all__ = ["limiter", "REASON_LIMIT"]
