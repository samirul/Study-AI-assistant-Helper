"""Alembic migration configuration for the application database.

This module wires Alembic to the project's SQLAlchemy metadata and async
engine so migrations can run in both offline and online modes.
"""

import asyncio
from logging.config import fileConfig
from sqlalchemy.engine import Connection
from alembic import context
from study_ai_assistant_helper.app.db.base import metadata
from study_ai_assistant_helper.app.db.session import async_engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""
    context.configure(
        url=async_engine.url,
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configure Alembic and run migrations using a synchronous connection."""
    context.configure(
        connection=connection,
        target_metadata=metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations through the application's async PostgreSQL engine."""
    try:
        async with async_engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await async_engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
