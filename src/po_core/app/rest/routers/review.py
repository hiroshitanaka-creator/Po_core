"""Human-in-the-loop review queue endpoints."""

from __future__ import annotations

from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException

from po_core.app.rest.config import APISettings, get_api_settings
from po_core.app.rest.models import (
    ReviewDecisionRequest,
    ReviewDecisionResponse,
    ReviewItem,
    ReviewPendingResponse,
)
from po_core.app.rest.redaction import redact_review_comment
from po_core.app.rest.review_store import apply_review_decision, get_pending_reviews
from po_core.app.rest.scopes import Scope, require_scope
from po_core.app.rest.store import append_trace_event
from po_core.domain.trace_event import TraceEvent

router = APIRouter(tags=["review"])


def _redact_item(item: dict, *, redact: bool) -> dict:
    if not redact:
        return item
    redacted = dict(item)
    redacted["comment"] = redact_review_comment(item.get("comment"))
    return redacted


@router.get(
    "/v1/review/pending",
    response_model=ReviewPendingResponse,
    summary="List pending human-review items",
)
async def pending_reviews(
    _: None = Depends(require_scope(Scope.REVIEW_WRITE)),
    settings: APISettings = Depends(get_api_settings),
) -> ReviewPendingResponse:
    redact = bool(settings.redact_trace_responses)
    items = [
        ReviewItem(**_redact_item(item, redact=redact))
        for item in get_pending_reviews()
    ]
    return ReviewPendingResponse(total=len(items), items=items)


@router.post(
    "/v1/review/{review_id}/decision",
    response_model=ReviewDecisionResponse,
    summary="Submit human decision for a review item",
)
async def review_decision(
    review_id: str,
    body: ReviewDecisionRequest,
    _: None = Depends(require_scope(Scope.REVIEW_WRITE)),
    settings: APISettings = Depends(get_api_settings),
) -> ReviewDecisionResponse:
    decision = body.decision.strip().lower()
    if decision not in {"approve", "reject"}:
        raise HTTPException(
            status_code=422, detail="decision must be 'approve' or 'reject'"
        )

    item = apply_review_decision(
        review_id,
        decision=decision,
        reviewer=body.reviewer,
        comment=body.comment,
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Review item not found")

    append_trace_event(
        item["session_id"],
        TraceEvent(
            event_type="HumanReviewDecided",
            occurred_at=item["decided_at"].astimezone(timezone.utc),
            correlation_id=item["request_id"],
            payload={
                "review_id": review_id,
                "decision": decision,
                "reviewer": body.reviewer,
                "comment": body.comment or "",
            },
        ),
    )

    redact = bool(settings.redact_trace_responses)
    return ReviewDecisionResponse(item=ReviewItem(**_redact_item(item, redact=redact)))
