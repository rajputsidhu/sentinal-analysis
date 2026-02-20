"""
Sentinel-AI — FastAPI Application Entry Point
CORS, router mounting, static file serving, and startup banner.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.routes import chat, sessions, health
from app.utils.logger import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    log.info("=" * 60)
    log.info("  🛡️  Sentinel-AI Security Gateway")
    log.info("=" * 60)
    log.info(f"  Mode:      {settings.analysis_mode}")
    log.info(f"  Model:     {settings.openai_model}")
    log.info(f"  Dry-run:   {settings.dry_run}")
    log.info(f"  Warn at:   {settings.threat_threshold_warn}")
    log.info(f"  Block at:  {settings.threat_threshold_block}")
    log.info(f"  Port:      {settings.port}")
    log.info("=" * 60)

    if settings.dry_run:
        log.warn("Running in DRY-RUN mode — no real LLM calls will be made")
        log.warn("Set OPENAI_API_KEY in .env for production use")

    yield

    # Shutdown
    log.info("Sentinel-AI shutting down")


app = FastAPI(
    title="Sentinel-AI Security Gateway",
    description="Middleware API gateway that intercepts and analyzes LLM traffic for security threats.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount API Routers ───────────────────────────────────────────

app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(sessions.router, prefix="/api", tags=["Sessions"])
app.include_router(health.router, prefix="/api", tags=["Health"])

# ── Serve Frontend Static Files ─────────────────────────────────

_frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

if os.path.isdir(_frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(_frontend_dist, "assets")), name="assets")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(_frontend_dist, "index.html"))

    @app.get("/{path:path}")
    async def serve_frontend_fallback(path: str):
        """SPA fallback — serve index.html for all non-API routes."""
        file_path = os.path.join(_frontend_dist, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(_frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "service": "Sentinel-AI Security Gateway",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs",
            "health": "/api/health",
        }
