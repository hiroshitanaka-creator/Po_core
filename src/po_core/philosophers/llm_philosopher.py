"""
LLM Philosopher — LLM API バックエンドを持つ哲学者基底クラス
=============================================================

``Philosopher`` を継承し、``reason()`` を LLM API 呼び出しで実装する。
既存の ``propose()`` / ``propose_async()`` / ``normalize_response()`` は
そのまま継承して使用する。

使用例（wiring.py 内）:
    adapter = LLMAdapter.from_settings(settings)
    ph = LLMPhilosopher.from_persona("kant", adapter)
    proposals = ph.propose(ctx, intent, tensors, memory)

設計原則:
- ``reason()`` のみオーバーライド — それ以外は Philosopher 基底に委譲
- LLM 障害時は空の推論（confidence=0.1）を返してパイプラインを止めない
- JSON パースを 2 段階で試みる（構造化 → raw テキスト）
- ``actual_model`` を ``metadata`` に記録（論文再現性）
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

import yaml

from po_core.philosophers.base import Philosopher
from po_core.philosophers.llm_personas import get_persona

if TYPE_CHECKING:
    from po_core.adapters.llm_adapter import LLMAdapter


_LLM_PHILOSOPHER_MAP_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "llm_philosopher_map.yaml"
)
_LLM_PHILOSOPHER_MAP_ENV = "PO_LLM_PHILOSOPHER_MAP_PATH"


def _resolve_llm_philosopher_map_path(path: Path | None = None) -> Path:
    """Resolve map path from explicit arg, env var, or bundled default."""
    if path is not None:
        return path

    override = os.getenv(_LLM_PHILOSOPHER_MAP_ENV, "").strip()
    if override:
        return Path(override).expanduser()

    return _LLM_PHILOSOPHER_MAP_PATH


def _load_llm_philosopher_map(path: Path | None = None) -> dict[str, dict[str, str]]:
    """Load philosopher-specific LLM provider/model overrides from YAML."""
    yaml_path = _resolve_llm_philosopher_map_path(path)
    if not yaml_path.exists():
        return {}

    try:
        payload = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError):
        return {}

    if not isinstance(payload, dict):
        return {}

    philosophers = payload.get("philosophers", {})
    if not isinstance(philosophers, dict):
        return {}

    normalized: dict[str, dict[str, str]] = {}
    for philosopher_id, cfg in philosophers.items():
        if not isinstance(philosopher_id, str) or not isinstance(cfg, dict):
            continue

        provider = cfg.get("provider")
        model = cfg.get("model")
        if not isinstance(provider, str) or not provider.strip():
            continue

        entry: dict[str, str] = {"provider": provider.strip()}
        if isinstance(model, str):
            entry["model"] = model.strip()
        normalized[philosopher_id] = entry

    return normalized


class LLMPhilosopher(Philosopher):
    """
    LLM API を使って哲学的推論を行う哲学者。

    Attributes:
        philosopher_id: manifest の philosopher_id（例: "kant"）
        _adapter: LLMAdapter インスタンス（共有シングルトン）
        _system_prompt: このペルソナのシステムプロンプト
    """

    def __init__(self, philosopher_id: str, adapter: "LLMAdapter") -> None:
        persona = get_persona(philosopher_id)
        super().__init__(
            name=persona.get("name", philosopher_id),
            description=persona.get("description", philosopher_id),
        )
        self.philosopher_id = philosopher_id
        self.tradition = persona.get("tradition", "")
        self._adapter = adapter
        self._system_prompt = persona.get("system_prompt", "")

    # ── Public factory ──────────────────────────────────────────────

    @classmethod
    def from_persona(
        cls, philosopher_id: str, adapter: "LLMAdapter"
    ) -> "LLMPhilosopher":
        """philosopher_id とアダプターから LLMPhilosopher を生成する。"""
        return cls(philosopher_id=philosopher_id, adapter=adapter)

    # ── Core override ───────────────────────────────────────────────

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        LLM API を呼んで哲学的推論を生成する。

        Args:
            prompt: ユーザー入力テキスト
            context: テンソル値・インテントなどのレガシーコンテキスト

        Returns:
            normalize_response() に渡せる形式の dict
        """
        if not self._system_prompt:
            return self._fallback(reason="no_persona_defined")

        raw = self._adapter.generate(self._system_prompt, prompt)
        if not raw:
            return self._fallback(reason="llm_unavailable")

        result = self._parse_llm_response(raw)
        result.setdefault("metadata", {})
        result["metadata"].update(
            {
                "philosopher": self.name,
                "llm_provider": self._adapter.provider.value,
                "llm_model": self._adapter.actual_model,
                "philosopher_id": self.philosopher_id,
            }
        )
        return result

    # ── Internal helpers ────────────────────────────────────────────

    def _parse_llm_response(self, raw: str) -> Dict[str, Any]:
        """
        LLM の出力から reasoning/perspective/confidence を抽出する。

        試行順序:
        1. 全体が JSON オブジェクト
        2. テキスト中の最初の {...} ブロック
        3. raw テキストをそのまま reasoning に使用
        """
        # 1) 全体 JSON
        try:
            data = json.loads(raw.strip())
            if isinstance(data, dict) and "reasoning" in data:
                return self._normalize_parsed(data)
        except (json.JSONDecodeError, ValueError):
            pass

        # 2) テキスト中の JSON ブロック（```json ... ``` も対応）
        json_match = re.search(r"\{[\s\S]*?\}", raw)
        if json_match:
            try:
                data = json.loads(json_match.group())
                if isinstance(data, dict) and "reasoning" in data:
                    return self._normalize_parsed(data)
            except (json.JSONDecodeError, ValueError):
                pass

        # 3) フォールバック: raw テキスト全体を reasoning に
        return {
            "reasoning": raw.strip(),
            "perspective": self.description,
            "confidence": 0.5,
            "tension": None,
        }

    def _normalize_parsed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """パース済み dict を PhilosopherResponse 互換形式に正規化する。"""
        confidence = data.get("confidence", 0.5)
        try:
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except (TypeError, ValueError):
            confidence = 0.5

        return {
            "reasoning": str(data.get("reasoning", "")),
            "perspective": str(data.get("perspective", self.description)),
            "confidence": confidence,
            "tension": data.get("tension"),
            "citations": data.get("citations", []),
            "action_type": data.get("action_type", "answer"),
        }

    def _fallback(self, reason: str = "unknown") -> Dict[str, Any]:
        """LLM が使えないときの最小応答。"""
        return {
            "reasoning": f"[LLM unavailable: {reason}]",
            "perspective": self.description,
            "confidence": 0.1,
            "tension": None,
            "metadata": {
                "philosopher": self.name,
                "llm_fallback": True,
                "fallback_reason": reason,
            },
        }

    def __repr__(self) -> str:
        return (
            f"LLMPhilosopher(id={self.philosopher_id!r}, "
            f"provider={self._adapter.provider.value!r})"
        )


def build_llm_philosopher_registry(
    adapter: "LLMAdapter",
    specs: Any = None,
    llm_philosopher_map: Optional[dict[str, dict[str, str]]] = None,
    *,
    max_normal: int = 42,
    max_warn: int = 5,
    max_critical: int = 1,
    budget_normal: int = 80,
    budget_warn: int = 12,
    budget_critical: int = 3,
    battalion_plans: Any = None,
    required_roles: Any = None,
) -> Any:
    """
    LLMPhilosopher インスタンスをキャッシュに持つ PhilosopherRegistry を構築する。

    既存の SPECS メタデータ（tags / cost / risk_level）を維持しつつ、
    ``load()`` 時に LLMPhilosopher インスタンスを返すようにする。
    ``dummy`` は元の DummyPhilosopher のままにする。

    Args:
        adapter: 全哲学者で共有する LLMAdapter
        specs: PhilosopherSpec リスト（None なら manifest.SPECS を使用）
        llm_philosopher_map: 哲学者ごとの provider/model 上書き設定
        ...その他は PhilosopherRegistry と同じパラメータ

    Returns:
        LLMPhilosopher がキャッシュされた PhilosopherRegistry
    """
    from po_core.philosophers.manifest import SPECS
    from po_core.philosophers.registry import PhilosopherRegistry

    if specs is None:
        specs = SPECS
    philosopher_map = (
        _load_llm_philosopher_map()
        if llm_philosopher_map is None
        else llm_philosopher_map
    )

    registry = PhilosopherRegistry(
        specs=specs,
        max_normal=max_normal,
        max_warn=max_warn,
        max_critical=max_critical,
        budget_normal=budget_normal,
        budget_warn=budget_warn,
        budget_critical=budget_critical,
        cache_instances=True,
        battalion_plans=battalion_plans,
        required_roles=required_roles,
    )

    # dummy 以外の全哲学者を LLMPhilosopher インスタンスでキャッシュに注入
    for spec in specs:
        if spec.philosopher_id == "dummy":
            continue  # dummy は元の DummyPhilosopher のまま
        if not spec.enabled:
            continue

        philosopher_adapter = adapter
        mapped = philosopher_map.get(spec.philosopher_id)
        if mapped:
            from po_core.adapters.llm_adapter import LLMAdapter

            provider = mapped.get("provider", "")
            model = mapped.get("model", "")
            try:
                philosopher_adapter = LLMAdapter(
                    provider=provider,
                    model=model,
                    timeout=adapter.timeout,
                )
            except Exception:
                philosopher_adapter = adapter

        registry._instances[spec.philosopher_id] = LLMPhilosopher(
            philosopher_id=spec.philosopher_id,
            adapter=philosopher_adapter,
        )

    return registry


__all__ = ["LLMPhilosopher", "build_llm_philosopher_registry"]
