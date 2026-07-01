# Project Dev — Autonomous Coding Mode

## SKILL OVERRIDE (your human partner explicitly instructs)

Your human partner explicitly tells you to **skip ALL skills** for this session:
- Skip the brainstorming skill.
- Skip the systematic-debugging skill.
- Skip ALL superpowers skills.
- Do NOT ask clarifying questions — there is no user to answer.
- Do NOT seek requirements or domain clarification.
- Make ALL decisions independently with reasonable assumptions and implement immediately.

Per skill rules: "User instructions (CLAUDE.md) take precedence over skills. Only skip skill workflows when your human partner has explicitly told you to." **They have.**

You are implementing a Jira subtask on branch `feature/oap-4403`.
The full task description is in your prompt. Context is also available at `.claude/context.json`.

**Rules:**
- Work in fully autonomous mode — make reasonable decisions independently.
- All changes MUST be committed with clear commit messages.
- Do NOT run `git push` — the system pushes automatically after you finish.
- Do NOT create pull requests — handled automatically.
- Do NOT switch branches.
- Do NOT modify `.claude/context.json` or `.claude/result.json`.
- Write `.claude/result.json` when done (see format below).

**When your work is complete**, write `.claude/result.json`:
```json
{
  "status": "ready_to_push",
  "branch": "feature/oap-4403",
  "base_branch": "main",
  "summary": "Brief description of what was implemented",
  "commits": [{"sha": "abc1234", "message": "feat: ..."}],
  "files_changed": ["path/to/file.ts"],
  "repo_url": "https://github.com/liuhm0719/test-obj"
}
```

If no code changes are needed, write `{"status": "no_changes", ...}`.

---

## Jira 执行摘要（必填）

完成所有工作后，在 `.claude/result.json` 的 `jira_summary` 字段写入以下 Markdown 格式：

```
<!-- devbox-agent-summary -->
## 摘要
（1-3 句话描述本次实现了什么）

## 关键决策
- （列出重要的技术选型及原因，无则写"无特殊决策"）

## 输出产物
- （列出对后续 task 有参考价值的文件路径，无则写"无新增文件"）

## 注意事项
- （下一个 task 需要特别注意的事项，无则写"无"）
```

**重要：** jira_summary 必须以 `<!-- devbox-agent-summary -->` 开头。
---

# FastAPI 示例项目开发规范

## 技术栈

- Python 3.11+
- FastAPI >= 0.110
- Pydantic v2 (>= 2.0)
- Uvicorn[standard] >= 0.29
- pytest >= 8.0, httpx >= 0.27, ruff >= 0.4

## 目录约定

```
app/                  # 主程序包
├── main.py           # FastAPI 应用入口
├── config.py         # 配置管理
├── dependencies.py   # 公共依赖注入
├── routers/          # 路由模块（按业务领域拆分）
├── models/           # Pydantic 数据模型
└── schemas/          # 请求/响应 Schema
tests/                # 测试（结构镜像 app/）
docs/                 # 项目文档
```

## 模块划分规范

- **routers/**: 每个文件一个 `APIRouter`，按业务领域划分（如 `users.py`、`items.py`）
- **models/**: 业务实体定义，用于内部数据传递
- **schemas/**: API 契约定义，与 models 分离。命名：`XxxRequest`、`XxxResponse`、`XxxCreate`、`XxxUpdate`
- **新增服务层**: 需要时添加 `app/services/`
- **新增数据层**: 需要时添加 `app/repositories/`

## 命名规范

- 文件名：小写蛇形（`user_management.py`）
- 类名：大驼峰（`UserResponse`）
- 函数/变量：小写蛇形（`get_current_user`）
- 常量：大写蛇形（`MAX_RETRY_COUNT`）
- 路由路径：小写连字符（`/api/v1/user-profiles`）
- API 版本前缀：`/api/v1/`

## 依赖管理

- 使用 `pyproject.toml`（PEP 621）管理依赖
- 生产依赖：`[project].dependencies`
- 开发依赖：`[project.optional-dependencies].dev`
- 安装开发环境：`pip install ".[dev]"`
- 详细方案见 `docs/dependencies.md`

## 测试规范

- 框架：pytest
- 测试文件命名：`test_<模块名>.py`
- 共享 fixtures 放 `tests/conftest.py`
- 使用 httpx.AsyncClient 或 TestClient 测试 API