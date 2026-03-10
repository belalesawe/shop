"""User request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Request schema for creating a user."""

    email: str
    name: str


class UserRead(BaseModel):
    """Response schema for a user."""

    id: int
    email: str
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
