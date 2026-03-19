import threading
import time
from dataclasses import dataclass, field

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers
from po_core.runtime.execution_budget import ExecutionBudget, ExecutionBudgetExceeded


@dataclass
class _BudgetAwarePhilosopher:
    name: str
    sleep_s: float = 0.01
    started: threading.Event = field(default_factory=threading.Event)
    stopped: threading.Event = field(default_factory=threading.Event)
    cancelled: threading.Event = field(default_factory=threading.Event)

    def propose(self, ctx, intent, tensors, memory, budget: ExecutionBudget | None = None):
        assert budget is not None
        self.started.set()
        try:
            while True:
                budget.raise_if_cancelled_or_expired()
                time.sleep(self.sleep_s)
        except ExecutionBudgetExceeded:
            self.cancelled.set()
            self.stopped.set()
            return []


@dataclass
class _LegacySlowPhilosopher:
    name: str
    sleep_s: float = 0.2

    def propose(self, ctx, intent, tensors, memory):
        time.sleep(self.sleep_s)
        return [
            Proposal(
                proposal_id=f"{self.name}-p1",
                action_type="answer",
                content="late proposal",
                confidence=0.2,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_budget_aware_philosopher_stops_promptly_when_cancelled():
    philosopher = _BudgetAwarePhilosopher(name="aware")

    start = time.perf_counter()
    proposals, results = run_philosophers(
        [philosopher],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=0.05,
    )
    elapsed = time.perf_counter() - start

    assert proposals == []
    assert elapsed < 0.2
    assert results[0].timed_out is True
    assert "Cooperative timeout after 0.05s" in (results[0].error or "")
    assert philosopher.started.wait(0.05)
    assert philosopher.cancelled.wait(0.2)
    assert philosopher.stopped.wait(0.2)


def test_execution_budget_expires_when_polled_directly():
    budget = ExecutionBudget(timeout_s=0.01)

    time.sleep(0.02)

    assert budget.is_expired() is True
    assert budget.time_remaining_s() == 0.0


def test_non_budget_aware_philosopher_timeout_remains_soft():
    start = time.perf_counter()
    proposals, results = run_philosophers(
        [_LegacySlowPhilosopher(name="legacy")],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=0.05,
    )
    elapsed = time.perf_counter() - start

    assert proposals == []
    assert elapsed < 0.15
    assert results[0].timed_out is True
    assert "Soft timeout after 0.05s" in (results[0].error or "")
    assert "background work may still continue" in (results[0].error or "")
