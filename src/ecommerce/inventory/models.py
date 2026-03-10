"""Inventory database model."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Inventory(SQLModel, table=True):
    """Product inventory tracking."""

    __tablename__ = "inventory"

    product_id: int = Field(foreign_key="products.id", primary_key=True)
    quantity: int = Field(default=0)
    reserved: int = Field(default=0)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
