---
"mattpocock-skills": patch
---

阻止技能尝试通过 Skill 工具调用用户调用技能：修复 `to-spec`、`wayfinder`、`to-tickets`、`triage`、`code-review` 和 `diagnosing-bugs` 中违反 `.agents/invocation.md`“其他技能都不能调用它”不变量的跨技能引用。

- `to-spec`、`wayfinder`、`to-tickets`、`triage` 和 `code-review` 各有前置条件（“……否则运行 `/setup-matt-pocock-skills`”），PR #878 将其改成了字面的 `Call the Skill tool with "setup-matt-pocock-skills"` 指令。`setup-matt-pocock-skills` 由用户调用，因此这些技能无论由用户还是模型调用，都不能调用它。五处全部改为指示 agent 告诉人去运行。
- `diagnosing-bugs` 的 Phase 6 复盘同样交接给 `improve-codebase-architecture`（也是用户调用），却来自自主且往往无人值守的修 bug 流程，没有人在环发现调用失败。由于实践中很少触发，直接移除了交接，而非弱化措辞。Phase 6 现在仅为“清理”；机械检查清单未变。
- 在 `.agents/invocation.md` 的“技能间依赖”一节增加例外段落：`Call the Skill tool with "name"` 约定只适用于指定技能由模型调用的情况。PR #878 引入该节时，没有与前八行已说明的用户调用/模型调用不变量协调；这个缺口很大程度上解释了 bug 为何扩散到六个调用点，而非一个。

修复 #453。
