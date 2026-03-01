from __future__ import annotations

from datetime import datetime, timezone

from po_core.deliberation.engine import DeliberationEngine
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode
from po_core.domain.safety_verdict import SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ensemble import EnsembleDeps, _PhasePreResult, _normalize_primary_proposals, _run_phase_post
from po_core.party_machine import run_philosophers


class _DummyPhilosopher:
    def __init__(self, name: str, proposals: list[Proposal | None]) -> None:
        self.name = name
        self._proposals = proposals

    def propose(self, *_args, **_kwargs):
        return list(self._proposals)


class _NullMemoryRead:
    def snapshot(self, _ctx):
        return MemorySnapshot(items=[], summary=None, meta={})


class _NullMemoryWrite:
    def __init__(self) -> None:
        self.records = []

    def append(self, _ctx, records):
        self.records.extend(records)


class _NullTracer:
    def __init__(self) -> None:
        self.events = []

    def emit(self, event):
        self.events.append(event)


class _NoopTensors:
    def compute(self, _ctx, _memory):
        return TensorSnapshot.now({"freedom_pressure": 0.0})


class _NoopSolarWill:
    def compute_intent(self, _ctx, _tensors, _memory):
        return Intent.neutral(), {}


class _AllowGate:
    def judge_intent(self, _ctx, _intent, _tensors, _memory):
        return SafetyVerdict.allow()

    def judge_action(self, _ctx, _intent, _proposal, _tensors, _memory):
        return SafetyVerdict.allow()


class _FirstProposalAggregator:
    def aggregate(self, _ctx, _intent, _tensors, proposals):
        return proposals[0]


def _mk_ctx() -> Context:
    return Context(
        request_id="req-multi",
        created_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        user_input="test",
    )


def _mk_proposal(pid: str, author: str | None = None, *, fallback: bool = False) -> Proposal:
    extra = {}
    if author is not None:
        extra = {PO_CORE: {AUTHOR: author}}
    if fallback:
        extra = {"philosopher": "legacy_author"}
    return Proposal(
        proposal_id=pid,
        action_type="answer",
        content=f"content:{pid}",
        confidence=0.6,
        extra=extra,
    )


def test_run_philosophers_collects_multiple_proposals_with_limit() -> None:
    ctx = _mk_ctx()
    ph = _DummyPhilosopher("dummy", [_mk_proposal("p0"), _mk_proposal("p1")])

    proposals, results = run_philosophers(
        [ph],
        ctx,
        Intent.neutral(),
        TensorSnapshot.now({"freedom_pressure": 0.0}),
        MemorySnapshot(items=[], summary=None, meta={}),
        max_workers=1,
        timeout_s=1.0,
        limit_per_philosopher=3,
    )

    assert len(proposals) == 2
    assert results[0].n == 2


def test_run_philosophers_embeds_author_and_proposal_index() -> None:
    ctx = _mk_ctx()
    ph = _DummyPhilosopher("dummy", [_mk_proposal("p0"), _mk_proposal("p1")])

    proposals, _ = run_philosophers(
        [ph],
        ctx,
        Intent.neutral(),
        TensorSnapshot.now({"freedom_pressure": 0.0}),
        MemorySnapshot(items=[], summary=None, meta={}),
        max_workers=1,
        timeout_s=1.0,
        limit_per_philosopher=3,
    )

    assert proposals[0].extra[PO_CORE][AUTHOR] == "dummy"
    assert proposals[0].extra[PO_CORE]["proposal_index"] == 0
    assert proposals[1].extra[PO_CORE][AUTHOR] == "dummy"
    assert proposals[1].extra[PO_CORE]["proposal_index"] == 1


def test_normalize_primary_proposals_handles_empty_none_and_fallback_author() -> None:
    primary, secondary = _normalize_primary_proposals([])
    assert primary == []
    assert secondary == []

    proposals = [
        _mk_proposal("a-0", "author_a"),
        _mk_proposal("a-1", "author_a"),
        _mk_proposal("legacy-0", None, fallback=True),
        _mk_proposal("legacy-1", None, fallback=True),
        _mk_proposal("no-author"),
    ]

    primary, secondary = _normalize_primary_proposals(proposals)

    assert [p.proposal_id for p in primary] == ["a-0", "legacy-0", "no-author"]
    assert [p.proposal_id for p in secondary] == ["a-1", "legacy-1"]


def test_run_phase_post_with_deliberation_rounds_two_completes_without_exception() -> None:
    ctx = _mk_ctx()
    tracer = _NullTracer()
    memory_write = _NullMemoryWrite()

    deps = EnsembleDeps(
        memory_read=_NullMemoryRead(),
        memory_write=memory_write,
        tracer=tracer,
        tensors=_NoopTensors(),
        solarwill=_NoopSolarWill(),
        gate=_AllowGate(),
        philosophers=[],
        aggregator=_FirstProposalAggregator(),
        aggregator_shadow=None,
        registry=None,  # type: ignore[arg-type]
        settings=None,  # type: ignore[arg-type]
        shadow_guard=None,
        deliberation_engine=DeliberationEngine(max_rounds=2),
    )

    pre = _PhasePreResult(
        memory=MemorySnapshot(items=[], summary=None, meta={}),
        tensors=TensorSnapshot.now({"freedom_pressure": 0.0}),
        intent=Intent.neutral(),
        mode=SafetyMode.NORMAL,
        philosophers=[],
        max_workers=1,
        timeout_s=1.0,
    )

    proposals = [_mk_proposal("a-0", "author_a"), _mk_proposal("a-1", "author_a")]
    result = _run_phase_post(
        ctx,
        deps,
        pre,
        proposals + [None],
        [],
    )

    assert result["status"] == "ok"
    assert result["proposal"]["proposal_id"] in {"a-0", "a-1"}
