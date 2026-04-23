"""Shared API-key authentication policy for REST, WebSocket, and legacy API transports."""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from typing import Mapping

from fastapi import Depends, HTTPException, Request, status

from po_core.app.rest.config import APISettings, get_api_settings

DEFAULT_API_KEY_HEADER = "X-API-Key"


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
        return AuthDecision(
            allowed=True, is_misconfigured=False, message="Auth bypassed"
        )

    expected = configured_api_key.strip()
    if not expected:
        return AuthDecision(
            allowed=False,
            is_misconfigured=True,
            message="Server misconfigured: PO_API_KEY must be set when PO_SKIP_AUTH=false",
        )

    provided = (presented_api_key or "").strip()
    if not hmac.compare_digest(provided, expected):
        return AuthDecision(
            allowed=False,
            is_misconfigured=False,
            message="Invalid or missing API key",
        )

    return AuthDecision(allowed=True, is_misconfigured=False, message="Authorized")


def resolve_api_key_header_names(configured_header_name: str) -> tuple[str, ...]:
    """Return accepted API-key header names in precedence order."""
    configured = configured_header_name.strip() or DEFAULT_API_KEY_HEADER
    if configured.lower() == DEFAULT_API_KEY_HEADER.lower():
        return (DEFAULT_API_KEY_HEADER,)
    return (configured, DEFAULT_API_KEY_HEADER)


def extract_api_key_from_header_map(
    headers: Mapping[str, str], *, configured_header_name: str
) -> str | None:
    """Resolve an API key from request headers without silently weakening auth."""
    for header_name in resolve_api_key_header_names(configured_header_name):
        value = headers.get(header_name) or headers.get(header_name.lower())
        if value and value.strip():
            return value.strip()
    return None


async def require_api_key(
    request: Request,
    settings: APISettings = Depends(get_api_settings),
) -> None:
    """FastAPI dependency that validates API-key auth with fail-closed defaults."""
    decision = evaluate_auth_policy(
        skip_auth=settings.skip_auth,
        configured_api_key=settings.api_key,
        presented_api_key=extract_api_key_from_header_map(
            request.headers, configured_header_name=settings.api_key_header
        ),
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


def extract_api_key_from_headers(
    *,
    x_api_key: str | None,
    authorization: str | None,
) -> str | None:
    """Resolve an API key from shared HTTP header conventions."""
    if x_api_key and x_api_key.strip():
        return x_api_key.strip()
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()
