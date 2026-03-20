from __future__ import annotations

import pytest

from po_core.adapters.llm_adapter import LLMErrorKind, LLMResult
from po_core.philosophers.llm_philosopher import LLMPhilosopher


class StubAdapter:
    def __init__(self, result: LLMResult) -> None:
        self._result = result
        self.provider = type("Provider", (), {"value": "openai"})()
        self.actual_model = result.actual_model or result.model or "gpt-4o-mini"

    def generate(self, system: str, user: str) -> LLMResult:
        return self._result


@pytest.mark.parametrize(
    ("result", "expected_reason"),
    [
        (
            LLMResult(text="", error_kind=LLMErrorKind.TIMEOUT, retriable=True),
            "provider_timeout",
        ),
        (
            LLMResult(
                text="",
                error_kind=LLMErrorKind.RATE_LIMIT,
                retriable=True,
                status_code=429,
            ),
            "provider_rate_limit",
        ),
        (
            LLMResult(
                text="", error_kind=LLMErrorKind.AUTH, retriable=False, status_code=401
            ),
            "provider_auth_error",
        ),
        (
            LLMResult(
                text="",
                error_kind=LLMErrorKind.TRANSIENT,
                retriable=True,
                status_code=503,
            ),
            "provider_5xx",
        ),
        (
            LLMResult(text="", error_kind=LLMErrorKind.UNKNOWN, retriable=False),
            "provider_unknown_error",
        ),
    ],
)
def test_reason_preserves_precise_fallback_reason(result, expected_reason):
    philosopher = LLMPhilosopher.from_persona("kant", StubAdapter(result))

    response = philosopher.reason("What is justice?")

    assert response["metadata"]["llm_fallback"] is True
    assert response["metadata"]["fallback_reason"] == expected_reason
    assert response["metadata"]["llm_provider"] == "openai"
    assert response["metadata"]["fallback"]["reason"] == expected_reason
    assert response["metadata"]["fallback"]["error_kind"] == result.error_kind.value
    assert response["metadata"]["fallback"]["retriable"] is result.retriable
    if result.status_code is not None:
        assert response["metadata"]["fallback"]["status_code"] == result.status_code
    assert response["confidence"] == pytest.approx(0.1)
    assert expected_reason in response["reasoning"]
