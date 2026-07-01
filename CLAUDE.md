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

You are implementing a Jira subtask on branch `feature/oap-4409`.
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
  "branch": "feature/oap-4409",
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

## 启动命令

```bash
# 开发模式（热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式（多 worker）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 使用启动脚本（自动根据 APP_ENV 切换）
./run.sh
```

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `APP_HOST` | `0.0.0.0` | 服务监听地址 |
| `APP_PORT` | `8000` | 服务监听端口 |
| `APP_ENV` | `dev` | 运行环境（`dev` / `prod`） |
| `APP_WORKERS` | `4` | 生产环境 worker 进程数 |