"""Tests for the users domain endpoints."""

import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_create_user(async_client: AsyncClient):
    """POST /users creates a user and returns UserRead format."""
    response = await async_client.post(
        "/users", json={"email": "alice@example.com", "name": "Alice"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["name"] == "Alice"
    assert "id" in data
    assert "created_at" in data


async def test_create_user_duplicate_email(async_client: AsyncClient):
    """POST /users with duplicate email returns 400."""
    payload = {"email": "bob@example.com", "name": "Bob"}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == 200

    # Attempt duplicate
    response = await async_client.post("/users", json=payload)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


async def test_get_user(async_client: AsyncClient):
    """GET /users/{id} returns user details."""
    # Create a user first
    create_resp = await async_client.post(
        "/users", json={"email": "carol@example.com", "name": "Carol"}
    )
    user_id = create_resp.json()["id"]

    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "carol@example.com"
    assert data["name"] == "Carol"
    assert "created_at" in data


async def test_get_user_not_found(async_client: AsyncClient):
    """GET /users/{id} returns 404 for non-existent user."""
    response = await async_client.get("/users/9999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


async def test_list_users_empty(async_client: AsyncClient):
    """GET /users returns empty list when no users exist."""
    response = await async_client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


async def test_list_users_with_data(async_client: AsyncClient):
    """GET /users returns all created users."""
    await async_client.post(
        "/users", json={"email": "dave@example.com", "name": "Dave"}
    )
    await async_client.post(
        "/users", json={"email": "eve@example.com", "name": "Eve"}
    )

    response = await async_client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    emails = {u["email"] for u in data}
    assert emails == {"dave@example.com", "eve@example.com"}


async def test_create_user_response_excludes_internal_fields(
    async_client: AsyncClient,
):
    """UserRead response should not include internal ORM fields."""
    response = await async_client.post(
        "/users", json={"email": "frank@example.com", "name": "Frank"}
    )
    data = response.json()
    # Should have exactly these keys
    expected_keys = {"id", "email", "name", "created_at"}
    assert set(data.keys()) == expected_keys
