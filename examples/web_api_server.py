"""
Po_core Web API Server
======================

FastAPIベースのRESTful APIサーバー
哲学的推論をWeb APIとして提供
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from po_core import __version__
from po_core.po_self import PoSelf
from po_core.ensemble import PHILOSOPHER_REGISTRY


# ============================================================================
# Pydantic Models
# ============================================================================

class PromptRequest(BaseModel):
    """推論リクエスト"""
    prompt: str = Field(..., min_length=1, description="質問またはプロンプト")
    philosophers: Optional[List[str]] = Field(
        None,
        description="使用する哲学者のリスト（省略時はデフォルト）"
    )
    enable_trace: bool = Field(True, description="トレース機能を有効化")


class PromptResponse(BaseModel):
    """推論レスポンス"""
    session_id: str
    prompt: str
    text: str
    consensus_leader: Optional[str]
    philosophers: List[str]
    metrics: Dict[str, float]
    responses: List[Dict]
    created_at: str


class SessionSummary(BaseModel):
    """セッションサマリー"""
    session_id: str
    prompt: str
    consensus_leader: Optional[str]
    created_at: str
    metrics: Dict[str, float]


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str
    version: str
    timestamp: str


# ============================================================================
# In-Memory Session Storage
# ============================================================================

class SessionStore:
    """セッション履歴の保存（メモリ内）"""

    def __init__(self):
        self.sessions: Dict[str, PromptResponse] = {}

    def save(self, session: PromptResponse):
        """セッションを保存"""
        self.sessions[session.session_id] = session

    def get(self, session_id: str) -> Optional[PromptResponse]:
        """セッションを取得"""
        return self.sessions.get(session_id)

    def list_all(self) -> List[SessionSummary]:
        """全セッションのサマリーを取得"""
        summaries = []
        for session in self.sessions.values():
            summaries.append(SessionSummary(
                session_id=session.session_id,
                prompt=session.prompt,
                consensus_leader=session.consensus_leader,
                created_at=session.created_at,
                metrics=session.metrics
            ))
        return sorted(summaries, key=lambda x: x.created_at, reverse=True)

    def count(self) -> int:
        """セッション数を取得"""
        return len(self.sessions)

    def clear(self):
        """全セッションをクリア"""
        self.sessions.clear()


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Po_core API",
    description="Philosophy-Driven AI System - RESTful API",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# セッションストア
session_store = SessionStore()


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """ルートエンドポイント - シンプルなWebインターフェース"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Po_core - Philosophy-Driven AI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-style: italic;
            }
            .input-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 600;
            }
            input[type="text"], textarea, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            textarea {
                min-height: 100px;
                resize: vertical;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                cursor: pointer;
                width: 100%;
                font-weight: 600;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:active {
                transform: translateY(0);
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                display: none;
            }
            .result.show {
                display: block;
            }
            .result h3 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .metric {
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .metric-label {
                color: #666;
                font-size: 14px;
                margin-bottom: 5px;
            }
            .metric-value {
                color: #667eea;
                font-size: 24px;
                font-weight: 700;
            }
            .response-text {
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-top: 15px;
                line-height: 1.6;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .loader {
                display: none;
                text-align: center;
                margin: 20px 0;
            }
            .loader.show {
                display: block;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .api-links {
                margin-top: 30px;
                text-align: center;
            }
            .api-links a {
                color: #667eea;
                text-decoration: none;
                margin: 0 15px;
                font-weight: 600;
            }
            .api-links a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐷🎈 Po_core</h1>
            <p class="subtitle">Philosophy-Driven AI System</p>

            <div class="input-group">
                <label for="prompt">質問・プロンプト</label>
                <textarea id="prompt" placeholder="例: 真の自由とは何か？"></textarea>
            </div>

            <div class="input-group">
                <label for="philosophers">哲学者（カンマ区切り、空欄でデフォルト）</label>
                <input type="text" id="philosophers" placeholder="例: aristotle, nietzsche, sartre">
            </div>

            <button onclick="submitPrompt()">推論を実行</button>

            <div class="loader" id="loader">
                <div class="spinner"></div>
                <p>哲学者たちが推論中...</p>
            </div>

            <div class="result" id="result">
                <h3>推論結果</h3>
                <p><strong>コンセンサスリーダー:</strong> <span id="leader"></span></p>
                <p><strong>参加哲学者:</strong> <span id="philosophers-list"></span></p>

                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">Freedom Pressure</div>
                        <div class="metric-value" id="fp">-</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Semantic Delta</div>
                        <div class="metric-value" id="sd">-</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Blocked Tensor</div>
                        <div class="metric-value" id="bt">-</div>
                    </div>
                </div>

                <div class="response-text" id="response-text"></div>
            </div>

            <div class="api-links">
                <a href="/docs" target="_blank">📚 API Documentation</a>
                <a href="/api/v1/philosophers">🧠 利用可能な哲学者</a>
                <a href="/api/v1/sessions">📊 セッション履歴</a>
            </div>
        </div>

        <script>
            async function submitPrompt() {
                const prompt = document.getElementById('prompt').value.trim();
                if (!prompt) {
                    alert('質問を入力してください');
                    return;
                }

                const philosophersInput = document.getElementById('philosophers').value.trim();
                const philosophers = philosophersInput ? philosophersInput.split(',').map(p => p.trim()) : null;

                document.getElementById('loader').classList.add('show');
                document.getElementById('result').classList.remove('show');

                try {
                    const response = await fetch('/api/v1/prompt', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            prompt: prompt,
                            philosophers: philosophers,
                            enable_trace: true
                        })
                    });

                    if (!response.ok) {
                        throw new Error('API request failed');
                    }

                    const data = await response.json();

                    document.getElementById('leader').textContent = data.consensus_leader || 'Unknown';
                    document.getElementById('philosophers-list').textContent = data.philosophers.join(', ');
                    document.getElementById('fp').textContent = data.metrics.freedom_pressure.toFixed(2);
                    document.getElementById('sd').textContent = data.metrics.semantic_delta.toFixed(2);
                    document.getElementById('bt').textContent = data.metrics.blocked_tensor.toFixed(2);
                    document.getElementById('response-text').textContent = data.text;

                    document.getElementById('result').classList.add('show');
                } catch (error) {
                    alert('エラーが発生しました: ' + error.message);
                } finally {
                    document.getElementById('loader').classList.remove('show');
                }
            }

            // Enterキーでの送信（Shift+Enterで改行）
            document.getElementById('prompt').addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    submitPrompt();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """ヘルスチェック"""
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/api/v1/philosophers")
async def list_philosophers():
    """利用可能な哲学者のリストを取得"""
    philosophers = []
    for key, cls in PHILOSOPHER_REGISTRY.items():
        instance = cls()
        philosophers.append({
            "key": key,
            "name": instance.name,
            "description": instance.description
        })
    return {
        "total": len(philosophers),
        "philosophers": sorted(philosophers, key=lambda x: x["name"])
    }


@app.post("/api/v1/prompt", response_model=PromptResponse)
async def generate_response(request: PromptRequest):
    """プロンプトに対して哲学的推論を実行"""
    try:
        # Po_selfインスタンスを作成
        po = PoSelf(
            philosophers=request.philosophers,
            enable_trace=request.enable_trace
        )

        # 推論を実行
        response = po.generate(request.prompt)

        # セッションIDを生成（トレースからまたは新規）
        session_id = response.log.get("session_id", str(uuid4()))

        # レスポンスを構築
        prompt_response = PromptResponse(
            session_id=session_id,
            prompt=response.prompt,
            text=response.text,
            consensus_leader=response.consensus_leader,
            philosophers=response.philosophers,
            metrics=response.metrics,
            responses=response.responses,
            created_at=datetime.utcnow().isoformat() + "Z"
        )

        # セッションを保存
        session_store.save(prompt_response)

        return prompt_response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/v1/sessions")
async def list_sessions(
    limit: int = Query(10, ge=1, le=100, description="取得するセッション数")
):
    """セッション履歴のリストを取得"""
    all_sessions = session_store.list_all()
    return {
        "total": len(all_sessions),
        "sessions": all_sessions[:limit]
    }


@app.get("/api/v1/sessions/{session_id}", response_model=PromptResponse)
async def get_session(session_id: str):
    """特定のセッションの詳細を取得"""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.delete("/api/v1/sessions")
async def clear_sessions():
    """全セッション履歴をクリア"""
    count = session_store.count()
    session_store.clear()
    return {
        "message": "All sessions cleared",
        "cleared_count": count
    }


@app.get("/api/v1/stats")
async def get_stats():
    """統計情報を取得"""
    all_sessions = session_store.list_all()

    if not all_sessions:
        return {
            "total_sessions": 0,
            "average_metrics": None,
            "most_common_leader": None
        }

    # 平均メトリクスを計算
    total_fp = sum(s.metrics.get("freedom_pressure", 0) for s in all_sessions)
    total_sd = sum(s.metrics.get("semantic_delta", 0) for s in all_sessions)
    total_bt = sum(s.metrics.get("blocked_tensor", 0) for s in all_sessions)
    count = len(all_sessions)

    # 最も多いリーダーを見つける
    leaders = [s.consensus_leader for s in all_sessions if s.consensus_leader]
    most_common_leader = max(set(leaders), key=leaders.count) if leaders else None

    return {
        "total_sessions": count,
        "average_metrics": {
            "freedom_pressure": round(total_fp / count, 2),
            "semantic_delta": round(total_sd / count, 2),
            "blocked_tensor": round(total_bt / count, 2)
        },
        "most_common_leader": most_common_leader
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("🐷🎈 Po_core Web API Server")
    print(f"Version: {__version__}")
    print("=" * 70)
    print()
    print("Starting server at http://localhost:8000")
    print("  - Web Interface: http://localhost:8000")
    print("  - API Docs: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print()

    uvicorn.run(app, host="0.0.0.0", port=8000)
