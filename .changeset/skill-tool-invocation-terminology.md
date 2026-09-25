---
"mattpocock-skills": patch
---

在 `code-review`、`diagnosing-bugs`、`grill-with-docs`、`grill-me`、`improve-codebase-architecture`、`tdd`、`to-spec`、`to-tickets`、`triage` 和 `wayfinder` 中，将跨技能调用统一为明确的“调用 Skill 工具”指令，替代单纯 `/skill` 形式的文字。

- 仅在文字中点名另一技能（“运行 `/grilling` 技能”），不能可靠触发加载。这是 `grill-with-docs` 最常报告问题背后已记录的缺陷。直接点名工具（`Call the Skill tool with "grilling"`）旨在提高命中率。去掉开头的 `/` 反而更不依赖 harness：不再假定 Claude Code 的触发语法。
- 某步骤需要多项技能时，现在明确写成多次调用（“调用 Skill 工具两次，分别加载 `grilling` 和 `domain-modeling`”），而不是一次传两个名称。
- 在 `.agents/invocation.md` 记录约定，供未来技能遵循。
