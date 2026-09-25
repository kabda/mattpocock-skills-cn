---
name: git-guardrails-claude-code
description: 设置 Claude Code hooks，在执行前阻止危险 Git 命令（push、reset --hard、clean、branch -D 等）。用户想防止破坏性 Git 操作、添加 Git 安全 hooks，或在 Claude Code 中阻止 git push/reset 时使用。
---

<a id="setup-git-guardrails"></a>

# 设置 Git 护栏

设置一个 PreToolUse hook，在 Claude 执行危险 Git 命令前拦截并阻止它们。

<a id="what-gets-blocked"></a>

## 阻止哪些命令

- `git push`（所有形式，包括 `--force`）
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

被阻止时，Claude 会看到消息，告知它没有使用这些命令的权限。

<a id="steps"></a>

## 步骤

<a id="1-ask-scope"></a>

### 1. 询问范围

询问用户：仅为**本项目**（`.claude/settings.json`）安装，还是为**所有项目**（`~/.claude/settings.json`）安装？

<a id="2-copy-the-hook-script"></a>

### 2. 复制 hook 脚本

随附脚本位于：[scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

根据范围复制到目标位置：

- **项目**：`.claude/hooks/block-dangerous-git.sh`
- **全局**：`~/.claude/hooks/block-dangerous-git.sh`

用 `chmod +x` 赋予可执行权限。

<a id="3-add-hook-to-settings"></a>

### 3. 把 hook 添加到设置

添加到相应设置文件：

**项目**（`.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**全局**（`~/.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

设置文件已存在时，将 hook 合并到现有 `hooks.PreToolUse` 数组中。不要覆盖其他设置。

<a id="4-ask-about-customization"></a>

### 4. 询问自定义需求

询问用户是否希望向拦截列表添加或移除模式，相应编辑复制后的脚本。

<a id="5-verify"></a>

### 5. 验证

运行快速测试：

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

应以退出码 2 结束，并向 stderr 输出 BLOCKED 消息。
