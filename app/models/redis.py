from datetime import datetime, timezone

from pydantic import BaseModel, Field


class RedisInstance(BaseModel):
    id: int = 0
    cluster_id: str
    node_type: str
    engine_version: str
    status: str = "creating"
    endpoint: str | None = None
    port: int = 6379
    num_shards: int = 1
    replicas_per_shard: int = 0
    region: str = "us-east-1"
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


redis_db: list[RedisInstance] = []

_next_id: int = 1


def _get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


def create_redis(
    cluster_id: str,
    node_type: str,
    engine_version: str,
    status: str = "creating",
    endpoint: str | None = None,
    port: int = 6379,
    num_shards: int = 1,
    replicas_per_shard: int = 0,
    region: str = "us-east-1",
) -> RedisInstance:
    for inst in redis_db:
        if inst.cluster_id == cluster_id:
            raise ValueError(f"cluster_id '{cluster_id}' already exists")
    instance = RedisInstance(
        id=_get_next_id(),
        cluster_id=cluster_id,
        node_type=node_type,
        engine_version=engine_version,
        status=status,
        endpoint=endpoint,
        port=port,
        num_shards=num_shards,
        replicas_per_shard=replicas_per_shard,
        region=region,
    )
    redis_db.append(instance)
    return instance


def get_redis(redis_id: int) -> RedisInstance | None:
    for inst in redis_db:
        if inst.id == redis_id:
            return inst
    return None


def get_redis_instances() -> list[RedisInstance]:
    return list(redis_db)


_UNSET = object()


def update_redis(
    redis_id: int,
    cluster_id: str | None = None,
    node_type: str | None = None,
    engine_version: str | None = None,
    status: str | None = None,
    endpoint: object = _UNSET,
    port: int | None = None,
    num_shards: int | None = None,
    replicas_per_shard: int | None = None,
    region: str | None = None,
) -> RedisInstance | None:
    instance = get_redis(redis_id)
    if instance is None:
        return None
    if cluster_id is not None:
        for inst in redis_db:
            if inst.id != redis_id and inst.cluster_id == cluster_id:
                raise ValueError(f"cluster_id '{cluster_id}' already exists")
        instance.cluster_id = cluster_id
    if node_type is not None:
        instance.node_type = node_type
    if engine_version is not None:
        instance.engine_version = engine_version
    if status is not None:
        instance.status = status
    if endpoint is not _UNSET:
        instance.endpoint = endpoint  # type: ignore[assignment]
    if port is not None:
        instance.port = port
    if num_shards is not None:
        instance.num_shards = num_shards
    if replicas_per_shard is not None:
        instance.replicas_per_shard = replicas_per_shard
    if region is not None:
        instance.region = region
    instance.updated_at = datetime.now(timezone.utc).isoformat()
    return instance


def delete_redis(redis_id: int) -> RedisInstance | None:
    for i, inst in enumerate(redis_db):
        if inst.id == redis_id:
            return redis_db.pop(i)
    return None
