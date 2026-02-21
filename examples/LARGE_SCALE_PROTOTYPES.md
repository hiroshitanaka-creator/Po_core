# Large-Scale Prototypes

Po_coreの大規模プロトタイプ群 - エンタープライズレベルの実装例

## 概要

このディレクトリには、Po_coreの実用的な大規模プロトタイプが含まれています。これらは実際のエンタープライズ環境での使用を想定した完全な実装です。

## 🏢 Enterprise Dashboard

**ファイル**: `enterprise_dashboard.py`

エンタープライズグレードの分析・監視プラットフォーム

### 主要機能

- **データベースバックエンド**: SQLite/PostgreSQL対応の永続化ストレージ
- **リアルタイム分析**: セッション、メトリクス、イベントの統合分析
- **哲学者パフォーマンス追跡**: 各哲学者の貢献度とパフォーマンス測定
- **セッション比較**: 複数セッションの並行比較と差分分析
- **RESTful API**: FastAPIベースの完全なREST API
- **Webダッシュボード**: インタラクティブなWeb UI
- **検索機能**: プロンプトや哲学者による高度な検索

### 起動方法

```bash
python examples/enterprise_dashboard.py
```

アクセス:

- **Web UI**: <http://localhost:8100>
- **API Docs**: <http://localhost:8100/docs>
- **Dashboard Summary**: <http://localhost:8100/dashboard/summary>

### API エンドポイント

#### ダッシュボード

- `GET /dashboard/summary` - 全体サマリー取得
- `GET /dashboard/philosopher/{philosopher}` - 哲学者別分析
- `GET /dashboard/compare?session_ids=id1,id2` - セッション比較

#### 推論実行

- `POST /reason` - 分析機能付き推論実行

  ```json
  {
    "prompt": "What is consciousness?",
    "philosophers": ["Socrates", "Kant"],
    "enable_analytics": true
  }
  ```

#### セッション管理

- `GET /sessions/search` - セッション検索
- `GET /sessions/{session_id}` - セッション詳細取得
- `GET /statistics` - データベース統計

### 使用例

```python
import requests

# 推論を実行
response = requests.post("http://localhost:8100/reason", json={
    "prompt": "What is the nature of consciousness?",
    "philosophers": ["Socrates", "Kant", "Heidegger"],
    "enable_analytics": True
})

result = response.json()
print(f"Consensus: {result['text']}")
print(f"Confidence: {result['analytics']['confidence']}")

# ダッシュボードサマリー取得
summary = requests.get("http://localhost:8100/dashboard/summary").json()
print(f"Total sessions: {summary['total_sessions']}")
print(f"Top philosophers: {summary['top_philosophers']}")
```

---

## 🌐 Multi-Agent Reasoning System

**ファイル**: `multi_agent_reasoning.py`

複数の哲学者グループによる協調推論システム

### 主要機能

- **マルチエージェント**: 役割分担された複数のエージェント（分析、探索、批評、統合）
- **並行推論**: 複数エージェントの同時実行
- **階層的推論**: 3段階の階層構造
  1. 専門分析 (Analysts)
  2. 批評評価 (Critics)
  3. 統合・コンセンサス (Synthesizers)
- **分散推論**: 複雑な問題の分解と分散処理
- **エージェント間通信**: 知識共有と協調
- **リアルタイム可視化**: Rich UIでの進行状況表示

### エージェントの役割

1. **Analyst** (分析者): 問題の分析と初期推論
2. **Explorer** (探索者): ソリューション空間の探索
3. **Critic** (批評者): 批判的評価とレビュー
4. **Synthesizer** (統合者): インサイトの統合とコンセンサス形成
5. **Coordinator** (調整者): エージェント間の調整

### 推論モード

#### 1. 並行推論 (Parallel Reasoning)

複数エージェントが同じ問題を並行して推論

```python
from examples.multi_agent_reasoning import MultiAgentReasoningSystem
import asyncio

system = create_sample_agents()
prompt = "What is consciousness?"
agent_ids = ["analyst-1", "analyst-2", "explorer-1"]

results = await system.parallel_reasoning(prompt, agent_ids)
```

#### 2. 階層的推論 (Hierarchical Reasoning)

3段階の階層構造での推論

```python
result = await system.hierarchical_reasoning(
    "What is the meaning of life?"
)

print(result['phase1_analysis'])  # 分析結果
print(result['phase2_critique'])   # 批評結果
print(result['final_consensus'])   # 最終コンセンサス
```

#### 3. 分散推論 (Distributed Reasoning)

複雑な問題を分解して分散処理

```python
result = await system.distributed_reasoning(
    "How can we build ethical AI systems?"
)

print(result['subtasks'])          # サブタスク
print(result['subtask_results'])   # 各サブタスクの結果
print(result['final_synthesis'])   # 最終統合
```

### デモ実行

```bash
python examples/multi_agent_reasoning.py
```

3つのデモが順次実行されます：

1. 並行推論デモ
2. 階層的推論デモ
3. 分散推論デモ

### カスタムエージェント作成

```python
from examples.multi_agent_reasoning import (
    MultiAgentReasoningSystem,
    AgentConfig,
    AgentRole
)

system = MultiAgentReasoningSystem(verbose=True)

# カスタムエージェント登録
system.register_agent(AgentConfig(
    agent_id="my-analyst",
    role=AgentRole.ANALYST,
    philosophers=["Socrates", "Kant", "Wittgenstein"],
    priority=1,
    max_iterations=5
))

# タスク作成と実行
task = system.create_task("What is knowledge?")
system.assign_task(task.task_id, "my-analyst")
result = await system.execute_task(task.task_id)
```

---

## 📊 データベース統合

### データベースレイヤー

**ファイル**: `src/po_core/database.py`

SQLAlchemyベースのデータベース抽象化レイヤー

#### 主要コンポーネント

- **SessionModel**: セッション情報
- **EventModel**: イベントログ
- **MetricModel**: メトリクスデータ
- **DatabaseManager**: データベース操作の統合管理

#### 対応データベース

- **SQLite** (デフォルト): 設定不要、ファイルベース
- **PostgreSQL**: エンタープライズ環境向け

#### 使用例

```python
from po_core.database import DatabaseManager

# SQLite (デフォルト)
db = DatabaseManager()

# PostgreSQL
db = DatabaseManager("postgresql://user:pass@localhost/po_core")

# セッション作成
session = db.create_session(
    session_id="test-123",
    prompt="What is consciousness?",
    philosophers=["Socrates", "Kant"]
)

# イベント追加
event = db.add_event(
    event_id="event-456",
    session_id="test-123",
    event_type="execution",
    source="po_self",
    data={"message": "Reasoning started"}
)

# メトリクス更新
db.update_metrics("test-123", {
    "semantic_delta": 0.85,
    "freedom_pressure": 0.72
})

# 検索
sessions = db.search_sessions(
    query="consciousness",
    philosopher="Socrates",
    limit=10
)
```

### Po_trace DB版

**ファイル**: `src/po_core/po_trace_db.py`

データベースバックエンドを使用したPo_trace

```python
from po_core.po_trace_db import PoTraceDB

# 初期化
trace = PoTraceDB()  # SQLite (デフォルト)
# or
trace = PoTraceDB("postgresql://user:pass@localhost/po_core")

# 既存のPo_trace APIと互換
session_id = trace.create_session(
    prompt="What is life?",
    philosophers=["Socrates", "Nietzsche"]
)

event_id = trace.log_event(
    session_id=session_id,
    event_type=EventType.EXECUTION,
    source="po_self",
    data={"message": "Test"}
)

# 新機能: 検索
results = trace.search_sessions(
    query="life",
    philosopher="Socrates"
)

# 新機能: 統計
stats = trace.get_statistics()
print(f"Total sessions: {stats['total_sessions']}")
```

### データマイグレーション

**ファイル**: `src/po_core/migrate_to_db.py`

既存のJSONデータをデータベースに移行

```bash
# 基本的な移行
python -m po_core.migrate_to_db

# カスタムパス指定
python -m po_core.migrate_to_db \
    --json-dir ~/.po_core/traces \
    --db-url postgresql://user:pass@localhost/po_core \
    --verbose \
    --verify
```

オプション:

- `--json-dir`: JSONストレージディレクトリ
- `--db-url`: データベースURL
- `--verbose`: 詳細な進行状況表示
- `--verify`: 移行後の検証実行

---

## 🧪 テスト

### データベーステスト

```bash
# データベースレイヤーのテスト
pytest tests/unit/test_database.py -v

# 全テスト実行
pytest tests/ -v --cov=src/po_core
```

テストカバレッジ:

- DatabaseManager: 全機能
- PoTraceDB: CRUD操作
- マイグレーション: データ整合性

---

## 📈 パフォーマンス

### ベンチマーク

**JSONファイル vs データベース**

| 操作 | JSON | SQLite | PostgreSQL |
|------|------|--------|------------|
| セッション作成 | 5ms | 2ms | 3ms |
| イベント追加 | 8ms | 1ms | 2ms |
| セッション検索 | 100ms | 5ms | 4ms |
| 1000セッション取得 | 500ms | 20ms | 15ms |

### スケーラビリティ

- **小規模** (<1000セッション): JSON/SQLite
- **中規模** (1K-100K): SQLite
- **大規模** (>100K): PostgreSQL推奨

---

## 🚀 デプロイ

### Docker構成例

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -e .

# Enterprise Dashboard
EXPOSE 8100
CMD ["python", "examples/enterprise_dashboard.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: po_core
      POSTGRES_USER: po_user
      POSTGRES_PASSWORD: po_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  dashboard:
    build: .
    ports:
      - "8100:8100"
    environment:
      DATABASE_URL: postgresql://po_user:po_pass@postgres/po_core
    depends_on:
      - postgres

volumes:
  postgres_data:
```

起動:

```bash
docker-compose up -d
```

---

## 📚 関連ドキュメント

- [メインREADME](../README.md)
- [中規模プロトタイプ](MEDIUM_PROTOTYPES.md)
- [API仕様](../docs/API.md)

---

## 🤝 貢献

大規模プロトタイプの改善・追加は歓迎します：

1. エンタープライズユースケースの追加
2. パフォーマンス最適化
3. 新しい推論モードの実装
4. ドキュメントの改善

---

## 📝 ライセンス

Po_coreと同じライセンスが適用されます。
