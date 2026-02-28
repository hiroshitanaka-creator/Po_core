# Decision Session v1: 回答入力契約（session_answers_v1）

この文書は、Decision Session v1 における「回答入力」の固定契約を定義する。

- 対応スキーマ: `docs/spec/session_answers_schema_v1.json`
- 目的: 質問回答と、その回答を反映する JSON Patch を決定的に受け渡す

## 1. トップレベル構造

トップレベルは次の4キーを必須とする。

- `version`: 契約バージョン文字列（`"1.0"` 固定）
- `case_ref`: 対象ケース参照（`case_id` など）
- `answers`: 質問ごとの回答配列
- `patch`: RFC6902 JSON Patch 操作配列

```json
{
  "version": "1.0",
  "case_ref": "case_012",
  "answers": [
    {
      "question_id": "q_budget_limit",
      "answer_text": "初期予算は月5万円までです。",
      "applied_patch_paths": ["/constraints/budget", "/notes/0"]
    }
  ],
  "patch": [
    { "op": "replace", "path": "/constraints/budget", "value": "<=50000 JPY/month" },
    { "op": "add", "path": "/notes/0", "value": "予算上限: 月5万円" }
  ]
}
```

## 2. answers[]

`answers[]` の各要素は以下を必須とする。

- `question_id` (`string`): 質問ID
- `answer_text` (`string`): ユーザー回答本文
- `applied_patch_paths` (`string[]`): この回答が影響する JSON Pointer の配列

制約:

- `question_id` は1文字以上
- `answer_text` は1文字以上
- `applied_patch_paths` は空配列可、各要素は `/` で始まる JSON Pointer 形式

## 3. patch[]

`patch[]` は RFC6902 互換の操作配列。

各操作オブジェクトで以下を必須とする。

- `op`: `add | remove | replace | move | copy | test`
- `path`: JSON Pointer（`/` で開始）
- `value`: 操作値（JSON値）

注記:

- 本契約では入力の単純化のため `value` を常に要求する。
- `from` を使う操作（`move`/`copy`）は v1 では受け付けない。

## 4. YAML入力例

```yaml
version: "1.0"
case_ref: "case_012"
answers:
  - question_id: "q_budget_limit"
    answer_text: "初期予算は月5万円までです。"
    applied_patch_paths:
      - "/constraints/budget"
patch:
  - op: "replace"
    path: "/constraints/budget"
    value: "<=50000 JPY/month"
```
