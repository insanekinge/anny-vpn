from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings, get_settings
from app.db.base import Base
from app.db.seed import ensure_seed_data


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def create_engine_and_session_factory(
    database_url: str,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    normalized_url = normalize_database_url(database_url)
    engine = create_async_engine(
        normalized_url,
        future=True,
        pool_pre_ping=True,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    return engine, session_factory


def get_engine(settings: Settings | None = None) -> AsyncEngine:
    global _engine, _session_factory

    if _engine is None or _session_factory is None:
        app_settings = settings or get_settings()
        _engine, _session_factory = create_engine_and_session_factory(app_settings.database_url)
    return _engine


def get_session_factory(settings: Settings | None = None) -> async_sessionmaker[AsyncSession]:
    global _engine, _session_factory

    if _engine is None or _session_factory is None:
        app_settings = settings or get_settings()
        _engine, _session_factory = create_engine_and_session_factory(app_settings.database_url)
    return _session_factory


async def init_database(settings: Settings | None = None) -> None:
    engine = get_engine(settings)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await ensure_seed_data(get_session_factory(settings))


async def get_db_session() -> AsyncIterator[AsyncSession]:
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session
