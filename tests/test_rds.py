import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import rds as rds_module

BASE_URL = "/api/v1/rds"


@pytest.fixture(autouse=True)
def clear_db():
    rds_module.rds_db.clear()
    rds_module._next_id = 1
    yield
    rds_module.rds_db.clear()
    rds_module._next_id = 1


@pytest.fixture
def client():
    return TestClient(app)


def _create_rds(client, **overrides):
    payload = {
        "db_instance_identifier": "test-mysql-01",
        "engine": "mysql",
        "engine_version": "8.0.35",
        "db_instance_class": "db.t3.micro",
        "allocated_storage": 20,
        "master_username": "admin",
    }
    payload.update(overrides)
    return client.post(BASE_URL, json=payload)


# =========================================================================
# POST /api/v1/rds - Create RDS Instance
# =========================================================================


class TestCreateRDS:
    def test_create_rds_success(self, client):
        resp = _create_rds(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["db_instance_identifier"] == "test-mysql-01"
        assert data["engine"] == "mysql"
        assert data["engine_version"] == "8.0.35"
        assert data["db_instance_class"] == "db.t3.micro"
        assert data["allocated_storage"] == 20
        assert data["master_username"] == "admin"
        assert data["status"] == "creating"
        assert data["port"] == 3306
        assert data["multi_az"] is False
        assert data["region"] == "us-east-1"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_rds_missing_required_field(self, client):
        resp = client.post(
            BASE_URL,
            json={"db_instance_identifier": "test-db", "engine": "mysql"},
        )
        assert resp.status_code == 422

    def test_create_rds_duplicate_identifier(self, client):
        _create_rds(client)
        resp = _create_rds(client)
        assert resp.status_code == 400
        data = resp.json()
        assert data["code"] == "DUPLICATE_IDENTIFIER"

    def test_create_rds_invalid_engine(self, client):
        resp = _create_rds(client, engine="invalid_engine")
        assert resp.status_code == 422


# =========================================================================
# GET /api/v1/rds - List RDS Instances
# =========================================================================


class TestListRDS:
    def test_list_rds_empty(self, client):
        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_rds_pagination(self, client):
        for i in range(5):
            _create_rds(client, db_instance_identifier=f"test-db-{i}")

        resp = client.get(BASE_URL, params={"page": 1, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["pages"] == 3

    def test_list_rds_second_page(self, client):
        for i in range(5):
            _create_rds(client, db_instance_identifier=f"test-db-{i}")

        resp = client.get(BASE_URL, params={"page": 2, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 2

    def test_list_rds_total_correct(self, client):
        for i in range(3):
            _create_rds(client, db_instance_identifier=f"test-db-{i}")

        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3


# =========================================================================
# GET /api/v1/rds/{rds_id} - Get Single RDS Instance
# =========================================================================


class TestGetRDS:
    def test_get_rds_success(self, client):
        create_resp = _create_rds(client)
        rds_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{rds_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == rds_id
        assert data["db_instance_identifier"] == "test-mysql-01"
        assert data["engine"] == "mysql"

    def test_get_rds_not_found(self, client):
        resp = client.get(f"{BASE_URL}/99999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"


# =========================================================================
# PUT /api/v1/rds/{rds_id} - Update RDS Instance
# =========================================================================


class TestUpdateRDS:
    def test_update_rds_success(self, client):
        create_resp = _create_rds(client)
        rds_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{rds_id}",
            json={"db_instance_class": "db.m5.large", "allocated_storage": 100},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["db_instance_class"] == "db.m5.large"
        assert data["allocated_storage"] == 100
        assert data["db_instance_identifier"] == "test-mysql-01"

    def test_update_rds_not_found(self, client):
        resp = client.put(
            f"{BASE_URL}/99999",
            json={"db_instance_class": "db.m5.large"},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"

    def test_update_rds_preserves_other_fields(self, client):
        create_resp = _create_rds(
            client, endpoint="test-mysql-01.abc.us-east-1.rds.amazonaws.com"
        )
        rds_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{rds_id}", json={"allocated_storage": 50}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["allocated_storage"] == 50
        assert (
            data["endpoint"]
            == "test-mysql-01.abc.us-east-1.rds.amazonaws.com"
        )
        assert data["engine"] == "mysql"
        assert data["master_username"] == "admin"


# =========================================================================
# DELETE /api/v1/rds/{rds_id} - Delete RDS Instance
# =========================================================================


class TestDeleteRDS:
    def test_delete_rds_success(self, client):
        create_resp = _create_rds(client)
        rds_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{rds_id}")
        assert resp.status_code == 204

    def test_delete_rds_then_get_returns_404(self, client):
        create_resp = _create_rds(client)
        rds_id = create_resp.json()["id"]

        client.delete(f"{BASE_URL}/{rds_id}")
        resp = client.get(f"{BASE_URL}/{rds_id}")
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_delete_rds_not_found(self, client):
        resp = client.delete(f"{BASE_URL}/99999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"
