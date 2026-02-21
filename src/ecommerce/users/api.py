"""User API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ecommerce.database import get_session
from ecommerce.models import User
from ecommerce.auth.schemas import UserProfileResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserProfileResponse)
async def create_user(user: User, session: AsyncSession = Depends(get_session)) -> UserProfileResponse:
    """Create a new user."""
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserProfileResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> UserProfileResponse:
    """Get user by ID."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfileResponse.model_validate(user)


@router.get("", response_model=list[UserProfileResponse])
async def list_users(session: AsyncSession = Depends(get_session)) -> list[UserProfileResponse]:
    """List all users."""
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [UserProfileResponse.model_validate(u) for u in users]
