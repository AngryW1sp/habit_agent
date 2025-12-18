import pytest

from app.core.config import settings

API_PREFIX = "/api/v1"


@pytest.mark.anyio
async def test_health(client):
    r = await client.get(f"{API_PREFIX}/health")
    assert r.status_code == 200
    assert r.json() == {
        "status": "ok",
        "service": "habit_service",
        "version": "0.1.0",
    }


@pytest.mark.anyio
async def test_create_habit(client):
    habit_data = {
        "name": "Test Habit",
        "description": "This is a test habit",
    }
    r = await client.post(f"{API_PREFIX}/habits/", json=habit_data)
    assert r.status_code == 201
    response_data = r.json()
    assert response_data["name"] == habit_data["name"]
    assert response_data["description"] == habit_data["description"]
    assert "id" in response_data

    r2 = await client.get(f"{API_PREFIX}/habits/{response_data['id']}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["name"] == habit_data["name"]
    assert data["description"] == habit_data["description"]
    assert data["id"] == response_data["id"]

@pytest.mark.anyio
async def test_create_habit_missing_name(client):
    habit_data = {
        "description": "This is a test habit without a name",}
    r = await client.post(f"{API_PREFIX}/habits/", json=habit_data)
    assert r.status_code == 422  # Unprocessable Entity due to validation error

@pytest.mark.anyio
async def test_create_habit_empty_name(client):
    habit_data = {
        "name": "",
        "description": "This is a test habit with an empty name",
    }
    r = await client.post(f"{API_PREFIX}/habits/", json=habit_data)
    assert r.status_code == 422  # Unprocessable Entity due to validation error

@pytest.mark.anyio
async def test_create_habit_long_name(client):
    habit_data = {
        "name": "AAAA",
        "description": "This is a test habit with a too long name",
    }
    r = await client.post(f"{API_PREFIX}/habits/", json=habit_data)
    assert r.status_code == 422  # Unprocessable Entity due to validation error

@pytest.mark.anyio
async def test_create_habit_no_description(client):
    habit_data = {
        "name": "Test Habit Without Description",
    }
    r = await client.post(f"{API_PREFIX}/habits/", json=habit_data)
    assert r.status_code == 201
    response_data = r.json()
    assert response_data["name"] == habit_data["name"]
    assert response_data["description"] is None
    assert "id" in response_data

