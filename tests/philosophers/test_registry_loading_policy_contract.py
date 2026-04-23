from __future__ import annotations

import pytest

from po_core.philosophers.manifest import PhilosopherSpec
from po_core.philosophers.registry import PhilosopherRegistry


def test_load_enabled_philosopher_is_strict_by_default() -> None:
    registry = PhilosopherRegistry(
        specs=[
            PhilosopherSpec(
                philosopher_id="broken_enabled",
                module="po_core.philosophers._does_not_exist",
                symbol="Missing",
                enabled=True,
            )
        ]
    )

    with pytest.raises(
        RuntimeError, match="failed_to_load_enabled_philosopher:broken_enabled"
    ):
        registry.load(["broken_enabled"])


def test_load_can_collect_enabled_failures_when_strict_disabled() -> None:
    registry = PhilosopherRegistry(
        specs=[
            PhilosopherSpec(
                philosopher_id="broken_enabled",
                module="po_core.philosophers._does_not_exist",
                symbol="Missing",
                enabled=True,
            )
        ]
    )

    philosophers, errors = registry.load(["broken_enabled"], strict_enabled=False)
    assert philosophers == []
    assert len(errors) == 1
    assert errors[0].philosopher_id == "broken_enabled"
    assert errors[0].error in {"ModuleNotFoundError", "ImportError"}
