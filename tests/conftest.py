"""Shared test fixtures for e-commerce API tests."""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# Import all models so SQLModel metadata is populated
from ecommerce import models  # noqa: F401
from ecommerce.database import get_session
from ecommerce.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create a session-scoped event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create an in-memory SQLite engine for testing."""
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a test database session."""
    async with AsyncSession(test_engine) as session:
        yield session


@pytest_asyncio.fixture
async def client(test_engine: AsyncEngine) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client with test database."""

    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = _get_test_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
