# FastAPI Example Project

基于 FastAPI 构建的示例 RESTful API 项目，包含 Todo、User、EC2、RDS 和 Redis 资源 CRUD 接口。

## 环境要求

- Python 3.11+
- pip

## 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

安装开发依赖（含测试和代码检查工具）：

```bash
pip install -e ".[dev]"
```

### 2. 启动服务

**开发模式**（带热重载）：

```bash
./run.sh
```

或手动指定环境：

```bash
APP_ENV=dev ./run.sh
```

**生产模式**（多 worker）：

```bash
APP_ENV=prod ./run.sh
```

自定义端口和 worker 数：

```bash
APP_ENV=prod APP_PORT=9000 APP_WORKERS=8 ./run.sh
```

### 3. 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `APP_ENV` | `dev` | 运行环境（`dev` / `prod`） |
| `APP_HOST` | `0.0.0.0` | 服务监听地址 |
| `APP_PORT` | `8000` | 服务监听端口 |
| `APP_WORKERS` | `4` | 生产环境 worker 进程数 |

参考 `.env.example` 了解所有可配置项。

## API 端点

### 通用

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/health` | 健康检查 |

### Todo 资源

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/todos` | 创建 Todo |
| GET | `/api/v1/todos` | Todo 列表（分页） |
| GET | `/api/v1/todos/{todo_id}` | 获取单个 Todo |
| PUT | `/api/v1/todos/{todo_id}` | 更新 Todo |
| DELETE | `/api/v1/todos/{todo_id}` | 删除 Todo |

### User 资源

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/users` | 创建用户（username/email 唯一） |
| GET | `/api/v1/users` | 用户列表（分页） |
| GET | `/api/v1/users/{user_id}` | 获取单个用户 |
| PUT | `/api/v1/users/{user_id}` | 更新用户（部分更新） |
| DELETE | `/api/v1/users/{user_id}` | 删除用户 |

### EC2 资源

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/ec2` | 创建 EC2 实例记录 |
| GET | `/api/v1/ec2` | EC2 实例列表（分页） |
| GET | `/api/v1/ec2/{ec2_id}` | 获取单个 EC2 实例 |
| PUT | `/api/v1/ec2/{ec2_id}` | 更新 EC2 实例记录 |
| DELETE | `/api/v1/ec2/{ec2_id}` | 删除 EC2 实例记录 |

### RDS 资源

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/rds` | 创建 RDS 实例记录 |
| GET | `/api/v1/rds` | RDS 实例列表（分页） |
| GET | `/api/v1/rds/{rds_id}` | 获取单个 RDS 实例 |
| PUT | `/api/v1/rds/{rds_id}` | 更新 RDS 实例记录 |
| DELETE | `/api/v1/rds/{rds_id}` | 删除 RDS 实例记录 |

### Redis 资源

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/redis` | 创建 Redis 实例记录 |
| GET | `/api/v1/redis` | Redis 实例列表（分页） |
| GET | `/api/v1/redis/{redis_id}` | 获取单个 Redis 实例 |
| PUT | `/api/v1/redis/{redis_id}` | 更新 Redis 实例记录 |
| DELETE | `/api/v1/redis/{redis_id}` | 删除 Redis 实例记录 |

## API 文档

启动服务后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 运行测试

```bash
pytest
```
