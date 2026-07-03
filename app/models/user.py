from datetime import datetime, timezone

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str
    email: str
    phone: str | None = None
    is_active: bool = True
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


users_db: dict[int, User] = {}
_user_id_counter: int = 0


def _next_id() -> int:
    global _user_id_counter
    _user_id_counter += 1
    return _user_id_counter


def create_user(username: str, email: str, phone: str | None = None) -> User:
    user = User(id=_next_id(), username=username, email=email, phone=phone)
    users_db[user.id] = user
    return user


def get_user(user_id: int) -> User | None:
    return users_db.get(user_id)


def get_users() -> list[User]:
    return list(users_db.values())


_UNSET = object()


def update_user(
    user_id: int,
    username: str | None = None,
    email: str | None = None,
    phone: object = _UNSET,
    is_active: bool | None = None,
) -> User | None:
    user = users_db.get(user_id)
    if user is None:
        return None
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if phone is not _UNSET:
        user.phone = phone
    if is_active is not None:
        user.is_active = is_active
    user.updated_at = datetime.now(timezone.utc)
    return user


def delete_user(user_id: int) -> User | None:
    return users_db.pop(user_id, None)
