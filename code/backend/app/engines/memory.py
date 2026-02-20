"""
Sentinel-AI — Module 2: Conversation Memory Loader
Fetches conversation history from the database and loads embeddings.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Conversation, Message
from app.utils.logger import log


async def get_or_create_conversation(db: AsyncSession, conversation_id: str, user_id: str) -> Conversation:
    """Get an existing conversation or create a new one."""
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conv = result.scalar_one_or_none()

    if not conv:
        conv = Conversation(id=conversation_id, user_id=user_id)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        log.info(f"New conversation created", conversation_id=conversation_id, user_id=user_id)

    return conv


async def load_conversation_history(db: AsyncSession, conversation_id: str, limit: int = 20) -> list[dict]:
    """Fetch the last N messages from the database."""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    messages.reverse()  # Chronological order

    history = [
        {
            "role": msg.role,
            "content": msg.content,
            "embedding": msg.embedding,
            "drift_score": msg.drift_score,
            "risk_score": msg.risk_score,
        }
        for msg in messages
    ]

    log.debug(f"Loaded conversation history", conversation_id=conversation_id, messages=len(history))
    return history


async def load_embedding_history(db: AsyncSession, conversation_id: str) -> list[list[float]]:
    """Fetch all non-null embeddings for a conversation."""
    result = await db.execute(
        select(Message.embedding)
        .where(
            Message.conversation_id == conversation_id,
            Message.embedding.isnot(None),
            Message.role == "user",
        )
        .order_by(Message.created_at)
    )
    embeddings = [row[0] for row in result.all() if row[0] is not None]
    log.debug(f"Loaded embedding history", conversation_id=conversation_id, count=len(embeddings))
    return embeddings


async def save_message(
    db: AsyncSession,
    conversation_id: str,
    role: str,
    content: str,
    embedding: list[float] | None = None,
    drift_score: float | None = None,
    risk_score: float | None = None,
    action: str | None = None,
    red_team_result: dict | None = None,
    blue_team_result: dict | None = None,
):
    """Save a message and its analysis to the database."""
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        embedding=embedding,
        drift_score=drift_score,
        risk_score=risk_score,
        action=action,
        red_team_result=red_team_result,
        blue_team_result=blue_team_result,
    )
    db.add(msg)
    await db.commit()
    log.debug(f"Message saved", conversation_id=conversation_id, role=role)
