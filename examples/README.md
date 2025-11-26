# Po_core Examples / サンプル集

Po_coreの使い方を示すサンプルコード集です。

## 📚 サンプル一覧

### 基本デモ（Basic Demos）

#### 1. `simple_demo.py` - シンプルなデモ

Po_coreの基本機能を体験できる対話型デモです。

```bash
python examples/simple_demo.py
```

**機能:**
- 基本デモ - 単一の質問に対する哲学的推論
- 哲学者比較デモ - 異なる哲学者グループの視点比較
- 対話型モード - 連続的な質問応答

#### 2. `api_demo.py` - API使用例

Po_core APIの様々な使い方を示す7つの例を含みます。

```bash
python examples/api_demo.py
```

**例の内容:**
1. 基本的な使い方
2. カスタム哲学者の選択
3. JSON形式での出力
4. ensemble関数の直接使用
5. 各哲学者の詳細な応答
6. トレース無効化（軽量モード）
7. 複数の質問を連続処理

#### 3. `quick_test.py` - クイックテスト

Po_coreの動作確認用テストスイート。

```bash
python examples/quick_test.py
```

**テスト項目:**
- デフォルト/カスタム哲学者での推論
- JSON形式への変換
- メトリクスの検証
- トレース機能
- 連続的な質問処理

### 中規模プロトタイプ（Medium-Scale Prototypes）

#### 4. `web_api_server.py` - Web APIサーバー ⭐

FastAPIベースのRESTful APIサーバー。Webブラウザから哲学的推論を実行できます。

```bash
# 必要な依存関係をインストール
pip install fastapi uvicorn pydantic

# サーバーを起動
python examples/web_api_server.py
```

**アクセス:**
- Webインターフェース: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**主要機能:**
- 🌐 Webベースの対話インターフェース
- 📡 RESTful API エンドポイント
- 💾 セッション履歴の管理
- 📊 統計情報の取得
- 🎨 美しいUIデザイン

**API エンドポイント:**
- `POST /api/v1/prompt` - 哲学的推論を実行
- `GET /api/v1/sessions` - セッション履歴を取得
- `GET /api/v1/sessions/{id}` - 特定セッションの詳細
- `GET /api/v1/philosophers` - 利用可能な哲学者リスト
- `GET /api/v1/stats` - 統計情報
- `DELETE /api/v1/sessions` - セッション履歴をクリア

#### 5. `batch_analyzer.py` - バッチ分析ツール ⭐

複数の質問を一括処理し、結果を分析・エクスポートするツール。

```bash
python examples/batch_analyzer.py
```

**機能:**
- 📦 複数の質問を一括処理
- 📊 統計分析とサマリー表示
- 💾 JSON/CSV形式でのエクスポート
- 📈 平均メトリクス計算
- 🏆 リーダー分布の可視化

**ユースケース:**
- 大量の質問を効率的に処理
- 哲学者の傾向分析
- 研究データの収集
- ベンチマークテスト

#### 6. `philosopher_comparison.py` - 哲学者比較ツール ⭐

同じ質問に対する異なる哲学者の視点を詳細に比較。

```bash
python examples/philosopher_comparison.py
```

**機能:**
- 🔍 グループ比較モード - 哲学者グループ間の比較
- 👤 個別比較モード - 個々の哲学者の詳細比較
- 📊 メトリクス比較テーブル
- 📝 詳細な応答分析

**定義済みグループ:**
- 実存主義、古典哲学、現代哲学
- 倫理学、現象学、プラグマティズム
- 精神分析、東洋哲学、西洋哲学
- 政治哲学

**ユースケース:**
- 異なる哲学的視点の理解
- 教育・研究目的
- 複雑な問題の多角的分析

## 🚀 クイックスタート

### インストール

```bash
# リポジトリのルートディレクトリで
pip install -e .
```

### 最小限のコード例

```python
from po_core.po_self import PoSelf

# Po_selfインスタンスを作成
po = PoSelf()

# 質問に対して哲学的推論を実行
response = po.generate("人生の意味とは何か？")

# 結果を表示
print(f"コンセンサスリーダー: {response.consensus_leader}")
print(f"回答: {response.text}")
print(f"メトリクス: {response.metrics}")
```

## 📖 詳細な使用例

### カスタム哲学者の選択

```python
from po_core.po_self import PoSelf

# 特定の哲学者を選択
philosophers = ["sartre", "heidegger", "kierkegaard"]
po = PoSelf(philosophers=philosophers)

response = po.generate("実存とは何か？")
```

### JSON出力

```python
import json
from po_core.po_self import PoSelf

po = PoSelf()
response = po.generate("倫理的決定とは？")

# JSON形式に変換
print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))
```

### ensemble関数の直接使用

```python
from po_core import run_ensemble

result = run_ensemble(
    prompt="美とは何か？",
    philosophers=["aristotle", "nietzsche", "wabi_sabi"]
)

print(f"コンセンサスリーダー: {result['consensus']['leader']}")
print(f"メトリクス: {result['aggregate']}")
```

## 🧠 利用可能な哲学者

Po_coreでは20人の哲学者を利用できます：

### 西洋哲学
- `aristotle` - アリストテレス（徳倫理学）
- `sartre` - サルトル（実存主義）
- `heidegger` - ハイデガー（現象学）
- `nietzsche` - ニーチェ（系譜学）
- `derrida` - デリダ（脱構築）
- `wittgenstein` - ウィトゲンシュタイン（言語哲学）
- `jung` - ユング（分析心理学）
- `dewey` - デューイ（プラグマティズム）
- `deleuze` - ドゥルーズ（差異の哲学）
- `kierkegaard` - キルケゴール（実存主義）
- `lacan` - ラカン（精神分析）
- `levinas` - レヴィナス（他者の倫理）
- `badiou` - バディウ（数学的存在論）
- `peirce` - パース（記号論）
- `merleau_ponty` - メルロ＝ポンティ（身体の現象学）
- `arendt` - アーレント（政治哲学）

### 東洋哲学
- `watsuji` - 和辻哲郎（間柄の倫理）
- `wabi_sabi` - 侘び寂び（日本美学）
- `confucius` - 孔子（儒教）
- `zhuangzi` - 荘子（道教）

## 📊 出力メトリクス

Po_coreは3つの主要なテンソルメトリクスを計算します：

- **Freedom Pressure (自由の圧力)**: 応答の責任重量を測定
- **Semantic Delta (意味の変化)**: 意味の進化を追跡
- **Blocked Tensor (ブロックされたテンソル)**: 何が言われなかったかを記録

## 🎯 使用ケース

### 1. 倫理的決定支援

```python
po = PoSelf(philosophers=["aristotle", "levinas", "confucius"])
response = po.generate("この状況で正しい行動は何か？")
```

### 2. 哲学的探究

```python
po = PoSelf(philosophers=["heidegger", "sartre", "kierkegaard"])
response = po.generate("存在とは何か？")
```

### 3. 美学的分析

```python
po = PoSelf(philosophers=["nietzsche", "wabi_sabi", "dewey"])
response = po.generate("この作品の美しさは何か？")
```

### 4. 言語と意味の探究

```python
po = PoSelf(philosophers=["wittgenstein", "derrida", "peirce"])
response = po.generate("この言葉の意味は何か？")
```

## 🔧 高度な使用法

### トレース機能の活用

```python
from po_core.po_self import PoSelf

# トレース有効でインスタンス作成（デフォルト）
po = PoSelf(enable_trace=True)
response = po.generate("正義とは何か？")

# トレースログを確認
print(response.log)
```

### 複数セッションの管理

```python
# セッション1: 倫理的問い
ethical_po = PoSelf(philosophers=["aristotle", "levinas"])
ethical_response = ethical_po.generate("善とは何か？")

# セッション2: 実存的問い
existential_po = PoSelf(philosophers=["sartre", "heidegger"])
existential_response = existential_po.generate("自由とは何か？")
```

## 📝 ライセンス

MIT License - 自由に使用、改変、配布できます。

## 🤝 貢献

フィードバックや改善提案は大歓迎です！
- Issues: [GitHub Issues](https://github.com/hiroshitanaka-creator/Po_core/issues)
- Discussions: [GitHub Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions)

---

**🐷🎈 Flying Pig Philosophy**: 豚は飛べないと言われています。でも、哲学という風船をつければ飛べるかもしれません。
