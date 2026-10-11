<a id="what-it-does"></a>

## 它能做什么

`research` 通过阅读对答案负责的原始来源来回答问题，然后在仓库中留下一份带引用的 Markdown 文件。它只使用**[一手来源](https://www.aihero.dev/ai-coding-dictionary/primary-source)**：官方文档、源代码、规格说明、第一方 API。它会将每项断言追溯到所属的原始来源，因此只要 API 自己的文档可访问，就不会复述博客对 API 的解读。

它不会在对话中回答你。输出是一个文件，写在仓库已有的此类笔记存放位置，每项断言都附链接。重点就在这里：得到一份可供反馈、交给另一个 agent 或直接丢弃的文档，而不是一段随[会话](https://www.aihero.dev/ai-coding-dictionary/session)结束而消失的回答。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/research`，或者当任务转为阅读调查时，由 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 自动使用。

当下一步是从工作目录之外*查明某件事*（第三方 API 如何运行、规格说明究竟写了什么、某个版本声明是否成立），而你不想让自己的对话停下来做阅读时使用。需要什么，决定了选择哪个技能：

| 你的需要 | 使用 |
| --- | --- |
| 某个决策正在等待的外部事实 | `research` |
| 通过访谈*与你一起*作出决策 | [grilling](https://aihero.dev/skills-grilling) |
| 持久的架构决策，记录到 `GLOSSARY.md` 和 ADR 中 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 查明某种方案在代码库中是否可行 | [prototype](https://aihero.dev/skills-prototype) |
| 大到一场会话容纳不下的计划 | [wayfinder](https://aihero.dev/skills-wayfinder) |

`research` 与 `grill-with-docs` 的分界是**产出内容的保质期**。研究产出短期材料：截至本周，这个库的认证机制如何工作。ADR 记录你会保留的决策。如果你产出的是决策而不是事实，你做的是[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)，而不是研究。

<a id="delegated-legwork"></a>

## 委派阅读调查

关键做法是让阅读作为**后台 agent**运行。你继续工作；它独立调查，将每项断言追溯到一手来源，写成一个 Markdown 文件，然后汇报。研究是可以委派的调查工作，而不是把思考外包：你得到一份可用于追问、规划或设计的文档，决定仍由你作出。

委派没有防护限制，后台 agent 还可以再启动自己的后台 agent。这是本技能记录最充分的问题。

文件保存在哪里由仓库决定，而不是技能决定：遵循已有的笔记约定；没有约定时，选一个合理位置并告诉你。每次运行写一个文件。

<a id="common-questions"></a>

## 常见问题

**它启动了第二个研究 agent，这是预期行为吗？**

不是。这是一个尚未解决的 bug，[issue #530](https://github.com/mattpocock/skills/issues/530)。技能要求调用方启动后台 agent，却没有限制 agent 类型，因此启动的是 `general-purpose` agent，它拥有 `Agent` 工具和同样的指令，又执行了一遍。一位报告者测得，单次研究任务在三次重叠运行中消耗了大约 450k [token](https://www.aihero.dev/ai-coding-dictionary/token)，重复任务在半小时后才完成，整个过程都不在视野中。Claude Code 之外也会复现；同样的嵌套已在使用 GPT-5.6-sol 的 Codex 中确认。目前没有已发布的修复。用户会修改本地安装副本，添加一条指令：如果已经是[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)，就自行完成工作。这有帮助，但属于指令层面的修补，不是结构性修复。调用后请观察后台任务列表，停止重复任务。

相反的失败情况也存在：如果全局指令禁止 agent 再次委派工作，后台 agent 会礼貌地拒绝任务，技能便悄悄地什么也没做。

**文件应该放在哪里，要提交吗？**

技能把文件放在仓库已有的笔记位置，除此之外没有立场。社区的意见比较一致：ADR 要保留，研究文件不要保留。Discord 上针对这个问题的讨论中，最鲜明的说法是：“ADR 要留。其他内容完成后归档或删除。否则就会成为工作残留；如果你已经偏离原来的规格说明／研究，它还可能污染以后的仓库阅读。”研究文件记录的是写作当天成立的事实，因此过时的文件比没有还糟。综合而言，这些交付物并不真正适合放进 Git，也没有统一的存放位置：有人改用 Obsidian、独立知识仓库或 issue 跟踪器。

**什么算“高可信度”的一手来源，由谁决定？**

由[模型](https://www.aihero.dev/ai-coding-dictionary/model)决定。技能列出了符合条件的来源*种类*（官方文档、源代码、规格说明、第一方 API），但没有白名单、域名门槛或验证步骤。这是技能最初被提出时最响亮的质疑，而且从未得到公开解答：“五个研究子 agent 都指向垃圾来源，只会更快地给出五个自信的错误答案。你们如何把关什么才是高可信度来源？”你真正拥有的缓解手段，是每项断言后的引用。点开其中两三个。如果到达的是对某事物的摘要，而不是该事物本身，这次运行就在唯一的职责上失败了。

**后续会话会复用之前研究得到的内容吗？**

不会。没有任何机制自动加载过去的研究文件；它只是放在仓库中的文档，直到有人或某个技能指向它。早期有人将此作为对设计最有力的挑战：“价值在于 Markdown 变成 agent 后来会重读的上下文，而不是获取本身。写一次就死掉的文件，只是花哨的搜索。”已经提供的技能没有解决这个问题。实际中，文件通过有意传入下一步才体现价值：附到规格说明中、在追问会话中引用，或让[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)指向它。

**为什么不直接让 agent 去读文档？**

可以，而一段两行的提示词正是本技能取代的旧做法。相比提示词，技能提供两点价值：在后台运行，让会话[上下文](https://www.aihero.dev/ai-coding-dictionary/context)保持干净；一手来源约束和带引用的文件输出每次都一致，而不取决于你碰巧如何措辞。与 [agent 运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)自身的深度研究模式相比，区别在于交付物与来源纪律，而不在搜索。如果一个小问题用两行提示词就能解决，那就用两行提示词。

**什么时候停止阅读？**

技能没有停止标准，这表现为两类看似相反、实际来自同一缺口的抱怨：有些 agent 钻得过深，有些则泛泛覆盖主题，却漏掉唯一重要的具体细节。一位使用者说：“深度研究技能有时有点过深。而让 agent 研究，通常又会漏掉关键细节。”范围控制由你负责。一个狭窄、可回答的问题（一个 API、一种行为、一项版本声明），结果远好于“研究 X”。

**`/wayfinder` 创建了研究工单，需要我自己解决吗？**

不用，现在会自动启动。在 v1.1 之后尚未发布的改动中，绘图会话为每张研究工单启动一个 `/research` 子 agent，并行运行。各自把发现记录在一次性的 `research/<name>` 分支，通过工单中的[上下文指针](https://www.aihero.dev/ai-coding-dictionary/context-pointer)引用。研究工单是 wayfinder 每会话一张工单规则的唯一例外，因为它们是 [AFK](https://www.aihero.dev/ai-coding-dictionary/afk)，不需要等待你。一项已知问题是之后删除分支会破坏工单指针。

<a id="its-working-if"></a>

## 如何判断它有效

- 你自己的会话仍在继续。如果你坐在那里看它阅读，就说明委派没有发生。
- 恰好出现一个新后台任务。第二个名称几乎相同的任务，说明发生了嵌套 bug。
- 仓库原本用来存笔记的目录中出现一个新 Markdown 文件，agent 告诉你路径。
- 文件中的每项断言都有链接，随机打开两个，会到达官方文档、规格说明或实际源文件，而不是他人的解读。
- 仅凭文件就能作出之前受阻的决策，无需自己再次回到来源查阅。

<a id="where-it-fits"></a>

## 它在流程中的位置

`research` 是随时可用的独立工具，为思考类技能提供输入，而不位于构建流程内部。它的文件是要带*入*流程的材料：当事实已经摆在面前，[grilling](https://aihero.dev/skills-grilling) 与 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 能提出更有力的问题，[to-spec](https://aihero.dev/skills-to-spec) 也可以据此综合整理。[wayfinder](https://aihero.dev/skills-wayfinder) 是唯一直接调用它的技能，用 `/research` 子 agent 解决地图上的每张研究工单。完整地图见 [ask-matt](https://aihero.dev/skills-ask-matt)。
