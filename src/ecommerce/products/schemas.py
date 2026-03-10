"""Product and category request/response schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """Request model for creating a category."""

    name: str
    description: Optional[str] = None


class CategoryRead(BaseModel):
    """Response model for category data."""

    id: int
    name: str
    description: Optional[str] = None


class ProductCreate(BaseModel):
    """Request model for creating a product."""

    name: str
    description: Optional[str] = None
    price: Decimal
    category_id: Optional[int] = None


class ProductRead(BaseModel):
    """Response model for product data."""

    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    category_id: Optional[int] = None
    created_at: datetime
