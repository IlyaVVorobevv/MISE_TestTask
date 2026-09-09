import datetime as dt
import pytest


@pytest.mark.asyncio
async def test_create_booking_success(client, valid_payload):
    response = await client.post("/bookings", json=valid_payload)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "active"
    assert body["name"] == valid_payload["name"]
    assert body["phone"] == valid_payload["phone"]
    assert "id" in body


@pytest.mark.asyncio
async def test_create_booking_past_date(client, valid_payload):
    valid_payload["booking_date"] = (
        dt.date.today() - dt.timedelta(days=1)
    ).isoformat()
    response = await client.post("/bookings", json=valid_payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_booking_too_far(client, valid_payload):
    valid_payload["booking_date"] = (
        dt.date.today() + dt.timedelta(days=91)
    ).isoformat()
    response = await client.post("/bookings", json=valid_payload)
    assert response.status_code == 422



@pytest.mark.asyncio
async def test_get_booking_by_id(client, valid_payload):
    created = await client.post("/bookings", json=valid_payload)
    booking_id = created.json()["id"]

    response = await client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["id"] == booking_id


@pytest.mark.asyncio
async def test_get_booking_not_found(client):
    response = await client.get("/bookings/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}


@pytest.mark.asyncio
async def test_cancel_booking_not_found(client):
    response = await client.delete("/bookings/999")
    assert response.status_code == 404


