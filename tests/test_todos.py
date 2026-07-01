import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.todo import todos_db


@pytest.fixture(autouse=True)
def clear_db():
    todos_db.clear()
    yield
    todos_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_todo(client):
    resp = client.post("/api/v1/todos", json={"title": "Test todo"})
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["title"] == "Test todo"
    assert data["done"] is False
    assert "created_at" in data


def test_get_todo(client):
    create_resp = client.post("/api/v1/todos", json={"title": "Fetch me"})
    todo_id = create_resp.json()["id"]

    resp = client.get(f"/api/v1/todos/{todo_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == todo_id
    assert data["title"] == "Fetch me"
    assert data["done"] is False


def test_get_todo_not_found(client):
    resp = client.get("/api/v1/todos/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
    data = resp.json()
    assert data["code"] == "NOT_FOUND"


def test_list_todos_pagination(client):
    for i in range(5):
        client.post("/api/v1/todos", json={"title": f"Todo {i}"})

    resp = client.get("/api/v1/todos", params={"page": 1, "size": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 3


def test_update_todo(client):
    create_resp = client.post("/api/v1/todos", json={"title": "Old title"})
    todo_id = create_resp.json()["id"]

    resp = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "New title", "done": True},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New title"
    assert data["done"] is True


def test_delete_todo(client):
    create_resp = client.post("/api/v1/todos", json={"title": "Delete me"})
    todo_id = create_resp.json()["id"]

    resp = client.delete(f"/api/v1/todos/{todo_id}")
    assert resp.status_code == 200

    resp = client.get(f"/api/v1/todos/{todo_id}")
    assert resp.status_code == 404
