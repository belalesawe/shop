"""Tests for user CRUD endpoints."""

import pytest
from httpx import AsyncClient


class TestCreateUser:
    """Tests for POST /users."""

    async def test_create_user(self, client: AsyncClient):
        """Test creating a new user."""
        response = await client.post(
            "/users", json={"email": "alice@example.com", "name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "alice@example.com"
        assert data["name"] == "Alice"
        assert "id" in data
        assert "created_at" in data

    async def test_create_user_duplicate_email(self, client: AsyncClient):
        """Test that duplicate email returns 400."""
        await client.post(
            "/users", json={"email": "bob@example.com", "name": "Bob"}
        )
        response = await client.post(
            "/users", json={"email": "bob@example.com", "name": "Bob 2"}
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]


class TestGetUser:
    """Tests for GET /users/{user_id}."""

    async def test_get_user(self, client: AsyncClient):
        """Test getting a user by ID."""
        create_response = await client.post(
            "/users", json={"email": "charlie@example.com", "name": "Charlie"}
        )
        user_id = create_response.json()["id"]

        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "charlie@example.com"
        assert data["name"] == "Charlie"

    async def test_get_user_not_found(self, client: AsyncClient):
        """Test getting a non-existent user returns 404."""
        response = await client.get("/users/999")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


class TestListUsers:
    """Tests for GET /users."""

    async def test_list_users_empty(self, client: AsyncClient):
        """Test listing users when none exist."""
        response = await client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_users(self, client: AsyncClient):
        """Test listing users after creation."""
        await client.post(
            "/users", json={"email": "dave@example.com", "name": "Dave"}
        )
        await client.post(
            "/users", json={"email": "eve@example.com", "name": "Eve"}
        )

        response = await client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        emails = {u["email"] for u in data}
        assert emails == {"dave@example.com", "eve@example.com"}
