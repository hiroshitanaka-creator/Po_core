# **Po_core Reason Log — Advanced Completion Module Spec**

## 1. Overview

To raise the structural completeness of Reason Log (manual operation records) in Po_core, this spec designs a complement module that integrates two elements: **reason_source_context** (context recording) and **reason_temporal_decay** (time-decay correction).

## 2. Extensions and Aims

| Extension | Content | Purpose |
| :-- | :-- | :-- |
| reason_source_context | Record the triggering output and the sensed mismatch | Enables reproducible human-judgment logs and supports Po_self’s understanding of background context. |
| reason_temporal_decay | Confidence attached to a reason decays over time | Prevents overly persistent reconstruction pressure and gives Po_self dynamic flexibility. |

## 3. Unified JSON Structure (Example)

```json
{
  "manual_override": true,
  "reason": {
    "category": "emotion",
    "label": "感情否定",
    "code": "E02",
    "description": "詩的出力だったが感情が伝わらなかった",
    "user_feedback_level": 2,
    "reason_confidence": 0.84,
    "reason_source_context": {
      "trigger_text": "君の詩的返答が冷たく感じられた",
      "observed_gap": "emotion_score ≈ 0.1 / user_expected ≈ 0.6",
      "notes": "過去の応答ではもっと共感的だった"
    },
    "timestamp": "2025-07-14T18:00:00Z"
  }
}
```

## 4. Temporal Decay

`reason_confidence` used for Po_self’s priority correction decays automatically as time passes.
Example: after 48 hours, confidence 0.84 → ~0.72.

Pseudo-code:

```python
def apply_temporal_decay(entry, timestamp_now):
    t0 = entry["reason"]["timestamp"]
    elapsed_hours = (timestamp_now - t0).total_seconds() / 3600
    decay_rate = 0.005
    decay_factor = max(0.6, 1 - decay_rate * elapsed_hours)
    return decay_factor
```

## 5. Po_self Priority Correction (Extended)

```python
def adjust_priority_by_reason_v2(entry, now):
    level_weight = {1: 0.05, 2: 0.15, 3: 0.30}
    category_weight = {
        "meaning": 0.2, "resonance": 0.1, "ethics": 0.25,
        "factual": 0.3, "emotion": 0.15, "structure": 0.1
    }

    reason = entry["reason"]
    level = reason.get("user_feedback_level", 2)
    confidence = reason.get("reason_confidence", 1.0)
    decay = apply_temporal_decay(entry, now)
    category = reason.get("category", "misc")

    base_weight = category_weight.get(category, 0.1)
    adjustment = base_weight * level_weight[level] * confidence * decay
    entry["priority_score"] *= (1 + adjustment)
```

## 6. Significance & Future Work

With these extensions, Po_core can reason about **why** a human made a certain judgment and **whether** that judgment should still carry weight. This enables ethically and resonantly dynamic corrections in Po_self’s reconstruction decisions.
