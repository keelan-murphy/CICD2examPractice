import pytest


def user_payload(
    name="Paul",
    email="paul@atu.ie",
    age=25,
    sid="S1234567",
):
    
    return {
        "name": name,
        "email": email,
        "age": age,
        "student_id": sid,
    }


def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Paul"

def test_duplicate_user_returns_409(client):
    client.post("/api/users", json=user_payload())
    response = client.post("/api/users", json=user_payload())
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()