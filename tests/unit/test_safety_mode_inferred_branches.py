# SPDX-License-Identifier: AGPL-3.0-or-later
"""MODE-TR-2: Branch coverage for _build_safety_mode_inferred_payload.

Four branches in _run_phase_pre:
  1. freedom_pressure metric missing          → reason = "freedom_pressure_missing"
  2. fp < warn_threshold                      → reason = "freedom_pressure < warn_threshold"
  3. warn_threshold <= fp < critical_threshold → reason = "warn_threshold <= freedom_pressure < critical_threshold"
  4. fp >= critical_threshold                 → reason = "freedom_pressure >= critical_threshold"

Tests call infer_safety_mode() + _build_safety_mode_inferred_payload() together,
mirroring the exact composition used in _run_phase_pre.  No full pipeline needed.
"""

from __future__ import annotations

import pytest

from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ensemble import _build_safety_mode_inferred_payload

_DEFAULT_CFG = SafetyModeConfig(warn=0.30, critical=0.50, missing_mode=SafetyMode.WARN)


def _snapshot(**metrics) -> TensorSnapshot:
    return TensorSnapshot(metrics=metrics, version="test")


def _infer_and_build(
    snapshot: TensorSnapshot, config: SafetyModeConfig = _DEFAULT_CFG
) -> dict:
    mode, fp_value = infer_safety_mode(snapshot, config)
    return _build_safety_mode_inferred_payload(mode, fp_value, config)


class TestSafetyModeInferredBranches:
    """MODE-TR-2: All four reason branches produce correct payloads."""

    def test_missing_freedom_pressure(self) -> None:
        """Branch: freedom_pressure metric absent → missing_mode, reason='freedom_pressure_missing'."""
        payload = _infer_and_build(_snapshot())  # no freedom_pressure key

        assert (
            payload["mode"] == _DEFAULT_CFG.missing_mode.value
        ), f"Expected mode={_DEFAULT_CFG.missing_mode.value!r}; got {payload['mode']!r}"
        assert (
            payload["reason"] == "freedom_pressure_missing"
        ), f"Expected reason='freedom_pressure_missing'; got {payload['reason']!r}"
        assert payload["freedom_pressure"] is None
        assert payload["source_metric"] == "freedom_pressure"
        assert payload["warn_threshold"] == _DEFAULT_CFG.warn
        assert payload["critical_threshold"] == _DEFAULT_CFG.critical
        assert payload["missing_mode"] == _DEFAULT_CFG.missing_mode.value

    def test_normal_branch(self) -> None:
        """Branch: fp < warn_threshold → mode='normal', reason='freedom_pressure < warn_threshold'."""
        fp = 0.10  # below warn=0.30
        payload = _infer_and_build(_snapshot(freedom_pressure=fp))

        assert (
            payload["mode"] == "normal"
        ), f"fp={fp} < warn={_DEFAULT_CFG.warn}: expected mode='normal'; got {payload['mode']!r}"
        assert (
            payload["reason"] == "freedom_pressure < warn_threshold"
        ), f"Unexpected reason: {payload['reason']!r}"
        assert payload["freedom_pressure"] == pytest.approx(fp)

    def test_warn_branch(self) -> None:
        """Branch: warn <= fp < critical → mode='warn', reason='warn_threshold <= freedom_pressure < critical_threshold'."""
        fp = 0.40  # between warn=0.30 and critical=0.50
        payload = _infer_and_build(_snapshot(freedom_pressure=fp))

        assert payload["mode"] == "warn", (
            f"fp={fp} in [warn={_DEFAULT_CFG.warn}, crit={_DEFAULT_CFG.critical}): "
            f"expected mode='warn'; got {payload['mode']!r}"
        )
        assert (
            payload["reason"]
            == "warn_threshold <= freedom_pressure < critical_threshold"
        ), f"Unexpected reason: {payload['reason']!r}"
        assert payload["freedom_pressure"] == pytest.approx(fp)

    def test_critical_branch(self) -> None:
        """Branch: fp >= critical_threshold → mode='critical', reason='freedom_pressure >= critical_threshold'."""
        fp = 0.70  # above critical=0.50
        payload = _infer_and_build(_snapshot(freedom_pressure=fp))

        assert payload["mode"] == "critical", (
            f"fp={fp} >= critical={_DEFAULT_CFG.critical}: "
            f"expected mode='critical'; got {payload['mode']!r}"
        )
        assert (
            payload["reason"] == "freedom_pressure >= critical_threshold"
        ), f"Unexpected reason: {payload['reason']!r}"
        assert payload["freedom_pressure"] == pytest.approx(fp)


class TestSafetyModeInferredBoundaries:
    """MODE-TR-2: Boundary values land in the correct branch."""

    def test_warn_boundary_exact(self) -> None:
        """fp == warn_threshold exactly → mode='warn' (>= wins over <)."""
        fp = _DEFAULT_CFG.warn  # 0.30 exactly
        payload = _infer_and_build(_snapshot(freedom_pressure=fp))

        assert payload["mode"] == "warn"
        assert (
            payload["reason"]
            == "warn_threshold <= freedom_pressure < critical_threshold"
        )

    def test_critical_boundary_exact(self) -> None:
        """fp == critical_threshold exactly → mode='critical'."""
        fp = _DEFAULT_CFG.critical  # 0.50 exactly
        payload = _infer_and_build(_snapshot(freedom_pressure=fp))

        assert payload["mode"] == "critical"
        assert payload["reason"] == "freedom_pressure >= critical_threshold"

    def test_custom_missing_mode_warn(self) -> None:
        """missing_mode=WARN is reflected in payload when metric is absent."""
        cfg = SafetyModeConfig(warn=0.30, critical=0.50, missing_mode=SafetyMode.WARN)
        payload = _infer_and_build(_snapshot(), config=cfg)

        assert payload["mode"] == "warn"
        assert payload["missing_mode"] == "warn"
        assert payload["reason"] == "freedom_pressure_missing"
