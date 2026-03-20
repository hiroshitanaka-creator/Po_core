from __future__ import annotations

from po_core.app.rest.routers.reason import _fallback_summary


def test_fallback_summary_keeps_stable_sorted_list_with_rich_metadata():
    result = {
        "proposals": [
            {
                "normalized_response": {
                    "metadata": {
                        "llm_fallback": True,
                        "fallback": {"reason": "provider_rate_limit"},
                    }
                }
            },
            {
                "metadata": {
                    "llm_fallback": True,
                    "fallback_reason": "provider_auth_error",
                    "fallback": {
                        "reason": "provider_auth_error",
                        "error_kind": "auth",
                        "status_code": 401,
                        "provider": "openai",
                        "model": "gpt-4o-mini",
                        "retriable": False,
                    },
                }
            },
            {
                "llm_fallback": True,
                "fallback_reason": "provider_rate_limit",
            },
        ]
    }

    llm_fallback, fallback_reasons = _fallback_summary(result)

    assert llm_fallback is True
    assert fallback_reasons == ["provider_auth_error", "provider_rate_limit"]
