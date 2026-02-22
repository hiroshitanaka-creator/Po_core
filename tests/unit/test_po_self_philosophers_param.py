"""
PR-2: Unit tests for philosophers allowlist behaviour in PoSelf.generate().

Verifies:
- _AllowlistRegistry.select() filters selection by the caller-supplied list
- Empty intersection raises ValueError (no silent pass-through)
- load() is delegated unchanged to the wrapped registry
- generate(philosophers=None) leaves registry untouched (regression guard)
- generate(philosophers=[...]) injects _AllowlistRegistry into EnsembleDeps
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch, call

from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.registry import Selection
from po_core.po_self import PoSelf, _AllowlistRegistry

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_selection(ids: list[str]) -> Selection:
    return Selection(
        mode=SafetyMode.NORMAL,
        selected_ids=ids,
        cost_total=len(ids) * 2,
        covered_tags=["planner", "critic", "compliance"],
    )


def _make_wrapped(selected_ids: list[str]) -> MagicMock:
    wrapped = MagicMock()
    wrapped.select.return_value = _make_selection(selected_ids)
    wrapped.load.return_value = ([], [])
    return wrapped


# ---------------------------------------------------------------------------
# _AllowlistRegistry.select() — core filter logic
# ---------------------------------------------------------------------------


class TestAllowlistRegistrySelect:
    def test_filters_to_intersection(self):
        """IDs in both the selection and the allowlist are returned."""
        wrapped = _make_wrapped(["aristotle", "kant", "plato"])
        reg = _AllowlistRegistry(wrapped, ["kant", "plato", "hegel"])
        sel = reg.select(SafetyMode.NORMAL)
        assert sel.selected_ids == ["kant", "plato"]

    def test_single_id_allowlist(self):
        """Single-element allowlist works when the ID is selected by safety."""
        wrapped = _make_wrapped(["aristotle", "confucius", "wittgenstein"])
        reg = _AllowlistRegistry(wrapped, ["confucius"])
        sel = reg.select(SafetyMode.NORMAL)
        assert sel.selected_ids == ["confucius"]

    def test_preserves_safety_selection_order(self):
        """Filtered list preserves the order from the underlying registry."""
        wrapped = _make_wrapped(["a", "b", "c", "d"])
        reg = _AllowlistRegistry(wrapped, ["d", "b"])
        sel = reg.select(SafetyMode.NORMAL)
        # order from safety selection is ["a", "b", "c", "d"] → intersection keeps ["b", "d"]
        assert sel.selected_ids == ["b", "d"]

    def test_empty_intersection_raises_value_error(self):
        """ValueError with informative message when no IDs overlap."""
        wrapped = _make_wrapped(["aristotle", "kant"])
        reg = _AllowlistRegistry(wrapped, ["mill", "rawls"])
        with pytest.raises(ValueError, match="allowlist"):
            reg.select(SafetyMode.NORMAL)

    def test_error_message_contains_allowlist_and_mode(self):
        """The ValueError message names the allowlist and the SafetyMode."""
        wrapped = _make_wrapped(["aristotle"])
        reg = _AllowlistRegistry(wrapped, ["nietzsche"])
        with pytest.raises(ValueError) as exc_info:
            reg.select(SafetyMode.NORMAL)
        msg = str(exc_info.value)
        assert "nietzsche" in msg
        assert "normal" in msg.lower()

    def test_underlying_select_called_with_mode(self):
        """_AllowlistRegistry always calls wrapped.select() with the given mode."""
        wrapped = _make_wrapped(["confucius"])
        reg = _AllowlistRegistry(wrapped, ["confucius"])
        reg.select(SafetyMode.WARN)
        wrapped.select.assert_called_once_with(SafetyMode.WARN)

    def test_returned_selection_mode_matches_input(self):
        """The returned Selection.mode reflects the input mode."""
        wrapped = _make_wrapped(["confucius"])
        reg = _AllowlistRegistry(wrapped, ["confucius"])
        sel = reg.select(SafetyMode.WARN)
        assert sel.mode == SafetyMode.WARN


# ---------------------------------------------------------------------------
# _AllowlistRegistry.load() — delegation
# ---------------------------------------------------------------------------


class TestAllowlistRegistryLoad:
    def test_load_delegates_to_wrapped(self):
        """load() passes IDs straight to the underlying registry."""
        wrapped = _make_wrapped(["aristotle"])
        sentinel_result = (["instance"], [])
        wrapped.load.return_value = sentinel_result

        reg = _AllowlistRegistry(wrapped, ["aristotle"])
        result = reg.load(["aristotle"])
        wrapped.load.assert_called_once_with(["aristotle"])
        assert result is sentinel_result


# ---------------------------------------------------------------------------
# PoSelf.generate() — registry injection
# ---------------------------------------------------------------------------


class TestPoSelfGeneratePhilosophersParam:
    """
    Verify that generate(philosophers=...) injects _AllowlistRegistry into
    EnsembleDeps without running the full pipeline (mocked run_turn).

    Note: build_test_system and run_turn are imported locally inside generate(),
    so we must patch them at their *source* module paths.
    """

    # Patch targets: local imports inside generate() must be patched at source
    _BUILD_PATH = "po_core.runtime.wiring.build_test_system"
    _RUN_TURN_PATH = "po_core.ensemble.run_turn"

    @staticmethod
    def _make_run_turn_result():
        return {
            "request_id": "test-req-id",
            "status": "ok",
            "proposal": {
                "proposal_id": "pareto:aristotle:1",
                "action_type": "answer",
                "content": "Test answer",
                "confidence": 0.8,
                "assumption_tags": [],
                "risk_tags": [],
            },
        }

    @staticmethod
    def _make_mock_sys(selected_ids=("aristotle", "confucius")):
        mock_sys = MagicMock()
        mock_sel = Selection(
            mode=SafetyMode.NORMAL,
            selected_ids=list(selected_ids),
            cost_total=len(selected_ids) * 2,
            covered_tags=["planner"],
        )
        mock_sys.registry.select.return_value = mock_sel
        mock_sys.registry.load.return_value = ([], [])
        return mock_sys

    def test_philosophers_none_uses_system_registry(self):
        """When philosophers=None, system.registry is used directly (no wrapping)."""
        fake_result = self._make_run_turn_result()
        captured_deps = {}

        def capture_run_turn(ctx, deps):
            captured_deps["deps"] = deps
            return fake_result

        mock_sys = self._make_mock_sys()
        with (
            patch(self._BUILD_PATH, return_value=mock_sys),
            patch(self._RUN_TURN_PATH, side_effect=capture_run_turn),
        ):
            PoSelf().generate("test prompt", philosophers=None)

        assert "deps" in captured_deps
        # registry should be the raw mock_sys.registry, not an _AllowlistRegistry
        assert not isinstance(captured_deps["deps"].registry, _AllowlistRegistry)

    def test_philosophers_list_activates_allowlist_registry(self):
        """When philosophers=[...] is given, _AllowlistRegistry is injected."""
        fake_result = self._make_run_turn_result()
        captured_deps = {}

        def capture_run_turn(ctx, deps):
            captured_deps["deps"] = deps
            return fake_result

        mock_sys = self._make_mock_sys(["aristotle", "confucius"])
        with (
            patch(self._BUILD_PATH, return_value=mock_sys),
            patch(self._RUN_TURN_PATH, side_effect=capture_run_turn),
        ):
            PoSelf().generate("test prompt", philosophers=["aristotle"])

        assert "deps" in captured_deps
        registry = captured_deps["deps"].registry
        assert isinstance(
            registry, _AllowlistRegistry
        ), "Expected _AllowlistRegistry when philosophers list is provided"

    def test_philosophers_empty_list_raises_value_error(self):
        """Empty allowlist produces no overlap → ValueError from _AllowlistRegistry.

        run_turn is given a side_effect that calls deps.registry.select() to
        simulate what _run_phase_pre does; this exercises the allowlist filter.
        """

        def trigger_select(ctx, deps):
            deps.registry.select(SafetyMode.NORMAL)
            return self._make_run_turn_result()

        mock_sys = self._make_mock_sys(["aristotle"])
        with (
            patch(self._BUILD_PATH, return_value=mock_sys),
            patch(self._RUN_TURN_PATH, side_effect=trigger_select),
        ):
            with pytest.raises(ValueError):
                PoSelf().generate("test prompt", philosophers=[])

    def test_philosophers_no_overlap_raises_value_error(self):
        """IDs not in safety selection → ValueError with 'allowlist' in message.

        Same simulation pattern: run_turn side_effect triggers registry.select().
        """

        def trigger_select(ctx, deps):
            deps.registry.select(SafetyMode.NORMAL)
            return self._make_run_turn_result()

        mock_sys = self._make_mock_sys(["aristotle", "kant"])
        with (
            patch(self._BUILD_PATH, return_value=mock_sys),
            patch(self._RUN_TURN_PATH, side_effect=trigger_select),
        ):
            with pytest.raises(ValueError, match="allowlist"):
                PoSelf().generate("test prompt", philosophers=["mill", "rawls"])
