"""Human-in-the-loop review queue endpoints."""

from __future__ import annotations

from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException

from po_core.app.rest.auth import require_api_key
from po_core.app.rest.models import (
    ReviewDecisionRequest,
    ReviewDecisionResponse,
    ReviewItem,
    ReviewPendingResponse,
)
from po_core.app.rest.review_store import (
    apply_review_decision,
    get_pending_reviews,
)
from po_core.app.rest.store import append_trace_event
from po_core.domain.trace_event import TraceEvent

router = APIRouter(tags=["review"])


@router.get(
    "/v1/review/pending",
    response_model=ReviewPendingResponse,
    summary="List pending human-review items",
)
async def pending_reviews(_: None = Depends(require_api_key)) -> ReviewPendingResponse:
    items = [ReviewItem(**item) for item in get_pending_reviews()]
    return ReviewPendingResponse(total=len(items), items=items)


@router.post(
    "/v1/review/{review_id}/decision",
    response_model=ReviewDecisionResponse,
    summary="Submit human decision for a review item",
)
async def review_decision(
    review_id: str,
    body: ReviewDecisionRequest,
    _: None = Depends(require_api_key),
) -> ReviewDecisionResponse:
    decision = body.decision.strip().lower()
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=422, detail="decision must be 'approve' or 'reject'")

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

    return ReviewDecisionResponse(item=ReviewItem(**item))
