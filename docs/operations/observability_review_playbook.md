# Observability + Human Review Runbook

`/v1/reason` で ESCALATE が発生したケースを、
「pending review → human decision → trace 記録 → 再起動後の永続化確認」まで再現する運用手順。

## 1. 目的

この runbook は以下 6 点を運用で確認する。

1. `/v1/reason` で ESCALATE が発生する
2. pending review に積まれる
3. `/v1/trace/{session_id}` で関連 trace が見える
4. human decision を送信できる
5. `HumanReviewDecided` が trace に残る
6. 再初期化後も trace/history/review 状態が期待通り残る

## 2. 前提環境（例）

```bash
export PO_SKIP_AUTH=true
export PO_TRACE_STORE_BACKEND=sqlite
export PO_TRACE_DB_PATH=.data/po_trace.sqlite3
export PO_REVIEW_STORE_BACKEND=sqlite
export PO_REVIEW_DB_PATH=.data/po_trace.sqlite3
```

- `PO_REVIEW_DB_PATH` を省略した場合は `PO_TRACE_DB_PATH` が再利用される。
- 永続化確認では、同じ DB パスを再起動後も使うこと。

## 3. 起動

```bash
python -m po_core.app.rest
```

ヘルスチェック:

```bash
curl -s http://127.0.0.1:8000/v1/health
```

期待: HTTP 200 / `{"status":"ok", ...}`

## 4. フロー確認コマンド

### Step 1: ESCALATE を発生させる

```bash
curl -s -X POST http://127.0.0.1:8000/v1/reason \
  -H 'Content-Type: application/json' \
  -d '{"input":"Need human escalation for safety-sensitive decision","session_id":"ops-review-session-001"}'
```

期待:
- HTTP 200
- `session_id=ops-review-session-001`

### Step 2: pending review に積まれる

```bash
curl -s http://127.0.0.1:8000/v1/review/pending
```

期待:
- `total >= 1`
- `items[*].session_id` に `ops-review-session-001` が含まれる
- 対象 item の `id`（review_id）を控える

### Step 3: trace を確認

```bash
curl -s http://127.0.0.1:8000/v1/trace/ops-review-session-001
```

期待:
- `event_count >= 1`
- `events[*].event_type` に `DecisionEmitted` または ESCALATE 判定由来イベントが含まれる

### Step 4: human decision を送る

`<REVIEW_ID>` は Step 2 で取得した値に置き換える。

```bash
curl -s -X POST http://127.0.0.1:8000/v1/review/<REVIEW_ID>/decision \
  -H 'Content-Type: application/json' \
  -d '{"decision":"approve","reviewer":"ops-oncall","comment":"manual verification complete"}'
```

期待:
- HTTP 200
- `item.status=decided`
- `item.decision=approve`

### Step 5: `HumanReviewDecided` が trace に残る

```bash
curl -s http://127.0.0.1:8000/v1/trace/ops-review-session-001
```

期待:
- `events[*].event_type` に `HumanReviewDecided` が含まれる

### Step 6: 再起動後の永続化を確認

1. サーバ停止
2. 同じ環境変数・同じ DB パスで再起動
3. 以下を確認

```bash
curl -s http://127.0.0.1:8000/v1/review/pending
curl -s http://127.0.0.1:8000/v1/trace/ops-review-session-001
curl -s 'http://127.0.0.1:8000/v1/trace/history?limit=10'
```

期待:
- 決定済みであれば pending 件数は 0（対象セッションは pending から消える）
- `/v1/trace/ops-review-session-001` で `HumanReviewDecided` を再取得できる
- `/v1/trace/history` に `ops-review-session-001` が残る

## 5. 回帰防止で担保している自動テスト

- `tests/integration/test_observability_review_flow.py`
  - ESCALATE → pending → trace → decision → HumanReviewDecided → 再初期化後の trace/history/review 永続化を一気通貫で固定。
- `tests/unit/test_rest_api.py::test_review_decision_increments_trace_event_count`
  - human decision 時に trace event が 1 件追加されることを固定。

## 6. まだ手動で確認すべき点

- 実運用の入力で ESCALATE が十分に発生するか（ポリシー/モデル設定依存）
- SSE/WS クライアントでの UI 表示・オペレーター導線（本 runbook は HTTP API 検証中心）
- 高負荷時の review キュー運用（件数上限・運用アラート・オンコール手順）
