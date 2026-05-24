"""Test fixtures: in-memory async SQLite database and HTTP client."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from kingdom.api.app import create_app
from kingdom.db import get_db
from kingdom.models import Base


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    """Provide an isolated in-memory SQLite session with tables created."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as s:
        yield s
    await engine.dispose()


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    """HTTP client bound to the app with the test session injected."""
    app = create_app()

    async def _override_get_db() -> AsyncIterator[AsyncSession]:
        yield session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
