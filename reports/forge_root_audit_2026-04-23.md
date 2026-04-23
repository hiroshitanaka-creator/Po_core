# ForgeRoot 総合技術評価レポート

## 1. エグゼクティブサマリー
- 本リポジトリは、2系統の実行基盤を同居させています。
  - `src/pocore/*` は決定性重視のケース実行パイプライン（`run_case_file`）です。
  - `src/po_core/*` は REST/CLI/非同期実行を含む本番向けプラットフォームです。
- 技術スタックは Python 3.10+、FastAPI、Pydantic v2、SlowAPI、SQLAlchemy、Torch、Transformers、Dash/Plotly などです。
- 総合評価: **84 / 100**
  - 強み: セキュリティ初期値（fail-closed auth, startup fail-fast）、テスト層の厚み、責務分離。
  - 懸念: 決定性モデル（`pocore`）と非決定ランタイム（`po_core`）の併存による運用複雑性、広域例外握りつぶし箇所、メモリ/永続ストア一部でスレッド安全性に余地。

## 2. アーキテクチャと設計の評価
- エントリーポイント
  - パッケージCLI: `po-core`, `po-self`, `po-trace`, `po-interactive`, `po-experiment` が `pyproject.toml` に定義されています。
  - REST実行: `python -m po_core.app.rest` は `uvicorn` で `po_core.app.rest.server:app` を起動します。
- 設計の良い点
  - `src/pocore/orchestrator.py` は parse→engines→trace→compose の責務が明確。
  - `src/po_core/app/api.py` は facade として機能し、内部実装依存の直接露出を避けています。
  - `src/po_core/runtime/settings.py` は設定集中管理で、環境切替を入口で吸収しています。
- 設計上の負債
  - `src/pocore/*` と `src/po_core/*` の二重系統が存在し、仕様境界を知らない開発者が誤った実装面を変更しやすい構造です。
  - Legacy API (`src/po_core/app/api.py` の `app`) を残しつつ新REST系が存在し、認証/運用ポリシーの一貫性を常時検証しないとドリフトしやすいです。

## 3. コード品質と保守性
### 【Good】
- スキーマ検証が入出力で明示され、失敗時の詳細メッセージも整備されています。
- RESTサーバ起動時に auth misconfig / 実行モード / sqlite+multi-worker を fail-fast で拒否する防御設計が入っています。
- 認証は `skip_auth`・APIキー未設定・不一致を状態分離して扱っており、HTTP 503/401 を明確に返します。
- ベンチマークテストが性能目標をコード化しており、回帰検知の運用がしやすいです。

### 【Bad/技術的負債】
- 例外握りつぶし
  - `src/po_core/ensemble.py` で `ExplanationEmitted` 生成失敗時に `except Exception: pass` があり、監査ログ欠落が静かに発生し得ます。
- 非決定性の混在
  - `src/po_core/app/rest/routers/reason.py` と `src/po_core/app/api.py` で `uuid4` や `datetime.now()` を使用。`pocore` の deterministic 契約と思想が異なり、テスト/監査観点で混同リスクがあります。
- 互換層の複雑化
  - Legacy surface の維持は移行容易性に寄与する一方、セキュリティ設定の二重管理ポイントとなります。

## 4. セキュリティとパフォーマンスのリスク
- セキュリティ（評価）
  - APIキー未設定時 fail-closed（起動拒否・503）を実装しており、公開APIとして良好。
  - WebSocket は query API key を既定拒否し、明示opt-in時のみ許可するため、漏えいリスクを抑制。
  - SQL層は SQLAlchemy ORM/SQLite parameter binding を使用しており、文字列連結SQL注入の典型パターンは確認されませんでした。
- セキュリティ（懸念）
  - API key 比較は通常比較（定数時間比較ではない）で、理論上タイミング差分攻撃面は残ります（実務上はTLS前提・ネットワークノイズで低リスクだが改善余地）。
  - 一部 broad exception により、障害の観測性低下→検知遅延のセキュリティ運用リスクがあります。
- パフォーマンス（評価）
  - `tests/benchmarks/*` で p50/p90/目標値を定義し、RESTオーバーヘッド評価まで含む点は高評価。
- パフォーマンス（懸念）
  - `append_trace_event()` は毎回 `get` + 全件 `save` の再書き込みで、イベント数増大時に O(n^2) 的コストを招く可能性があります。
  - in-memory WS rate log は prune 実装ありだが、極端なIP分散攻撃時には辞書キー膨張の余地が残ります。

## 5. 改善のためのネクストアクション（優先順位順）
1. [Highest] **例外握りつぶしの解消と監査イベント保証**
   - `except Exception: pass` をやめ、構造化ログ＋失敗イベントを emit して可観測性を担保。
2. [Medium] **認証比較のハードニング**
   - API key 比較を `hmac.compare_digest` に置換し、ヘッダ解決・認可判定の一貫テストを追加。
3. [Low] **トレース追記の計算量改善**
   - `append_trace_event` を差分追記SQLへ変更し、長時間セッションでの再書き込みコストを削減。

