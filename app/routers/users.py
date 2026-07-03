import math

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import (
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user,
    users_db,
)
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


def _check_username_unique(username: str, exclude_id: int | None = None) -> None:
    for user in users_db.values():
        if user.username == username and user.id != exclude_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "USER_EXISTS",
                    "message": "Username already exists",
                },
            )


def _check_email_unique(email: str, exclude_id: int | None = None) -> None:
    for user in users_db.values():
        if user.email == email and user.id != exclude_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "EMAIL_EXISTS",
                    "message": "Email already exists",
                },
            )


def _check_phone_unique(phone: str, exclude_id: int | None = None) -> None:
    for user in users_db.values():
        if user.phone == phone and user.id != exclude_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "PHONE_EXISTS",
                    "message": "Phone already exists",
                },
            )


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}},
)
async def create_user_endpoint(body: UserCreate):
    _check_username_unique(body.username)
    _check_email_unique(body.email)
    if body.phone is not None:
        _check_phone_unique(body.phone)
    user = create_user(username=body.username, email=body.email, phone=body.phone)
    return UserResponse.model_validate(user)


@router.get("", response_model=UserListResponse)
async def list_users(pagination: PaginationParams = Depends()):
    all_users = get_users()
    total = len(all_users)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_users[start:end]
    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_user_endpoint(user_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
    return UserResponse.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    },
)
async def update_user_endpoint(user_id: int, body: UserUpdate):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
    if body.username is not None:
        _check_username_unique(body.username, exclude_id=user_id)
    if body.email is not None:
        _check_email_unique(body.email, exclude_id=user_id)
    if body.phone is not None:
        _check_phone_unique(body.phone, exclude_id=user_id)
    updated = update_user(
        user_id,
        username=body.username,
        email=body.email,
        phone=body.phone,
        is_active=body.is_active,
    )
    return UserResponse.model_validate(updated)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_user_endpoint(user_id: int):
    user = delete_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
