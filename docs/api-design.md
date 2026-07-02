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
  "email": "john@example.com"
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| username | string | 是 | 3-32 字符，唯一 | 用户名 |
| email | string | 是 | 合法邮箱格式，唯一 | 邮箱地址 |

**成功响应：** `201 Created`

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

**错误响应：**

- `400 Bad Request` — username 已存在：`{"code": "USER_EXISTS", "message": "Username already exists"}`
- `400 Bad Request` — email 已存在：`{"code": "EMAIL_EXISTS", "message": "Email already exists"}`
- `422 Unprocessable Entity` — 请求体校验失败（如 username 长度不符、email 格式非法）

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
  "is_active": false
}
```

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| username | string | 否 | 3-32 字符，唯一 | 用户名 |
| email | string | 否 | 合法邮箱格式，唯一 | 邮箱地址 |
| is_active | bool | 否 | — | 是否激活 |

**成功响应：** `200 OK`

```json
{
  "id": 1,
  "username": "john_updated",
  "email": "john_new@example.com",
  "is_active": false,
  "created_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

**错误响应：**

- `404 Not Found` — 用户不存在：`{"code": "NOT_FOUND", "message": "User not found"}`
- `400 Bad Request` — username 已存在：`{"code": "USER_EXISTS", "message": "Username already exists"}`
- `400 Bad Request` — email 已存在：`{"code": "EMAIL_EXISTS", "message": "Email already exists"}`
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

### User 错误码汇总

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `NOT_FOUND` | 404 | 用户不存在 |
| `USER_EXISTS` | 400 | username 已被占用 |
| `EMAIL_EXISTS` | 400 | email 已被占用 |
| `VALIDATION_ERROR` | 422 | 请求参数或请求体校验失败 |
