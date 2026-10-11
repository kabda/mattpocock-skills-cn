<a id="what-it-does"></a>

## 它能做什么

`grill-with-docs` 围绕计划或设计访谈你，直到你与 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 达成一致理解，同时将词汇和重要决策写入仓库。它运行的访谈与 [grill-me](https://aihero.dev/skills-grill-me) 相同（一轮问题、等待、再进入下一轮），只是面向代码库。

它是**[有状态](https://www.aihero.dev/ai-coding-dictionary/stateful)**的。其他追问技能把[会话](https://www.aihero.dev/ai-coding-dictionary/session)留在你的脑海里；本技能会在磁盘上留下文件。术语一旦明确，就立即写入 `GLOSSARY.md`，而不是最后批量整理。决策通过三道门槛，就形成 ADR。这就是全部区别，也是人们使用本技能时大多数问题的来源：交付物是真实仓库中的真实文件，因此你期待它们出现时，它们可能不存在；多人共同编写时，内容也可能偏移。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/grill-with-docs` 调用它；agent 不会自行使用。

在仓库中开始一项变更、计划仍然模糊、相关词汇尚未确定时使用。它是用于单场会话的工具。该选哪个追问技能，取决于眼前的情况：

| 你的情况 | 使用 |
| --- | --- |
| 完全不在工作目录中开展工作 | [grill-me](https://aihero.dev/skills-grill-me) |
| 有仓库，且变更能在一场会话中确定 | `grill-with-docs` |
| 工作规模大到一场会话容纳不下（全新项目、大型功能） | [wayfinder](https://aihero.dev/skills-wayfinder) |
| 仓库完全没有领域文档，也没有具体功能要做 | `grill-with-docs`，针对整个仓库而非某项变更 |
| 决策被他人头脑中的知识阻塞 | [to-questionnaire](https://aihero.dev/skills-to-questionnaire) |

与 wayfinder 的区别归根结底是会话数量：单场会话规划用 `/grill-with-docs`，跨多场会话规划用 `/wayfinder`。

<a id="prerequisites"></a>

## 前置条件

技能会写入仓库，因此你需要处于可安全写入的位置。已确定的术语写入根目录的 `GLOSSARY.md` 术语表；如果根目录的 `GLOSSARY-MAP.md` 标明仓库有多个上下文，则写入相关上下文的 `GLOSSARY.md`。决策写入 `docs/adr/`。两者均按需创建；第一个术语或决策明确之前，不会有任何文件，因此无需提前搭建结构。

它还需要另外两个技能，因为自己的 `SKILL.md` 只有一行，将工作委托给它们：[grilling](https://aihero.dev/skills-grilling) 提供访谈，[domain-modeling](https://aihero.dev/skills-domain-modeling) 提供写作。只安装 `grill-with-docs`，得到的技能无法正常工作。

<a id="the-paper-trail"></a>

## 文档记录

一场会话会产生三类内容，它们并不等价。

| 已确定的内容 | 保存位置 |
| --- | --- |
| 一个术语：项目对某事物的专用名称 | 确定时立即写入 `GLOSSARY.md` |
| 难以撤销、缺少背景时令人困惑，并来自真实取舍的决策 | `docs/adr/` 下的 ADR |
| 其他所有决定 | 仅在对话中，不存放到其他地方 |

第三行最容易让人措手不及。`GLOSSARY.md` 是术语表，并且被刻意维持为术语表：不含实现细节、[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)或草稿笔记。ADR 要求同时满足三个条件，因此大多数决策不符合，大多数会话不会产出 ADR。如果一场会话让术语表更清晰，却没有任何 ADR，它依然符合设计；但这也意味着，你们商定的大部分内容只存在于当时的[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)中。将同一段对话交给 [to-spec](https://aihero.dev/skills-to-spec)，不要[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)它。

术语表才是重点。本技能实际构建的是领域语言：将项目自己的词语约定一次，让你、agent 和同事不必反复付出重新推导的代价。也应当说明，并非所有人都同意这能提升 agent 表现：最有力的公开质疑是，一个术语及其用直白语言展开的描述，会让[模型](https://www.aihero.dev/ai-coding-dictionary/model)给出相同结果；词汇真正压缩的是共享这些词语的人类之间的沟通。这种理解仍然承认术语表有价值，只是价值所在不同。

<a id="common-questions"></a>

## 常见问题

**该用这个，还是 `/wayfinder`？**
由范围决定。能在一场会话中确定的事情用本技能；工作量大到一场容纳不下时用 [wayfinder](https://aihero.dev/skills-wayfinder)，它会先将工作绘成决策[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)地图。Wayfinder 更慢、更密集，对范围明确的功能使用它是常见错误。它不会替代本技能：地图中适合通过追问解决的部分，仍可进入追问会话。

**它运行了，却没有生成 `GLOSSARY.md`，也没有 ADR。**
有两种已知原因。普通情况是：没有内容符合条件。ADR 必须通过三道门槛，而如果变更不涉及新词汇，确实可能没有内容需要写入。真正的 bug 是：当技能在另一个编排层中运行（规格驱动开发封装、多 agent 框架、把它作为他人流水线步骤调用的规则），有人报告写文件的那一半工作会悄无声息地消失，而访谈仍在进行。该问题已记录，尚未修复。如果你处于这种环境，在信任会话产出之前先检查工作目录。

**它一次问完所有问题，没有推荐答案，也从未提及 `GLOSSARY.md`。**
这是技能未能加载两个依赖。因为 `SKILL.md` 只有一行委托，如果 agent 没有加载 [grilling](https://aihero.dev/skills-grilling) 和 [domain-modeling](https://aihero.dev/skills-domain-modeling)，就会猜测追问的含义，给你一堆未经区分的问题。只加载一部分时更令人困惑：加载了 `grilling`，没加载 `domain-modeling`，于是访谈不错，却没有文档记录。这与模型及[推理力度](https://www.aihero.dev/ai-coding-dictionary/effort)有关，是本技能被报告最多的问题。如果怀疑发生了这种情况，直接问 agent 加载了哪些技能。

**其他所有决策去哪了？**
只留在对话里。这是对本技能最实质性的未解决批评：术语表不是规格说明，大多数回答不够形成 ADR，也没有台账将每个已确定的答案一路关联到规格说明、工单和测试。精确回答（顺序保证、禁止性需求、数值默认值）在下游会被弱化成更含糊的文字，结果看起来完整，却漏掉了你真正决定的事项。当前可用的缓解办法是保留会话，直接交给 [to-spec](https://aihero.dev/skills-to-spec)，然后对照自己的回答重读规格说明，不要假设它已完整捕获。

**能针对一个完全没有文档的既有仓库使用它吗？**
可以。对于没有 ADR、领域语言或设计原则的代码库，这就是合适的技能：调用它，并说 "help me document my repo"。社区常用做法是将它与 [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 配合，建立或修复 `GLOSSARY.md`。要准备好引导它：它会读取代码，询问你对发现的看法，而你要决定代码库中现有的哪些词是正确的。

**会话结束后该做什么？**
技能的结束语往往比较开放，这是已知的不顺手之处。在主流程中，答案是在同一段对话中运行 [to-spec](https://aihero.dev/skills-to-spec)。如果变更足够小，可以立即构建，就直接进入 [implement](https://aihero.dev/skills-implement)。

**为什么叫这个名字？**
没人满意这个名字。有一项尚未落实的建议是改名为 `grill-domain-model`，它更准确地描述行为。目前没有进展。如果将来改名，文档页也会随之移动，URL 会改变。

<a id="its-working-if"></a>

## 如何判断它有效

- `GLOSSARY.md` 在会话*期间*逐个术语更新，而不是结束时一次性出现。
- 术语表读起来是纯粹的词汇表（项目用语及简练定义），不含实现细节或类似规格说明的文字。
- 代码库能回答的问题，通过读取代码库解决，而不是问你。
- 只产生少量或不产生 ADR；生成的 ADR 记录的是那些你不愿反复重新争论的决策。
- 它会质疑你使用的某个词，因为现有术语表对它有不同定义。

<a id="where-it-fits"></a>

## 它在流程中的位置

`grill-with-docs` 位于主构建流程的起点：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

它发生在任何内容被写成规格说明之前：先产出共同理解和确定的词汇，再由 [to-spec](https://aihero.dev/skills-to-spec) 综合整理，无需再次访谈。与它相邻的技能是 [grill-me](https://aihero.dev/skills-grill-me)，提供相同访谈但不需要仓库、不写文件；以及 [domain-modeling](https://aihero.dev/skills-domain-modeling)，提供它所驱动的术语表与 ADR 实践；两种追问入口都建立在 [grilling](https://aihero.dev/skills-grilling) 基础技能之上。其上游的 [wayfinder](https://aihero.dev/skills-wayfinder) 为一场会话容纳不下的工作绘制地图，并能将部分地图交回本技能处理。不确定哪个技能或流程适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
