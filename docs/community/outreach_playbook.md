# Good First Issue Outreach Playbook

> **核心命題：** "good first issue" は入門者向けラベルではなく、
> **GitHub の発見エンジン**である。
> 玄人ほど「このプロジェクトは本当に設計されているか？」を素早く査定するために
> good first issue を読む。

---

## なぜ good first issue が玄人を引き寄せるのか

```
初心者の行動:  「どこから始めれば？」→ good first issue を探す
玄人の行動:    「このプロジェクト、本物か？」→ good first issue で設計を判断する
```

GitHub 上での発見フロー：

1. **GitHub Explore** — `good-first-issue` タグが Topic ページに出る
2. **ラベル検索** — `is:issue label:"good first issue" is:open` で横断検索
3. **スター直後の行動** — スターした後、issues タブを見る。good first issue があれば「参加できるか」を判断
4. **ポートフォリオ目的** — 「面白いプロジェクトのコントリビューター」になりたい開発者が browsing

**玄人が issue を判断する 3 秒ルール:**

```
Title:  単純そう → クリック
Body:   「ん、6次元テンソル？」→ 読み込む
Code:   「AsyncPartyMachine / DeliberationEngine」→ 関心度 UP
Stretch: 「arXiv paper の図になる可能性」→ 参加を決断
```

---

## Issue の設計公式

### 構造

```
[Title]
  シンプルな動詞 + 明確な対象
  例: "Add a chart", "Write acceptance test", "Explain why X scores 0.95"
  ← 初心者には親しみやすく、玄人には「何が問題か」が即わかる

[Hook (最初の 2 行)]
  プロジェクトの設計を一言で開示する
  例: "Po_core represents each philosopher as a 6-dimensional ML tensor"
  ← 玄人が「へえ」と思う情報

[Task]
  2 段階で記述する:
  (1) 初心者でもできる具体的なタスク
  (2) 玄人向けの stretch goal (オプション)

[Architecture reveal]
  関連ファイルを列挙するとき、単なるパスではなく
  アーキテクチャの意図を添える
  例: "src/po_core/deliberation/emergence.py — EmergenceDetector"
      ← 「EmergenceDetector ってなんだ？」と思わせる

[Why it matters]
  そのタスクがプロジェクト全体でどんな意味を持つかを書く
  例: "This test may become a figure in our arXiv paper."
```

### タイトル設計の例

| 悪い例 | 良い例 |
|--------|--------|
| Add tests | Add pytest fixtures for W_Ethics Gate layers W0–W4 |
| Fix docs  | Explain why Nietzsche scores 0.95 on freedom_pressure |
| New feature | Add philosopher #44: Ibn Khaldun — Social Cohesion |
| Benchmark | Benchmark: how many philosophers can deliberate within 100ms? |

---

## ポスト計画

### 第一弾（プロジェクト公開直後）

優先度：哲学 × コード の「橋渡し感」が強いものから

```
Week 1: OUTREACH-03 (Ibn Khaldun — 哲学 + Python)
Week 2: OUTREACH-01 (テンソル重みの説明 — ノーコード)
Week 3: OUTREACH-06 (ベンチマーク — パフォーマンス)
Week 4: OUTREACH-02 (W_Ethics Gate テスト — セキュリティ)
Week 5: OUTREACH-04 (WebUI チャート — 可視化)
Week 6: OUTREACH-05 (AT-016 — AI ガバナンス)
```

**週 1 本ずつ** 出すのが重要。まとめてポストすると各 issue の注目度が分散する。

### 各 issue 投稿後の行動

1. **初コメントから 24 時間以内に返信** — 「いい質問ですね、〇〇を見てみると…」
2. **Discussions にクロスポスト** — "Working on OUTREACH-03? Share your philosopher proposal here"
3. **Weekly digest に含める** — CHANGELOG や Twitter に "New good first issue: ..."

---

## クロスプラットフォーム拡散

### GitHub Discussions

[discussion_starter.md](./discussion_starter.md) の Thread 1 と連動させる:

```
Issue #44 を Discussions に pin する:
"Proposing Ibn Khaldun for slot #44 — join the tensor weight design discussion!"
```

### Hacker News

good first issue を直接リンクするのではなく、**技術的な問いとして投稿**する:

```
Ask HN: Is there a principled way to encode a philosopher's ethics as a 6D vector?

We're building Po_core (philosophy-driven AI) and hit this problem:
Nietzsche scores 0.95 on freedom_pressure, Kant scores 0.12.
But is this principled or arbitrary?

We made it a "good first issue" for documentation:
[link to OUTREACH-01]
```

### X (Twitter)

```
🐷 New "good first issue" in Po_core:

"Why does Nietzsche score 0.95 on freedom_pressure but Kant scores 0.12?"

Not a coding task — philosophy + explanation required.
39 philosophers encoded as 6D ML tensors.

→ [link]

#GoodFirstIssue #Philosophy #AI #OpenSource
```

### Reddit: r/MachineLearning / r/Python / r/philosophy

各 subreddit に合わせてフレーミングを変える:

| Subreddit | フレーミング |
|-----------|------------|
| r/MachineLearning | "We encoded 43 philosophers as ML tensors — looking for review" |
| r/Python | "Good first issue: add pytest fixtures for a 5-layer AI safety gate" |
| r/philosophy | "Help us check if our Nietzsche tensor weight is philosophically accurate" |
| r/AIethics | "Good first issue: write acceptance test for AI governance dilemma" |

---

## 成功指標

| 指標 | 目標 | 測定方法 |
|------|------|---------|
| issue に対するコメント数 | ≥ 3 / issue | GitHub issue comments |
| コントリビューター数増加 | +2 / 月 | CHANGELOG, git log --shortstat |
| スター増加速度 | +10% / 月 | GitHub insights |
| PR 提出率 | 20% の issue が PR に繋がる | GitHub projects |
| 玄人コントリビューター | 少なくとも 1 名 / Quarter | GitHub profile 確認 |

---

## テンプレート: 新しい outreach issue を作る時

```markdown
## [good first issue] [Simple action] — [Intriguing context]

**Labels:** `good first issue`, `[track]`

---

[1行で何が面白いかを開示]

[Hook: アーキテクチャの一部を見せる (コード or 表)]

### Task

[初心者でもできる具体的な 3-5 ステップ]

### Why this matters

[このタスクがプロジェクト全体で持つ意味]

### Relevant files

- `path/to/file.py` — [その役割を添える]

### Stretch goal (for [expert domain])

[玄人が「それは面白い」と思う次のステップ]
```

---

## 注意点

- **クローズしない** — 誰かが作業中でも、他の人も参加できるよう open のままにする
  （"multiple PRs welcome" と書く）
- **ありがとうを忘れない** — コメントだけでも感謝する。それが次の人を呼ぶ
- **stretch goal は難しすぎない** — 「論文になるかも」は動機付けになるが、
  「量子コンピューターが必要」はならない
- **issue タイトルは変えない** — 一度 indexed されたら URL が変わる
