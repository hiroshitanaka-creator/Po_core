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


def test_run_philosophers_adaptive_sequential_and_timeout_fallback(monkeypatch):
    from po_core.party_machine import _LATENCY_EMA_BY_PHILOSOPHER

    _LATENCY_EMA_BY_PHILOSOPHER.clear()
    monkeypatch.setenv("PO_PHILOSOPHER_SEQUENTIAL_THRESHOLD_MS", "1000")

    philosophers = [_SleepyPhilosopher(name="fast-seq", sleep_s=0.02)]

    # first run seeds EMA
    _, first_results = run_philosophers(
        philosophers,
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=1.0,
    )
    assert first_results[0].ok is True

    # second run should go sequential path and timeout fallback should be explicit
    philosophers_timeout = [_SleepyPhilosopher(name="fast-seq", sleep_s=0.06)]
    _, second_results = run_philosophers(
        philosophers_timeout,
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=0.01,
    )

    assert second_results[0].timed_out is True
    assert "fallback=empty_proposals" in (second_results[0].error or "")
