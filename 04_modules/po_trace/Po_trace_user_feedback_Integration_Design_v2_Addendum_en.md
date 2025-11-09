# **Po_trace × /api/user_feedback Integration Design Ver.2 – Addendum (Minor Revisions)**

## **1. Precision Adjustment for TraceEvent.timestamp**

- Change the current `Optional[str]` to `Optional[datetime]` so Pydantic handles type inference, validation, and ISO8601 conversion correctly.

**Example:**
from datetime import datetime
from pydantic import Field

timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow())

## **2. Helper Strings for Enum (for OpenAPI UI)**

- To display helper text on Swagger UI / FastAPI docs for Enum values, add `__str__()` for control.

**Example:**
from enum import Enum

class FeedbackAction(str, Enum):
    like = "like"
    override_persona = "override_persona"
    drag_cluster = "drag_cluster"

    def __str__(self):
        return f"{self.value} - Feedback via Viewer interaction"

## **3. Significance of the Addendum**

- Using datetime improves historical consistency between Viewer and Po_trace.
- Enum helper strings improve readability and intent in OpenAPI docs, aiding collaboration and review.
