from __future__ import annotations

from fastapi import FastAPI, Request
from starlette.datastructures import Headers
from starlette.requests import ClientDisconnect

from po_core.app.rest.config import APISettings
from po_core.app.rest.rate_limit import get_rate_limit_key
from po_core.app.rest.routers.reason import _client_ip_from_headers


class _Client:
    def __init__(self, host: str) -> None:
        self.host = host


def _build_request(
    *, trust_proxy_headers: bool, x_forwarded_for: str | None
) -> Request:
    app = FastAPI()
    app.state.settings = APISettings(trust_proxy_headers=trust_proxy_headers)
    headers: list[tuple[bytes, bytes]] = []
    if x_forwarded_for is not None:
        headers.append((b"x-forwarded-for", x_forwarded_for.encode("utf-8")))
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "path": "/v1/reason",
        "raw_path": b"/v1/reason",
        "query_string": b"",
        "headers": headers,
        "client": ("198.51.100.10", 50000),
        "server": ("testserver", 80),
        "scheme": "http",
        "app": app,
    }

    async def _receive() -> ClientDisconnect:
        raise AssertionError("request body should not be read")

    return Request(scope, _receive)


def test_http_rate_limit_key_ignores_forwarded_for_when_proxy_trust_disabled() -> None:
    request = _build_request(
        trust_proxy_headers=False,
        x_forwarded_for="203.0.113.5, 198.51.100.2",
    )

    assert get_rate_limit_key(request) == "198.51.100.10"


def test_http_rate_limit_key_uses_forwarded_for_when_proxy_trust_enabled() -> None:
    request = _build_request(
        trust_proxy_headers=True,
        x_forwarded_for="203.0.113.5, 198.51.100.2",
    )

    assert get_rate_limit_key(request) == "203.0.113.5"


def test_websocket_rate_limit_key_matches_http_proxy_trust_rules() -> None:
    headers = Headers({"x-forwarded-for": "203.0.113.7, 198.51.100.3"})
    client = _Client(host="198.51.100.10")

    trusted = _client_ip_from_headers(
        headers,
        APISettings(trust_proxy_headers=True),
        client,
    )
    untrusted = _client_ip_from_headers(
        headers,
        APISettings(trust_proxy_headers=False),
        client,
    )

    assert trusted == "203.0.113.7"
    assert untrusted == "198.51.100.10"
