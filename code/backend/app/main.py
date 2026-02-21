"""
Sentinel-AI — FastAPI Entry Point
Main application setup with CORS, router mounting, database init, and startup banner.
"""

import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import init_db
from app.routes import analyze, sessions, health
from app.utils.logger import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # ── Startup ──
    log.info("=" * 60)
    log.info("  🛡️  Sentinel-AI Security Gateway v2")
    log.info("=" * 60)
    log.info(f"  Mode:      {settings.analysis_mode}")
    log.info(f"  Provider:  {settings.llm_provider}")
    model_name = {"openai": settings.openai_model, "gemini": settings.gemini_model, "groq": settings.groq_model}.get(settings.llm_provider, settings.openai_model)
    log.info(f"  Model:     {model_name}")
    log.info(f"  Embedding: {settings.embedding_model}")
    log.info(f"  Dry-run:   {settings.dry_run}")
    log.info(f"  Database:  {settings.database_url.split('://')[0]}")
    log.info(f"  Thresholds: allow<{settings.threshold_allow} warn<{settings.threshold_warn} rewrite<{settings.threshold_rewrite} block≥{settings.threshold_rewrite}")
    log.info(f"  Port:      {settings.port}")
    log.info("=" * 60)

    if settings.dry_run:
        log.warn("Running in DRY-RUN mode — no real LLM calls will be made")

    # Initialize database tables
    await init_db()
    log.info("Database initialized")

    yield

    # ── Shutdown ──
    log.info("Sentinel-AI shutting down")


app = FastAPI(
    title="Sentinel-AI Security Gateway",
    description="Middleware API gateway for LLM threat analysis",
    version="2.0.0",
    lifespan=lifespan,
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ──
app.include_router(analyze.router, prefix="/api", tags=["Analyze"])
app.include_router(sessions.router, prefix="/api", tags=["Sessions"])
app.include_router(health.router, prefix="/api", tags=["Health"])

# ── Serve Frontend Static Files ──
_frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "dist")

if os.path.isdir(_frontend_dist):
    # Serve /assets/* from dist/assets/
    assets_dir = os.path.join(_frontend_dist, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(_frontend_dist, "index.html"))

    @app.get("/{path:path}")
    async def serve_spa(path: str):
        file_path = os.path.join(_frontend_dist, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(_frontend_dist, "index.html"))
