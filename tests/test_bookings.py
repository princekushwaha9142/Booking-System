import pytest

HOTEL = {
    "hotel_name": "Grand Delhi Hotel",
    "hotel_location": "Delhi, India",
    "room_type": "Deluxe",
    "check_in_date": "2026-08-01T14:00:00",
    "check_out_date": "2026-08-05T11:00:00",
    "num_guests": 2,
    "total_price": 480.00,
}


@pytest.mark.asyncio
async def test_book_hotel(auth_client):
    client, _ = auth_client
    resp = await client.post("/api/v1/bookings/hotels", json=HOTEL)
    assert resp.status_code == 201
    assert resp.json()["booking_type"] == "hotel"
    assert resp.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_list_bookings(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/bookings/")
    assert resp.status_code == 200
    assert "total" in resp.json()


@pytest.mark.asyncio
async def test_list_bookings_filter(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/bookings/?booking_type=hotel")
    assert resp.status_code == 200
    assert "bookings" in resp.json()


@pytest.mark.asyncio
async def test_get_booking_by_id(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/bookings/hotels", json=HOTEL)
    bid = create.json()["id"]
    resp = await client.get(f"/api/v1/bookings/{bid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == bid


@pytest.mark.asyncio
async def test_get_booking_not_found(auth_client):
    client, _ = auth_client
    resp = await client.get("/api/v1/bookings/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_booking(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/bookings/hotels", json=HOTEL)
    bid = create.json()["id"]
    resp = await client.patch(f"/api/v1/bookings/{bid}", json={"status": "confirmed"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_cancel_booking(auth_client):
    client, _ = auth_client
    create = await client.post("/api/v1/bookings/hotels", json=HOTEL)
    bid = create.json()["id"]
    resp = await client.delete(f"/api/v1/bookings/{bid}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_search_hotels(client):
    resp = await client.post("/api/v1/bookings/search/hotels", json={
        "location": "Mumbai",
        "check_in": "2026-08-01T14:00:00",
        "check_out": "2026-08-03T11:00:00",
        "num_guests": 1,
    })
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_search_flights(client):
    resp = await client.post("/api/v1/bookings/search/flights", json={
        "origin": "Delhi",
        "destination": "Mumbai",
        "departure_date": "2026-09-01T06:00:00",
        "num_passengers": 1,
    })
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_unauthenticated(client):
    resp = await client.post("/api/v1/bookings/hotels", json=HOTEL)
    assert resp.status_code == 403