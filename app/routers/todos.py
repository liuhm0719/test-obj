import math
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.todo import Todo, todos_db
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.todo import TodoCreate, TodoListResponse, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=TodoListResponse)
async def list_todos(pagination: PaginationParams = Depends()):
    all_todos = list(todos_db.values())
    total = len(all_todos)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_todos[start:end]
    return TodoListResponse(
        items=[TodoResponse.model_validate(t) for t in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(body: TodoCreate):
    todo = Todo(title=body.title)
    todos_db[str(todo.id)] = todo
    return TodoResponse.model_validate(todo)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_todo(todo_id: UUID):
    todo = todos_db.get(str(todo_id))
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Todo not found"},
        )
    return TodoResponse.model_validate(todo)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={404: {"model": ErrorResponse}},
)
async def update_todo(todo_id: UUID, body: TodoUpdate):
    todo = todos_db.get(str(todo_id))
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Todo not found"},
        )
    todo.title = body.title
    todo.done = body.done
    return TodoResponse.model_validate(todo)


@router.delete(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={404: {"model": ErrorResponse}},
)
async def delete_todo(todo_id: UUID):
    todo = todos_db.pop(str(todo_id), None)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Todo not found"},
        )
    return TodoResponse.model_validate(todo)
