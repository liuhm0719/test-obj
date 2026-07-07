from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str | None = None
    status: str = "active"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


projects_db: dict[str, Project] = {}
