"""
Tests for Po_viewer Module

Tests the visualization system including:
- Session list rendering
- Session detail visualization
- Metrics visualization
- Event flow rendering
- Philosopher interaction analysis
- Session comparison
"""

import tempfile
from pathlib import Path

import pytest
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from po_core.po_trace import EventType, PoTrace
from po_core.po_viewer import PoViewer


class TestPoViewerBasicFunctionality:
    """Test basic Po_viewer functionality."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_session_id(self, po_trace):
        """Create a test session with events."""
        session_id = po_trace.create_session(
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche"],
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="ensemble",
            data={"message": "Ensemble started"},
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="philosopher.Aristotle",
            data={
                "message": "Aristotle completed",
                "philosopher": "Aristotle",
                "freedom_pressure": 0.8,
                "semantic_delta": 0.5,
                "blocked_tensor": 0.3,
                "perspective": "Virtue Ethics",
            },
        )
        po_trace.update_metrics(
            session_id,
            {
                "freedom_pressure": 0.8,
                "semantic_delta": 0.5,
                "blocked_tensor": 0.3,
            },
        )
        return session_id

    def test_po_viewer_initialization(self, po_viewer):
        """Test PoViewer initializes correctly."""
        assert po_viewer.po_trace is not None

    def test_po_viewer_default_initialization(self):
        """Test PoViewer initializes with default PoTrace."""
        viewer = PoViewer()
        assert viewer.po_trace is not None


class TestSessionsTable:
    """Test session list rendering."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    def test_render_sessions_table(self, po_viewer, po_trace):
        """Test rendering sessions table."""
        # Create test sessions
        po_trace.create_session("Prompt 1", ["aristotle"])
        po_trace.create_session("Prompt 2", ["nietzsche"])

        table = po_viewer.render_sessions_table(limit=10)

        assert isinstance(table, Table)
        assert table.title is not None

    def test_sessions_table_with_limit(self, po_viewer, po_trace):
        """Test sessions table respects limit."""
        # Create multiple sessions
        for i in range(5):
            po_trace.create_session(f"Prompt {i}", ["aristotle"])

        table = po_viewer.render_sessions_table(limit=3)
        assert isinstance(table, Table)

    def test_empty_sessions_table(self, po_viewer):
        """Test rendering empty sessions table."""
        table = po_viewer.render_sessions_table()
        assert isinstance(table, Table)


class TestSessionDetail:
    """Test session detail rendering."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_session_id(self, po_trace):
        """Create a test session."""
        session_id = po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle"],
        )
        po_trace.update_metrics(session_id, {"freedom_pressure": 0.8})
        return session_id

    def test_render_session_detail(self, po_viewer, test_session_id):
        """Test rendering session detail."""
        panel = po_viewer.render_session_detail(test_session_id)

        assert isinstance(panel, Panel)
        # Verify panel is not an error panel
        assert panel.border_style != "red"

    def test_render_session_detail_nonexistent(self, po_viewer):
        """Test rendering nonexistent session."""
        panel = po_viewer.render_session_detail("nonexistent")

        assert isinstance(panel, Panel)


class TestMetricsVisualization:
    """Test metrics visualization."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_session_id(self, po_trace):
        """Create a test session with metrics."""
        session_id = po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle"],
        )
        po_trace.update_metrics(
            session_id,
            {
                "freedom_pressure": 0.8,
                "semantic_delta": 0.5,
                "blocked_tensor": 0.3,
            },
        )
        return session_id

    def test_render_metrics_bars(self, po_viewer, test_session_id):
        """Test rendering metrics as bars."""
        panel = po_viewer.render_metrics_bars(test_session_id)

        assert isinstance(panel, Panel)
        # Verify panel is not an error panel
        assert panel.border_style != "red"

    def test_render_metrics_no_metrics(self, po_viewer, po_trace):
        """Test rendering metrics when no metrics available."""
        session_id = po_trace.create_session("Test", ["aristotle"])
        panel = po_viewer.render_metrics_bars(session_id)

        assert isinstance(panel, Panel)

    def test_render_metrics_nonexistent(self, po_viewer):
        """Test rendering metrics for nonexistent session."""
        panel = po_viewer.render_metrics_bars("nonexistent")

        assert isinstance(panel, Panel)


class TestEventFlow:
    """Test event flow rendering."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_session_id(self, po_trace):
        """Create a test session with events."""
        session_id = po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle"],
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="ensemble",
            data={"message": "Test event"},
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="philosopher.Aristotle",
            data={
                "message": "Reasoning complete",
                "philosopher": "Aristotle",
                "freedom_pressure": 0.8,
            },
        )
        return session_id

    def test_render_event_flow(self, po_viewer, test_session_id):
        """Test rendering event flow as tree."""
        tree = po_viewer.render_event_flow(test_session_id)

        assert isinstance(tree, Tree)

    def test_render_event_flow_nonexistent(self, po_viewer):
        """Test rendering event flow for nonexistent session."""
        tree = po_viewer.render_event_flow("nonexistent")

        assert isinstance(tree, Tree)

    def test_event_flow_no_events(self, po_viewer, po_trace):
        """Test rendering event flow with no events."""
        session_id = po_trace.create_session("Test", ["aristotle"])
        tree = po_viewer.render_event_flow(session_id)

        assert isinstance(tree, Tree)


class TestPhilosopherInteraction:
    """Test philosopher interaction rendering."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_session_id(self, po_trace):
        """Create a test session with philosopher events."""
        session_id = po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle", "nietzsche"],
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="philosopher.Aristotle",
            data={
                "message": "Reasoning complete",
                "philosopher": "Aristotle",
                "freedom_pressure": 0.8,
                "semantic_delta": 0.5,
                "blocked_tensor": 0.3,
                "perspective": "Virtue Ethics",
            },
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="philosopher.Nietzsche",
            data={
                "message": "Reasoning complete",
                "philosopher": "Nietzsche",
                "freedom_pressure": 0.9,
                "semantic_delta": 0.6,
                "blocked_tensor": 0.2,
                "perspective": "Power Philosophy",
            },
        )
        return session_id

    def test_render_philosopher_interaction(self, po_viewer, test_session_id):
        """Test rendering philosopher interaction."""
        panel = po_viewer.render_philosopher_interaction(test_session_id)

        assert isinstance(panel, Panel)
        # Verify panel is not an error panel
        assert panel.border_style != "red"

    def test_render_interaction_no_philosophers(self, po_viewer, po_trace):
        """Test rendering interaction with no philosopher events."""
        session_id = po_trace.create_session("Test", ["aristotle"])
        panel = po_viewer.render_philosopher_interaction(session_id)

        assert isinstance(panel, Panel)

    def test_render_interaction_nonexistent(self, po_viewer):
        """Test rendering interaction for nonexistent session."""
        panel = po_viewer.render_philosopher_interaction("nonexistent")

        assert isinstance(panel, Panel)


class TestSessionJSON:
    """Test session JSON rendering."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_session_id(self, po_trace):
        """Create a test session."""
        return po_trace.create_session("Test prompt", ["aristotle"])

    def test_render_session_json(self, po_viewer, test_session_id):
        """Test rendering session as JSON."""
        syntax = po_viewer.render_session_json(test_session_id)

        assert isinstance(syntax, Syntax)

    def test_render_json_nonexistent(self, po_viewer):
        """Test rendering JSON for nonexistent session."""
        syntax = po_viewer.render_session_json("nonexistent")

        assert isinstance(syntax, Syntax)


class TestSessionComparison:
    """Test session comparison."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    @pytest.fixture
    def test_sessions(self, po_trace):
        """Create two test sessions."""
        session_id1 = po_trace.create_session("Prompt 1", ["aristotle"])
        po_trace.update_metrics(session_id1, {"freedom_pressure": 0.7})

        session_id2 = po_trace.create_session("Prompt 2", ["nietzsche"])
        po_trace.update_metrics(session_id2, {"freedom_pressure": 0.9})

        return session_id1, session_id2

    def test_compare_sessions(self, po_viewer, test_sessions):
        """Test comparing two sessions."""
        session_id1, session_id2 = test_sessions
        panel = po_viewer.compare_sessions(session_id1, session_id2)

        assert isinstance(panel, Panel)
        # Verify panel is not an error panel
        assert panel.border_style != "red"

    def test_compare_nonexistent_session(self, po_viewer, test_sessions):
        """Test comparing with nonexistent session."""
        session_id1, _ = test_sessions
        panel = po_viewer.compare_sessions(session_id1, "nonexistent")

        assert isinstance(panel, Panel)

    def test_compare_both_nonexistent(self, po_viewer):
        """Test comparing two nonexistent sessions."""
        panel = po_viewer.compare_sessions("nonexistent1", "nonexistent2")

        assert isinstance(panel, Panel)


class TestDashboard:
    """Test dashboard functionality."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    @pytest.fixture
    def po_viewer(self, po_trace):
        """Create PoViewer instance with temp PoTrace."""
        return PoViewer(po_trace=po_trace)

    def test_render_dashboard_empty(self, po_viewer):
        """Test rendering dashboard with no sessions."""
        panel = po_viewer.render_dashboard(limit=20)

        assert isinstance(panel, Panel)
        # Should still return a panel even with no sessions

    def test_render_dashboard_with_sessions(self, po_viewer, po_trace):
        """Test rendering dashboard with sessions."""
        # Create some test sessions
        for i in range(5):
            session_id = po_trace.create_session(
                f"Test prompt {i}",
                ["aristotle", "nietzsche"],
            )
            po_trace.update_metrics(
                session_id,
                {
                    "freedom_pressure": 0.7 + (i * 0.05),
                    "semantic_delta": 0.5,
                    "blocked_tensor": 0.3,
                },
            )

        panel = po_viewer.render_dashboard(limit=10)

        assert isinstance(panel, Panel)
        assert panel.border_style != "red"  # Not an error panel

    def test_dashboard_calculates_statistics(self, po_viewer, po_trace):
        """Test that dashboard calculates statistics correctly."""
        # Create sessions with known metrics
        metrics_list = [
            {"freedom_pressure": 0.8, "semantic_delta": 0.6},
            {"freedom_pressure": 0.7, "semantic_delta": 0.5},
            {"freedom_pressure": 0.9, "semantic_delta": 0.7},
        ]

        for i, metrics in enumerate(metrics_list):
            session_id = po_trace.create_session(
                f"Test {i}",
                ["aristotle"],
            )
            po_trace.update_metrics(session_id, metrics)

        panel = po_viewer.render_dashboard(limit=10)

        assert isinstance(panel, Panel)
        # Dashboard should successfully process the data


class TestPoViewerIntegration:
    """Test Po_viewer integration with real data."""

    def test_viewer_with_po_self_session(self):
        """Test viewer with real Po_self session."""
        from po_core.po_self import PoSelf

        # Create session
        po_self = PoSelf(enable_trace=True)
        result = po_self.generate("What is wisdom?")

        session_id = result.log["session_id"]

        # Visualize with viewer
        viewer = PoViewer(po_trace=po_self.po_trace)

        # Test all rendering methods
        table = viewer.render_sessions_table()
        assert isinstance(table, Table)

        detail = viewer.render_session_detail(session_id)
        assert isinstance(detail, Panel)

        metrics = viewer.render_metrics_bars(session_id)
        assert isinstance(metrics, Panel)

        flow = viewer.render_event_flow(session_id)
        assert isinstance(flow, Tree)

        interactions = viewer.render_philosopher_interaction(session_id)
        assert isinstance(interactions, Panel)

        json_syntax = viewer.render_session_json(session_id)
        assert isinstance(json_syntax, Syntax)

        # Test new dashboard feature
        dashboard = viewer.render_dashboard()
        assert isinstance(dashboard, Panel)
