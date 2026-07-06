# API 接口设计

## 概述

本文档定义项目中各资源的 RESTful API 接口，供开发任务直接实现。

- 基础路径：`/api/v1`
- 内容类型：`application/json`
- 认证：暂无（后续迭代添加）

---

## 端点列表

| 方法 | 路径 | 描述 | 状态码 |
|------|------|------|--------|
| GET | `/api/v1/todos` | 获取 Todo 列表（分页） | 200 |
| POST | `/api/v1/todos` | 创建 Todo | 201 |
| GET | `/api/v1/todos/{id}` | 获取单个 Todo | 200 / 404 |
| PUT | `/api/v1/todos/{id}` | 更新 Todo | 200 / 404 |
| DELETE | `/api/v1/todos/{id}` | 删除 Todo | 200 / 404 |
| POST | `/api/v1/ec2` | 创建 EC2 实例记录 | 201 |
| GET | `/api/v1/ec2` | 获取 EC2 实例列表（分页） | 200 |
| GET | `/api/v1/ec2/{ec2_id}` | 获取单个 EC2 实例 | 200 / 404 |
| PUT | `/api/v1/ec2/{ec2_id}` | 更新 EC2 实例记录 | 200 / 404 |
| DELETE | `/api/v1/ec2/{ec2_id}` | 删除 EC2 实例记录 | 204 / 404 |
| POST | `/api/v1/rds` | 创建 RDS 实例记录 | 201 |
| GET | `/api/v1/rds` | 获取 RDS 实例列表（分页） | 200 |
| GET | `/api/v1/rds/{rds_id}` | 获取单个 RDS 实例 | 200 / 404 |
| PUT | `/api/v1/rds/{rds_id}` | 更新 RDS 实例记录 | 200 / 404 |
| DELETE | `/api/v1/rds/{rds_id}` | 删除 RDS 实例记录 | 204 / 404 |

---

## 端点详细定义

### 1. GET /api/v1/todos

获取 Todo 列表，支持分页。

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 约束 | 说明 |
|------|------|------|--------|------|------|
| page | int | 否 | 1 | >= 1 | 页码 |
| size | int | 否 | 20 | 1-100 | 每页条数 |

**成功响应：** `200 OK`

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "done": false,
      "created_at": "2026-07-01T10:00:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "size": 20,
  "pages": 3
}
```

**错误响应：**

- `422 Unprocessable Entity` — 参数校验失败（如 page < 1 或 size > 100）

---

### 2. POST /api/v1/todos

创建新的 Todo。

**请求体：**

```json
{
  "title": "Buy groceries"
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| title | string | 是 | 1-200 字符 | Todo 标题 |

**成功响应：** `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "done": false,
  "created_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `422 Unprocessable Entity` — 请求体校验失败（如 title 为空或超长）

---

### 3. GET /api/v1/todos/{id}

获取单个 Todo 详情。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | UUID | Todo 的唯一标识符 |

**成功响应：** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "done": false,
  "created_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — Todo 不存在
- `422 Unprocessable Entity` — id 格式非法（非 UUID）

---

### 4. PUT /api/v1/todos/{id}

更新已有 Todo（全量更新）。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | UUID | Todo 的唯一标识符 |

**请求体：**

```json
{
  "title": "Buy groceries and cook",
  "done": true
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| title | string | 是 | 1-200 字符 | Todo 标题 |
| done | bool | 是 | — | 完成状态 |

**成功响应：** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook",
  "done": true,
  "created_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — Todo 不存在
- `422 Unprocessable Entity` — 请求体校验失败

---

### 5. DELETE /api/v1/todos/{id}

删除指定 Todo。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | UUID | Todo 的唯一标识符 |

**成功响应：** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "done": false,
  "created_at": "2026-07-01T10:00:00Z"
}
```

返回被删除的 Todo 对象，方便客户端确认。

**错误响应：**

- `404 Not Found` — Todo 不存在
- `422 Unprocessable Entity` — id 格式非法

---

## 统一错误响应格式

所有错误响应使用统一结构：

```json
{
  "code": "ERROR_CODE",
  "message": "人类可读的错误描述"
}
```

**错误码定义：**

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `NOT_FOUND` | 404 | 资源不存在 |
| `VALIDATION_ERROR` | 422 | 请求参数或请求体校验失败 |
| `BAD_REQUEST` | 400 | 请求格式错误（如非法 JSON） |

---

## 分页规范

分页响应包含以下元数据字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| items | array | 当前页的数据列表 |
| total | int | 总记录数 |
| page | int | 当前页码 |
| size | int | 每页条数 |
| pages | int | 总页数（向上取整） |

分页参数约束：
- `page` >= 1，默认 1
- `size` >= 1 且 <= 100，默认 20
- 超出范围的页码返回空 items 列表（不报错）

---

## User 资源

### 端点列表

| 方法 | 路径 | 描述 | 状态码 |
|------|------|------|--------|
| POST | `/api/v1/users` | 创建用户 | 201 |
| GET | `/api/v1/users` | 获取用户列表（分页） | 200 |
| GET | `/api/v1/users/{user_id}` | 获取单个用户 | 200 / 404 |
| PUT | `/api/v1/users/{user_id}` | 更新用户（部分更新） | 200 / 404 |
| DELETE | `/api/v1/users/{user_id}` | 删除用户 | 204 / 404 |

---

### 端点详细定义

#### 1. POST /api/v1/users

创建新用户。

**请求体：**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+8613800138000"
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| username | string | 是 | 3-32 字符，唯一 | 用户名 |
| email | string | 是 | 合法邮箱格式，唯一 | 邮箱地址 |
| phone | string | 否 | 格式匹配 `+?[1-9]\d{6,14}`，唯一 | 电话号码 |

**成功响应：** `201 Created`

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+8613800138000",
  "is_active": true,
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `400 Bad Request` — username 已存在：`{"code": "USER_EXISTS", "message": "Username already exists"}`
- `400 Bad Request` — email 已存在：`{"code": "EMAIL_EXISTS", "message": "Email already exists"}`
- `400 Bad Request` — phone 已存在：`{"code": "PHONE_EXISTS", "message": "Phone already exists"}`
- `422 Unprocessable Entity` — 请求体校验失败（如 username 长度不符、email 格式非法、phone 格式不匹配）

---

#### 2. GET /api/v1/users

获取用户列表，支持分页。

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 约束 | 说明 |
|------|------|------|--------|------|------|
| page | int | 否 | 1 | >= 1 | 页码 |
| size | int | 否 | 20 | 1-100 | 每页条数 |

**成功响应：** `200 OK`

```json
{
  "items": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "phone": "+8613800138000",
      "is_active": true,
      "created_at": "2026-07-01T10:00:00Z",
      "updated_at": "2026-07-01T10:00:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

**错误响应：**

- `422 Unprocessable Entity` — 参数校验失败（如 page < 1 或 size > 100）

---

#### 3. GET /api/v1/users/{user_id}

获取单个用户详情。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户的唯一标识符 |

**成功响应：** `200 OK`

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+8613800138000",
  "is_active": true,
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — 用户不存在：`{"code": "NOT_FOUND", "message": "User not found"}`

---

#### 4. PUT /api/v1/users/{user_id}

更新已有用户，支持部分更新（仅传入需要修改的字段）。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户的唯一标识符 |

**请求体：**

```json
{
  "username": "john_updated",
  "email": "john_new@example.com",
  "phone": "+8613900139000",
  "is_active": false
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| username | string | 否 | 3-32 字符，唯一 | 用户名 |
| email | string | 否 | 合法邮箱格式，唯一 | 邮箱地址 |
| phone | string | 否 | 格式匹配 `+?[1-9]\d{6,14}`，唯一 | 电话号码 |
| is_active | bool | 否 | — | 是否激活 |

**成功响应：** `200 OK`

```json
{
  "id": 1,
  "username": "john_updated",
  "email": "john_new@example.com",
  "phone": "+8613900139000",
  "is_active": false,
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — 用户不存在：`{"code": "NOT_FOUND", "message": "User not found"}`
- `400 Bad Request` — username 已存在：`{"code": "USER_EXISTS", "message": "Username already exists"}`
- `400 Bad Request` — email 已存在：`{"code": "EMAIL_EXISTS", "message": "Email already exists"}`
- `400 Bad Request` — phone 已存在：`{"code": "PHONE_EXISTS", "message": "Phone already exists"}`
- `422 Unprocessable Entity` — 请求体校验失败

---

#### 5. DELETE /api/v1/users/{user_id}

删除指定用户。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户的唯一标识符 |

**成功响应：** `204 No Content`

无响应体。

**错误响应：**

- `404 Not Found` — 用户不存在：`{"code": "NOT_FOUND", "message": "User not found"}`

---

### User 业务规则

| 规则 | 错误码 | HTTP 状态码 | 说明 |
|------|--------|-------------|------|
| username 唯一 | `USER_EXISTS` | 400 | 创建或更新时 username 已被其他用户占用 |
| email 唯一 | `EMAIL_EXISTS` | 400 | 创建或更新时 email 已被其他用户占用 |
| phone 唯一 | `PHONE_EXISTS` | 400 | 创建或更新时 phone 已被其他用户占用 |

### User 错误码汇总

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `NOT_FOUND` | 404 | 用户不存在 |
| `USER_EXISTS` | 400 | username 已被占用 |
| `EMAIL_EXISTS` | 400 | email 已被占用 |
| `PHONE_EXISTS` | 400 | phone 已被占用 |
| `VALIDATION_ERROR` | 422 | 请求参数或请求体校验失败 |

---

## EC2 资源

### 端点列表

| 方法 | 路径 | 描述 | 状态码 |
|------|------|------|--------|
| POST | `/api/v1/ec2` | 创建 EC2 实例记录 | 201 |
| GET | `/api/v1/ec2` | 获取 EC2 实例列表（分页） | 200 |
| GET | `/api/v1/ec2/{ec2_id}` | 获取单个 EC2 实例 | 200 / 404 |
| PUT | `/api/v1/ec2/{ec2_id}` | 更新 EC2 实例记录（部分更新） | 200 / 404 |
| DELETE | `/api/v1/ec2/{ec2_id}` | 删除 EC2 实例记录 | 204 / 404 |

---

### 端点详细定义

#### 1. POST /api/v1/ec2

创建新的 EC2 实例记录。

**请求体：**

```json
{
  "instance_id": "i-0abc1234def56789",
  "name": "web-server-01",
  "instance_type": "t2.micro",
  "state": "running",
  "region": "us-east-1",
  "availability_zone": "us-east-1a",
  "private_ip": "10.0.1.100",
  "public_ip": "54.123.45.67",
  "vpc_id": "vpc-0abc1234",
  "key_name": "my-key-pair",
  "launch_time": "2026-07-01T10:00:00Z",
  "tags": {"Environment": "production", "Team": "backend"}
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| instance_id | string | 是 | 非空 | AWS 实例 ID |
| name | string | 是 | 1-255 字符 | 实例名称（对应 Name 标签） |
| instance_type | string | 是 | 非空 | 实例类型 |
| state | string | 是 | 枚举：running/stopped/terminated/pending | 实例状态 |
| region | string | 是 | 非空 | AWS 区域 |
| availability_zone | string | 否 | — | 可用区 |
| private_ip | string | 否 | — | 私有 IP 地址 |
| public_ip | string | 否 | — | 公网 IP 地址 |
| vpc_id | string | 否 | — | VPC ID |
| key_name | string | 否 | — | SSH 密钥对名称 |
| launch_time | string | 否 | ISO 8601 格式 | 实例启动时间 |
| tags | object | 否 | 键值对 | 标签（默认空对象） |

**成功响应：** `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "instance_id": "i-0abc1234def56789",
  "name": "web-server-01",
  "instance_type": "t2.micro",
  "state": "running",
  "region": "us-east-1",
  "availability_zone": "us-east-1a",
  "private_ip": "10.0.1.100",
  "public_ip": "54.123.45.67",
  "vpc_id": "vpc-0abc1234",
  "key_name": "my-key-pair",
  "launch_time": "2026-07-01T10:00:00Z",
  "tags": {"Environment": "production", "Team": "backend"},
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `422 Unprocessable Entity` — 请求体校验失败（如必填字段缺失、state 不在枚举范围内）

---

#### 2. GET /api/v1/ec2

获取 EC2 实例列表，支持分页。

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 约束 | 说明 |
|------|------|------|--------|------|------|
| page | int | 否 | 1 | >= 1 | 页码 |
| size | int | 否 | 20 | 1-100 | 每页条数 |

**成功响应：** `200 OK`

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "instance_id": "i-0abc1234def56789",
      "name": "web-server-01",
      "instance_type": "t2.micro",
      "state": "running",
      "region": "us-east-1",
      "availability_zone": "us-east-1a",
      "private_ip": "10.0.1.100",
      "public_ip": "54.123.45.67",
      "vpc_id": "vpc-0abc1234",
      "key_name": "my-key-pair",
      "launch_time": "2026-07-01T10:00:00Z",
      "tags": {"Environment": "production"},
      "created_at": "2026-07-01T10:00:00Z",
      "updated_at": "2026-07-01T10:00:00Z"
    }
  ],
  "total": 10,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

**错误响应：**

- `422 Unprocessable Entity` — 参数校验失败（如 page < 1 或 size > 100）

---

#### 3. GET /api/v1/ec2/{ec2_id}

获取单个 EC2 实例详情。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| ec2_id | string (UUID) | EC2 实例的内部唯一标识符 |

**成功响应：** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "instance_id": "i-0abc1234def56789",
  "name": "web-server-01",
  "instance_type": "t2.micro",
  "state": "running",
  "region": "us-east-1",
  "availability_zone": "us-east-1a",
  "private_ip": "10.0.1.100",
  "public_ip": "54.123.45.67",
  "vpc_id": "vpc-0abc1234",
  "key_name": "my-key-pair",
  "launch_time": "2026-07-01T10:00:00Z",
  "tags": {"Environment": "production"},
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — EC2 实例不存在：`{"code": "NOT_FOUND", "message": "EC2 instance not found"}`

---

#### 4. PUT /api/v1/ec2/{ec2_id}

更新已有 EC2 实例记录，支持部分更新（仅传入需要修改的字段）。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| ec2_id | string (UUID) | EC2 实例的内部唯一标识符 |

**请求体：**

```json
{
  "state": "stopped",
  "instance_type": "m5.large",
  "tags": {"Environment": "staging"}
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| instance_id | string | 否 | 非空 | AWS 实例 ID |
| name | string | 否 | 1-255 字符 | 实例名称 |
| instance_type | string | 否 | 非空 | 实例类型 |
| state | string | 否 | 枚举：running/stopped/terminated/pending | 实例状态 |
| region | string | 否 | 非空 | AWS 区域 |
| availability_zone | string | 否 | — | 可用区 |
| private_ip | string | 否 | — | 私有 IP 地址 |
| public_ip | string | 否 | — | 公网 IP 地址 |
| vpc_id | string | 否 | — | VPC ID |
| key_name | string | 否 | — | SSH 密钥对名称 |
| launch_time | string | 否 | ISO 8601 格式 | 实例启动时间 |
| tags | object | 否 | 键值对 | 标签 |

**成功响应：** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "instance_id": "i-0abc1234def56789",
  "name": "web-server-01",
  "instance_type": "m5.large",
  "state": "stopped",
  "region": "us-east-1",
  "availability_zone": "us-east-1a",
  "private_ip": "10.0.1.100",
  "public_ip": "54.123.45.67",
  "vpc_id": "vpc-0abc1234",
  "key_name": "my-key-pair",
  "launch_time": "2026-07-01T10:00:00Z",
  "tags": {"Environment": "staging"},
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — EC2 实例不存在：`{"code": "NOT_FOUND", "message": "EC2 instance not found"}`
- `422 Unprocessable Entity` — 请求体校验失败

---

#### 5. DELETE /api/v1/ec2/{ec2_id}

删除指定 EC2 实例记录。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| ec2_id | string (UUID) | EC2 实例的内部唯一标识符 |

**成功响应：** `204 No Content`

无响应体。

**错误响应：**

- `404 Not Found` — EC2 实例不存在：`{"code": "NOT_FOUND", "message": "EC2 instance not found"}`

---

### EC2 错误码汇总

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `NOT_FOUND` | 404 | EC2 实例不存在 |
| `VALIDATION_ERROR` | 422 | 请求参数或请求体校验失败 |

---

## RDS 资源

### 端点列表

| 方法 | 路径 | 描述 | 状态码 |
|------|------|------|--------|
| POST | `/api/v1/rds` | 创建 RDS 实例记录 | 201 |
| GET | `/api/v1/rds` | 获取 RDS 实例列表（分页） | 200 |
| GET | `/api/v1/rds/{rds_id}` | 获取单个 RDS 实例 | 200 / 404 |
| PUT | `/api/v1/rds/{rds_id}` | 更新 RDS 实例记录 | 200 / 404 |
| DELETE | `/api/v1/rds/{rds_id}` | 删除 RDS 实例记录 | 204 / 404 |

---

### 端点详细定义

#### 1. POST /api/v1/rds

创建新的 RDS 实例记录。

**请求体：**

```json
{
  "db_instance_identifier": "my-database-01",
  "engine": "mysql",
  "engine_version": "8.0.35",
  "db_instance_class": "db.t3.micro",
  "allocated_storage": 20,
  "master_username": "admin",
  "status": "creating",
  "endpoint": "my-database-01.abc123.us-east-1.rds.amazonaws.com",
  "port": 3306,
  "multi_az": false,
  "region": "us-east-1"
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| db_instance_identifier | string | 是 | 非空，唯一 | RDS 实例标识符 |
| engine | string | 是 | 枚举：mysql/postgres/mariadb/oracle/sqlserver | 数据库引擎 |
| engine_version | string | 是 | 非空 | 引擎版本号 |
| db_instance_class | string | 是 | 非空 | 实例规格 |
| allocated_storage | int | 是 | > 0 | 分配存储空间（GB） |
| master_username | string | 是 | 非空 | 主用户名 |
| status | string | 否 | 枚举：creating/available/deleting/stopped | 实例状态（默认 creating） |
| endpoint | string | 否 | — | 连接端点地址 |
| port | int | 否 | 1-65535 | 连接端口（默认 3306） |
| multi_az | bool | 否 | — | 是否多可用区部署（默认 false） |
| region | string | 否 | 非空 | 所在区域（默认 us-east-1） |

**成功响应：** `201 Created`

```json
{
  "id": 1,
  "db_instance_identifier": "my-database-01",
  "engine": "mysql",
  "engine_version": "8.0.35",
  "db_instance_class": "db.t3.micro",
  "allocated_storage": 20,
  "status": "creating",
  "endpoint": "my-database-01.abc123.us-east-1.rds.amazonaws.com",
  "port": 3306,
  "master_username": "admin",
  "multi_az": false,
  "region": "us-east-1",
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `400 Bad Request` — db_instance_identifier 已存在：`{"code": "DUPLICATE_IDENTIFIER", "message": "db_instance_identifier 'my-database-01' already exists"}`
- `422 Unprocessable Entity` — 请求体校验失败（如必填字段缺失、engine 不在枚举范围内）

---

#### 2. GET /api/v1/rds

获取 RDS 实例列表，支持分页。

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 约束 | 说明 |
|------|------|------|--------|------|------|
| page | int | 否 | 1 | >= 1 | 页码 |
| size | int | 否 | 20 | 1-100 | 每页条数 |

**成功响应：** `200 OK`

```json
{
  "items": [
    {
      "id": 1,
      "db_instance_identifier": "my-database-01",
      "engine": "mysql",
      "engine_version": "8.0.35",
      "db_instance_class": "db.t3.micro",
      "allocated_storage": 20,
      "status": "available",
      "endpoint": "my-database-01.abc123.us-east-1.rds.amazonaws.com",
      "port": 3306,
      "master_username": "admin",
      "multi_az": false,
      "region": "us-east-1",
      "created_at": "2026-07-01T10:00:00Z",
      "updated_at": "2026-07-01T10:00:00Z"
    }
  ],
  "total": 10,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

**错误响应：**

- `422 Unprocessable Entity` — 参数校验失败（如 page < 1 或 size > 100）

---

#### 3. GET /api/v1/rds/{rds_id}

获取单个 RDS 实例详情。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| rds_id | int | RDS 实例的内部唯一标识符 |

**成功响应：** `200 OK`

```json
{
  "id": 1,
  "db_instance_identifier": "my-database-01",
  "engine": "mysql",
  "engine_version": "8.0.35",
  "db_instance_class": "db.t3.micro",
  "allocated_storage": 20,
  "status": "available",
  "endpoint": "my-database-01.abc123.us-east-1.rds.amazonaws.com",
  "port": 3306,
  "master_username": "admin",
  "multi_az": false,
  "region": "us-east-1",
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — RDS 实例不存在：`{"code": "NOT_FOUND", "message": "RDS instance not found"}`

---

#### 4. PUT /api/v1/rds/{rds_id}

更新已有 RDS 实例记录，支持部分更新（仅传入需要修改的字段）。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| rds_id | int | RDS 实例的内部唯一标识符 |

**请求体：**

```json
{
  "db_instance_class": "db.m5.large",
  "allocated_storage": 100,
  "status": "available"
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| db_instance_identifier | string | 否 | 非空，唯一 | RDS 实例标识符 |
| engine | string | 否 | 枚举：mysql/postgres/mariadb/oracle/sqlserver | 数据库引擎 |
| engine_version | string | 否 | 非空 | 引擎版本号 |
| db_instance_class | string | 否 | 非空 | 实例规格 |
| allocated_storage | int | 否 | > 0 | 分配存储空间（GB） |
| status | string | 否 | 枚举：creating/available/deleting/stopped | 实例状态 |
| endpoint | string | 否 | — | 连接端点地址 |
| port | int | 否 | 1-65535 | 连接端口 |
| master_username | string | 否 | 非空 | 主用户名 |
| multi_az | bool | 否 | — | 是否多可用区部署 |
| region | string | 否 | 非空 | 所在区域 |

**成功响应：** `200 OK`

```json
{
  "id": 1,
  "db_instance_identifier": "my-database-01",
  "engine": "mysql",
  "engine_version": "8.0.35",
  "db_instance_class": "db.m5.large",
  "allocated_storage": 100,
  "status": "available",
  "endpoint": "my-database-01.abc123.us-east-1.rds.amazonaws.com",
  "port": 3306,
  "master_username": "admin",
  "multi_az": false,
  "region": "us-east-1",
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

**错误响应：**

- `400 Bad Request` — db_instance_identifier 已存在：`{"code": "DUPLICATE_IDENTIFIER", "message": "db_instance_identifier 'my-database-01' already exists"}`
- `404 Not Found` — RDS 实例不存在：`{"code": "NOT_FOUND", "message": "RDS instance not found"}`
- `422 Unprocessable Entity` — 请求体校验失败

---

#### 5. DELETE /api/v1/rds/{rds_id}

删除指定 RDS 实例记录。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| rds_id | int | RDS 实例的内部唯一标识符 |

**成功响应：** `204 No Content`

无响应体。

**错误响应：**

- `404 Not Found` — RDS 实例不存在：`{"code": "NOT_FOUND", "message": "RDS instance not found"}`

---

### RDS 错误码汇总

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `NOT_FOUND` | 404 | RDS 实例不存在 |
| `DUPLICATE_IDENTIFIER` | 400 | db_instance_identifier 已被占用 |
| `VALIDATION_ERROR` | 422 | 请求参数或请求体校验失败 |
