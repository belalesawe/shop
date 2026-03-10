"""Product catalog API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ecommerce.database import get_session
from ecommerce.models import Product, Category, Inventory

router = APIRouter(prefix="/products", tags=["products"])
categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.post("", response_model=Category)
async def create_category(
    category: Category, session: AsyncSession = Depends(get_session)
) -> Category:
    """Create a new category."""
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@categories_router.get("", response_model=list[Category])
async def list_categories(
    session: AsyncSession = Depends(get_session),
) -> list[Category]:
    """List all categories."""
    result = await session.execute(select(Category))
    return result.scalars().all()


@router.post("", response_model=Product)
async def create_product(
    product: Product, session: AsyncSession = Depends(get_session)
) -> Product:
    """Create a new product."""
    # Verify category exists if provided
    if product.category_id:
        category = await session.get(Category, product.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    session.add(product)
    await session.commit()
    await session.refresh(product)

    # Initialize inventory for new product
    inventory = Inventory(product_id=product.id, quantity=0, reserved=0)
    session.add(inventory)
    await session.commit()
    await session.refresh(product)

    return product


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int, session: AsyncSession = Depends(get_session)
) -> Product:
    """Get product by ID."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=list[Product])
async def list_products(session: AsyncSession = Depends(get_session)) -> list[Product]:
    """List all products."""
    result = await session.execute(select(Product))
    return result.scalars().all()
