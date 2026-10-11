---
name: handoff
description: 将当前对话压缩成一份交接文档，供另一个 agent 接手。
argument-hint: "下一场会话将用于什么？"
disable-model-invocation: true
---

编写总结当前对话的交接文档，使新 agent 能继续工作。保存在用户操作系统临时目录（`$TMPDIR`，否则 `/tmp`；Windows 使用 `%TEMP%`），而非当前工作空间。

在文档中加入 "suggested skills"（建议使用的技能）章节，列出下一位 agent 应当通过 Skill 工具调用的技能。

不要重复其他交付物（规格说明、计划、ADR、issue、提交、diff）中已经记录的内容。改为通过路径或 URL 引用。

隐去 API 密钥、密码或个人身份信息等任何敏感信息。

如果用户传入参数，将其视为对下一场会话重点的描述，并据此调整文档。
