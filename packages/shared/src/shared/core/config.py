"""
Shared configuration using Pydantic settings.

Settings are loaded from environment variables with .env file support.
The settings instance is cached as a singleton via @cache decorator.

Usage:
    from shared.core.config import shared_settings

    print(shared_settings.APPLICATION_DATABASE_URL)
"""

from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class SharedSettings(BaseSettings):
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

    # Database configuration
    APPLICATION_DATABASE_URL: str
    DB_ECHO_SQL: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_PRE_PING: bool = False


@cache
def get_shared_settings() -> SharedSettings:
    """Return cached settings instance (singleton pattern)."""
    return SharedSettings()


# Global settings instance
shared_settings = get_shared_settings()
