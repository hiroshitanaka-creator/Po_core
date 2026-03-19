from __future__ import annotations

import time
from dataclasses import dataclass, field
from threading import Event


class ExecutionBudgetExceeded(TimeoutError):
    """Raised when cooperative execution budget is cancelled or expires."""


@dataclass(slots=True)
class ExecutionBudget:
    """Thread-safe cooperative budget with a monotonic deadline."""

    timeout_s: float
    deadline_monotonic: float = field(init=False)
    _cancel_event: Event = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.deadline_monotonic = time.monotonic() + max(0.0, self.timeout_s)
        self._cancel_event = Event()

    def time_remaining_s(self) -> float:
        """Return remaining budget in seconds, floored at zero."""
        return max(0.0, self.deadline_monotonic - time.monotonic())

    def is_cancelled(self) -> bool:
        """Return True when the budget has been cancelled explicitly."""
        return self._cancel_event.is_set()

    def is_expired(self) -> bool:
        """Return True when cancelled or when the monotonic deadline has passed."""
        return self.is_cancelled() or self.time_remaining_s() <= 0.0

    def cancel(self) -> None:
        """Request cooperative cancellation."""
        self._cancel_event.set()

    def raise_if_cancelled_or_expired(self) -> None:
        """Raise ExecutionBudgetExceeded if cancellation or timeout was requested."""
        if self.is_cancelled():
            raise ExecutionBudgetExceeded("Execution budget cancelled")
        if self.time_remaining_s() <= 0.0:
            raise ExecutionBudgetExceeded("Execution budget expired")


__all__ = ["ExecutionBudget", "ExecutionBudgetExceeded"]
