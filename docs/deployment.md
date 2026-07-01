# Uvicorn 服务启动与配置方案

## 概述

本项目使用 Uvicorn 作为 ASGI 服务器运行 FastAPI 应用。通过环境变量和启动脚本区分开发与生产环境配置。

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `APP_HOST` | `0.0.0.0` | 服务监听地址 |
| `APP_PORT` | `8000` | 服务监听端口 |
| `APP_ENV` | `dev` | 运行环境（`dev` / `prod`） |
| `APP_WORKERS` | `4` | 生产环境 worker 进程数 |

## 开发环境配置

开发环境启用热重载，单进程运行，便于快速迭代。

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**参数说明：**

| 参数 | 值 | 说明 |
|------|-----|------|
| `--reload` | — | 文件变更时自动重启服务 |
| `--host` | `0.0.0.0` | 允许外部访问（容器/远程开发场景） |
| `--port` | `8000` | 开发端口 |

**注意事项：**
- `--reload` 仅用于开发，会增加额外的文件监听开销
- 热重载使用 watchfiles 库（uvicorn[standard] 已包含）

## 生产环境配置

生产环境禁用热重载，使用多 worker 进程提高并发能力。

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**参数说明：**

| 参数 | 值 | 说明 |
|------|-----|------|
| `--host` | `0.0.0.0` | 监听所有网络接口 |
| `--port` | `8000` | 服务端口（通过反向代理暴露） |
| `--workers` | `4` | worker 进程数，建议 `2 * CPU核心数 + 1` |
| 无 `--reload` | — | 生产环境禁止热重载 |

**生产建议：**
- Worker 数量可根据服务器 CPU 核心数调整，公式：`2 * cores + 1`
- 搭配 Nginx/Traefik 等反向代理处理 TLS 终止和静态资源
- 使用 systemd 或容器编排工具管理进程生命周期
- 日志级别建议设为 `info`（默认值）

## 开发 vs 生产配置对比

| 配置项 | 开发环境 | 生产环境 |
|--------|----------|----------|
| reload | 启用 | 禁用 |
| workers | 1（默认） | 4（可配置） |
| 日志级别 | debug | info |
| 访问日志 | 启用 | 启用 |
| 进程管理 | 直接运行 | systemd / Docker |

## 启动脚本规范 (run.sh)

项目根目录提供 `run.sh` 脚本，根据 `APP_ENV` 环境变量自动选择启动模式。

### 脚本骨架

```bash
#!/usr/bin/env bash
set -euo pipefail

# 读取环境变量（带默认值）
HOST="${APP_HOST:-0.0.0.0}"
PORT="${APP_PORT:-8000}"
ENV="${APP_ENV:-dev}"
WORKERS="${APP_WORKERS:-4}"

echo "Starting app in [${ENV}] mode on ${HOST}:${PORT}"

if [ "$ENV" = "prod" ]; then
    exec uvicorn app.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --workers "$WORKERS"
else
    exec uvicorn app.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --reload
fi
```

### 脚本说明

- 使用 `set -euo pipefail` 确保脚本在出错时立即终止
- 使用 `exec` 替换当前 shell 进程，保证信号正确传递（对容器环境尤为重要）
- 所有参数通过环境变量覆盖，支持灵活部署
- `APP_ENV` 非 `prod` 时统一按开发模式启动

### 使用示例

```bash
# 开发模式（默认）
./run.sh

# 生产模式
APP_ENV=prod ./run.sh

# 自定义端口和 worker 数
APP_ENV=prod APP_PORT=9000 APP_WORKERS=8 ./run.sh
```

## 容器部署参考

配合 Dockerfile 使用时的建议：

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
ENV APP_ENV=prod
EXPOSE 8000
CMD ["./run.sh"]
```

## 健康检查

部署时配合健康检查端点验证服务可用性：

```bash
curl -f http://localhost:8000/health || exit 1
```
