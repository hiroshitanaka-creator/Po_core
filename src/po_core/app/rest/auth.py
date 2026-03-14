"""Shared API-key authentication policy for REST and WebSocket transports."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from po_core.app.rest.config import APISettings, get_api_settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@dataclass(frozen=True)
class AuthDecision:
    """Authorization result used across HTTP and WebSocket transports."""

    allowed: bool
    is_misconfigured: bool
    message: str


def evaluate_auth_policy(
    *,
    skip_auth: bool,
    configured_api_key: str,
    presented_api_key: str | None,
) -> AuthDecision:
    """Apply the shared auth policy.

    Policy:
      - skip_auth=True → allow
      - skip_auth=False and configured_api_key empty → reject as misconfiguration
      - configured key present but missing/wrong presented key → reject as unauthorized
      - otherwise allow
    """
    if skip_auth:
        return AuthDecision(allowed=True, is_misconfigured=False, message="Auth bypassed")

    expected = configured_api_key.strip()
    if not expected:
        return AuthDecision(
            allowed=False,
            is_misconfigured=True,
            message="Server misconfigured: PO_API_KEY must be set when PO_SKIP_AUTH=false",
        )

    provided = (presented_api_key or "").strip()
    if provided != expected:
        return AuthDecision(
            allowed=False,
            is_misconfigured=False,
            message="Invalid or missing API key",
        )

    return AuthDecision(allowed=True, is_misconfigured=False, message="Authorized")


async def require_api_key(
    api_key: str | None = Security(_api_key_header),
    settings: APISettings = Depends(get_api_settings),
) -> None:
    """FastAPI dependency that validates API-key auth with fail-closed defaults."""
    decision = evaluate_auth_policy(
        skip_auth=settings.skip_auth,
        configured_api_key=settings.api_key,
        presented_api_key=api_key,
    )
    if decision.allowed:
        return

    if decision.is_misconfigured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=decision.message,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=decision.message,
        headers={"WWW-Authenticate": "ApiKey"},
    )
