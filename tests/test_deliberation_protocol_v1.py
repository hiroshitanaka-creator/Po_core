from __future__ import annotations

from datetime import datetime, timezone

from po_core.deliberation.protocol import CritiqueCard, run_deliberation
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode
from po_core.domain.safety_verdict import SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ensemble import EnsembleDeps, _PhasePreResult, _run_phase_post


class DummyPhilosopher:
    def __init__(self, name: str, content: str, confidence: float, stance: str):
        self.name = name
        self._content = content
        self._confidence = confidence
        self._stance = stance

    def propose_card(self, _input, _axis_spec, _settings):
        return {
            "philosopher": self.name,
            "proposal_id": f"{self.name}:0",
            "stance": self._stance,
            "claims": [self._content],
            "confidence": self._confidence,
        }

    def critique_card(self, target, _axis_spec):
        return CritiqueCard(
            critic=self.name,
            target=target.philosopher,
            target_proposal_id=target.proposal_id,
            weakness="counterexample_gap",
            detail=f"{target.philosopher}は反例条件が不足しています。",
            question="反例が成立する境界条件はどこですか？",
        )


class MinimalPhilosopher:
    def __init__(self, name: str):
        self.name = name

    def propose(self, *_args, **_kwargs):
        return [
            Proposal(
                proposal_id=f"{self.name}:0",
                action_type="answer",
                content="We support this path but do not list risk.",
                confidence=0.55,
                extra={PO_CORE: {AUTHOR: self.name}},
            )
        ]


class _NullMemoryWrite:
    def append(self, _ctx, _records):
        return None


class _NullTracer:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)


class _AllowGate:
    def judge_intent(self, _ctx, _intent, _tensors, _memory):
        return SafetyVerdict.allow()

    def judge_action(self, _ctx, _intent, _proposal, _tensors, _memory):
        return SafetyVerdict.allow()


class _FirstProposalAggregator:
    def aggregate(self, _ctx, _intent, _tensors, proposals):
        return proposals[0]


class _NullMemoryRead:
    def snapshot(self, _ctx):
        return MemorySnapshot(items=[], summary=None, meta={})


class _NoopTensors:
    def compute(self, _ctx, _memory):
        return TensorSnapshot.now({"freedom_pressure": 0.0})


class _NoopSolarWill:
    def compute_intent(self, _ctx, _tensors, _memory):
        return Intent.neutral(), {}


def _mk_ctx() -> Context:
    return Context(
        request_id="req-protocol-v1",
        created_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        user_input="How should we balance innovation and precaution?",
    )


def test_protocol_v1_generates_critiques_and_report_fields():
    philosophers = [
        DummyPhilosopher("A", "We support rapid deployment.", 0.9, "pro"),
        DummyPhilosopher("B", "We oppose deployment without safeguards.", 0.8, "con"),
        MinimalPhilosopher("C"),
    ]

    cards, critiques, report = run_deliberation(
        input={"prompt": "test"},
        philosophers=philosophers,
        axis_spec={"axes": ["risk", "ethics"]},
        settings={"max_critiques_per_philosopher": 2},
    )

    assert len(cards) == 3
    assert critiques, "critique stage should not be empty"
    assert report["disagreements"], "synthesis should capture disagreements"
    assert report["open_questions"], "synthesis should surface open questions"


def test_ensemble_feature_flag_runs_protocol_v1(monkeypatch):
    ctx = _mk_ctx()
    tracer = _NullTracer()
    deps = EnsembleDeps(
        memory_read=_NullMemoryRead(),
        memory_write=_NullMemoryWrite(),
        tracer=tracer,
        tensors=_NoopTensors(),
        solarwill=_NoopSolarWill(),
        gate=_AllowGate(),
        philosophers=[MinimalPhilosopher("A"), MinimalPhilosopher("B")],
        aggregator=_FirstProposalAggregator(),
        aggregator_shadow=None,
        registry=None,  # type: ignore[arg-type]
        settings=None,  # type: ignore[arg-type]
        shadow_guard=None,
        deliberation_engine=None,
    )
    pre = _PhasePreResult(
        memory=MemorySnapshot(items=[], summary=None, meta={}),
        tensors=TensorSnapshot.now({"freedom_pressure": 0.0}),
        intent=Intent.neutral(),
        mode=SafetyMode.NORMAL,
        philosophers=[MinimalPhilosopher("A"), MinimalPhilosopher("B")],
        max_workers=1,
        timeout_s=1.0,
    )
    proposals = [
        Proposal(
            proposal_id="A:0",
            action_type="answer",
            content="We support deployment.",
            confidence=0.6,
            extra={PO_CORE: {AUTHOR: "A"}},
        ),
        Proposal(
            proposal_id="B:0",
            action_type="answer",
            content="We oppose deployment.",
            confidence=0.7,
            extra={PO_CORE: {AUTHOR: "B"}},
        ),
    ]

    monkeypatch.setenv("PO_DEBATE_V1", "1")
    result = _run_phase_post(ctx, deps, pre, proposals, run_results=[])

    assert result["status"] == "ok"
    assert any(getattr(e, "event_type", "") == "DebateProtocolV1Completed" for e in tracer.events)
