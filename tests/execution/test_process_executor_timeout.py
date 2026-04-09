from __future__ import annotations

import time
from dataclasses import dataclass
from types import SimpleNamespace

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers
from po_core.runtime.philosopher_executor import _run_one_in_subprocess


@dataclass
class _BlockingPhil:
    name: str
    sleep_s: float

    def propose(self, ctx, intent, tensors, memory):
        time.sleep(self.sleep_s)
        return [
            Proposal(
                proposal_id=f"{self.name}-late",
                action_type="answer",
                content="late",
                confidence=0.1,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


@dataclass
class _FastPhil:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return [
            Proposal(
                proposal_id=f"{self.name}-ok",
                action_type="answer",
                content="ok",
                confidence=0.9,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_process_executor_timeout_is_authoritative():
    proposals, results = run_philosophers(
        [_BlockingPhil(name="slow", sleep_s=0.6), _FastPhil(name="fast")],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=2,
        timeout_s=0.2,
        execution_mode="process",
    )

    assert [result.philosopher_id for result in results] == ["slow", "fast"]
    assert results[0].timed_out is True
    assert results[0].ok is False
    assert results[0].n == 0
    assert results[0].error == "Hard timeout after 0.2s"
    assert results[1].timed_out is False
    assert results[1].ok is True
    assert [proposal.proposal_id for proposal in proposals] == ["fast-ok"]

    time.sleep(0.7)
    assert [proposal.proposal_id for proposal in proposals] == ["fast-ok"]


def test_process_executor_child_bootstrap_failure_is_not_reported_as_timeout(
    monkeypatch,
):
    """Regression: child crash/bootstrap failure is currently collapsed into timeout."""

    class _DummyQueue:
        def get(self, timeout):
            raise EOFError("child exited before posting outcome")

        def close(self):
            return None

    class _DummyProcess:
        def __init__(self):
            self._alive = False
            self.exitcode = 1

        def start(self):
            return None

        def terminate(self):
            return None

        def join(self, timeout=None):
            return None

        def is_alive(self):
            return self._alive

        def kill(self):
            return None

    class _DummyContext:
        def Queue(self, maxsize=1):
            return _DummyQueue()

        def Process(self, target, args):
            return _DummyProcess()

    monkeypatch.setattr(
        "po_core.runtime.philosopher_executor.multiprocessing.get_context",
        lambda _method: _DummyContext(),
    )
    monkeypatch.setattr(
        "po_core.runtime.philosopher_executor.multiprocessing.get_all_start_methods",
        lambda: ["spawn"],
    )

    job = SimpleNamespace(
        philosopher=SimpleNamespace(name="boot-fail"),
        timeout_s=0.2,
    )

    outcome = _run_one_in_subprocess(job)

    assert outcome.error is not None
    assert "timeout" not in outcome.error.lower()
