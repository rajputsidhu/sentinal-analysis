"""
Sentinel-AI — Health Check Route
"""

import time
from fastapi import APIRouter
from app.config import settings

router = APIRouter()

_start_time = time.time()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - _start_time, 1),
        "config": {
            "analysis_mode": settings.analysis_mode,
            "dry_run": settings.dry_run,
            "model": settings.openai_model,
            "embedding_model": settings.embedding_model,
            "threshold_allow": settings.threshold_allow,
            "threshold_warn": settings.threshold_warn,
            "threshold_rewrite": settings.threshold_rewrite,
        },
    }
