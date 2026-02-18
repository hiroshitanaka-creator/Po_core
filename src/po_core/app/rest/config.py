"""
API Server Configuration
========================

Pydantic BaseSettings for environment-variable-driven configuration.

All settings can be overridden via environment variables or a .env file.
Prefix: PO_

Example .env:
    PO_API_KEY=secret-key-here
    PO_HOST=0.0.0.0
    PO_PORT=8000
    PO_WORKERS=4
    PO_LOG_LEVEL=info
    PO_CORS_ORIGINS=https://app.example.com,https://admin.example.com
    PO_RATE_LIMIT_PER_MINUTE=60
"""

from __future__ import annotations

from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """
    API server settings.

    All fields read from environment variables with prefix ``PO_``.
    """

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    log_level: str = "info"
    reload: bool = False

    # Authentication
    api_key: str = ""
    api_key_header: str = "X-API-Key"
    skip_auth: bool = False  # Set True for local dev / testing

    # CORS — comma-separated list of allowed origins.
    # Use "*" (default) to allow all origins in development.
    # In production set to specific domains: "https://app.example.com,https://admin.example.com"
    cors_origins: str = "*"

    # Rate limiting — requests per minute per IP for the /v1/reason endpoints.
    # Set to 0 to disable rate limiting.
    rate_limit_per_minute: int = 60

    # Po_core engine
    enable_solarwill: bool = True
    enable_intention_gate: bool = True
    enable_action_gate: bool = True

    # Trace storage
    max_trace_sessions: int = 1000

    class Config:
        env_prefix = "PO_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Module-level singleton (overridable in tests via dependency injection)
_settings: APISettings | None = None


def get_api_settings() -> APISettings:
    """Return cached APISettings instance."""
    global _settings
    if _settings is None:
        _settings = APISettings()
    return _settings
