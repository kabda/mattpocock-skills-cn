<a id="what-it-does"></a>

## 功能

`wayfinder` 接手一个 agent [会话](https://www.aihero.dev/ai-coding-dictionary/session) 容纳不下的工作：能说出**目标**、却还看不清路线的想法。它把工作绘制成 issue 跟踪器上的共享**决策工单地图**，再逐一解决，直到道路清晰。

它做规划，不做执行。每张工单包含一个问题，解决后产出决策，而非待执行的构建切片；当有人动手构建之前已无事需要决定时，地图就完成了。这条规则区分了 wayfinder 工单与普通实现[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)，也是 agent 最常违反的规则。地图清晰后，wayfinder 会交接，不会继续写代码。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/wayfinder` 调用；[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。

它是整套技能中最重、最密集的流程，因此触发范围很窄：工作必须确实超过一个 agent 会话所能容纳的规模，而且通往目标的路仍有迷雾。界线很清楚：`/grill-with-docs` 用于单会话规划，`/wayfinder` 用于多会话规划。

| 面前的工作 | 运行什么 |
| --- | --- |
| 范围清楚，一次讨论即可确定的功能 | [grill-me](https://aihero.dev/skills-grill-me)，有代码库时用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 全新项目，或跨多个会话的构建，路线尚不清晰 | `/wayfinder` |
| 决策已经完成的会话 | [to-spec](https://aihero.dev/skills-to-spec)：直接跳过地图 |
| 已经清晰的 wayfinder 地图 | [to-spec](https://aihero.dev/skills-to-spec)，再用 [to-tickets](https://aihero.dev/skills-to-tickets) 和 [implement](https://aihero.dev/skills-implement) |
| 已经膨胀过大的现有会话 | 说“交接给 `/wayfinder`”（[handoff](https://aihero.dev/skills-handoff) 既能接入地图，也能从地图交出） |

不要求必须是全新项目。Wayfinder 经常用于遗留和半成品代码库，甚至在那里更有效，因为大量迷雾关乎“这里已有的事实是什么”，而不是“我们应当做什么”。

<a id="prerequisites"></a>

## 前置条件

地图和工单位于仓库的 issue 跟踪器，因此 wayfinder 需要 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 配好跟踪器。该步骤写入 "Wayfinding operations" 章节，描述 GitHub、GitLab 或本地 Markdown 如何表示地图、子工单、阻塞关系和前沿查询。Wayfinder 通过 `CLAUDE.md` / `AGENTS.md` 中的指针找到该文档，而非固定路径；完全没有跟踪器配置时，回退到本地 Markdown 文件。

跟踪器不是装饰。阻塞关系让前沿在跟踪器 UI 中可视化；如果没有原生依赖链接（比如自托管 Gitea），wayfinder 就退化为从地图文本推断阻塞项，虽然可用，但需要更密切监督。

<a id="the-map-the-fog-and-the-frontier"></a>

## 地图、迷雾与前沿

**地图**是带 `wayfinder:map` 标签的单个 issue；工单是其子 issue。它是**索引，而非存储库**：每个决策恰好只保存在自己的工单中，地图只给概要和链接。会话加载低分辨率地图，按需深入个别工单，因此地图可以持续增长，而不必让每个会话都承担全部历史的成本。

地图有四节：

- **Destination**：到达地图终点是什么样。命名目标是绘图的第一步，先于任何工单，因为目标确定了衡量所有工单的范围。
- **Decisions so far**：每张已关闭工单一行，链接到细节实际所在处。
- **Not yet specified**：**战争迷雾**。知道将要面对，却还无法清晰表述的决策。区分迷雾与工单的判据是*现在*能否精确陈述问题，而非能否回答。解决工单会驱散前方迷雾，把现在能够明确描述的部分转成新工单。
- **Out of scope**：判定超出目标的工作。迷雾只会*朝向*目标聚集，因此范围外工作被关闭，永不转化为工单。

**前沿**是开放、无阻塞、未认领的工单（已知领域的边缘）。会话在任何工作开始前，把工单分配给自己来认领，所以受理人*就是*认领标记，并发会话会跳过它。始终按名称引用工单，绝不用裸 `#42`；在过程说明中，一堵 issue 编号墙无法阅读。

<a id="the-four-decision-ticket-types"></a>

## 四种决策工单类型

每张工单带 `wayfinder:<type>` 标签，要么是 **[HITL](https://www.aihero.dev/ai-coding-dictionary/human-in-the-loop)**（与代表自己发言的人共同处理），要么是 **[AFK](https://www.aihero.dev/ai-coding-dictionary/afk)**，由 agent 独立推动。HITL 工单只能通过实时交流解决；agent 自己回答[追问](https://www.aihero.dev/ai-coding-dictionary/grilling) 问题就违反了要求。

| 类型 | 模式 | 何时使用 | 由谁解决 |
| --- | --- | --- | --- |
| `grilling` | HITL | 默认情况。问题可以通过讨论确定。 | 新会话中的 [grilling](https://aihero.dev/skills-grilling) 加 [domain-modeling](https://aihero.dev/skills-domain-modeling) |
| `prototype` | HITL | “应当长什么样”或“应当怎样运行”：单靠对话无法解决的问题。 | [prototype](https://aihero.dev/skills-prototype)，从工单把构建产物作为资源链接 |
| `research` | AFK | 工作目录之外的事实阻塞了决策。 | 绘图时启动 [research](https://aihero.dev/skills-research) [子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)，在 `research/<name>` 分支上并行完成 |
| `task` | 任一种 | 没有什么要决定，但手动工作阻塞了决策，例如开通权限、注册服务、移动数据以看清其形态。 | 能独立完成时由 agent 执行，否则给人一份精确清单 |

`task` 是唯一*做事*而非决策的类型，它因解除决策阻塞而有必要，绝不是为了交付目标的一部分。实践中这种类型最容易出错：agent 将它理解为实现步骤，开始在地图内编写产品代码。

研究是*每个会话一张工单*的唯一例外。

<a id="common-questions"></a>

## 常见问题

**与 `/grill-with-docs` 有何区别？该从哪个开始？**
区别在会话数量，不在项目大小。`/grill-with-docs` 用于单会话规划；wayfinder 用于多会话规划。整个事情能在一次对话中容纳时，grilling 更便宜也更好，wayfinder 在这种情形下确实更慢、更密集。社区形成的简明说法是：只有一个会话容纳不下的工作，wayfinder 才有意义。这是遥遥领先的最常见问题，反复被问，是因为描述没有告诉你自己的任务位于界线哪侧。会话数量需要你自己判断。

**它问“目标”时，指本会话结束，还是整个事情结束？**
整张地图。也就是整张地图的目标，不只是初始会话。这个问题读起来有歧义，因为 wayfinder 本就是多会话工具，所以只针对会话的答案永远不合理。典型目标包括供交接的[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)、规划开始前需锁定的决策、概念验证，或数据迁移等就地变更。

**地图已经清晰。wayfinder 不是已经写了规格说明、建了工单吗？为什么还需要 `/to-spec` 和 `/to-tickets`？**
不是。Wayfinder 的工单是决策工单，地图关闭时它们也都已关闭。剩下的是满是相互链接决策的地图，并非构建计划。[to-spec](https://aihero.dev/skills-to-spec) 把这些链接决策收敛成一份规格说明（`/to-spec #<map_issue>`），[to-tickets](https://aihero.dev/skills-to-tickets) 再切成曳光弹实现工单。直接把地图接到 [implement](https://aihero.dev/skills-implement) 会跳过收敛，丢失链接细节。只有最终发现工作确实很小时，才直接实现。确实有人采用简化流程并报告可行；多出的两步换来的是审阅者或同事能读的明确规格产物，越不是单打独斗，就越重要。

**我的 agent 在 wayfinder 会话中途开始写生产代码。**
这是该技能最常报告的失败，背后确有缺口。Wayfinder“规划、不执行”的默认行为可以在地图的 **Notes** 中覆盖，但 Notes 是 agent 写的，因此约束和豁免都位于被约束者自己掌控的文件。一个用户看见 agent 在自己的 Notes 写入“本地图包含执行”，之后会话又读回这句话，把它当作许可，在真实运行的服务器上构建。技能内部没有针对“我指的是默认行为”的硬性停止机制。在补上之前：阅读任何非你亲手绘制地图的 Notes，把实现放在独立会话中，并把任何看似构建切片的 `wayfinder:task` 视为类型错误。

**我绘了 27 张工单，做到第十三张时，剩下的都不再合理。**
这是一个真实、反复被报告的结果，直接来自实地报告。Wayfinder 的默认倾向是全面规划，后期工单依赖的假设被前期工单推翻，正是人们指责它陷入的瀑布陷阱。有两种应对。把地图限定到有界目标，而非整个产品。实践者一致反馈，围绕一个明确 epic 的地图，比蔓延的“实现 V1”更可靠；一开始的目的就不是规划巨物，而是交付小增量。再者，大量做[原型](https://www.aihero.dev/ai-coding-dictionary/prototyping)：让路线保持有效的根本原因，是在实现依赖不确定性之前，用低成本具体产物把它消除。Wayfinder 是 "prototypemaxxing"，不是 "planmaxxing"。

**可以并行处理多张工单吗？**
前沿用于显示哪些可接手，阻塞关系让并行工作在理论上安全。实践中逐张处理是更稳妥的默认方式。用户同时处理两张追问工单时，一个会话会问另一个会话刚回答过的问题，因为会话之间不共享[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。原型工单还有一个已知缺口：有人报告 agent 做出三个 UI 变体，自行选一个并关闭工单。选择权在你，技能目前对此强调不足。如果确实并行，先亲自审查依赖图。

**必须使用 GitHub Issues 吗？**
不用，任何 issue 跟踪器都可以。GitHub 支持最好，因为原生子 issue 和阻塞关系让你无需打开地图就能看见前沿；GitLab、Linear、Jira 和本地 Markdown 都有人用。坦率地说，有两点限制：没有原生阻塞的跟踪器需要从文本推断依赖图，并手动修正；本地 Markdown 把产物放进仓库，这并不推荐，因为这些材料容易意外长期留存。开源维护者则遇到相反的问题（公开跟踪器被 agent 生成的规划工单塞满），因此往往仍选择本地 Markdown。

**追问太累了，每个问题都长达三段。**
这是关于 wayfinder 最尖锐的现行抱怨，尚未解决。有位用户把问题拆为两部分：冗长本身造成决策疲劳，篇幅又淹没了*为什么*要问这个问题，地图越长，越难看清决策之间的联系。冗长似乎是当前这批[模型](https://www.aihero.dev/ai-coding-dictionary/model) 的特性，而非技能本身，尚无修复落地。实践者流传的缓解办法是降低[推理强度](https://www.aihero.dev/ai-coding-dictionary/effort)，在全局 `CLAUDE.md` 中加入使用通俗语言的指令。无论如何，都要准备投入真正的思考，因为 wayfinder 要求你思考的量并非缺陷，而是它的大部分用途。

**已经关闭的决策后来发现错了。编辑旧工单，还是新建？**
没有官方指引，而 agent 的本能也帮不上忙：它倾向于围绕错误决策设计，而非质疑它，所以需要你手动引导。可行做法是明确告诉 wayfinder 什么变了；它会更新地图、修订受影响工单，并在已关闭工单上评论。中途范围变化可以挽回；从设计之初就打算变化的地图，则是范围界定有问题的信号。

**`decision-mapping` 去哪里了？**
就是本技能，v1.1 改名为 `wayfinder`，通过 `/wayfinder` 调用。“Decision map”既是术语，也不准确，因为四种工单类型中只有一种本身真正是决策。重构表达后，技能获得了一套连贯词汇（目标、战争迷雾、前沿、地图），不再额外叠加生造术语。不过工作单位保留了“decision”：wayfinder 的工单称为**决策工单**，正是为了防止被当作实现工单。

<a id="its-working-if"></a>

## 有效运行的迹象

- 在任何工单存在前，目标已写下并达成一致。
- 每张开放工单读起来都是问题。任何写着“构建 X”的工单，要么类型错误，要么应当位于地图的下游。
- 无需打开地图，就能在跟踪器里看出哪些工单可接手，因为原生阻塞关系呈现了前沿。
- 一个会话解决一张工单，以解决结果评论发布答案，关闭它，在地图的 *Decisions so far* 留一行，然后停止。
- **Not yet specified** 随时间缩小。某片迷雾转成工单后，从该章节消失，不会两处并存。
- 开场的广度优先追问完全没发现迷雾时，技能停止，并告知工作足够小，可以跳过地图。
- 完成地图的会话引导你走向规格说明，而非 pull request。

<a id="where-it-fits"></a>

## 所处位置

`wayfinder` 是**特定情境的入口支路**，不是默认前门。大部分工作仍从追问引领的想法 → 交付链条开始；想法大到一个会话装不下时，才走 wayfinder，再从 [to-spec](https://aihero.dev/skills-to-spec) 汇回主链，因为地图清晰后会交接，而非构建。

底层主要是由 wayfinder 调度其他技能：[grilling](https://aihero.dev/skills-grilling) 和 [domain-modeling](https://aihero.dev/skills-domain-modeling) 解决默认类型工单；[prototype](https://aihero.dev/skills-prototype) 解决靠对话无法解决的工单；[research](https://aihero.dev/skills-research) 作为子 agent 运行，使阅读内容不进入你的会话。[handoff](https://aihero.dev/skills-handoff) 是进出地图的桥梁：对话膨胀过大时接入地图，会话中途出现支线任务时从地图交出。其他情况由 [ask-matt](https://aihero.dev/skills-ask-matt) 在整套技能中指路。
