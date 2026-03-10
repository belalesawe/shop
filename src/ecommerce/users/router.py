"""User API route handlers."""

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ecommerce.database import get_session
from ecommerce.users.schemas import UserCreate, UserRead
from ecommerce.users import service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead)
async def create_user(
    data: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    """Create a new user."""
    user = await service.create_user(session, data)
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> UserRead:
    """Get user by ID."""
    user = await service.get_user(session, user_id)
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
    )


@router.get("", response_model=list[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
) -> list[UserRead]:
    """List all users."""
    users = await service.list_users(session)
    return [
        UserRead(
            id=u.id,
            email=u.email,
            name=u.name,
            created_at=u.created_at,
        )
        for u in users
    ]
