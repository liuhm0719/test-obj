from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Buy groceries"],
        description="Todo 标题",
    )


class TodoUpdate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Buy groceries and cook"],
        description="Todo 标题",
    )
    done: bool = Field(
        ...,
        examples=[True],
        description="完成状态",
    )


class TodoResponse(BaseModel):
    id: UUID = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="唯一标识符",
    )
    title: str = Field(
        ...,
        examples=["Buy groceries"],
        description="Todo 标题",
    )
    done: bool = Field(
        ...,
        examples=[False],
        description="完成状态",
    )
    created_at: datetime = Field(
        ...,
        examples=["2026-07-01T10:00:00Z"],
        description="创建时间（UTC）",
    )

    model_config = {"from_attributes": True}


class TodoListResponse(BaseModel):
    items: list[TodoResponse] = Field(
        ...,
        description="当前页的 Todo 列表",
    )
    total: int = Field(
        ...,
        ge=0,
        examples=[42],
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
        examples=[3],
        description="总页数",
    )
