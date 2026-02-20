"""
Sentinel-AI — Database Setup
SQLAlchemy async engine + session factory.
Supports PostgreSQL (asyncpg) and SQLite (aiosqlite).
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    """Create all tables."""
    async with engine.begin() as conn:
        from app.models.db_models import Conversation, Message  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency: yield an async DB session."""
    async with async_session() as session:
        yield session
