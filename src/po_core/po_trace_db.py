"""
Po_trace with Database Backend
================================

Database-enabled version of Po_trace using SQLAlchemy
Compatible with existing Po_trace API
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from po_core.database import DatabaseManager
from po_core.po_trace import Event, EventType, Session


class PoTraceDB:
    """Po_trace with database backend."""

    def __init__(self, db_url: Optional[str] = None):
        """
        Initialize Po_trace with database backend.

        Args:
            db_url: Database URL (default: SQLite in user home)
        """
        self.db = DatabaseManager(db_url)

    def create_session(
        self,
        prompt: str,
        philosophers: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a new reasoning session.

        Args:
            prompt: The prompt for this session
            philosophers: List of philosopher names
            metadata: Optional metadata

        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())

        self.db.create_session(
            session_id=session_id,
            prompt=prompt,
            philosophers=philosophers,
            metadata=metadata,
        )

        return session_id

    def log_event(
        self,
        session_id: str,
        event_type: EventType,
        source: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log an event to a session.

        Args:
            session_id: Session identifier
            event_type: Type of event
            source: Source module/component
            data: Event data
            metadata: Optional event metadata

        Returns:
            event_id: Unique event identifier
        """
        event_id = str(uuid.uuid4())

        self.db.add_event(
            event_id=event_id,
            session_id=session_id,
            event_type=event_type.value,
            source=source,
            data=data,
            metadata=metadata,
        )

        return event_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session object or None if not found
        """
        db_session = self.db.get_session_by_id(session_id)
        if db_session is None:
            return None

        # Convert database model to dataclass
        events = [
            Event(
                event_id=e.event_id,
                session_id=e.session_id,
                timestamp=e.timestamp.isoformat() + "Z",
                event_type=EventType(e.event_type),
                source=e.source,
                data=e.data,
                metadata=e.meta_data or {},
            )
            for e in db_session.events
        ]

        metrics = {m.key: m.value for m in db_session.metrics}

        return Session(
            session_id=db_session.session_id,
            prompt=db_session.prompt,
            philosophers=db_session.philosophers,
            created_at=db_session.created_at.isoformat() + "Z",
            events=events,
            metrics=metrics,
            metadata=db_session.meta_data or {},
        )

    def list_sessions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all sessions.

        Args:
            limit: Optional limit on number of sessions to return

        Returns:
            List of session metadata
        """
        return self.db.list_sessions(limit=limit)

    def update_metrics(self, session_id: str, metrics: Dict[str, float]) -> None:
        """
        Update session metrics.

        Args:
            session_id: Session identifier
            metrics: Metrics to update
        """
        self.db.update_metrics(session_id, metrics)

    def export_session(self, session_id: str, format: str = "json") -> str:
        """
        Export a session to a specific format.

        Args:
            session_id: Session identifier
            format: Export format ('json' or 'text')

        Returns:
            Exported content as string
        """
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        if format == "json":
            import json

            return json.dumps(session.to_dict(), indent=2, ensure_ascii=False)
        elif format == "text":
            lines = []
            lines.append(f"Session: {session.session_id}")
            lines.append(f"Created: {session.created_at}")
            lines.append(f"Prompt: {session.prompt}")
            lines.append(f"Philosophers: {', '.join(session.philosophers)}")
            lines.append(f"\nMetrics:")
            for key, value in session.metrics.items():
                lines.append(f"  {key}: {value}")
            lines.append(f"\nEvents ({len(session.events)}):")
            for event in session.events:
                lines.append(
                    f"  [{event.timestamp}] {event.event_type.value} - {event.source}"
                )
                if "message" in event.data:
                    lines.append(f"    {event.data['message']}")
            return "\n".join(lines)
        else:
            raise ValueError(f"Unknown format: {format}")

    def search_sessions(
        self,
        query: Optional[str] = None,
        philosopher: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search sessions by query or philosopher.

        Args:
            query: Search query for prompt
            philosopher: Filter by philosopher name
            limit: Optional limit on number of sessions to return

        Returns:
            List of session metadata
        """
        return self.db.search_sessions(
            query=query, philosopher=philosopher, limit=limit
        )

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Statistics dictionary
        """
        return self.db.get_statistics()

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and all associated data.

        Args:
            session_id: Session identifier

        Returns:
            True if deleted, False if not found
        """
        return self.db.delete_session(session_id)
