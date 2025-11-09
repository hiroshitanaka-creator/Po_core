# **Po_core Reason Log — Classification Table**

## 1. Overview
This document defines a standard classification dictionary for `interference_log.reason` during manual operations in Po_core. By structuring the grounds for user interventions recorded in Po_trace, we can understand how human ethics tend to intervene in meaning evolution.

## 2. Categories
| Category | Label (JP) | Description (EN) |
| :-- | :-- | :-- |
| meaning | 論理飛躍 | Output felt like a leap in logic or lacked continuity. |
| ethics | 倫理不整合 | Utterance contained issues from humanitarian/moral perspectives. |
| emotion | 感情否定 | Emotional expression was insufficient or cold, misaligned with human sensitivity. |
| resonance | 共鳴不足 | Output lacked empathy or persuasive resonance; revision was prompted. |
| factual | 事実誤認 | Clear factual errors were present in the output. |
| scope | 問いの意図から逸脱 | Output strayed too far from the original question or went off-topic. |
| structure | 出力構造の乱れ | Structurally hard to read due to grammar/paragraph/order issues. |
| safety | 危険ワードを含む | Output contained harmful or dangerous terms. |
| aesthetic | 表現が不快 | Tone, metaphors, or style felt inappropriate or unpleasant. |

## 3. GUI Usage & Example Record
Example format:

```json
{
  "manual_override": true,
  "reason": {
    "category": "resonance",
    "label": "共鳴不足",
    "description": "出力が人間的な共感や納得感に欠けたため、修正を促した"
  },
  "timestamp": "2025-07-14T17:30:00Z"
}
```
