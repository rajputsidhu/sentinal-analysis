"""
Sentinel-AI — Session Management Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.db_models import Conversation, Message

router = APIRouter()


@router.get("/sessions")
async def list_sessions(user_id: str = None, db: AsyncSession = Depends(get_db)):
    """List all conversations, optionally filtered by user_id."""
    query = select(Conversation).order_by(Conversation.created_at.desc())
    if user_id:
        query = query.where(Conversation.user_id == user_id)

    result = await db.execute(query)
    conversations = result.scalars().all()

    return [
        {
            "id": c.id,
            "user_id": c.user_id,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in conversations
    ]


@router.get("/sessions/{conversation_id}")
async def get_session(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """Get all messages for a conversation with analysis data."""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "drift_score": m.drift_score,
                "risk_score": m.risk_score,
                "action": m.action,
                "red_team_result": m.red_team_result,
                "blue_team_result": m.blue_team_result,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ],
    }


@router.delete("/sessions/{conversation_id}")
async def delete_session(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a conversation and all its messages."""
    result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id)
    )
    messages = result.scalars().all()
    for m in messages:
        await db.delete(m)

    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conv = result.scalar_one_or_none()
    if conv:
        await db.delete(conv)

    await db.commit()
    return {"status": "deleted", "conversation_id": conversation_id}
