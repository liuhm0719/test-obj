# API 接口设计

## 概述

本文档定义 Todo 资源的 RESTful API 接口，供开发任务（OAP-4407）直接实现。

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
