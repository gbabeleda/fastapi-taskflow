"""
Application configuration using Pydantic settings.

Settings are loaded from environment variables with .env file support.
The settings instance is cached as a singleton via @cache decorator.

Usage:
    from api.core.config import settings

    print(settings.PROJECT_NAME)
"""

from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Values are loaded from environment variables, with .env file as fallback.

    Local development:
        Create .env file in project root with overrides

    Production:
        Set as actual environment variables (no .env file)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore unknown environment variables
    )

    # Project metadata
    PROJECT_NAME: str = "FastAPI Taskflow API"
    VERSION: str = "0.1.0"

    # API configuration
    API_V1_PREFIX: str = "/api/v1"


@cache
def get_settings() -> Settings:
    """Return cached settings instance (singleton pattern)."""
    return Settings()


# Global settings instance
settings = get_settings()
