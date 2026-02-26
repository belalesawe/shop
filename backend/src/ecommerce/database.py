"""Database connection and session management."""

from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from ecommerce.settings import settings

engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=False)


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database sessions."""
    async with AsyncSession(engine) as session:
        yield session
