import math
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.membership import (
    add_member,
    get_project_members,
    remove_all_project_members,
    remove_member,
)
from app.models.project import Project, projects_db
from app.models.user import get_user
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.membership import (
    MembershipAdd,
    MembershipResponse,
    ProjectMembersResponse,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ProjectListResponse)
async def list_projects(pagination: PaginationParams = Depends()):
    all_projects = list(projects_db.values())
    total = len(all_projects)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_projects[start:end]
    return ProjectListResponse(
        items=[ProjectResponse.model_validate(p) for p in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(body: ProjectCreate):
    project = Project(
        name=body.name,
        description=body.description,
        status=body.status.value,
    )
    projects_db[project.id] = project
    return ProjectResponse.model_validate(project)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_project(project_id: UUID):
    project = projects_db.get(str(project_id))
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Project not found"},
        )
    return ProjectResponse.model_validate(project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={404: {"model": ErrorResponse}},
)
async def update_project(project_id: UUID, body: ProjectUpdate):
    project = projects_db.get(str(project_id))
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Project not found"},
        )
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value is not None:
            setattr(project, field, value.value)
        else:
            setattr(project, field, value)
    project.updated_at = datetime.now(timezone.utc)
    return ProjectResponse.model_validate(project)


@router.delete(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={404: {"model": ErrorResponse}},
)
async def delete_project(project_id: UUID):
    project = projects_db.pop(str(project_id), None)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Project not found"},
        )
    remove_all_project_members(str(project_id))
    return ProjectResponse.model_validate(project)


@router.post(
    "/{project_id}/members",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
async def add_project_member(project_id: UUID, body: MembershipAdd):
    pid = str(project_id)
    if pid not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Project not found"},
        )
    user = get_user(body.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "User not found"},
        )
    success = add_member(pid, body.user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "ALREADY_EXISTS",
                "message": "User is already a member of this project",
            },
        )
    return MembershipResponse(
        user_id=body.user_id,
        project_id=pid,
        added_at=datetime.now(timezone.utc),
    )


@router.delete(
    "/{project_id}/members/{user_id}",
    response_model=MembershipResponse,
    responses={404: {"model": ErrorResponse}},
)
async def remove_project_member(project_id: UUID, user_id: int):
    pid = str(project_id)
    if pid not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Project not found"},
        )
    success = remove_member(pid, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "User is not a member of this project",
            },
        )
    return MembershipResponse(
        user_id=user_id,
        project_id=pid,
        added_at=datetime.now(timezone.utc),
    )


@router.get(
    "/{project_id}/members",
    response_model=ProjectMembersResponse,
    responses={404: {"model": ErrorResponse}},
)
async def list_project_members(project_id: UUID):
    pid = str(project_id)
    if pid not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Project not found"},
        )
    member_ids = get_project_members(pid)
    members = []
    for uid in member_ids:
        user = get_user(uid)
        if user is not None:
            members.append(UserResponse.model_validate(user))
    return ProjectMembersResponse(
        project_id=pid,
        members=members,
        total=len(members),
    )
