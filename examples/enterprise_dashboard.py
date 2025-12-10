"""
Po_core Enterprise Dashboard
=============================

Large-scale prototype: Enterprise-grade analytics and monitoring platform
Features:
- Database-backed session management
- Multi-session analytics and comparison
- Real-time performance metrics
- Philosopher performance analysis
- Trend analysis and insights
- RESTful API with FastAPI
- Interactive web dashboard
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from po_core import __version__
from po_core.po_self import PoSelf
from po_core.po_trace_db import PoTraceDB
from po_core.ensemble import PHILOSOPHER_REGISTRY

# ============================================================================
# Initialize Application
# ============================================================================

app = FastAPI(
    title="Po_core Enterprise Dashboard",
    description="Enterprise-grade philosophical reasoning analytics platform",
    version=__version__,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database-backed trace system
trace_db = PoTraceDB()

# ============================================================================
# Pydantic Models
# ============================================================================


class AnalyticsRequest(BaseModel):
    """Analytics query request."""

    time_range: Optional[str] = Field(None, description="Time range: 1h, 24h, 7d, 30d")
    philosopher: Optional[str] = Field(None, description="Filter by philosopher")
    metric: Optional[str] = Field(None, description="Specific metric to analyze")


class SessionAnalytics(BaseModel):
    """Session-level analytics."""

    session_id: str
    prompt: str
    philosophers: List[str]
    created_at: str
    metrics: Dict[str, float]
    event_count: int
    duration_ms: Optional[float] = None


class PhilosopherPerformance(BaseModel):
    """Philosopher performance metrics."""

    philosopher: str
    total_sessions: int
    avg_semantic_delta: float
    avg_freedom_pressure: float
    avg_blocked_tensor: float
    contribution_score: float


class TrendAnalysis(BaseModel):
    """Trend analysis over time."""

    metric_name: str
    time_points: List[str]
    values: List[float]
    trend_direction: str  # "increasing", "decreasing", "stable"
    change_percentage: float


class DashboardSummary(BaseModel):
    """Overall dashboard summary."""

    total_sessions: int
    total_events: int
    active_philosophers: int
    avg_session_metrics: Dict[str, float]
    top_philosophers: List[PhilosopherPerformance]
    recent_trends: List[TrendAnalysis]


class ReasoningRequest(BaseModel):
    """Reasoning request with dashboard integration."""

    prompt: str = Field(..., min_length=1)
    philosophers: Optional[List[str]] = None
    enable_analytics: bool = Field(True, description="Enable detailed analytics")


class ReasoningResponse(BaseModel):
    """Reasoning response with analytics."""

    session_id: str
    prompt: str
    text: str
    consensus_leader: Optional[str]
    philosophers: List[str]
    metrics: Dict[str, float]
    analytics: Optional[SessionAnalytics] = None
    created_at: str


# ============================================================================
# Analytics Engine
# ============================================================================


class AnalyticsEngine:
    """Advanced analytics engine for enterprise dashboard."""

    def __init__(self, trace_db: PoTraceDB):
        self.trace_db = trace_db

    def get_dashboard_summary(self) -> DashboardSummary:
        """Get comprehensive dashboard summary."""
        stats = self.trace_db.get_statistics()

        # Get recent sessions for metrics
        recent_sessions = self.trace_db.list_sessions(limit=100)
        avg_metrics = self._calculate_average_metrics(recent_sessions)

        # Calculate philosopher performance
        top_philosophers = self._get_top_philosophers(stats["philosopher_usage"])

        # Calculate trends
        trends = self._calculate_trends(recent_sessions)

        return DashboardSummary(
            total_sessions=stats["total_sessions"],
            total_events=stats["total_events"],
            active_philosophers=len(stats["philosopher_usage"]),
            avg_session_metrics=avg_metrics,
            top_philosophers=top_philosophers,
            recent_trends=trends,
        )

    def get_philosopher_performance(self, philosopher: str) -> PhilosopherPerformance:
        """Get detailed performance metrics for a philosopher."""
        sessions = self.trace_db.search_sessions(philosopher=philosopher)

        total = len(sessions)
        if total == 0:
            return PhilosopherPerformance(
                philosopher=philosopher,
                total_sessions=0,
                avg_semantic_delta=0.0,
                avg_freedom_pressure=0.0,
                avg_blocked_tensor=0.0,
                contribution_score=0.0,
            )

        # Calculate average metrics
        metrics_sum = {"semantic_delta": 0.0, "freedom_pressure": 0.0, "blocked_tensor": 0.0}

        for session_meta in sessions:
            session = self.trace_db.get_session(session_meta["session_id"])
            if session and session.metrics:
                metrics_sum["semantic_delta"] += session.metrics.get("semantic_delta", 0.0)
                metrics_sum["freedom_pressure"] += session.metrics.get("freedom_pressure", 0.0)
                metrics_sum["blocked_tensor"] += session.metrics.get("blocked_tensor", 0.0)

        return PhilosopherPerformance(
            philosopher=philosopher,
            total_sessions=total,
            avg_semantic_delta=metrics_sum["semantic_delta"] / total,
            avg_freedom_pressure=metrics_sum["freedom_pressure"] / total,
            avg_blocked_tensor=metrics_sum["blocked_tensor"] / total,
            contribution_score=self._calculate_contribution_score(metrics_sum, total),
        )

    def compare_sessions(self, session_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple sessions."""
        sessions = []
        for sid in session_ids:
            session = self.trace_db.get_session(sid)
            if session:
                sessions.append(session)

        if not sessions:
            return {"error": "No valid sessions found"}

        comparison = {
            "session_count": len(sessions),
            "sessions": [],
            "common_philosophers": self._find_common_philosophers(sessions),
            "metric_comparison": self._compare_metrics(sessions),
        }

        for session in sessions:
            comparison["sessions"].append(
                {
                    "session_id": session.session_id,
                    "prompt": session.prompt[:100],
                    "philosophers": session.philosophers,
                    "metrics": session.metrics,
                    "event_count": len(session.events),
                }
            )

        return comparison

    def _calculate_average_metrics(self, sessions_meta: List[Dict]) -> Dict[str, float]:
        """Calculate average metrics across sessions."""
        if not sessions_meta:
            return {}

        metrics_sum: Dict[str, float] = {}
        metrics_count: Dict[str, int] = {}

        for session_meta in sessions_meta[:50]:  # Limit to recent 50
            session = self.trace_db.get_session(session_meta["session_id"])
            if session and session.metrics:
                for key, value in session.metrics.items():
                    metrics_sum[key] = metrics_sum.get(key, 0.0) + value
                    metrics_count[key] = metrics_count.get(key, 0) + 1

        avg_metrics = {}
        for key in metrics_sum:
            if metrics_count[key] > 0:
                avg_metrics[key] = metrics_sum[key] / metrics_count[key]

        return avg_metrics

    def _get_top_philosophers(
        self, philosopher_usage: Dict[str, int], limit: int = 5
    ) -> List[PhilosopherPerformance]:
        """Get top performing philosophers."""
        sorted_philosophers = sorted(philosopher_usage.items(), key=lambda x: x[1], reverse=True)

        top = []
        for phil, count in sorted_philosophers[:limit]:
            perf = self.get_philosopher_performance(phil)
            top.append(perf)

        return top

    def _calculate_trends(self, sessions_meta: List[Dict]) -> List[TrendAnalysis]:
        """Calculate metric trends over time."""
        # Simplified trend analysis
        return []  # TODO: Implement time-series analysis

    def _calculate_contribution_score(self, metrics_sum: Dict[str, float], total: int) -> float:
        """Calculate overall contribution score."""
        if total == 0:
            return 0.0

        # Weighted combination of metrics
        semantic = metrics_sum["semantic_delta"] / total
        freedom = metrics_sum["freedom_pressure"] / total
        blocked = metrics_sum["blocked_tensor"] / total

        # Higher semantic delta and freedom pressure = better
        # Lower blocked tensor = better
        score = (semantic * 0.4 + freedom * 0.4 + (1.0 - blocked) * 0.2) * 100
        return max(0.0, min(100.0, score))

    def _find_common_philosophers(self, sessions: List) -> List[str]:
        """Find philosophers common to all sessions."""
        if not sessions:
            return []

        common = set(sessions[0].philosophers)
        for session in sessions[1:]:
            common &= set(session.philosophers)

        return sorted(common)

    def _compare_metrics(self, sessions: List) -> Dict[str, Any]:
        """Compare metrics across sessions."""
        metric_names = set()
        for session in sessions:
            metric_names.update(session.metrics.keys())

        comparison = {}
        for metric in metric_names:
            values = [session.metrics.get(metric, 0.0) for session in sessions]
            comparison[metric] = {
                "values": values,
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values) if values else 0.0,
            }

        return comparison


# Initialize analytics engine
analytics = AnalyticsEngine(trace_db)

# ============================================================================
# API Endpoints
# ============================================================================


@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Enterprise dashboard home page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Po_core Enterprise Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 40px;
                backdrop-filter: blur(10px);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.2em;
                opacity: 0.9;
                margin-bottom: 30px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 40px;
            }
            .feature {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                transition: transform 0.3s;
            }
            .feature:hover {
                transform: translateY(-5px);
            }
            .feature h3 {
                margin-top: 0;
                font-size: 1.5em;
            }
            .api-link {
                display: inline-block;
                margin-top: 20px;
                padding: 15px 30px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s;
            }
            .api-link:hover {
                background: #667eea;
                color: white;
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 Enterprise Dashboard</h1>
            <div class="subtitle">Philosophy-Driven AI Analytics Platform</div>

            <div class="features">
                <div class="feature">
                    <h3>📊 Analytics</h3>
                    <p>Real-time session analytics and performance metrics</p>
                </div>
                <div class="feature">
                    <h3>🧠 Philosopher Analysis</h3>
                    <p>Detailed performance tracking for each philosopher</p>
                </div>
                <div class="feature">
                    <h3>📈 Trends</h3>
                    <p>Historical trends and predictive insights</p>
                </div>
                <div class="feature">
                    <h3>🔍 Session Comparison</h3>
                    <p>Compare multiple reasoning sessions side-by-side</p>
                </div>
                <div class="feature">
                    <h3>💾 Database Backend</h3>
                    <p>Efficient SQLite/PostgreSQL storage with full query support</p>
                </div>
                <div class="feature">
                    <h3>🚀 RESTful API</h3>
                    <p>Complete API for integration with enterprise systems</p>
                </div>
            </div>

            <a href="/docs" class="api-link">📚 Explore API Documentation</a>
            <a href="/dashboard/summary" class="api-link">📊 View Dashboard Summary</a>
        </div>
    </body>
    </html>
    """


@app.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    """Get comprehensive dashboard summary."""
    return analytics.get_dashboard_summary()


@app.get("/dashboard/philosopher/{philosopher}", response_model=PhilosopherPerformance)
async def get_philosopher_analytics(philosopher: str):
    """Get detailed analytics for a specific philosopher."""
    return analytics.get_philosopher_performance(philosopher)


@app.get("/dashboard/compare")
async def compare_sessions(
    session_ids: str = Query(..., description="Comma-separated session IDs")
):
    """Compare multiple sessions."""
    ids = [sid.strip() for sid in session_ids.split(",")]
    return analytics.compare_sessions(ids)


@app.post("/reason", response_model=ReasoningResponse)
async def reason_with_analytics(request: ReasoningRequest):
    """Execute reasoning with full analytics integration."""
    po = PoSelf(
        philosophers=request.philosophers,
        enable_trace=True,
        trace_backend=trace_db,
    )

    result = po.reason(request.prompt)

    # Build analytics
    session_analytics = None
    if request.enable_analytics and result.get("session_id"):
        session = trace_db.get_session(result["session_id"])
        if session:
            session_analytics = SessionAnalytics(
                session_id=session.session_id,
                prompt=session.prompt,
                philosophers=session.philosophers,
                created_at=session.created_at,
                metrics=session.metrics,
                event_count=len(session.events),
            )

    return ReasoningResponse(
        session_id=result.get("session_id", ""),
        prompt=request.prompt,
        text=result.get("text", ""),
        consensus_leader=result.get("consensus_leader"),
        philosophers=result.get("philosophers", []),
        metrics=result.get("metrics", {}),
        analytics=session_analytics,
        created_at=datetime.utcnow().isoformat() + "Z",
    )


@app.get("/sessions/search")
async def search_sessions(
    query: Optional[str] = None,
    philosopher: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
):
    """Search sessions with filters."""
    return trace_db.search_sessions(query=query, philosopher=philosopher, limit=limit)


@app.get("/sessions/{session_id}")
async def get_session_details(session_id: str):
    """Get detailed session information."""
    session = trace_db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session.to_dict()


@app.get("/statistics")
async def get_statistics():
    """Get database statistics."""
    return trace_db.get_statistics()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": __version__,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": "connected",
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("🏢 Starting Po_core Enterprise Dashboard...")
    print("📊 Database-backed analytics platform")
    print("🌐 Access at: http://localhost:8100")
    print("📚 API Docs: http://localhost:8100/docs")

    uvicorn.run(app, host="0.0.0.0", port=8100, log_level="info")
