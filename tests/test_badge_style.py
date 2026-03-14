from __future__ import annotations

import pytest

from po_echo.badge_style import get_label_config, normalize_label


def test_normalize_label_aliases() -> None:
    assert normalize_label("blocked") == "ECHO_BLOCKED"
    assert normalize_label("echo_check") == "ECHO_CHECK"


def test_get_label_config_contains_required_fields() -> None:
    config = get_label_config("ECHO_VERIFIED")
    assert config["display"] == "ECHO VERIFIED"
    assert config["pig_state"] == "🐷🌈"


def test_normalize_label_rejects_unknown() -> None:
    with pytest.raises(ValueError):
        normalize_label("something_else")
