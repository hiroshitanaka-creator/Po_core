# Reason Log Specification

The reason log captures **why** Po_core made a decision at a specific time.
The schema is intentionally compact so that it can be emitted from CLI tools or
stored alongside other traces.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string (UUID) | Unique identifier for the reasoning event. |
| `version` | string | Schema version. Current: `1.0`. |
| `created_at` | string (ISO 8601) | Timestamp in UTC. |
| `actor` | string | Name of the module or user that authored the log. |
| `prompt` | string | Input prompt or situation being evaluated. |
| `conclusion` | string | Final decision, answer, or selected action. |
| `rationale` | string | Explanation of how the conclusion was reached. |
| `influences` | array[string] | References to signals or prior logs that shaped the outcome. |
| `evidence` | array[string] | Concrete artifacts, citations, or data points. |
| `confidence` | float (0-1) | Normalized confidence value. |
| `tags` | array[string] | Lightweight labels for filtering. |
| `metadata` | object | Free-form structured metadata. |

## Serialization rules

- **JSON**: UTF-8 encoded object that preserves all fields above. `created_at`
  uses `datetime.isoformat()` in UTC without microseconds.
- **Markdown**: Human-friendly report including headings for Prompt, Conclusion,
  Rationale, and optional sections for Influences, Evidence, and Metadata.
- Unknown fields are ignored when parsing to keep forward compatibility.

## Example

```json
{
  "id": "7f7ab1c6-7f5d-4ed3-9410-19e2d88a7bb7",
  "version": "1.0",
  "created_at": "2024-04-01T12:00:00",
  "actor": "po-trace",
  "prompt": "Should we deploy the new viewer module?",
  "conclusion": "Proceed with staged rollout",
  "rationale": "User feedback is positive and regression tests are passing",
  "influences": ["user-feedback:R02", "test-report:2024-04-01"],
  "evidence": ["ci:green", "doc:viewer-release-notes"],
  "confidence": 0.82,
  "tags": ["release", "viewer"],
  "metadata": {"reviewers": ["po-self", "po-viewer"]}
}
```
