"""Async PostgreSQL engine and request-scoped SQLModel sessions."""

from collections.abc import AsyncIterator
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from study_ai_assistant_helper.app.config.settings import database_settings

_database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=database_settings.POSTGRES_USER,
    password=database_settings.POSTGRES_PASSWORD.get_secret_value(),
    host=database_settings.POSTGRES_HOST,
    port=database_settings.POSTGRES_PORT,
    database=database_settings.POSTGRES_DB,
)

async_engine = create_async_engine(
    _database_url,
    pool_pre_ping=True,
    pool_size=database_settings.DB_POOL_SIZE,
    max_overflow=database_settings.DB_MAX_OVERFLOW,
    pool_timeout=database_settings.DB_POOL_TIMEOUT_SECONDS,
    pool_recycle=database_settings.DB_POOL_RECYCLE_SECONDS,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield a request-scoped session and close it when the request completes."""
    async with async_session_maker() as session:
        yield session
