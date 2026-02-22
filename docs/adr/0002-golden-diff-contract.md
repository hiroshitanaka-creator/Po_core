# ADR 0002: Golden Diff Contract

**Date:** 2026-02-22
**Status:** Accepted
**Deciders:** Po_core project

---

## Context

Po_coreの出力を「期待値（golden files）」と比較するE2Eテスト（golden diff）を導入する。
golden diffは「現物で殴る」最も強力な検証手段だが、設計が悪いと
「毎回違うから落ちるフレーク地獄」になる。

ここでは「何を一致させるか」「何を正規化するか」「goldenをいつ更新するか」を凍結する。

---

## Decision

### 1. 比較方法

```
canonical_json(actual) == canonical_json(expected)
```

完全一致（フィールドを削ったり無視したりしない）。

### 2. 正規化ルール（canonical_json）

| フィールド | 扱い | 理由 |
|-----------|------|------|
| `meta.created_at` | テストで固定時刻を注入して一致させる（削除しない） | 決定性を実装で保証する |
| `meta.run_id` | `{case_id}:{seed}:{pocore_version}:{input_digest[:8]}` で決定的生成 | 削除しない |
| `meta.seed` | テスト時は seed=0 で固定 | 決定性の前提 |
| `trace.steps[*].started_at/ended_at` | 固定時刻からの決定的オフセット（1秒刻み）で生成 | 削除しない |
| `options` 配列順序 | `option_id` でソートしてから出力 | 順序揺れ防止 |
| `questions` 配列順序 | `(priority, question_id)` でソートしてから出力 | 順序揺れ防止 |
| JSON key順序 | `sort_keys=True` で正規化 | dict順序揺れ防止 |

**canonical化の実装例：**

```python
import json

def canonical_json(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

### 3. input_digest の計算方法

```python
import hashlib
import json

def compute_input_digest(case_dict: dict) -> str:
    canonical = json.dumps(case_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

YAML由来の `date`/`datetime` は ISO文字列に正規化してから canonical化する。

### 4. golden更新のルール（最重要）

**golden を更新してよい条件：**
- SRS（srs_v0.1.md）の要件が変更された場合
- output_schema_v1.json が変更された場合
- バグ修正により「正しい出力」が変わった場合（ADRに記録必須）

**golden を更新してはいけない条件：**
- CIを通すためだけの更新
- 「雰囲気で変えた」更新
- 上記のいずれにも当てはまらない更新

**更新手順：**
1. SRS/ADRに変更理由を記載
2. `scripts/update_goldens.py --accept` を実行（将来実装）
3. PRに「SRS/ADRの変更リンク」「golden更新理由」を必記

---

## Rationale

- `created_at` や `run_id` を削除して比較すると「意味のある出力の変化」を検出できなくなる
- 決定性を「実装」で保証することで、テストが正確な契約になる
- 配列のソートを固定することで、実装の実行順序が変わっても比較が安定する
- golden更新を「SRS変更に紐づく」ことで、「goldenがただのログ」に堕落するのを防ぐ

---

## Consequences

- Po_core の `orchestrator.py` は `seed`, `now` を外部注入できる必要がある
- テスト側は `now=固定時刻` で Po_core を呼ぶ
- golden更新は「意図した仕様変更」のみ許可（CIで強制はできないが運用で縛る）
- フレークを防ぐために決定性実装は M1（2026-03-15）までに必須

---

## Alternatives Considered

| 代替案 | 却下理由 |
|-------|---------|
| `created_at` / `run_id` を比較から除外 | 出力の意味的変化を検出できなくなる（弱い） |
| スナップショットだけで差分を表示（更新自由） | goldenが「雰囲気の記録」になり契約として機能しない |
| 主要フィールドのみ比較 | 何が「主要」かが曖昧で仕様が崩れやすい |
