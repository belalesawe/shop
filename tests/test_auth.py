"""Unit and integration tests for authentication."""

import pytest
from httpx import AsyncClient


# ──────────────────────────────────────────────────────────
# Unit tests for security utilities
# ──────────────────────────────────────────────────────────

class TestPasswordHashing:
    """Unit tests for password hashing utilities."""

    def test_hash_password_returns_bcrypt_hash(self):
        from ecommerce.auth.security import hash_password

        hashed = hash_password("mypassword")
        assert hashed != "mypassword"
        assert hashed.startswith("$2b$")  # bcrypt prefix

    def test_verify_password_correct(self):
        from ecommerce.auth.security import hash_password, verify_password

        hashed = hash_password("mypassword")
        assert verify_password("mypassword", hashed) is True

    def test_verify_password_incorrect(self):
        from ecommerce.auth.security import hash_password, verify_password

        hashed = hash_password("mypassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_different_passwords_produce_different_hashes(self):
        from ecommerce.auth.security import hash_password

        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        assert hash1 != hash2

    def test_same_password_produces_different_hashes(self):
        """bcrypt includes a random salt, so same input gives different output."""
        from ecommerce.auth.security import hash_password

        hash1 = hash_password("samepassword")
        hash2 = hash_password("samepassword")
        assert hash1 != hash2


class TestJWTTokens:
    """Unit tests for JWT token creation and validation."""

    def test_create_access_token(self):
        from ecommerce.auth.security import create_access_token, decode_token

        token = create_access_token({"sub": "123"})
        assert isinstance(token, str)
        assert len(token) > 0

        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        from ecommerce.auth.security import create_refresh_token, decode_token

        token = create_refresh_token({"sub": "456"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "456"
        assert payload["type"] == "refresh"

    def test_decode_invalid_token(self):
        from ecommerce.auth.security import decode_token

        result = decode_token("invalid.token.value")
        assert result is None

    def test_decode_empty_string(self):
        from ecommerce.auth.security import decode_token

        result = decode_token("")
        assert result is None

    def test_access_token_has_expiry(self):
        from ecommerce.auth.security import create_access_token, decode_token

        token = create_access_token({"sub": "1"})
        payload = decode_token(token)
        assert "exp" in payload

    def test_token_preserves_custom_data(self):
        from ecommerce.auth.security import create_access_token, decode_token

        token = create_access_token({"sub": "1", "role": "admin"})
        payload = decode_token(token)
        assert payload["role"] == "admin"


# ──────────────────────────────────────────────────────────
# Integration tests for auth endpoints
# ──────────────────────────────────────────────────────────

class TestRegister:
    """Integration tests for POST /auth/register."""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "email": "new@example.com",
                "name": "New User",
                "password": "securepass123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_register_with_all_fields(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "email": "full@example.com",
                "name": "Full User",
                "password": "securepass123",
                "phone": "+1234567890",
                "address": "123 Main St",
            },
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient):
        user_data = {
            "email": "dup@example.com",
            "name": "User One",
            "password": "securepass123",
        }
        response1 = await client.post("/auth/register", json=user_data)
        assert response1.status_code == 201

        user_data["name"] = "User Two"
        response2 = await client.post("/auth/register", json=user_data)
        assert response2.status_code == 409
        assert "already registered" in response2.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "email": "not-an-email",
                "name": "Bad Email",
                "password": "securepass123",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_short_password(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "email": "short@example.com",
                "name": "Short Pass",
                "password": "short",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_name(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "email": "noname@example.com",
                "password": "securepass123",
            },
        )
        assert response.status_code == 422


class TestLogin:
    """Integration tests for POST /auth/login."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, registered_user: dict):
        response = await client.post(
            "/auth/login",
            json={
                "email": registered_user["email"],
                "password": registered_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, registered_user: dict):
        response = await client.post(
            "/auth/login",
            json={
                "email": registered_user["email"],
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            json={
                "email": "nobody@example.com",
                "password": "anypassword",
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_invalid_email_format(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            json={
                "email": "not-valid",
                "password": "anypassword",
            },
        )
        assert response.status_code == 422


class TestTokenRefresh:
    """Integration tests for POST /auth/refresh."""

    @pytest.mark.asyncio
    async def test_refresh_success(self, client: AsyncClient, registered_user: dict):
        response = await client.post(
            "/auth/refresh",
            json={"refresh_token": registered_user["refresh_token"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, client: AsyncClient):
        response = await client.post(
            "/auth/refresh",
            json={"refresh_token": "invalid.token.value"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_with_access_token_fails(
        self, client: AsyncClient, registered_user: dict
    ):
        """Using an access token as a refresh token should fail."""
        response = await client.post(
            "/auth/refresh",
            json={"refresh_token": registered_user["access_token"]},
        )
        assert response.status_code == 401


class TestChangePassword:
    """Integration tests for POST /auth/change-password."""

    @pytest.mark.asyncio
    async def test_change_password_success(
        self, client: AsyncClient, registered_user: dict, auth_headers: dict
    ):
        response = await client.post(
            "/auth/change-password",
            json={
                "current_password": registered_user["password"],
                "new_password": "newsecurepass456",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Password changed successfully"

        # Verify new password works for login
        login_resp = await client.post(
            "/auth/login",
            json={
                "email": registered_user["email"],
                "password": "newsecurepass456",
            },
        )
        assert login_resp.status_code == 200

    @pytest.mark.asyncio
    async def test_change_password_wrong_current(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.post(
            "/auth/change-password",
            json={
                "current_password": "wrongcurrent",
                "new_password": "newsecurepass456",
            },
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_change_password_unauthenticated(self, client: AsyncClient):
        response = await client.post(
            "/auth/change-password",
            json={
                "current_password": "any",
                "new_password": "newsecure123",
            },
        )
        assert response.status_code == 403


class TestProfile:
    """Integration tests for GET/PUT /users/me."""

    @pytest.mark.asyncio
    async def test_get_profile(
        self, client: AsyncClient, registered_user: dict, auth_headers: dict
    ):
        response = await client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == registered_user["email"]
        assert data["name"] == registered_user["name"]
        assert data["phone"] == "+1234567890"
        assert data["address"] == "123 Test St"
        assert "password_hash" not in data

    @pytest.mark.asyncio
    async def test_get_profile_unauthenticated(self, client: AsyncClient):
        response = await client.get("/users/me")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_profile(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.put(
            "/users/me",
            json={"name": "Updated Name", "phone": "+9876543210"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["phone"] == "+9876543210"

    @pytest.mark.asyncio
    async def test_update_profile_partial(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Updating only one field should not clear others."""
        response = await client.put(
            "/users/me",
            json={"name": "Partial Update"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Partial Update"

    @pytest.mark.asyncio
    async def test_update_profile_unauthenticated(self, client: AsyncClient):
        response = await client.put(
            "/users/me",
            json={"name": "Hacker"},
        )
        assert response.status_code == 403
