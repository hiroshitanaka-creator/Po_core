"""
LLM Adapter — 4社統合クライアント
====================================

Gemini / OpenAI(GPT) / Anthropic(Claude) / xAI(Grok) を
単一インターフェースで切り替える。

設計原則:
- ``generate(system, user) -> LLMResult`` を公開
- 失敗時も構造化された失敗分類を返す（呼び出し側が安全にフォールバック）
- SDKは lazy import（provider 選択時のみロード）
- 1実験内で全哲学者が同一 provider/model を使う（シングルトン推奨）
- 使用モデルID を ``actual_model`` 属性に記録（論文再現性）

環境変数:
    GEMINI_API_KEY     — Google AI Studio キー
    OPENAI_API_KEY     — OpenAI キー
    ANTHROPIC_API_KEY  — Anthropic キー
    XAI_API_KEY        — xAI (Grok) キー
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger(__name__)

# provider 別デフォルトモデル（2026年3月調査）
_DEFAULT_MODELS: dict[str, str] = {
    "gemini": "gemini-2.0-flash-lite",
    "openai": "gpt-4o-mini",
    "claude": "claude-haiku-4-5",
    "grok": "grok-3-mini",
}

_RETRIABLE_ERROR_KINDS: frozenset["LLMErrorKind"] = frozenset()


class LLMProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    GROK = "grok"


class LLMErrorKind(str, Enum):
    NONE = "none"
    AUTH = "auth"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    TRANSIENT = "transient"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class LLMResult:
    text: str
    error_kind: LLMErrorKind = LLMErrorKind.NONE
    retriable: bool = False
    provider: str | None = None
    model: str | None = None
    actual_model: str | None = None
    status_code: int | None = None
    error_message: str | None = None

    @property
    def ok(self) -> bool:
        return self.error_kind == LLMErrorKind.NONE and bool(self.text)


_RETRIABLE_ERROR_KINDS = frozenset(
    {LLMErrorKind.RATE_LIMIT, LLMErrorKind.TIMEOUT, LLMErrorKind.TRANSIENT}
)


class LLMAdapter:
    """
    4社統合LLMクライアント。

    ``generate(system, user)`` を呼ぶと指定 provider に HTTP リクエストを送り、
    構造化された ``LLMResult`` を返す。

    Attributes:
        provider: 使用する LLM プロバイダ
        model: リクエストするモデル名
        actual_model: 実際に使用したモデルID（APIレスポンスから確認）
        timeout: タイムアウト秒数
    """

    def __init__(
        self,
        provider: str | LLMProvider,
        model: str = "",
        timeout: float = 10.0,
        max_retries: int = 2,
    ) -> None:
        self.provider = LLMProvider(provider)
        self.model = model or _DEFAULT_MODELS[self.provider.value]
        self.actual_model: str = self.model
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))

    # ── Public API ─────────────────────────────────────────────────

    def generate(self, system: str, user: str) -> LLMResult:
        """
        LLM にシステムプロンプト + ユーザープロンプトを送り、構造化結果を返す。
        """
        provider_fn = self._provider_callable()
        attempts = self.max_retries + 1
        last_result: LLMResult | None = None

        for attempt in range(1, attempts + 1):
            try:
                result = provider_fn(system, user)
            except Exception as exc:
                result = self._error_result_from_exception(exc)

            if result.ok:
                return result

            last_result = result
            logger.warning(
                "LLMAdapter.generate failed (provider=%s, model=%s, attempt=%s/%s, kind=%s, retriable=%s, status=%s): %s",
                self.provider.value,
                self.model,
                attempt,
                attempts,
                result.error_kind.value,
                result.retriable,
                result.status_code,
                result.error_message,
            )
            if not result.retriable or attempt >= attempts:
                break

        return last_result or self._empty_success_result()

    # ── Factory ────────────────────────────────────────────────────

    @classmethod
    def from_settings(cls, settings: object) -> "LLMAdapter":
        """Settings オブジェクトから LLMAdapter を構築する。"""
        return cls(
            provider=getattr(settings, "llm_provider", "gemini"),
            model=getattr(settings, "llm_model", ""),
            timeout=float(getattr(settings, "llm_timeout_s", 10.0)),
        )

    @classmethod
    def from_env(cls) -> "LLMAdapter":
        """環境変数から LLMAdapter を構築する（CLI・スクリプト用）。"""
        return cls(
            provider=os.getenv("PO_LLM_PROVIDER", "gemini"),
            model=os.getenv("PO_LLM_MODEL", ""),
            timeout=float(os.getenv("PO_LLM_TIMEOUT", "10.0")),
        )

    # ── Provider implementations ────────────────────────────────────

    def _generate_gemini(self, system: str, user: str) -> LLMResult:
        import google.genai as genai
        import google.genai.types as genai_types

        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        response = client.models.generate_content(
            model=self.model,
            contents=user,
            config=genai_types.GenerateContentConfig(
                system_instruction=system,
                max_output_tokens=1024,
            ),
            request_options=genai_types.RequestOptions(timeout=self.timeout),
        )
        self.actual_model = self.model
        return self._success_result(text=response.text or "")

    def _generate_openai_compat(self, system: str, user: str) -> LLMResult:
        from openai import OpenAI

        if self.provider == LLMProvider.GROK:
            client = OpenAI(
                api_key=os.environ["XAI_API_KEY"],
                base_url="https://api.x.ai/v1",
            )
        else:
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=1024,
            timeout=self.timeout,
        )
        if resp.model:
            self.actual_model = resp.model
        content = resp.choices[0].message.content or ""
        return self._success_result(text=content)

    def _generate_claude(self, system: str, user: str) -> LLMResult:
        from anthropic import Anthropic

        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
            timeout=self.timeout,
        )
        self.actual_model = msg.model or self.model
        text = msg.content[0].text if msg.content else ""
        return self._success_result(text=text)

    def _provider_callable(self) -> Callable[[str, str], LLMResult]:
        if self.provider == LLMProvider.GEMINI:
            return self._generate_gemini
        if self.provider in (LLMProvider.OPENAI, LLMProvider.GROK):
            return self._generate_openai_compat
        return self._generate_claude

    def _success_result(self, *, text: str) -> LLMResult:
        return LLMResult(
            text=text,
            error_kind=LLMErrorKind.NONE,
            retriable=False,
            provider=self.provider.value,
            model=self.model,
            actual_model=self.actual_model,
        )

    def _empty_success_result(self) -> LLMResult:
        return self._success_result(text="")

    def _error_result_from_exception(self, exc: Exception) -> LLMResult:
        status_code = self._extract_status_code(exc)
        error_kind = self._classify_error(exc, status_code)
        return LLMResult(
            text="",
            error_kind=error_kind,
            retriable=error_kind in _RETRIABLE_ERROR_KINDS,
            provider=self.provider.value,
            model=self.model,
            actual_model=self.actual_model,
            status_code=status_code,
            error_message=f"{type(exc).__name__}: {exc}",
        )

    def _classify_error(
        self, exc: Exception, status_code: int | None = None
    ) -> LLMErrorKind:
        if status_code in {401, 403}:
            return LLMErrorKind.AUTH
        if status_code == 429:
            return LLMErrorKind.RATE_LIMIT
        if status_code is not None and status_code >= 500:
            return LLMErrorKind.TRANSIENT

        name = type(exc).__name__.lower()
        message = str(exc).lower()

        if isinstance(exc, TimeoutError) or "timeout" in name or "timed out" in message:
            return LLMErrorKind.TIMEOUT
        if any(
            token in name for token in ("authentication", "permission", "unauthorized")
        ):
            return LLMErrorKind.AUTH
        if any(
            token in message
            for token in (
                "invalid api key",
                "unauthorized",
                "forbidden",
                "authentication",
            )
        ):
            return LLMErrorKind.AUTH
        if "rate" in name and "limit" in name:
            return LLMErrorKind.RATE_LIMIT
        if "rate limit" in message or "too many requests" in message:
            return LLMErrorKind.RATE_LIMIT
        if any(
            token in name
            for token in (
                "apiconnection",
                "connection",
                "server",
                "serviceunavailable",
            )
        ):
            return LLMErrorKind.TRANSIENT
        if any(
            token in message
            for token in (
                "connection reset",
                "temporary",
                "service unavailable",
                "bad gateway",
                "network",
            )
        ):
            return LLMErrorKind.TRANSIENT
        return LLMErrorKind.UNKNOWN

    def _extract_status_code(self, exc: Exception) -> int | None:
        candidates: list[Any] = [
            getattr(exc, "status_code", None),
            getattr(exc, "http_status", None),
        ]
        response = getattr(exc, "response", None)
        if response is not None:
            candidates.extend(
                [
                    getattr(response, "status_code", None),
                    getattr(response, "status", None),
                    getattr(response, "code", None),
                ]
            )
        body = getattr(exc, "body", None)
        if isinstance(body, dict):
            candidates.append(body.get("status"))
            error = body.get("error")
            if isinstance(error, dict):
                candidates.append(error.get("code"))

        for candidate in candidates:
            try:
                if candidate is None:
                    continue
                return int(candidate)
            except (TypeError, ValueError):
                continue
        return None

    def __repr__(self) -> str:
        return f"LLMAdapter(provider={self.provider.value!r}, model={self.model!r})"


__all__ = ["LLMAdapter", "LLMErrorKind", "LLMProvider", "LLMResult"]
