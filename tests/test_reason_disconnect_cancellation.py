from __future__ import annotations

import asyncio
from unittest.mock import patch

import pytest

from po_core.app.rest.config import APISettings
from po_core.app.rest.models import ReasonRequest
from po_core.app.rest.routers.reason import _stream_reasoning_chunks


async def _assert_stream_disconnect_cancels_task(source: str) -> None:
    started = asyncio.Event()
    cancelled = asyncio.Event()
    finalized = asyncio.Event()
    saw_started = asyncio.Event()

    async def _never_finishes(*, user_input, settings, tracer, philosophers=None):
        started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise
        finally:
            finalized.set()

    async def _consume_until_cancelled() -> None:
        body = ReasonRequest(
            input="disconnect me",
            session_id=f"session-{source.rsplit('/', 1)[-1]}",
        )
        api_settings = APISettings(skip_auth=True, api_key="")
        async for chunk in _stream_reasoning_chunks(body, api_settings, source=source):
            if chunk["chunk_type"] == "started":
                saw_started.set()

    with patch("po_core.app.rest.routers.reason.po_async_run", side_effect=_never_finishes):
        consumer = asyncio.create_task(_consume_until_cancelled())
        await asyncio.wait_for(saw_started.wait(), timeout=1.0)
        await asyncio.wait_for(started.wait(), timeout=1.0)
        consumer.cancel()
        with pytest.raises(asyncio.CancelledError):
            await consumer

    await asyncio.wait_for(cancelled.wait(), timeout=1.0)
    await asyncio.wait_for(finalized.wait(), timeout=1.0)


@pytest.mark.asyncio
async def test_sse_disconnect_cancels_stream_worker() -> None:
    await _assert_stream_disconnect_cancels_task("/v1/reason/stream")


@pytest.mark.asyncio
async def test_websocket_disconnect_cancels_stream_worker() -> None:
    await _assert_stream_disconnect_cancels_task("/v1/ws/reason")
