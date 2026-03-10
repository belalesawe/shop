"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = "sqlite+aiosqlite:///./ecommerce.db"
    app_title: str = "E-commerce API"
    debug: bool = False

    model_config = {"env_prefix": "SHOP_"}


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
