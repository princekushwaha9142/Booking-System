import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
    })
    assert resp.status_code == 201
    assert resp.json()["email"] == "newuser@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "username": "dup1", "password": "password123"}
    await client.post("/api/v1/auth/register", json=payload)
    payload["username"] = "dup2"
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_register_weak_password(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "weak@example.com",
        "username": "weakuser",
        "password": "123",
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "password123",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "password123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "refresh@example.com",
        "username": "refreshuser",
        "password": "testpass123",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "refresh@example.com",
        "password": "testpass123",
    })
    refresh_token = resp.json()["refresh_token"]
    resp2 = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert resp2.status_code == 200
    assert "access_token" in resp2.json()


@pytest.mark.asyncio
async def test_get_me(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_me_invalid_token(client):
    client.headers.update({"Authorization": "Bearer invalidtoken"})
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401
    client.headers.clear()