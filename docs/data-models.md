# Pydantic 数据模型设计

## 概述

本文档定义项目中各资源的 Pydantic v2 数据模型，供开发任务直接实现。

所有模型使用 Pydantic v2 语法，配合 `model_config` 而非已废弃的 `Config` 内部类。

---

## 模型一览

| 模型 | 用途 | 所在文件 |
|------|------|----------|
| `TodoCreate` | 创建请求体 | `app/schemas/todo.py` |
| `TodoUpdate` | 更新请求体 | `app/schemas/todo.py` |
| `TodoResponse` | 单个 Todo 响应 | `app/schemas/todo.py` |
| `TodoListResponse` | Todo 列表分页响应 | `app/schemas/todo.py` |
| `UserCreate` | 创建用户请求体 | `app/schemas/user.py` |
| `UserUpdate` | 更新用户请求体（部分更新） | `app/schemas/user.py` |
| `UserResponse` | 单个用户响应 | `app/schemas/user.py` |
| `UserListResponse` | 用户列表分页响应 | `app/schemas/user.py` |
| `EC2State` | EC2 实例状态枚举 | `app/schemas/ec2.py` |
| `EC2Create` | 创建 EC2 实例请求体 | `app/schemas/ec2.py` |
| `EC2Update` | 更新 EC2 实例请求体（部分更新） | `app/schemas/ec2.py` |
| `EC2Response` | 单个 EC2 实例响应 | `app/schemas/ec2.py` |
| `EC2ListResponse` | EC2 实例列表分页响应 | `app/schemas/ec2.py` |
| `RDSEngine` | RDS 数据库引擎枚举 | `app/schemas/rds.py` |
| `RDSStatus` | RDS 实例状态枚举 | `app/schemas/rds.py` |
| `RDSCreate` | 创建 RDS 实例请求体 | `app/schemas/rds.py` |
| `RDSUpdate` | 更新 RDS 实例请求体（部分更新） | `app/schemas/rds.py` |
| `RDSResponse` | 单个 RDS 实例响应 | `app/schemas/rds.py` |
| `RDSListResponse` | RDS 实例列表分页响应 | `app/schemas/rds.py` |
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

---

## User 模型定义

### UserCreate

创建用户的请求体。

```python
from pydantic import BaseModel, Field, EmailStr


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
        description="电话号码，可选，唯一",
    )
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| username | str | 是 | 3-32 字符，唯一 | — | `"john_doe"` |
| email | EmailStr | 是 | 合法邮箱格式，唯一 | — | `"john@example.com"` |
| phone | str \| None | 否 | 格式匹配 `+?[1-9]\d{6,14}`，唯一 | None | `"+8613800138000"` |

---

### UserUpdate

更新用户的请求体（部分更新，所有字段可选）。

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        examples=["john_updated"],
        description="用户名，唯一",
    )
    email: Optional[EmailStr] = Field(
        None,
        examples=["john_new@example.com"],
        description="邮箱地址，唯一，合法邮箱格式",
    )
    phone: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{6,14}$",
        examples=["+8613800138000"],
        description="电话号码，可选，唯一",
    )
    is_active: Optional[bool] = Field(
        None,
        examples=[False],
        description="是否激活",
    )
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| username | str \| None | 否 | 3-32 字符，唯一 | None | `"john_updated"` |
| email | EmailStr \| None | 否 | 合法邮箱格式，唯一 | None | `"john_new@example.com"` |
| phone | str \| None | 否 | 格式匹配 `+?[1-9]\d{6,14}`，唯一 | None | `"+8613800138000"` |
| is_active | bool \| None | 否 | — | None | `false` |

---

### UserResponse

单个用户的响应体。

```python
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


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
    email: EmailStr = Field(
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
```

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | int | 自增主键 | `1` |
| username | str | 用户名 | `"john_doe"` |
| email | EmailStr | 邮箱地址 | `"john@example.com"` |
| phone | str \| None | 电话号码，可选，格式需匹配 `+?[1-9]\d{6,14}`，唯一 | `"+8613800138000"` |
| is_active | bool | 是否激活 | `true` |
| created_at | datetime | 创建时间（UTC，ISO 8601） | `"2026-07-01T10:00:00Z"` |
| updated_at | datetime | 更新时间（UTC，ISO 8601） | `"2026-07-01T10:00:00Z"` |

---

### UserListResponse

用户列表分页响应。

```python
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
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| items | list[UserResponse] | — | 当前页的用户列表 |
| total | int | >= 0 | 总记录数 |
| page | int | >= 1 | 当前页码 |
| size | int | >= 1 | 每页条数 |
| pages | int | >= 0 | 总页数 |

---

---

## EC2 模型定义

### EC2State 枚举

EC2 实例状态枚举值。

| 值 | 说明 |
|------|------|
| `running` | 运行中 |
| `stopped` | 已停止 |
| `terminated` | 已终止 |
| `pending` | 待处理 |

---

### EC2Instance（内部模型）

EC2 实例的业务实体模型（`app/models/ec2.py`），使用内存字典存储。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | str | 自动生成 | UUID4 | 内部唯一标识 |
| instance_id | str | 是 | — | AWS 实例 ID |
| name | str | 是 | — | 实例名称 |
| instance_type | str | 是 | — | 实例类型 |
| state | str | 是 | — | 实例状态（EC2State 枚举值） |
| region | str | 是 | — | AWS 区域 |
| availability_zone | str \| None | 否 | None | 可用区 |
| private_ip | str \| None | 否 | None | 私有 IP 地址 |
| public_ip | str \| None | 否 | None | 公网 IP 地址 |
| vpc_id | str \| None | 否 | None | VPC ID |
| key_name | str \| None | 否 | None | SSH 密钥对名称 |
| launch_time | str \| None | 否 | None | 实例启动时间（ISO 8601） |
| tags | dict[str, str] | 否 | `{}` | 标签键值对 |
| created_at | str | 自动生成 | 当前 UTC 时间 ISO 8601 | 记录创建时间 |
| updated_at | str | 自动生成 | 当前 UTC 时间 ISO 8601 | 记录更新时间 |

---

### EC2Create

创建 EC2 实例的请求体。

```python
from pydantic import BaseModel, Field
from app.schemas.ec2 import EC2State


class EC2Create(BaseModel):
    instance_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=255)
    instance_type: str = Field(..., min_length=1)
    state: EC2State = Field(...)
    region: str = Field(..., min_length=1)
    availability_zone: str | None = Field(None)
    private_ip: str | None = Field(None)
    public_ip: str | None = Field(None)
    vpc_id: str | None = Field(None)
    key_name: str | None = Field(None)
    launch_time: str | None = Field(None)
    tags: dict[str, str] = Field(default_factory=dict)
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| instance_id | str | 是 | 非空 | — | `"i-0abc1234def56789"` |
| name | str | 是 | 1-255 字符 | — | `"web-server-01"` |
| instance_type | str | 是 | 非空 | — | `"t2.micro"` |
| state | EC2State | 是 | 枚举 | — | `"running"` |
| region | str | 是 | 非空 | — | `"us-east-1"` |
| availability_zone | str \| None | 否 | — | None | `"us-east-1a"` |
| private_ip | str \| None | 否 | — | None | `"10.0.1.100"` |
| public_ip | str \| None | 否 | — | None | `"54.123.45.67"` |
| vpc_id | str \| None | 否 | — | None | `"vpc-0abc1234"` |
| key_name | str \| None | 否 | — | None | `"my-key-pair"` |
| launch_time | str \| None | 否 | ISO 8601 | None | `"2026-07-01T10:00:00Z"` |
| tags | dict[str, str] | 否 | — | `{}` | `{"Environment": "production"}` |

---

### EC2Update

更新 EC2 实例的请求体（部分更新，所有字段可选）。

```python
class EC2Update(BaseModel):
    instance_id: str | None = Field(None, min_length=1)
    name: str | None = Field(None, min_length=1, max_length=255)
    instance_type: str | None = Field(None, min_length=1)
    state: EC2State | None = Field(None)
    region: str | None = Field(None, min_length=1)
    availability_zone: str | None = Field(None)
    private_ip: str | None = Field(None)
    public_ip: str | None = Field(None)
    vpc_id: str | None = Field(None)
    key_name: str | None = Field(None)
    launch_time: str | None = Field(None)
    tags: dict[str, str] | None = Field(None)
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| instance_id | str \| None | 否 | 非空 | None | `"i-0abc1234def56789"` |
| name | str \| None | 否 | 1-255 字符 | None | `"web-server-02"` |
| instance_type | str \| None | 否 | 非空 | None | `"m5.large"` |
| state | EC2State \| None | 否 | 枚举 | None | `"stopped"` |
| region | str \| None | 否 | 非空 | None | `"us-west-2"` |
| availability_zone | str \| None | 否 | — | None | `"us-west-2a"` |
| private_ip | str \| None | 否 | — | None | `"10.0.2.200"` |
| public_ip | str \| None | 否 | — | None | `"52.200.100.50"` |
| vpc_id | str \| None | 否 | — | None | `"vpc-0def5678"` |
| key_name | str \| None | 否 | — | None | `"new-key-pair"` |
| launch_time | str \| None | 否 | ISO 8601 | None | `"2026-07-01T12:00:00Z"` |
| tags | dict[str, str] \| None | 否 | — | None | `{"Environment": "staging"}` |

---

### EC2Response

单个 EC2 实例的响应体。

```python
class EC2Response(BaseModel):
    id: str
    instance_id: str
    name: str
    instance_type: str
    state: str
    region: str
    availability_zone: str | None = None
    private_ip: str | None = None
    public_ip: str | None = None
    vpc_id: str | None = None
    key_name: str | None = None
    launch_time: str | None = None
    tags: dict[str, str] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | str | 内部唯一标识（UUID） | `"550e8400-e29b-41d4-a716-446655440000"` |
| instance_id | str | AWS 实例 ID | `"i-0abc1234def56789"` |
| name | str | 实例名称 | `"web-server-01"` |
| instance_type | str | 实例类型 | `"t2.micro"` |
| state | str | 实例状态 | `"running"` |
| region | str | AWS 区域 | `"us-east-1"` |
| availability_zone | str \| None | 可用区 | `"us-east-1a"` |
| private_ip | str \| None | 私有 IP | `"10.0.1.100"` |
| public_ip | str \| None | 公网 IP | `"54.123.45.67"` |
| vpc_id | str \| None | VPC ID | `"vpc-0abc1234"` |
| key_name | str \| None | SSH 密钥对名称 | `"my-key-pair"` |
| launch_time | str \| None | 启动时间 | `"2026-07-01T10:00:00Z"` |
| tags | dict[str, str] | 标签 | `{"Environment": "production"}` |
| created_at | datetime | 记录创建时间（UTC） | `"2026-07-01T10:00:00Z"` |
| updated_at | datetime | 记录更新时间（UTC） | `"2026-07-01T10:00:00Z"` |

---

### EC2ListResponse

EC2 实例列表分页响应。

```python
class EC2ListResponse(BaseModel):
    items: list[EC2Response]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1)
    pages: int = Field(..., ge=0)
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| items | list[EC2Response] | — | 当前页的 EC2 实例列表 |
| total | int | >= 0 | 总记录数 |
| page | int | >= 1 | 当前页码 |
| size | int | >= 1 | 每页条数 |
| pages | int | >= 0 | 总页数 |

---

### EC2 Schema 字段对比

| 字段 | EC2Create | EC2Update | EC2Response |
|------|-----------|-----------|-------------|
| id | — | — | ✓ |
| instance_id | ✓ 必填 | ✓ 可选 | ✓ |
| name | ✓ 必填 | ✓ 可选 | ✓ |
| instance_type | ✓ 必填 | ✓ 可选 | ✓ |
| state | ✓ 必填 | ✓ 可选 | ✓ |
| region | ✓ 必填 | ✓ 可选 | ✓ |
| availability_zone | ✓ 可选 | ✓ 可选 | ✓ |
| private_ip | ✓ 可选 | ✓ 可选 | ✓ |
| public_ip | ✓ 可选 | ✓ 可选 | ✓ |
| vpc_id | ✓ 可选 | ✓ 可选 | ✓ |
| key_name | ✓ 可选 | ✓ 可选 | ✓ |
| launch_time | ✓ 可选 | ✓ 可选 | ✓ |
| tags | ✓ 可选（默认 `{}`） | ✓ 可选 | ✓ |
| created_at | — | — | ✓ |
| updated_at | — | — | ✓ |

---

## RDS 模型定义

### RDSEngine 枚举

RDS 数据库引擎枚举值。

| 值 | 说明 |
|------|------|
| `mysql` | MySQL |
| `postgres` | PostgreSQL |
| `mariadb` | MariaDB |
| `oracle` | Oracle |
| `sqlserver` | SQL Server |

---

### RDSStatus 枚举

RDS 实例状态枚举值。

| 值 | 说明 |
|------|------|
| `creating` | 创建中 |
| `available` | 可用 |
| `deleting` | 删除中 |
| `stopped` | 已停止 |

---

### RDSInstance（内部模型）

RDS 实例的业务实体模型（`app/models/rds.py`），使用内存列表存储，自增 ID。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | int | 自动生成 | 自增 | 内部唯一标识 |
| db_instance_identifier | str | 是 | — | RDS 实例标识符，唯一 |
| engine | str | 是 | — | 数据库引擎 |
| engine_version | str | 是 | — | 引擎版本号 |
| db_instance_class | str | 是 | — | 实例规格 |
| allocated_storage | int | 是 | — | 分配存储空间（GB） |
| status | str | 否 | `"creating"` | 实例状态（RDSStatus 枚举值） |
| endpoint | str \| None | 否 | None | 连接端点地址 |
| port | int | 否 | 3306 | 连接端口 |
| master_username | str | 是 | — | 主用户名 |
| multi_az | bool | 否 | False | 是否多可用区部署 |
| region | str | 否 | `"us-east-1"` | 所在区域 |
| created_at | str | 自动生成 | 当前 UTC 时间 ISO 8601 | 记录创建时间 |
| updated_at | str | 自动生成 | 当前 UTC 时间 ISO 8601 | 记录更新时间 |

---

### RDSCreate

创建 RDS 实例的请求体。

```python
from pydantic import BaseModel, Field
from app.schemas.rds import RDSEngine, RDSStatus


class RDSCreate(BaseModel):
    db_instance_identifier: str = Field(..., min_length=1)
    engine: RDSEngine = Field(...)
    engine_version: str = Field(..., min_length=1)
    db_instance_class: str = Field(..., min_length=1)
    allocated_storage: int = Field(..., gt=0)
    master_username: str = Field(..., min_length=1)
    status: RDSStatus = Field(default=RDSStatus.creating)
    endpoint: str | None = Field(None)
    port: int = Field(default=3306, gt=0, le=65535)
    multi_az: bool = Field(default=False)
    region: str = Field(default="us-east-1", min_length=1)
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| db_instance_identifier | str | 是 | 非空，唯一 | — | `"my-database-01"` |
| engine | RDSEngine | 是 | 枚举 | — | `"mysql"` |
| engine_version | str | 是 | 非空 | — | `"8.0.35"` |
| db_instance_class | str | 是 | 非空 | — | `"db.t3.micro"` |
| allocated_storage | int | 是 | > 0 | — | `20` |
| master_username | str | 是 | 非空 | — | `"admin"` |
| status | RDSStatus | 否 | 枚举 | `"creating"` | `"creating"` |
| endpoint | str \| None | 否 | — | None | `"my-database-01.abc123.us-east-1.rds.amazonaws.com"` |
| port | int | 否 | 1-65535 | 3306 | `3306` |
| multi_az | bool | 否 | — | False | `false` |
| region | str | 否 | 非空 | `"us-east-1"` | `"us-east-1"` |

---

### RDSUpdate

更新 RDS 实例的请求体（部分更新，所有字段可选）。

```python
class RDSUpdate(BaseModel):
    db_instance_identifier: str | None = Field(None, min_length=1)
    engine: RDSEngine | None = Field(None)
    engine_version: str | None = Field(None, min_length=1)
    db_instance_class: str | None = Field(None, min_length=1)
    allocated_storage: int | None = Field(None, gt=0)
    status: RDSStatus | None = Field(None)
    endpoint: str | None = Field(None)
    port: int | None = Field(None, gt=0, le=65535)
    master_username: str | None = Field(None, min_length=1)
    multi_az: bool | None = Field(None)
    region: str | None = Field(None, min_length=1)
```

| 字段 | 类型 | 必填 | 约束 | 默认值 | 示例 |
|------|------|------|------|--------|------|
| db_instance_identifier | str \| None | 否 | 非空，唯一 | None | `"my-database-02"` |
| engine | RDSEngine \| None | 否 | 枚举 | None | `"postgres"` |
| engine_version | str \| None | 否 | 非空 | None | `"15.4"` |
| db_instance_class | str \| None | 否 | 非空 | None | `"db.m5.large"` |
| allocated_storage | int \| None | 否 | > 0 | None | `100` |
| status | RDSStatus \| None | 否 | 枚举 | None | `"available"` |
| endpoint | str \| None | 否 | — | None | `"my-database-02.abc123.us-east-1.rds.amazonaws.com"` |
| port | int \| None | 否 | 1-65535 | None | `5432` |
| master_username | str \| None | 否 | 非空 | None | `"dbadmin"` |
| multi_az | bool \| None | 否 | — | None | `true` |
| region | str \| None | 否 | 非空 | None | `"us-west-2"` |

---

### RDSResponse

单个 RDS 实例的响应体。

```python
class RDSResponse(BaseModel):
    id: int
    db_instance_identifier: str
    engine: str
    engine_version: str
    db_instance_class: str
    allocated_storage: int
    status: str
    endpoint: str | None = None
    port: int
    master_username: str
    multi_az: bool
    region: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | int | 内部唯一标识（自增） | `1` |
| db_instance_identifier | str | RDS 实例标识符 | `"my-database-01"` |
| engine | str | 数据库引擎 | `"mysql"` |
| engine_version | str | 引擎版本号 | `"8.0.35"` |
| db_instance_class | str | 实例规格 | `"db.t3.micro"` |
| allocated_storage | int | 分配存储空间（GB） | `20` |
| status | str | 实例状态 | `"available"` |
| endpoint | str \| None | 连接端点地址 | `"my-database-01.abc123.us-east-1.rds.amazonaws.com"` |
| port | int | 连接端口 | `3306` |
| master_username | str | 主用户名 | `"admin"` |
| multi_az | bool | 是否多可用区部署 | `false` |
| region | str | 所在区域 | `"us-east-1"` |
| created_at | datetime | 记录创建时间（UTC） | `"2026-07-01T10:00:00Z"` |
| updated_at | datetime | 记录更新时间（UTC） | `"2026-07-01T10:00:00Z"` |

---

### RDSListResponse

RDS 实例列表分页响应。

```python
class RDSListResponse(BaseModel):
    items: list[RDSResponse]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1)
    pages: int = Field(..., ge=0)
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| items | list[RDSResponse] | — | 当前页的 RDS 实例列表 |
| total | int | >= 0 | 总记录数 |
| page | int | >= 1 | 当前页码 |
| size | int | >= 1 | 每页条数 |
| pages | int | >= 0 | 总页数 |

---

### RDS Schema 字段对比

| 字段 | RDSCreate | RDSUpdate | RDSResponse |
|------|-----------|-----------|-------------|
| id | — | — | ✓ |
| db_instance_identifier | ✓ 必填 | ✓ 可选 | ✓ |
| engine | ✓ 必填 | ✓ 可选 | ✓ |
| engine_version | ✓ 必填 | ✓ 可选 | ✓ |
| db_instance_class | ✓ 必填 | ✓ 可选 | ✓ |
| allocated_storage | ✓ 必填 | ✓ 可选 | ✓ |
| master_username | ✓ 必填 | ✓ 可选 | ✓ |
| status | ✓ 可选（默认 `creating`） | ✓ 可选 | ✓ |
| endpoint | ✓ 可选 | ✓ 可选 | ✓ |
| port | ✓ 可选（默认 `3306`） | ✓ 可选 | ✓ |
| multi_az | ✓ 可选（默认 `false`） | ✓ 可选 | ✓ |
| region | ✓ 可选（默认 `us-east-1`） | ✓ 可选 | ✓ |
| created_at | — | — | ✓ |
| updated_at | — | — | ✓ |

---

## 文件组织

```
app/schemas/
├── __init__.py       # 导出所有 Schema
├── common.py         # ErrorResponse, PaginationParams
├── ec2.py            # EC2State, EC2Create, EC2Update, EC2Response, EC2ListResponse
├── rds.py            # RDSEngine, RDSStatus, RDSCreate, RDSUpdate, RDSResponse, RDSListResponse
├── todo.py           # TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
└── user.py           # UserCreate, UserUpdate, UserResponse, UserListResponse
```

### `app/schemas/__init__.py`

```python
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.ec2 import EC2Create, EC2Update, EC2Response, EC2ListResponse, EC2State
from app.schemas.rds import RDSEngine, RDSStatus, RDSCreate, RDSUpdate, RDSResponse, RDSListResponse
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse

__all__ = [
    "ErrorResponse",
    "PaginationParams",
    "EC2State",
    "EC2Create",
    "EC2Update",
    "EC2Response",
    "EC2ListResponse",
    "RDSEngine",
    "RDSStatus",
    "RDSCreate",
    "RDSUpdate",
    "RDSResponse",
    "RDSListResponse",
    "TodoCreate",
    "TodoUpdate",
    "TodoResponse",
    "TodoListResponse",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserListResponse",
]
```
