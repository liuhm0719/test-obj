from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RDSEngine(str, Enum):
    mysql = "mysql"
    postgres = "postgres"
    mariadb = "mariadb"
    oracle = "oracle"
    sqlserver = "sqlserver"


class RDSStatus(str, Enum):
    creating = "creating"
    available = "available"
    deleting = "deleting"
    stopped = "stopped"


class RDSCreate(BaseModel):
    db_instance_identifier: str = Field(
        ...,
        min_length=1,
        examples=["my-database-01"],
        description="RDS 实例标识符，唯一",
    )
    engine: RDSEngine = Field(
        ...,
        examples=["mysql"],
        description="数据库引擎（mysql/postgres/mariadb/oracle/sqlserver）",
    )
    engine_version: str = Field(
        ...,
        min_length=1,
        examples=["8.0.35"],
        description="引擎版本号",
    )
    db_instance_class: str = Field(
        ...,
        min_length=1,
        examples=["db.t3.micro"],
        description="实例规格",
    )
    allocated_storage: int = Field(
        ...,
        gt=0,
        examples=[20],
        description="分配存储空间（GB）",
    )
    master_username: str = Field(
        ...,
        min_length=1,
        examples=["admin"],
        description="主用户名",
    )
    status: RDSStatus = Field(
        default=RDSStatus.creating,
        examples=["creating"],
        description="实例状态",
    )
    endpoint: str | None = Field(
        None,
        examples=["my-database-01.abc123.us-east-1.rds.amazonaws.com"],
        description="连接端点地址",
    )
    port: int = Field(
        default=3306,
        gt=0,
        le=65535,
        examples=[3306],
        description="连接端口",
    )
    multi_az: bool = Field(
        default=False,
        examples=[False],
        description="是否多可用区部署",
    )
    region: str = Field(
        default="us-east-1",
        min_length=1,
        examples=["us-east-1"],
        description="所在区域",
    )


class RDSUpdate(BaseModel):
    db_instance_identifier: str | None = Field(
        None,
        min_length=1,
        examples=["my-database-02"],
        description="RDS 实例标识符",
    )
    engine: RDSEngine | None = Field(
        None,
        examples=["postgres"],
        description="数据库引擎",
    )
    engine_version: str | None = Field(
        None,
        min_length=1,
        examples=["15.4"],
        description="引擎版本号",
    )
    db_instance_class: str | None = Field(
        None,
        min_length=1,
        examples=["db.m5.large"],
        description="实例规格",
    )
    allocated_storage: int | None = Field(
        None,
        gt=0,
        examples=[100],
        description="分配存储空间（GB）",
    )
    status: RDSStatus | None = Field(
        None,
        examples=["available"],
        description="实例状态",
    )
    endpoint: str | None = Field(
        None,
        examples=["my-database-02.abc123.us-east-1.rds.amazonaws.com"],
        description="连接端点地址",
    )
    port: int | None = Field(
        None,
        gt=0,
        le=65535,
        examples=[5432],
        description="连接端口",
    )
    master_username: str | None = Field(
        None,
        min_length=1,
        examples=["dbadmin"],
        description="主用户名",
    )
    multi_az: bool | None = Field(
        None,
        examples=[True],
        description="是否多可用区部署",
    )
    region: str | None = Field(
        None,
        min_length=1,
        examples=["us-west-2"],
        description="所在区域",
    )


class RDSResponse(BaseModel):
    id: int = Field(
        ...,
        examples=[1],
        description="内部唯一标识（自增主键）",
    )
    db_instance_identifier: str = Field(
        ...,
        examples=["my-database-01"],
        description="RDS 实例标识符",
    )
    engine: str = Field(
        ...,
        examples=["mysql"],
        description="数据库引擎",
    )
    engine_version: str = Field(
        ...,
        examples=["8.0.35"],
        description="引擎版本号",
    )
    db_instance_class: str = Field(
        ...,
        examples=["db.t3.micro"],
        description="实例规格",
    )
    allocated_storage: int = Field(
        ...,
        examples=[20],
        description="分配存储空间（GB）",
    )
    status: str = Field(
        ...,
        examples=["available"],
        description="实例状态",
    )
    endpoint: str | None = Field(
        None,
        examples=["my-database-01.abc123.us-east-1.rds.amazonaws.com"],
        description="连接端点地址",
    )
    port: int = Field(
        ...,
        examples=[3306],
        description="连接端口",
    )
    master_username: str = Field(
        ...,
        examples=["admin"],
        description="主用户名",
    )
    multi_az: bool = Field(
        ...,
        examples=[False],
        description="是否多可用区部署",
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


class RDSListResponse(BaseModel):
    items: list[RDSResponse] = Field(
        ...,
        description="当前页的 RDS 实例列表",
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
