"""
Async SQLAlchemy session management.

Provides async engine and session factory for database operations.
The async context manager handles session lifecycle automatically.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.core.config import shared_settings

# Create async engine with connection pooling
# Pool settings are configurable via environment variables
async_engine = create_async_engine(
    url=shared_settings.APPLICATION_DATABASE_URL,
    echo=shared_settings.DB_ECHO_SQL,
    pool_size=shared_settings.DB_POOL_SIZE,
    max_overflow=shared_settings.DB_MAX_OVERFLOW,
    pool_recycle=shared_settings.DB_POOL_RECYCLE,
    pool_pre_ping=shared_settings.DB_POOL_PRE_PING,
)


# Session Factory
# expire_on_commit=False: Keep objects usable after commit (no lazy-load issues)
async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """
    FastAPI dependency that provides async database session.

    The async context manager automatically:
    - Opens a new session
    - Yields it to the endpoint
    - Closes the session (even if an exception occurs)

    No manual cleanup needed - the context manager handles it.

    Usage:
        @router.get("/items")
        async def get_items(session: Annotated[AsyncSession, Depends(get_db_session)]):
            result = await session.execute(select(Item))
            return result.scalars().all()
    """
    async with async_session_maker() as session:
        yield session
