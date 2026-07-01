from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field
from uuid import UUID


class Todo(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    done: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


todos_db: dict[str, Todo] = {}
