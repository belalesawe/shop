"""User business logic."""

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ecommerce.users.models import User
from ecommerce.users.schemas import UserCreate


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    """Create a new user after checking email uniqueness."""
    result = await session.execute(select(User).where(User.email == data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=data.email, name=data.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User:
    """Get user by ID."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def list_users(session: AsyncSession) -> list[User]:
    """List all users."""
    result = await session.execute(select(User))
    return list(result.scalars().all())
