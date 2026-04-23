"""Scope-based authorization for REST endpoints.

The global ``PO_API_KEY`` remains a backwards-compatible super-key that grants
every scope.  In addition, per-scope keys can be configured via the environment
so that a separate key is required for:

- ``reason:write``  — POST /v1/reason, POST /v1/reason/stream, WS /v1/ws/reason
- ``trace:read``    — GET /v1/trace/*, GET /v1/tradeoff-map/*
- ``review:write``  — POST /v1/review/{id}/decision, GET /v1/review/pending

If a scope-specific env var is set, requests to that endpoint accept EITHER
the global ``api_key`` (if configured) OR any of the scope-specific keys.
If none is configured, the endpoint falls back to the standard global key.
"""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from typing import Awaitable, Callable, Iterable

from fastapi import Depends, HTTPException, Request, status

from po_core.app.rest.auth import (
    evaluate_auth_policy,
    extract_api_key_from_header_map,
)
from po_core.app.rest.config import APISettings, get_api_settings


class Scope:
    """Canonical scope identifiers."""

    REASON_WRITE = "reason:write"
    TRACE_READ = "trace:read"
    REVIEW_WRITE = "review:write"


def _parse_key_list(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def _scope_keys(settings: APISettings, scope: str) -> list[str]:
    if scope == Scope.REASON_WRITE:
        raw = settings.api_keys_reason_write
    elif scope == Scope.TRACE_READ:
        raw = settings.api_keys_trace_read
    elif scope == Scope.REVIEW_WRITE:
        raw = settings.api_keys_review_write
    else:
        raw = ""
    return _parse_key_list(raw)


def _any_scope_configured(settings: APISettings) -> bool:
    return any(
        _scope_keys(settings, s)
        for s in (Scope.REASON_WRITE, Scope.TRACE_READ, Scope.REVIEW_WRITE)
    )


def _match_any(candidate: str, allowed: Iterable[str]) -> bool:
    return any(hmac.compare_digest(candidate, expected) for expected in allowed)


@dataclass(frozen=True)
class ScopeAuthDecision:
    allowed: bool
    is_misconfigured: bool
    message: str


def evaluate_scope_policy(
    *,
    settings: APISettings,
    presented_api_key: str | None,
    scope: str,
) -> ScopeAuthDecision:
    """Evaluate whether *presented_api_key* is authorised for *scope*.

    Policy:
      1. ``skip_auth=True`` always allows (dev override).
      2. If neither the global key nor any scope key is configured, startup
         validation has already failed — but defensively we reject here too.
      3. If *no* scope key is configured for any scope, fall back to the
         standard global-key policy (backwards-compatible single-key mode).
      4. Otherwise, accept the request if the presented key equals either
         the global key *or* any key listed under the requested scope.
    """
    if settings.skip_auth:
        return ScopeAuthDecision(
            allowed=True, is_misconfigured=False, message="Auth bypassed"
        )

    global_key = settings.api_key.strip()
    scope_keys = _scope_keys(settings, scope)

    if not global_key and not _any_scope_configured(settings):
        return ScopeAuthDecision(
            allowed=False,
            is_misconfigured=True,
            message=(
                "Server misconfigured: PO_API_KEY (or a scope-specific key) "
                "must be set when PO_SKIP_AUTH=false"
            ),
        )

    provided = (presented_api_key or "").strip()
    if not provided:
        return ScopeAuthDecision(
            allowed=False,
            is_misconfigured=False,
            message="Invalid or missing API key",
        )

    # Global key: only honour it if it is set AND either (a) no scope-specific
    # keys have been configured at all (single-key mode) or (b) the global key
    # is present — we still treat the global key as an implicit super-key so
    # that existing single-key deployments keep working.
    if global_key and hmac.compare_digest(provided, global_key):
        return ScopeAuthDecision(
            allowed=True, is_misconfigured=False, message="Authorized (global)"
        )

    if scope_keys and _match_any(provided, scope_keys):
        return ScopeAuthDecision(
            allowed=True,
            is_misconfigured=False,
            message=f"Authorized ({scope})",
        )

    return ScopeAuthDecision(
        allowed=False,
        is_misconfigured=False,
        message=f"API key does not grant scope {scope}",
    )


def require_scope(
    scope: str,
) -> Callable[[Request, APISettings], Awaitable[None]]:
    """FastAPI dependency factory enforcing ``scope`` on the decorated route.

    Callers use it as ``_: None = Depends(require_scope(Scope.TRACE_READ))``.
    """

    async def _dep(
        request: Request,
        settings: APISettings = Depends(get_api_settings),
    ) -> None:
        presented = extract_api_key_from_header_map(
            request.headers,
            configured_header_name=settings.api_key_header,
        )

        # If no scope is configured for any endpoint, behave exactly like the
        # legacy single-key auth (so plain PO_API_KEY deployments continue to
        # work without any code change on the client).
        if not _any_scope_configured(settings):
            decision = evaluate_auth_policy(
                skip_auth=settings.skip_auth,
                configured_api_key=settings.api_key,
                presented_api_key=presented,
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

        scope_decision = evaluate_scope_policy(
            settings=settings,
            presented_api_key=presented,
            scope=scope,
        )
        if scope_decision.allowed:
            return
        if scope_decision.is_misconfigured:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=scope_decision.message,
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=scope_decision.message,
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return _dep


__all__ = [
    "Scope",
    "ScopeAuthDecision",
    "evaluate_scope_policy",
    "require_scope",
]
