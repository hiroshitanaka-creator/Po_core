"""
Vertical Slice Test
===================

Tests the full pipeline through run_turn.
"""
from __future__ import annotations

from datetime import datetime, timezone

from po_core.app.api import run


class FakePoSelf:
    """Fake Po_self for testing."""

    def __init__(self):
        self.writes = []

    def read(self, request_id, user_input, meta):
        """Return a minimal memory snapshot."""
        return {
            "items": [
                {
                    "id": "m1",
                    "created_at": datetime.now(timezone.utc),
                    "text": "hello",
                    "tags": ["seed"],
                },
            ],
            "summary": "seed memory",
            "meta": {"source": "fake"},
        }

    def write(self, request_id, payload):
        """Record writes for verification."""
        self.writes.append((request_id, payload))


def test_vertical_slice_runs():
    """Test that the full vertical slice pipeline runs."""
    mem = FakePoSelf()
    out = run("test input", memory_backend=mem)

    assert out["status"] in ("ok", "fallback")
    assert "request_id" in out


def test_vertical_slice_without_memory():
    """Test the pipeline with in-memory adapter (no backend)."""
    out = run("test input without backend")

    assert out["status"] in ("ok", "fallback")
    assert "request_id" in out


def test_vertical_slice_produces_proposal():
    """Test that successful run produces a proposal."""
    out = run("What is justice?")

    if out["status"] == "ok":
        assert "proposal" in out
        assert "proposal_id" in out["proposal"]
        assert "action_type" in out["proposal"]
    elif out["status"] == "fallback":
        # Fallback generates a safe proposal from verdict
        assert "stage" in out
        assert "verdict" in out
        assert "proposal" in out
        assert "action_type" in out["proposal"]
    else:
        raise AssertionError(f"Unexpected status: {out['status']}")
