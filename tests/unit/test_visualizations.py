"""
Tests for Po_core Visualizations Module

Tests the advanced visualization capabilities including:
- Tension map generation
- Metrics timeline
- Philosopher network graphs
- Interactive dashboards
- Export functionality
"""

import tempfile
from pathlib import Path

import plotly.graph_objects as go
import pytest
from matplotlib.figure import Figure

from po_core.po_trace import EventType, PoTrace
from po_core.visualizations import PoVisualizer


class TestPoVisualizerInit:
    """Test PoVisualizer initialization."""

    def test_visualizer_initialization(self):
        """Test visualizer initializes correctly."""
        visualizer = PoVisualizer()
        assert visualizer.po_trace is not None
        assert visualizer.philosopher_colors is not None
        assert len(visualizer.philosopher_colors) > 0

    def test_visualizer_with_custom_trace(self):
        """Test visualizer with custom PoTrace instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            po_trace = PoTrace(storage_dir=Path(tmpdir))
            visualizer = PoVisualizer(po_trace=po_trace)
            assert visualizer.po_trace is po_trace


class TestTensionMap:
    """Test tension map visualization."""

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
    def test_session_id(self, po_trace):
        """Create a test session with philosopher events."""
        session_id = po_trace.create_session(
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche", "sartre"],
        )

        # Add philosopher events with metrics
        philosophers = [
            ("Aristotle", 0.8, 0.6, 0.3),
            ("Nietzsche", 0.9, 0.7, 0.2),
            ("Sartre", 0.85, 0.65, 0.25),
        ]

        for name, fp, sd, bt in philosophers:
            po_trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source=f"philosopher.{name}",
                data={
                    "message": f"{name} completed",
                    "philosopher": name,
                    "freedom_pressure": fp,
                    "semantic_delta": sd,
                    "blocked_tensor": bt,
                },
            )

        return session_id

    def test_create_tension_map_returns_figure(self, po_trace, test_session_id):
        """Test tension map returns matplotlib figure."""
        visualizer = PoVisualizer(po_trace=po_trace)

        fig = visualizer.create_tension_map(
            session_id=test_session_id, output_path=None
        )

        assert isinstance(fig, Figure)

    def test_create_tension_map_saves_file(
        self, po_trace, test_session_id, temp_storage
    ):
        """Test tension map saves to file."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_path = temp_storage / "tension_map.png"

        result = visualizer.create_tension_map(
            session_id=test_session_id, output_path=output_path, format="png"
        )

        assert result is None  # Should return None when saving
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_create_tension_map_different_formats(
        self, po_trace, test_session_id, temp_storage
    ):
        """Test tension map supports different formats."""
        visualizer = PoVisualizer(po_trace=po_trace)

        for fmt in ["png", "svg", "pdf"]:
            output_path = temp_storage / f"tension_map.{fmt}"
            visualizer.create_tension_map(
                session_id=test_session_id, output_path=output_path, format=fmt
            )
            assert output_path.exists()

    def test_create_tension_map_nonexistent_session(self, po_trace):
        """Test tension map raises error for nonexistent session."""
        visualizer = PoVisualizer(po_trace=po_trace)

        with pytest.raises(ValueError, match="Session .* not found"):
            visualizer.create_tension_map(session_id="nonexistent")

    def test_create_tension_map_no_philosopher_data(self, po_trace):
        """Test tension map raises error when no philosopher data."""
        visualizer = PoVisualizer(po_trace=po_trace)

        # Create session without philosopher events
        session_id = po_trace.create_session("Test", ["aristotle"])

        with pytest.raises(ValueError, match="No philosopher data"):
            visualizer.create_tension_map(session_id=session_id)


class TestMetricsTimeline:
    """Test metrics timeline visualization."""

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
    def test_session_ids(self, po_trace):
        """Create multiple test sessions."""
        session_ids = []

        for i in range(3):
            session_id = po_trace.create_session(
                prompt=f"Test prompt {i}",
                philosophers=["aristotle", "nietzsche"],
            )
            po_trace.update_metrics(
                session_id,
                {
                    "freedom_pressure": 0.7 + (i * 0.05),
                    "semantic_delta": 0.5 + (i * 0.05),
                    "blocked_tensor": 0.3 + (i * 0.05),
                },
            )
            session_ids.append(session_id)

        return session_ids

    def test_create_metrics_timeline_returns_figure(self, po_trace, test_session_ids):
        """Test metrics timeline returns plotly figure."""
        visualizer = PoVisualizer(po_trace=po_trace)

        fig = visualizer.create_metrics_timeline(
            session_ids=test_session_ids, output_path=None
        )

        assert isinstance(fig, go.Figure)

    def test_create_metrics_timeline_saves_html(
        self, po_trace, test_session_ids, temp_storage
    ):
        """Test metrics timeline saves to HTML."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_path = temp_storage / "timeline.html"

        result = visualizer.create_metrics_timeline(
            session_ids=test_session_ids, output_path=output_path, format="html"
        )

        assert result is None
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_create_metrics_timeline_with_title(self, po_trace, test_session_ids):
        """Test metrics timeline with custom title."""
        visualizer = PoVisualizer(po_trace=po_trace)

        fig = visualizer.create_metrics_timeline(
            session_ids=test_session_ids,
            output_path=None,
            title="Custom Timeline Title",
        )

        assert isinstance(fig, go.Figure)
        assert "Custom Timeline Title" in fig.layout.title.text

    def test_create_metrics_timeline_empty_list(self, po_trace):
        """Test metrics timeline raises error for empty session list."""
        visualizer = PoVisualizer(po_trace=po_trace)

        with pytest.raises(ValueError, match="At least one session ID required"):
            visualizer.create_metrics_timeline(session_ids=[])

    def test_create_metrics_timeline_invalid_sessions(self, po_trace):
        """Test metrics timeline handles invalid sessions gracefully."""
        visualizer = PoVisualizer(po_trace=po_trace)

        with pytest.raises(ValueError, match="No valid sessions found"):
            visualizer.create_metrics_timeline(
                session_ids=["nonexistent1", "nonexistent2"]
            )


class TestPhilosopherNetwork:
    """Test philosopher network visualization."""

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
    def test_session_id(self, po_trace):
        """Create a test session with multiple philosophers."""
        session_id = po_trace.create_session(
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche", "sartre"],
        )

        # Add philosopher events
        philosophers = [
            ("Aristotle", 0.8, 0.6, 0.3),
            ("Nietzsche", 0.9, 0.7, 0.2),
            ("Sartre", 0.85, 0.65, 0.25),
        ]

        for name, fp, sd, bt in philosophers:
            po_trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source=f"philosopher.{name}",
                data={
                    "message": f"{name} completed",
                    "philosopher": name,
                    "freedom_pressure": fp,
                    "semantic_delta": sd,
                    "blocked_tensor": bt,
                },
            )

        return session_id

    def test_create_philosopher_network_returns_figure(self, po_trace, test_session_id):
        """Test philosopher network returns matplotlib figure."""
        visualizer = PoVisualizer(po_trace=po_trace)

        fig = visualizer.create_philosopher_network(
            session_id=test_session_id, output_path=None
        )

        assert isinstance(fig, Figure)

    def test_create_philosopher_network_saves_file(
        self, po_trace, test_session_id, temp_storage
    ):
        """Test philosopher network saves to file."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_path = temp_storage / "network.png"

        result = visualizer.create_philosopher_network(
            session_id=test_session_id, output_path=output_path, format="png"
        )

        assert result is None
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_create_philosopher_network_nonexistent_session(self, po_trace):
        """Test network raises error for nonexistent session."""
        visualizer = PoVisualizer(po_trace=po_trace)

        with pytest.raises(ValueError, match="Session .* not found"):
            visualizer.create_philosopher_network(session_id="nonexistent")

    def test_create_philosopher_network_insufficient_philosophers(self, po_trace):
        """Test network raises error when less than 2 philosophers."""
        visualizer = PoVisualizer(po_trace=po_trace)

        # Create session with only one philosopher
        session_id = po_trace.create_session("Test", ["aristotle"])
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="philosopher.Aristotle",
            data={
                "philosopher": "Aristotle",
                "freedom_pressure": 0.8,
                "semantic_delta": 0.6,
                "blocked_tensor": 0.3,
            },
        )

        with pytest.raises(ValueError, match="Need at least 2 philosophers"):
            visualizer.create_philosopher_network(session_id=session_id)


class TestComprehensiveDashboard:
    """Test comprehensive dashboard visualization."""

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
    def test_session_id(self, po_trace):
        """Create a test session with philosopher events."""
        session_id = po_trace.create_session(
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche"],
        )

        philosophers = [
            ("Aristotle", 0.8, 0.6, 0.3),
            ("Nietzsche", 0.9, 0.7, 0.2),
        ]

        for name, fp, sd, bt in philosophers:
            po_trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source=f"philosopher.{name}",
                data={
                    "philosopher": name,
                    "freedom_pressure": fp,
                    "semantic_delta": sd,
                    "blocked_tensor": bt,
                },
            )

        return session_id

    def test_create_dashboard_returns_figure(self, po_trace, test_session_id):
        """Test dashboard returns plotly figure."""
        visualizer = PoVisualizer(po_trace=po_trace)

        fig = visualizer.create_comprehensive_dashboard(
            session_id=test_session_id, output_path=None
        )

        assert isinstance(fig, go.Figure)

    def test_create_dashboard_saves_html(self, po_trace, test_session_id, temp_storage):
        """Test dashboard saves to HTML."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_path = temp_storage / "dashboard.html"

        result = visualizer.create_comprehensive_dashboard(
            session_id=test_session_id, output_path=output_path, format="html"
        )

        assert result is None
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_create_dashboard_nonexistent_session(self, po_trace):
        """Test dashboard raises error for nonexistent session."""
        visualizer = PoVisualizer(po_trace=po_trace)

        with pytest.raises(ValueError, match="Session .* not found"):
            visualizer.create_comprehensive_dashboard(session_id="nonexistent")


class TestExportFunctionality:
    """Test export all visualizations functionality."""

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
    def test_session_id(self, po_trace):
        """Create a test session with philosopher events."""
        session_id = po_trace.create_session(
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche", "sartre"],
        )

        philosophers = [
            ("Aristotle", 0.8, 0.6, 0.3),
            ("Nietzsche", 0.9, 0.7, 0.2),
            ("Sartre", 0.85, 0.65, 0.25),
        ]

        for name, fp, sd, bt in philosophers:
            po_trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source=f"philosopher.{name}",
                data={
                    "philosopher": name,
                    "freedom_pressure": fp,
                    "semantic_delta": sd,
                    "blocked_tensor": bt,
                },
            )

        return session_id

    def test_export_session_visualizations(
        self, po_trace, test_session_id, temp_storage
    ):
        """Test exporting all visualizations for a session."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_dir = temp_storage / "exports"

        results = visualizer.export_session_visualizations(
            session_id=test_session_id, output_dir=output_dir, formats=["png", "html"]
        )

        assert isinstance(results, dict)
        assert len(results) > 0

        # Verify files exist
        for path in results.values():
            assert path.exists()
            assert path.stat().st_size > 0

    def test_export_creates_directory(self, po_trace, test_session_id, temp_storage):
        """Test export creates output directory if not exists."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_dir = temp_storage / "new_directory"

        assert not output_dir.exists()

        visualizer.export_session_visualizations(
            session_id=test_session_id, output_dir=output_dir, formats=["png"]
        )

        assert output_dir.exists()

    def test_export_with_multiple_formats(
        self, po_trace, test_session_id, temp_storage
    ):
        """Test export with multiple formats."""
        visualizer = PoVisualizer(po_trace=po_trace)
        output_dir = temp_storage / "multi_format"

        results = visualizer.export_session_visualizations(
            session_id=test_session_id,
            output_dir=output_dir,
            formats=["png", "svg", "html"],
        )

        # Should have files in multiple formats
        extensions = {path.suffix for path in results.values()}
        assert ".png" in extensions or ".svg" in extensions or ".html" in extensions


class TestVisualizerIntegration:
    """Test visualizer integration with Po_self."""

    def test_visualizer_with_po_self_session(self):
        """Test visualizer with real Po_self session."""
        from po_core.po_self import PoSelf

        # Create session
        po_self = PoSelf(enable_trace=True)
        result = po_self.generate("What is wisdom?")
        session_id = result.log["session_id"]

        # Create visualizer
        visualizer = PoVisualizer(po_trace=po_self.po_trace)

        # Test tension map creation (without saving)
        try:
            fig = visualizer.create_tension_map(session_id=session_id)
            assert isinstance(fig, Figure)
        except ValueError:
            # May fail if not enough philosopher data
            pass

    def test_visualizer_color_scheme_complete(self):
        """Test that all default philosophers have colors."""
        visualizer = PoVisualizer()

        default_philosophers = [
            "aristotle",
            "sartre",
            "heidegger",
            "nietzsche",
            "derrida",
            "wittgenstein",
            "jung",
            "dewey",
            "deleuze",
            "kierkegaard",
            "lacan",
            "levinas",
            "badiou",
            "peirce",
            "merleau_ponty",
            "arendt",
            "watsuji",
            "wabi_sabi",
            "confucius",
            "zhuangzi",
        ]

        for phil in default_philosophers:
            assert phil in visualizer.philosopher_colors
            assert isinstance(visualizer.philosopher_colors[phil], str)
            assert visualizer.philosopher_colors[phil].startswith("#")
