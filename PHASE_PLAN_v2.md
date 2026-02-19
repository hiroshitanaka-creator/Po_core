# Po_core 完全体ロードマップ — Phase 1〜5

> Grand Architect Assessment — 2026-02-10 策定
> **現在地更新 — 2026-02-19**
>
> 前提: Phase 0〜4（PhilosopherBridge, E2E Test, Pipeline Integration, Tensor Deepening, Production Readiness）は完了済み。
> 本文書は「次の5フェーズ」として、Po_coreを完全体へ導くための戦略的ロードマップである。

---

## 現在地（2026-02-19 時点）

**Phase 1〜4 および Phase 5-A/B/C が完了。** Phase 5-D/E/F が残課題。

| フェーズ | 状態 | 完了サマリー |
|---|---|---|
| Phase 1: 基盤固め | ✅ COMPLETE | 39人スケール検証・技術負債清算・テスト基盤整備 |
| Phase 2: テンソル知性 | ✅ COMPLETE | sentence-transformers Semantic Delta・Interaction Tensor・Deliberation Engine |
| Phase 3: 可視化 | ✅ COMPLETE | Dash WebUI 4タブ・ExplanationChain・リアルタイムリスナー |
| Phase 4: 防御強化 | ✅ COMPLETE | PromptInjectionDetector・85件 Red Team・全14件 green |
| Phase 5-A: REST API | ✅ COMPLETE | FastAPI 5ルート・認証・レート制限・SSE |
| Phase 5-B: セキュリティ | ✅ COMPLETE | CORS・SlowAPI・pydantic-settings |
| Phase 5-C: Docker | ✅ COMPLETE | multi-stage Dockerfile・docker-compose.yml |
| Phase 5-D: 真の非同期 | 🔲 PENDING | SSEはthreadpool経由で動作中。async PartyMachine未実装 |
| Phase 5-E: ベンチマーク | 🔲 PENDING | アドホック計測 ~30ms。正式スイート未作成 |
| Phase 5-F: PyPI公開 | 🔲 PENDING | publish.yml 準備済み。TestPyPI/PyPI 公開未実施 |

---

## 現状診断（Status Quo）

> ⚠️ 下記の成熟度マトリクスは **2026-02-10 策定時点**の値です。
> **2026-02-19 現在の値**は括弧内に記載。

### モジュール成熟度マトリクス

| モジュール | 策定時 | 現在 | 変化の根拠 |
|---|---|---|---|
| 39哲学者フレームワーク | 8/10 | **9/10** | Voice Layer 39本（YAML+VoiceRenderer）追加。propose()のvoice上書きバグ修正（2026-02-19）|
| W_Ethics Gate | 8/10 | **9/10** | Phase 4: PromptInjectionDetector・EnglishKWDetector v0.2・obfuscation正規化。injection/jailbreak 100%検出 |
| Freedom Pressure テンソル | 5/10 | **6/10** | 6D構造は維持。well-tested。ML化は未着手 |
| Semantic Delta | 4/10 | **7/10** | sentence-transformers実装完了。multi-backend（sbert/tfidf/basic）・encode_texts() API |
| Interaction Tensor | 2/10 | **8/10** | NxN harmony（cosine類似度）+ tension（対立キーワード）+ synthesis 完成。InteractionPair・high_interference_pairs() |
| Semantic Profile | 2/10 | **4/10** | マルチターン追跡の基盤は存在。深化は未着手 |
| 合意形成エンジン（Deliberation Engine）| 5/10 | **8/10** | 多ラウンド議論完成。Round1→高干渉ペア特定→counterargument→re-propose。RoundTrace・n_revised追跡 |
| Viewer | 6/10 | **8/10** | Dash WebUI 4タブ（Pipeline/Philosophers/W_Ethics/Deliberation）。ExplanationChain・リアルタイムリスナー |
| REST API | 0/10 | **7/10** | FastAPI 5ルート実装。X-API-Key認証・SlowAPI・SSE streaming |
| ストリーミング | 2/10 | **5/10** | SSEはthreadpool経由で動作。true async PartyMachine未実装 |
| テストカバレッジ | 5/10 | **7/10** | 1,359+ テスト・91ファイル。pipeline marker CI必須 |
| Red Team テスト | 3/10 | **8/10** | 56件redteam・29件phase4・85件合計。攻撃検出率≥85%・偽陽性≤20%。全14件green |

### 技術的負債（策定時 → 現在）

| 負債 | 状態 |
|---|---|
| レガシーテスト197件の移行（`run_ensemble` → `run_turn`）| ✅ Phase 1で解消 |
| `PhilosopherBridge`二重インターフェース除去 | ✅ Phase 1で解消 |
| sentence-level semantic delta未実装 | ✅ Phase 2で解消 |
| Golden regression テスト不足 | ✅ Phase 1/2で整備 |
| Interaction Tensor / Semantic Profile 未完成 | ✅ Phase 2で解消（Semantic Profileは基盤のみ）|
| Voice Layer が propose() の content を上書き（deliberation破壊）| ✅ 2026-02-19 修正済み |

---

## Phase 1: 「39賢人の共鳴調整＋技術的負債の清算」 ✅ COMPLETE

**英名:** Resonance Calibration & Foundation Settlement

**完了サマリー（2026-02-19）:** レガシー197テスト移行・PhilosopherBridge除去・39人同時実行検証・
Freedom Pressure / W_Ethics Gate スケーリング調整・哲学者意味的ユニーク度評価。2354テスト。

### 焦点
39人規模での安定動作の保証と、積み残した技術的負債の一括清算。

### 具体的タスク

#### 1.1 レガシーテスト移行とテスト基盤強化
- 197件のレガシーテスト（`run_ensemble`ベース）をトリアージし、有効なものを`run_turn` / `po_core.run()`ベースに移行。不要なものは削除。
- `@pytest.mark.slow` マーカーの付与（現在0件）。CIでの高速/低速テスト分離を可能に。
- テストカバレッジ目標を60%以上に設定し、`.coveragerc`に閾値を明記。

#### 1.2 PhilosopherBridge二重インターフェース除去
- 39人全員を`PhilosopherProtocol.propose()`ネイティブ実装に移行。
- `PhilosopherBridge`アダプタを削除し、レジストリを簡素化。
- これにより、哲学者モジュールのコードパスが一本化され、デバッグ・プロファイリングが容易に。

#### 1.3 39人同時実行の負荷・安定性テスト
- `test_all_39_philosophers.py`を拡張し、NORMAL/WARN/CRITICALモードでの39人同時実行を検証。
- メモリ消費量・レイテンシのベースラインを計測し、回帰テストに組み込む。
- `PartyMachine`の ThreadPoolExecutor（12 workers）で39人を処理した際のタイムアウト・デッドロックの有無を確認。

#### 1.4 Freedom Pressure / Ethics Gate の39人スケーリング調整
- 20人→39人でパレート最適化の重み付けがどう変化するか計測。
- `battalion_table.py`のNORMALモード設定（現在39人全員参加）の妥当性を検証。
- `W_Ethics Gate`の`tau_reject` / `tau_escalate`閾値が39人規模で適切か確認。合意が得にくくなる（沈黙問題）か、逆に安全バイアスが薄まる（暴走問題）かを両方テスト。

#### 1.5 各哲学者の「らしさ」定性評価
- `test_comprehensive_layers.py`（229テスト、4レイヤー）の結果を分析し、哲学者間の出力が均質化していないか確認。
- 特にリスクレベル2の哲学者（Nietzsche, Foucault, Deleuze等）がリスクレベル0の哲学者に「埋没」していないか検証。
- 各哲学者のセマンティックプロファイルのユニーク度をメトリクス化。

### なぜこの項目か

**理由1: 不安定な基盤の上に何を積んでも崩壊する。**
レガシーテスト197件が未移行ということは、コードの約40%が検証されていない旧パイプラインに依存している。この状態で新機能を追加すると、回帰バグの温床になる。

**理由2: 二重インターフェースは認知的負荷を倍増させる。**
`reason()` と `propose()` の二重コードパスは、以降のすべてのPhaseにおけるデバッグコストを増大させる。Phase 1で一本化すれば、Phase 2以降の生産性が飛躍的に向上する。

**理由3: 39人スケーリングは「未知の未知」。**
個別テストが通っていても、39人が同時に動いた際の創発的挙動（emergent behavior）は予測不能。ユーザー案と同じく、この検証なしに先へ進むのは危険。

### なぜこの順番か

Phase 0〜4で整備された環境の「最後の仕上げ」として、技術的負債を完全に清算してからPhase 2に進む。哲学者の出力品質が担保されていなければ、Phase 2のテンソル強化もPhase 3の可視化も意味をなさない。

### ユーザー案との差異

ユーザー案のPhase 1「39賢人の共鳴調整」は本質的に正しい。しかし、**技術的負債の清算を含めていない点が弱い**。レガシーテスト移行とPhilosopherBridge除去を同時に行わなければ、「共鳴調整」の結果を信頼できるテスト基盤で検証することができない。

---

## Phase 2: 「テンソル知性と創発エンジン」 ✅ COMPLETE

**英名:** Tensor Intelligence & Emergence Engine

**完了サマリー（2026-02-19）:** sentence-transformers Semantic Delta（multi-backend）・
InteractionMatrix（NxN harmony/tension/synthesis）・DeliberationEngine（多ラウンド再提案）実装。2396テスト。

### 焦点
キーワードベースのテンソル計算をMLベースに進化させ、哲学者間の「真の対話」メカニズムを構築する。

### 具体的タスク

#### 2.1 Sentence-Transformer Semantic Delta
- 現在のトークンオーバーラップ（Jaccard類似度）を`sentence-transformers`（`all-MiniLM-L6-v2`、既にrequirements.txtに存在）によるコサイン類似度に置換。
- 戻り値の`(str, float)`シグネチャは維持し、後方互換を保つ。
- 日本語対応: `paraphrase-multilingual-MiniLM-L12-v2`の検討。

#### 2.2 Interaction Tensor 完成
- 現在フレームワークのみ（成熟度2/10）のInteraction Tensorに計算ロジックを実装。
- 哲学者ペア間の「干渉」（interference）を定量化: 同意・対立・無関係の3状態。
- `test_comprehensive_layers.py`のLayer 3（Tension/Contradiction テスト）と連携。

#### 2.3 Semantic Profile マルチターン追跡
- 会話全体にわたるセマンティックプロファイルの変化を追跡。
- 「議論がどの方向に進化しているか」をベクトル空間上で可視化可能に。
- `TensorEngine`への`MetricFn`プラグインとして実装。

#### 2.4 真の議論メカニズム（Deliberation Engine）
- **現状の問題**: 39人の哲学者は独立に応答し、Pareto集約で「勝者」が選ばれるだけ。哲学者同士が「反論」「修正」「統合」する仕組みがない。
- **実装案**:
  - Round 1: 全哲学者が独立に`propose()`。
  - Round 2: Interaction Tensorで高干渉ペアを特定し、そのペアに「相手の提案を踏まえた再提案」を要求。
  - Round 3: 修正された提案群をPareto集約。
- これにより「議論による創発（Emergence through Deliberation）」が初めて実現する。
- `max_rounds`パラメータで制御し、パフォーマンスとのトレードオフを明示。

### なぜこの項目か

**理由1: テンソルがキーワードベースでは「哲学」ではなく「テキスト処理」。**
Freedom Pressureが「自由」「責任」「選択」といったキーワードの出現頻度で計算されている現状は、哲学的深みに欠ける。sentence-transformersによる意味的類似度は、最低限の「理解」をシステムに与える。

**理由2: 39人が独立に喋るだけでは「創発」は起きない。**
Po_coreの最大の差別化要因は「複数哲学者による創発的意味生成」だが、現在の実装はただの「39並列 → 投票」。これは39人の委員会が各自メモを書いて投票するのと同じで、議論（deliberation）ではない。Interaction TensorとDeliberation Engineの組み合わせが、このシステムのコア価値を実現する。

**理由3: Phase 3の可視化に「見るべきもの」を提供する。**
テンソルが粗雑なままでは、Phase 3でViewerを作っても「キーワードカウントのグラフ」しか表示できない。MLベースのテンソルと議論ラウンドの存在が、可視化を意味のあるものにする。

### なぜこの順番か

Phase 1で39人の安定動作と品質が確認された後でなければ、テンソル計算の改善は「ガベージイン・ガベージアウト」になる。また、Phase 3（可視化）やPhase 4（レッドチーム）は、このPhaseで強化されたテンソルデータを前提とする。

### ユーザー案との差異

**ユーザー案にこのPhaseは存在しない。** これが最大の差分であり、最も重要な追加提案。ユーザー案のPhase 2（可視化）に直接進むと、「見えるようにはなったが、見るべきものが浅い」という事態に陥る。真の創発メカニズムの構築は、可視化の前に行うべきである。

---

## Phase 3: 「内部状態の完全可視化と説明可能性」 ✅ COMPLETE

**英名:** Observability, Explainability & Viewer Integration

**完了サマリー（2026-02-19）:** Dash WebUI 4タブ・ExplanationChain・build_explanation_from_verdict()・
InMemoryTracer リスナー機構・Deliberation ラウンドチャート・InteractionMatrix ヒートマップ。34テスト。

### 焦点
Phase 2で強化されたテンソルと議論メカニズムを、開発者が直感的に理解できる形で可視化する。

### 具体的タスク

#### 3.1 Viewer WebUI化
- 現在のテキスト/Markdown出力を、ブラウザベースのインタラクティブダッシュボードに拡張。
- 技術選定: `viewer/`モジュールが既にRich, Matplotlib, Plotly, NetworkX, Seaborn, Bokehに依存 → **Plotly Dash** または **Streamlit** を採用し、既存の可視化関数をラップ。
- 最小構成: テンソル時系列グラフ + 哲学者参加マップ + パイプラインステップ追跡。

#### 3.2 議論プロセスの可視化
- Phase 2のDeliberation Engineのラウンド進行を、議論グラフ（Argument Graph）として表示。
- `evolution_graph.py` と `tension_map.py` をInteraction Tensorと接続。
- 「どの哲学者の影響で結論がどう変化したか」を追跡可能に。

#### 3.3 W_Ethics Gate 説明可能性（Explainable AI）
- Gateの判定（ALLOW / ALLOW_WITH_REPAIR / REJECT / ESCALATE）に対し、**根拠チェーン**を生成。
- 「なぜ却下されたか」だけでなく、「どのポリシーが、どのエビデンスに基づいて、どの閾値で発火したか」を構造化JSON + 自然言語で出力。
- `GateResult`に`explanation`フィールドを追加し、TraceEventとして記録。

#### 3.4 トレースのリアルタイムストリーミング
- `InMemoryTracer`をイベントバス（`asyncio.Queue`ベース）に拡張し、Viewerへのプッシュ型配信を可能に。
- パイプライン実行中に「今どのステップを実行中か」をリアルタイムで表示。

### なぜこの項目か

**理由: 複雑系のデバッグには「観測」が不可欠。**
ユーザー案の指摘通り、Viewerは「単なるUI」ではなく「最強のデバッグツール」。Phase 2で追加された議論メカニズムとMLテンソルは、可視化なしには正しく機能しているか判断できない。

### なぜこの順番か

Phase 2でテンソルの知性と議論メカニズムが揃った後に可視化することで、表示されるデータが意味のあるものになる。また、Phase 4（レッドチーム）では「攻撃を受けた際にシステム内部で何が起きたか」を分析する必要があり、この可視化基盤が前提となる。

### ユーザー案との差異

基本的にユーザー案のPhase 2と同じ方向性。差分は:
1. Phase 2（テンソル知性）を挟んだことで、可視化対象のデータがリッチになっている。
2. WebUI化の技術選定を具体化（Plotly Dash / Streamlit）。
3. W_Ethics Gateの説明可能性を「explanation chain」として構造化。

---

## Phase 4: 「倫理的堅牢化とレッドチーミング」 ✅ COMPLETE

**英名:** Adversarial Hardening & Ethical Stress Testing

**完了サマリー（2026-02-19）:** PromptInjectionDetector（injection/jailbreak 100%検出）・
EnglishKWDetector v0.2・IntentionGate obfuscation正規化・85件 Red Team テスト（全14件 green）・
CI防御メトリクス自動化（≥85%検出・≤20%偽陽性）。※LLMベースDetectorは未着手。

### 焦点
Phase 3で可視化された内部状態を武器に、悪意ある入力に対する防御力を体系的に検証・強化する。

### 具体的タスク

#### 4.1 レッドチームテストの体系的拡充
- 現在2ファイル（`test_prompt_injection.py`: 7テスト、`test_goal_misalignment.py`: 7テスト）+ 4実験ファイルを、以下のカテゴリに体系化:
  - **Prompt Injection**: 直接注入、間接注入、エンコーディング攻撃、多言語攻撃
  - **Jailbreak**: ロールプレイ型、DAN型、段階的エスカレーション型
  - **Goal Misalignment**: セマンティックドリフト、隠れたアジェンダ、意図-目標不一致
  - **Ethics Boundary**: 倫理的グレーゾーン（トロッコ問題的二律背反）
  - **Philosopher Exploitation**: 特定哲学者（リスクレベル2）を悪用してゲートを迂回する試行
- 最低50テストケースを目標。

#### 4.2 W_Ethics Gate エッジケース検証
- `wethics_gate/policies/`の6ポリシーすべてに対し、境界値テストを実施。
- `tau_reject` / `tau_escalate` 閾値の直上・直下での挙動を検証。
- 修復（Repair）が意味を変えてしまうケース（セマンティックドリフト偽陰性）の検出。
- **LLMベースのDetector導入検討**: 現在はルールベースのみ。コードに「in production, swap with LLM」というコメントが存在する。このフェーズでプロトタイプを作成。

#### 4.3 39人哲学者の倫理的グレーゾーン応答テスト
- 「倫理的に正解がない問い」（安楽死、AI権利、集団的自衛権等）に対し、39人がどう反応し、システムとしてどう結論を出すかを記録・分析。
- Phase 2のDeliberation Engineにより、哲学者間で実際に議論が発生するため、**議論の過程そのもの**がテスト対象となる。
- 「安全すぎる沈黙」と「危険な暴走」の間の適切な応答バンドを定義。

#### 4.4 防御メトリクスの自動化
- Phase 3のViewer + Trace基盤を活用し、攻撃テスト結果をダッシュボードで自動集約。
- 「攻撃成功率」「検出率」「修復成功率」「偽陽性率」をCI上で自動計測。
- 回帰テストとして組み込み、新コードが防御力を劣化させていないことを保証。

### なぜこの項目か

**理由: 「責任ある意味生成」がPo_coreの存在意義。**
ユーザー案と完全に同意。倫理ゲートが脆弱であれば、39人の哲学者も、美しいテンソルも、すべてが「責任のないおしゃべり」に堕する。

### なぜこの順番か

Phase 3で可視化基盤が整っているため、攻撃を受けた際に「どのテンソルが反応したか」「どの哲学者が暴走したか」「Gateのどの段階で検出/見逃しが起きたか」を詳細に分析できる。ブラインドでの防御強化は非効率。

### ユーザー案との差異

方向性は完全に一致。追加点:
1. Phase 2のDeliberation Engineを前提とした「議論過程テスト」が可能になっている。
2. LLMベースDetectorの導入を具体的に提案。
3. 防御メトリクスのCI自動化を含む。

---

## Phase 5: 「製品化と世界への配布」 🔄 IN PROGRESS

**英名:** Productization, API & Delivery

### 焦点
安全で知的で透明なシステムを、世界中の開発者が使える形にパッケージングする。

### 具体的タスク

#### 5.1 FastAPI REST API 実装 ✅ COMPLETE（Phase 5-A）
- 実装済みエンドポイント（`src/po_core/app/rest/`）:
  - `POST /v1/reason` — 同期推論
  - `POST /v1/reason/stream` — SSE ストリーミング
  - `GET /v1/philosophers` — 39人マニフェスト
  - `GET /v1/trace/{session_id}` — セッション別トレース
  - `GET /v1/health` — ヘルスチェック
- OpenAPI / Swagger自動生成済み（FastAPI標準）。
- `X-API-Key` 認証（`PO_API_KEY` 環境変数）。24ユニットテスト。

#### 5.2 セキュリティ強化 ✅ COMPLETE（Phase 5-B）
- CORS: `PO_CORS_ORIGINS`（デフォルト `"*"`、本番はカンマ区切り）。
- レート制限: SlowAPI + `PO_RATE_LIMIT_PER_MINUTE`（デフォルト 60 req/min/IP）。
- 設定: pydantic-settings `APISettings`（全設定が `PO_` prefix 環境変数で制御）。

#### 5.3 Docker化 ✅ COMPLETE（Phase 5-C）
- multi-stage `Dockerfile`（builder + slim runtime、non-root `pocore` ユーザー）。
- `docker-compose.yml`（named volume + 30秒ヘルスチェック）。
- `.dockerignore`（dev/test/docs を除外）。
- `.env.example`（全環境変数リファレンス）。

#### 5.4 非同期・ストリーミング対応 🔲 PENDING（Phase 5-D）
- 現状: SSE は threadpool 経由で動作（機能はする）。
- 未実装: `PartyMachine` の `async def propose()` 移行（true non-blocking）。
- `InMemoryTracer` のイベントバスを asyncio.Queue ベースに拡張。

#### 5.5 パフォーマンスベンチマーク 🔲 PENDING（Phase 5-E）
- アドホック計測で ~30ms（パイプライン全体）。
- 正式ベンチマークスイート未作成。
- 目標: NORMAL mode 39人で単一リクエスト < 5秒。

#### 5.6 リリース準備 🔲 PENDING（Phase 5-F）
- バージョン `0.2.0-beta` 設定済み（`pyproject.toml`）。
- `.github/workflows/publish.yml`（OIDC trusted publishing）準備済み。
- 残: TestPyPI → PyPI 実際の公開。
- 残: QUICKSTART.md / QUICKSTART_EN.md を REST API 使用例に更新。

### なぜこの項目か

**理由: 「使えないシステム」は「存在しないシステム」と同じ。**
ユーザー案と完全に同意。REST APIが無いことは現状最大のギャップ（0/10）であり、これなしにはライブラリとしてもサービスとしても外部利用が困難。

### なぜこの順番か

堅牢で（Phase 1）、知的で（Phase 2）、透明性があり（Phase 3）、安全な（Phase 4）システムであって初めて、世に出す価値が生まれる。中途半端な状態でAPI公開すると、セキュリティ脆弱性や品質問題が外部に露出するリスクがある。

---

## 全体アーキテクチャの流れ

```
Phase 1         Phase 2           Phase 3          Phase 4         Phase 5
基盤固め    →   知性強化      →   可視化       →   防御強化    →   配布
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
技術負債清算     ML テンソル       WebUI            Red Team        REST API
39人スケール     Deliberation     Explainable AI   Grey Zone       Docker
テスト基盤       Interaction T.   リアルタイム      CI防御指標      Streaming
二重IF除去       Semantic Prof.   Argument Graph   LLM Detector    PyPI
```

---

## ユーザー案との比較総括

| 観点 | ユーザー案 | 本提案 | 差分理由 |
|---|---|---|---|
| Phase数 | 4 (1-4) | 5 (1-5) | Phase 2「テンソル知性」を新規追加 |
| Phase 1 | 39賢人共鳴調整 | +技術負債清算 | レガシー197テスト＋二重IFが未解決のまま進むのは危険 |
| Phase 2 | 可視化 | テンソル知性＋創発 | 可視化の前に「見るべきもの」を充実させる |
| Phase 3 | — | 可視化 | ユーザー案Phase 2を1つ後ろにスライド |
| Phase 4 | レッドチーム | レッドチーム（強化版） | Deliberation Engineの議論過程テスト追加 |
| Phase 5 | 製品化 | 製品化（+API+Streaming） | REST API実装とStreaming対応を明示 |

### 最大の差分: Phase 2「テンソル知性と創発エンジン」の追加

ユーザー案が「可視化 → 防御 → 製品化」と進むのに対し、本提案は「知性強化 → 可視化 → 防御 → 製品化」の順序を取る。

理由は明確: **現在のテンソル計算はキーワードカウントであり、合意形成は並列実行+投票にすぎない**。この状態で可視化しても「39人が独立に喋った結果のキーワード頻度グラフ」が表示されるだけで、「哲学者の対話による意味の創発」は見えない。なぜなら、まだ創発が起きていないから。

Po_coreの存在意義が「AI人格と哲学の融合による創発的意味生成」であるならば、その創発メカニズム（Deliberation Engine + MLテンソル）の実装は、可視化やレッドチームよりも先行すべきである。

---

## リスクと緩和策

| リスク | 影響度 | 状態 |
|---|---|---|
| Phase 2のDeliberation Engineが複雑すぎる | 高 | ✅ `max_rounds=2`で実装・段階的拡張済み |
| sentence-transformerのレイテンシ | 中 | ✅ 起動時ロード + multi-backend fallback（sbert→tfidf→basic）で対処 |
| Phase 1の技術負債清算が予想以上に大きい | 中 | ✅ Phase 1で完全清算済み |
| REST API のセキュリティ | 高 | ✅ Phase 4防御強化後にAPI公開。SlowAPI・CORS・APIキー認証実装済み |
| 39人同時実行のパフォーマンス | 中 | 🔲 Phase 5-E でベンチマークスイート作成予定 |
| Voice Layer が deliberation を破壊するバグ | 高 | ✅ 2026-02-19 修正済み（propose() content 保護） |
| true async 非対応（SSE がthreadpool依存）| 中 | 🔲 Phase 5-D で対処予定 |

---

## 結語

ユーザー案は本質的に正しい方向を向いていた。特に「Phase 1で39人の動作を確認してからPhase 2で可視化」
「可視化の後にレッドチーム」という順序は、複雑系システムの開発として合理的であった。

本提案の核心的な追加「Phase 2: テンソル知性と創発エンジン」は実装された。
Po_coreは「39人の哲学者が独立に喋るシステム」から
「39人が対話し、Deliberation Engine で創発的に意味を生成するシステム」へ進化した。

2026-02-19 現在、残るのは Phase 5-D/E/F のみ。

---

**2026-02-19 時点の現在地:**

> "We don't know if pigs can fly. But we attached a balloon to one to find out."
>
> 気球はついた。風も読んだ（テンソル知性・Phase 2）。
> 内部も見えるようにした（可視化・Phase 3）。
> 悪意にも耐えた（防御強化・Phase 4）。
> 世界に繋がった（REST API・Docker・Phase 5-A/B/C）。
>
> 次は飛ぶ（PyPI公開・真の非同期・Phase 5-D/E/F）。
