from __future__ import annotations

from types import SimpleNamespace

from po_core.runtime.philosopher_executor import _run_one_in_subprocess


class _FakeQueue:
    def __init__(self, *, raises_empty: bool = False):
        self._raises_empty = raises_empty

    def get(self, timeout):
        if self._raises_empty:
            import queue

            raise queue.Empty()
        return "not-used"

    def close(self):
        return None


class _FakeProc:
    def __init__(self, exitcode):
        self.exitcode = exitcode

    def start(self):
        return None

    def terminate(self):
        return None

    def join(self, timeout=None):
        return None

    def is_alive(self):
        return False

    def kill(self):
        return None


class _FakeCtx:
    def __init__(self, *, exitcode):
        self._exitcode = exitcode

    def Queue(self, maxsize=1):
        return _FakeQueue(raises_empty=True)

    def Process(self, target, args):
        return _FakeProc(exitcode=self._exitcode)


def _fake_job(timeout_s: float):
    return SimpleNamespace(
        philosopher=SimpleNamespace(name="phil"), timeout_s=timeout_s
    )


def test_subprocess_empty_queue_with_nonzero_exit_is_child_crash(monkeypatch):
    monkeypatch.setattr(
        "po_core.runtime.philosopher_executor.multiprocessing.get_context",
        lambda name: _FakeCtx(exitcode=9),
    )

    outcome = _run_one_in_subprocess(_fake_job(timeout_s=0.01))
    assert outcome.timed_out is False
    assert outcome.error == "Child process crashed (exit_code=9)"


def test_subprocess_empty_queue_with_zero_exit_is_timeout(monkeypatch):
    monkeypatch.setattr(
        "po_core.runtime.philosopher_executor.multiprocessing.get_context",
        lambda name: _FakeCtx(exitcode=0),
    )

    outcome = _run_one_in_subprocess(_fake_job(timeout_s=0.01))
    assert outcome.timed_out is True
    assert outcome.error == "Hard timeout after 0.01s"
