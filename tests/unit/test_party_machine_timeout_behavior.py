import time
from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers


@dataclass
class _SleepyPhilosopher:
    name: str
    sleep_s: float

    def propose(self, ctx, intent, tensors, memory):
        time.sleep(self.sleep_s)
        return [
            Proposal(
                proposal_id=f"{self.name}-p1",
                action_type="answer",
                content=f"proposal from {self.name}",
                confidence=0.5,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_run_philosophers_uses_global_timeout_window():
    philosophers = [
        _SleepyPhilosopher(name="slow-a", sleep_s=0.35),
        _SleepyPhilosopher(name="slow-b", sleep_s=0.35),
        _SleepyPhilosopher(name="fast", sleep_s=0.01),
    ]

    start = time.perf_counter()
    proposals, results = run_philosophers(
        philosophers,
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=3,
        timeout_s=0.1,
    )
    elapsed = time.perf_counter() - start

    assert elapsed < 0.25

    by_id = {r.philosopher_id: r for r in results}
    assert by_id["slow-a"].timed_out is True
    assert by_id["slow-b"].timed_out is True
    assert by_id["fast"].ok is True

    assert len(proposals) == 1
    assert proposals[0].extra["_po_core"]["author"] == "fast"
