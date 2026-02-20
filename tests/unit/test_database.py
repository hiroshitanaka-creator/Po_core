"""
Tests for database layer (database.py)
"""

import tempfile
from pathlib import Path

from po_core.database import DatabaseManager


class TestDatabaseManager:
    """Test DatabaseManager functionality."""

    def test_database_initialization(self):
        """Test database initialization with SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            assert db.engine is not None
            assert db.SessionLocal is not None

    def test_create_session(self):
        """Test creating a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            session = db.create_session(
                session_id="test-123",
                prompt="What is consciousness?",
                philosophers=["Socrates", "Kant"],
                metadata={"test": True},
            )

            assert session.session_id == "test-123"
            assert session.prompt == "What is consciousness?"
            assert len(session.philosophers) == 2
            assert session.meta_data["test"] is True

    def test_add_event(self):
        """Test adding an event to a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create session first
            db.create_session(
                session_id="test-123",
                prompt="Test prompt",
                philosophers=["Socrates"],
            )

            # Add event
            event = db.add_event(
                event_id="event-456",
                session_id="test-123",
                event_type="execution",
                source="po_self",
                data={"message": "Testing"},
                metadata={"priority": "high"},
            )

            assert event.event_id == "event-456"
            assert event.session_id == "test-123"
            assert event.event_type == "execution"
            assert event.data["message"] == "Testing"

    def test_update_metrics(self):
        """Test updating session metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create session
            db.create_session(
                session_id="test-123",
                prompt="Test prompt",
                philosophers=["Socrates"],
            )

            # Update metrics
            db.update_metrics(
                "test-123",
                {
                    "semantic_delta": 0.85,
                    "freedom_pressure": 0.72,
                    "blocked_tensor": 0.23,
                },
            )

            # Retrieve and verify
            retrieved = db.get_session_by_id("test-123")
            assert len(retrieved.metrics) == 3
            metric_dict = {m.key: m.value for m in retrieved.metrics}
            assert metric_dict["semantic_delta"] == 0.85

    def test_get_session_by_id(self):
        """Test retrieving a session by ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create session
            db.create_session(
                session_id="test-123",
                prompt="Test prompt",
                philosophers=["Socrates", "Kant"],
            )

            # Retrieve
            session = db.get_session_by_id("test-123")
            assert session is not None
            assert session.session_id == "test-123"
            assert len(session.philosophers) == 2

    def test_get_session_not_found(self):
        """Test retrieving a non-existent session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            session = db.get_session_by_id("nonexistent")
            assert session is None

    def test_list_sessions(self):
        """Test listing sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create multiple sessions
            for i in range(5):
                db.create_session(
                    session_id=f"test-{i}",
                    prompt=f"Prompt {i}",
                    philosophers=["Socrates"],
                )

            # List all
            sessions = db.list_sessions()
            assert len(sessions) == 5

            # List with limit
            sessions = db.list_sessions(limit=3)
            assert len(sessions) == 3

    def test_search_sessions_by_query(self):
        """Test searching sessions by query."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create sessions with different prompts
            db.create_session(
                session_id="test-1",
                prompt="What is consciousness?",
                philosophers=["Socrates"],
            )
            db.create_session(
                session_id="test-2",
                prompt="What is ethics?",
                philosophers=["Kant"],
            )

            # Search for "consciousness"
            results = db.search_sessions(query="consciousness")
            assert len(results) == 1
            assert results[0]["session_id"] == "test-1"

    def test_get_statistics(self):
        """Test getting database statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create sessions and events
            db.create_session(
                session_id="test-1",
                prompt="Test 1",
                philosophers=["Socrates", "Kant"],
            )
            db.create_session(
                session_id="test-2",
                prompt="Test 2",
                philosophers=["Socrates"],
            )
            db.add_event(
                event_id="event-1",
                session_id="test-1",
                event_type="execution",
                source="test",
                data={},
            )

            # Get statistics
            stats = db.get_statistics()
            assert stats["total_sessions"] == 2
            assert stats["total_events"] == 1
            assert "Socrates" in stats["philosopher_usage"]
            assert stats["philosopher_usage"]["Socrates"] == 2

    def test_delete_session(self):
        """Test deleting a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            # Create session
            db.create_session(
                session_id="test-123",
                prompt="Test prompt",
                philosophers=["Socrates"],
            )

            # Delete
            deleted = db.delete_session("test-123")
            assert deleted is True

            # Verify deletion
            session = db.get_session_by_id("test-123")
            assert session is None

    def test_delete_session_not_found(self):
        """Test deleting a non-existent session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            db = DatabaseManager(db_url)

            deleted = db.delete_session("nonexistent")
            assert deleted is False


class TestPoTraceDB:
    """Test PoTraceDB wrapper."""

    def test_po_trace_db_initialization(self):
        """Test PoTraceDB initialization."""
        from po_core.po_trace_db import PoTraceDB

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            trace = PoTraceDB(db_url)

            assert trace.db is not None

    def test_create_and_retrieve_session(self):
        """Test creating and retrieving a session through PoTraceDB."""
        from po_core.po_trace_db import PoTraceDB

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            trace = PoTraceDB(db_url)

            # Create session
            session_id = trace.create_session(
                prompt="What is life?",
                philosophers=["Socrates", "Nietzsche"],
                metadata={"test": True},
            )

            # Retrieve
            session = trace.get_session(session_id)
            assert session is not None
            assert session.session_id == session_id
            assert session.prompt == "What is life?"
            assert len(session.philosophers) == 2

    def test_log_event(self):
        """Test logging an event."""
        from po_core.po_trace import EventType
        from po_core.po_trace_db import PoTraceDB

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db_url = f"sqlite:///{db_path}"
            trace = PoTraceDB(db_url)

            # Create session
            session_id = trace.create_session(
                prompt="Test",
                philosophers=["Socrates"],
            )

            # Log event
            event_id = trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source="test",
                data={"message": "Test event"},
            )

            # Retrieve and verify
            session = trace.get_session(session_id)
            assert len(session.events) == 1
            assert session.events[0].event_id == event_id
