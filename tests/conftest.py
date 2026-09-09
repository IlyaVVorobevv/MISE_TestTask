from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app


@pytest_asyncio.fixture
async def async_session_factory():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield session_factory
    await engine.dispose()


@pytest_asyncio.fixture
async def client(async_session_factory) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        async with async_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def valid_payload() -> dict:
    import datetime as dt

    tomorrow = dt.date.today() + dt.timedelta(days=1)
    return {
        "name": "Иван Петров",
        "phone": "+79161234567",
        "booking_date": tomorrow.isoformat(),
        "booking_time": "19:00:00",
        "guests": 4,
    }
