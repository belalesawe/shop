"""Application settings using pydantic-settings."""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the e-commerce application.

    Settings are loaded from environment variables and .env file.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite+aiosqlite:///./ecommerce.db"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    LOG_LEVEL: str = "info"


settings = Settings()
