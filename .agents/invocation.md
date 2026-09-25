<a id="model-invoked-vs-user-invoked"></a>

# 模型调用与用户调用

本仓库每个 `SKILL.md` 都是一项技能。区分它们的唯一维度是**调用**，即谁能访问：

- **用户调用**：**只有人输入名称**才能访问。在 frontmatter 设置 `disable-model-invocation: true`（Claude Code），在 `agents/openai.yaml` 设置 `policy.allow_implicit_invocation: false`（Codex）。`description` **面向人**：供浏览 slash command 的人阅读的一行摘要。移除触发条件列表（“当用户说……时使用”）。
- **模型调用**：**模型或用户**均可访问。这是默认方式：省略 `disable-model-invocation` 和 `agents/openai.yaml` 中的 `policy` 块。`description` **面向模型**，保留丰富的触发措辞（“用户想……、提及……、要求……时使用”），让自动调用生效。判断技能是否应保持模型调用的标准是：*模型自主使用它，是否会有帮助？*（复用是提取技能的理由，不是这个判据。）

各 harness 以自己的方式把用户调用技能排除在模型可访问范围外，所以只有人能触发，其他技能都不能。用户调用技能可以调用模型调用技能，却永远不能调用另一项用户调用技能。

每项技能还在 `SKILL.md` 旁附有 `agents/openai.yaml`，保存 Codex UI 元数据：用于技能选择器的 `interface.display_name` 和 `interface.short_description`，以及用户调用技能中与 `disable-model-invocation` 配对的 `policy.allow_implicit_invocation: false`。两者保持同步：技能要么在两个 harness 中都由用户调用，要么都不是。

分类 `README.md` 和顶层 `README.md` 按**用户调用**与**模型调用**分组。

<a id="dependencies-between-them"></a>

## 技能间依赖

依赖以明确指令表达：**调用 Skill 工具**加载指定技能（`Call the Skill tool with "grilling"`），不使用跨层的 `../other-skill/FILE.md` 引用，也不只留一个 `/skill` 形式的提及让模型猜。点名工具才能让它运行：大多数 harness 把技能调用作为模型可调用的工具，明确写出来，比在文字里丢一个 `/name` 并希望它被读作命令命中率更高。去掉开头的 `/` 反而更中立，不偏向某个 harness：单独技能名不假定属于哪个 harness 的触发语法。共享参考文档放在拥有它的技能内部；其他技能通过调用 Skill 工具加载该技能来访问，而非跨目录链接。

这里指**实际操作**指令：技能自身步骤要求 agent 现在运行另一项技能。只列出技能供人选择的路由文字（`ask-matt`、分类 `README.md`）不调用任何东西，因此保留 `/skill` 形式作为普通标签。

Skill 工具每次调用只接受一项技能。某步骤需要两项技能，就调用两次，不是一次传两个名字；明确写出（`Call the Skill tool twice, for "grilling" and "domain-modeling"`），不要写“用 X 和 Y 调用它”，那会被理解成一次调用同时接受两者。

整套约定只适用于指定技能为**模型调用**的情况。用户调用技能绝不能如此访问，没有例外：根据上述不变量，其他技能都不能调用它，包括把名称传给 Skill 工具。步骤的前置条件是用户调用技能时（例如 `setup-matt-pocock-skills`），应写成让人操作的指示：“告诉用户运行 `/setup-matt-pocock-skills`”，绝不写成 Skill 工具调用。

<a id="passive-vs-active-domain-work"></a>

## 被动与主动领域工作

仅为词汇而*阅读* `CONTEXT.md`，用一行文字指针即可，不是 `domain-modeling` 技能。只有主动构建/打磨的方法（质疑术语、边界场景、编写 ADR、同步更新 `CONTEXT.md`）才属于 `domain-modeling`。
