"""Tests for inventory endpoints."""

import pytest
from httpx import AsyncClient


async def _create_product_with_inventory(client: AsyncClient) -> int:
    """Helper: create a category, product, and return the product_id."""
    cat_resp = await client.post(
        "/categories", json={"name": "Test Cat"}
    )
    category_id = cat_resp.json()["id"]
    prod_resp = await client.post(
        "/products",
        json={
            "name": "Test Product",
            "price": 25.00,
            "category_id": category_id,
        },
    )
    return prod_resp.json()["id"]


class TestGetInventory:
    """Tests for GET /inventory/{product_id}."""

    async def test_get_inventory(self, client: AsyncClient):
        """Test getting inventory for a product."""
        product_id = await _create_product_with_inventory(client)

        response = await client.get(f"/inventory/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == product_id
        assert data["quantity"] == 0
        assert data["reserved"] == 0
        assert "last_updated" in data

    async def test_get_inventory_not_found(self, client: AsyncClient):
        """Test getting inventory for non-existent product returns 404."""
        response = await client.get("/inventory/999")
        assert response.status_code == 404
        assert "Inventory not found" in response.json()["detail"]


class TestUpdateInventory:
    """Tests for PUT /inventory/{product_id}."""

    async def test_update_inventory(self, client: AsyncClient):
        """Test updating inventory quantity."""
        product_id = await _create_product_with_inventory(client)

        response = await client.put(
            f"/inventory/{product_id}", json={"quantity": 100}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == product_id
        assert data["quantity"] == 100
        assert data["reserved"] == 0

    async def test_update_inventory_not_found(self, client: AsyncClient):
        """Test updating inventory for non-existent product returns 404."""
        response = await client.put(
            "/inventory/999", json={"quantity": 50}
        )
        assert response.status_code == 404
        assert "Inventory not found" in response.json()["detail"]

    async def test_update_inventory_persists(self, client: AsyncClient):
        """Test that inventory update persists when re-fetched."""
        product_id = await _create_product_with_inventory(client)
        await client.put(
            f"/inventory/{product_id}", json={"quantity": 75}
        )

        response = await client.get(f"/inventory/{product_id}")
        assert response.status_code == 200
        assert response.json()["quantity"] == 75


class TestReserveInventory:
    """Tests for POST /inventory/{product_id}/reserve."""

    async def test_reserve_inventory_success(self, client: AsyncClient):
        """Test successful inventory reservation."""
        product_id = await _create_product_with_inventory(client)
        await client.put(
            f"/inventory/{product_id}", json={"quantity": 50}
        )

        response = await client.post(
            f"/inventory/{product_id}/reserve", json={"quantity": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == product_id
        assert data["quantity"] == 50
        assert data["reserved"] == 10

    async def test_reserve_inventory_multiple(self, client: AsyncClient):
        """Test multiple sequential reservations."""
        product_id = await _create_product_with_inventory(client)
        await client.put(
            f"/inventory/{product_id}", json={"quantity": 100}
        )

        await client.post(
            f"/inventory/{product_id}/reserve", json={"quantity": 30}
        )
        response = await client.post(
            f"/inventory/{product_id}/reserve", json={"quantity": 20}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 100
        assert data["reserved"] == 50

    async def test_reserve_inventory_insufficient(self, client: AsyncClient):
        """Test reservation with insufficient stock returns 400."""
        product_id = await _create_product_with_inventory(client)
        await client.put(
            f"/inventory/{product_id}", json={"quantity": 5}
        )

        response = await client.post(
            f"/inventory/{product_id}/reserve", json={"quantity": 10}
        )
        assert response.status_code == 400
        assert "Insufficient inventory" in response.json()["detail"]

    async def test_reserve_inventory_insufficient_with_existing_reservation(
        self, client: AsyncClient
    ):
        """Test reservation fails when available (quantity - reserved) is insufficient."""
        product_id = await _create_product_with_inventory(client)
        await client.put(
            f"/inventory/{product_id}", json={"quantity": 20}
        )

        # Reserve 15 of the 20
        await client.post(
            f"/inventory/{product_id}/reserve", json={"quantity": 15}
        )

        # Try to reserve 10 more (only 5 available)
        response = await client.post(
            f"/inventory/{product_id}/reserve", json={"quantity": 10}
        )
        assert response.status_code == 400
        assert "Insufficient inventory" in response.json()["detail"]

    async def test_reserve_inventory_not_found(self, client: AsyncClient):
        """Test reservation for non-existent product returns 404."""
        response = await client.post(
            "/inventory/999/reserve", json={"quantity": 5}
        )
        assert response.status_code == 404
        assert "Inventory not found" in response.json()["detail"]
