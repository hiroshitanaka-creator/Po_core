# Po_core クイックスタート 🐷🎈

Po_coreの哲学駆動型AIシステムをすぐに試せるガイドです。

## 📦 インストール

```bash
# リポジトリをクローン
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core

# 公開済み public version 1.0.3 を install
pip install "po-core-flyingpig==1.0.3"
```

## 🚀 リリース成果物の作成（maintainer向け）

```bash
# ビルドツールをインストール
pip install build twine

# sdist/wheel を生成
python -m build

# PyPIメタデータ検証
twine check dist/*
```

> Repository target version は `1.1.0` で、latest published public version は `1.0.3` です。公開証跡は `docs/release/pypi_publication_v1.0.3.md` / `docs/release/testpypi_publish_log_v1.0.3.md` / `docs/release/smoke_verification_v1.0.3.md` に固定されています。`1.1.0` の publish は pending です。

## 🔐 REST ランタイム既定値

- 通常運用では `PO_SKIP_AUTH=false` のままにし、非空の `PO_API_KEY` を設定してください。
- 既定の CORS は localhost のみ許可します。`PO_CORS_ORIGINS=*` は短命な開発時 override としてのみ使ってください。
- REST server は `PO_PHILOSOPHER_EXECUTION_MODE=process` を既定にし、`thread` は `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` を明示した開発時にだけ許可します。


### ✅ 公開前の最短検証（maintainer向け）

```bash
# 1) クリーン環境へソース checkout を導入
python -m pip install --upgrade pip
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core
pip install -e .

# 2) import 成功確認
python -c "import po_core; print(po_core.__name__)"

# 3) 最短クイックスタート確認（生成APIの疎通）
python - <<'PY'
from po_core.po_self import PoSelf
po = PoSelf()
res = po.generate("公開後の動作確認")
print(bool(res.text), res.consensus_leader)
PY
```

期待結果: install/import が成功し、最後の行で `True` とリーダー名が出力されること。install 例は latest published public version `1.0.3` に整合しています。

## ⚡ 30秒で試す

### 最小限のコード

```python
from po_core.po_self import PoSelf

# Po_selfインスタンスを作成
po = PoSelf()

# 質問に対して哲学的推論を実行
response = po.generate("人生の意味とは何か？")

# 結果を表示
print(f"回答: {response.text}")
print(f"リーダー: {response.consensus_leader}")
```

### コマンドライン（CLI）

```bash
# ヘルプを表示
po-core --help

# バージョン確認
po-core version

# 質問に対して推論
po-core prompt "真の自由とは何か？"

# JSON形式で出力
po-core prompt "倫理とは何か？" --format json
```

## 🎮 デモを試す

### 対話型デモ

```bash
# PYTHONPATHを設定して実行
PYTHONPATH=src python examples/simple_demo.py
```

デモでは以下の機能を体験できます：

1. **基本デモ** - 単一の質問に対する哲学的推論
2. **哲学者比較デモ** - 異なる哲学者グループの視点比較
3. **対話型モード** - 連続的な質問応答

### API使用例

```bash
# すべてのAPI例を実行
PYTHONPATH=src python examples/api_demo.py
```

7つの実用的な使用例が実行されます。

## 🧠 基本的な使い方

### 1. デフォルト哲学者で推論

```python
from po_core.po_self import PoSelf

po = PoSelf()
response = po.generate("正義とは何か？")

print(response.text)
print(f"メトリクス: {response.metrics}")
```

### 2. カスタム哲学者を選択

```python
# 実存主義者グループ（constructor はデフォルトallowlist）
default_philosophers = ["sartre", "heidegger", "kierkegaard"]
po = PoSelf(philosophers=default_philosophers)

response = po.generate("実存とは何か？")
print(response.text)

# 呼び出し単位で上書きも可能
override = po.generate("実存とは何か？", philosophers=["nietzsche"])
print(override.text)
```

### 3. JSON形式で取得

```python
import json

po = PoSelf()
response = po.generate("美とは何か？")

# 辞書形式に変換
data = response.to_dict()

# JSON出力
print(json.dumps(data, indent=2, ensure_ascii=False))
```

## 🎯 利用可能な哲学者

Po_coreでは **42人の哲学者** を正式 roster として扱います。内部には compliance helper として `dummy` スロットもありますが、これは哲学者数には含めません。1リクエストで動員される人数は SafetyMode と予算設定により変動し、NORMAL 既定では哲学者の参加は最大39です：

| 哲学者 | キー名 | 専門分野 |
|--------|--------|----------|
| アリストテレス | `aristotle` | 徳倫理学、テレオロジー |
| サルトル | `sartre` | 実存主義 |
| ハイデガー | `heidegger` | 現象学、存在論 |
| ニーチェ | `nietzsche` | 力への意志、系譜学 |
| デリダ | `derrida` | 脱構築 |
| ウィトゲンシュタイン | `wittgenstein` | 言語哲学 |
| ユング | `jung` | 分析心理学 |
| デューイ | `dewey` | プラグマティズム |
| ドゥルーズ | `deleuze` | 差異の哲学 |
| キルケゴール | `kierkegaard` | 実存主義 |
| ラカン | `lacan` | 精神分析 |
| レヴィナス | `levinas` | 他者の倫理 |
| バディウ | `badiou` | 数学的存在論 |
| パース | `peirce` | 記号論、プラグマティズム |
| メルロ＝ポンティ | `merleau_ponty` | 身体の現象学 |
| アーレント | `arendt` | 政治哲学 |
| 和辻哲郎 | `watsuji` | 間柄の倫理 |
| 侘び寂び | `wabi_sabi` | 日本美学 |
| 孔子 | `confucius` | 儒教 |
| 荘子 | `zhuangzi` | 道教 |
| … 他 19人 | `GET /v1/philosophers` | で完全一覧取得可能 |

## 📊 出力構造

```python
response = po.generate("質問")

# アクセス可能な属性
response.prompt              # 入力した質問
response.text                # 推論結果のテキスト
response.consensus_leader    # コンセンサスリーダー（最も影響力のある哲学者）
response.philosophers        # 参加した哲学者のリスト
response.metrics            # 哲学的テンソルメトリクス
response.responses          # 各哲学者の詳細な応答
response.log                # トレースログ（Po_trace）
```

### メトリクスの意味

- **freedom_pressure**: 自由の圧力 - 応答の責任重量を測定（0.0〜1.0）
- **semantic_delta**: 意味の変化 - 意味の進化を追跡（0.0〜1.0）
- **blocked_tensor**: ブロックされたテンソル - 何が言われなかったかを記録（0.0〜1.0）

## 🔧 高度な使用法

### po_core.run() を直接使用

```python
from po_core import run

result = run(user_input="美とは何か？")

print(result['status'])       # "ok"
print(result['request_id'])   # リクエストID
print(result['proposal'])     # 提案内容

# public API facade でも subset 指定可能
subset = run(user_input="正義とは何か？", philosophers=["kant"])
print(subset['status'])
```

### トレース機能の制御

```python
# トレース有効（デフォルト）
po = PoSelf(enable_trace=True)
response = po.generate("正義とは何か？")
print(response.log)  # トレースログを確認

# トレース無効（軽量モード）
po = PoSelf(enable_trace=False)
response = po.generate("正義とは何か？")
```

## 💡 使用ケース例

### 倫理的決定支援

```python
# 倫理専門の哲学者を選択
ethical_philosophers = ["aristotle", "levinas", "confucius", "arendt"]
po = PoSelf(philosophers=ethical_philosophers)

response = po.generate("この状況で正しい行動は何か？")
```

### 実存的問い

```python
# 実存主義者を選択
existentialists = ["sartre", "heidegger", "kierkegaard"]
po = PoSelf(philosophers=existentialists)

response = po.generate("自由とは何か？")
```

### 美学的分析

```python
# 美学・芸術哲学者を選択
aesthetics = ["nietzsche", "wabi_sabi", "dewey"]
po = PoSelf(philosophers=aesthetics)

response = po.generate("この作品の美しさは何か？")
```

### 言語と意味の探究

```python
# 言語哲学者を選択
language_philosophers = ["wittgenstein", "derrida", "peirce"]
po = PoSelf(philosophers=language_philosophers)

response = po.generate("この言葉の意味は何か？")
```

## 📚 次のステップ

- **詳細なAPI例**: `examples/api_demo.py` を参照
- **対話型デモ**: `examples/simple_demo.py` を試す
- **完全なドキュメント**: `/docs` ディレクトリを参照
- **哲学者の詳細**: `/04_modules` で各哲学者のスペックを確認

## 🐛 トラブルシューティング

### ModuleNotFoundError: No module named 'po_core'

```bash
# PYTHONPATHを設定
export PYTHONPATH=/path/to/Po_core/src:$PYTHONPATH

# または開発モードでインストール
pip install "po-core-flyingpig==1.0.3"
```

### ImportError: No module named 'click' or 'rich'

```bash
# パッケージ依存を含めて source checkout から再インストール
pip install -e .
```

## 🤝 フィードバック

質問や提案がありましたら：

- [GitHub Issues](https://github.com/hiroshitanaka-creator/Po_core/issues)
- [GitHub Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions)

---

## 🚀 REST API (Phase 5)

### Docker で起動する（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core

# .env を設定
cp .env.example .env
# 推奨デフォルト: `PO_SKIP_AUTH=false` のまま、非空の `PO_API_KEY` を設定
# `PO_SKIP_AUTH=true` は認証なしで試したいローカル開発時だけに限定してください

# Docker Compose で起動
docker compose up

# Swagger UI で対話的に試す
open http://localhost:8000/docs
```

### ローカルで起動する

```bash
pip install "po-core-flyingpig==1.0.3"

# 推奨: 開発でも認証を有効化したまま試す
export PO_API_KEY=dev-secret-key

# サーバー起動
python -m po_core.app.rest
# → http://localhost:8000
```

### エンドポイント一覧

| Method | Path | 説明 |
|--------|------|------|
| `POST` | `/v1/reason` | 同期的な哲学的推論（42人の哲学者、通常時は最大39名を動員して Pareto 集約） |
| `POST` | `/v1/reason/stream` | SSE ストリーミング推論（asyncio非同期） |
| `GET`  | `/v1/philosophers` | 正式な42人の哲学者マニフェスト一覧（`dummy` helper は除外） |
| `GET`  | `/v1/trace/{session_id}` | セッション別トレースイベント取得 |
| `GET`  | `/v1/health` | ヘルスチェック（バージョン・稼働時間） |

> 注意: LLM provider/model 設定は「どのバックエンドで各哲学者を実行するか」を決めます。
> これは哲学者の人数を決める設定ではありません（人数は SafetyMode/allowlist で制御）。

### 使用例

```bash
# 同期推論（推奨デフォルトの認証有効モード）
curl -X POST http://localhost:8000/v1/reason \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"input": "What is justice?", "philosophers": ["kant"]}'

# SSE ストリーミング（true async offload）
curl -N -X POST http://localhost:8000/v1/reason/stream \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"input": "What is the good life?"}'

# 統合済み42ランタイム・ペルソナ一覧
curl -H "X-API-Key: dev-secret-key" http://localhost:8000/v1/philosophers

# ヘルスチェック
curl http://localhost:8000/v1/health

# API キー認証あり
curl -X POST http://localhost:8000/v1/reason \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"input": "What is freedom?"}'
```

### 環境変数

`.env.example` をコピーして `.env` を作成し、必要な変数を設定してください。

| 変数 | デフォルト | 説明 |
|------|-----------|------|
| `PO_API_KEY` | `""` | `PO_SKIP_AUTH=false` のときに必要な API キー。空/blank のままでは起動失敗 |
| `PO_SKIP_AUTH` | `false` | 推奨デフォルトは `false`。`true` は認証なしで試すローカル開発時だけ |
| `PO_API_KEY_HEADER` | `X-API-Key` | 必要な場合だけ使う上級者向け設定。主ヘッダー名を変更しても `X-API-Key` は後方互換で受理 |
| `PO_CORS_ORIGINS` | `http://localhost,http://127.0.0.1,http://localhost:3000,http://127.0.0.1:3000` | 許可オリジン。既定は localhost 限定、`*` は短命な開発時 override のみ |
| `PO_RATE_LIMIT_PER_MINUTE` | `60` | IP ごとのレート制限（req/min） |
| `PO_PORT` | `8000` | サーバーポート |
| `PO_WORKERS` | `1` | uvicorn ワーカー数 |
| `PO_LOG_LEVEL` | `info` | ログレベル |
| `PO_PHILOSOPHER_EXECUTION_MODE` | `process` | 哲学者実行バックエンド。REST の安全既定値は `process` |
| `PO_ALLOW_UNSAFE_THREAD_EXECUTION` | `false` | REST/server は `thread` を拒否し、この値を `true` にした短命な開発時だけ例外的に許可 |

### ⚡ パフォーマンス（Phase 5-E 実測値）

| モード | 哲学者数 | p50 レイテンシ | req/s |
|--------|---------|--------------|-------|
| NORMAL | 最大39人 | ~33 ms | ~30 |
| WARN | 5人 | ~34 ms | ~30 |
| CRITICAL | 1人 | ~35 ms | ~29 |

5 並列同時リクエスト（WARN）: 壁時計 **181 ms** 完了

---

**🐷🎈 Flying Pig Philosophy**

「豚は飛べない」と言われています。でも、哲学という風船をつければ飛べるかもしれません。

*井の中の蛙、大海は知らずとも、大空を知る*
