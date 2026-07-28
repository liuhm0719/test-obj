import csv
import io

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.subnet import create_subnet, get_subnets, subnet_db

BASE_URL = "/api/v1/subnets"


@pytest.fixture(autouse=True)
def clear_db():
    subnet_db.clear()
    yield
    subnet_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def _create_subnet(client, **overrides):
    payload = {
        "subnet_id": "subnet-0abc1234",
        "name": "private-subnet-01",
        "vpc_id": "vpc-0abc1234",
        "cidr_block": "10.0.1.0/24",
        "availability_zone": "us-east-1a",
        "state": "available",
        "region": "us-east-1",
    }
    payload.update(overrides)
    return client.post(BASE_URL, json=payload)


# =========================================================================
# POST /api/v1/subnets - Create Subnet
# =========================================================================


class TestCreateSubnet:
    def test_create_subnet_success(self, client):
        resp = _create_subnet(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["subnet_id"] == "subnet-0abc1234"
        assert data["name"] == "private-subnet-01"
        assert data["vpc_id"] == "vpc-0abc1234"
        assert data["cidr_block"] == "10.0.1.0/24"
        assert data["availability_zone"] == "us-east-1a"
        assert data["state"] == "available"
        assert data["region"] == "us-east-1"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_subnet_with_optional_fields(self, client):
        resp = _create_subnet(
            client,
            map_public_ip_on_launch=True,
            available_ip_count=251,
            tags={"Environment": "production", "Team": "backend"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["map_public_ip_on_launch"] is True
        assert data["available_ip_count"] == 251
        assert data["tags"] == {"Environment": "production", "Team": "backend"}

    def test_create_subnet_missing_required_field(self, client):
        resp = client.post(
            BASE_URL, json={"subnet_id": "subnet-123", "name": "test"}
        )
        assert resp.status_code == 422

    def test_create_subnet_invalid_state(self, client):
        resp = _create_subnet(client, state="invalid_state")
        assert resp.status_code == 422


# =========================================================================
# GET /api/v1/subnets - List Subnets
# =========================================================================


class TestListSubnet:
    def test_list_subnet_empty(self, client):
        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_subnet_pagination(self, client):
        for i in range(5):
            _create_subnet(
                client, subnet_id=f"subnet-{i:08d}", name=f"subnet-{i}"
            )

        resp = client.get(BASE_URL, params={"page": 1, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["pages"] == 3

    def test_list_subnet_second_page(self, client):
        for i in range(5):
            _create_subnet(
                client, subnet_id=f"subnet-{i:08d}", name=f"subnet-{i}"
            )

        resp = client.get(BASE_URL, params={"page": 2, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 2

    def test_list_subnet_total_correct(self, client):
        for i in range(3):
            _create_subnet(
                client, subnet_id=f"subnet-{i:08d}", name=f"subnet-{i}"
            )

        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3


# =========================================================================
# GET /api/v1/subnets/{subnet_id} - Get Single Subnet
# =========================================================================


class TestGetSubnet:
    def test_get_subnet_success(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{subnet_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == subnet_id
        assert data["subnet_id"] == "subnet-0abc1234"
        assert data["name"] == "private-subnet-01"
        assert data["state"] == "available"

    def test_get_subnet_not_found(self, client):
        resp = client.get(f"{BASE_URL}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"


# =========================================================================
# PUT /api/v1/subnets/{subnet_id} - Update Subnet
# =========================================================================


class TestUpdateSubnet:
    def test_update_subnet_success(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}",
            json={"name": "updated-subnet", "state": "pending"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "updated-subnet"
        assert data["state"] == "pending"
        assert data["subnet_id"] == "subnet-0abc1234"

    def test_update_subnet_not_found(self, client):
        resp = client.put(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000",
            json={"name": "ghost"},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"

    def test_update_subnet_invalid_state(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}",
            json={"state": "invalid_state"},
        )
        assert resp.status_code == 422

    def test_update_subnet_preserves_other_fields(self, client):
        create_resp = _create_subnet(
            client, map_public_ip_on_launch=True, available_ip_count=251
        )
        subnet_id = create_resp.json()["id"]

        resp = client.put(f"{BASE_URL}/{subnet_id}", json={"name": "new-name"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "new-name"
        assert data["map_public_ip_on_launch"] is True
        assert data["available_ip_count"] == 251
        assert data["region"] == "us-east-1"


# =========================================================================
# DELETE /api/v1/subnets/{subnet_id} - Delete Subnet
# =========================================================================


class TestDeleteSubnet:
    def test_delete_subnet_success(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{subnet_id}")
        assert resp.status_code == 204

    def test_delete_subnet_then_get_returns_404(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        client.delete(f"{BASE_URL}/{subnet_id}")
        resp = client.get(f"{BASE_URL}/{subnet_id}")
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_delete_subnet_not_found(self, client):
        resp = client.delete(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"


# =========================================================================
# get_subnets() - Tag Filtering (Data Layer)
# =========================================================================


class TestGetSubnetsTagFilter:
    def test_no_filter_returns_all(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Env": "prod", "Team": "backend"},
        )
        create_subnet(
            subnet_id="subnet-002", name="s2", vpc_id="vpc-1",
            cidr_block="10.0.2.0/24", availability_zone="us-east-1b",
            state="available", region="us-east-1",
            tags={"Env": "dev"},
        )
        result = get_subnets()
        assert len(result) == 2

    def test_filter_by_tag_key_and_value(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Env": "prod", "Team": "backend"},
        )
        create_subnet(
            subnet_id="subnet-002", name="s2", vpc_id="vpc-1",
            cidr_block="10.0.2.0/24", availability_zone="us-east-1b",
            state="available", region="us-east-1",
            tags={"Env": "dev"},
        )
        result = get_subnets(tag_key="Env", tag_value="prod")
        assert len(result) == 1
        assert result[0].subnet_id == "subnet-001"

    def test_filter_by_tag_key_only(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Env": "prod", "Team": "backend"},
        )
        create_subnet(
            subnet_id="subnet-002", name="s2", vpc_id="vpc-1",
            cidr_block="10.0.2.0/24", availability_zone="us-east-1b",
            state="available", region="us-east-1",
            tags={"Env": "dev"},
        )
        create_subnet(
            subnet_id="subnet-003", name="s3", vpc_id="vpc-1",
            cidr_block="10.0.3.0/24", availability_zone="us-east-1c",
            state="available", region="us-east-1",
            tags={},
        )
        result = get_subnets(tag_key="Env")
        assert len(result) == 2
        subnet_ids = {s.subnet_id for s in result}
        assert subnet_ids == {"subnet-001", "subnet-002"}

    def test_filter_by_tag_key_only_returns_all_values(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Team": "backend"},
        )
        create_subnet(
            subnet_id="subnet-002", name="s2", vpc_id="vpc-1",
            cidr_block="10.0.2.0/24", availability_zone="us-east-1b",
            state="available", region="us-east-1",
            tags={"Team": "frontend"},
        )
        result = get_subnets(tag_key="Team")
        assert len(result) == 2

    def test_tag_value_without_tag_key_is_ignored(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Env": "prod"},
        )
        create_subnet(
            subnet_id="subnet-002", name="s2", vpc_id="vpc-1",
            cidr_block="10.0.2.0/24", availability_zone="us-east-1b",
            state="available", region="us-east-1",
            tags={"Env": "dev"},
        )
        result = get_subnets(tag_value="prod")
        assert len(result) == 2

    def test_filter_no_match_returns_empty(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Env": "prod"},
        )
        result = get_subnets(tag_key="NonExistent")
        assert result == []

    def test_filter_key_value_no_match_returns_empty(self):
        create_subnet(
            subnet_id="subnet-001", name="s1", vpc_id="vpc-1",
            cidr_block="10.0.1.0/24", availability_zone="us-east-1a",
            state="available", region="us-east-1",
            tags={"Env": "prod"},
        )
        result = get_subnets(tag_key="Env", tag_value="staging")
        assert result == []

    def test_filter_on_empty_db_returns_empty(self):
        result = get_subnets(tag_key="Env", tag_value="prod")
        assert result == []


# =========================================================================
# GET /api/v1/subnets/{subnet_id}/tags - Get Tags
# =========================================================================


class TestGetTags:
    def test_get_tags_success(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert resp.status_code == 200
        data = resp.json()
        assert data["tags"] == {"Env": "prod", "Team": "backend"}

    def test_get_tags_empty(self, client):
        create_resp = _create_subnet(client, tags={})
        subnet_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert resp.status_code == 200
        assert resp.json()["tags"] == {}

    def test_get_tags_not_found(self, client):
        resp = client.get(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags"
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"
        assert data["message"] == "Subnet not found"


# =========================================================================
# PUT /api/v1/subnets/{subnet_id}/tags - Replace Tags
# =========================================================================


class TestReplaceTags:
    def test_replace_tags_success(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Team": "frontend", "Version": "v2"}},
        )
        assert resp.status_code == 200
        assert resp.json()["tags"] == {"Team": "frontend", "Version": "v2"}

    def test_replace_tags_replaces_all(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"NewKey": "newval"}},
        )
        assert resp.status_code == 200
        assert resp.json()["tags"] == {"NewKey": "newval"}

    def test_replace_tags_not_found(self, client):
        resp = client.put(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags",
            json={"tags": {"Env": "prod"}},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"

    def test_replace_tags_empty_body_422(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {}},
        )
        assert resp.status_code == 422


# =========================================================================
# PATCH /api/v1/subnets/{subnet_id}/tags - Merge Tags
# =========================================================================


class TestMergeTags:
    def test_merge_tags_success(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Team": "frontend", "Version": "v2"}},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["tags"] == {
            "Env": "prod",
            "Team": "frontend",
            "Version": "v2",
        }

    def test_merge_tags_adds_new_keys(self, client):
        create_resp = _create_subnet(client, tags={"Env": "prod"})
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Team": "backend"}},
        )
        assert resp.status_code == 200
        assert resp.json()["tags"] == {"Env": "prod", "Team": "backend"}

    def test_merge_tags_not_found(self, client):
        resp = client.patch(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags",
            json={"tags": {"Env": "prod"}},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"

    def test_merge_tags_empty_body_422(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {}},
        )
        assert resp.status_code == 422


# =========================================================================
# DELETE /api/v1/subnets/{subnet_id}/tags/{tag_key} - Delete Tag
# =========================================================================


class TestDeleteTag:
    def test_delete_tag_success(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{subnet_id}/tags/Env")
        assert resp.status_code == 204

        get_resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert get_resp.json()["tags"] == {"Team": "backend"}

    def test_delete_tag_nonexistent_key_returns_204(self, client):
        create_resp = _create_subnet(client, tags={"Env": "prod"})
        subnet_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{subnet_id}/tags/NonExistentKey")
        assert resp.status_code == 204

    def test_delete_tag_subnet_not_found(self, client):
        resp = client.delete(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags/Env"
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"
        assert data["message"] == "Subnet not found"


# =========================================================================
# TestGetSubnetTags - Tags Sub-resource Unit Tests
# =========================================================================


class TestGetSubnetTags:
    def test_get_empty_tags(self, client):
        create_resp = _create_subnet(client, tags={})
        subnet_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert resp.status_code == 200
        assert resp.json()["tags"] == {}

    def test_get_tags_with_data(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert resp.status_code == 200
        assert resp.json()["tags"] == {"Env": "prod", "Team": "backend"}

    def test_get_tags_subnet_not_found(self, client):
        resp = client.get(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


# =========================================================================
# TestReplaceSubnetTags - PUT Tags Sub-resource Unit Tests
# =========================================================================


class TestReplaceSubnetTags:
    def test_put_replaces_tags(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Version": "v2"}},
        )
        assert resp.status_code == 200
        assert resp.json()["tags"] == {"Version": "v2"}

    def test_put_old_tags_disappear(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        client.put(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"NewKey": "newval"}},
        )

        resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert "Env" not in resp.json()["tags"]
        assert "Team" not in resp.json()["tags"]
        assert resp.json()["tags"] == {"NewKey": "newval"}

    def test_put_empty_dict_returns_422(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {}},
        )
        assert resp.status_code == 422

    def test_put_subnet_not_found(self, client):
        resp = client.put(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags",
            json={"tags": {"Env": "prod"}},
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


# =========================================================================
# TestMergeSubnetTags - PATCH Tags Sub-resource Unit Tests
# =========================================================================


class TestMergeSubnetTags:
    def test_patch_adds_new_tag(self, client):
        create_resp = _create_subnet(client, tags={"Env": "prod"})
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Team": "backend"}},
        )
        assert resp.status_code == 200
        assert resp.json()["tags"] == {"Env": "prod", "Team": "backend"}

    def test_patch_overwrites_existing_key(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Env": "staging"}},
        )
        assert resp.status_code == 200
        assert resp.json()["tags"]["Env"] == "staging"

    def test_patch_does_not_affect_unspecified_keys(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend", "Version": "v1"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {"Env": "staging"}},
        )
        assert resp.status_code == 200
        tags = resp.json()["tags"]
        assert tags["Team"] == "backend"
        assert tags["Version"] == "v1"

    def test_patch_empty_dict_returns_422(self, client):
        create_resp = _create_subnet(client)
        subnet_id = create_resp.json()["id"]

        resp = client.patch(
            f"{BASE_URL}/{subnet_id}/tags",
            json={"tags": {}},
        )
        assert resp.status_code == 422

    def test_patch_subnet_not_found(self, client):
        resp = client.patch(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags",
            json={"tags": {"Env": "prod"}},
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


# =========================================================================
# TestDeleteSubnetTag - DELETE Tags Sub-resource Unit Tests
# =========================================================================


class TestDeleteSubnetTag:
    def test_delete_existing_tag_key_returns_204(self, client):
        create_resp = _create_subnet(
            client, tags={"Env": "prod", "Team": "backend"}
        )
        subnet_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{subnet_id}/tags/Env")
        assert resp.status_code == 204

        get_resp = client.get(f"{BASE_URL}/{subnet_id}/tags")
        assert "Env" not in get_resp.json()["tags"]
        assert get_resp.json()["tags"] == {"Team": "backend"}

    def test_delete_nonexistent_tag_key_returns_204(self, client):
        create_resp = _create_subnet(client, tags={"Env": "prod"})
        subnet_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{subnet_id}/tags/NoSuchKey")
        assert resp.status_code == 204

    def test_delete_tag_subnet_not_found_returns_404(self, client):
        resp = client.delete(
            f"{BASE_URL}/00000000-0000-0000-0000-000000000000/tags/Env"
        )
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"


# =========================================================================
# TestListSubnetTagFilter - List Subnets with Tag Filter (API Level)
# =========================================================================


class TestListSubnetTagFilter:
    def test_filter_by_tag_key_and_value(self, client):
        _create_subnet(
            client,
            subnet_id="subnet-001",
            name="s1",
            tags={"Env": "prod", "Team": "backend"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-002",
            name="s2",
            tags={"Env": "dev"},
        )

        resp = client.get(
            BASE_URL, params={"tag_key": "Env", "tag_value": "prod"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["subnet_id"] == "subnet-001"

    def test_filter_by_tag_key_only(self, client):
        _create_subnet(
            client,
            subnet_id="subnet-001",
            name="s1",
            tags={"Env": "prod"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-002",
            name="s2",
            tags={"Env": "dev"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-003",
            name="s3",
            tags={},
        )

        resp = client.get(BASE_URL, params={"tag_key": "Env"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        subnet_ids = {item["subnet_id"] for item in data["items"]}
        assert subnet_ids == {"subnet-001", "subnet-002"}

    def test_no_tag_params_returns_all(self, client):
        _create_subnet(
            client,
            subnet_id="subnet-001",
            name="s1",
            tags={"Env": "prod"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-002",
            name="s2",
            tags={"Env": "dev"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-003",
            name="s3",
            tags={},
        )

        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3


# =========================================================================
# GET /api/v1/subnets/export - Export Subnets as CSV
# =========================================================================

EXPORT_URL = f"{BASE_URL}/export"

EXPECTED_COLUMNS = [
    "id", "subnet_id", "name", "vpc_id", "cidr_block", "availability_zone",
    "state", "region", "map_public_ip_on_launch", "available_ip_count",
    "tags", "created_at", "updated_at",
]


def _parse_csv(response_text: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(response_text))
    return list(reader)


class TestExportSubnetsCSV:
    def test_export_empty_returns_header_only(self, client):
        resp = client.get(EXPORT_URL)
        assert resp.status_code == 200
        rows = _parse_csv(resp.text)
        assert len(rows) == 0
        reader = csv.reader(io.StringIO(resp.text))
        header = next(reader)
        assert header == EXPECTED_COLUMNS

    def test_export_returns_csv_content_type(self, client):
        resp = client.get(EXPORT_URL)
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]

    def test_export_content_disposition(self, client):
        resp = client.get(EXPORT_URL)
        assert resp.status_code == 200
        assert resp.headers["content-disposition"] == "attachment; filename=subnets.csv"

    def test_export_all_columns_present(self, client):
        _create_subnet(client)
        resp = client.get(EXPORT_URL)
        assert resp.status_code == 200
        reader = csv.reader(io.StringIO(resp.text))
        header = next(reader)
        assert header == EXPECTED_COLUMNS

    def test_export_all_records_no_pagination(self, client):
        for i in range(25):
            _create_subnet(
                client, subnet_id=f"subnet-{i:08d}", name=f"subnet-{i}"
            )

        resp = client.get(EXPORT_URL)
        assert resp.status_code == 200
        rows = _parse_csv(resp.text)
        assert len(rows) == 25

    def test_export_filter_by_tag_key_and_value(self, client):
        _create_subnet(
            client,
            subnet_id="subnet-001",
            name="s1",
            tags={"Env": "prod", "Team": "backend"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-002",
            name="s2",
            tags={"Env": "dev"},
        )

        resp = client.get(EXPORT_URL, params={"tag_key": "Env", "tag_value": "prod"})
        assert resp.status_code == 200
        rows = _parse_csv(resp.text)
        assert len(rows) == 1
        assert rows[0]["subnet_id"] == "subnet-001"

    def test_export_filter_by_tag_key_only(self, client):
        _create_subnet(
            client,
            subnet_id="subnet-001",
            name="s1",
            tags={"Env": "prod"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-002",
            name="s2",
            tags={"Env": "dev"},
        )
        _create_subnet(
            client,
            subnet_id="subnet-003",
            name="s3",
            tags={},
        )

        resp = client.get(EXPORT_URL, params={"tag_key": "Env"})
        assert resp.status_code == 200
        rows = _parse_csv(resp.text)
        assert len(rows) == 2
        subnet_ids = {row["subnet_id"] for row in rows}
        assert subnet_ids == {"subnet-001", "subnet-002"}

    def test_export_tags_serialization(self, client):
        _create_subnet(
            client,
            subnet_id="subnet-001",
            name="s1",
            tags={"Z": "last", "A": "first"},
        )

        resp = client.get(EXPORT_URL)
        assert resp.status_code == 200
        rows = _parse_csv(resp.text)
        assert len(rows) == 1
        assert rows[0]["tags"] == "A=first;Z=last"
