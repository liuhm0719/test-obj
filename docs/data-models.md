# Pydantic 数据模型设计

## 概述

本文档定义 Todo 资源相关的 Pydantic v2 数据模型，供开发任务（OAP-4407）直接实现。

所有模型使用 Pydantic v2 语法，配合 `model_config` 而非已废弃的 `Config` 内部类。

---

## 模型一览

| 模型 | 用途 | 所在文件 |
|------|------|----------|
| `TodoCreate` | 创建请求体 | `app/schemas/todo.py` |
| `TodoUpdate` | 更新请求体 | `app/schemas/todo.py` |
| `TodoResponse` | 单个 Todo 响应 | `app/schemas/todo.py` |
| `TodoListResponse` | Todo 列表分页响应 | `app/schemas/todo.py` |
| `ErrorResponse` | 统一错误响应 | `app/schemas/common.py` |
| `PaginationParams` | 分页查询参数 | `app/schemas/common.py` |

---

## 详细模型定义

### TodoCreate

创建 Todo 的请求体。

```python
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Buy groceries"],
        description="Todo 标题",
    )
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| title | str | 是 | 1-200 字符 | — | `"Buy groceries"` |

---

### TodoUpdate

更新 Todo 的请求体（全量更新）。

```python
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
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| title | str | 是 | 1-200 字符 | — | `"Buy groceries and cook"` |
| done | bool | 是 | — | — | `true` |

---

### TodoResponse

单个 Todo 的响应体。

```python
from datetime import datetime
from uuid import UUID


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
```

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | UUID | 唯一标识符 | `"550e8400-e29b-41d4-a716-446655440000"` |
| title | str | Todo 标题 | `"Buy groceries"` |
| done | bool | 完成状态 | `false` |
| created_at | datetime | 创建时间（UTC，ISO 8601） | `"2026-07-01T10:00:00Z"` |

---

### TodoListResponse

Todo 列表分页响应。

```python
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
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| items | list[TodoResponse] | — | 当前页的 Todo 列表 |
| total | int | >= 0 | 总记录数 |
| page | int | >= 1 | 当前页码 |
| size | int | >= 1 | 每页条数 |
| pages | int | >= 0 | 总页数 |

---

### ErrorResponse

统一错误响应。

```python
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
```

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| code | str | 机器可读的错误码 | `"NOT_FOUND"` |
| message | str | 人类可读的错误描述 | `"Todo not found"` |

---

### PaginationParams

分页查询参数（用于依赖注入）。

```python
from pydantic import Field
from fastapi import Query


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
```

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|------|------|--------|------|------|
| page | int | 1 | >= 1 | 页码 |
| size | int | 20 | 1-100 | 每页条数 |

---

## 文件组织

```
app/schemas/
├── __init__.py       # 导出所有 Schema
├── common.py         # ErrorResponse, PaginationParams
└── todo.py           # TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
```

### `app/schemas/__init__.py`

```python
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse

__all__ = [
    "ErrorResponse",
    "PaginationParams",
    "TodoCreate",
    "TodoUpdate",
    "TodoResponse",
    "TodoListResponse",
]
```
