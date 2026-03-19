from __future__ import annotations

import pytest

from po_core.runtime.wiring import (
    _load_battalion_plans_from_env_or_package,
    _load_pareto_cfg_from_env_or_package,
)


@pytest.mark.unit
def test_missing_battalion_override_path_raises(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    missing_path = tmp_path / "missing_battalion.yaml"
    monkeypatch.setenv("PO_CORE_BATTALION_TABLE", str(missing_path))

    with pytest.raises(
        FileNotFoundError,
        match=f"PO_CORE_BATTALION_TABLE not found: {missing_path}",
    ):
        _load_battalion_plans_from_env_or_package()


@pytest.mark.unit
def test_missing_pareto_override_path_raises(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    missing_path = tmp_path / "missing_pareto.yaml"
    monkeypatch.setenv("PO_CORE_PARETO_TABLE", str(missing_path))

    with pytest.raises(
        FileNotFoundError,
        match=f"PO_CORE_PARETO_TABLE not found: {missing_path}",
    ):
        _load_pareto_cfg_from_env_or_package()


@pytest.mark.unit
def test_empty_battalion_override_uses_packaged_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PO_CORE_BATTALION_TABLE", "")

    battalion = _load_battalion_plans_from_env_or_package()

    assert battalion


@pytest.mark.unit
def test_empty_pareto_override_uses_packaged_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PO_CORE_PARETO_TABLE", "")

    pareto = _load_pareto_cfg_from_env_or_package()

    assert pareto is not None
