"""Tests for product and category CRUD endpoints."""

import pytest
from httpx import AsyncClient


class TestCreateCategory:
    """Tests for POST /categories."""

    async def test_create_category(self, client: AsyncClient):
        """Test creating a new category."""
        response = await client.post(
            "/categories",
            json={"name": "Electronics", "description": "Electronic devices"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Electronics"
        assert data["description"] == "Electronic devices"
        assert "id" in data

    async def test_create_category_without_description(self, client: AsyncClient):
        """Test creating a category without a description."""
        response = await client.post(
            "/categories", json={"name": "Books"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Books"
        assert data["description"] is None


class TestListCategories:
    """Tests for GET /categories."""

    async def test_list_categories_empty(self, client: AsyncClient):
        """Test listing categories when none exist."""
        response = await client.get("/categories")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_categories(self, client: AsyncClient):
        """Test listing categories after creation."""
        await client.post(
            "/categories", json={"name": "Clothing"}
        )
        await client.post(
            "/categories", json={"name": "Food"}
        )

        response = await client.get("/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        names = {c["name"] for c in data}
        assert names == {"Clothing", "Food"}


class TestCreateProduct:
    """Tests for POST /products."""

    async def test_create_product_with_category(self, client: AsyncClient):
        """Test creating a product with a valid category."""
        cat_response = await client.post(
            "/categories", json={"name": "Gadgets"}
        )
        category_id = cat_response.json()["id"]

        response = await client.post(
            "/products",
            json={
                "name": "Widget",
                "description": "A useful widget",
                "price": 29.99,
                "category_id": category_id,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Widget"
        assert data["description"] == "A useful widget"
        assert float(data["price"]) == 29.99
        assert data["category_id"] == category_id
        assert "id" in data
        assert "created_at" in data

    async def test_create_product_without_category(self, client: AsyncClient):
        """Test creating a product without a category."""
        response = await client.post(
            "/products",
            json={
                "name": "Standalone Item",
                "price": 9.99,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Standalone Item"
        assert data["category_id"] is None

    async def test_create_product_invalid_category(self, client: AsyncClient):
        """Test creating a product with non-existent category returns 404."""
        response = await client.post(
            "/products",
            json={
                "name": "Bad Product",
                "price": 5.00,
                "category_id": 999,
            },
        )
        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    async def test_create_product_initializes_inventory(self, client: AsyncClient):
        """Test that creating a product auto-initializes inventory."""
        cat_response = await client.post(
            "/categories", json={"name": "Test Category"}
        )
        category_id = cat_response.json()["id"]

        product_response = await client.post(
            "/products",
            json={
                "name": "Inventoried Product",
                "price": 15.00,
                "category_id": category_id,
            },
        )
        product_id = product_response.json()["id"]

        # Verify inventory was auto-created
        inv_response = await client.get(f"/inventory/{product_id}")
        assert inv_response.status_code == 200
        inv_data = inv_response.json()
        assert inv_data["product_id"] == product_id
        assert inv_data["quantity"] == 0
        assert inv_data["reserved"] == 0


class TestGetProduct:
    """Tests for GET /products/{product_id}."""

    async def test_get_product(self, client: AsyncClient):
        """Test getting a product by ID."""
        create_response = await client.post(
            "/products",
            json={"name": "Findable Product", "price": 19.99},
        )
        product_id = create_response.json()["id"]

        response = await client.get(f"/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Findable Product"

    async def test_get_product_not_found(self, client: AsyncClient):
        """Test getting a non-existent product returns 404."""
        response = await client.get("/products/999")
        assert response.status_code == 404
        assert "Product not found" in response.json()["detail"]


class TestListProducts:
    """Tests for GET /products."""

    async def test_list_products_empty(self, client: AsyncClient):
        """Test listing products when none exist."""
        response = await client.get("/products")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_products(self, client: AsyncClient):
        """Test listing products after creation."""
        await client.post(
            "/products", json={"name": "Product A", "price": 10.00}
        )
        await client.post(
            "/products", json={"name": "Product B", "price": 20.00}
        )

        response = await client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        names = {p["name"] for p in data}
        assert names == {"Product A", "Product B"}
