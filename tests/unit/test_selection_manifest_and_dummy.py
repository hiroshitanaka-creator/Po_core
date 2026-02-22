from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.registry import PhilosopherRegistry

AI_IDS = {"claude_anthropic", "gpt_chatgpt", "gemini_google", "grok_xai"}


def test_normal_selection_excludes_ai_slots_by_default():
    selection = PhilosopherRegistry(cache_instances=False).select(SafetyMode.NORMAL)

    assert AI_IDS.isdisjoint(selection.selected_ids)
    assert len(selection.selected_ids) == 39


def test_critical_selection_never_picks_dummy_by_default_manifest():
    selection = PhilosopherRegistry(cache_instances=False).select(SafetyMode.CRITICAL)

    assert selection.selected_ids == ["confucius"]
    assert "dummy" not in selection.selected_ids
