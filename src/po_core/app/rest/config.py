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

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """
    API server settings.

    All fields read from environment variables with prefix ``PO_``.
    """

    # Server
    host: str = (
        "0.0.0.0"  # nosec B104 — intentional default for container deployments; override via PO_HOST
    )
    port: int = 8000
    workers: int = 1
    log_level: str = "info"
    reload: bool = False

    # Authentication
    api_key: str = Field(
        default="",
        validation_alias=AliasChoices("PO_API_KEY", "PO_CORE_API_KEY"),
    )
    api_key_header: str = Field(default="X-API-Key", min_length=1)
    skip_auth: bool = False  # Set True for local dev / testing
    ws_allow_query_api_key: bool = False

    # Scope-based API keys.  Each setting is a comma-separated list of keys
    # authorised for that scope.  When any scope key is configured, the global
    # ``api_key`` is no longer granted every scope implicitly — it only gets
    # the scopes it is explicitly listed under.  If every scope setting is
    # empty, behaviour falls back to the global ``api_key`` which is treated
    # as if it had all scopes (backwards-compatible single-key deployments).
    api_keys_reason_write: str = Field(
        default="",
        validation_alias=AliasChoices("PO_API_KEYS_REASON_WRITE"),
        description="Comma-separated API keys with scope reason:write.",
    )
    api_keys_trace_read: str = Field(
        default="",
        validation_alias=AliasChoices("PO_API_KEYS_TRACE_READ"),
        description="Comma-separated API keys with scope trace:read.",
    )
    api_keys_review_write: str = Field(
        default="",
        validation_alias=AliasChoices("PO_API_KEYS_REVIEW_WRITE"),
        description="Comma-separated API keys with scope review:write.",
    )
    # When true, redact PII-like payload fields and internal tracebacks from
    # /v1/trace responses and review comments before returning them to clients.
    redact_trace_responses: bool = Field(
        default=True,
        validation_alias=AliasChoices("PO_REDACT_TRACE_RESPONSES"),
        description=(
            "Redact PII / internal tracebacks from trace payloads and redact "
            "review comments before returning to the client."
        ),
    )

    # CORS — comma-separated list of allowed origins.
    # Default is local-only for safer public-package behavior.
    # Use "*" only for short-lived local development when you intentionally want permissive CORS.
    cors_origins: str = Field(
        default="http://localhost,http://127.0.0.1,http://localhost:3000,http://127.0.0.1:3000",
        validation_alias=AliasChoices("PO_CORS_ORIGINS", "PO_CORE_CORS_ORIGINS"),
    )

    # Rate limiting — requests per minute per IP for the /v1/reason endpoints.
    # Set to 0 to disable rate limiting.
    rate_limit_per_minute: int = 60
    trust_proxy_headers: bool = False
    request_timeout_s: float = 30.0

    # Bounded worker pool for the synchronous /v1/reason endpoint.  The
    # endpoint offloads the blocking pipeline to this executor and gates
    # submissions through an ``asyncio.Semaphore`` so the number of concurrent
    # in-flight reasoning jobs cannot exceed the pool size.  Before this the
    # endpoint used ``run_in_executor(None, ...)`` which dispatches onto the
    # default loop executor (typically ``min(32, cpu_count * 5)`` threads) —
    # enough that a burst of requests with short timeouts would keep growing
    # active workers even after the client hung up.  See
    # ``tests/test_reason_request_validation.py`` for regression coverage.
    reason_sync_max_workers: int = Field(
        default=4,
        ge=1,
        le=64,
        validation_alias=AliasChoices("PO_REASON_SYNC_MAX_WORKERS"),
    )

    # Po_core engine
    enable_solarwill: bool = True
    enable_intention_gate: bool = True
    enable_action_gate: bool = True
    enable_pareto_shadow: bool = False
    use_freedom_pressure_v2: bool = Field(
        default=False, validation_alias=AliasChoices("PO_FREEDOM_PRESSURE_V2")
    )
    deliberation_max_rounds: int = Field(
        default=2, validation_alias=AliasChoices("PO_DELIBERATION_MAX_ROUNDS")
    )
    philosopher_roles: str = Field(
        default="", validation_alias=AliasChoices("PO_ROLES")
    )
    philosopher_execution_mode: str = Field(
        default="process",
        validation_alias=AliasChoices("PO_PHILOSOPHER_EXECUTION_MODE"),
    )
    allow_unsafe_thread_execution: bool = False

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

    # Review queue storage
    review_store_backend: str = "sqlite"  # sqlite | memory
    review_db_path: str = ""

    @field_validator("philosopher_execution_mode", mode="before")
    @classmethod
    def _validate_philosopher_execution_mode(cls, value: object) -> str:
        normalized = str(value).strip().lower()
        if normalized not in {"thread", "process"}:
            raise ValueError("philosopher_execution_mode must be 'thread' or 'process'")
        return normalized

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


def parse_cors_origins(cors_origins: str) -> list[str]:
    """Parse a comma-separated CORS origins string into a stable list."""
    if cors_origins.strip() == "*":
        return ["*"]
    return [origin.strip() for origin in cors_origins.split(",") if origin.strip()]


def is_rate_limit_enabled(rate_limit_per_minute: int) -> bool:
    """Return True when request rate limiting should be enforced."""
    return rate_limit_per_minute > 0
