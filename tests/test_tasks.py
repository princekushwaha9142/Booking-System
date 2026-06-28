import pytest

TASK = {"title": "Book Flight to Goa", "category": "travel"}


@pytest.mark.asyncio
async def test_create_task(auth_client):
    client, _ = auth_client
    resp = await client.post("/api/v1/tasks/", json=TASK)
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_list_tasks(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/tasks/")
    assert resp.status_code == 200
    assert "total" in resp.json()


@pytest.mark.asyncio
async def test_filter_tasks_by_status(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/tasks/?task_status=pending")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_filter_tasks_by_category(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/tasks/?category=travel")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_get_task_by_id(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/tasks/", json=TASK)
    tid = create.json()["id"]
    resp = await client.get(f"/api/v1/tasks/{tid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == tid


@pytest.mark.asyncio
async def test_task_not_found(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/tasks/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_task_status(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/tasks/", json=TASK)
    tid = create.json()["id"]
    resp = await client.patch(f"/api/v1/tasks/{tid}", json={"status": "booked"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "booked"


@pytest.mark.asyncio
async def test_delete_task(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/tasks/", json=TASK)
    tid = create.json()["id"]
    await client.delete(f"/api/v1/tasks/{tid}")
    resp2 = await client.get(f"/api/v1/tasks/{tid}")
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_create_task_unauthenticated(client):
    resp = await client.post("/api/v1/tasks/", json=TASK)
    assert resp.status_code == 403