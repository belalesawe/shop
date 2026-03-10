"""Re-export all database models for centralized metadata discovery."""

from ecommerce.users.models import User  # noqa: F401
from ecommerce.products.models import Category, Product  # noqa: F401
from ecommerce.inventory.models import Inventory  # noqa: F401

# Models not yet split into domain files — will be moved in subsequent milestones
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


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
