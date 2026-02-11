"""
Tests for Po_trace Database Backend

Comprehensive tests for the database-enabled Po_trace system.
"""

import json
import os
import tempfile

import pytest

from po_core.po_trace import EventType
from po_core.po_trace_db import PoTraceDB

pytestmark = pytest.mark.skip(reason="Legacy PoTraceDB session API — replaced by InMemoryTracer — to be migrated in Phase 1")



class TestPoTraceDBBasicFunctionality:
    """Test basic Po_trace DB functionality."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db_url = f"sqlite:///{path}"
        yield db_url
        # Cleanup
        try:
            os.unlink(path)
        except:
            pass

    def test_potrace_db_initialization(self, temp_db):
        """Test that PoTraceDB initializes correctly."""
        trace_db = PoTraceDB(db_url=temp_db)
        assert trace_db is not None
        assert trace_db.db is not None

    def test_potrace_db_create_session(self, temp_db):
        """Test creating a session."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session(
            prompt="What is truth?",
            philosophers=["aristotle", "nietzsche"],
        )

        assert session_id is not None
        assert isinstance(session_id, str)
        assert len(session_id) > 0

    def test_potrace_db_log_event(self, temp_db):
        """Test logging an event."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session(
            prompt="What is freedom?",
            philosophers=["sartre", "heidegger"],
        )

        event_id = trace_db.log_event(
            session_id=session_id,
            event_type=EventType.PHILOSOPHER_REASONING,
            source="sartre",
            data={"reasoning": "Freedom is responsibility"},
        )

        assert event_id is not None
        assert isinstance(event_id, str)

    def test_potrace_db_get_session(self, temp_db):
        """Test retrieving a session."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create session
        session_id = trace_db.create_session(
            prompt="What is knowledge?",
            philosophers=["wittgenstein", "dewey"],
        )

        # Retrieve session
        session = trace_db.get_session(session_id)

        assert session is not None
        assert session.session_id == session_id
        assert session.prompt == "What is knowledge?"
        assert set(session.philosophers) == {"wittgenstein", "dewey"}

    def test_potrace_db_get_nonexistent_session(self, temp_db):
        """Test retrieving a non-existent session returns None."""
        trace_db = PoTraceDB(db_url=temp_db)

        session = trace_db.get_session("nonexistent-id")

        assert session is None


class TestPoTraceDBSessionManagement:
    """Test session management features."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db_url = f"sqlite:///{path}"
        yield db_url
        try:
            os.unlink(path)
        except:
            pass

    def test_list_sessions(self, temp_db):
        """Test listing all sessions."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create multiple sessions
        session_id1 = trace_db.create_session("Prompt 1", ["aristotle"])
        session_id2 = trace_db.create_session("Prompt 2", ["nietzsche"])

        # List sessions
        sessions = trace_db.list_sessions()

        assert len(sessions) >= 2
        session_ids = [s["session_id"] for s in sessions]
        assert session_id1 in session_ids
        assert session_id2 in session_ids

    def test_list_sessions_with_limit(self, temp_db):
        """Test listing sessions with limit."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create multiple sessions
        for i in range(5):
            trace_db.create_session(f"Prompt {i}", ["aristotle"])

        # List with limit
        sessions = trace_db.list_sessions(limit=3)

        assert len(sessions) == 3

    def test_update_metrics(self, temp_db):
        """Test updating session metrics."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session("Test prompt", ["aristotle"])

        # Update metrics
        metrics = {
            "freedom_pressure": 0.85,
            "semantic_delta": 0.72,
            "blocked_tensor": 0.45,
        }
        trace_db.update_metrics(session_id, metrics)

        # Retrieve and verify
        session = trace_db.get_session(session_id)
        assert session.metrics == metrics

    def test_delete_session(self, temp_db):
        """Test deleting a session."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session("Test prompt", ["aristotle"])

        # Delete session
        result = trace_db.delete_session(session_id)
        assert result is True

        # Verify deletion
        session = trace_db.get_session(session_id)
        assert session is None

    def test_delete_nonexistent_session(self, temp_db):
        """Test deleting a non-existent session."""
        trace_db = PoTraceDB(db_url=temp_db)

        result = trace_db.delete_session("nonexistent-id")
        assert result is False


class TestPoTraceDBSearch:
    """Test search functionality."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db_url = f"sqlite:///{path}"
        yield db_url
        try:
            os.unlink(path)
        except:
            pass

    def test_search_sessions_by_query(self, temp_db):
        """Test searching sessions by query string."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create sessions with different prompts
        trace_db.create_session("What is truth?", ["aristotle"])
        trace_db.create_session("What is beauty?", ["nietzsche"])
        trace_db.create_session("What is truth in art?", ["dewey"])

        # Search for "truth"
        results = trace_db.search_sessions(query="truth")

        assert len(results) >= 2
        prompts = [r["prompt"] for r in results]
        assert any("truth" in p.lower() for p in prompts)

    def test_search_sessions_by_philosopher(self, temp_db):
        """Test searching sessions by philosopher."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create sessions with different philosophers
        trace_db.create_session("Prompt 1", ["aristotle", "nietzsche"])
        trace_db.create_session("Prompt 2", ["sartre"])
        trace_db.create_session("Prompt 3", ["aristotle"])

        # Search for aristotle
        results = trace_db.search_sessions(philosopher="aristotle")

        assert len(results) >= 2
        for result in results:
            assert "aristotle" in result["philosophers"]

    def test_search_sessions_with_limit(self, temp_db):
        """Test search with limit."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create multiple sessions
        for i in range(5):
            trace_db.create_session(f"Truth prompt {i}", ["aristotle"])

        # Search with limit
        results = trace_db.search_sessions(query="Truth", limit=3)

        assert len(results) == 3


class TestPoTraceDBExport:
    """Test export functionality."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db_url = f"sqlite:///{path}"
        yield db_url
        try:
            os.unlink(path)
        except:
            pass

    def test_export_session_json(self, temp_db):
        """Test exporting session as JSON."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session(
            "What is wisdom?",
            ["aristotle", "confucius"],
        )

        # Export as JSON
        json_export = trace_db.export_session(session_id, format="json")

        assert json_export is not None
        assert isinstance(json_export, str)

        # Verify it's valid JSON
        data = json.loads(json_export)
        assert data["prompt"] == "What is wisdom?"
        assert set(data["philosophers"]) == {"aristotle", "confucius"}

    def test_export_session_text(self, temp_db):
        """Test exporting session as text."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session(
            "What is courage?",
            ["aristotle"],
        )

        # Export as text
        text_export = trace_db.export_session(session_id, format="text")

        assert text_export is not None
        assert isinstance(text_export, str)
        assert "What is courage?" in text_export
        assert "aristotle" in text_export

    def test_export_nonexistent_session_raises_error(self, temp_db):
        """Test that exporting non-existent session raises error."""
        trace_db = PoTraceDB(db_url=temp_db)

        with pytest.raises(ValueError):
            trace_db.export_session("nonexistent-id")

    def test_export_invalid_format_raises_error(self, temp_db):
        """Test that invalid export format raises error."""
        trace_db = PoTraceDB(db_url=temp_db)

        session_id = trace_db.create_session("Test", ["aristotle"])

        with pytest.raises(ValueError):
            trace_db.export_session(session_id, format="invalid")


class TestPoTraceDBStatistics:
    """Test statistics functionality."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db_url = f"sqlite:///{path}"
        yield db_url
        try:
            os.unlink(path)
        except:
            pass

    def test_get_statistics(self, temp_db):
        """Test getting database statistics."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create some sessions
        trace_db.create_session("Prompt 1", ["aristotle"])
        trace_db.create_session("Prompt 2", ["nietzsche", "sartre"])

        # Get statistics
        stats = trace_db.get_statistics()

        assert stats is not None
        assert isinstance(stats, dict)
        assert "total_sessions" in stats
        assert stats["total_sessions"] >= 2

    def test_statistics_philosopher_usage(self, temp_db):
        """Test that statistics track philosopher usage."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create sessions with different philosophers
        trace_db.create_session("Prompt 1", ["aristotle"])
        trace_db.create_session("Prompt 2", ["aristotle", "nietzsche"])
        trace_db.create_session("Prompt 3", ["sartre"])

        # Get statistics
        stats = trace_db.get_statistics()

        assert "philosopher_usage" in stats
        philosopher_usage = stats["philosopher_usage"]

        # Aristotle should appear twice
        assert philosopher_usage.get("aristotle", 0) == 2
        # Sartre should appear once
        assert philosopher_usage.get("sartre", 0) == 1


class TestPoTraceDBIntegration:
    """Test integration scenarios."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db_url = f"sqlite:///{path}"
        yield db_url
        try:
            os.unlink(path)
        except:
            pass

    def test_complete_reasoning_session(self, temp_db):
        """Test a complete reasoning session workflow."""
        trace_db = PoTraceDB(db_url=temp_db)

        # 1. Create session
        session_id = trace_db.create_session(
            prompt="What is the meaning of life?",
            philosophers=["aristotle", "nietzsche", "sartre"],
        )

        # 2. Log events for each philosopher
        trace_db.log_event(
            session_id=session_id,
            event_type=EventType.ENSEMBLE_STARTED,
            source="po_self",
            data={"message": "Starting ensemble reasoning"},
        )

        for phil in ["aristotle", "nietzsche", "sartre"]:
            trace_db.log_event(
                session_id=session_id,
                event_type=EventType.PHILOSOPHER_REASONING,
                source=phil,
                data={"reasoning": f"{phil}'s perspective on meaning"},
            )

        # 3. Update metrics
        metrics = {
            "freedom_pressure": 0.87,
            "semantic_delta": 0.79,
            "blocked_tensor": 0.42,
        }
        trace_db.update_metrics(session_id, metrics)

        # 4. Retrieve and verify complete session
        session = trace_db.get_session(session_id)

        assert session is not None
        assert session.prompt == "What is the meaning of life?"
        assert len(session.philosophers) == 3
        assert len(session.events) == 4  # 1 start + 3 philosopher events
        assert session.metrics == metrics

    def test_multiple_sessions_isolation(self, temp_db):
        """Test that multiple sessions are properly isolated."""
        trace_db = PoTraceDB(db_url=temp_db)

        # Create two separate sessions
        session_id1 = trace_db.create_session("Question 1", ["aristotle"])
        session_id2 = trace_db.create_session("Question 2", ["nietzsche"])

        # Log events to different sessions
        trace_db.log_event(
            session_id=session_id1,
            event_type=EventType.PHILOSOPHER_REASONING,
            source="aristotle",
            data={"test": "data1"},
        )

        trace_db.log_event(
            session_id=session_id2,
            event_type=EventType.PHILOSOPHER_REASONING,
            source="nietzsche",
            data={"test": "data2"},
        )

        # Verify isolation
        session1 = trace_db.get_session(session_id1)
        session2 = trace_db.get_session(session_id2)

        assert session1.prompt == "Question 1"
        assert session2.prompt == "Question 2"
        assert len(session1.events) == 1
        assert len(session2.events) == 1
        assert session1.events[0].data["test"] == "data1"
        assert session2.events[0].data["test"] == "data2"
