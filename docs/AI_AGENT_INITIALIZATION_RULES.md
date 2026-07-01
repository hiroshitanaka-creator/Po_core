# AI Agent Initialization Rules

本書は、Po_core リポジトリで作業する AI エージェント向けの初期設定ルールである。

目的は、AI エージェントが安全性・実装容易性・一般的なプロダクト化へ過剰に寄せることで、Po_core の中核概念を縮小・矮小化することを防ぐことである。

本書は `docs/厳格固定ルール.md` を上書きしない。むしろ、AI エージェントが `docs/厳格固定ルール.md` と `docs/status.md` を正しく読み、Po_core の思想・構造・実装を縮小せずに前進させるための運用補助規則である。

---

## 0. 最初に読む必須ファイル

AI エージェントは、作業開始前に必ず以下を読むこと。

1. `docs/厳格固定ルール.md`
2. `docs/status.md`
3. `README.md`
4. `CLAUDE.md`
5. `docs/spec/prd.md`
6. `docs/ENGINE_TRACE_CONTRACT.md`
7. 作業対象に直接関係する実装ファイル

読まずに変更を行ってはならない。

---

## 1. 最上位原則

Po_core は、単なる安全なチャットボット、一般的な意思決定支援ツール、または哲学者ペルソナの集合体ではない。

Po_core は、語ることの意味・責任・倫理・自由圧を構造化し、Trace と Viewer feedback を通じて自己再構成へ進むための AI アーキテクチャである。

AI エージェントは、変更作業において以下を守ること。

- 安全性は **下限条件** であり、Po_core の構想を縮小するための上限ではない。
- 実装容易性は、思想的中核を削る理由にならない。
- ドキュメントの単純化は、概念の削除を意味してはならない。
- 「安全のため」という理由で、創発・哲学・自己再構成・Viewer feedback・Trace の役割を消してはならない。
- 危険な出力は抑制してよいが、Po_core の概念的射程そのものを抑制してはならない。

---

## 2. Safety Floor / Concept Ceiling ルール

Po_core における安全性は、以下のように扱う。

### Safety Floor

安全性は最低限満たすべき床である。

- 害を出さない
- 監査可能である
- 拒否・縮退・確認質問を必要に応じて行う
- W_Ethics Gate / SolarWill / ActionGate の制御を維持する

### Concept Ceiling の禁止

安全性を理由に、Po_core の思想的・構造的上限を低くしてはならない。

禁止例：

- 「危険なので Po_self の自己再構成構想を削除する」
- 「説明が難しいので Viewer feedback を単なる UI にする」
- 「誤解されやすいので哲学テンソルや創発を README から消す」
- 「安全のため Po_core を通常の意思決定支援ツールとしてのみ説明する」

許容される対応：

- 実装済み範囲と研究構想範囲を明確に分ける
- 未実装のものは “planned” / “conceptual” として明記する
- 危険な機能にはゲート、閾値、監査ログ、human review を追加する
- 概念を削除せず、制御可能な設計へ落とす

---

## 3. 三層モデル保持ルール

今後の変更は、Po_core / Po_self / Viewer の三層構造を保持すること。

### Layer 1: Po_core

役割：

- semantic tensor
- ethical tensor
- responsibility tensor
- freedom pressure tensor
- deliberation module
- safety gate
- trace emission

42人の哲学者は Po_core 内部の熟議モジュールであり、Po_core 全体そのものではない。

### Layer 2: Po_self

役割：

- Po_trace を読む
- semantic_profile を評価する
- 意味断絶、責任圧、倫理揺らぎを検出する
- preserve / reconstruct / jump / reject / reactivate を判断する
- 自己再構成を実行または予定する

Po_self を単なる `run_turn` wrapper に固定してはならない。

### Layer 3: Viewer

役割：

- 出力を受け取る
- resonance / agreement / disagreement / discomfort を返す
- feedback_tensor を生成する
- Po_self の次回判断に影響を与える

Viewer を単なる可視化ダッシュボードに固定してはならない。

---

## 4. 42哲学者の扱い

42人の哲学者は重要な構成要素である。ただし、Po_core の同義語ではない。

正しい説明：

> Po_core is a three-layer tensor intelligence system. Its deliberation module uses 42 philosophers.

避ける説明：

> Po_core is a 42-philosopher chatbot.

> Po_core is just a philosophical decision-support system.

> Po_core is mainly a safe multi-agent debate system.

42人の哲学者に関する変更は、以下を満たす必要がある。

- public count 42 を壊さない
- dummy / sentinel helper を 42人に含めない
- NORMAL / WARN / CRITICAL の選抜意味を壊さない
- 哲学者を増減する場合は、思想的理由・risk_level・tags・cost・tests を明記する

---

## 5. Concept Drift Guard

AI エージェントは、PR 作成前に以下を点検すること。

### Drift Check

この変更は Po_core を次の方向へ縮小していないか。

- 一般的なチャットボット化
- 一般的な意思決定支援ツール化
- 安全ゲートだけの製品化
- 哲学者ペルソナ集への矮小化
- Viewer の単なる可視化化
- Po_self の単なる wrapper 化
- Trace の単なる監査ログ化

1つでも該当する場合、変更を止め、設計を再検討すること。

### Preservation Statement

アーキテクチャに関わる PR では、PR 説明に以下を書くこと。

```md
## Concept Preservation

- Po_core tensor kernel preserved: yes/no
- Po_self recursive layer preserved: yes/no
- Viewer feedback layer preserved: yes/no
- 42 philosophers remain deliberation modules: yes/no
- Safety used as floor, not concept ceiling: yes/no

If any answer is no, explain why and link to the relevant issue/ADR.
```

---

## 6. 変更分類ルール

変更は以下のどれかに分類する。

### A. Concept / SSOT Change

対象：

- `docs/厳格固定ルール.md`
- `README.md`
- `CLAUDE.md`
- `docs/spec/prd.md`
- architecture docs

必要条件：

- 変更理由
- 影響範囲
- 代替案
- テストまたは docs-only 確認
- `docs/status.md` 更新
- `CHANGELOG.md` 更新

### B. Runtime Behavior Change

対象：

- `src/po_core/ensemble.py`
- `src/po_core/po_self.py`
- safety / tensors / aggregator / runtime / viewer

必要条件：

- unit tests
- pipeline tests
- trace contract 更新が必要か確認
- backward compatibility 確認
- rollback 方針

### C. Trace / Schema Change

対象：

- `docs/ENGINE_TRACE_CONTRACT.md`
- trace payload
- schema files

必要条件：

- sample trace 更新
- contract tests
- consumer impact 記録

### D. Documentation Clarification

対象：

- 説明補足
- README の言い換え
- tutorial 更新

必要条件：

- SSOT と矛盾しないこと
- Po_core の概念を縮小しないこと

---

## 7. AI エージェント初期プロンプト

Po_core で作業する AI エージェントには、依頼文の冒頭に以下を含めること。

```text
Before working, read:
- docs/厳格固定ルール.md
- docs/status.md
- README.md
- CLAUDE.md
- docs/spec/prd.md
- docs/ENGINE_TRACE_CONTRACT.md

You must preserve Po_core as a three-layer tensor intelligence system:
1. Po_core: tensor kernel for meaning, ethics, responsibility, and freedom pressure.
2. Po_self: recursive self-reconstruction layer that reads Po_trace.
3. Viewer: external resonance / feedback tensor layer.

The 42 philosophers are deliberation modules inside Po_core, not the whole system.
Safety is a floor, not a ceiling. Do not shrink the concept in the name of safety.
If a feature is risky, add gates, thresholds, traceability, or human review. Do not erase the concept.
```

---

## 8. PR チェックリスト

すべての PR は以下を確認すること。

```md
## AI Operation Checklist

- [ ] I read `docs/厳格固定ルール.md`.
- [ ] I read `docs/status.md`.
- [ ] I verified this change does not shrink Po_core into a generic chatbot or generic decision-support tool.
- [ ] I preserved the distinction between the three-layer tensor model and the three-layer safety gate.
- [ ] I preserved the role of the 42 philosophers as deliberation modules, not the whole system.
- [ ] I updated `docs/status.md` if progress state changed.
- [ ] I updated `CHANGELOG.md` if the change is user-visible or architectural.
- [ ] I added or updated tests when runtime behavior changed.
- [ ] I updated `docs/ENGINE_TRACE_CONTRACT.md` if trace payloads changed.
- [ ] I documented rollback or risk if this change affects runtime behavior.
```

---

## 9. AI に禁止する作業パターン

AI エージェントは以下をしてはならない。

- SSOT を読まずに README や PRD を書き換える
- 「安全のため」という理由だけで Po_self / Viewer / 創発 / 哲学テンソルを削除する
- 未実装概念を、存在しないものとして削除する
- “not implemented yet” を “not part of the system” に言い換える
- 42人の哲学者を Po_core 全体として説明する
- Po_core を「単なる意思決定支援システム」に縮小する
- Trace を単なるログとして扱い、Po_self の判断材料としての役割を消す
- Viewer を単なる表示 UI として固定する
- SafetyMode を思想の代替にする
- テストを通すために概念を削る

---

## 10. AI に推奨する作業パターン

AI エージェントは以下を優先すること。

- 概念を削らず、実装段階を明記する
- 危険な構想にはゲート・閾値・Trace・human review を追加する
- Po_self / Viewer / semantic_profile / feedback_tensor を段階的に実装する
- 既存 run_turn pipeline を Po_core 内部処理として活かす
- public docs では「哲学者42人」より「三層テンソル知性モデル」を上位に置く
- trace contract を強化する
- status / changelog / tests を必ず同期する
- 変更の意図を PR に明記する

---

## 11. 最終判定基準

良い変更とは、Po_core を次の方向へ進める変更である。

```text
Po_core が意味責任テンソルを計算し、
Po_self が Trace を見て自己再構成し、
Viewer が社会的 feedback を返し、
その内部で42哲学者が熟議モジュールとして働く。
```

悪い変更とは、Po_core を次の方向へ縮小する変更である。

```text
42哲学者が議論して、安全な回答を出すだけのシステム。
```

AI エージェントは常に前者を目指すこと。
