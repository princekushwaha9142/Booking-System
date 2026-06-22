import pytest

TASK = {"title": "Book Flight to Goa", "category": "travel"}


@pytest.mark.asyncio
async def test_create_task(auth_client):
    client, _ = auth_client
    resp = await client.post("/api/v1/tasks/", json=TASK)
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_update_task_status(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/tasks/", json=TASK)
    tid = create.json()["id"]
    resp = await client.patch(f"/api/v1/tasks/{tid}", json={"status": "booked"})
    assert resp.json()["status"] == "booked"


@pytest.mark.asyncio
async def test_delete_task(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/tasks/", json=TASK)
    tid = create.json()["id"]
    await client.delete(f"/api/v1/tasks/{tid}")
    resp = await client.get(f"/api/v1/tasks/{tid}")
    assert resp.status_code == 404