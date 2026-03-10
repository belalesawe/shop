"""Inventory API route handlers."""

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ecommerce.database import get_session
from ecommerce.inventory.schemas import InventoryUpdate, ReserveRequest, InventoryRead
from ecommerce.inventory import service

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/{product_id}", response_model=InventoryRead)
async def get_inventory(
    product_id: int, session: AsyncSession = Depends(get_session)
) -> InventoryRead:
    """Get inventory for a product."""
    inventory = await service.get_inventory(session, product_id)
    return InventoryRead(
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        reserved=inventory.reserved,
        last_updated=inventory.last_updated,
    )


@router.put("/{product_id}", response_model=InventoryRead)
async def update_inventory(
    product_id: int,
    update: InventoryUpdate,
    session: AsyncSession = Depends(get_session),
) -> InventoryRead:
    """Update inventory quantity."""
    inventory = await service.update_inventory(session, product_id, update.quantity)
    return InventoryRead(
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        reserved=inventory.reserved,
        last_updated=inventory.last_updated,
    )


@router.post("/{product_id}/reserve", response_model=InventoryRead)
async def reserve_inventory(
    product_id: int,
    reserve: ReserveRequest,
    session: AsyncSession = Depends(get_session),
) -> InventoryRead:
    """Reserve inventory for an order."""
    inventory = await service.reserve_inventory(session, product_id, reserve.quantity)
    return InventoryRead(
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        reserved=inventory.reserved,
        last_updated=inventory.last_updated,
    )
