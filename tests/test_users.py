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

#409 TESTS


@pytest.mark.parametrize(
    "bad_sid",
    ["1234567", "s1234567", "S123", "S12345678"],
)
def test_bad_student_id_returns_422(client, bad_sid):
    response = client.post(
        "/api/users",
        json=user_payload(sid=bad_sid),
    )
    assert response.status_code == 422


    #GET TESTS

def test_get_users(client):
    client.post("/api/users", json=user_payload())
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["student_id"] == "S1234567"


def test_get_user_by_id(client):
    created = client.post("/api/users", json=user_payload()).json()
    user_id = created["id"]
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "paul@atu.ie"


def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


#DELETE TESTS
def test_delete_user(client):
    created = client.post("/api/users", json=user_payload()).json()
    user_id = created["id"]
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/api/users/{user_id}").status_code == 404


def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()