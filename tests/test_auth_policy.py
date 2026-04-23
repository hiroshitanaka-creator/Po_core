from __future__ import annotations

from po_core.app.rest import auth


def test_evaluate_auth_policy_uses_compare_digest(monkeypatch) -> None:
    calls: list[tuple[str, str]] = []

    def _fake_compare_digest(provided: str, expected: str) -> bool:
        calls.append((provided, expected))
        return False

    monkeypatch.setattr(auth.hmac, "compare_digest", _fake_compare_digest)

    decision = auth.evaluate_auth_policy(
        skip_auth=False,
        configured_api_key="secret",
        presented_api_key="wrong",
    )

    assert decision.allowed is False
    assert decision.is_misconfigured is False
    assert decision.message == "Invalid or missing API key"
    assert calls == [("wrong", "secret")]

