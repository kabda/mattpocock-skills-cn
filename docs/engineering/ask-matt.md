<a id="what-it-does"></a>

## 功能

`ask-matt` 是本仓库技能的路由器。你描述自己的情境（一个不知如何起步的想法、一堆收到的 bug 报告、持续太久的[会话](https://www.aihero.dev/ai-coding-dictionary/session)），它会指出适合的技能或技能序列，以及其中哪些位置需要人作出决策。

它提出建议后就停止。不会追问、编写[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)、打开文件或启动刚提到的技能；返回的是下一步要输入的内容，由你来输入。它也是本仓库技能的手写地图，不会扫描已安装的技能，因此无法指引你使用自己的技能或其他作者的技能。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/ask-matt` 调用；agent 不会自行使用。

| 你的情境 | 路由器的回答 |
| --- | --- |
| 有想法，却不知从何开始 | 主流程入口，以及构建是否足够小、可以跳过规格说明 |
| 收到他人的 bug 和请求 | [triage](https://aihero.dev/skills-triage) 入口支路，以及为什么你自己生成的[工单](https://www.aihero.dev/ai-coding-dictionary/ticket) 不属于这条支路 |
| 两项技能看似可以互换 | 两者的界线，通常是一个具体判据，而非品味问题。[grill-me](https://aihero.dev/skills-grill-me) 与 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 的区别取决于是否在工作目录中；[grill-with-docs](https://aihero.dev/skills-grill-with-docs) 与 [wayfinder](https://aihero.dev/skills-wayfinder) 的区别取决于一个会话能否容纳这项工作 |
| 会话很长，需要决定如何处理[上下文](https://www.aihero.dev/ai-coding-dictionary/context) | 阶段边界处五种选择的有序决策树 |
| 已经选好了技能 | 没什么帮助。直接调用那项技能。 |

<a id="prerequisites"></a>

## 前置条件

路由器指出技能，但不安装技能。它所指向的一切都必须已安装，建议才能付诸行动；它只知道本仓库正式收录的技能。

依赖跟踪器的路线（triage、`to-spec`、`to-tickets`、`implement`）假定 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 已在仓库中配置 issue 跟踪器。即使尚未配置，路由器也照样会推荐。

<a id="flows-not-skills"></a>

## 看流程，而不只是技能

这个技能提供的思考概念是**流程**：*贯穿*多项技能的一条路径，而非单项技能。说清情境，就能定位到某条流程的某一步，这与“这是匹配你关键词的技能”是不同的回答。共有四类路线，技能正文完整描述了它们：

- **主流程**，从想法到交付。追问、规格说明、工单、实现、审查，其中有两条分支：问题需要运行代码才能解决时，绕道做原型；构建跨多个会话时，规格说明和工单的拆分才值得其成本。
- **入口支路**，从某种产生工作的情境出发，再汇入主流程：收到 bug 报告、某处故障，或工作过于模糊庞大，一个会话容纳不下。
- **独立技能**，在所有流程之外，按各自条件使用：原型、问卷、你已经陷入的合并冲突。
- **底层词汇层**，当问题在用词而非流程时，由其他技能引入的两项参考技能。

<a id="the-phase-boundary"></a>

## 阶段边界

它提供的另一个概念是**阶段边界**。阶段是会话内的一段工作（[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)、实现、QA），两个阶段之间的边界才是考虑“该怎样处理这段上下文”的地方。阶段中途无需决策：继续，或把剩余工作拆给[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)。

| 选项 | 何时选择 |
| --- | --- |
| **继续（Continue）** | 下一阶段需要原样保留当前阶段，或者 [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone) 仍有余量。唯有它能把会话保留为[一手来源](https://www.aihero.dev/ai-coding-dictionary/primary-source)，因此先排除它 |
| **`/clear`** | 此前的一切都可丢弃。成本最低，判断错了却无法逆转 |
| **[handoff](https://aihero.dev/skills-handoff)** | 有内容需要转移：新的 [harness](https://www.aihero.dev/ai-coding-dictionary/harness)、新目录、同事，或阶段中途分出的旁支任务 |
| **子 agent** | 任务范围足够明确，你[离开键盘](https://www.aihero.dev/ai-coding-dictionary/afk) 后也能执行 |
| **`/compact`** | 以上都不适用。默认选择，而且经常会落到这里 |

其中两项经常被用错，所以路由器给出的是顺序，而不只是列表。`/handoff` 看起来像窗口之间的通用桥梁，其实不是：可携带性就是它的全部价值。`/compact` 位于决策树底部，不应首先尝试，因为前面四个问题对应的选择都更便宜或更精确。

<a id="common-questions"></a>

## 常见问题

**不能直接按正确顺序列出技能吗？**

不断有人在 README 中提出这个要求。这个技能就是那份列表：这正是它存在的意义。静态表格可能写成 `wayfinder → to-spec → to-tickets → implement → code-review`，但对大多数情境都不正确，因为关键恰在分支：是否有代码库、构建是否跨会话、这个问题能否靠对话解决。必须承认的代价是路由器靠手工维护，会滞后于仓库。`/grilling` 和 `/resolving-merge-conflicts` 都发布了很久，才被路由器提及。

**它说一半技能没有安装。**

这是已知但尚未修复的 bug。路由器指引的大多数技能设有 `disable-model-invocation: true`，意味着 harness 不会把它们放入注入 agent 上下文的技能列表。agent 把这份列表当作完整清单，就报告技能缺失。有次报告中的会话声称整个规格说明与工单流程都不存在，转而只用 `/grilling` 和 `/tdd`。插件的二十二项技能中有十三项带有该标志，因此这是常见情况，而不是边缘情形。它们已经安装。照样输入 slash command，或查看 `.claude-plugin/plugin.json`，那才是存在性判断的权威来源。

**它描述了某项技能的行为，但该技能根本不这么做。**

这也确实存在，也尚未修复。路由器依据自己对各技能的一行摘要回答，而不是读取技能本身。一份详细报告在同一会话中追踪到三次这种情况，其中一次仅凭“把会话转成规格说明”这句概述，就建议跳过 [to-spec](https://aihero.dev/skills-to-spec)：它从未打开 `to-spec/SKILL.md`。每次都是用户质疑后才核实，从不主动核实。当时跳过 `to-spec` 导致漏掉一次真正的 seam 检查，生成的工单低估了工作量。当路由器对另一项技能作出关键断言时，要求它先打开相应的 `SKILL.md`。对于地图完全没覆盖的问题，比如是否使用 [plan mode](https://www.aihero.dev/ai-coding-dictionary/agent-mode)，也一样：那个回答是[模型](https://www.aihero.dev/ai-coding-dictionary/model)的推断，不是这里写明的内容。

**为什么用散文，而不是编号清单？**

这是合理的抱怨，已有开放 issue 指出大部分路由逻辑是确定的，叙述形式让人难以扫读。你完全可以要求压缩形式：“只给我顺序”就能得到顺序。散文承载的是条件部分：分支、需要人决策的位置，以及步骤之间何时清空或压缩上下文。扁平清单恰好会丢失这些内容。

**它能指引我使用自己的技能或其他作者的技能吗？**

不能。已有三个独立提案，希望路由器读取本地 `skills/` 目录，从已安装技能中推荐。`ask-matt` 不是这样的工具。它是手工维护的一套技能地图，对你自己编写或从别处安装的技能一无所知。

**它让我编辑 SKILL.md。**

这个建议往往正确，却很难持久。有人问如何让 [implement](https://aihero.dev/skills-implement) 关闭工单，得到的建议是在技能中加一行，随即发现问题：`npx skills update` 会覆盖文件，插件安装目录则是只读的。把长期行为写入你自己的 `CLAUDE.md` 或 `AGENTS.md`，或在调用时说明。提示词层面的调整能经受更新：把流程指向 Linear 而不是 GitHub，或询问哪些未关闭工单可以并行处理，人们都用这种方式实现。

**它提到了我没有的技能，或漏掉了我有的技能。**

先检查 changelog 中是否改过名，再判断是否被移除。`writing-great-skills` 改名为 [writing-for-agents](https://aihero.dev/skills-writing-for-agents)，没有别名；`to-prd` 改名为 [to-spec](https://aihero.dev/skills-to-spec)，`pathfinder` 改名为 [wayfinder](https://aihero.dev/skills-wayfinder)。另有四项技能直接退役，被其他技能吸收：`ubiquitous-language`、`design-an-interface`、`qa` 和 `request-refactor-plan`。反过来，漏掉已有技能的原因就是上文所说的路由器滞后。

<a id="its-working-if"></a>

## 有效运行的迹象

- 最后指出要输入什么，然后停下，而不是自己开始工作。
- 给出的路线说明何时清空或压缩上下文，以及何时需要你审阅，而不只是列技能名。
- 两项技能接近时，说明该选哪一项，以及另一项为什么不适合你。
- 对其他技能行为的任何断言，都能在执行轨迹中看到它读取对应 `SKILL.md`。
- 你能从回答中认出自己的情境，而不是最接近的泛化场景。

<a id="where-it-fits"></a>

## 所处位置

`ask-matt` 是覆盖整套技能的**独立路由器**。它从不是链条中的一步，而是指向每条链条；其他文档页都链接回这个节点，就不必各自重画整张图。从这里最常去的是主流程入口 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，或处理外来工作而非自发工作的入口支路 [triage](https://aihero.dev/skills-triage)。

对于所描述的技能，它是[二手来源](https://www.aihero.dev/ai-coding-dictionary/secondary-source)。路由器与 `SKILL.md` 不一致时，以 `SKILL.md` 为准。
