# Status Snapshot (A〜F)

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：このファイル（[docs/status.md](/docs/status.md)）

公開手順（再現可能Runbook）：[docs/operations/publish_playbook.md](/docs/operations/publish_playbook.md)

この文書は、A〜Fおよび Phase9〜12 反映後の状態を会話コンテキスト非依存で固定するためのスナップショット。

## Completed
- **A**: 入力正規化として `features` 抽出レイヤを導入し、case固有分岐増殖を抑制した。
- **B**: recommendation裁定閾値を `policy_v1` に集約し、裁定ロジックを決定論で一元化した。
- **C**: trace（generic）に `unknowns_count` / `stakeholders_count` / `days_to_deadline` 観測値を追加し、監査性を強化した。
- **D**: ethics guardrails v1 を拡張しつつ、recommendation裁定への非干渉（非介入）契約を明文化した。
- **E**: recommendationの裁定経路を `arbitration_code` として保持できるようにし、裁定理由の可観測性を上げた。
- **F**: ethicsをruleset化し、`rule_id` と `rules_fired` により「どの規則が発火したか」を追跡可能にした。

## CI Fixes
- **ci-fix-black**: `pyproject.toml` の `black==23.12.1` を `26.1.0` に統一し、CI lint ジョブと `.pre-commit-config.yaml` のバージョンを一致させた（コミット #379 のダウングレードを修正）。

## Meta (Docs Governance)
- **Phase13-PR-2**: legacy `pocore` 契約メタデータのバージョン整合を実施。`src/pocore/orchestrator.py` の `POCORE_VERSION` を `0.3.0` 方針へ更新し、凍結契約（`case_001` / `case_009`）は `scenario_profile` ベースで `0.1.0` を維持。非凍結 golden の `meta.pocore_version` / `meta.generator.version` は `0.3.0` へ同期した。
- **Phase13-PR-3**: policy override と execution coverage を整合。`src/pocore/orchestrator.py` に policy override 互換（`UNKNOWN_BLOCK` / `TIME_PRESSURE_DAYS`）を維持しつつ trace `policy_snapshot` を同一閾値で記録するよう修正し、`scripts/policy_lab.py` の一時 override 実行中に planning・recommendation 判定と整合する状態へ改善した。
- **Phase13-PR-1**: `docs/status.md` を現実の main 状態へ再同期し、Phase9〜12・`0.3.0` 到達点・公開運用証跡（publish playbook / acceptance proof / PyPI publish evidence）との整合を更新した。
- **Phase11-prep-1**: TestPyPI `0.3.0` の evidence 本体は未作成（template only / evidence pending: outbound access `HTTP 403`）。`docs/release/templates/testpypi_publish_log_template_v0.3.0.md` を追加した。
- **Phase11-prep-2**: 2026-03-08 に TestPyPI evidence 昇格可否を再検証したが、`python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==0.3.0` は `ProxyError: Tunnel connection failed: 403 Forbidden` で失敗し、GitHub Actions workflow URL 取得（`curl -I -L https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml`）も `CONNECT tunnel failed, response 403` のため、evidence 本体は未作成のまま。
- **Phase12-PR-1**: PyPI公開とスモーク検証の証跡を固定。`docs/release/pypi_publish_log_v0.3.0.md` を追加し、workflow URL / PyPI URL / `pip install po-core-flyingpig==0.3.0` / import smoke + `run()` 最小呼び出し例を記録した。
- **Phase10-PR-1**: CHANGELOGのUnreleased項目を `0.3.0` release sectionへ切り出し、Unreleasedを空（No unreleased changes）に戻した。
- **Phase9-PR-3**: deliberation scaling benchmark（`tests/benchmarks/test_pipeline_perf.py::test_bench_deliberation_scaling`）のしきい値を、実測（複数回計測で rounds=3 p50 が概ね 0.84–0.87s）に基づく根拠付き定数 `max(r1 * 4.0, 0.95)` へ見直し。scheduler/CI jitter によるフレークを抑えつつ、退行検知感度を維持。
- **Phase13-PR-4**: deliberation scaling benchmark（`tests/benchmarks/test_pipeline_perf.py::test_bench_deliberation_scaling`）の計測手法を安定化。`stable-p50`（複数バッチのp50中央値）を導入し、判定しきい値 `max(r1 * 4.0, 0.95)` を維持したままCI jitter由来のフレークを抑制して回帰検知感度を保った。
- **Phase9-PR-1**: pytest設定の単一真実化（pytest.ini）を完了。
- **Phase9-PR-2**: policy_lab/coverageの定数参照を動的化し、テストを安定化。
- **Phase8-PR-1**: publish playbook（`docs/operations/publish_playbook.md`）を追加し、publish.yml の TestPyPI→PyPI 手順と失敗時ロールバックを再現可能な運用手順として固定した。
- **Phase6-PR-2**: acceptance must-pass（`pytest tests/acceptance/ -v -m acceptance`）のgreen実行証跡をrepo内に固定した（acceptance proof: `docs/release/acceptance_proof_v0.3.0.md`）。
- **Phase6-PR-4**: OpenAPIライセンス表記をAGPL+Commercialに修正し、OpenAPI description にライセンスリンクを追加した。
- **Phase6-PR-3**: 42人表記へ統一した。
- **Phase6-PR-1**: バージョン表記を0.3.0へ統一し、OpenAPI license表示をAGPL-3.0-or-later + Commercialへ更新した（acceptance proof: `docs/release/acceptance_proof_v0.3.0.md`）。
- **Phase7-PR-1**: PRD（`docs/spec/prd.md`）のStatus/Package/人数/マイルストーンを`docs/status.md`と現行実装（v0.3.0・42人・M0/M1完了）に整合させた。
- **Phase5-PR-2**: PR本文ガバナンスチェックを追加し、SSOT確認・進捗更新・テスト報告・影響範囲記載を pull_request 時に検査するようにした。
- **Phase5-PR-1**: PRテンプレを追加し、SSOT確認・進捗更新・テスト報告・影響範囲記載を要求するようにした。
- **Phase4-PR-1**: 創発比較スクリプトを追加し、議論あり/なしの比較計測（avg_novelty 集計修正と回帰テスト固定を含む）を可能にした。
- **Phase3-PR-2**: SolarWillのWARN/CRITICAL縮退をテストで凍結した。
- **Phase3-PR-1**: SolarWillの宇宙ルール倫理（NORMAL）をテストで凍結した。
- **Phase2-PR-2**: G-2（stakeholders外部性）goldenを追加し観測境界を固定した。
- **Phase2-PR-1**: G-1（unknowns×deadline）golden追加に加え、acceptanceのnow基準を決定論で固定してgolden腐敗（日次ドリフト）を防止した。
- **Phase 0 (docs)**: `docs/厳格固定ルール.md` をSolarWill公理（歪み/例外/NORMAL-WARN-CRITICAL）に整合させ、主要文書の導線を統一した。
- **Phase1-PR-1**: Manifestoファイル名をPo_core_Manifesto_When_Pigs_Fly.mdへ改名し、全参照を更新した。
- **Phase1-PR-2**: 旧Manifesto参照（URLエンコード含む）を全掃討し、参照0件を保証した。

## Contracts
- **最優先ルール**: `docs/厳格固定ルール.md` を参照（これに反する変更は禁止）。
- **凍結golden**: `scenarios/case_001_expected.json` / `scenarios/case_009_expected.json` は凍結契約（改変禁止）。
- **決定性**: 同一入力 + 同一 `seed` + 同一 `now` + 同一バージョンで出力JSON完全一致（wall-clock/乱数禁止）。
- **golden更新手順**: 仕様根拠（ADR/SRS）を先に固定し、決定論パラメータで生成→保存→`pytest -q` 全通を確認する。
- **責務境界**:
  - `features` は観測のみ（判断を入れない）
  - `engines` はルール判定と生成
  - `recommendation` は最終裁定の単独責務
  - `ethics` はガードレール/トレードオフ提示（裁定はしない）

## M4 Governance (2026-03-08 完了)

- **M4-PR**: `.github/PULL_REQUEST_TEMPLATE.md`（大文字）を `pull_request_template.md` と統一。全セクションをガバナンス準拠形式に更新し、重複テンプレート問題を解消した。
- **M4-REQ**: `scripts/check_pr_governance.py` に M4ゲートを追加。実質的な変更PRに対し `REQ-xxx-001` / `NFR-xxx-001` / `FR-xxx-001` 形式の要件ID参照を必須化した（NFR-GOV-001 準拠）。
- **M4-STATUS**: 既存の CI `jsonschema` 必須ゲート（schema-gate job）・`update_traceability.py --check`・`calc_traceability_coverage.py --min-at 8`・`pr-governance.yml` ワークフローはすべて実装済みを確認。

M4 完了基準「PR マージ時に自動で Traceability チェックが走る」→ ✅ 充足。

## Legacy Test Migration (2026-03-09)

大規模レガシーテスト移行を実施。3534 passed / 134 skipped → **3682 passed / 0 skipped**（+148 tests, −134 skips）。

- **cli-click-PR**: `src/po_core/cli/commands.py` 新規追加。Click ベース非インタラクティブ CLI（`hello` / `status` / `version` / `prompt` / `log`）を実装。`test_cli.py` 16 件パス化。
- **potrace-fix**: `PoTrace.log_event()` がイベントIDを返すよう修正・存在しないセッションに対し `ValueError` を raise するよう修正。`update_metrics()` も同様。`test_po_trace.py` 28 件パス化。
- **philosophers-legacy**: テストの 3 件の誤ったアサーション（`🧠` emoji、`temporal_dimension["has_past"]`、Sartre description のタイポ）を修正。16 件パス化。
- **potracedb-fix**: `test_po_trace_db.py` の `EventType.ENSEMBLE_STARTED`（非存在）→ `EXECUTION` へ修正、`philosophers` key チェックを `session_id` へ修正。21 件パス化。
- **visualization-update**: `test_visualizations.py` の唯一のスキップ（`test_visualizer_with_po_self_session`）を InMemoryTracer ベースの現行 API テストに書き換え。1 件パス化。
- **po-viewer-rewrite**: `test_po_viewer.py` を `PoViewer.from_run(prompt)` の現行 API に完全書き換え（25 件 → 24 件）。全件パス化。
- **prototypes-migration**: `test_prototypes.py`（26 件）を examples/ の現行 API（`BatchAnalyzer.po` / `AnalysisResult` dataclass / `export_json(filepath)` / `export_csv(filepath)` / `session_store`）に移行。26 件全通パス化。
- **nietzsche-fix**: `_check_eternal_recurrence` の条件順序を修正（reject を affirm より先にチェック）。"never again" を含む文が誤って "Passes" と判定される単語マッチ bug を解消。`test_nietzsche.py` 1 件パス化（58 件、0 スキップ）。

残存スキップ（0 件）：全スキップ解消。

## Next
- **Snapshot sync policy**: `docs/status.md` は main の実態同期を優先し、完了済み項目を Next に残置しない。
- **Open follow-up（運用上の未解消）**: TestPyPI 側の外部接続制限（HTTP 403）により evidence 本体は未作成のまま。PyPI `0.3.0` 公開証跡・acceptance proof・publish playbook は整備済み。

## Deliberation Protocol v1 (PR-4)
- 新しい内部プロトコル `Propose -> Critique -> Synthesize` を `src/po_core/deliberation/protocol.py` に追加。
- feature flag `PO_DEBATE_V1=1` 時、Ensemble/PartyMachine 内部で protocol v1 を実行し、最終出力互換を維持したまま相互批判の観測が可能。
- synthesis report は `open_questions` と `disagreements` を含み、批判フェーズが空になりにくいようにデフォルト批判ルールを実装。
