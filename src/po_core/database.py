"""
Po_core Database Layer
======================

SQLAlchemy-based database layer for Po_trace
Supports SQLite (default) and PostgreSQL
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session as DBSession

Base = declarative_base()


class SessionModel(Base):
    """Database model for reasoning sessions."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), unique=True, nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    philosophers = Column(JSON, nullable=False)  # List of philosopher names
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)

    # Relationships
    events = relationship("EventModel", back_populates="session", cascade="all, delete-orphan")
    metrics = relationship("MetricModel", back_populates="session", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "session_id": self.session_id,
            "prompt": self.prompt,
            "philosophers": self.philosophers,
            "created_at": self.created_at.isoformat() + "Z",
            "events": [event.to_dict() for event in self.events],
            "metrics": {metric.key: metric.value for metric in self.metrics},
            "metadata": self.metadata or {},
        }


class EventModel(Base):
    """Database model for session events."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(36), unique=True, nullable=False, index=True)
    session_id = Column(String(36), ForeignKey("sessions.session_id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    event_type = Column(String(50), nullable=False, index=True)
    source = Column(String(100), nullable=False)
    data = Column(JSON, nullable=False)
    metadata = Column(JSON, default=dict)

    # Relationships
    session = relationship("SessionModel", back_populates="events")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "event_id": self.event_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat() + "Z",
            "event_type": self.event_type,
            "source": self.source,
            "data": self.data,
            "metadata": self.metadata or {},
        }


class MetricModel(Base):
    """Database model for session metrics."""

    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey("sessions.session_id"), nullable=False, index=True)
    key = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)

    # Relationships
    session = relationship("SessionModel", back_populates="metrics")


class DatabaseManager:
    """Database manager for Po_trace."""

    def __init__(self, db_url: Optional[str] = None):
        """
        Initialize database manager.

        Args:
            db_url: Database URL (default: SQLite in user home)
        """
        if db_url is None:
            from pathlib import Path

            db_path = Path.home() / ".po_core" / "po_trace.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            db_url = f"sqlite:///{db_path}"

        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Create tables
        Base.metadata.create_all(self.engine)

    def get_session(self) -> DBSession:
        """Get a new database session."""
        return self.SessionLocal()

    def create_session(
        self,
        session_id: str,
        prompt: str,
        philosophers: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SessionModel:
        """
        Create a new reasoning session.

        Args:
            session_id: Unique session identifier
            prompt: The prompt for this session
            philosophers: List of philosopher names
            metadata: Optional metadata

        Returns:
            SessionModel instance
        """
        with self.get_session() as db:
            session = SessionModel(
                session_id=session_id,
                prompt=prompt,
                philosophers=philosophers,
                created_at=datetime.utcnow(),
                metadata=metadata or {},
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session

    def add_event(
        self,
        event_id: str,
        session_id: str,
        event_type: str,
        source: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EventModel:
        """
        Add an event to a session.

        Args:
            event_id: Unique event identifier
            session_id: Session identifier
            event_type: Type of event
            source: Source module/component
            data: Event data
            metadata: Optional event metadata

        Returns:
            EventModel instance
        """
        with self.get_session() as db:
            event = EventModel(
                event_id=event_id,
                session_id=session_id,
                timestamp=datetime.utcnow(),
                event_type=event_type,
                source=source,
                data=data,
                metadata=metadata or {},
            )
            db.add(event)
            db.commit()
            db.refresh(event)
            return event

    def update_metrics(self, session_id: str, metrics: Dict[str, float]) -> None:
        """
        Update session metrics.

        Args:
            session_id: Session identifier
            metrics: Metrics to update
        """
        with self.get_session() as db:
            # Delete existing metrics
            db.query(MetricModel).filter(MetricModel.session_id == session_id).delete()

            # Add new metrics
            for key, value in metrics.items():
                metric = MetricModel(session_id=session_id, key=key, value=value)
                db.add(metric)

            db.commit()

    def get_session_by_id(self, session_id: str) -> Optional[SessionModel]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            SessionModel instance or None if not found
        """
        with self.get_session() as db:
            session = (
                db.query(SessionModel)
                .filter(SessionModel.session_id == session_id)
                .first()
            )
            if session:
                # Eager load relationships
                db.refresh(session)
                _ = session.events  # Trigger lazy load
                _ = session.metrics  # Trigger lazy load
            return session

    def list_sessions(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all sessions.

        Args:
            limit: Optional limit on number of sessions to return
            offset: Offset for pagination

        Returns:
            List of session metadata
        """
        with self.get_session() as db:
            query = db.query(SessionModel).order_by(SessionModel.created_at.desc())

            if limit:
                query = query.limit(limit)

            if offset:
                query = query.offset(offset)

            sessions = query.all()

            return [
                {
                    "session_id": s.session_id,
                    "prompt": s.prompt[:100],  # Truncate for listing
                    "created_at": s.created_at.isoformat() + "Z",
                    "philosophers_count": len(s.philosophers),
                }
                for s in sessions
            ]

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
        with self.get_session() as db:
            q = db.query(SessionModel)

            if query:
                q = q.filter(SessionModel.prompt.contains(query))

            if philosopher:
                # Search in JSON array
                q = q.filter(SessionModel.philosophers.contains(philosopher))

            q = q.order_by(SessionModel.created_at.desc())

            if limit:
                q = q.limit(limit)

            sessions = q.all()

            return [
                {
                    "session_id": s.session_id,
                    "prompt": s.prompt[:100],
                    "created_at": s.created_at.isoformat() + "Z",
                    "philosophers_count": len(s.philosophers),
                }
                for s in sessions
            ]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Statistics dictionary
        """
        with self.get_session() as db:
            total_sessions = db.query(SessionModel).count()
            total_events = db.query(EventModel).count()

            # Get philosopher usage
            philosopher_counts: Dict[str, int] = {}
            sessions = db.query(SessionModel).all()
            for session in sessions:
                for phil in session.philosophers:
                    philosopher_counts[phil] = philosopher_counts.get(phil, 0) + 1

            return {
                "total_sessions": total_sessions,
                "total_events": total_events,
                "philosopher_usage": philosopher_counts,
            }

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and all associated data.

        Args:
            session_id: Session identifier

        Returns:
            True if deleted, False if not found
        """
        with self.get_session() as db:
            session = (
                db.query(SessionModel)
                .filter(SessionModel.session_id == session_id)
                .first()
            )
            if session:
                db.delete(session)
                db.commit()
                return True
            return False
