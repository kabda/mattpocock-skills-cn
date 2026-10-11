<a id="scope"></a>

# 范围

本仓库收录我每天使用的技能，并经过筛选维护：欢迎提出想法，每项想法都按下方门槛评估。Issue 用于跟踪技能变更，问题和讨论请前往 [GitHub Discussions](https://github.com/mattpocock/skills/discussions)。

<a id="the-bar"></a>

## 门槛

想法或反馈 issue 只有同时满足**两项**要求，才会保持开放：

1. **观察到的失败。** 描述真实会话中发生的错误：运行了什么、技能做了什么、预期是什么。假想改进（“如果……会更好”）不满足这一项。
2. **符合理念。** 不属于 [`.out-of-scope/`](./.out-of-scope/) 或此前已拒绝的情形，也不是配置选项、harness 专用分支或迎合个人工作流的调整。这些应放在自己的 `CLAUDE.md` / `AGENTS.md` 或 fork 中（skills.sh 提供可编辑副本）。

改动大小无关：修改一个词和完整重写都面对同一门槛。表情回应和 +1 评论不计入判断。

<a id="by-bucket"></a>

## 按分类

- **`engineering/`、`productivity/`、`in-progress/`**：采用上面的门槛。
- **`misc/`**：已冻结、不再维护，所有 issue 都会关闭。参见 [`frozen-misc-skills.md`](./.out-of-scope/frozen-misc-skills.md)。
- **新技能**：建议和贡献会关闭。如果行为能由现有技能组合，就不另建技能。参见 [`new-skills.md`](./.out-of-scope/new-skills.md)。

<a id="already-decided"></a>

## 已作出的决策

[`.out-of-scope/`](./.out-of-scope/) 中每个文件记录一个被拒绝的概念及原因，提交前请阅读：

- [`frozen-misc-skills.md`](./.out-of-scope/frozen-misc-skills.md)
- [`harness-name-collisions.md`](./.out-of-scope/harness-name-collisions.md)
- [`mainstream-issue-trackers-only.md`](./.out-of-scope/mainstream-issue-trackers-only.md)
- [`native-question-tool.md`](./.out-of-scope/native-question-tool.md)
- [`new-skills.md`](./.out-of-scope/new-skills.md)
- [`question-limits.md`](./.out-of-scope/question-limits.md)
- [`setup-skill-verify-mode.md`](./.out-of-scope/setup-skill-verify-mode.md)
- [`subagent-recursion.md`](./.out-of-scope/subagent-recursion.md)

<a id="unclear-issues"></a>

## 不明确的 issue

无法按门槛评估的 issue 会收到一轮问题并标记 `needs-info`。报告者 14 天未回复，就会关闭。被拒绝的 issue 以 “not planned” 关闭。
