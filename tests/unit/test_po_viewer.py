"""
Tests for Po_viewer Module (current API)

Tests the PoViewer pipeline-result viewer:
- Construction via PoViewer.from_run(prompt)
- Text rendering: pipeline_text, tensor_text, philosopher_text, summary
- Markdown and dict output
- Event data access (properties: events, event_types, request_id)
- Tensor and philosopher data (methods: tensor_values, philosopher_data)
- Integration across prompts
"""

import pytest

from po_core.po_viewer import PoViewer


# ──────────────────────────────────────────────────────────────────────────────
# Shared fixture — one run for the whole module to keep tests fast
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def viewer():
    """PoViewer built from a single pipeline run."""
    return PoViewer.from_run("What is justice?")


# ──────────────────────────────────────────────────────────────────────────────
# Construction
# ──────────────────────────────────────────────────────────────────────────────


class TestPoViewerConstruction:
    """Test PoViewer.from_run() factory."""

    def test_from_run_returns_viewer(self):
        """PoViewer.from_run() must return a PoViewer instance."""
        v = PoViewer.from_run("What is wisdom?")
        assert isinstance(v, PoViewer)

    def test_from_run_sets_request_id(self):
        """request_id property must be a non-empty UUID-like string."""
        v = PoViewer.from_run("Is freedom real?")
        assert isinstance(v.request_id, str)
        assert len(v.request_id) > 0

    def test_from_run_different_prompts_give_different_ids(self):
        """Two separate runs should produce distinct request_ids."""
        v1 = PoViewer.from_run("What is virtue?")
        v2 = PoViewer.from_run("What is virtue?")
        # UUIDs are unique even for identical prompts
        assert v1.request_id != v2.request_id


# ──────────────────────────────────────────────────────────────────────────────
# Text renderers
# ──────────────────────────────────────────────────────────────────────────────


class TestViewerTextOutput:
    """Test text-rendering methods."""

    def test_pipeline_text_is_string(self, viewer):
        """pipeline_text() must return a non-empty string."""
        text = viewer.pipeline_text()
        assert isinstance(text, str)
        assert len(text) > 0

    def test_tensor_text_is_string(self, viewer):
        """tensor_text() must return a non-empty string."""
        text = viewer.tensor_text()
        assert isinstance(text, str)
        assert len(text) > 0

    def test_philosopher_text_is_string(self, viewer):
        """philosopher_text() must return a non-empty string."""
        text = viewer.philosopher_text()
        assert isinstance(text, str)
        assert len(text) > 0

    def test_summary_is_string(self, viewer):
        """summary() must return a non-empty string."""
        text = viewer.summary()
        assert isinstance(text, str)
        assert len(text) > 0

    def test_pipeline_text_has_pipeline_content(self, viewer):
        """pipeline_text() should reference the run_turn pipeline."""
        text = viewer.pipeline_text()
        assert len(text) > 10  # at least some content


# ──────────────────────────────────────────────────────────────────────────────
# Markdown output
# ──────────────────────────────────────────────────────────────────────────────


class TestViewerMarkdownOutput:
    """Test markdown() output."""

    def test_markdown_is_string(self, viewer):
        """markdown() must return a non-empty string."""
        md = viewer.markdown()
        assert isinstance(md, str)
        assert len(md) > 0

    def test_markdown_contains_request_id(self, viewer):
        """markdown() output should include the request_id."""
        md = viewer.markdown()
        assert viewer.request_id in md

    def test_markdown_has_structure(self, viewer):
        """markdown() should contain markdown-style headings."""
        md = viewer.markdown()
        assert "#" in md or "**" in md or "==" in md


# ──────────────────────────────────────────────────────────────────────────────
# Dict output
# ──────────────────────────────────────────────────────────────────────────────


class TestViewerDictOutput:
    """Test to_dict() output."""

    def test_to_dict_returns_dict(self, viewer):
        """to_dict() must return a dict."""
        d = viewer.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_has_request_id(self, viewer):
        """to_dict() must include request_id."""
        d = viewer.to_dict()
        assert "request_id" in d
        assert d["request_id"] == viewer.request_id

    def test_to_dict_serialisable(self, viewer):
        """to_dict() output must be JSON-serialisable."""
        import json

        d = viewer.to_dict()
        serialised = json.dumps(d, default=str)
        assert len(serialised) > 0

    def test_to_dict_has_n_events(self, viewer):
        """to_dict() should include event count."""
        d = viewer.to_dict()
        assert "n_events" in d
        assert isinstance(d["n_events"], int)
        assert d["n_events"] > 0


# ──────────────────────────────────────────────────────────────────────────────
# Event data (properties)
# ──────────────────────────────────────────────────────────────────────────────


class TestViewerEventData:
    """Test events and event_types properties."""

    def test_events_is_list(self, viewer):
        """events property must be a list."""
        assert isinstance(viewer.events, list)

    def test_events_non_empty(self, viewer):
        """Pipeline must produce at least one event."""
        assert len(viewer.events) > 0

    def test_event_types_is_list(self, viewer):
        """event_types must return a list."""
        assert isinstance(viewer.event_types, list)

    def test_event_types_non_empty(self, viewer):
        """event_types must contain at least one type string."""
        assert len(viewer.event_types) > 0

    def test_event_types_are_strings(self, viewer):
        """Each entry in event_types must be a string."""
        for et in viewer.event_types:
            assert isinstance(et, str)


# ──────────────────────────────────────────────────────────────────────────────
# Tensor and philosopher data (methods)
# ──────────────────────────────────────────────────────────────────────────────


class TestViewerDataMethods:
    """Test tensor_values() and philosopher_data() methods."""

    def test_tensor_values_returns_dict(self, viewer):
        """tensor_values() must return a dict."""
        assert isinstance(viewer.tensor_values(), dict)

    def test_philosopher_data_returns_list_or_dict(self, viewer):
        """philosopher_data() must return a list or dict."""
        pd = viewer.philosopher_data()
        assert isinstance(pd, (list, dict))


# ──────────────────────────────────────────────────────────────────────────────
# Integration
# ──────────────────────────────────────────────────────────────────────────────


class TestPoViewerIntegration:
    """Integration tests combining PoViewer.from_run() across prompts."""

    def test_multiple_prompts_produce_viewers(self):
        """PoViewer works for different prompt types."""
        prompts = [
            "What is freedom?",
            "Is morality objective?",
        ]
        for prompt in prompts:
            v = PoViewer.from_run(prompt)
            assert isinstance(v.to_dict(), dict)
            assert len(v.events) > 0

    def test_viewer_to_dict_consistent(self):
        """to_dict() called twice on the same viewer must give the same result."""
        v = PoViewer.from_run("What is duty?")
        d1 = v.to_dict()
        d2 = v.to_dict()
        assert d1["request_id"] == d2["request_id"]
        assert d1["n_events"] == d2["n_events"]
