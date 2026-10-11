---
name: claude-handoff
description: 把当前对话交接给一个全新的后台 agent，立即接手工作。
argument-hint: "下一会话将用于什么？"
disable-model-invocation: true
---

编写当前对话的交接摘要，使新 agent 能继续工作。保存到用户操作系统的临时目录，再以文件内容为提示词启动后台 agent：`claude --bg --name "<descriptive name>" -- "$(cat <summary file>)"`。通过文件传入可避免 shell 执行摘要中的反引号或展开 `$`。它在当前工作目录启动，立即返回；用户通过 `claude agents` 管理。

始终用 `-n`/`--name` 传入描述性名称（例如 `--name "Fix login bug"`）；它决定任务列表、会话选择器和终端标题中显示的名称。

在摘要中加入 "suggested skills" 章节，列出下一 agent 应通过 Skill 工具调用的技能。

不要重复已在其他产物（规格说明、计划、ADR、issue、commit、diff）中记录的内容，改用路径或 URL 引用。

隐去 API keys、密码、个人身份信息等敏感内容，因为摘要会成为 agent 的提示词。

如果用户传入参数，将其视为下一会话重点的描述，并据此调整摘要。
