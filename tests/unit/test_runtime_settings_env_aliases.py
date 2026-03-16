from __future__ import annotations

import pytest

from po_core.runtime.settings import Settings


@pytest.mark.unit
@pytest.mark.phase5
def test_runtime_settings_accepts_legacy_llm_env_aliases(monkeypatch):
    monkeypatch.delenv("PO_LLM_ENABLED", raising=False)
    monkeypatch.delenv("PO_LLM_TIMEOUT", raising=False)
    monkeypatch.setenv("PO_ENABLE_LLM_PHILOSOPHERS", "1")
    monkeypatch.setenv("PO_LLM_PROVIDER", "claude")
    monkeypatch.setenv("PO_LLM_MODEL", "claude-haiku-4-5")
    monkeypatch.setenv("PO_LLM_TIMEOUT_S", "7.0")

    settings = Settings.from_env()

    assert settings.enable_llm_philosophers is True
    assert settings.llm_provider == "claude"
    assert settings.llm_model == "claude-haiku-4-5"
    assert settings.llm_timeout_s == pytest.approx(7.0)
