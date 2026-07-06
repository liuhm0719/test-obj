# 项目目录结构设计

## 概述

本项目基于 FastAPI 框架，采用分层架构组织代码。各模块职责清晰，便于团队协作与后续扩展。

## 目录结构

```
project-root/
├── app/                    # 主程序包
│   ├── __init__.py
│   ├── main.py             # FastAPI 应用入口，创建 app 实例、注册路由
│   ├── config.py           # 配置管理（环境变量、应用设置）
│   ├── dependencies.py     # 公共依赖注入（数据库会话、认证等）
│   ├── routers/            # 路由模块
│   │   ├── __init__.py
│   │   ├── health.py      # 健康检查路由
│   │   ├── todos.py       # Todo CRUD 路由端点
│   │   ├── users.py       # User CRUD 路由端点
│   │   └── ec2.py         # EC2 实例 CRUD 路由端点
│   ├── models/             # Pydantic 数据模型（业务实体）
│   │   ├── __init__.py
│   │   ├── todo.py        # Todo 实体模型与内存存储
│   │   ├── user.py        # User 实体模型与内存存储（int 自增 ID）
│   │   └── ec2.py         # EC2 实例模型与内存存储（UUID ID）
│   └── schemas/            # 请求/响应 Schema 定义
│       ├── __init__.py
│       ├── common.py      # 通用 Schema（ErrorResponse、PaginationParams）
│       ├── ec2.py         # EC2 请求/响应 Schema（含 EC2State 枚举）
│       ├── todo.py        # Todo 请求/响应 Schema
│       └── user.py        # User 请求/响应 Schema（含 EmailStr 校验）
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures（TestClient 等）
│   ├── test_health.py     # 健康检查测试
│   ├── test_startup.py    # 项目环境验证测试
│   ├── test_startup_script.py # 服务启动脚本验证测试
│   ├── test_todos.py      # Todo CRUD API 测试
│   ├── test_users.py      # User CRUD API 测试（22 个用例）
│   └── test_ec2.py        # EC2 CRUD API 测试
├── docs/                   # 项目文档
│   ├── api-design.md      # API 接口设计文档
│   ├── data-models.md     # 数据模型设计文档
│   ├── dependencies.md    # 依赖管理方案
│   ├── deployment.md      # 部署配置方案
│   ├── delivery-report.md # 项目交付报告
│   └── project-structure.md # 项目目录结构（本文件）
├── pyproject.toml          # 项目元数据与依赖管理
├── CLAUDE.md               # 开发规范与约定
└── README.md               # 项目说明
```

## 模块职责

### `app/`

主程序包，包含所有业务代码。

| 文件/目录 | 职责 |
|-----------|------|
| `main.py` | 创建 FastAPI 实例，注册中间件，挂载路由 |
| `config.py` | 使用 pydantic-settings 管理配置，支持 `.env` 文件 |
| `dependencies.py` | 定义可复用的 Depends 依赖项 |

### `app/routers/`

路由模块，按业务领域拆分。每个文件对应一组相关的 API 端点。

- 每个路由文件创建独立的 `APIRouter` 实例
- 在 `main.py` 中通过 `app.include_router()` 注册
- 路由文件命名使用小写蛇形：`user_management.py`

### `app/models/`

Pydantic 数据模型，表示业务实体和领域对象。

- 用于内部数据传递和业务逻辑
- 如需 ORM 集成，此处放置 SQLAlchemy 模型

### `app/schemas/`

API 请求/响应的 Schema 定义。

- 与 `models/` 分离，保证 API 契约独立于内部实现
- 命名约定：`XxxRequest`、`XxxResponse`、`XxxCreate`、`XxxUpdate`

### `tests/`

测试代码，结构镜像 `app/` 目录。

- 使用 pytest 框架
- `conftest.py` 放置共享 fixtures（如 TestClient）
- 测试文件命名：`test_<模块名>.py`

### `docs/`

项目文档，包含架构设计、API 说明等。

## 命名规范

| 类别 | 规范 | 示例 |
|------|------|------|
| 文件名 | 小写蛇形 | `user_management.py` |
| 类名 | 大驼峰 | `UserResponse` |
| 函数/变量 | 小写蛇形 | `get_current_user` |
| 常量 | 大写蛇形 | `MAX_RETRY_COUNT` |
| 路由路径 | 小写连字符 | `/api/v1/user-profiles` |
| API 版本前缀 | `/api/v1/` | — |

## 扩展规则

当项目规模增长时：

1. `routers/` 下按业务领域添加新路由文件
2. `models/` 和 `schemas/` 下按领域添加对应文件
3. 如需服务层，添加 `app/services/` 目录
4. 如需数据访问层，添加 `app/repositories/` 目录
5. 如需后台任务，添加 `app/tasks/` 目录
