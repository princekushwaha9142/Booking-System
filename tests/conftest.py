import os
os.environ["TESTING"] = "true"  

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.database import Base, get_db
from app.core.config import settings
from main import app

TEST_DB_URL = settings.DATABASE_URL.replace("/booking_db", "/booking_test")


@pytest_asyncio.fixture(scope="function")
async def client():
    engine = create_async_engine(TEST_DB_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def auth_client(client):
    reg = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
    })
    assert reg.status_code == 201, f"Register failed: {reg.json()}"

    resp = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123",
    })
    assert resp.status_code == 200, f"Login failed: {resp.json()}"

    token = resp.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client, token