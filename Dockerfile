# =============================================================================
# Po_core — Multi-stage Docker build
# =============================================================================
#
# Build:
#   docker build -t po-core:latest .
#
# Run:
#   docker run -p 8000:8000 -e PO_API_KEY=secret po-core:latest
#
# Stages:
#   builder — installs all dependencies into a venv
#   runtime — lean production image (copies venv from builder)
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: builder
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# System build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies first (layer-cache friendly)
COPY pyproject.toml requirements.txt ./
RUN pip install --upgrade pip wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy source and install package
COPY src/ ./src/
RUN pip install --no-cache-dir --no-deps -e .

# ---------------------------------------------------------------------------
# Stage 2: runtime
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="Po_core REST API" \
      org.opencontainers.image.description="Philosophy-driven AI deliberation via 39 philosopher personas" \
      org.opencontainers.image.source="https://github.com/hiroshitanaka-creator/Po_core" \
      org.opencontainers.image.licenses="MIT"

# Non-root user for security
RUN groupadd --gid 1001 pocore \
    && useradd --uid 1001 --gid pocore --shell /bin/bash --create-home pocore

WORKDIR /app

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source
COPY --from=builder /build/src ./src

# Config files
COPY src/po_core/config/ ./src/po_core/config/

# Runtime env vars (override via docker run -e or docker-compose)
ENV PO_HOST=0.0.0.0 \
    PO_PORT=8000 \
    PO_WORKERS=1 \
    PO_LOG_LEVEL=info \
    PO_SKIP_AUTH=false \
    PO_API_KEY="" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Shadow guard state dir (writable by non-root)
RUN mkdir -p /app/.po_core && chown pocore:pocore /app/.po_core
ENV PO_SHADOW_GUARD_STATE_PATH=/app/.po_core/shadow_guard_state.json

USER pocore

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PO_PORT}/v1/health')"

# Entry point
CMD ["python", "-m", "po_core.app.rest"]
