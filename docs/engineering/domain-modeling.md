<a id="what-it-does"></a>

## 它能做什么

`domain-modeling` 在设计过程中构建并精炼项目的**通用语言（ubiquitous language）**：质疑与术语表冲突的用词，用精确的词替代含糊表达，并用具体情景对关系进行压力测试，直到边界明确。

它是**主动**实践，而不是被动实践。阅读 `CONTEXT.md` 以借用其中的词汇，是任何技能都能执行的一条简单习惯；本技能用于*改变*模型。因此它会打断你。术语明确的那一刻，它就会在对话进行中将其写入 `CONTEXT.md`，而不是等结束时才生成整齐的术语表，因为批量整理版本只是[会话](https://www.aihero.dev/ai-coding-dictionary/session)的摘要，随时记录的版本才是会话的实际产出。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/domain-modeling`，或者在任务适合时由 agent 自动使用它。实践中，自动调用是本技能最薄弱的部分：当 `grill-with-docs` 或 `wayfinder` 要求加载它时，[模型](https://www.aihero.dev/ai-coding-dictionary/model)经常加载 `grilling`，却跳过本技能。如果一场[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)会话结束时 `CONTEXT.md` 完全没有变化，发生的就是这种情况；请在调用另一个技能时，同时明确点名调用它。

当问题出在*词语*上时使用：

| 情况 | 做法 |
| --- | --- |
| 两个人对 "cancellation" 的理解不同 | `domain-modeling`：选定规范术语，将另一个词列在 `_Avoid_` 下 |
| "Account" 在三个文件里承担三种角色 | `domain-modeling`：将它拆分为 Customer 和 User |
| 刚刚作出了难以撤销的架构选择 | `domain-modeling`：如果选择达到标准，它会提议 ADR |
| 问题在模块的*形态*：seam 在哪里，接口有多深 | [codebase-design](https://aihero.dev/skills-codebase-design) |
| 希望构建前对整个计划进行追问 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，它会在底层驱动本技能 |
| 只想查阅一个术语，而不是改变它 | 什么技能都不需要。阅读 `CONTEXT.md`。它就是一个文件。 |

<a id="prerequisites"></a>

## 前置条件

不需要提前准备。本技能写入两个位置，均按需创建：

- 仓库根目录的 **`CONTEXT.md`**，在第一个术语明确时创建。如果仓库根目录有 `CONTEXT-MAP.md`，则将术语写入映射指向的各上下文 `CONTEXT.md`。
- **`docs/adr/`**，在第一份达到标准的 ADR 出现时创建。

开始前不需要预先存在任何内容，也不会因预想中的需要而创建文件。

<a id="two-artifacts-two-bars"></a>

## 两种交付物，两套标准

术语表和 ADR 遵循不同标准，混淆两者是本技能大多数问题的来源。

| | `CONTEXT.md` | `docs/adr/NNNN-slug.md` |
| --- | --- | --- |
| 保存什么 | 术语。用一两句话说明某事物**是什么**，将弃用的同义词列在 `_Avoid_` 下 | 一项决策，用一到三句话说明：背景、选择、理由 |
| 写入门槛 | 含糊的术语已成为规范用词 | **同时满足三项**：难以撤销、缺少背景时令人困惑、来自真实的取舍 |
| 何时写入 | 术语确定时立即写入 | 先提议，不擅自认定要写 |
| 绝不保存 | 实现细节、[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)、草稿、通用编程概念 | 本次会话每一个选择的流水账 |

ADR 的三个条件只要缺少一个，就不创建 ADR。容易撤销的决策直接撤销即可；不令人困惑的决策没人会追问；没有真正替代方案的决策只不过记录了你做了显而易见的事。

真正需要牢牢守住的是 `CONTEXT.md` 的规则，因为它在实际使用中最容易被破坏。**它只是术语表，仅此而已。** 如果放任不管，模型会把“写入 `CONTEXT.md`”理解成获准保存你的每一个回答，文件就会变成不断增长的规格说明。这是多个模型中关于本技能被报告最多的问题。

<a id="cross-referencing-and-where-it-stops"></a>

## 交叉核对及其边界

让这个技能发挥作用的关键动作是：当你陈述某件事如何工作时，它检查代码并指出矛盾。*“代码会取消整个 Orders，但你刚才说可以部分取消，哪个是对的？”* 在改变语言或代码之前，先明确让两者达成一致。

也应当了解它的限制。它只交叉核对**代码**以及已提交的 `CONTEXT.md`/ADR，除此之外没有其他来源。它不会搜索 issue 跟踪器，因此几个月前已经在关闭的 issue 中讨论并有意解决的命名冲突，会被当作新问题重新提出。目前有[尚未解决的请求](https://github.com/mattpocock/skills/issues/717)要求修复这一点；在此之前，应对方法是把相关指令写入你自己的 `docs/agents/domain.md`，技能原本就会读取该文件。

<a id="common-questions"></a>

## 常见问题

**我的 `CONTEXT.md` 已经有 500 行、1,000 行甚至 3,000 行，该怎么办？**
大小是症状，不是病因：这个文件吸收了本不属于术语表的实现细节和决策。修复方法是直接下达指令：`/grill-with-docs make my CONTEXT.md more concise and remove any implementation details from it`。对膨胀的文件运行后，大部分内容都会被移除。只有文件已经足够精简，却仍覆盖两个读者不愿同时记住的领域时，才考虑用 `CONTEXT-MAP.md` 拆分；拆分一个膨胀文件，只会得到几个膨胀文件。本技能目前的指导还不足以从源头防止这种增长，跟踪该问题的 issue 仍未解决。

**为什么叫 `CONTEXT.md`，而不是 `GLOSSARY.md`？**
这是整套技能中争论最多的命名问题，尚无定论。反对当前名称的理由很充分：既然它“只是术语表，仅此而已”，`GLOSSARY.md` 就能直接说明这一点；正如一位读者所说，“对于 AI agent，一切都是[上下文](https://www.aihero.dev/ai-coding-dictionary/context)”。支持当前名称的理由在于映射：`CONTEXT-MAP.md` 指向多个 `CONTEXT.md` 文件读起来很自然，`GLOSSARY-MAP.md` 则没有这种效果，而且 `context` 是 DDD 中表示模型限界区域的常用词。至少有一个人维护本地 fork，仅仅为了重命名这个文件。你也可以这样做，但技能集中的其他每个技能都在寻找 `CONTEXT.md`，所以重命名意味着全部都要修改。

**`/ubiquitous-language` 去哪了？**
它被移除了，并不是被标记为弃用。它的职责转移到 `domain-modeling`，后者会持续维护整个模型，而不是从一场对话中倒出一份术语表。词汇约束变得更加关键，而非更加次要：如今它在追问、分流和绘图过程中作为底层能力运行，不再是需要你记得单独执行的一轮工作。

**如何为没有术语表的代码库建立术语表？**
明确提出请求，不要等它慢慢积累。文档给出的方式是 `/grill-with-docs help me scaffold my existing repo with a CONTEXT.md`；应当预期这会是一场漫长的追问：一位用户报告说，文件成形前回答了 50 多个问题。对于既有仓库，顺带使用这个技能，术语表建立得太慢。

**能保留领域模型功能，同时使用自己的 ADR 格式吗？**
目前无法顺畅做到。术语表和 ADR 两部分在同一个技能中交付，因此已有 ADR 约定的团队（不同模板、不同位置、不同命名）会收到与自身风格冲突的指令。当前的选择是复制技能到本地并修改，或在仓库自己的 agent 文档中覆盖 ADR 约定。将两者拆开是[尚未解决的请求](https://github.com/mattpocock/skills/issues/557)。

**术语表真的值得维护吗？它又增加了一份要审查的交付物，而且可能过时。**
有时确实不值得，应当坦诚说明哪些情况如此。DDD 越接近实现，其价值越低：收益在上游，在于命名和概念对齐，而不是聚合与分层仪式。控制同义词在命名边界很重要：模块名、表名、状态枚举、issue 标题、CLI 命令。在普通文字中，重要性就小得多。还有一种正在讨论的反对意见：领域术语压缩的是已共享这些术语的*人类之间*的沟通，而 agent 对直白的自然语言描述会给出同样的响应。按这种理解，术语表的价值是让你和审阅者与 agent 的工作保持一致，而不是让 agent 变得更好。只做一天的项目，就跳过它。未经审阅、由 agent 编写的术语表比没有还糟：它会变成听起来信心十足的传言，被后续会话当作事实。

**它能帮我把含糊的提示词转成领域语言吗？**
不能，也没有计划创建这样的技能。连你自己都不理解的领域语言，一旦写下来就会变成毫无意义的废话。本技能在你已经理解的前提下要求精确，而不会凭空制造你并不掌握的词汇。相关陷阱是：不做建模，却使用领域词语。在错误的概念结构上放上正确的名词，产出的内容看起来正确，实际却不对。

<a id="its-working-if"></a>

## 如何判断它有效

- 它在你说到一半时打断，询问你指的是两种事物中的哪一种，而不是自行选一个继续。
- `CONTEXT.md` 在对话**期间**变化，而不是结束时集中写入。
- 对于明天就能撤销的事情，它拒绝编写 ADR，并说明三个条件中哪一项不满足。
- 新条目用一两句话定义事物*是什么*，并在 `_Avoid_` 下列出你放弃使用的词。
- 当代码与你的话不一致时，它会引用代码向你指出。
- `CONTEXT.md` 缩短的频率与增长的频率相当。

<a id="where-it-fits"></a>

## 它在流程中的位置

`domain-modeling` 是**由模型调用的参考技能**，更多时候在其他技能*底下*运行，而不是单独运行。[grill-with-docs](https://aihero.dev/skills-grill-with-docs) 在追问会话中驱动它，[wayfinder](https://aihero.dev/skills-wayfinder) 在绘制地图时加载它，[triage](https://aihero.dev/skills-triage) 用它确保[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)使用项目自身的语言，[improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 则在决策明确时调用它。它最接近的同类是 [codebase-design](https://aihero.dev/skills-codebase-design)：两者构成其他所有技能之下的词汇层，本技能负责*领域*，后者负责模块*形态*。当你只想采用这套实践，却不想承诺执行通常会调用它的其他技能的步骤时，也可以直接使用。不确定哪个技能适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
