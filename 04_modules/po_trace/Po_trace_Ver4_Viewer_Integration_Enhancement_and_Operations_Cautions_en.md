# **Po_trace Ver.4 — Viewer Integration Enhancements & Operational Cautions (Design Doc)**

## **1. Overview**

This document proposes an extension plan for Po_trace Ver.4 that strengthens integration with the Viewer: adding helper methods, separating UI-facing structures, exposing metadata via API, and capturing operational caveats for Enums.

## **2. TraceEvent Reinforcement: `as_ui_card()`**

Provide a method that returns a ready-to-render dictionary for card display on the Viewer.

```python
def as_ui_card(self) -> dict:
    return {
        "timestamp": self.timestamp.isoformat(),
        "actor": self.actor_id,
        "source": self.source,
        "event": self.event_type,
        "reason": {
            "value": self.reason.value,
            "label": self.reason.label,
            "description": self.reason.description
        },
        "impact": {
            "value": self.impact_on_chain.value,
            "label": self.impact_on_chain.label,
            "description": self.impact_on_chain.description
        },
        "chain_id": self.chain_id
    }
```

## **3. Using `Enum.label()` to Improve UI Selectors**

- Show `reason.label` in Viewer select boxes to make categories intuitive.
- Reuse `impact.label` as-is for tag badges (e.g., 🔁 Re-clustering).

## **4. OpenAPI Limitations and `/api/event_metadata`**

- Custom accessors like `.description_en()` and `.label()` won’t appear in FastAPI’s auto docs.
  Expose the mapping as JSON via a dedicated endpoint such as `/api/event_metadata` to supply labels and translations for each Enum.

## **5. Handling Enums in the Database**

- Persist the Enum’s `.value` so queries and aggregation stay simple.
- Reconstruct in logic via `ReasonType(stored_value)` when needed.

## **6. Closing Note**

Po_trace Ver.4 evolves from a raw history log to a multi-layered, accountable structure for meaning/role/responsibility. These extensions markedly increase interoperability and semantic density between the Viewer and Po_self.
