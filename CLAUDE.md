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

You are implementing a Jira subtask on branch `feature/oap-4406`.
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
  "branch": "feature/oap-4406",
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

# DevBox Agent

## API 约定

### 路由规范

- 基础路径前缀：`/api/v1`
- 路径使用小写连字符：`/api/v1/todo-items`
- 资源名使用复数形式：`/todos` 而非 `/todo`
- 路径参数使用 UUID：`/todos/{id}`

### 错误响应格式

所有错误统一返回以下 JSON 结构：

```json
{
  "code": "ERROR_CODE",
  "message": "人类可读的错误描述"
}
```

错误码命名使用大写蛇形（`NOT_FOUND`、`VALIDATION_ERROR`、`BAD_REQUEST`）。

### HTTP 状态码规范

| 状态码 | 用途 |
|--------|------|
| 200 | 成功（查询、更新、删除） |
| 201 | 资源创建成功 |
| 400 | 请求格式错误（如非法 JSON） |
| 404 | 资源不存在 |
| 422 | 请求体/参数校验失败 |

### 分页规范

列表接口统一使用以下分页参数：

- `page`：页码，默认 1，最小 1
- `size`：每页条数，默认 20，最小 1，最大 100

分页响应结构：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "size": 20,
  "pages": 0
}
```

### Schema 命名规范

| 用途 | 命名模式 | 示例 |
|------|----------|------|
| 创建请求 | `XxxCreate` | `TodoCreate` |
| 更新请求 | `XxxUpdate` | `TodoUpdate` |
| 响应 | `XxxResponse` | `TodoResponse` |
| 列表响应 | `XxxListResponse` | `TodoListResponse` |

### 时间格式

- 所有时间字段使用 UTC 时区
- 序列化格式：ISO 8601（`2026-07-01T10:00:00Z`）