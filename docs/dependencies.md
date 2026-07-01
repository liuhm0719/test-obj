# 依赖管理方案

## 概述

本项目使用 `pyproject.toml` 管理依赖，遵循 PEP 621 标准。通过可选依赖组（optional-dependencies）区分生产依赖与开发依赖。

## 技术栈

- **Python**: 3.11+
- **Web 框架**: FastAPI 0.110+
- **数据验证**: Pydantic v2
- **ASGI 服务器**: Uvicorn (standard)
- **测试**: pytest + httpx

## 生产依赖

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| fastapi | >=0.110 | Web 框架 |
| uvicorn[standard] | >=0.29 | ASGI 服务器（含 uvloop、httptools） |
| pydantic | >=2.0 | 数据验证与序列化 |

## 开发依赖

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| pytest | >=8.0 | 测试框架 |
| httpx | >=0.27 | 异步 HTTP 客户端（用于 TestClient） |
| ruff | >=0.4 | 代码检查与格式化 |

## 版本锁定策略

- **下限锁定**：使用 `>=` 指定最低兼容版本，允许补丁和小版本更新
- **主版本约束**：通过语义化版本的隐式约束避免破坏性更新（如 pydantic>=2.0 不会安装 v3）
- **lock 文件**：生产部署时使用 `pip freeze > requirements.lock` 或 `pip-tools` 生成精确锁定文件
- **定期更新**：每月检查依赖更新，通过 CI 验证兼容性后升级

## pyproject.toml 配置参考

```toml
[project]
name = "fastapi-example"
version = "0.1.0"
description = "FastAPI example project"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]>=0.29",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "httpx>=0.27",
    "ruff>=0.4",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
```

## 安装方式

```bash
# 安装生产依赖
pip install .

# 安装开发依赖
pip install ".[dev]"

# 生成锁定文件（用于生产部署）
pip freeze > requirements.lock
```

## 依赖更新流程

1. 修改 `pyproject.toml` 中的版本约束
2. 在开发环境执行 `pip install ".[dev]"`
3. 运行完整测试套件：`pytest`
4. 运行代码检查：`ruff check .`
5. 确认无问题后提交变更
