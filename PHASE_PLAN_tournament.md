# Tournament Debate Plan — ガチンコ哲学議論

> 目標: 哲学者が互いを本当に論駁し合い、
> チーム戦を経て陪審評決を下す「哲学トーナメント」エンジンへ。

---

## ロードマップ全体

```
Phase 6-A  Prompt Hardening          ← 今ここ (実装済 後に ✅)
Phase 6-B  Dialectic Roles           ← 次
Phase 6-C1 Position Clustering
Phase 6-C2 Team Debate Engine
Phase 6-C3 Jury & Verdict  → PyPI
```

---

## Phase 6-A: Prompt Hardening ✅ COMPLETE

**目的:** 既存の counterargument 送信の「ゆるさ」を排除し、
哲学者に明示的な反論義務を課す。

### 変更範囲

| ファイル | 変更内容 |
|---------|---------|
| `src/po_core/deliberation/engine.py` | `_re_propose()` プロンプト強化、`round_number` 動的記録 |
| `src/po_core/runtime/settings.py` | `deliberation_prompt_mode: str` 追加 (`"basic"` / `"debate"`) |
| `tests/unit/test_phase6a_prompt_hardening.py` | 新規テスト |

### 強化後プロンプト形式 (`debate` モード)

```
[PHILOSOPHICAL CHALLENGE — Round {n}]
{peer_philosopher} opposes your position with the following argument:

"{peer_proposal}"

You MUST respond by:
1. Identifying the strongest point in {peer}'s argument (steelman)
2. Exposing the core flaw in their reasoning
3. Defending your own position with a new or sharpened argument

Do NOT repeat your Round 1 response verbatim.
```

### 完了条件

- [x] `debate` モードで counterargument プロンプトが変わる
- [x] `round_number` が round 2, 3, … と動的に記録される
- [x] テスト 16 本グリーン (35/35 全体)
- [x] CI 通過

---

## Phase 6-B: Dialectic Roles

**目的:** 各ラウンドに Hegel 弁証法的な役割を割り当て、
議論の構造を Thesis → Antithesis → Synthesis に進化させる。

### 設計

```
Round 1 (Thesis)     : 全哲学者が独自立場を提案 [現状と同じ]
Round 2 (Antithesis) : 高干渉ペアが「否定」を構築
                       プロンプト: "Your task is to REFUTE, not just rebut."
Round 3 (Synthesis)  : Synthesizer 哲学者群 (Hegel, Rawls, Habermas) が
                       対立する提案を統合して上位命題を生成
```

### 変更範囲

| ファイル | 変更内容 |
|---------|---------|
| `src/po_core/deliberation/engine.py` | `DebateRole` enum、`RoundTrace.role` フィールド |
| `src/po_core/deliberation/roles.py` | 新規: role → prompt prefix マッピング |
| `src/po_core/runtime/settings.py` | `deliberation_mode: str` (`"standard"` / `"dialectic"`) |
| `tests/unit/test_phase6b_dialectic.py` | 新規テスト |

### 完了条件

- [ ] `dialectic` モードで 3 ラウンド実行される
- [ ] `RoundTrace.role` が `"thesis"` / `"antithesis"` / `"synthesis"` を持つ
- [ ] Synthesis ラウンドの出力が round 1, 2 の折衷案として検証可能
- [ ] テスト 10 本以上グリーン

---

## Phase 6-C1: Position Clustering

**目的:** `InteractionMatrix.harmony` 行列を使い、
哲学者を「立場クラスタ」に自動分類する。

### 設計

```
harmony NxN 行列 (コサイン類似度)
  → Spectral Clustering (sklearn) で k クラスタに分類
  → k は Silhouette スコアで自動決定 (k=2..6 を試す)
  → ClusterResult: {cluster_id → [philosopher_names]}
```

### 変更範囲

| ファイル | 変更内容 |
|---------|---------|
| `src/po_core/deliberation/clustering.py` | 新規: `PositionClusterer`, `ClusterResult` |
| `src/po_core/deliberation/engine.py` | clustering を round 1 後に実行 |
| `src/po_core/trace/schema.py` | `ClusteringCompleted` TraceEvent 追加 |
| `tests/unit/test_phase6c1_clustering.py` | 新規テスト |

### 完了条件

- [ ] harmony 行列からクラスタが生成される
- [ ] クラスタ数が入力次第で 2〜6 に自動決定される
- [ ] `ClusteringCompleted` Trace Event が emit される
- [ ] テスト 8 本以上グリーン

---

## Phase 6-C2: Team Debate Engine

**目的:** クラスタをチームとして扱い、
チーム内 consensus → チーム間 confrontation の 2 段階戦を実装。

### 設計

```
Stage 1 — Intra-team Consensus
  各チームの哲学者が互いの提案を読み、
  チーム代表提案 (team_proposal) を 1 本に絞る
  (最高 synthesis スコアの提案を代表に選出)

Stage 2 — Inter-team Confrontation
  チーム代表同士が 3 ラウンド議論
  (Phase 6-A の強化プロンプトを使用)
  各チームは代表の主張を補強するサポーター提案も提出可

Stage 3 — Revised Full Proposals
  全哲学者が「チーム戦の結果」を踏まえて最終提案を更新
```

### 変更範囲

| ファイル | 変更内容 |
|---------|---------|
| `src/po_core/deliberation/team_engine.py` | 新規: `TeamDebateEngine`, `TeamDebateResult` |
| `src/po_core/deliberation/engine.py` | `TeamDebateEngine` をオプション呼び出し |
| `src/po_core/trace/schema.py` | `TeamDebateCompleted` TraceEvent |
| `tests/unit/test_phase6c2_team_debate.py` | 新規テスト |

### 完了条件

- [ ] チーム代表が自動選出される
- [ ] チーム間 3 ラウンド議論が実行される
- [ ] `TeamDebateResult` に `team_proposals`, `confrontation_rounds` が含まれる
- [ ] テスト 10 本以上グリーン

---

## Phase 6-C3: Jury & Verdict → PyPI

**目的:** 全哲学者が審査員となりチームの議論を採点し、
最終評決を下す。REST API でも公開。

### 設計

```
Jury Pool: チームに属さない「中立」哲学者 + 全哲学者
  → 各審査員が (team_A_score, team_B_score, rationale) を返す
  → Weighted vote: tensor の freedom_pressure / semantic_delta で重み付け
  → Verdict: winning_team, margin, dissenting_opinions

REST API:
  POST /v1/reason → response に "verdict" フィールド追加
  GET  /v1/debate/{session_id} → 全ラウンド + 評決を返す
```

### 変更範囲

| ファイル | 変更内容 |
|---------|---------|
| `src/po_core/deliberation/jury.py` | 新規: `JuryEngine`, `Verdict` |
| `src/po_core/app/rest/routers/debate.py` | 新規: `/v1/debate/{session_id}` |
| `src/po_core/app/rest/models.py` | `VerdictSchema` 追加 |
| `tests/unit/test_phase6c3_jury.py` | 新規テスト |
| `.github/workflows/publish.yml` | PyPI 公開 trigger |

### 完了条件

- [ ] 評決が `Verdict` dataclass に格納される
- [ ] `/v1/reason` レスポンスに `verdict` が含まれる
- [ ] `/v1/debate/{session_id}` で全ラウンドと評決が取得できる
- [ ] テスト 12 本以上グリーン
- [ ] TestPyPI に publish 成功

---

## ブランチ戦略

```
main
 └─ claude/phase6a-prompt-hardening     ← Phase 6-A
 └─ claude/phase6b-dialectic-roles      ← Phase 6-B
 └─ claude/phase6c1-clustering          ← Phase 6-C1
 └─ claude/phase6c2-team-debate         ← Phase 6-C2
 └─ claude/phase6c3-jury-verdict        ← Phase 6-C3 + PyPI
```

各フェーズは PR → main でマージしてから次フェーズ開始。

---

## 迷ったときの判断基準

1. **既存テストが壊れたら** — 即修正、次フェーズに進まない
2. **設計変更が出たら** — このファイルを先に更新してから実装
3. **PyPI を先に出したいなら** — Phase 6-B 完了後でも出せる (6-C は後付け可)
