"""User API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ecommerce.database import get_session
from ecommerce.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=User)
async def create_user(user: User, session: AsyncSession = Depends(get_session)) -> User:
    """Create a new user."""
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> User:
    """Get user by ID."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=list[User])
async def list_users(session: AsyncSession = Depends(get_session)) -> list[User]:
    """List all users."""
    result = await session.execute(select(User))
    return result.scalars().all()
