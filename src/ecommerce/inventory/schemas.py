"""Inventory request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class InventoryUpdate(BaseModel):
    """Request model for updating inventory."""

    quantity: int


class ReserveRequest(BaseModel):
    """Request model for reserving inventory."""

    quantity: int


class InventoryRead(BaseModel):
    """Response model for inventory data."""

    product_id: int
    quantity: int
    reserved: int
    last_updated: datetime
