from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EC2State(str, Enum):
    running = "running"
    stopped = "stopped"
    terminated = "terminated"
    pending = "pending"


class EC2Create(BaseModel):
    instance_id: str = Field(
        ...,
        min_length=1,
        examples=["i-0abc1234def56789"],
        description="AWS 实例 ID",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["web-server-01"],
        description="实例名称（对应 Name 标签）",
    )
    instance_type: str = Field(
        ...,
        min_length=1,
        examples=["t2.micro"],
        description="实例类型",
    )
    state: EC2State = Field(
        ...,
        examples=["running"],
        description="实例状态",
    )
    region: str = Field(
        ...,
        min_length=1,
        examples=["us-east-1"],
        description="AWS 区域",
    )
    availability_zone: str | None = Field(
        None,
        examples=["us-east-1a"],
        description="可用区",
    )
    private_ip: str | None = Field(
        None,
        examples=["10.0.1.100"],
        description="私有 IP 地址",
    )
    public_ip: str | None = Field(
        None,
        examples=["54.123.45.67"],
        description="公网 IP 地址",
    )
    vpc_id: str | None = Field(
        None,
        examples=["vpc-0abc1234"],
        description="VPC ID",
    )
    key_name: str | None = Field(
        None,
        examples=["my-key-pair"],
        description="SSH 密钥对名称",
    )
    launch_time: str | None = Field(
        None,
        examples=["2026-07-01T10:00:00Z"],
        description="实例启动时间（ISO 8601 格式）",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        examples=[{"Environment": "production", "Team": "backend"}],
        description="标签键值对",
    )


class EC2Update(BaseModel):
    instance_id: str | None = Field(
        None,
        min_length=1,
        examples=["i-0abc1234def56789"],
        description="AWS 实例 ID",
    )
    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        examples=["web-server-02"],
        description="实例名称",
    )
    instance_type: str | None = Field(
        None,
        min_length=1,
        examples=["m5.large"],
        description="实例类型",
    )
    state: EC2State | None = Field(
        None,
        examples=["stopped"],
        description="实例状态",
    )
    region: str | None = Field(
        None,
        min_length=1,
        examples=["us-west-2"],
        description="AWS 区域",
    )
    availability_zone: str | None = Field(
        None,
        examples=["us-west-2a"],
        description="可用区",
    )
    private_ip: str | None = Field(
        None,
        examples=["10.0.2.200"],
        description="私有 IP 地址",
    )
    public_ip: str | None = Field(
        None,
        examples=["52.200.100.50"],
        description="公网 IP 地址",
    )
    vpc_id: str | None = Field(
        None,
        examples=["vpc-0def5678"],
        description="VPC ID",
    )
    key_name: str | None = Field(
        None,
        examples=["new-key-pair"],
        description="SSH 密钥对名称",
    )
    launch_time: str | None = Field(
        None,
        examples=["2026-07-01T12:00:00Z"],
        description="实例启动时间（ISO 8601 格式）",
    )
    tags: dict[str, str] | None = Field(
        None,
        examples=[{"Environment": "staging"}],
        description="标签键值对",
    )


class EC2Response(BaseModel):
    id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="内部唯一标识",
    )
    instance_id: str = Field(
        ...,
        examples=["i-0abc1234def56789"],
        description="AWS 实例 ID",
    )
    name: str = Field(
        ...,
        examples=["web-server-01"],
        description="实例名称",
    )
    instance_type: str = Field(
        ...,
        examples=["t2.micro"],
        description="实例类型",
    )
    state: str = Field(
        ...,
        examples=["running"],
        description="实例状态",
    )
    region: str = Field(
        ...,
        examples=["us-east-1"],
        description="AWS 区域",
    )
    availability_zone: str | None = Field(
        None,
        examples=["us-east-1a"],
        description="可用区",
    )
    private_ip: str | None = Field(
        None,
        examples=["10.0.1.100"],
        description="私有 IP 地址",
    )
    public_ip: str | None = Field(
        None,
        examples=["54.123.45.67"],
        description="公网 IP 地址",
    )
    vpc_id: str | None = Field(
        None,
        examples=["vpc-0abc1234"],
        description="VPC ID",
    )
    key_name: str | None = Field(
        None,
        examples=["my-key-pair"],
        description="SSH 密钥对名称",
    )
    launch_time: str | None = Field(
        None,
        examples=["2026-07-01T10:00:00Z"],
        description="实例启动时间",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        examples=[{"Environment": "production"}],
        description="标签键值对",
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


class EC2ListResponse(BaseModel):
    items: list[EC2Response] = Field(
        ...,
        description="当前页的 EC2 实例列表",
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
