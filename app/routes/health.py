"""
Sentinel-AI — Health Route
System health check endpoint.
"""

import time
from fastapi import APIRouter

from app.config import settings
from app.engines.memory import memory
from app.models import HealthResponse

router = APIRouter()

_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health():
    """Returns uptime, active session count, and configuration summary."""
    return HealthResponse(
        status="ok",
        uptime_seconds=round(time.time() - _start_time, 2),
        active_sessions=memory.active_session_count(),
        config={
            "analysis_mode": settings.analysis_mode,
            "dry_run": settings.dry_run,
            "model": settings.openai_model,
            "threshold_warn": settings.threat_threshold_warn,
            "threshold_block": settings.threat_threshold_block,
            "max_session_history": settings.max_session_history,
            "session_ttl_minutes": settings.session_ttl_minutes,
        },
    )
