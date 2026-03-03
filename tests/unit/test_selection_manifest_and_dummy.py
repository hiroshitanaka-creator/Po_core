from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.registry import PhilosopherRegistry

NEW_PHILOSOPHERS = {"appiah", "fanon", "charles_taylor"}


def test_normal_selection_includes_new_philosophers():
    selection = PhilosopherRegistry(cache_instances=False).select(SafetyMode.NORMAL)

    assert NEW_PHILOSOPHERS.issubset(set(selection.selected_ids))
    assert len(selection.selected_ids) == 42


def test_critical_selection_never_picks_dummy_by_default_manifest():
    selection = PhilosopherRegistry(cache_instances=False).select(SafetyMode.CRITICAL)

    assert selection.selected_ids == ["confucius"]
    assert "dummy" not in selection.selected_ids
