from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=32,
        examples=["john_doe"],
        description="用户名，唯一",
    )
    email: EmailStr = Field(
        ...,
        examples=["john@example.com"],
        description="邮箱地址，唯一，合法邮箱格式",
    )
    phone: str | None = Field(
        None,
        pattern=r"^\+?[1-9]\d{6,14}$",
        examples=["+8613800138000"],
        description="电话号码，可选，唯一，支持国际格式",
    )


class UserUpdate(BaseModel):
    username: str | None = Field(
        None,
        min_length=3,
        max_length=32,
        examples=["john_updated"],
        description="用户名，唯一",
    )
    email: EmailStr | None = Field(
        None,
        examples=["john_new@example.com"],
        description="邮箱地址，唯一，合法邮箱格式",
    )
    phone: str | None = Field(
        None,
        pattern=r"^\+?[1-9]\d{6,14}$",
        examples=["+8613800138000"],
        description="电话号码，可选，唯一，支持国际格式",
    )
    is_active: bool | None = Field(
        None,
        examples=[False],
        description="是否激活",
    )


class UserResponse(BaseModel):
    id: int = Field(
        ...,
        examples=[1],
        description="用户 ID，自增主键",
    )
    username: str = Field(
        ...,
        examples=["john_doe"],
        description="用户名",
    )
    email: str = Field(
        ...,
        examples=["john@example.com"],
        description="邮箱地址",
    )
    phone: str | None = Field(
        None,
        examples=["+8613800138000"],
        description="电话号码",
    )
    is_active: bool = Field(
        ...,
        examples=[True],
        description="是否激活",
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


class UserListResponse(BaseModel):
    items: list[UserResponse] = Field(
        ...,
        description="当前页的用户列表",
    )
    total: int = Field(
        ...,
        ge=0,
        examples=[5],
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
