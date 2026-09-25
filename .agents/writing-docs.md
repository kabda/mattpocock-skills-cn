<a id="writing-docs-pages"></a>

# 编写文档页

`engineering/` 和 `productivity/` 中每项技能，都在 `docs/<bucket>/<skill-name>.md` 有面向人的**文档页**。docs 树镜像 `skills/` 下这两个分类目录。页面发布到 `https://aihero.dev/skills-<skill-name>`；无论分类，URL 始终为 `skills-<skill-name>`，因此 docs 路径仅用于仓库组织。页面不是技能，也不是 `SKILL.md` 的副本。只有这两个分类正式收录，其他分类（`misc/`、`in-progress/`、`deprecated/`）不提供文档页。

大多数技能由**用户调用**：agent 绝不会替你触发，所以*你*就是必须记住其存在和适用时机的索引。这种记忆是**认知负荷**。文档页的职责是减轻负荷：围绕一个技能为一位读者建立方位感，让他们记得住、知道何时使用，并看见它在系统中的位置。所有页面共同构成分布式路由器，每页是一个节点。

正式技能新增、改名或行为变化时，就创建或重新同步文档页。改名也要移动文件（`docs/<bucket>/<old>.md` → `docs/<bucket>/<new>.md`），因为发布 URL 跟随名称；技能在 `engineering/` 与 `productivity/` 之间移动时，文档也移到相应目录。`misc/`、`in-progress/` 和 `deprecated/` 不配页面，因为这些分类都未正式收录。技能从它们*移出*、进入 `engineering/` 或 `productivity/` 时新增页面，反向移动则移除页面。

页面发布于 `aihero.dev`，所以**所有链接都用绝对 URL**，绝不用仓库相对路径。其他技能的链接指向 `https://aihero.dev/skills-<name>`；仓库内容的链接指向完整的 `https://github.com/mattpocock/skills/...` URL。仓库中可用的相对链接发布后会失效。

没有 H1。发布页面从 slug 获取标题。

<a id="page-structure"></a>

## 页面结构

填写下方模板，保持顺序。**固定框架**（`## What it does`、`## When to reach for it`、`## Where it fits`）出现在每页。`## Prerequisites` 和自由形式的主体章节只保留该技能确实需要的内容，删除其余部分。

四个章节让页面值得阅读：`What it does`、`When to reach for it`、`Common questions`、`It's working if`。前两个帮助读者定位，后两个让页面从概述技能转向回答读者自身情境。后两者各有下文规定的门槛；两者都未达标的页面应视为未完成，而非已完成但较短。

**页面不包含安装命令。** ai-hero 页面模板会在正文上方渲染安装组件（复制按钮、单技能命令、整套命令、更新命令行）。页面再写一遍，就会给读者重复展示同一命令，而且两份会漂移：每页手写的命令对照旁边组件都已过时。安装措辞属于网站，不属于页面。需要修改时，在 ai-hero 修改；规范措辞见[安装片段](./install-block.md)。

<page-template>

## What it does

一两段通俗文字。先用一句话说明技能职责，再说明**决定性约束**：使它区别于显然默认行为的那个事实（对 `to-spec` 而言：不重新访谈用户，而是综合已知内容）。用普通陈述句写，不要加“决定性约束：”或“关键点：”之类标签式旁白，这种公式读起来像填充物。这是页面最有价值的一行，绝不省略。

## When to reach for it

分两个环节说明如何以及何时使用技能，实际上两者几乎始终都要有：

- **调用模式。** 说明由你输入，还是由 agent 触发。用户调用技能：“输入 `/<name>` 调用，agent 不会自行使用。”模型调用技能：“输入 `/<name>`，或由 agent 在任务适合时自动使用。”
- **触发边界。** 索引条目：“在……时使用。”容易与相邻技能混淆时，加上另一半：“如果是 <X>，改用 [<sibling>](https://aihero.dev/skills-<sibling>)。”

## Prerequisites

可选：仅在技能必须先具备某些条件才能工作时保留，否则整个标题都省略。涵盖：**写入的工作空间**（`grill-with-docs` 等有状态技能会写 `CONTEXT.md` 和 ADR；`teach` 构建整个目录，因此说明写什么、写在哪里）、**事先设置**（`triage`/`to-spec`/`to-tickets` 需要 `setup-matt-pocock-skills` 已配置 issue 跟踪器），或**仓库专用工具**。到处都能运行的无状态技能没有前置条件，删除此节。

## <free-form middle>

一到三个短章节，用技能*自己的词汇*把它讲明白。标题按技能选择：运行的循环、产出的文件、作出的分支选择、消除的一个反模式。没有规定标题，因为技能差异太大。

唯一不可妥协的要求：**呈现技能的引导词/决定性观念**（`tight` 反馈循环、`deep module`、用一次性代码回答问题、red-green）。这有双重收益：读者既知道技能*是什么*，也学到以后*想到要用它*时所依托的词。

## Common questions

读者确实会问的该技能问题，每个加粗，答案紧接其下。不要子标题。

观察到的问题永远优于凭空编造的问题，因此落笔前先寻找：

- **Wiki。** 如果本机有 `~/repos/matt/personal-wiki`，它就是最丰富的来源。`wiki/audience/` 围绕受众想要什么、讨论什么，以及**对什么感到困惑**组织：先读 `wiki/index.md` 获取页面索引，再读与技能相关的页面。每页都有 `sources:` 链接回原始 X、Discord、GitHub 和邮件讨论；wiki 是二手来源，因此引用提问者原话，而非 wiki 的摘要。目录不存在时跳过此项。
- **本仓库 issue。** `gh issue list --repo mattpocock/skills --search "<skill-name>" --state all`。被提出两次的问题，就是页面欠读者一个答案的问题。
- **`CHANGELOG.md`。** 任何改名、移动或行为变化，都会产生页面必须回答的“它去哪了？”

寻找结果不多时，也可加入读者显然会问的问题，但**数量必须忠实于证据**。讨论充分的技能可以有六个；冷门技能可能只有一两个，甚至没有。为了追平丰富页面而填充冷门技能，会让章节塞满没人问的问题，而编造的问题教不了读者什么。

按出现频率排序，最突出的问题放前面；属实时就说出不讨好的事实：追问会话很长，通常说明范围太大；让模型写自己的技能，会得到冗长结果。没有值得回答的内容时，省略标题。

## It's working if

用几个要点说明技能有效工作时，读者会看到什么。每条的门槛是：无需打开 `SKILL.md` 就能检查，是自己工作中或眼前执行轨迹中的信号。“文档越好越短”达标；“库章节与 `template.sh` 逐字节相同”则是披着本节外衣的技能内部合规检查。迹象清晰时保留，始终含糊时省略标题。

## Where it fits

始终保留。用一两句话说明技能在系统中的位置：

- **角色。** 明确命名：**链条步骤**（`grill-with-docs → to-spec → to-tickets → implement → code-review`）、**运行一次的设置**（`setup-matt-pocock-skills`）、**定期维护**（`improve-codebase-architecture`，“每隔几天”），或**随时可用的独立技能**（`diagnosing-bugs`、`prototype`、`handoff`）。独立技能的地图只需一句诚实说明，远比省略本节好。
- **相邻技能。** 说明重要的一两项相邻技能，各附原因，并使用绝对链接。
- **地图。** 指向覆盖整套技能的路由器 [ask-matt](https://aihero.dev/skills-ask-matt)，让本页保持为节点，而无需重画整张图。

</page-template>

<a id="conventions"></a>

## 约定

- 解释**为什么**，而非流程。页面帮助读者定位技能，绝不复刻 `SKILL.md` 的步骤或大段模板；选择工具的人不需要操作手册。
- **绝不点名作者。** 页面是技术文档，不是记录谁说过什么。“Matt 说”“Matt 本人的回答”“他的立场是”、引用回复，都删掉。寻找问题得到的发现值得保留，归因不值得。把实质内容写成关于技能的普通断言（“修复方式是一条直接指令：……”“区别取决于会话数量”），去掉叙事框架。读者在决定是否使用工具；观点无论归谁，分量都相同，而署名观点会随立场变化立刻过时。引用*用户*仍可：“一位用户报告……”是技能实际表现的证据，保持匿名。
- 使用技能的**引导词**（_seam_、_deep module_、_tracer bullet_），让页面与技能说同一种语言。
- **[AI Coding Dictionary](https://www.aihero.dev/ai-coding-dictionary) 已有的术语就使用其形式，并在页面首次使用时链接。** 该词典是 AI 编码的统一词汇：_context window_、_subagent_、_harness_、_primary source_、_agent mode_。优先用它的词，不另造同义词。每个术语首次出现时链接到 `https://www.aihero.dev/ai-coding-dictionary/<slug>`（slug 为小写术语，非字母数字换为连字符：_context window_ → `context-window`），后续不再链接。仅在使用词典含义时链接：领域 *model*、背景 *context* 或认证 *token* 是恰好同形的其他词。标题、代码 span 和已有链接内绝不再加链接；表示本仓库技能名而非概念的词也绝不链接。完整术语表优先读本机 `~/repos/ai/ai-coding-dictionary/dictionary/`（如存在，每个术语一个文件，文件名*就是*术语），否则读 [mattpocock/dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding)，它无论如何都是权威来源。
- **分支放进表格或列表，绝不写成段落。** 页面呈现选择时（技能可产出的两类文件、四种触发情境、边界处五种选项），读者是在扫描匹配自己情况的一行。段落迫使他们读完才能找到。简短 Markdown 表格（左列条件，右列做法）或项目列表能让人一眼找到。所有分支出现处都适用，最常见于 `## When to reach for it` 和自由形式的中间部分。
- 保持页面自身低负荷。它是*关于*低认知负荷技能的文档；多余装饰（多余标题、重复链接）恰是它所反对的东西。

<a id="done-when"></a>

## 完成条件

- 页面位于 `docs/<bucket>/<name>.md`，改名或移动分类后没有旧页面残留。
- 页面不带源码链接，也不自行写安装命令。
- `## What it does` 以普通文字说明决定性约束，不加标签式旁白。
- 页面不点名或引用作者，每条论断独立成立。
- `## When to reach for it` 说明调用模式和触发边界。
- `## Where it fits` 说明角色，并链接到 `ask-matt`。
- 有前置条件（工作空间、事先设置、工具）就说明；没有就不设该节。
- 中间部分呈现引导词。
- 页面使用的每个 AI Coding Dictionary 术语都采用词典写法，并且仅首次出现链接到词条。
- 每个多路分支都用表格或列表，而非需要完整阅读的段落。
- 已寻找真实问题（wiki、issue、changelog）；`## Common questions` 的篇幅由结果决定，不为追平更丰富技能的页面而填充。
- `## It's working if` 每个要点都无需打开 `SKILL.md` 即可检查。
- 章节按模板顺序排列。
- 每个链接都是绝对链接，且都可解析。
