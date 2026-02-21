"""Shared test fixtures for auth tests."""

import asyncio
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ecommerce.main import app  # noqa: E402
from ecommerce.database import get_session  # noqa: E402


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    """Create a fresh test database engine for each test."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine: AsyncEngine):
    """Create a database session for each test."""
    async with AsyncSession(test_engine) as session:
        yield session


@pytest_asyncio.fixture
async def client(test_engine: AsyncEngine):
    """Create an async HTTP client configured to use the test database."""

    async def override_get_session():
        async with AsyncSession(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient):
    """Create and return a registered user with their tokens."""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpass123",
        "phone": "+1234567890",
        "address": "123 Test St",
    }
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    tokens = response.json()
    return {
        "email": user_data["email"],
        "name": user_data["name"],
        "password": user_data["password"],
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


@pytest_asyncio.fixture
async def auth_headers(registered_user: dict):
    """Return authorization headers for an authenticated user."""
    return {"Authorization": f"Bearer {registered_user['access_token']}"}
