"""
Tests for Phase 3 explanation extensions.

- build_explanation_from_verdict (SafetyVerdict → ExplanationChain)
- WethicsGate.check_with_explanation()
- WethicsGateExplained TraceEvent schema
"""

import pytest

from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.trace_event import TraceEvent
from po_core.safety.wethics_gate.explanation import (
    ExplanationChain,
    build_explanation_from_verdict,
)
from po_core.safety.wethics_gate.gate import WethicsGate
from po_core.safety.wethics_gate.types import Candidate, GateDecision
from po_core.trace.decision_events import emit_wethics_gate_explained
from po_core.trace.in_memory import InMemoryTracer
from po_core.trace.schema import validate_event

pytestmark = [pytest.mark.unit, pytest.mark.observability]


class TestBuildExplanationFromVerdict:
    """build_explanation_from_verdict converts SafetyVerdict to ExplanationChain."""

    def test_allow_verdict(self):
        v = SafetyVerdict(decision=Decision.ALLOW)
        chain = build_explanation_from_verdict(v)

        assert chain.decision == "allow"
        assert chain.violations == []
        assert "passed" in chain.summary.lower()

    def test_reject_verdict(self):
        v = SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=["W0_viability", "W1_capture"],
            reasons=["Viability harm detected", "Domination pattern found"],
        )
        chain = build_explanation_from_verdict(v)

        assert chain.decision == "reject"
        assert len(chain.violations) == 2
        assert "rejected" in chain.summary.lower()
        assert chain.violations[0].severity == 1.0

    def test_revise_verdict(self):
        v = SafetyVerdict(
            decision=Decision.REVISE,
            rule_ids=["W3_dependency"],
            reasons=["Lock-in pattern"],
            required_changes=["Add opt-out mechanism"],
        )
        chain = build_explanation_from_verdict(v)

        assert chain.decision == "revise"
        assert len(chain.violations) == 1
        assert chain.violations[0].repairable is True
        assert "revision" in chain.summary.lower()

    def test_to_dict_roundtrip(self):
        v = SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=["W0_test"],
            reasons=["test reason"],
        )
        chain = build_explanation_from_verdict(v)
        d = chain.to_dict()

        assert d["decision"] == "reject"
        assert len(d["violations"]) == 1
        assert d["summary"]

    def test_to_markdown_output(self):
        v = SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=["W2_dignity"],
            reasons=["Dignity issue"],
        )
        chain = build_explanation_from_verdict(v)
        md = chain.to_markdown()

        assert "W_Ethics Gate Decision" in md
        assert "reject" in md


class TestCheckWithExplanation:
    """WethicsGate.check_with_explanation() attaches ExplanationChain."""

    def test_allow_has_chain(self):
        gate = WethicsGate()
        candidate = Candidate(cid="c1", text="Hello world")
        result = gate.check_with_explanation(candidate)

        assert result.explanation_chain is not None
        assert isinstance(result.explanation_chain, ExplanationChain)
        assert result.explanation_chain.decision == "allow"

    def test_reject_has_chain_with_violations(self):
        gate = WethicsGate()
        candidate = Candidate(
            cid="c2",
            text="We will brainwash users and lock them in with no escape",
        )
        result = gate.check_with_explanation(candidate)

        assert result.explanation_chain is not None
        chain = result.explanation_chain
        # The chain should reflect the gate decision
        assert chain.decision == result.decision.value


class TestWethicsGateExplainedEvent:
    """emit_wethics_gate_explained emits valid TraceEvent."""

    @staticmethod
    def _make_ctx(rid: str = "req-x"):
        from datetime import datetime, timezone

        from po_core.domain.context import Context

        return Context(
            request_id=rid,
            created_at=datetime.now(timezone.utc),
            user_input="test",
        )

    def test_event_emitted(self):
        tracer = InMemoryTracer()
        ctx = self._make_ctx("req-x")
        v = SafetyVerdict(decision=Decision.ALLOW)
        chain = build_explanation_from_verdict(v)

        emit_wethics_gate_explained(tracer, ctx, explanation_chain=chain)

        assert len(tracer.events) == 1
        ev = tracer.events[0]
        assert ev.event_type == "WethicsGateExplained"
        assert ev.payload["decision"] == "allow"
        assert "summary" in ev.payload
        assert "n_violations" in ev.payload

    def test_event_passes_schema(self):
        tracer = InMemoryTracer()
        ctx = self._make_ctx("req-y")
        v = SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=["W0_harm"],
            reasons=["harm"],
        )
        chain = build_explanation_from_verdict(v)
        emit_wethics_gate_explained(tracer, ctx, explanation_chain=chain)

        ev = tracer.events[0]
        issues = validate_event(ev)
        assert issues == [], f"Schema validation failed: {issues}"
