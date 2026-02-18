"""
CLI entry point: python -m po_core.app.rest
"""

from __future__ import annotations

import uvicorn

from po_core.app.rest.config import get_api_settings


def main() -> None:
    settings = get_api_settings()
    uvicorn.run(
        "po_core.app.rest.server:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        log_level=settings.log_level,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
