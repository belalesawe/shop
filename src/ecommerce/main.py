"""FastAPI application - E-commerce API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from ecommerce.config import get_settings
from ecommerce.database import init_db
from ecommerce.users.router import router as users_router
from ecommerce.products.router import router as products_router
from ecommerce.products.router import categories_router
from ecommerce.orders.router import router as orders_router
from ecommerce.inventory.router import router as inventory_router
from ecommerce.reports.router import router as reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    description="E-commerce REST API",
    version="1.0.0",
    lifespan=lifespan,
)

# Register all routers
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(inventory_router)
app.include_router(reports_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ecommerce-api"}
