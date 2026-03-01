from __future__ import annotations

from po_core.deliberation.roles import (
    DEFAULT_ROLES,
    PHILOSOPHER_ROLE_MAP,
    Role,
    RoleCoverage,
)
from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.runtime.settings import Settings


def test_default_roles_cover_all_axis_dimensions_v1():
    assert RoleCoverage.is_fully_covered(DEFAULT_ROLES)


def test_registry_can_filter_by_role_set():
    registry = PhilosopherRegistry(required_roles=(Role.DEONTOLOGIST,))
    selection = registry.select(SafetyMode.NORMAL)

    assert selection.selected_ids
    assert all(PHILOSOPHER_ROLE_MAP.get(pid) == Role.DEONTOLOGIST for pid in selection.selected_ids)


def test_settings_from_env_parses_po_roles(monkeypatch):
    monkeypatch.setenv("PO_ROLES", "utilitarian, deontologist")
    settings = Settings.from_env()
    assert settings.philosopher_roles == (Role.DEONTOLOGIST, Role.UTILITARIAN)
