from fastapi import Query
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(
        ...,
        examples=["NOT_FOUND"],
        description="错误码",
    )
    message: str = Field(
        ...,
        examples=["Todo not found"],
        description="人类可读的错误描述",
    )


class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="页码"),
        size: int = Query(default=20, ge=1, le=100, description="每页条数"),
    ):
        self.page = page
        self.size = size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size
