<a id="what-it-does"></a>

## 功能

`writing-for-agents` 是编写面向 agent 的文档时所依据的参考：技能、`AGENTS.md` / `CLAUDE.md`、[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)、运行时提示词、README，以及任何 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 会读的文档。封装方式不同，写作方法相同：相同的着力点让它们可预测，使 agent 每次采用相同的*过程*，而非生成相同的输出。

它的默认动作是删除，不是解释。让 agent 为另一 agent 写指令，它会用大多数篇幅解释[模型](https://www.aihero.dev/ai-coding-dictionary/model) 已知的东西。这些行每一行都是 **no-op**，付出[上下文](https://www.aihero.dev/ai-coding-dictionary/context) 却不改变行为。本参考用来识别它们，因此它对已有文档的价值至少不亚于对空白文件的价值。

v1.1 之前它叫 `writing-great-skills`。改名反映了它一直以来的本质：几乎没有内容是技能专属的。只有技能机制（frontmatter、模型调用或用户调用的选择、路由技能）被移到链接的 `SKILL-MECHANICS.md`，仅在面前的文档是技能时才阅读。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/writing-for-agents`，或者在创建、编辑技能，或修改 `AGENTS.md`、`CLAUDE.md` 时由 agent 自行使用。

其他供 agent 阅读的内容，手动调用：文档、规格说明、[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)、系统提示词和 [AFK](https://www.aihero.dev/ai-coding-dictionary/afk) 提示词。判据只有一个问题：agent 会读它吗？文档如何到达它面前并不重要，无论是指针引用、人粘贴，还是只放在仓库里。要先弄清代码库实际包含什么，用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)；本参考管文档如何表达，不管它知道什么。

<a id="the-two-loads"></a>

## 两种负荷

整个参考围绕一对预算展开，每份文档和每个指针都会消耗它们：

- **上下文负荷**：始终加载的材料对 agent 窗口的成本：一行 `AGENTS.md`、技能描述，或无论触发与否、每一[轮](https://www.aihero.dev/ai-coding-dictionary/turn) 都待在上下文中的内容。
- **认知负荷**：你承担的成本，即有哪些文档、何时使用哪份。你就是索引。这不是需要最小化的成本，而是人掌握自主权的代价。

一旦用这两种负荷思考，大部分写作决策（拆不拆、内联还是披露、用指针还是直接放入）就成了在不同地方作出的同一种取舍。

<a id="the-levers"></a>

## 着力点

- **[上下文指针](https://www.aihero.dev/ai-coding-dictionary/context-pointer)**：保存在上下文中的引用，指明上下文之外的材料及其访问时机。技能 description 和 `AGENTS.md` 中指向文档的一行是同一种东西；决定 agent 多可靠地沿指针访问的是其*措辞*，不是目标。
- **信息层级**：从文件内步骤，到文件内参考，再到指针之后按需披露参考的阶梯。**[渐进披露](https://www.aihero.dev/ai-coding-dictionary/progressive-disclosure)** 是沿阶梯下移，使顶层保持清楚。
- **完成标准**：每个步骤完成条件的清晰度与要求力度，以及力度驱动的**调查工作**；用于防御**过早完成**。
- **引导词**：模型预训练中已存在的紧凑概念（*tight*、*red*、*tracer bullet*），agent 执行文档时借助它思考。它两次锚定：正文中锚定执行，指针中锚定调用。
- **修剪**：唯一权威来源、相关性，以及逐句应用的 no-op 判据，用来应对**重复**、**沉积**和**蔓延**。

<a id="common-questions"></a>

## 常见问题

**`/writing-great-skills` 去哪了？**
就是本技能，v1.1 改了名。早在名称追上之前，实践者就把它用于 `AGENTS.md`、文档、规格说明、工单和运行时提示词；结构、引导词和修剪，原来是所有 agent 阅读文本的写作技艺。没有别名。请按新名称重新安装。

**“Writing for agents”：是让 agent 来写吗？**
恰好反过来。你是作者，agent 是读者。这正是这种文体的难点：你面对的是已经读过一切的读者，因此解释是浪费，精确才是全部工作。

**不能直接让 agent 帮我写吗？**
可以，但它会写得冗长。无人干预时，模型会解释它已经知道的东西，不会自行应用 no-op 判据，也不会主动寻找引导词。用本参考审阅草稿：大部分价值体现在审查这一轮。

**我让 agent 精简文档，它把功能删掉了。**
被要求“精简”的 agent 会优化长度，因为长度是它看得见的东西。no-op 判据关乎行为，不关乎美感：删掉一行，再问 agent 行为是否改变。句子不通过判据时，删除整句，不要只删词；意见不同则通过运行文档解决，而非争论。

**怎么知道何时完成？**
当它能工作，而且再也找不到重复、沉积或 no-op 时。这里没有自动评估；检查方式是手动运行，加上失败模式词汇作为诊断。文档行为异常时，这套词汇也是修理工具：先说清失败模式，再修复它。

**这该放在 `CLAUDE.md`，还是别处？**
问自己愿意支付哪种负荷。`CLAUDE.md` 无条件加载到每个[会话](https://www.aihero.dev/ai-coding-dictionary/session)；指针后的材料在触发前只付出指针那一行的成本。只在十种情境之一适用的内容，其他九次也都在支付上下文负荷。

**每出一个新模型，都要重写文档吗？**
大多不用，过度适配单一模型本身也是陷阱。针对新模型更新通常只是再做一轮 no-op 检查，而非重写。

**我的技能只对提炼它时那一个具体任务有效。**
常见路径（先做一次工作，再让 agent 把它写成技能）会过度依赖那一次运行，示例变得过于具体。保留该次运行作为证据，再有意识地抽象：剥离属于那个仓库和那些文件的内容，面向任务类别编写。

**英语不是我的母语，会失去引导词优势吗？**
不会。找到用最少 [tokens](https://www.aihero.dev/ai-coding-dictionary/token) 承载最多行为的词，正是本参考会帮助你做的工作，也是它的用途之一。

<a id="its-working-if"></a>

## 有效运行的迹象

- 文档越好越短，剩下的内容少得令人意外。
- 能指出某个引导词，并看到它在多处发挥作用。
- 没有任何内容以任何形式陈述两次。重复是文档从未测试过的最可靠信号。
- 只有某条分支需要的参考放在指针之后，而非主文件中。

<a id="where-it-fits"></a>

## 所处位置

这是随时可用的独立参考，适用于整套技能，而非其中一项。各技能都按它编写；其他技能产出的文档（`GLOSSARY.md` 和 ADR、规格说明、工单）需要 agent 阅读时也由它规范。唯一直接调用方是 [retro](https://aihero.dev/skills-retro)，在建议引导文件或技能前加载它。不确定任务需要哪项技能时，由 [ask-matt](https://aihero.dev/skills-ask-matt) 路由。
