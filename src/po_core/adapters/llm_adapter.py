"""
LLM Adapter — 4社統合クライアント
====================================

Gemini / OpenAI(GPT) / Anthropic(Claude) / xAI(Grok) を
単一インターフェースで切り替える。

設計原則:
- ``generate(system, user) -> str`` のみ公開
- 失敗時は空文字列を返す（呼び出し側がフォールバック）
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
from enum import Enum
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    pass

# provider 別デフォルトモデル（2026年3月調査）
_DEFAULT_MODELS: dict[str, str] = {
    "gemini": "gemini-2.0-flash-lite",
    "openai": "gpt-4o-mini",
    "claude": "claude-haiku-4-5",
    "grok": "grok-3-mini",
}


class LLMProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    GROK = "grok"


class LLMAdapter:
    """
    4社統合LLMクライアント。

    ``generate(system, user)`` を呼ぶと指定 provider に HTTP リクエストを送り、
    テキストを返す。エラー時は空文字列を返す。

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
    ) -> None:
        self.provider = LLMProvider(provider)
        self.model = model or _DEFAULT_MODELS[self.provider.value]
        self.actual_model: str = self.model
        self.timeout = timeout

    # ── Public API ─────────────────────────────────────────────────

    def generate(self, system: str, user: str) -> str:
        """
        LLM にシステムプロンプト + ユーザープロンプトを送り、テキストを返す。

        Args:
            system: システムプロンプト（哲学者ペルソナ定義）
            user: ユーザー入力（哲学的に分析するテキスト）

        Returns:
            LLM のテキスト出力。エラー時は空文字列。
        """
        try:
            if self.provider == LLMProvider.GEMINI:
                return self._generate_gemini(system, user)
            elif self.provider in (LLMProvider.OPENAI, LLMProvider.GROK):
                return self._generate_openai_compat(system, user)
            elif self.provider == LLMProvider.CLAUDE:
                return self._generate_claude(system, user)
        except Exception as exc:
            logger.warning(
                "LLMAdapter.generate failed (provider=%s, model=%s): %s: %s",
                self.provider.value,
                self.model,
                type(exc).__name__,
                exc,
            )
        return ""

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

    def _generate_gemini(self, system: str, user: str) -> str:
        import google.genai as genai  # type: ignore[import-untyped]
        import google.genai.types as genai_types  # type: ignore[import-untyped]

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
        return response.text or ""

    def _generate_openai_compat(self, system: str, user: str) -> str:
        from openai import OpenAI  # type: ignore[import-untyped]

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
        return resp.choices[0].message.content or ""

    def _generate_claude(self, system: str, user: str) -> str:
        from anthropic import Anthropic  # type: ignore[import-untyped]

        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
            timeout=self.timeout,
        )
        self.actual_model = msg.model or self.model
        return msg.content[0].text if msg.content else ""

    def __repr__(self) -> str:
        return f"LLMAdapter(provider={self.provider.value!r}, model={self.model!r})"


__all__ = ["LLMAdapter", "LLMProvider"]
