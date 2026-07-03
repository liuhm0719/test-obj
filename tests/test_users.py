import time

import pytest
from fastapi.testclient import TestClient

import app.models.user as user_module
from app.main import app
from app.models.user import users_db

BASE_URL = "/api/v1/users"


@pytest.fixture(autouse=True)
def clear_db():
    users_db.clear()
    user_module._user_id_counter = 0
    yield
    users_db.clear()
    user_module._user_id_counter = 0


@pytest.fixture
def client():
    return TestClient(app)


def _create_user(client, username="testuser", email="test@example.com"):
    return client.post(BASE_URL, json={"username": username, "email": email})


# =========================================================================
# POST /api/users - Create User
# =========================================================================


class TestCreateUser:
    def test_create_user_success(self, client):
        resp = _create_user(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_user_username_too_short(self, client):
        resp = client.post(BASE_URL, json={"username": "ab", "email": "a@b.com"})
        assert resp.status_code == 422

    def test_create_user_username_too_long(self, client):
        resp = client.post(
            BASE_URL, json={"username": "a" * 33, "email": "a@b.com"}
        )
        assert resp.status_code == 422

    def test_create_user_invalid_email(self, client):
        resp = client.post(
            BASE_URL, json={"username": "validuser", "email": "not-an-email"}
        )
        assert resp.status_code == 422

    def test_create_user_duplicate_username(self, client):
        _create_user(client, username="dupeuser", email="first@example.com")
        resp = _create_user(client, username="dupeuser", email="second@example.com")
        assert resp.status_code == 400
        assert resp.json()["code"] == "USER_EXISTS"

    def test_create_user_duplicate_email(self, client):
        _create_user(client, username="user1", email="same@example.com")
        resp = _create_user(client, username="user2", email="same@example.com")
        assert resp.status_code == 400
        assert resp.json()["code"] == "EMAIL_EXISTS"

    def test_create_user_with_phone(self, client):
        resp = client.post(
            BASE_URL,
            json={"username": "phoneuser", "email": "p@test.com", "phone": "+8613800138000"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["phone"] == "+8613800138000"

    def test_create_user_without_phone(self, client):
        resp = _create_user(client)
        assert resp.status_code == 201
        assert resp.json()["phone"] is None

    def test_create_user_invalid_phone(self, client):
        resp = client.post(
            BASE_URL,
            json={"username": "phoneuser", "email": "p@test.com", "phone": "abc"},
        )
        assert resp.status_code == 422

    def test_create_user_duplicate_phone(self, client):
        client.post(
            BASE_URL,
            json={"username": "user1", "email": "u1@test.com", "phone": "+8613800138000"},
        )
        resp = client.post(
            BASE_URL,
            json={"username": "user2", "email": "u2@test.com", "phone": "+8613800138000"},
        )
        assert resp.status_code == 400
        assert resp.json()["code"] == "PHONE_EXISTS"


# =========================================================================
# GET /api/users - List Users
# =========================================================================


class TestListUsers:
    def test_list_users_empty(self, client):
        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_users_pagination(self, client):
        for i in range(5):
            _create_user(client, username=f"user{i}", email=f"user{i}@test.com")

        resp = client.get(BASE_URL, params={"page": 1, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["pages"] == 3

    def test_list_users_second_page(self, client):
        for i in range(5):
            _create_user(client, username=f"user{i}", email=f"user{i}@test.com")

        resp = client.get(BASE_URL, params={"page": 2, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 2

    def test_list_users_default_pagination(self, client):
        _create_user(client)
        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert data["size"] == 20


# =========================================================================
# GET /api/users/{user_id} - Get Single User
# =========================================================================


class TestGetUser:
    def test_get_user_success(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{user_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == user_id
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_user_not_found(self, client):
        resp = client.get(f"{BASE_URL}/9999")
        assert resp.status_code == 404
        assert resp.json()["code"] == "USER_NOT_FOUND"


# =========================================================================
# PUT /api/users/{user_id} - Update User
# =========================================================================


class TestUpdateUser:
    def test_update_username(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]
        original_updated_at = create_resp.json()["updated_at"]

        time.sleep(0.01)
        resp = client.put(
            f"{BASE_URL}/{user_id}", json={"username": "newname"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "newname"
        assert data["updated_at"] >= original_updated_at

    def test_update_email(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{user_id}", json={"email": "new@example.com"}
        )
        assert resp.status_code == 200
        assert resp.json()["email"] == "new@example.com"

    def test_update_is_active(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]

        resp = client.put(f"{BASE_URL}/{user_id}", json={"is_active": False})
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    def test_partial_update_preserves_other_fields(self, client):
        create_resp = _create_user(client, username="original", email="orig@test.com")
        user_id = create_resp.json()["id"]

        resp = client.put(f"{BASE_URL}/{user_id}", json={"username": "changed"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "changed"
        assert data["email"] == "orig@test.com"
        assert data["is_active"] is True

    def test_update_user_not_found(self, client):
        resp = client.put(f"{BASE_URL}/9999", json={"username": "ghost"})
        assert resp.status_code == 404
        assert resp.json()["code"] == "USER_NOT_FOUND"

    def test_update_username_conflict(self, client):
        _create_user(client, username="alice", email="alice@test.com")
        create_resp = _create_user(client, username="bob", email="bob@test.com")
        bob_id = create_resp.json()["id"]

        resp = client.put(f"{BASE_URL}/{bob_id}", json={"username": "alice"})
        assert resp.status_code == 400
        assert resp.json()["code"] == "USER_EXISTS"

    def test_update_email_conflict(self, client):
        _create_user(client, username="alice", email="alice@test.com")
        create_resp = _create_user(client, username="bob", email="bob@test.com")
        bob_id = create_resp.json()["id"]

        resp = client.put(f"{BASE_URL}/{bob_id}", json={"email": "alice@test.com"})
        assert resp.status_code == 400
        assert resp.json()["code"] == "EMAIL_EXISTS"

    def test_update_phone(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{user_id}", json={"phone": "+8613900139000"}
        )
        assert resp.status_code == 200
        assert resp.json()["phone"] == "+8613900139000"

    def test_update_phone_conflict(self, client):
        client.post(
            BASE_URL,
            json={"username": "alice", "email": "alice@test.com", "phone": "+8613800138000"},
        )
        create_resp = _create_user(client, username="bob", email="bob@test.com")
        bob_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{bob_id}", json={"phone": "+8613800138000"}
        )
        assert resp.status_code == 400
        assert resp.json()["code"] == "PHONE_EXISTS"


# =========================================================================
# DELETE /api/users/{user_id} - Delete User
# =========================================================================


class TestDeleteUser:
    def test_delete_user_success(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{user_id}")
        assert resp.status_code == 204

    def test_delete_then_get_returns_404(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.json()["id"]

        client.delete(f"{BASE_URL}/{user_id}")
        resp = client.get(f"{BASE_URL}/{user_id}")
        assert resp.status_code == 404
        assert resp.json()["code"] == "USER_NOT_FOUND"

    def test_delete_user_not_found(self, client):
        resp = client.delete(f"{BASE_URL}/9999")
        assert resp.status_code == 404
        assert resp.json()["code"] == "USER_NOT_FOUND"
