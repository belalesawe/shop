"""User request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Request model for creating a user."""

    email: str
    name: str


class UserRead(BaseModel):
    """Response model for user data."""

    id: int
    email: str
    name: str
    created_at: datetime
