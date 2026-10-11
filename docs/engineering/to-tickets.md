<a id="what-it-does"></a>

## 它能做什么

`to-tickets` 将计划、[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)或当前对话拆分为 issue 跟踪器中的一组**[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)**。每张工单都声明其**阻塞关系**：哪些其他工单必须完成，它才能开始。

每张工单都是一枚**曳光弹**：一条贯穿变更每一层（schema、API、UI、测试）的狭窄但完整的路径，落地后就能独立演示。这个约束使它区别于最直观的拆分方式，即每次切一层，最后再集成。它还会把每张工单控制在一个全新[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)能容纳的大小，因为接手工单的将是一场从未见过规格说明的[会话](https://www.aihero.dev/ai-coding-dictionary/session)。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/to-tickets` 调用。[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。

| 你所处的阶段 | 运行什么 |
| --- | --- |
| 已有规格说明 issue，构建跨多场会话 | `/to-tickets` 或 `/to-tickets #<spec_issue>` |
| 计划只在对话中，从未写成文档 | `/to-tickets` 直接读取对话，不需要规格说明 |
| 整项变更能放进一个上下文窗口 | [implement](https://aihero.dev/skills-implement)，跳过工单 |
| 尚未决定任何事情 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，然后 [to-spec](https://aihero.dev/skills-to-spec) |
| 一份 [wayfinder](https://aihero.dev/skills-wayfinder) 地图已经清空待决项 | 先用 [to-spec](https://aihero.dev/skills-to-spec) 收束地图，再运行 `/to-tickets` |

`to-tickets` 产出的工单从设计上就已准备好交给 agent。不要再对它们运行 [triage](https://aihero.dev/skills-triage)。分流用于从他人那里接收的工作。

<a id="prerequisites"></a>

## 前置条件

`to-tickets` 会发布到跟踪器，因此必须由 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 为仓库配置跟踪器及分流标签词汇。两种形式都可以：GitHub 或 Linear 这样的真实跟踪器，或 `.scratch/` 下的本地 Markdown 文件，后者开箱即用。

<a id="tracer-bullets-not-layers"></a>

## 曳光弹式切片，而非按层拆分

**横向**切片交付变更中的一层。只有每层都落地，功能才能工作，而且每张工单的验收标准都不得不涉及另一张工单负责的工作。**纵向**切片（曳光弹）一次交付贯穿所有层的一条窄路径，因此可独立验证，并拥有它所考核的全部内容。

这是人们最常违反的规则，后果已有充分记录。一个团队运行了按层拆分的 26 张工单栈（语料库、生产者、聚合器、选择器），每关闭一张工单大约需要二十次 agent 运行，其中约四分之三是返工。他们自己的复盘将每一类失败都追溯到横向切片，而不是实现。

发布前会发生两件事。`to-tickets` 寻找预先重构的机会（“先让变更变得容易，再做这个容易的变更”原则），将这类工作排在最前。然后以编号列表展示拆分方案，并向你核对：粒度是否合适、阻塞关系是否真实、是否需要合并或拆分。批准之前，任何内容都不会进入跟踪器；核对环节正是提出异议的时机。

<a id="blocking-edges"></a>

## 阻塞关系

关系就是这个交付物的重点。根据跟踪器不同，它有两种形式：

| 跟踪器 | 关系存放在哪里 | 如何处理 |
| --- | --- | --- |
| 本地 Markdown | `.scratch/<feature>/issues/<NN>-<slug>.md` 下每张工单一个文件，以文字记录，按阻塞项在前编号 | 手动从上到下处理 |
| 真实跟踪器（GitHub、Linear） | 原生阻塞链接，或跟踪器支持的子 issue | 所有阻塞项均完成的工单位于**前沿**，可领取 |

无论哪种形式，关系都存在于工单中。载体只决定是否有工具能据此并行执行。`to-tickets` 产出交付物；执行它（逐场会话，或一组 agent）是你的工作，不是技能的职责。

<a id="the-wide-refactor-exception"></a>

## 大范围重构的例外

有一种情况会打破曳光弹规则。**大范围重构**是一项机械性变更（重命名列、改变共享符号的类型），其**影响范围**扩散到整个代码库，一次编辑就破坏成千上万个调用点，没有纵向切片能以 Green 状态落地。

`to-tickets` 会改用 **expand–contract（扩展－收缩）** 排序：

- **Expand（扩展）**：在旧形式旁边添加新形式，让一切保持正常。
- **Migrate（迁移）**：按影响范围分批迁移调用点（按包、按目录），每批一张工单，均被扩展工单阻塞。旧形式仍在，所以 CI 保持 Green。
- **Contract（收缩）**：没有调用方残留后删除旧形式，该工单被所有迁移批次阻塞。

如果连各批次也无法独立保持 Green，就共享一个集成分支，并共同阻塞最后的“集成并验证”工单。只在最后这一步承诺 Green。

<a id="common-questions"></a>

## 常见问题

**三行改动，它却生成了十二张工单。**
过度拆分是本技能被报告最多的使用障碍，各类使用者的经历一致：[模型](https://www.aihero.dev/ai-coding-dictionary/model)默认拆成原子单元，丢掉了赋予它们意义的分组。核对步骤正是为此而设：让它合并，它就会合并。更深层的答案是工单有规模下限：如果整项变更能放进一个上下文窗口，就根本不需要本技能。直接进入 [implement](https://aihero.dev/skills-implement)。

**生成的工单每层一张：所有 schema 放一张，所有 API 放另一张。**
这正是纵向切片规则要防止的失败，而技能有时仍会这样做。在核对步骤中，对每张工单问一个问题：完成后能演示什么？没有答案的工单就是横向切片。有人因此在每张工单中增加“演示路径”一行，并报告这能推动模型采用纵向拆分。

**GitHub 上的工单没有创建为规格说明 issue 的子 issue。**
多个模型、十多轮运行都报告过，[issue #554 的记录最完整](https://github.com/mattpocock/skills/issues/554)。现已修复：`to-tickets` 把工单设为来源 issue 的子 issue，GitHub 模板给出命令（`gh issue create --parent <n>`，`gh` 2.94+）。重新运行 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills)，刷新旧 `docs/agents/issue-tracker.md`。

**"Blocked by" 被写进 issue 正文，而没有建立真正的阻塞链接。**
这是同类问题，[issue #513 曾报告](https://github.com/mattpocock/skills/issues/513)，agent 甚至断言 GitHub 没有原生阻塞关系。实际上有：`gh issue create --blocked-by 12,15`。技能先发布阻塞项，因此创建时已有编号。正文文字只是无原生边的跟踪器的回退方案，不是默认。模板现在会在采用原生边时省略 `## Blocked by`。

**本地工单存在哪里？v1.1 说明说是根目录的 `tickets.md`。**
确实如此，那是个 bug：多个 agent 并行写入单个共享文件时也会竞争。现在本地模式按依赖顺序，在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md` 下每张工单写一个文件，与本地跟踪器模板原本描述的布局一致。`NN` 前缀是真正的工单 ID，因此可以用 `/implement 03`，无需重输长标题。

**它尝试读取规格说明时一直被截断。**
特别大的规格说明可能超出跟踪器 issue 能完整返回的范围，又没有本地副本作为后备，于是 agent 不断消耗[工具调用](https://www.aihero.dev/ai-coding-dictionary/tool-call)重新获取片段，却始终读不到结尾。不要在 `/to-spec` 与 `/to-tickets` 之间[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)或[压缩](https://www.aihero.dev/ai-coding-dictionary/compaction)。在同一个上下文窗口中运行，就根本不需要重新获取规格说明。

**验收标准没有考核任何东西：有些在工作开始前就已经通过。**
模板要求提供标准，却没说明它们是否可能失败，因此会出现这种情况。三种形式反复出现：在基准提交上已经成立的标准、只能由另一张工单负责的工作满足的标准，以及只是复述请求而不是从交付物推导出来的标准。纵向切片可以防止大多数问题（交付此前不存在行为的切片，在基准提交上必然是 Red），但仍值得手动检查。对每项标准，说明什么观察结果会证明它不成立，并确认它在实现者开始工作的提交上失败。

**工单已经发布，实际该怎么运行？**
技能止步于交付物，没有自动分派模式。分派是手动的：查看看板，数一数没有未关闭阻塞项的工单，然后打开对应数量的 agent 会话。每个新上下文一张工单，工单之间清空。注意，无论 GitHub 还是本地 Markdown，[implement](https://aihero.dev/skills-implement) 完成后都不会可靠地关闭工单或勾选条目，因此工单状态需要你来更新。

<a id="its-working-if"></a>

## 如何判断它有效

- 每张工单都能回答“完成后能演示什么？”，答案是行为，而不是某一层。
- 发布任何内容之前，先向你返回编号列表，每项都有 "Blocked by" 一行。
- 最前面的工单没有阻塞项，可以立即开始。
- 除了原型产出的片段，工单正文中没有文件路径或行号。
- 每张工单读起来都像是一场新会话能够在你不在场时完成的工作。
- 如果发现需要预先重构，它会排在顺序最前，而不是混进功能工单。

<a id="where-it-fits"></a>

## 它在流程中的位置

`to-tickets` 是主构建流程中的一步：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

上游 [to-spec](https://aihero.dev/skills-to-spec) 提供已确定的规格说明供拆分，两步应留在同一上下文窗口，中途不清空。下游 [implement](https://aihero.dev/skills-implement) 在各自新会话实现一张工单，以 [tdd](https://aihero.dev/skills-tdd) 驱动测试，用 [code-review](https://aihero.dev/skills-code-review) 收尾。[implement-spec](https://aihero.dev/skills-implement-spec) 是另一条下游路线，把同样的阻塞边读取为任务图，在一个集成分支并行实现就绪工单。不确定流程时，由 [ask-matt](https://aihero.dev/skills-ask-matt) 路由。
