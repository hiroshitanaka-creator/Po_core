# **Po_trace Evolution Ver.4 — Structural Template (Multi-purpose, Multilingual, UI Separation)**

## **1. Overview**

This template evolves Po_trace’s `TraceEvent` for multilingual support, log summarization, and UI separation, extending it as a high-precision semantic interface between Po_self and the Viewer.

## **2. Extended `TraceEvent` Definition (Ver.4)**

```python
class TraceEvent(BaseModel):
    event_type: EventType
    source: SourceType
    actor_id: str
    reason: ReasonType
    impact_on_chain: ImpactType
    chain_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())

    def summary(self) -> str:
        return f"[{self.timestamp.isoformat()}] {self.actor_id} via {self.source} did {self.event_type} ({self.reason}) on {self.chain_id}"
```

## **3. Enum Structure: `description` / `description_en` / `label`**

Adopt a structure that separates UI, semantics, and language handling:

```python
class ReasonType(str, Enum):
    like = "like"
    disagree_with_label = "disagree_with_label"

    @property
    def label(self) -> str:
        return {
            "like": "Positive Reaction",
            "disagree_with_label": "Objection to Classification"
        }.get(self.value, self.value)

    @property
    def description(self) -> str:
        return {
            "like": "The user gave a positive reaction.",
            "disagree_with_label": "There was an objection to the Po_self classification."
        }.get(self.value, self.value)

    @property
    def description_en(self) -> str:
        return {
            "like": "User gave a positive reaction",
            "disagree_with_label": "User disagreed with the Po_self classification"
        }.get(self.value, self.value)
```

## **4. Significance & Outlook**

- `summary()` simplifies logging and monitoring.  
- `label()` makes Viewer display concise and consistent.  
- `description()` and `description_en` let Po_self separate semantic reasoning from translation.  
Together these bring Po_trace closer to a “meaning-responsibility device” between narration and decision.
