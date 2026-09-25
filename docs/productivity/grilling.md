<a id="what-it-does"></a>

## 它能做什么

`grilling` 是一个访谈循环，在任何人采取行动之前，对计划、决策或想法进行压力测试。它将主题映射为一棵**设计树**：每项决策都会分支出依赖它的决策，然后逐个分支访谈你，直到没有任何内容被默默假定。

它既不是一次只问一个问题，也不是一次问完所有问题。每一**轮**覆盖整个**前沿**：所有前提已经确定的决策，仅此而已。如果两个问题存在依赖，就绝不会放在同一轮；依赖于尚未得到答案的问题，应当放到后续轮次。你的回答确定决策，前沿向外推进，下一轮询问由此解锁的问题。十三个问题通常只需大约三轮，而不是十三轮。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/grilling`，或者在任务适合时由 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 自行使用。它是追问系列中唯一可由模型调用的[技能](https://www.aihero.dev/ai-coding-dictionary/skill)，因此你很少直接输入它：通常是你*确实输入过*的另一个技能在替你运行它。

直接输入 `/grilling`，得到的只有纯粹的访谈。如果需要更多：

| 你的情况 | 使用 |
| --- | --- |
| 不在工作目录中开展工作 | [grill-me](https://aihero.dev/skills-grill-me)：相同的[会话](https://www.aihero.dev/ai-coding-dictionary/session)，但这个名称永远不会由 agent 自行触发 |
| 正在工作目录中 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)：相同的会话，同时不断写入 `CONTEXT.md` 和 ADR |
| 工作量大到一场会话容纳不下 | [wayfinder](https://aihero.dev/skills-wayfinder)：绘制地图，并在决策工单内运行追问 |
| 无法靠讨论解决的问题：某物应当看起来怎样或感觉如何 | [prototype](https://aihero.dev/skills-prototype)：先构建一次性版本，再回来 |
| 你自己的技能需要访谈能力 | 从该技能调用 `/grilling`，而不是另写一套访谈流程 |

<a id="the-round-the-frontier-and-who-decides"></a>

## 轮次、前沿，以及谁作决定

三个概念支撑着整个技能。

**设计树**是主题的模型：决策之下还有依赖它的决策。**前沿**是所有前提已确定的决策集合：也就是当前真正可以提出的那些问题。一**轮**对应一个前沿，完整提问，也完整作答。

每轮中的每个问题都有固定格式：`❓` 后是编号和标题，再给出正文，然后在单独的 `➡️` 行上给出 agent 的推荐答案。这样你可以按编号回答一整轮（“1 同意，2 选第二项，3 不同意，原因如下”），而不必把问题引用回来。这个格式有一个已知的不顺手之处：推荐意见有时会*反对*问题的表述，因此同意推荐就意味着对问题回答“不”。出现这种情况时，按推荐意见回答，并说明这一点。

设计的另一半是将事实与决策分开。事实是技能自己的工作：当前沿问题需要[环境](https://www.aihero.dev/ai-coding-dictionary/environment)能够查明的信息时，它会派出[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)调查，而不是问你。它不会因此阻塞；只有正在调查事项的下游问题需要等待。决策属于你，它必须等待。如果运行 `grilling` 的 agent 自己回答了需要决策的问题，就是违反技能要求，而不是灵活解释。当前沿为空时会话结束；在你确认已达成共同理解之前，它不会根据商定内容采取行动。

需要坦诚承认的限制是：前沿来自 agent 的判断，而不是计算出来的图。它可能把两个问题放在一轮，事后才发现一个答案本应改变另一个问题。除了告诉它，没有其他防护；指出后，受影响的分支会在下一轮重新打开。

<a id="what-lives-here-and-what-lives-in-the-wrappers"></a>

## 本技能与外层封装各自负责什么

本页介绍机制。人们最常关心的事项，记录在上一层的文档中。

| 问题 | 在哪里解答 |
| --- | --- |
| 设计树、前沿、轮次、问题格式、事实与决策的区别 | 本页 |
| 会话应当持续多久、无法靠讨论回答的问题怎么办、如何避免一味点头 | [grill-me](https://aihero.dev/skills-grill-me) |
| 哪些内容写入 `CONTEXT.md`，哪些形成 ADR | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |

<a id="common-questions"></a>

## 常见问题

**能恢复一次只问一个问题吗？**
可以，而且很多用户都这样做。将以下内容加入全局 `CLAUDE.md`：

```
进行 grilling 时，一次只问一个问题。
```

默认按轮提问确实存在争议。阅读速度较慢、使用第二语言，或依赖顺序格式帮助集中注意力的使用者，都反馈一次一个问题的节奏更适合自己。这种退出默认模式的方式是受支持的，而不只是勉强允许。

**`/batch-grill-me` 去哪了？**
并入了本技能。按轮提问曾短暂作为独立技能发布，之后移入 `grilling` 本身，因此所有基于这一基础技能构建的技能（`grill-me`、`grill-with-docs`、`triage`、`wayfinder`）同时获得了该能力。现在没有可安装的 `batch-grill-me`，也没有单独的顺序提问技能；上面的 `CLAUDE.md` 指令就是恢复一次一个问题的方法。

**一次问完一整轮，不就会漏掉前面的答案本应引出的新问题吗？**
这是对按轮设计最常见的质疑，而前沿就是对此的回答：一轮始终只包含互不依赖的问题，因此本轮任何答案都不会使同轮的另一个问题失效。答案仍会重塑所有下游内容：下一轮会重新计算，不是预先写好。损失比“一次问完所有问题”听起来要小，但也并非为零：参见上文前沿的限制。

**它没问题可问后，就开始构建了。**
确认关卡正是为此设置的：前沿清空时，技能还没有完成；你说双方已达成共同理解时，才算完成。能力较弱、速度较快的[模型](https://www.aihero.dev/ai-coding-dictionary/model)仍会违反这条要求；这最常见于较低推理力度或非前沿模型，它们会把“访谈直到达成共同理解”压缩成几个问题加一份大纲。如果你的模型这样做，可靠的修复方法是在自己的 `AGENTS.md` 或 `CLAUDE.md` 中加一条指令，要求 agent 未经许可不得实现。

**它自己回答了问题，而不是问我。**
这是运行中的 bug，不是预期行为，也正是技能文本要区分事实与决策的原因。当另一个技能在“解决这张工单”的任务框架内运行 `grilling` 时，最容易出现这种情况，因为外围任务看起来像是允许不断推进。同一项约束也解释了为什么没有异步模式：有人要求一种读取 GitHub issue 后发布一份整合决策备忘录的变体，但那是另一种技能，因为没有人作答的追问会话产出的是 agent 的意见，而不是你的意见。

**能限制问题数量吗？**
不能，而且上限被明确排除在范围之外。有些计划需要三个问题，有些需要五十个；固定上限要么截断复杂情况，要么在简单情况下显得武断。预期的控制方式是用自然语言引导：告诉它收尾，或停止并接受当前状态的计划。如果会话持续很久，原因通常是范围太大；拆分工作，再逐部分追问。

**我只安装了 `grill-me`，却什么也没发生。**
`grill-me` 是一个只有一行正文的技能，全部内容就是“运行一场 `/grilling` 会话”，所以也需要安装本技能。`grill-with-docs` 同样如此，而且还需要 [domain-modeling](https://aihero.dev/skills-domain-modeling)。安装整套技能可以避免这个问题；选择性安装就意味着也要安装基础技能。

**`grill-with-docs` 运行了，却从没加载 `grilling`。**
这是一个真实且尚未修复的问题，在不同 [agent 运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)和模型中都有报告：技能提到另一个技能，并不能可靠地促使后者加载，而 `grill-with-docs` 提到了两个。明显征兆是：会话一次性问完所有问题，却不附推荐答案；那是模型在即兴访谈，而不是运行本技能。直接问 agent 是否加载了 `grilling` 和 `domain-modeling`，通常可以让它恢复正确流程。

<a id="its-working-if"></a>

## 如何判断它有效

- 每轮以编号列表呈现，每个问题的推荐答案都在独立的 `➡️` 行上，你可以按编号回答整轮。
- 本轮没有问题需要先回答同轮的另一个问题。
- 后续轮次会提出第一轮还无法提出的问题。
- 它会自行查明事实（读取文件、派出子 agent），而不是问你那些它本来可以查到的事情。
- 后台调查不会让整轮停滞；只有依赖调查的问题需要等待。
- 结束时它会停下来，请你确认已达成共同理解，而不是开始工作。
- 问题数量可以很高，轮次数量保持较低。

<a id="where-it-fits"></a>

## 它在流程中的位置

`grilling` 是一个**基础技能**，不是需要排期的步骤：它是访谈技术的唯一权威来源，集中在一处，让每个需要访谈的技能都来使用，而不是另造一套。[grill-me](https://aihero.dev/skills-grill-me) 和 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 是它的两个用户调用入口；`grill-with-docs` 也是主构建流程的起点，位于 [to-spec](https://aihero.dev/skills-to-spec) 之前。[wayfinder](https://aihero.dev/skills-wayfinder) 用它解决决策工单，[triage](https://aihero.dev/skills-triage) 用它把含糊报告追问成可处理的报告，[improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 则在你选定要加深的候选对象之后，用它遍历设计树。不确定哪个入口适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
