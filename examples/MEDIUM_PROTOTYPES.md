# Po_core 中規模プロトタイプガイド 🚀

Po_coreの実用的な中規模プロトタイプの詳細ガイドです。

## 📋 目次

1. [Web API Server](#1-web-api-server)
2. [Batch Analyzer](#2-batch-analyzer)
3. [Philosopher Comparison Tool](#3-philosopher-comparison-tool)

---

## 1. Web API Server 🌐

FastAPIベースのRESTful APIサーバー。Webブラウザから哲学的推論を実行できます。

### インストール

```bash
# 必要な依存関係
pip install fastapi uvicorn pydantic
```

### 起動方法

```bash
python examples/web_api_server.py
```

サーバーが起動すると以下のURLでアクセスできます：
- **Webインターフェース**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要機能

#### 🌐 Webインターフェース

美しいグラデーションUIで哲学的推論を実行：
- リアルタイムで推論結果を表示
- メトリクスを視覚的に表示
- カスタム哲学者の選択が可能
- レスポンシブデザイン

#### 📡 RESTful API

完全なRESTful APIを提供：

**POST /api/v1/prompt** - 哲学的推論を実行

```bash
curl -X POST "http://localhost:8000/api/v1/prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "真の自由とは何か？",
    "philosophers": ["sartre", "nietzsche"],
    "enable_trace": true
  }'
```

レスポンス:
```json
{
  "session_id": "uuid-here",
  "prompt": "真の自由とは何か？",
  "text": "推論結果...",
  "consensus_leader": "Jean-Paul Sartre",
  "philosophers": ["sartre", "nietzsche"],
  "metrics": {
    "freedom_pressure": 0.85,
    "semantic_delta": 1.0,
    "blocked_tensor": 0.57
  },
  "responses": [...],
  "created_at": "2025-11-26T12:00:00Z"
}
```

**GET /api/v1/sessions** - セッション履歴を取得

```bash
curl "http://localhost:8000/api/v1/sessions?limit=10"
```

**GET /api/v1/sessions/{session_id}** - 特定セッションの詳細

```bash
curl "http://localhost:8000/api/v1/sessions/{session_id}"
```

**GET /api/v1/philosophers** - 利用可能な哲学者リスト

```bash
curl "http://localhost:8000/api/v1/philosophers"
```

レスポンス:
```json
{
  "total": 20,
  "philosophers": [
    {
      "key": "aristotle",
      "name": "Aristotle (Ἀριστοτέλης)",
      "description": "Ancient Greek philosopher focused on virtue ethics..."
    },
    ...
  ]
}
```

**GET /api/v1/stats** - 統計情報

```bash
curl "http://localhost:8000/api/v1/stats"
```

レスポンス:
```json
{
  "total_sessions": 42,
  "average_metrics": {
    "freedom_pressure": 0.78,
    "semantic_delta": 0.95,
    "blocked_tensor": 0.61
  },
  "most_common_leader": "Aristotle (Ἀριστοτέλης)"
}
```

**DELETE /api/v1/sessions** - セッション履歴をクリア

```bash
curl -X DELETE "http://localhost:8000/api/v1/sessions"
```

### Pythonクライアント例

```python
import requests

# APIベースURL
base_url = "http://localhost:8000"

# 推論を実行
response = requests.post(
    f"{base_url}/api/v1/prompt",
    json={
        "prompt": "美とは何か？",
        "philosophers": ["aristotle", "nietzsche", "wabi_sabi"],
        "enable_trace": True
    }
)

result = response.json()
print(f"Leader: {result['consensus_leader']}")
print(f"Metrics: {result['metrics']}")

# セッション履歴を取得
sessions = requests.get(f"{base_url}/api/v1/sessions").json()
print(f"Total sessions: {sessions['total']}")
```

### 機能詳細

#### セッション管理
- インメモリでセッション履歴を保存
- セッションIDで個別に取得可能
- 統計情報の自動計算

#### CORS対応
- すべてのオリジンからのリクエストを許可
- 開発環境での利用に最適

#### エラーハンドリング
- 適切なHTTPステータスコード
- 詳細なエラーメッセージ

---

## 2. Batch Analyzer 📦

複数の質問を一括処理し、結果を分析・エクスポートするツール。

### 実行方法

```bash
python examples/batch_analyzer.py
```

デモモードでは10個の哲学的問いを自動的に分析します。

### 主要機能

#### 📊 一括処理
- 複数の質問を効率的に処理
- 進捗バーで進行状況を表示
- バックグラウンドで並列処理（オプション）

#### 📈 統計分析
自動的に以下を計算：
- 平均メトリクス（Freedom Pressure, Semantic Delta, Blocked Tensor）
- リーダー分布（各哲学者がリーダーになった回数）
- 使用された哲学者の総数

#### 💾 データエクスポート

**JSON形式:**
```json
{
  "total_prompts": 10,
  "total_philosophers_used": 1,
  "average_metrics": {
    "freedom_pressure": 0.79,
    "semantic_delta": 1.00,
    "blocked_tensor": 0.60
  },
  "leader_distribution": {
    "Aristotle (Ἀριστοτέλης)": 10
  },
  "results": [...]
}
```

**CSV形式:**
```csv
Prompt,Consensus Leader,Freedom Pressure,Semantic Delta,Blocked Tensor,Philosopher Count,Response Length
真の自由とは何か？,Aristotle (Ἀριストοτέλης),0.79,1.0,0.6,3,542
...
```

### カスタム使用例

#### ファイルから質問を読み込む

```python
from batch_analyzer import BatchAnalyzer, load_prompts_from_file

# questions.txt (1行1質問)
prompts = load_prompts_from_file("questions.txt")

# バッチ分析を実行
analyzer = BatchAnalyzer(philosophers=["sartre", "heidegger"])
analyzer.analyze_batch(prompts, show_progress=True)

# サマリーを表示
analyzer.print_summary()

# 結果をエクスポート
analyzer.export_json("results.json")
analyzer.export_csv("results.csv")
```

#### カスタム哲学者で分析

```python
from batch_analyzer import BatchAnalyzer

# 倫理学者グループで分析
ethical_philosophers = ["aristotle", "levinas", "confucius"]
analyzer = BatchAnalyzer(philosophers=ethical_philosophers)

prompts = [
    "正義とは何か？",
    "善とは何か？",
    "道徳的決定をどう下すべきか？"
]

results = analyzer.analyze_batch(prompts)
report = analyzer.generate_report()

print(f"Average Freedom Pressure: {report.average_metrics['freedom_pressure']}")
print(f"Most Common Leader: {max(report.leader_distribution.items(), key=lambda x: x[1])}")
```

### ユースケース

1. **研究データ収集**
   - 大量の質問を処理してデータセットを作成
   - 哲学者の傾向を統計的に分析

2. **ベンチマークテスト**
   - 異なる哲学者グループの性能比較
   - メトリクスの分布を分析

3. **教育目的**
   - 学生の質問に対する複数の哲学的視点を一括取得
   - 比較教材の作成

---

## 3. Philosopher Comparison Tool 🔍

同じ質問に対する異なる哲学者の視点を詳細に比較。

### 実行方法

```bash
python examples/philosopher_comparison.py
```

インタラクティブメニューから選択：
1. グループ比較モード
2. 個別比較モード
3. 利用可能なグループ表示
4. すべて実行

### モード1: グループ比較

定義済みの哲学者グループ間で視点を比較。

#### 利用可能なグループ

| グループ | 哲学者 |
|---------|--------|
| **実存主義** | Sartre, Heidegger, Kierkegaard |
| **古典哲学** | Aristotle, Confucius, Wabi-Sabi |
| **現代哲学** | Wittgenstein, Derrida, Deleuze |
| **倫理学** | Aristotle, Levinas, Confucius |
| **現象学** | Heidegger, Merleau-Ponty, Sartre |
| **プラグマティズム** | Dewey, Peirce, Wittgenstein |
| **精神分析** | Jung, Lacan, Nietzsche |
| **東洋哲学** | Confucius, Zhuangzi, Watsuji, Wabi-Sabi |
| **西洋哲学** | Aristotle, Nietzsche, Sartre, Wittgenstein |
| **政治哲学** | Arendt, Confucius, Aristotle |

#### 使用例

```python
from philosopher_comparison import PhilosopherComparison

comparison = PhilosopherComparison()

# 3つのグループを比較
comparison.compare_groups(
    prompt="人生の意味とは何か？",
    groups=["実存主義", "古典哲学", "東洋哲学"]
)
```

出力:
- メトリクス比較テーブル
- 各グループの応答サマリー
- コンセンサスリーダー

### モード2: 個別比較

特定の哲学者を個別に比較。

#### 使用例

```python
comparison = PhilosopherComparison()

# 4人の哲学者を個別比較
comparison.compare_philosophers(
    prompt="真の自由とは何か？",
    philosophers=["sartre", "aristotle", "confucius", "nietzsche"]
)
```

出力:
- 個別メトリクス比較
- 各哲学者の詳細な推論
- 視点（Perspective）の違い
- 応答長の比較

### 高度な使用例

#### カスタムグループの定義

```python
from philosopher_comparison import PhilosopherComparison

comparison = PhilosopherComparison()

# カスタムグループを追加
comparison.PHILOSOPHER_GROUPS["カスタム"] = ["sartre", "nietzsche", "deleuze"]

# カスタムグループを使用
comparison.compare_groups(
    prompt="権力とは何か？",
    groups=["カスタム", "政治哲学"]
)
```

#### プログラマティックな比較

```python
# 全グループを比較
comparison = PhilosopherComparison()
comparison.compare_groups(
    prompt="真理とは何か？",
    groups=None  # 全グループ
)

# 応答データにアクセス
for group_name, data in comparison.responses.items():
    response = data["response"]
    print(f"{group_name}: FP={response.metrics['freedom_pressure']}")
```

### ユースケース

1. **教育・研究**
   - 異なる哲学的立場の理解
   - 比較哲学の教材作成
   - 学生への多角的視点の提示

2. **複雑な問題分析**
   - 倫理的ジレンマの多角的検討
   - 政策決定の哲学的基盤
   - 芸術作品の多様な解釈

3. **自己理解**
   - 自分の価値観と異なる視点の理解
   - 思考の幅を広げる
   - 新しい視座の発見

---

## 🎯 実践的なワークフロー例

### ワークフロー1: 研究プロジェクト

```bash
# 1. 質問リストを作成
cat > research_questions.txt << EOF
正義とは何か？
自由とは何か？
平等とは何か？
権利とは何か？
責任とは何か？
EOF

# 2. バッチ分析を実行
python -c "
from batch_analyzer import BatchAnalyzer, load_prompts_from_file
prompts = load_prompts_from_file('research_questions.txt')
analyzer = BatchAnalyzer(philosophers=['aristotle', 'arendt', 'confucius'])
analyzer.analyze_batch(prompts)
analyzer.export_json('research_results.json')
analyzer.export_csv('research_results.csv')
"

# 3. 結果を分析・可視化（別のツールで）
```

### ワークフロー2: 比較研究

```python
# 東洋vs西洋の哲学的視点を比較
from philosopher_comparison import PhilosopherComparison

comparison = PhilosopherComparison()

questions = [
    "幸福とは何か？",
    "調和とは何か？",
    "美徳とは何か？"
]

for question in questions:
    print(f"\n{'='*70}")
    print(f"Question: {question}")
    print('='*70)

    comparison.compare_groups(
        prompt=question,
        groups=["東洋哲学", "西洋哲学"]
    )
```

### ワークフロー3: Web APIとの連携

```python
import requests
import time

# Web APIサーバーを起動しておく
base_url = "http://localhost:8000"

# 複数の質問を送信
questions = [
    "愛とは何か？",
    "知識とは何か？",
    "存在とは何か？"
]

session_ids = []
for question in questions:
    response = requests.post(
        f"{base_url}/api/v1/prompt",
        json={"prompt": question}
    )
    result = response.json()
    session_ids.append(result['session_id'])
    time.sleep(1)  # レート制限対策

# 統計情報を取得
stats = requests.get(f"{base_url}/api/v1/stats").json()
print(f"Total sessions: {stats['total_sessions']}")
print(f"Average FP: {stats['average_metrics']['freedom_pressure']}")
print(f"Most common leader: {stats['most_common_leader']}")
```

---

## 🔧 トラブルシューティング

### Web APIサーバーが起動しない

```bash
# ポートが使用中の場合、別のポートで起動
python -c "
import uvicorn
from web_api_server import app
uvicorn.run(app, host='0.0.0.0', port=8080)
"
```

### 依存関係エラー

```bash
# 必要なパッケージを一括インストール
pip install fastapi uvicorn pydantic rich
```

### メモリ不足

```python
# バッチ分析でトレースを無効化
analyzer = BatchAnalyzer()
# Po_selfのenable_traceは内部で使用されているため、
# 大量処理の場合は小さなバッチに分割
```

---

## 📚 次のステップ

1. **カスタマイズ**
   - 独自の哲学者グループを定義
   - カスタムメトリクスの追加
   - エクスポート形式の拡張

2. **統合**
   - 他のツールとの連携
   - データベースへの保存
   - 可視化ツールの追加

3. **スケーリング**
   - 非同期処理の実装
   - キャッシング機能
   - 分散処理

---

**🐷🎈 Flying Pig Philosophy**

これらのプロトタイプは、Po_coreの哲学駆動型AIシステムの実用的な応用例です。
より大規模な実装へのステップとしてご活用ください。

*井の中の蛙、大海は知らずとも、大空を知る*
