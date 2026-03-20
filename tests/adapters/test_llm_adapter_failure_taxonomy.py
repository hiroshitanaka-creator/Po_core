from __future__ import annotations

from po_core.adapters.llm_adapter import LLMAdapter, LLMErrorKind, LLMResult


class FakeError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def test_generate_classifies_auth_without_retry(monkeypatch):
    adapter = LLMAdapter(provider="openai", model="gpt-4o-mini", max_retries=2)
    calls = {"count": 0}

    def _boom(system: str, user: str) -> LLMResult:
        calls["count"] += 1
        raise FakeError("invalid api key", status_code=401)

    monkeypatch.setattr(adapter, "_generate_openai_compat", _boom)

    result = adapter.generate("system", "user")

    assert result.text == ""
    assert result.error_kind is LLMErrorKind.AUTH
    assert result.retriable is False
    assert result.status_code == 401
    assert calls["count"] == 1


def test_generate_retries_rate_limit_until_success(monkeypatch):
    adapter = LLMAdapter(provider="openai", model="gpt-4o-mini", max_retries=2)
    calls = {"count": 0}

    def _flaky(system: str, user: str) -> LLMResult:
        calls["count"] += 1
        if calls["count"] < 3:
            raise FakeError("too many requests", status_code=429)
        adapter.actual_model = "gpt-4o-mini-2026-03"
        return LLMResult(
            text="structured answer",
            provider="openai",
            model="gpt-4o-mini",
            actual_model=adapter.actual_model,
        )

    monkeypatch.setattr(adapter, "_generate_openai_compat", _flaky)

    result = adapter.generate("system", "user")

    assert result.text == "structured answer"
    assert result.error_kind is LLMErrorKind.NONE
    assert calls["count"] == 3


def test_generate_classifies_timeout_as_retriable(monkeypatch):
    adapter = LLMAdapter(
        provider="gemini", model="gemini-2.0-flash-lite", max_retries=1
    )
    calls = {"count": 0}

    def _timeout(system: str, user: str) -> LLMResult:
        calls["count"] += 1
        raise TimeoutError("request timed out")

    monkeypatch.setattr(adapter, "_generate_gemini", _timeout)

    result = adapter.generate("system", "user")

    assert result.error_kind is LLMErrorKind.TIMEOUT
    assert result.retriable is True
    assert calls["count"] == 2


def test_generate_classifies_provider_5xx_as_transient(monkeypatch):
    adapter = LLMAdapter(provider="claude", model="claude-haiku-4-5", max_retries=0)

    def _server_error(system: str, user: str) -> LLMResult:
        raise FakeError("service unavailable", status_code=503)

    monkeypatch.setattr(adapter, "_generate_claude", _server_error)

    result = adapter.generate("system", "user")

    assert result.error_kind is LLMErrorKind.TRANSIENT
    assert result.retriable is True
    assert result.status_code == 503


def test_generate_classifies_unrecognized_failure_as_unknown(monkeypatch):
    adapter = LLMAdapter(provider="openai", model="gpt-4o-mini", max_retries=0)

    def _unknown(system: str, user: str) -> LLMResult:
        raise RuntimeError("unexpected parser explosion")

    monkeypatch.setattr(adapter, "_generate_openai_compat", _unknown)

    result = adapter.generate("system", "user")

    assert result.error_kind is LLMErrorKind.UNKNOWN
    assert result.retriable is False
