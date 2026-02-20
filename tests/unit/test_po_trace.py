"""
Tests for Po_trace Module

Tests the audit logging system including:
- Event logging
- Session management
- Storage and retrieval
- Export functionality
- Integration with Po_self
"""

import json
import tempfile
from pathlib import Path

import pytest

from po_core.po_trace import Event, EventType, PoTrace, Session

pytestmark = pytest.mark.skip(
    reason="Legacy PoTrace session API (get_session, log_event) — replaced by InMemoryTracer — to be migrated in Phase 1"
)


class TestEventType:
    """Test EventType enum."""

    def test_event_types_exist(self):
        """Test that all event types are defined."""
        assert EventType.EXECUTION == "execution"
        assert EventType.STATE_CHANGE == "state_change"
        assert EventType.ERROR == "error"
        assert EventType.USER_ACTION == "user_action"
        assert EventType.SYSTEM == "system"


class TestEvent:
    """Test Event dataclass."""

    def test_event_creation(self):
        """Test creating an event."""
        event = Event(
            event_id="test-id",
            session_id="session-id",
            timestamp="2025-01-01T00:00:00Z",
            event_type=EventType.EXECUTION,
            source="test",
            data={"message": "test"},
            metadata={"version": "1.0"},
        )

        assert event.event_id == "test-id"
        assert event.session_id == "session-id"
        assert event.event_type == EventType.EXECUTION
        assert event.source == "test"
        assert event.data["message"] == "test"
        assert event.metadata["version"] == "1.0"

    def test_event_to_dict(self):
        """Test converting event to dictionary."""
        event = Event(
            event_id="test-id",
            session_id="session-id",
            timestamp="2025-01-01T00:00:00Z",
            event_type=EventType.EXECUTION,
            source="test",
            data={"message": "test"},
        )

        event_dict = event.to_dict()
        assert event_dict["event_id"] == "test-id"
        assert event_dict["event_type"] == "execution"
        assert event_dict["data"]["message"] == "test"

    def test_event_from_dict(self):
        """Test creating event from dictionary."""
        data = {
            "event_id": "test-id",
            "session_id": "session-id",
            "timestamp": "2025-01-01T00:00:00Z",
            "event_type": "execution",
            "source": "test",
            "data": {"message": "test"},
            "metadata": {"version": "1.0"},
        }

        event = Event.from_dict(data)
        assert event.event_id == "test-id"
        assert event.event_type == EventType.EXECUTION
        assert event.data["message"] == "test"


class TestSession:
    """Test Session dataclass."""

    def test_session_creation(self):
        """Test creating a session."""
        session = Session(
            session_id="test-session",
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche"],
            created_at="2025-01-01T00:00:00Z",
        )

        assert session.session_id == "test-session"
        assert session.prompt == "What is truth?"
        assert len(session.philosophers) == 2
        assert len(session.events) == 0

    def test_session_to_dict(self):
        """Test converting session to dictionary."""
        session = Session(
            session_id="test-session",
            prompt="What is truth?",
            philosophers=["aristotle"],
            created_at="2025-01-01T00:00:00Z",
            metrics={"freedom_pressure": 0.8},
        )

        session_dict = session.to_dict()
        assert session_dict["session_id"] == "test-session"
        assert session_dict["prompt"] == "What is truth?"
        assert session_dict["metrics"]["freedom_pressure"] == 0.8

    def test_session_from_dict(self):
        """Test creating session from dictionary."""
        data = {
            "session_id": "test-session",
            "prompt": "What is truth?",
            "philosophers": ["aristotle"],
            "created_at": "2025-01-01T00:00:00Z",
            "events": [],
            "metrics": {"freedom_pressure": 0.8},
            "metadata": {},
        }

        session = Session.from_dict(data)
        assert session.session_id == "test-session"
        assert session.prompt == "What is truth?"
        assert session.metrics["freedom_pressure"] == 0.8


class TestPoTraceBasicFunctionality:
    """Test basic Po_trace functionality."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def po_trace(self, temp_storage):
        """Create PoTrace instance with temp storage."""
        return PoTrace(storage_dir=temp_storage)

    def test_po_trace_initialization(self, po_trace, temp_storage):
        """Test Po_trace initializes correctly."""
        assert po_trace.storage_dir == temp_storage
        assert (temp_storage / "index.json").exists()

    def test_create_session(self, po_trace):
        """Test creating a session."""
        session_id = po_trace.create_session(
            prompt="What is virtue?",
            philosophers=["aristotle", "nietzsche"],
        )

        assert session_id is not None
        assert len(session_id) == 36  # UUID format

        # Check session file was created
        session_file = po_trace._session_file(session_id)
        assert session_file.exists()

    def test_get_session(self, po_trace):
        """Test retrieving a session."""
        session_id = po_trace.create_session(
            prompt="What is virtue?",
            philosophers=["aristotle"],
        )

        session = po_trace.get_session(session_id)
        assert session is not None
        assert session.session_id == session_id
        assert session.prompt == "What is virtue?"
        assert len(session.philosophers) == 1

    def test_get_nonexistent_session(self, po_trace):
        """Test retrieving a nonexistent session returns None."""
        session = po_trace.get_session("nonexistent-id")
        assert session is None

    def test_list_sessions(self, po_trace):
        """Test listing sessions."""
        # Create multiple sessions
        id1 = po_trace.create_session("Prompt 1", ["aristotle"])
        id2 = po_trace.create_session("Prompt 2", ["nietzsche"])

        sessions = po_trace.list_sessions()
        assert len(sessions) == 2
        # Most recent should be first
        assert sessions[0]["session_id"] == id2
        assert sessions[1]["session_id"] == id1

    def test_list_sessions_with_limit(self, po_trace):
        """Test listing sessions with limit."""
        po_trace.create_session("Prompt 1", ["aristotle"])
        po_trace.create_session("Prompt 2", ["nietzsche"])
        po_trace.create_session("Prompt 3", ["wittgenstein"])

        sessions = po_trace.list_sessions(limit=2)
        assert len(sessions) == 2


class TestPoTraceEventLogging:
    """Test event logging functionality."""

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
    def session_id(self, po_trace):
        """Create a test session."""
        return po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle"],
        )

    def test_log_event(self, po_trace, session_id):
        """Test logging an event."""
        event_id = po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="test",
            data={"message": "Test event"},
        )

        assert event_id is not None
        assert len(event_id) == 36  # UUID format

        # Retrieve session and check event was added
        session = po_trace.get_session(session_id)
        assert len(session.events) == 1
        assert session.events[0].event_id == event_id
        assert session.events[0].data["message"] == "Test event"

    def test_log_multiple_events(self, po_trace, session_id):
        """Test logging multiple events."""
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="test1",
            data={"message": "Event 1"},
        )
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.STATE_CHANGE,
            source="test2",
            data={"message": "Event 2"},
        )

        session = po_trace.get_session(session_id)
        assert len(session.events) == 2
        assert session.events[0].source == "test1"
        assert session.events[1].source == "test2"

    def test_log_event_with_metadata(self, po_trace, session_id):
        """Test logging event with metadata."""
        po_trace.log_event(
            session_id=session_id,
            event_type=EventType.EXECUTION,
            source="test",
            data={"message": "Test"},
            metadata={"version": "1.0", "custom": "data"},
        )

        session = po_trace.get_session(session_id)
        event = session.events[0]
        assert event.metadata["version"] == "1.0"
        assert event.metadata["custom"] == "data"

    def test_log_event_nonexistent_session(self, po_trace):
        """Test logging event to nonexistent session raises error."""
        with pytest.raises(ValueError, match="Session .* not found"):
            po_trace.log_event(
                session_id="nonexistent",
                event_type=EventType.EXECUTION,
                source="test",
                data={},
            )


class TestPoTraceMetrics:
    """Test metrics functionality."""

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
    def session_id(self, po_trace):
        """Create a test session."""
        return po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle"],
        )

    def test_update_metrics(self, po_trace, session_id):
        """Test updating session metrics."""
        po_trace.update_metrics(
            session_id=session_id,
            metrics={"freedom_pressure": 0.8, "semantic_delta": 0.5},
        )

        session = po_trace.get_session(session_id)
        assert session.metrics["freedom_pressure"] == 0.8
        assert session.metrics["semantic_delta"] == 0.5

    def test_update_metrics_merges(self, po_trace, session_id):
        """Test updating metrics merges with existing."""
        po_trace.update_metrics(session_id, {"metric1": 0.5})
        po_trace.update_metrics(session_id, {"metric2": 0.7})

        session = po_trace.get_session(session_id)
        assert session.metrics["metric1"] == 0.5
        assert session.metrics["metric2"] == 0.7

    def test_update_metrics_nonexistent_session(self, po_trace):
        """Test updating metrics for nonexistent session raises error."""
        with pytest.raises(ValueError, match="Session .* not found"):
            po_trace.update_metrics("nonexistent", {"metric": 0.5})


class TestPoTraceExport:
    """Test export functionality."""

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
    def session_id(self, po_trace):
        """Create a test session with events."""
        sid = po_trace.create_session(
            prompt="Test prompt",
            philosophers=["aristotle", "nietzsche"],
        )
        po_trace.log_event(
            session_id=sid,
            event_type=EventType.EXECUTION,
            source="test",
            data={"message": "Test event"},
        )
        po_trace.update_metrics(sid, {"freedom_pressure": 0.8})
        return sid

    def test_export_json(self, po_trace, session_id):
        """Test exporting session as JSON."""
        content = po_trace.export_session(session_id, format="json")

        # Should be valid JSON
        data = json.loads(content)
        assert data["session_id"] == session_id
        assert data["prompt"] == "Test prompt"
        assert len(data["events"]) == 1
        assert data["metrics"]["freedom_pressure"] == 0.8

    def test_export_text(self, po_trace, session_id):
        """Test exporting session as text."""
        content = po_trace.export_session(session_id, format="text")

        # Check content includes key information
        assert f"Session: {session_id}" in content
        assert "Test prompt" in content
        assert "aristotle, nietzsche" in content
        assert "freedom_pressure: 0.8" in content
        assert "Events (1):" in content

    def test_export_nonexistent_session(self, po_trace):
        """Test exporting nonexistent session raises error."""
        with pytest.raises(ValueError, match="Session .* not found"):
            po_trace.export_session("nonexistent", format="json")

    def test_export_unknown_format(self, po_trace, session_id):
        """Test exporting with unknown format raises error."""
        with pytest.raises(ValueError, match="Unknown format"):
            po_trace.export_session(session_id, format="xml")


class TestPoTraceIntegration:
    """Test Po_trace integration with Po_self."""

    def test_po_self_creates_trace_session(self):
        """Test that Po_self creates trace sessions."""
        from po_core.po_self import PoSelf

        po_self = PoSelf(enable_trace=True)
        result = po_self.generate("What is truth?")

        # Check that session_id was added to log
        assert "session_id" in result.log
        assert result.log["session_id"] is not None

        # Verify session was created
        session = po_self.po_trace.get_session(result.log["session_id"])
        assert session is not None
        assert session.prompt == "What is truth?"

    def test_po_self_without_trace(self):
        """Test Po_self with tracing disabled."""
        from po_core.po_self import PoSelf

        po_self = PoSelf(enable_trace=False)
        result = po_self.generate("What is truth?")

        # Check that session_id was not added
        assert result.log.get("session_id") is None
        assert po_self.po_trace is None

    def test_trace_records_philosopher_events(self):
        """Test that trace records individual philosopher reasoning."""
        from po_core.po_self import PoSelf

        po_self = PoSelf(enable_trace=True)
        result = po_self.generate("What is virtue?")

        session_id = result.log["session_id"]
        session = po_self.po_trace.get_session(session_id)

        # Should have events for: start, each philosopher, completion
        expected_events = 2 + len(
            result.philosophers
        )  # start + philosophers + completion
        assert len(session.events) == expected_events

        # Check event types
        assert session.events[0].data["message"] == "Ensemble reasoning started"
        assert session.events[-1].data["message"] == "Ensemble reasoning completed"

    def test_trace_records_metrics(self):
        """Test that trace records ensemble metrics."""
        from po_core.po_self import PoSelf

        po_self = PoSelf(enable_trace=True)
        result = po_self.generate("What is virtue?")

        session_id = result.log["session_id"]
        session = po_self.po_trace.get_session(session_id)

        # Check metrics were recorded
        assert "freedom_pressure" in session.metrics
        assert "semantic_delta" in session.metrics
        assert "blocked_tensor" in session.metrics
