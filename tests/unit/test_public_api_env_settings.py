from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def _stub_system():
    return SimpleNamespace(
        memory_read=None,
        memory_write=None,
        tracer=None,
        tensor_engine=None,
        solarwill=None,
        gate=None,
        philosophers=[],
        aggregator=None,
        aggregator_shadow=None,
        registry=MagicMock(),
        settings=None,
        shadow_guard=None,
        deliberation_engine=None,
    )


@pytest.mark.unit
@pytest.mark.phase5
def test_public_run_uses_settings_from_env_when_settings_is_none(
    monkeypatch, _stub_system
):
    from po_core.app import api

    monkeypatch.setenv("PO_PHILOSOPHERS_MAX_NORMAL", "42")
    monkeypatch.setenv("PO_PHILOSOPHER_COST_BUDGET_NORMAL", "90")

    def _fake_build_test_system(*, settings):
        _stub_system.settings = settings
        return _stub_system

    def _fake_run_turn(ctx, deps):
        return {
            "status": "ok",
            "philosophers_max_normal": deps.settings.philosophers_max_normal,
            "philosopher_cost_budget_normal": deps.settings.philosopher_cost_budget_normal,
        }

    monkeypatch.setattr(api, "build_test_system", _fake_build_test_system)
    monkeypatch.setattr(api, "run_turn", _fake_run_turn)

    result = api.run("env check")

    assert result["status"] == "ok"
    assert result["philosophers_max_normal"] == 42
    assert result["philosopher_cost_budget_normal"] == 90


@pytest.mark.unit
@pytest.mark.phase5
def test_public_run_supports_philosopher_allowlist(monkeypatch, _stub_system):
    from po_core.app import api
    from po_core.philosophers.allowlist import AllowlistRegistry

    def _fake_build_test_system(*, settings):
        _stub_system.settings = settings
        return _stub_system

    def _fake_run_turn(ctx, deps):
        return {
            "status": "ok",
            "registry_type": type(deps.registry).__name__,
            "is_allowlist": isinstance(deps.registry, AllowlistRegistry),
        }

    monkeypatch.setattr(api, "build_test_system", _fake_build_test_system)
    monkeypatch.setattr(api, "run_turn", _fake_run_turn)

    result = api.run("allowlist check", philosophers=["kant"])

    assert result["status"] == "ok"
    assert result["is_allowlist"] is True


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_public_async_run_uses_settings_from_env_when_settings_is_none(
    monkeypatch, _stub_system
):
    from po_core.app import api

    monkeypatch.setenv("PO_PHILOSOPHERS_MAX_WARN", "7")
    monkeypatch.setenv("PO_PHILOSOPHER_COST_BUDGET_WARN", "15")

    def _fake_build_test_system(*, settings):
        _stub_system.settings = settings
        return _stub_system

    async def _fake_async_run_turn(ctx, deps):
        return {
            "status": "ok",
            "philosophers_max_warn": deps.settings.philosophers_max_warn,
            "philosopher_cost_budget_warn": deps.settings.philosopher_cost_budget_warn,
        }

    monkeypatch.setattr(api, "build_test_system", _fake_build_test_system)
    monkeypatch.setattr(api, "async_run_turn", _fake_async_run_turn)

    result = await api.async_run("env check")

    assert result["status"] == "ok"
    assert result["philosophers_max_warn"] == 7
    assert result["philosopher_cost_budget_warn"] == 15
