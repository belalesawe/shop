"""Product and category database models."""

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
