import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.membership import project_members, user_projects
from app.models.project import projects_db
from app.models.user import users_db


@pytest.fixture(autouse=True)
def clear_db():
    projects_db.clear()
    users_db.clear()
    project_members.clear()
    user_projects.clear()
    yield
    projects_db.clear()
    users_db.clear()
    project_members.clear()
    user_projects.clear()


@pytest.fixture
def client():
    return TestClient(app)


def _create_project(client, name="Test Project"):
    resp = client.post("/api/v1/projects", json={"name": name})
    return resp.json()["id"]


def _create_user(client, username="testuser", email="test@example.com"):
    resp = client.post(
        "/api/v1/users", json={"username": username, "email": email}
    )
    return resp.json()["id"]


class TestAddMember:
    def test_add_member_success(self, client):
        project_id = _create_project(client)
        user_id = _create_user(client)

        resp = client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": user_id},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["user_id"] == user_id
        assert data["project_id"] == project_id
        assert "added_at" in data

    def test_add_member_project_not_found(self, client):
        user_id = _create_user(client)
        resp = client.post(
            "/api/v1/projects/00000000-0000-0000-0000-000000000000/members",
            json={"user_id": user_id},
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_add_member_user_not_found(self, client):
        project_id = _create_project(client)
        resp = client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": 99999},
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_add_member_duplicate_returns_409(self, client):
        project_id = _create_project(client)
        user_id = _create_user(client)

        client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": user_id},
        )
        resp = client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": user_id},
        )
        assert resp.status_code == 409
        assert resp.json()["code"] == "ALREADY_EXISTS"


class TestRemoveMember:
    def test_remove_member_success(self, client):
        project_id = _create_project(client)
        user_id = _create_user(client)
        client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": user_id},
        )

        resp = client.delete(
            f"/api/v1/projects/{project_id}/members/{user_id}"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == user_id
        assert data["project_id"] == project_id

    def test_remove_member_not_a_member(self, client):
        project_id = _create_project(client)
        user_id = _create_user(client)

        resp = client.delete(
            f"/api/v1/projects/{project_id}/members/{user_id}"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_remove_member_project_not_found(self, client):
        resp = client.delete(
            "/api/v1/projects/00000000-0000-0000-0000-000000000000/members/1"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


class TestListProjectMembers:
    def test_list_members_empty(self, client):
        project_id = _create_project(client)

        resp = client.get(f"/api/v1/projects/{project_id}/members")
        assert resp.status_code == 200
        data = resp.json()
        assert data["members"] == []
        assert data["total"] == 0
        assert data["project_id"] == project_id

    def test_list_members_multiple(self, client):
        project_id = _create_project(client)
        uid1 = _create_user(client, username="user1", email="u1@x.com")
        uid2 = _create_user(client, username="user2", email="u2@x.com")

        client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": uid1},
        )
        client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": uid2},
        )

        resp = client.get(f"/api/v1/projects/{project_id}/members")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        member_ids = {m["id"] for m in data["members"]}
        assert uid1 in member_ids
        assert uid2 in member_ids

    def test_list_members_project_not_found(self, client):
        resp = client.get(
            "/api/v1/projects/00000000-0000-0000-0000-000000000000/members"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


class TestListUserProjects:
    def test_user_no_projects(self, client):
        user_id = _create_user(client)

        resp = client.get(f"/api/v1/users/{user_id}/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert data["projects"] == []
        assert data["total"] == 0
        assert data["user_id"] == user_id

    def test_user_multiple_projects(self, client):
        user_id = _create_user(client)
        pid1 = _create_project(client, name="P1")
        pid2 = _create_project(client, name="P2")

        client.post(
            f"/api/v1/projects/{pid1}/members", json={"user_id": user_id}
        )
        client.post(
            f"/api/v1/projects/{pid2}/members", json={"user_id": user_id}
        )

        resp = client.get(f"/api/v1/users/{user_id}/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        project_ids = {p["id"] for p in data["projects"]}
        assert pid1 in project_ids
        assert pid2 in project_ids

    def test_user_projects_user_not_found(self, client):
        resp = client.get("/api/v1/users/99999/projects")
        assert resp.status_code == 404
        assert resp.json()["code"] == "USER_NOT_FOUND"


class TestCascadeCleanup:
    def test_delete_project_removes_from_user_projects(self, client):
        project_id = _create_project(client)
        user_id = _create_user(client)
        client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": user_id},
        )

        client.delete(f"/api/v1/projects/{project_id}")

        resp = client.get(f"/api/v1/users/{user_id}/projects")
        assert resp.status_code == 200
        data = resp.json()
        project_ids = [p["id"] for p in data["projects"]]
        assert project_id not in project_ids

    def test_delete_user_removes_from_project_members(self, client):
        project_id = _create_project(client)
        user_id = _create_user(client)
        client.post(
            f"/api/v1/projects/{project_id}/members",
            json={"user_id": user_id},
        )

        client.delete(f"/api/v1/users/{user_id}")

        resp = client.get(f"/api/v1/projects/{project_id}/members")
        assert resp.status_code == 200
        data = resp.json()
        member_ids = [m["id"] for m in data["members"]]
        assert user_id not in member_ids
