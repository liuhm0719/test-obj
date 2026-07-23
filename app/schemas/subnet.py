from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class SubnetState(str, Enum):
    available = "available"
    pending = "pending"


class SubnetCreate(BaseModel):
    subnet_id: str = Field(
        ...,
        min_length=1,
        examples=["subnet-0abc1234"],
        description="AWS Subnet ID",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["private-subnet-01"],
        description="子网名称",
    )
    vpc_id: str = Field(
        ...,
        min_length=1,
        examples=["vpc-0abc1234"],
        description="VPC ID",
    )
    cidr_block: str = Field(
        ...,
        min_length=1,
        examples=["10.0.1.0/24"],
        description="CIDR 地址块",
    )
    availability_zone: str = Field(
        ...,
        min_length=1,
        examples=["us-east-1a"],
        description="可用区",
    )
    state: SubnetState = Field(
        ...,
        examples=["available"],
        description="子网状态",
    )
    region: str = Field(
        ...,
        min_length=1,
        examples=["us-east-1"],
        description="AWS 区域",
    )
    map_public_ip_on_launch: bool | None = Field(
        None,
        examples=[False],
        description="是否自动分配公网 IP",
    )
    available_ip_count: int | None = Field(
        None,
        ge=0,
        examples=[251],
        description="可用 IP 数量",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        examples=[{"Environment": "production", "Team": "backend"}],
        description="标签键值对",
    )


class SubnetUpdate(BaseModel):
    subnet_id: str | None = Field(
        None,
        min_length=1,
        examples=["subnet-0abc1234"],
        description="AWS Subnet ID",
    )
    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        examples=["private-subnet-02"],
        description="子网名称",
    )
    vpc_id: str | None = Field(
        None,
        min_length=1,
        examples=["vpc-0def5678"],
        description="VPC ID",
    )
    cidr_block: str | None = Field(
        None,
        min_length=1,
        examples=["10.0.2.0/24"],
        description="CIDR 地址块",
    )
    availability_zone: str | None = Field(
        None,
        min_length=1,
        examples=["us-west-2a"],
        description="可用区",
    )
    state: SubnetState | None = Field(
        None,
        examples=["pending"],
        description="子网状态",
    )
    region: str | None = Field(
        None,
        min_length=1,
        examples=["us-west-2"],
        description="AWS 区域",
    )
    map_public_ip_on_launch: bool | None = Field(
        None,
        examples=[True],
        description="是否自动分配公网 IP",
    )
    available_ip_count: int | None = Field(
        None,
        ge=0,
        examples=[120],
        description="可用 IP 数量",
    )
    tags: dict[str, str] | None = Field(
        None,
        examples=[{"Environment": "staging"}],
        description="标签键值对",
    )


class SubnetResponse(BaseModel):
    id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="内部唯一标识",
    )
    subnet_id: str = Field(
        ...,
        examples=["subnet-0abc1234"],
        description="AWS Subnet ID",
    )
    name: str = Field(
        ...,
        examples=["private-subnet-01"],
        description="子网名称",
    )
    vpc_id: str = Field(
        ...,
        examples=["vpc-0abc1234"],
        description="VPC ID",
    )
    cidr_block: str = Field(
        ...,
        examples=["10.0.1.0/24"],
        description="CIDR 地址块",
    )
    availability_zone: str = Field(
        ...,
        examples=["us-east-1a"],
        description="可用区",
    )
    state: str = Field(
        ...,
        examples=["available"],
        description="子网状态",
    )
    region: str = Field(
        ...,
        examples=["us-east-1"],
        description="AWS 区域",
    )
    map_public_ip_on_launch: bool | None = Field(
        None,
        examples=[False],
        description="是否自动分配公网 IP",
    )
    available_ip_count: int | None = Field(
        None,
        ge=0,
        examples=[251],
        description="可用 IP 数量",
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


class SubnetListResponse(BaseModel):
    items: list[SubnetResponse] = Field(
        ...,
        description="当前页的 Subnet 列表",
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


class TagsResponse(BaseModel):
    tags: dict[str, str] = Field(
        ...,
        examples=[{"Environment": "production", "Team": "backend"}],
        description="标签键值对",
    )


class TagsPutRequest(BaseModel):
    tags: dict[str, str] = Field(
        ...,
        examples=[{"Environment": "production", "Team": "backend"}],
        description="全量替换的标签键值对，不可为空",
    )

    @field_validator("tags")
    @classmethod
    def tags_must_not_be_empty(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) == 0:
            raise ValueError("tags must contain at least one key-value pair")
        return v


class TagsPatchRequest(BaseModel):
    tags: dict[str, str] = Field(
        ...,
        examples=[{"Environment": "staging"}],
        description="合并更新的标签键值对，至少包含一个 key",
    )

    @field_validator("tags")
    @classmethod
    def tags_must_not_be_empty(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) == 0:
            raise ValueError("tags must contain at least one key-value pair")
        return v
