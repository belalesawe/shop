"""Re-export all database models for centralized metadata discovery."""

from ecommerce.users.models import User  # noqa: F401

# Models not yet split into domain files — will be moved in subsequent milestones
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """Product category."""

    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None


class Product(SQLModel, table=True):
    """Product in catalog."""

    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: Decimal = Field(decimal_places=2)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Inventory(SQLModel, table=True):
    """Product inventory tracking."""

    __tablename__ = "inventory"

    product_id: int = Field(foreign_key="products.id", primary_key=True)
    quantity: int = Field(default=0)
    reserved: int = Field(default=0)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class Order(SQLModel, table=True):
    """Customer order."""

    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    status: str = Field(default="pending")  # pending, confirmed, shipped, delivered
    total: Decimal = Field(decimal_places=2)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderItem(SQLModel, table=True):
    """Items in an order."""

    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    price: Decimal = Field(decimal_places=2)
