<a id="what-it-does"></a>

## 它能做什么

`to-spec` 将刚刚进行的对话转成一份**[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)**，并以单个 issue 发布到你的 issue 跟踪器。

它不会访谈你。使用它时，决策已经完成，因此它会综合整理已知内容（来自对话、代码库、`CONTEXT.md` 和 ADR），而不是开启新一轮提问。规格说明是已经作出决策的记录，不是作出新决策的地方。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/to-spec` 调用它；[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。

当构建规模大到一场 agent [会话](https://www.aihero.dev/ai-coding-dictionary/session)容纳不下，必须跨多场会话继续时使用。这就是全部触发条件：

| 你所处的阶段 | 运行什么 |
| --- | --- |
| 尚未作出任何决策 | 先用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 已经决定，工作能放进一个[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window) | [implement](https://aihero.dev/skills-implement)：跳过规格说明 |
| 已经决定，工作横跨多场会话 | `/to-spec`，然后 [to-tickets](https://aihero.dev/skills-to-tickets) |
| 一份 [wayfinder](https://aihero.dev/skills-wayfinder) 地图已经清空待决项 | `/to-spec #<map_issue>` |

<a id="prerequisites"></a>

## 前置条件

`to-spec` 会将规格说明发布为 issue，因此必须先由 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 为仓库配置跟踪器及分流标签词汇。两种形式都可以：GitHub 这样的真实跟踪器，或 `.scratch/` 下的本地 Markdown 文件，后者开箱即用。

<a id="the-spec-is-a-decision-record"></a>

## 规格说明是决策记录

规格说明存在，是因为上下文窗口会结束。[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)时确定的一切（方案形态、争论后作出的选择、有意拒绝的事项）都位于一段即将被清空的对话中。规格说明就是在这之后保留下来的内容。

因此，它不验证任何事，也不决定任何事。它用项目自身的词汇记录已确定的内容，让新会话无需你重新解释就能接手。规格说明中的任何断言，只要你从未真正说过，就是缺陷。

<a id="seams-before-prose"></a>

## 先定 seam，再写正文

写下任何文字之前，`to-spec` 会勾勒功能的测试 **seam**，并与你核对。它优先选择已有 seam，而不是新建，且尽可能选择高层 seam：一次变更的理想数量是一个。

这些约定的 seam 随后会传递下去。[tdd](https://aihero.dev/skills-tdd) 只在事先约定的 seam 上工作，[code-review](https://aihero.dev/skills-code-review) 则对照规格说明审查 diff，因此未经任何人同意的 seam 会成为审查发现。这种约束是间接的：它通过本文档传递。这也正是应当在这里认真讨论 seam，而不是推迟到实现时的原因。

<a id="common-questions"></a>

## 常见问题

**`/to-prd` 去哪了？**
就是本技能，在 v1.1 中改名。如今 "Spec" 是贯穿流程的统一术语，旧的 `to-prd` slug 已失效；请按新名称重新安装。替代旧词汇的是*规格说明*和*工单*这一对概念：规格说明是目标及确定目标的决策，[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)是到达目标的执行步骤。如果改变方向，删除未完成工单，保留规格说明。

**为什么规格说明会打上 `ready-for-agent` 标签？我不想让 agent 直接照它实现。**
标签表示“无需进一步分流”：文档已经足够完整，可以让 agent 据此工作。它是输入分类，不是工作指令。但如果你运行会轮询 `ready-for-agent` 的 [AFK](https://www.aihero.dev/ai-coding-dictionary/afk) agent，它们看不出这种区别，会试图一次实现整份规格说明，而不是领取工单切片。这是本技能被报告最多的问题。在行为改变之前，请在 AFK agent 的提示词中明确排除父级规格说明，或在 `/to-tickets` 运行后去掉该标签。

**为什么不从追问直接进入 `/to-tickets`，跳过规格说明？**
很多时候确实应该跳过；只有跨多场会话的工作，规格说明这一步才有价值。价值在于工单是可丢弃的，规格说明不是：每张工单大小适合一个全新上下文窗口，会被删除或关闭，而规格说明保留为背后推理的唯一存放处。对于单场会话的变更，这毫无收益，却多付出了一次综合整理的代价，[模型](https://www.aihero.dev/ai-coding-dictionary/model)还可能在这一步偏移。直接走追问 → `/implement`。

**刚完成一份 wayfinder 地图，该传给它什么？**
主地图 issue：`/to-spec #<map_issue>`，而不是单独的决策工单。[wayfinder](https://aihero.dev/skills-wayfinder) 产出的是散布在地图上的决策，而不是交付物；`to-spec` 将这些决策收束成一份可构建的文档。直接把地图交给 `/implement`，就丢掉了这次收束。

**规格说明是给我审阅的，还是只给 agent 看？**
主要给 agent，所以读起来也是如此：完整、密集、引用很多。最值得你关注的是 seam 和范围之外章节，因为这两处的错误决策最容易及早发现，也最难承受事后才发现的代价。人们确实抱怨从头到尾阅读负担很重，而技能没有摘要模式；坦诚的回答是，如果规格说明让你意外，问题在追问太浅，而不是规格说明太长。

**工单开始执行后，应当冻结规格说明，还是让 agent 重写？**
没有任何机制保持同步，所以它实际是当时认知的快照；实现第一次带来新发现时，它就过时了。工作交付后，将其视为可丢弃材料。应当比它存活更久的交付物是 `CONTEXT.md` 和 ADR；如果实现中学到的内容值得长期保留，应当放在那里，而不是编辑规格说明。

**我的工作是重构或模块边界，而不是功能，这个模板适用吗？**
适用性较差，这是已知限制。模板高度依赖用户故事，不适合架构工作：真正涉及接口和不变量的决策，最后会被包装成没人要求过的故事。应当更多依靠实现决策和测试决策章节，让持久的架构选择通过 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 形成 ADR，而不是强迫规格说明承载它们。

**它会检查跟踪器中的相关工作，或引用自己遵守的 ADR 吗？**
两者都不会。它会读取并遵守所涉及区域的 ADR，但不链接它们；起草前也不会搜索跟踪器中重叠的 issue，因此规格说明可能悄悄重复别人已登记的工作。如果该区域工作活跃，先自行搜索跟踪器。

**`/to-tickets` 读不到我的规格说明：一直被截断。**
特别大的规格说明可能超出跟踪器 issue 能完整返回的范围，而且没有本地副本作为后备。解决办法是管理好上下文：不要在 `/to-spec` 与 `/to-tickets` 之间[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)或[压缩](https://www.aihero.dev/ai-coding-dictionary/compaction)。在同一个窗口中运行，就根本不需要重新获取规格说明。

<a id="its-working-if"></a>

## 如何判断它有效

- 它开始写作，而不是发起新一轮提问。
- 写作前先把 seam 交给你确认，并尽可能减少数量。
- 产出使用项目自己的名词，而不是通用产品管理套话。
- 其中每项决策，你都记得自己曾经作出。没有为了填满章节而编造内容。
- 范围之外章节包含真实事项：你拒绝的内容，往往是整页最有用的文字。

<a id="where-it-fits"></a>

## 它在流程中的位置

`to-spec` 是主构建流程的一步，但只位于跨多场会话的分支上：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

上游相邻技能是 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，负责作出本技能只负责记录的决策；以及 [wayfinder](https://aihero.dev/skills-wayfinder)，其完成后的地图恰好在这里接入主流程。下游 [to-tickets](https://aihero.dev/skills-to-tickets) 将规格说明切成曳光弹式工单，供 [implement](https://aihero.dev/skills-implement) 构建。不确定哪个技能或流程适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
