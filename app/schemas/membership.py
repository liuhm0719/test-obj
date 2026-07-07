from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.project import ProjectResponse
from app.schemas.user import UserResponse


class MembershipAdd(BaseModel):
    user_id: int = Field(
        ...,
        examples=[1],
        description="用户 ID",
    )


class MembershipResponse(BaseModel):
    user_id: int = Field(
        ...,
        examples=[1],
        description="用户 ID",
    )
    project_id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="项目 ID",
    )
    added_at: datetime = Field(
        ...,
        examples=["2026-07-01T10:00:00Z"],
        description="添加时间（UTC）",
    )


class ProjectMembersResponse(BaseModel):
    project_id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="项目 ID",
    )
    members: list[UserResponse] = Field(
        ...,
        description="项目成员列表",
    )
    total: int = Field(
        ...,
        ge=0,
        examples=[3],
        description="成员总数",
    )


class UserProjectsResponse(BaseModel):
    user_id: int = Field(
        ...,
        examples=[1],
        description="用户 ID",
    )
    projects: list[ProjectResponse] = Field(
        ...,
        description="用户所属项目列表",
    )
    total: int = Field(
        ...,
        ge=0,
        examples=[2],
        description="项目总数",
    )
