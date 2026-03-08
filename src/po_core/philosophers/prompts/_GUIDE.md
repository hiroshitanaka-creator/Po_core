# 哲学者プロンプト作成ガイド

> **目的:** このディレクトリの YAML ファイルが、LLM（GPT-5.4 Pro 等）への哲学者プロンプトの唯一の真実源（SSOT）となる。
> **担当:** 各 `{philosopher}.yaml` をここに記述し、`LLMPhilosopher` クラスが読み込んで LLM を呼び出す。

---

## ディレクトリ構造

```
prompts/
├── _GUIDE.md              ← このファイル（読むべき最初のファイル）
├── _template.yaml         ← 全フィールドのリファレンス（コピー元）
├── aristotle.yaml         ← 記入済みサンプル（最初に読むこと）
├── kant.yaml
├── plato.yaml
├── ...（42ファイル）
```

---

## プロンプト設計の原則

### 1. system_prompt の書き方

LLM に「あなたは〇〇である」と告げるブロック。以下を含めること：

- **名前・生没年・所属文化圏**
- **代表的な哲学的立場・概念**（3〜5個）
- **特徴的な思考スタイル**（問い方、論理展開の癖、好む比喩など）
- **他の哲学者との関係**（対立・継承・影響関係）
- **倫理的判断の軸**：「この哲学者は何を最重要視するか」を明確に

**長さの目安:** 300〜600 words（英語）

### 2. user_template の書き方

LLM への毎回の呼び出しテンプレート。以下の変数が実行時に埋め込まれる：

| 変数名 | 内容 |
|---|---|
| `{prompt}` | ユーザーの入力・質問 |
| `{context}` | セッション文脈（JSON文字列） |
| `{freedom_pressure}` | 自由圧力テンソル値（0.0〜1.0） |
| `{semantic_delta}` | 意味的新規性（0.0〜1.0） |
| `{blocked_tensor}` | ブロックテンソル値（0.0〜1.0） |
| `{intent}` | SolarWillが判定した意図 |

**必ずJSON出力を要求すること。** 後述の出力フォーマット参照。

### 3. 出力フォーマット（必須）

LLM は以下の JSON を返すよう指示する：

```json
{
  "reasoning": "哲学的分析（複数段落）",
  "perspective": "この哲学者の視点名（短い）",
  "tension": {
    "level": "low|medium|high",
    "description": "識別された緊張・矛盾の説明"
  },
  "confidence": 0.75,
  "action_type": "answer|refuse|ask_clarification|defer",
  "citations": ["著作名1", "著作名2"]
}
```

`tension` は `null` でも可。`confidence` は 0.0〜1.0。

---

## 記入の手順

1. `_template.yaml` をコピーして `{philosopher_id}.yaml` にリネーム
2. `philosopher_id` は Python モジュール名と一致させる（例: `marcus_aurelius`）
3. `system_prompt` を英語で記述（LLM が英語の哲学的概念をより正確に扱うため）
4. `user_template` の変数プレースホルダ（`{prompt}` 等）はそのまま残す
5. `example_input` と `example_output` を記述してセルフチェック
6. 完成後、`aristotle.yaml` と見比べて品質確認

---

## 品質チェックリスト

各 YAML を仕上げたら確認：

- [ ] `system_prompt` に哲学者の主要概念が3つ以上含まれているか
- [ ] `system_prompt` が 300 words 以上あるか
- [ ] `user_template` に `{prompt}` が含まれているか
- [ ] `user_template` に JSON 出力要求が含まれているか
- [ ] `tension` の説明が哲学者固有の概念を使っているか
- [ ] `citations` に実際の著作名が少なくとも1つあるか
- [ ] `example_output.reasoning` が哲学者の文体を反映しているか

---

## base.py との関係

**変更不要。** `base.py` の `Philosopher.propose()` → `reason()` → `normalize_response()` の連鎖はそのまま使う。

新たに作る `LLMPhilosopher`（`llm_philosopher.py`）は：

```
class LLMPhilosopher(Philosopher):
    def reason(self, prompt, context=None):
        # 1. prompts/{module_id}.yaml を読む
        # 2. system_prompt + user_template を組み立てる
        # 3. OpenAI API (GPT-5.4 Pro) に送る
        # 4. JSON をパースして return する
        # → base.py の normalize_response() が後続処理
```

既存の 42 の `.py` ファイルは、LLM 統合後も **段階的に置き換え可能**（1ファイルずつ差し替え、テストで確認）。
