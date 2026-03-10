"""Product and category business logic."""

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ecommerce.products.models import Category, Product
from ecommerce.products.schemas import CategoryCreate, ProductCreate
from ecommerce.inventory.models import Inventory


async def create_category(session: AsyncSession, data: CategoryCreate) -> Category:
    """Create a new category."""
    category = Category(name=data.name, description=data.description)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def list_categories(session: AsyncSession) -> list[Category]:
    """List all categories."""
    result = await session.execute(select(Category))
    return list(result.scalars().all())


async def create_product(session: AsyncSession, data: ProductCreate) -> Product:
    """Create a new product with category validation and inventory initialization.

    Uses flush-then-commit for atomic product + inventory creation.
    """
    # Verify category exists if provided
    if data.category_id:
        category = await session.get(Category, data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        category_id=data.category_id,
    )
    session.add(product)
    await session.flush()  # Get product.id without committing

    # Initialize inventory for new product (atomic with product creation)
    inventory = Inventory(product_id=product.id, quantity=0, reserved=0)
    session.add(inventory)

    await session.commit()
    await session.refresh(product)
    return product


async def get_product(session: AsyncSession, product_id: int) -> Product:
    """Get product by ID."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def list_products(session: AsyncSession) -> list[Product]:
    """List all products."""
    result = await session.execute(select(Product))
    return list(result.scalars().all())
