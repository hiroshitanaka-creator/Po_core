# `run_case()` API Guide

`run_case(case: dict)` is the structured-case entry point for Po_core.

Use it when you want an `output_schema_v1`-conformant decision-support response with top-level fields such as `meta`, `case_ref`, `options`, `recommendation`, `ethics`, `responsibility`, `questions`, `uncertainty`, and `trace`.

Use `run(user_input: str)` when you want the raw philosophical runtime result for a plain text prompt.

---

## API split

| API | Input | Output | Use when |
|---|---|---|---|
| `run(user_input: str)` | Plain text | Raw pipeline dict: `{status, request_id, proposal, proposals}` | You want direct philosopher pipeline output |
| `run_case(case: dict)` | Structured case dict | `output_schema_v1`-conformant dict | You want decision-support output with options, ethics, uncertainty, questions, and trace |

`run_case()` does **not** replace `run()`. It is a separate public entry point that preserves the existing `run(user_input: str)` contract.

---

## Minimal example

```python
from po_core import run_case

case = {
    "case_id": "case_001_job_change",
    "title": "転職すべきか：現職維持 vs やりがい優先の転職",
    "problem": "現職は安定しているが成長感がない。転職先はやりがいがあるが収入が2割減。",
    "values": ["長期的な成長", "家族との時間", "経済的安定", "誠実さ"],
    "constraints": ["引っ越し不可", "生活費を下回る収入は不可"],
    "stakeholders": ["自分", "配偶者", "子ども（2人）"],
}

result = run_case(case)

print(result["meta"]["schema_version"])
print(result["case_ref"]["case_id"])
print(result["recommendation"]["status"])
print(result["options"][0]["description"])
```

---

## Empty values case

When `values` is an explicit empty list, `run_case()` surfaces values-clarification behavior through the schema output.

```python
from po_core import run_case

case = {
    "case_id": "case_009_unclear_values",
    "title": "価値観が未定義な状態での意思決定",
    "problem": "将来のキャリアについて考えているが、何を重視すべきか自分でもわかっていない。",
    "values": [],
    "constraints": [],
}

result = run_case(case)

assert result["questions"]
print(result["recommendation"]["status"])
print(result["questions"][0]["question"])
```

---

## Conflicting constraints case

When a structured case contains conflicting constraints, `run_case()` uses `CaseSignals` before adapting the result to `output_schema_v1`.

```python
from po_core import run_case

case = {
    "case_id": "case_010_conflicting_constraints",
    "title": "矛盾した制約のもとでの起業計画",
    "problem": "副業として起業を検討しているが、制約が相互に矛盾している。",
    "constraints": [
        "半年以内に起業を本格始動（週20時間以上投入したい）",
        "収入は一切落とせない",
        "起業に使える時間は週5時間が上限",
        "今の仕事は辞めない",
    ],
    "values": ["経済的自立", "自己実現", "家族の安定"],
    "extensions": {"scenario_profile": "conflicting_constraints"},
}

result = run_case(case)

assert result["uncertainty"]["overall_level"] == "high"
print(result["questions"])
```

---

## Determinism contract

By default, `run_case()` uses `seed=42`. When a seed is provided and the case does not include a `now` field, the output uses the fixed timestamp:

```text
2026-03-03T00:00:00Z
```

This mirrors the `StubComposer` determinism contract.

```python
from po_core import run_case

result = run_case({
    "case_id": "case_demo",
    "title": "Demo",
    "problem": "Should I proceed?",
    "values": ["safety", "accountability"],
})

assert result["meta"]["created_at"] == "2026-03-03T00:00:00Z"
assert result["meta"]["deterministic"] is True
```

To opt out of deterministic timestamping, pass `seed=None`.

```python
result = run_case(case, seed=None)
assert result["meta"]["deterministic"] is False
```

To set an explicit timestamp, pass `now` or include `case["now"]`.

---

## Internal flow

`run_case()` is intentionally thin:

```text
case dict
  ├─ build_user_input(case)
  ├─ from_case_dict(case)
  ├─ run(user_input, case_signals=...)
  └─ adapt_to_schema(case, run_result, ...)
```

It does not change `run(user_input: str)`. It does not remove `output_adapter`. It makes the structured-output bridge explicit and available as a public API.

---

## Validation

`run_case()` is covered by runtime acceptance tests for three representative scenarios:

- AT-001: full-values decision case
- AT-009: empty-values clarification case
- AT-010: conflicting-constraints case

The tests validate `run_case()` output against `docs/spec/output_schema_v1.json`.
