"""
API Key Authentication
======================

Provides FastAPI dependency for API key validation.

Usage:
    @router.post("/v1/reason")
    async def reason(
        request: ReasonRequest,
        _: None = Depends(require_api_key),
    ):
        ...

When PO_SKIP_AUTH=true the check is bypassed
(useful for local development and unit tests).
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from po_core.app.rest.config import APISettings, get_api_settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(
    api_key: str | None = Security(_api_key_header),
    settings: APISettings = Depends(get_api_settings),
) -> None:
    """
    FastAPI dependency that validates the X-API-Key header.

    Raises 401 when the key is missing or incorrect.
    Raises 503 when API key auth is enabled but PO_API_KEY is not configured.
    Bypassed only when skip_auth=True (dev mode).
    """
    if settings.skip_auth:
        return
    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key authentication is enabled but PO_API_KEY is not configured",
        )
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
