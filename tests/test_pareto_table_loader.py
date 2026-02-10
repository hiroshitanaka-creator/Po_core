"""
Test pareto_table loader
========================

Verify that load_pareto_table correctly parses JSON-in-YAML format
and resolves inheritance.
"""

from __future__ import annotations

import json

import pytest

from po_core.domain.safety_mode import SafetyMode
from po_core.runtime.pareto_table import load_pareto_table


def test_load_pareto_table_json_in_yaml(tmp_path):
    """Load JSON-in-YAML format with all fields."""
    p = tmp_path / "pareto_table.yaml"
    p.write_text(
        json.dumps(
            {
                "version": 9,
                "weights": {
                    "normal": {
                        "safety": 1.0,
                        "freedom": 0.0,
                        "explain": 0.0,
                        "brevity": 0.0,
                        "coherence": 0.0,
                    },
                    "warn": {"inherit": "normal"},
                    "critical": {"inherit": "normal"},
                    "unknown": {"inherit": "normal"},
                },
                "tuning": {
                    "brevity_max_len": 100,
                    "explain_mix": {"rationale": 0.5, "author_rel": 0.5},
                    "front_limit": 7,
                },
            }
        ),
        encoding="utf-8",
    )

    cfg = load_pareto_table(str(p))

    assert cfg.version == 9
    assert cfg.tuning.front_limit == 7
    assert cfg.tuning.brevity_max_len == 100
    assert cfg.tuning.explain_rationale_weight == 0.5
    assert cfg.tuning.explain_author_rel_weight == 0.5
    assert cfg.source == f"file:{p}"


def test_load_pareto_table_inherit_resolution(tmp_path):
    """Verify inherit resolution works correctly."""
    p = tmp_path / "pareto_table.yaml"
    p.write_text(
        json.dumps(
            {
                "version": 2,
                "weights": {
                    "normal": {
                        "safety": 0.25,
                        "freedom": 0.30,
                        "explain": 0.20,
                        "brevity": 0.10,
                        "coherence": 0.15,
                    },
                    "warn": {
                        "safety": 0.40,
                        "freedom": 0.10,
                        "explain": 0.20,
                        "brevity": 0.15,
                        "coherence": 0.25,
                    },
                    "critical": {
                        "safety": 0.55,
                        "freedom": 0.00,
                        "explain": 0.20,
                        "brevity": 0.15,
                        "coherence": 0.30,
                    },
                    "unknown": {"inherit": "warn"},
                },
                "tuning": {},
            }
        ),
        encoding="utf-8",
    )

    cfg = load_pareto_table(str(p))

    # unknown should inherit from warn
    w_unknown = cfg.weights_by_mode[SafetyMode.UNKNOWN]
    w_warn = cfg.weights_by_mode[SafetyMode.WARN]

    assert w_unknown.safety == w_warn.safety
    assert w_unknown.freedom == w_warn.freedom
    assert w_unknown.explain == w_warn.explain
    assert w_unknown.brevity == w_warn.brevity
    assert w_unknown.coherence == w_warn.coherence


def test_load_pareto_table_inherit_cycle_raises(tmp_path):
    """Verify circular inheritance raises ValueError."""
    p = tmp_path / "pareto_table.yaml"
    p.write_text(
        json.dumps(
            {
                "version": 1,
                "weights": {
                    "normal": {"inherit": "unknown"},
                    "warn": {"inherit": "normal"},
                    "critical": {"inherit": "warn"},
                    "unknown": {"inherit": "critical"},
                },
                "tuning": {},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="inherit cycle"):
        load_pareto_table(str(p))


def test_load_pareto_table_defaults_for_missing_tuning(tmp_path):
    """Verify default tuning values are used when not specified."""
    p = tmp_path / "pareto_table.yaml"
    p.write_text(
        json.dumps(
            {
                "version": 3,
                "weights": {
                    "normal": {
                        "safety": 0.25,
                        "freedom": 0.30,
                        "explain": 0.20,
                        "brevity": 0.10,
                        "coherence": 0.15,
                    },
                    "warn": {"inherit": "normal"},
                    "critical": {"inherit": "normal"},
                    "unknown": {"inherit": "normal"},
                },
            }
        ),
        encoding="utf-8",
    )

    cfg = load_pareto_table(str(p))

    # Default tuning values
    assert cfg.tuning.brevity_max_len == 2000
    assert cfg.tuning.explain_rationale_weight == 0.65
    assert cfg.tuning.explain_author_rel_weight == 0.35
    assert cfg.tuning.front_limit == 20


def test_pareto_config_defaults_has_source():
    """Verify ParetoConfig.defaults() has source='defaults'."""
    from po_core.domain.pareto_config import ParetoConfig

    cfg = ParetoConfig.defaults()
    assert cfg.source == "defaults"
