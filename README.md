# FastAPI Example Project

基于 FastAPI 构建的示例 RESTful API 项目，包含 Todo CRUD 接口。

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

## API 文档

启动服务后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 运行测试

```bash
pytest
```
