"""
Sentinel-AI — Sessions Route
Session management endpoints for conversation history and analysis logs.
"""

from fastapi import APIRouter, HTTPException

from app.engines.memory import memory

router = APIRouter()


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Retrieve all messages for a session."""
    if not memory.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    messages = memory.get_messages(session_id)
    return {
        "session_id": session_id,
        "message_count": len(messages),
        "messages": messages,
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and all its data."""
    deleted = memory.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"status": "deleted", "session_id": session_id}


@router.get("/sessions/{session_id}/analysis")
async def get_session_analysis(session_id: str):
    """Get all analysis results for a session."""
    if not memory.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    analyses = memory.get_analyses(session_id)
    return {
        "session_id": session_id,
        "analysis_count": len(analyses),
        "analyses": analyses,
    }
