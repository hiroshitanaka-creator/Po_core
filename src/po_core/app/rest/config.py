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

from pydantic import AliasChoices, Field
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
    enable_llm_philosophers: bool = Field(
        default=False,
        validation_alias=AliasChoices("PO_LLM_ENABLED", "PO_ENABLE_LLM_PHILOSOPHERS"),
    )
    llm_provider: str = "gemini"
    llm_model: str = ""
    llm_timeout_s: float = Field(
        default=10.0,
        validation_alias=AliasChoices("PO_LLM_TIMEOUT", "PO_LLM_TIMEOUT_S"),
    )

    # Philosopher selection tuning (limit + budget per SafetyMode)
    philosopher_cost_budget_normal: int = 80
    philosopher_cost_budget_warn: int = 12
    philosopher_cost_budget_critical: int = 3
    philosophers_max_normal: int = 39
    philosophers_max_warn: int = 5
    philosophers_max_critical: int = 1

    # Trace storage
    max_trace_sessions: int = 1000
    trace_store_backend: str = "sqlite"  # sqlite | memory
    trace_db_path: str = ".po_core/trace_store.sqlite3"
    enable_trace_history: bool = False

    class Config:
        env_prefix = "PO_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        populate_by_name = True


# Module-level singleton (overridable in tests via dependency injection)
_settings: APISettings | None = None


def get_api_settings() -> APISettings:
    """Return cached APISettings instance."""
    global _settings
    if _settings is None:
        _settings = APISettings()
    return _settings


def set_api_settings(settings: APISettings) -> None:
    """Override the cached settings singleton.

    Used by ``create_app(settings=...)`` so that runtime overrides
    (e.g. test fixtures, programmatic configuration) are visible to
    components that call ``get_api_settings()`` — including the
    dynamic rate-limit callable in reason.py.
    """
    global _settings
    _settings = settings
