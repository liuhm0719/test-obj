from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RedisStatus(str, Enum):
    creating = "creating"
    available = "available"
    deleting = "deleting"
    stopped = "stopped"


class RedisCreate(BaseModel):
    cluster_id: str = Field(
        ...,
        min_length=1,
        examples=["my-redis-cluster-01"],
        description="Redis 集群标识符，唯一",
    )
    node_type: str = Field(
        ...,
        min_length=1,
        examples=["cache.t3.micro"],
        description="节点实例规格",
    )
    engine_version: str = Field(
        ...,
        min_length=1,
        examples=["7.0"],
        description="Redis 引擎版本号",
    )
    status: RedisStatus = Field(
        default=RedisStatus.creating,
        examples=["creating"],
        description="实例状态",
    )
    endpoint: str | None = Field(
        None,
        examples=["my-redis-cluster-01.abc123.0001.use1.cache.amazonaws.com"],
        description="连接端点地址",
    )
    port: int = Field(
        default=6379,
        gt=0,
        le=65535,
        examples=[6379],
        description="连接端口",
    )
    num_shards: int = Field(
        default=1,
        ge=1,
        examples=[1],
        description="分片数量",
    )
    replicas_per_shard: int = Field(
        default=0,
        ge=0,
        examples=[1],
        description="每分片副本数",
    )
    region: str = Field(
        default="us-east-1",
        min_length=1,
        examples=["us-east-1"],
        description="所在区域",
    )


class RedisUpdate(BaseModel):
    cluster_id: str | None = Field(
        None,
        min_length=1,
        examples=["my-redis-cluster-02"],
        description="Redis 集群标识符",
    )
    node_type: str | None = Field(
        None,
        min_length=1,
        examples=["cache.m5.large"],
        description="节点实例规格",
    )
    engine_version: str | None = Field(
        None,
        min_length=1,
        examples=["7.2"],
        description="Redis 引擎版本号",
    )
    status: RedisStatus | None = Field(
        None,
        examples=["available"],
        description="实例状态",
    )
    endpoint: str | None = Field(
        None,
        examples=["my-redis-cluster-02.abc123.0001.use1.cache.amazonaws.com"],
        description="连接端点地址",
    )
    port: int | None = Field(
        None,
        gt=0,
        le=65535,
        examples=[6379],
        description="连接端口",
    )
    num_shards: int | None = Field(
        None,
        ge=1,
        examples=[2],
        description="分片数量",
    )
    replicas_per_shard: int | None = Field(
        None,
        ge=0,
        examples=[2],
        description="每分片副本数",
    )
    region: str | None = Field(
        None,
        min_length=1,
        examples=["us-west-2"],
        description="所在区域",
    )


class RedisResponse(BaseModel):
    id: int = Field(
        ...,
        examples=[1],
        description="内部唯一标识（自增主键）",
    )
    cluster_id: str = Field(
        ...,
        examples=["my-redis-cluster-01"],
        description="Redis 集群标识符",
    )
    node_type: str = Field(
        ...,
        examples=["cache.t3.micro"],
        description="节点实例规格",
    )
    engine_version: str = Field(
        ...,
        examples=["7.0"],
        description="Redis 引擎版本号",
    )
    status: str = Field(
        ...,
        examples=["available"],
        description="实例状态",
    )
    endpoint: str | None = Field(
        None,
        examples=["my-redis-cluster-01.abc123.0001.use1.cache.amazonaws.com"],
        description="连接端点地址",
    )
    port: int = Field(
        ...,
        examples=[6379],
        description="连接端口",
    )
    num_shards: int = Field(
        ...,
        examples=[1],
        description="分片数量",
    )
    replicas_per_shard: int = Field(
        ...,
        examples=[1],
        description="每分片副本数",
    )
    region: str = Field(
        ...,
        examples=["us-east-1"],
        description="所在区域",
    )
    created_at: datetime = Field(
        ...,
        examples=["2026-07-01T10:00:00Z"],
        description="记录创建时间（UTC）",
    )
    updated_at: datetime = Field(
        ...,
        examples=["2026-07-01T10:00:00Z"],
        description="记录更新时间（UTC）",
    )

    model_config = {"from_attributes": True}


class RedisListResponse(BaseModel):
    items: list[RedisResponse] = Field(
        ...,
        description="当前页的 Redis 实例列表",
    )
    total: int = Field(
        ...,
        ge=0,
        examples=[10],
        description="总记录数",
    )
    page: int = Field(
        ...,
        ge=1,
        examples=[1],
        description="当前页码",
    )
    size: int = Field(
        ...,
        ge=1,
        examples=[20],
        description="每页条数",
    )
    pages: int = Field(
        ...,
        ge=0,
        examples=[1],
        description="总页数",
    )
