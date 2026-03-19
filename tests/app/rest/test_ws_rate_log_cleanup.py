from __future__ import annotations

from collections import deque
from types import SimpleNamespace

from starlette.datastructures import Headers

from po_core.app.rest.config import APISettings
from po_core.app.rest.routers import reason as reason_router


def test_ws_rate_log_cleanup_removes_stale_and_empty_entries(monkeypatch) -> None:
    reason_router._ws_rate_log.clear()
    reason_router._ws_rate_log["stale"] = deque([1.0])
    reason_router._ws_rate_log["empty"] = deque()
    reason_router._ws_rate_log["fresh"] = deque([115.0])

    websocket = SimpleNamespace(
        headers=Headers({"x-forwarded-for": "203.0.113.10"}),
        client=SimpleNamespace(host="198.51.100.10"),
    )

    monkeypatch.setattr(reason_router.time, "monotonic", lambda: 122.0)

    limited = reason_router._is_ws_rate_limited(
        websocket,
        rpm=2,
        settings=APISettings(trust_proxy_headers=True),
    )

    assert limited is False
    assert "stale" not in reason_router._ws_rate_log
    assert "empty" not in reason_router._ws_rate_log
    assert list(reason_router._ws_rate_log["fresh"]) == [115.0]
    assert list(reason_router._ws_rate_log["203.0.113.10"]) == [122.0]
