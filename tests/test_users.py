#this whole thing is on page 16 on lecture 2
#builds a valid user JSON body for tests
import pytest

def user_payload(
    uid=1,
    name="Keelan",
    email="keelan@atu.ie",
    age=22,
    student_id="S1234567",
):
    return {
        "user_id": uid,
        "name": name,
        "email": email,
        "age": age,
        "student_id": student_id,
    }

# Happy path: valid POST must return 201 Created
def test_create_user_returns_201(client):
    # client comes from conftest — fake Swagger caller
    response = client.post("/api/users", json=user_payload())
    assert response.status_code == 201  # Created
    assert response.json()["name"] == "Keelan"  # body should match what we sent


# Error path: same user_id twice must return 409 Conflict
def test_duplicate_user_id_returns_409(client):
    client.post("/api/users", json=user_payload(uid=2))  # creating user with id 2
    response = client.post("/api/users", json=user_payload(uid=2))  # creating it again (duplicate)
    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()

# Error path: invalid student_id must be rejected by the schema (422)
#FULLY IN LECTURE NOTES PAGE 20
@pytest.mark.parametrize(
    "bad_student_id",
    ["1234567", "s1234567", "S123", "S12345678"],  # each one fails the S+7digits rule
)
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post(
        "/api/users",
        json=user_payload(uid=3, student_id=bad_student_id),
    )
    assert response.status_code == 422




#none of this stuff below is in the lecture note

# GET all users — after creating one, list should contain it
def test_get_users_returns_created_users(client):
    client.post("/api/users", json=user_payload(uid=10, name="Alice", email="alice@atu.ie"))
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == 10
    assert data[0]["name"] == "Alice"

# GET one user — existing id returns 200
def test_get_existing_user_returns_200(client):
    client.post("/api/users", json=user_payload(uid=11))
    response = client.get("/api/users/11")
    assert response.status_code == 200
    assert response.json()["user_id"] == 11

# GET missing user — unknown id returns 404
def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"



# DELETE existing user → 204 No Content (empty body)
def test_delete_existing_user_returns_204(client):
    client.post("/api/users", json=user_payload(uid=20))
    response = client.delete("/api/users/20")
    assert response.status_code == 204
    assert response.content == b""  # no JSON body
# DELETE missing user → 404

def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"