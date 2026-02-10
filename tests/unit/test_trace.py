"""
Unit tests for Po_trace reasoning audit log system.

Tests cover:
- ReasoningTracer logging functionality
- TraceEntry creation and management
- PhilosophicalAnnotator concept matching
- JSON export for audit trails
"""

import json
from datetime import datetime

import pytest

from po_core.trace import (
    PhilosophicalAnnotator,
    ReasoningTracer,
    TraceEntry,
    TraceLevel,
)
from po_core.trace.annotator import PhilosophicalAnnotation


class TestTraceLevel:
    """Tests for TraceLevel enum."""

    def test_trace_level_values(self):
        """Test that TraceLevel has expected values."""
        assert TraceLevel.DEBUG.value == "debug"
        assert TraceLevel.INFO.value == "info"
        assert TraceLevel.REASONING.value == "reasoning"
        assert TraceLevel.DECISION.value == "decision"
        assert TraceLevel.BLOCKED.value == "blocked"
        assert TraceLevel.WARNING.value == "warning"
        assert TraceLevel.ERROR.value == "error"


class TestTraceEntry:
    """Tests for TraceEntry dataclass."""

    def test_trace_entry_creation(self):
        """Test creating a TraceEntry."""
        entry = TraceEntry(
            timestamp="2024-01-01T00:00:00Z",
            level=TraceLevel.REASONING,
            event="philosopher_reasoning",
            message="Testing reasoning",
            philosopher="sartre",
            data={"key": "value"},
        )

        assert entry.timestamp == "2024-01-01T00:00:00Z"
        assert entry.level == TraceLevel.REASONING
        assert entry.event == "philosopher_reasoning"
        assert entry.message == "Testing reasoning"
        assert entry.philosopher == "sartre"
        assert entry.data == {"key": "value"}

    def test_trace_entry_to_dict(self):
        """Test converting TraceEntry to dictionary."""
        entry = TraceEntry(
            timestamp="2024-01-01T00:00:00Z",
            level=TraceLevel.INFO,
            event="test_event",
            message="test message",
            philosopher="nietzsche",
            data={"test": "data"},
        )

        entry_dict = entry.to_dict()

        assert entry_dict["timestamp"] == "2024-01-01T00:00:00Z"
        assert entry_dict["level"] == "info"
        assert entry_dict["event"] == "test_event"
        assert entry_dict["message"] == "test message"
        assert entry_dict["philosopher"] == "nietzsche"
        assert entry_dict["data"] == {"test": "data"}


class TestReasoningTracer:
    """Tests for ReasoningTracer."""

    def test_tracer_initialization(self):
        """Test ReasoningTracer initialization."""
        tracer = ReasoningTracer()

        assert tracer.session_id is not None
        assert len(tracer.entries) == 0
        assert tracer.start_time is not None

    def test_tracer_with_custom_session_id(self):
        """Test tracer with custom session ID."""
        tracer = ReasoningTracer(session_id="custom-session-123")

        assert tracer.session_id == "custom-session-123"

    def test_log_event(self):
        """Test logging a basic event."""
        tracer = ReasoningTracer()

        tracer.log_event(
            level=TraceLevel.INFO,
            event="test_event",
            message="This is a test message",
        )

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.level == TraceLevel.INFO
        assert entry.event == "test_event"
        assert entry.message == "This is a test message"

    def test_log_event_with_philosopher(self):
        """Test logging event with philosopher."""
        tracer = ReasoningTracer()

        tracer.log_event(
            level=TraceLevel.REASONING,
            event="philosopher_reasoning",
            message="Sartre's reasoning",
            philosopher="sartre",
            data={"confidence": 0.9},
        )

        entry = tracer.entries[0]
        assert entry.philosopher == "sartre"
        assert entry.data["confidence"] == 0.9

    def test_log_philosopher_reasoning(self):
        """Test logging philosopher reasoning."""
        tracer = ReasoningTracer()

        tracer.log_philosopher_reasoning(
            philosopher="heidegger",
            prompt="What is Being?",
            response="Dasein is Being-in-the-world",
            confidence=0.85,
            reasoning="Fundamental ontology",
        )

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.philosopher == "heidegger"
        assert entry.level == TraceLevel.REASONING
        assert "response" in entry.data
        assert entry.data["confidence"] == 0.85

    def test_log_blocked_content(self):
        """Test logging blocked content."""
        tracer = ReasoningTracer()

        tracer.log_blocked_content(
            content="Harmful suggestion",
            reason="Potentially harmful",
            philosopher="sartre",
            alternative="Ethical alternative",
        )

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.level == TraceLevel.BLOCKED
        assert entry.event == "content_blocked"
        assert "reason" in entry.data

    def test_log_tensor_computation(self):
        """Test logging tensor computation."""
        tracer = ReasoningTracer()

        tracer.log_tensor_computation(
            tensor_name="FreedomPressure",
            tensor_data=[0.1, 0.2, 0.3],
            metadata={"foo": "bar"},
        )

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.event == "tensor_computation"
        assert "tensor_name" in entry.data
        assert entry.data["tensor_name"] == "FreedomPressure"

    def test_log_decision(self):
        """Test logging a decision point."""
        tracer = ReasoningTracer()

        tracer.log_decision(
            decision="Choose ethical path",
            reasoning="Aligns with values",
            confidence=0.9,
            alternatives=["Option A", "Option B"],
        )

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.level == TraceLevel.DECISION
        assert entry.event == "decision_point"
        assert "decision" in entry.data

    def test_log_synthesis(self):
        """Test logging synthesis."""
        tracer = ReasoningTracer()

        tracer.log_synthesis(
            perspectives=[
                {"philosopher": "sartre", "response": "Freedom"},
                {"philosopher": "nietzsche", "response": "Power"},
            ],
            synthesis="Unified response",
        )

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.event == "synthesis"
        assert "perspectives_count" in entry.data

    def test_log_error(self):
        """Test logging an error."""
        tracer = ReasoningTracer()

        tracer.log_error("Something went wrong", exception="ValueError")

        assert len(tracer.entries) == 1
        entry = tracer.entries[0]
        assert entry.level == TraceLevel.ERROR
        assert entry.event == "error"

    def test_get_entries_by_level(self):
        """Test filtering entries by level."""
        tracer = ReasoningTracer()

        tracer.log_event(TraceLevel.INFO, "event1", "Message 1")
        tracer.log_event(TraceLevel.REASONING, "event2", "Message 2")
        tracer.log_event(TraceLevel.INFO, "event3", "Message 3")
        tracer.log_event(TraceLevel.ERROR, "event4", "Message 4")

        info_entries = tracer.get_entries_by_level(TraceLevel.INFO)
        assert len(info_entries) == 2

        reasoning_entries = tracer.get_entries_by_level(TraceLevel.REASONING)
        assert len(reasoning_entries) == 1

    def test_get_entries_by_philosopher(self):
        """Test filtering entries by philosopher."""
        tracer = ReasoningTracer()

        tracer.log_philosopher_reasoning("sartre", "Q1", "A1", 0.9, "R1")
        tracer.log_philosopher_reasoning("nietzsche", "Q2", "A2", 0.8, "R2")
        tracer.log_philosopher_reasoning("sartre", "Q3", "A3", 0.85, "R3")

        sartre_entries = tracer.get_entries_by_philosopher("sartre")
        assert len(sartre_entries) == 2
        assert all(e.philosopher == "sartre" for e in sartre_entries)

    def test_get_entries_by_event(self):
        """Test filtering entries by event type."""
        tracer = ReasoningTracer()

        tracer.log_event(TraceLevel.INFO, "custom_event", "Message 1")
        tracer.log_event(TraceLevel.INFO, "other_event", "Message 2")
        tracer.log_event(TraceLevel.INFO, "custom_event", "Message 3")

        custom_entries = tracer.get_entries_by_event("custom_event")
        assert len(custom_entries) == 2

    def test_get_timeline_summary(self):
        """Test getting timeline summary."""
        tracer = ReasoningTracer()

        tracer.log_event(TraceLevel.INFO, "start", "Starting")
        tracer.log_philosopher_reasoning("sartre", "Q", "A", 0.9, "R")
        tracer.log_decision("Choice", "Reasoning", 0.8)

        summary = tracer.get_timeline_summary()

        assert summary["session_id"] == tracer.session_id
        assert summary["total_entries"] == 3
        assert "by_level" in summary
        assert "by_event" in summary
        assert "philosophers_involved" in summary

    def test_export_json(self):
        """Test exporting trace to JSON."""
        tracer = ReasoningTracer()

        tracer.log_event(TraceLevel.INFO, "test", "Test message")
        tracer.log_philosopher_reasoning("sartre", "Q", "A", 0.9, "R")

        json_str = tracer.export_json()
        data = json.loads(json_str)

        assert "session_id" in data
        assert "entries" in data
        assert len(data["entries"]) == 2
        assert data["metadata"]["total_entries"] == 2

    def test_export_json_indent(self):
        """Test exporting JSON with indentation."""
        tracer = ReasoningTracer()
        tracer.log_event(TraceLevel.INFO, "test", "message")

        json_str = tracer.export_json(indent=2)

        # Should be formatted with newlines
        assert "\n" in json_str

    def test_clear_trace(self):
        """Test clearing the trace."""
        tracer = ReasoningTracer()

        tracer.log_event(TraceLevel.INFO, "test", "message")
        assert len(tracer.entries) == 1

        tracer.clear()
        assert len(tracer.entries) == 0


class TestPhilosophicalAnnotator:
    """Tests for PhilosophicalAnnotator."""

    def test_annotator_initialization(self):
        """Test PhilosophicalAnnotator initialization."""
        annotator = PhilosophicalAnnotator()

        assert len(annotator.concept_library) > 0
        assert "freedom" in annotator.concept_library

    def test_concept_library_structure(self):
        """Test that concept library has expected structure."""
        annotator = PhilosophicalAnnotator()

        freedom_concept = annotator.concept_library["freedom"]
        assert "definition" in freedom_concept
        assert "philosophers" in freedom_concept
        assert "keywords" in freedom_concept
        assert isinstance(freedom_concept["philosophers"], list)

    def test_annotate_reasoning_basic(self):
        """Test basic reasoning annotation."""
        annotator = PhilosophicalAnnotator()

        reasoning = {
            "response": "We must take responsibility for our freedom and choices",
            "philosopher": "sartre",
        }

        annotations = annotator.annotate_reasoning(reasoning)

        assert len(annotations) > 0
        # Should find "freedom" concept
        concepts = [a.concept for a in annotations]
        assert "freedom" in concepts

    def test_annotate_reasoning_with_being(self):
        """Test annotation with Being-related concepts."""
        annotator = PhilosophicalAnnotator()

        reasoning = {"response": "Dasein's being is characterized by its existence"}

        annotations = annotator.annotate_reasoning(reasoning)

        # Should find being/dasein concepts
        concepts = [a.concept for a in annotations]
        assert any(c in ["being", "dasein"] for c in concepts)

    def test_annotate_reasoning_filters_by_philosopher(self):
        """Test that annotation filters by philosopher when provided."""
        annotator = PhilosophicalAnnotator()

        reasoning = {
            "response": "Freedom is radical responsibility",
            "philosopher": "sartre",
        }

        annotations = annotator.annotate_reasoning(reasoning)

        # All annotations should be relevant to Sartre
        for annotation in annotations:
            assert "sartre" in [p.lower() for p in annotation.associated_philosophers]

    def test_annotate_reasoning_no_matches(self):
        """Test annotation with text that has no philosophical keywords."""
        annotator = PhilosophicalAnnotator()

        reasoning = {"response": "The weather is nice today"}

        annotations = annotator.annotate_reasoning(reasoning)

        # May return empty or very few annotations
        assert isinstance(annotations, list)

    def test_find_concepts_in_text(self):
        """Test finding concepts in text."""
        annotator = PhilosophicalAnnotator()

        text = "Authentic existence requires confronting one's own freedom and being"

        concepts = annotator.find_concepts_in_text(text)

        assert len(concepts) > 0
        assert "freedom" in concepts or "authenticity" in concepts

    def test_find_concepts_multiple_matches(self):
        """Test finding multiple concepts."""
        annotator = PhilosophicalAnnotator()

        text = "The will to power drives the eternal return of the Übermensch"

        concepts = annotator.find_concepts_in_text(text)

        # Should find Nietzschean concepts
        assert len(concepts) > 0

    def test_get_concept_definition(self):
        """Test getting concept definition."""
        annotator = PhilosophicalAnnotator()

        definition = annotator.get_concept_definition("freedom")

        assert definition is not None
        assert isinstance(definition, str)
        assert len(definition) > 0

    def test_get_concept_definition_nonexistent(self):
        """Test getting definition for nonexistent concept."""
        annotator = PhilosophicalAnnotator()

        definition = annotator.get_concept_definition("nonexistent_concept_xyz")

        assert definition is None

    def test_get_philosopher_concepts(self):
        """Test getting concepts by philosopher."""
        annotator = PhilosophicalAnnotator()

        sartre_concepts = annotator.get_philosopher_concepts("sartre")

        assert len(sartre_concepts) > 0
        assert "freedom" in sartre_concepts

    def test_get_philosopher_concepts_case_insensitive(self):
        """Test that philosopher lookup is case-insensitive."""
        annotator = PhilosophicalAnnotator()

        concepts1 = annotator.get_philosopher_concepts("Sartre")
        concepts2 = annotator.get_philosopher_concepts("sartre")
        concepts3 = annotator.get_philosopher_concepts("SARTRE")

        assert concepts1 == concepts2 == concepts3

    def test_annotation_object_structure(self):
        """Test PhilosophicalAnnotation object structure."""
        annotation = PhilosophicalAnnotation(
            concept="freedom",
            definition="Radical responsibility",
            associated_philosophers=["Sartre", "Camus"],
            relevance_score=0.9,
            matched_keywords=["freedom", "choice"],
        )

        assert annotation.concept == "freedom"
        assert annotation.definition == "Radical responsibility"
        assert len(annotation.associated_philosophers) == 2
        assert annotation.relevance_score == 0.9
        assert len(annotation.matched_keywords) == 2

    def test_annotation_to_dict(self):
        """Test converting annotation to dictionary."""
        annotation = PhilosophicalAnnotation(
            concept="dasein",
            definition="Being-there",
            associated_philosophers=["Heidegger"],
            relevance_score=0.95,
            matched_keywords=["dasein", "being"],
        )

        ann_dict = annotation.to_dict()

        assert ann_dict["concept"] == "dasein"
        assert ann_dict["definition"] == "Being-there"
        assert "Heidegger" in ann_dict["associated_philosophers"]
        assert ann_dict["relevance_score"] == 0.95

    def test_annotate_multiple_perspectives(self):
        """Test annotating multiple philosopher perspectives."""
        annotator = PhilosophicalAnnotator()

        perspectives = [
            {"philosopher": "sartre", "response": "Freedom is responsibility"},
            {"philosopher": "nietzsche", "response": "Will to power"},
            {"philosopher": "heidegger", "response": "Being and Time"},
        ]

        all_annotations = []
        for perspective in perspectives:
            annotations = annotator.annotate_reasoning(perspective)
            all_annotations.extend(annotations)

        # Should have found concepts from all perspectives
        assert len(all_annotations) > 0


class TestTraceIntegration:
    """Integration tests for trace components working together."""

    def test_tracer_with_annotator(self):
        """Test using tracer and annotator together."""
        tracer = ReasoningTracer()
        annotator = PhilosophicalAnnotator()

        # Log philosopher reasoning
        response = "Freedom requires authentic choice and responsibility"
        tracer.log_philosopher_reasoning(
            philosopher="sartre",
            prompt="What is freedom?",
            response=response,
            confidence=0.9,
            reasoning="Existentialist perspective",
        )

        # Annotate the reasoning
        reasoning_dict = {"response": response, "philosopher": "sartre"}
        annotations = annotator.annotate_reasoning(reasoning_dict)

        # Log the annotations
        for annotation in annotations:
            tracer.log_event(
                level=TraceLevel.INFO,
                event="philosophical_annotation",
                message=f"Concept: {annotation.concept}",
                data=annotation.to_dict(),
            )

        # Should have reasoning + annotation entries
        assert len(tracer.entries) > 1

    def test_complete_reasoning_trace(self):
        """Test a complete reasoning trace workflow."""
        tracer = ReasoningTracer()
        annotator = PhilosophicalAnnotator()

        # 1. Start reasoning
        tracer.log_event(TraceLevel.INFO, "reasoning_start", "Starting reasoning")

        # 2. Log philosopher perspectives
        tracer.log_philosopher_reasoning(
            "sartre",
            "What is authenticity?",
            "Living in good faith",
            0.9,
            "Existentialism",
        )

        tracer.log_philosopher_reasoning(
            "heidegger",
            "What is authenticity?",
            "Being true to Dasein",
            0.85,
            "Phenomenology",
        )

        # 3. Log blocked content
        tracer.log_blocked_content(
            "Inauthentic answer", "Does not address the question", "sartre"
        )

        # 4. Log decision
        tracer.log_decision("Synthesize perspectives", "Both contribute", 0.95)

        # 5. Log synthesis
        tracer.log_synthesis(
            perspectives=[{"philosopher": "sartre"}, {"philosopher": "heidegger"}],
            synthesis="Combined authentic response",
        )

        # Export and verify
        timeline = tracer.get_timeline_summary()
        assert timeline["total_entries"] == 5
        assert len(timeline["philosophers_involved"]) == 2

        json_export = tracer.export_json()
        assert json_export is not None
