from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    active = "active"
    archived = "archived"


class ProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["My Project"],
        description="项目名称",
    )
    description: str | None = Field(
        None,
        max_length=1000,
        examples=["A sample project description"],
        description="项目描述",
    )
    status: ProjectStatus = Field(
        default=ProjectStatus.active,
        examples=["active"],
        description="项目状态（active/archived）",
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=200,
        examples=["Updated Project Name"],
        description="项目名称",
    )
    description: str | None = Field(
        None,
        max_length=1000,
        examples=["Updated description"],
        description="项目描述",
    )
    status: ProjectStatus | None = Field(
        None,
        examples=["archived"],
        description="项目状态（active/archived）",
    )


class ProjectResponse(BaseModel):
    id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="唯一标识符（UUID4）",
    )
    name: str = Field(
        ...,
        examples=["My Project"],
        description="项目名称",
    )
    description: str | None = Field(
        None,
        examples=["A sample project description"],
        description="项目描述",
    )
    status: str = Field(
        ...,
        examples=["active"],
        description="项目状态",
    )
    created_at: datetime = Field(
        ...,
        examples=["2026-07-01T10:00:00Z"],
        description="创建时间（UTC）",
    )
    updated_at: datetime = Field(
        ...,
        examples=["2026-07-01T10:00:00Z"],
        description="更新时间（UTC）",
    )

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse] = Field(
        ...,
        description="当前页的 Project 列表",
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
