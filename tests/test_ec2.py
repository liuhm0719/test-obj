import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.ec2 import ec2_db

BASE_URL = "/api/v1/ec2"


@pytest.fixture(autouse=True)
def clear_db():
    ec2_db.clear()
    yield
    ec2_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def _create_ec2(client, **overrides):
    payload = {
        "instance_id": "i-0abc1234def56789",
        "name": "web-server-01",
        "instance_type": "t2.micro",
        "state": "running",
        "region": "us-east-1",
    }
    payload.update(overrides)
    return client.post(BASE_URL, json=payload)


# =========================================================================
# POST /api/v1/ec2 - Create EC2 Instance
# =========================================================================


class TestCreateEC2:
    def test_create_ec2_success(self, client):
        resp = _create_ec2(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["instance_id"] == "i-0abc1234def56789"
        assert data["name"] == "web-server-01"
        assert data["instance_type"] == "t2.micro"
        assert data["state"] == "running"
        assert data["region"] == "us-east-1"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_ec2_with_optional_fields(self, client):
        resp = _create_ec2(
            client,
            availability_zone="us-east-1a",
            private_ip="10.0.1.100",
            public_ip="54.123.45.67",
            vpc_id="vpc-0abc1234",
            key_name="my-key-pair",
            launch_time="2026-07-01T10:00:00Z",
            tags={"Environment": "production"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["availability_zone"] == "us-east-1a"
        assert data["private_ip"] == "10.0.1.100"
        assert data["public_ip"] == "54.123.45.67"
        assert data["vpc_id"] == "vpc-0abc1234"
        assert data["key_name"] == "my-key-pair"
        assert data["launch_time"] == "2026-07-01T10:00:00Z"
        assert data["tags"] == {"Environment": "production"}

    def test_create_ec2_missing_required_field(self, client):
        resp = client.post(BASE_URL, json={"instance_id": "i-123", "name": "test"})
        assert resp.status_code == 422

    def test_create_ec2_invalid_state(self, client):
        resp = _create_ec2(client, state="invalid_state")
        assert resp.status_code == 422


# =========================================================================
# GET /api/v1/ec2 - List EC2 Instances
# =========================================================================


class TestListEC2:
    def test_list_ec2_empty(self, client):
        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_ec2_pagination(self, client):
        for i in range(5):
            _create_ec2(client, instance_id=f"i-{i:017d}", name=f"server-{i}")

        resp = client.get(BASE_URL, params={"page": 1, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["pages"] == 3

    def test_list_ec2_second_page(self, client):
        for i in range(5):
            _create_ec2(client, instance_id=f"i-{i:017d}", name=f"server-{i}")

        resp = client.get(BASE_URL, params={"page": 2, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 2

    def test_list_ec2_total_correct(self, client):
        for i in range(3):
            _create_ec2(client, instance_id=f"i-{i:017d}", name=f"server-{i}")

        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3


# =========================================================================
# GET /api/v1/ec2/{ec2_id} - Get Single EC2 Instance
# =========================================================================


class TestGetEC2:
    def test_get_ec2_success(self, client):
        create_resp = _create_ec2(client)
        ec2_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{ec2_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == ec2_id
        assert data["instance_id"] == "i-0abc1234def56789"
        assert data["name"] == "web-server-01"
        assert data["state"] == "running"

    def test_get_ec2_not_found(self, client):
        resp = client.get(f"{BASE_URL}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"


# =========================================================================
# PUT /api/v1/ec2/{ec2_id} - Update EC2 Instance
# =========================================================================


class TestUpdateEC2:
    def test_update_ec2_success(self, client):
        create_resp = _create_ec2(client)
        ec2_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{ec2_id}",
            json={"name": "updated-server", "state": "stopped"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "updated-server"
        assert data["state"] == "stopped"
        assert data["instance_id"] == "i-0abc1234def56789"

    def test_update_ec2_not_found(self, client):
        resp = client.put(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000",
            json={"name": "ghost"},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"

    def test_update_ec2_invalid_state(self, client):
        create_resp = _create_ec2(client)
        ec2_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{ec2_id}",
            json={"state": "invalid_state"},
        )
        assert resp.status_code == 422

    def test_update_ec2_preserves_other_fields(self, client):
        create_resp = _create_ec2(
            client, availability_zone="us-east-1a", private_ip="10.0.1.100"
        )
        ec2_id = create_resp.json()["id"]

        resp = client.put(f"{BASE_URL}/{ec2_id}", json={"name": "new-name"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "new-name"
        assert data["availability_zone"] == "us-east-1a"
        assert data["private_ip"] == "10.0.1.100"
        assert data["region"] == "us-east-1"


# =========================================================================
# DELETE /api/v1/ec2/{ec2_id} - Delete EC2 Instance
# =========================================================================


class TestDeleteEC2:
    def test_delete_ec2_success(self, client):
        create_resp = _create_ec2(client)
        ec2_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{ec2_id}")
        assert resp.status_code == 204

    def test_delete_ec2_then_get_returns_404(self, client):
        create_resp = _create_ec2(client)
        ec2_id = create_resp.json()["id"]

        client.delete(f"{BASE_URL}/{ec2_id}")
        resp = client.get(f"{BASE_URL}/{ec2_id}")
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_delete_ec2_not_found(self, client):
        resp = client.delete(f"{BASE_URL}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"
