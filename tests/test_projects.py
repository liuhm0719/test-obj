import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.project import projects_db


@pytest.fixture(autouse=True)
def clear_db():
    projects_db.clear()
    yield
    projects_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def _create_project(client, name="Test Project", **kwargs):
    payload = {"name": name, **kwargs}
    return client.post("/api/v1/projects", json=payload)


class TestCreateProject:
    def test_create_project_success(self, client):
        resp = _create_project(client, name="My Project", description="desc")
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["name"] == "My Project"
        assert data["description"] == "desc"
        assert data["status"] == "active"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_project_only_required_fields(self, client):
        resp = client.post("/api/v1/projects", json={"name": "Minimal"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Minimal"
        assert data["description"] is None
        assert data["status"] == "active"

    def test_create_project_default_status_active(self, client):
        resp = _create_project(client)
        assert resp.status_code == 201
        assert resp.json()["status"] == "active"


class TestListProjects:
    def test_list_projects_empty(self, client):
        resp = client.get("/api/v1/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_projects_pagination(self, client):
        for i in range(5):
            _create_project(client, name=f"Project {i}")

        resp = client.get("/api/v1/projects", params={"page": 1, "size": 3})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 3
        assert data["page"] == 1
        assert data["size"] == 3

    def test_list_projects_page_two(self, client):
        for i in range(5):
            _create_project(client, name=f"Project {i}")

        resp = client.get("/api/v1/projects", params={"page": 2, "size": 3})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2

    def test_list_projects_total_correct(self, client):
        for i in range(3):
            _create_project(client, name=f"Project {i}")

        resp = client.get("/api/v1/projects")
        assert resp.status_code == 200
        assert resp.json()["total"] == 3


class TestGetProject:
    def test_get_project_success(self, client):
        create_resp = _create_project(client, name="Fetch Me")
        project_id = create_resp.json()["id"]

        resp = client.get(f"/api/v1/projects/{project_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == project_id
        assert data["name"] == "Fetch Me"

    def test_get_project_not_found(self, client):
        resp = client.get(
            "/api/v1/projects/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


class TestUpdateProject:
    def test_update_project_name(self, client):
        create_resp = _create_project(client, name="Old Name")
        project_id = create_resp.json()["id"]

        resp = client.put(
            f"/api/v1/projects/{project_id}", json={"name": "New Name"}
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

    def test_update_project_status(self, client):
        create_resp = _create_project(client)
        project_id = create_resp.json()["id"]

        resp = client.put(
            f"/api/v1/projects/{project_id}", json={"status": "archived"}
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "archived"

    def test_update_project_not_found(self, client):
        resp = client.put(
            "/api/v1/projects/00000000-0000-0000-0000-000000000000",
            json={"name": "Whatever"},
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_update_project_updated_at_changes(self, client):
        create_resp = _create_project(client)
        project_id = create_resp.json()["id"]
        original_updated_at = create_resp.json()["updated_at"]

        resp = client.put(
            f"/api/v1/projects/{project_id}", json={"name": "Updated"}
        )
        assert resp.status_code == 200
        assert resp.json()["updated_at"] >= original_updated_at


class TestDeleteProject:
    def test_delete_project_success(self, client):
        create_resp = _create_project(client, name="Delete Me")
        project_id = create_resp.json()["id"]

        resp = client.delete(f"/api/v1/projects/{project_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == project_id

    def test_delete_project_not_found(self, client):
        resp = client.delete(
            "/api/v1/projects/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_delete_project_then_get_returns_404(self, client):
        create_resp = _create_project(client)
        project_id = create_resp.json()["id"]

        client.delete(f"/api/v1/projects/{project_id}")
        resp = client.get(f"/api/v1/projects/{project_id}")
        assert resp.status_code == 404
