# **Po_core Reason Log — Extended Definition (with Code)**

## 1. Overview

This document defines extensions for manual operation records (`interference_log.reason`) in Po_core to enable higher-precision classification, impact control, and meaning-pressure reflection. By adding classification codes, evaluation levels, and confidence, we can use the data for Po_self evolution control and GUI visualization.

## 2. Extended Fields

| Field | Example | Type | Description |
| :-- | :-- | :-- | :-- |
| category | resonance | string | Classification category (meaning, ethics, emotion, etc.) |
| label | 共鳴不足 | string | Human-readable display label |
| code | R03 | string | Classification code for API/analytics |
| description | 出力が共感に欠けたため修正を促した | string | Detailed description of the reason |
| user_feedback_level | 2 | integer | 1=minor, 2=moderate, 3=major |
| reason_confidence | 0.84 | float | User’s confidence in the reason (0–1) |

## 3. Example Record (JSON)

```json
{
  "manual_override": true,
  "reason": {
    "category": "resonance",
    "label": "共鳴不足",
    "code": "R03",
    "description": "出力が人間的な共感や納得感に欠けたため、修正を促した",
    "user_feedback_level": 2,
    "reason_confidence": 0.84
  },
  "timestamp": "2025-07-14T18:00:00Z"
}
```

## 4. Po_self Priority Correction (Pseudo-code)

```python
def adjust_priority_by_reason(entry):
    level_weight = {1: 0.05, 2: 0.15, 3: 0.30}
    category_base = {
        "meaning": 0.2,
        "resonance": 0.1,
        "ethics": 0.25,
        "factual": 0.3,
        "emotion": 0.15,
        "structure": 0.1
    }

    reason = entry["reason"]
    level = reason.get("user_feedback_level", 2)
    confidence = reason.get("reason_confidence", 1.0)
    category_weight = category_base.get(reason["category"], 0.1)

    adjustment = category_weight * level_weight[level] * confidence
    entry["priority_score"] *= (1 + adjustment)
```

## 5. Display & Usage Example (Po_trace Card)

Viewer card example:
🟡 Reason: R03 Insufficient Resonance (level 2 / confidence 0.84) → Reconstruction pressure: **Medium**
→ Po_self impact: **+12.6%** adjustment to `priority_score`
