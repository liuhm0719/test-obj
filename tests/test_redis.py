import pytest

from app.models import redis as redis_module

BASE_URL = "/api/v1/redis"


@pytest.fixture(autouse=True)
def clear_db():
    redis_module.redis_db.clear()
    redis_module._next_id = 1
    yield
    redis_module.redis_db.clear()
    redis_module._next_id = 1


def _create_redis(client, **overrides):
    payload = {
        "cluster_id": "test-redis-01",
        "node_type": "cache.t3.micro",
        "engine_version": "7.0",
    }
    payload.update(overrides)
    return client.post(BASE_URL, json=payload)


# =========================================================================
# POST /api/v1/redis - Create Redis Instance
# =========================================================================


class TestCreateRedis:
    def test_create_redis_success(self, client):
        resp = _create_redis(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["cluster_id"] == "test-redis-01"
        assert data["node_type"] == "cache.t3.micro"
        assert data["engine_version"] == "7.0"
        assert data["status"] == "creating"
        assert data["port"] == 6379
        assert data["num_shards"] == 1
        assert data["replicas_per_shard"] == 0
        assert data["region"] == "us-east-1"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_redis_missing_required_field(self, client):
        resp = client.post(
            BASE_URL,
            json={"cluster_id": "test-redis"},
        )
        assert resp.status_code == 422

    def test_create_redis_duplicate_cluster_id(self, client):
        _create_redis(client)
        resp = _create_redis(client)
        assert resp.status_code == 400
        data = resp.json()
        assert data["code"] == "DUPLICATE_IDENTIFIER"

    def test_create_redis_with_all_fields(self, client):
        resp = _create_redis(
            client,
            cluster_id="full-redis",
            node_type="cache.m5.large",
            engine_version="7.2",
            status="available",
            endpoint="full-redis.abc123.0001.use1.cache.amazonaws.com",
            port=6380,
            num_shards=3,
            replicas_per_shard=2,
            region="us-west-2",
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["cluster_id"] == "full-redis"
        assert data["node_type"] == "cache.m5.large"
        assert data["engine_version"] == "7.2"
        assert data["status"] == "available"
        assert data["endpoint"] == "full-redis.abc123.0001.use1.cache.amazonaws.com"
        assert data["port"] == 6380
        assert data["num_shards"] == 3
        assert data["replicas_per_shard"] == 2
        assert data["region"] == "us-west-2"


# =========================================================================
# GET /api/v1/redis - List Redis Instances
# =========================================================================


class TestListRedis:
    def test_list_redis_empty(self, client):
        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_redis_pagination(self, client):
        for i in range(5):
            _create_redis(client, cluster_id=f"test-redis-{i}")

        resp = client.get(BASE_URL, params={"page": 1, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["pages"] == 3

    def test_list_redis_second_page(self, client):
        for i in range(5):
            _create_redis(client, cluster_id=f"test-redis-{i}")

        resp = client.get(BASE_URL, params={"page": 2, "size": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["page"] == 2

    def test_list_redis_total_correct(self, client):
        for i in range(3):
            _create_redis(client, cluster_id=f"test-redis-{i}")

        resp = client.get(BASE_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

    def test_list_redis_invalid_page_zero(self, client):
        resp = client.get(BASE_URL, params={"page": 0})
        assert resp.status_code == 422

    def test_list_redis_invalid_size_zero(self, client):
        resp = client.get(BASE_URL, params={"size": 0})
        assert resp.status_code == 422

    def test_list_redis_invalid_size_exceeds_max(self, client):
        resp = client.get(BASE_URL, params={"size": 101})
        assert resp.status_code == 422


# =========================================================================
# GET /api/v1/redis/{redis_id} - Get Single Redis Instance
# =========================================================================


class TestGetRedis:
    def test_get_redis_success(self, client):
        create_resp = _create_redis(client)
        redis_id = create_resp.json()["id"]

        resp = client.get(f"{BASE_URL}/{redis_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == redis_id
        assert data["cluster_id"] == "test-redis-01"
        assert data["node_type"] == "cache.t3.micro"

    def test_get_redis_not_found(self, client):
        resp = client.get(f"{BASE_URL}/99999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"


# =========================================================================
# PUT /api/v1/redis/{redis_id} - Update Redis Instance
# =========================================================================


class TestUpdateRedis:
    def test_update_redis_success(self, client):
        create_resp = _create_redis(client)
        redis_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{redis_id}",
            json={"node_type": "cache.m5.large", "num_shards": 3},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["node_type"] == "cache.m5.large"
        assert data["num_shards"] == 3
        assert data["cluster_id"] == "test-redis-01"

    def test_update_redis_not_found(self, client):
        resp = client.put(
            f"{BASE_URL}/99999",
            json={"node_type": "cache.m5.large"},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"

    def test_update_redis_preserves_other_fields(self, client):
        create_resp = _create_redis(
            client, endpoint="test-redis-01.abc.0001.use1.cache.amazonaws.com"
        )
        redis_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{redis_id}", json={"num_shards": 2}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["num_shards"] == 2
        assert (
            data["endpoint"]
            == "test-redis-01.abc.0001.use1.cache.amazonaws.com"
        )
        assert data["node_type"] == "cache.t3.micro"
        assert data["engine_version"] == "7.0"

    def test_update_redis_duplicate_cluster_id(self, client):
        _create_redis(client, cluster_id="redis-a")
        create_resp = _create_redis(client, cluster_id="redis-b")
        redis_id = create_resp.json()["id"]

        resp = client.put(
            f"{BASE_URL}/{redis_id}", json={"cluster_id": "redis-a"}
        )
        assert resp.status_code == 400
        assert resp.json()["code"] == "DUPLICATE_IDENTIFIER"


# =========================================================================
# DELETE /api/v1/redis/{redis_id} - Delete Redis Instance
# =========================================================================


class TestDeleteRedis:
    def test_delete_redis_success(self, client):
        create_resp = _create_redis(client)
        redis_id = create_resp.json()["id"]

        resp = client.delete(f"{BASE_URL}/{redis_id}")
        assert resp.status_code == 204

    def test_delete_redis_then_get_returns_404(self, client):
        create_resp = _create_redis(client)
        redis_id = create_resp.json()["id"]

        client.delete(f"{BASE_URL}/{redis_id}")
        resp = client.get(f"{BASE_URL}/{redis_id}")
        assert resp.status_code == 404
        assert resp.json()["code"] == "NOT_FOUND"

    def test_delete_redis_not_found(self, client):
        resp = client.delete(f"{BASE_URL}/99999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "NOT_FOUND"
