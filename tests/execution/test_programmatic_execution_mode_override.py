from __future__ import annotations

import asyncio
from types import SimpleNamespace

from po_core.domain.safety_mode import SafetyMode
from po_core.ensemble import _PhasePreResult, async_run_turn, run_turn
from po_core.runtime.settings import Settings


def _make_deps(execution_mode: str):
    return SimpleNamespace(
        settings=Settings(philosopher_execution_mode=execution_mode),
        tracer=SimpleNamespace(),
    )


def test_run_turn_uses_injected_execution_mode_over_env(monkeypatch):
    import po_core.ensemble as ensemble_mod

    monkeypatch.setenv("PO_PHILOSOPHER_EXECUTION_MODE", "thread")
    captured = {}

    monkeypatch.setattr(
        ensemble_mod,
        "_run_phase_pre",
        lambda ctx, deps, **kw: _PhasePreResult(
            memory=None,
            tensors=None,
            intent=None,
            mode=SafetyMode.NORMAL,
            philosophers=[],
            max_workers=2,
            timeout_s=0.5,
        ),
    )

    def _fake_run_philosophers(*args, **kwargs):
        captured["execution_mode"] = kwargs["execution_mode"]
        return [], []

    monkeypatch.setattr(ensemble_mod, "run_philosophers", _fake_run_philosophers)
    monkeypatch.setattr(
        ensemble_mod,
        "_run_phase_post",
        lambda ctx, deps, pre, proposals, run_results: captured,
    )

    result = run_turn(SimpleNamespace(request_id="req-sync"), _make_deps("process"))

    assert result["execution_mode"] == "process"


def test_async_run_turn_uses_injected_execution_mode_over_env(monkeypatch):
    import po_core.ensemble as ensemble_mod

    monkeypatch.setenv("PO_PHILOSOPHER_EXECUTION_MODE", "process")
    captured = {}

    monkeypatch.setattr(
        ensemble_mod,
        "_run_phase_pre",
        lambda ctx, deps, **kw: _PhasePreResult(
            memory=None,
            tensors=None,
            intent=None,
            mode=SafetyMode.NORMAL,
            philosophers=[],
            max_workers=3,
            timeout_s=0.25,
        ),
    )

    async def _fake_async_run_philosophers(*args, **kwargs):
        captured["execution_mode"] = kwargs["execution_mode"]
        return [], []

    monkeypatch.setattr(
        ensemble_mod, "async_run_philosophers", _fake_async_run_philosophers
    )
    monkeypatch.setattr(
        ensemble_mod,
        "_run_phase_post",
        lambda ctx, deps, pre, proposals, run_results: captured,
    )

    result = asyncio.run(
        async_run_turn(SimpleNamespace(request_id="req-async"), _make_deps("thread"))
    )

    assert result["execution_mode"] == "thread"
