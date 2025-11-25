from datetime import datetime
from typing import Iterator

import pytest

from po_core import ensemble


@pytest.fixture()
def fixed_timestamp(monkeypatch) -> Iterator[str]:
    """Patch ensemble datetime to produce deterministic timestamps for logs."""

    class _FixedDatetime(datetime):
        @classmethod
        def utcnow(cls) -> datetime:
            return datetime(2024, 1, 1, 12, 0, 0)

    monkeypatch.setattr(ensemble, "datetime", _FixedDatetime)
    yield _FixedDatetime.utcnow().isoformat() + "Z"


@pytest.fixture()
def ensemble_run(sample_prompt, fixed_timestamp):
    """Execute the deterministic ensemble with a fixed timestamp."""

    return ensemble.run_ensemble(sample_prompt)
