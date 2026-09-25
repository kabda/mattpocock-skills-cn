<a id="what-it-does"></a>

## 它能做什么

`improve-codebase-architecture` 调研代码库，寻找**模块加深机会**：浅模块（接口几乎与其隐藏的内容一样复杂）可以变成深模块的位置。它将这些机会写成自包含 HTML 报告，然后围绕你选中的一项进行[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)。

它绝不改变代码。整次运行产出的是操作系统临时目录中的一个 HTML 文件和一场对话；真正的重构随后在独立[会话](https://www.aihero.dev/ai-coding-dictionary/session)中，通过正常构建流程完成。因此它是调研工具，而不是重构工具，也因此适合用在你尚未准备动手修改的代码库上。

两道筛选避免报告变成泛泛的清理建议。每个候选项必须通过**删除检验**：移除该模块，会把复杂性集中到更小接口后，还是只是把它散布到调用方？只有“集中”的情况才配拥有卡片。而且，除非你指定了具体区域，它会先读近期提交历史，优先扫描正在活跃变化的路径，因为加深一个没人碰的代码区域，是永远无法兑现收益的重构。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/improve-codebase-architecture` 调用；[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。

它位于构建循环之外：不是主循环中的步骤，而是定期运行，用来排出更多改善代码库的工作。主要用于四种情况：

| 情况 | 如何使用 |
| --- | --- |
| 日常维护 | 每隔几天或有空时运行，防止功能开发之间结构腐化。 |
| 大型构建之前 | 指向[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)，问“怎样让这项变更更容易？”这是最有效的提示。 |
| 既有项目审计 | 对大型、缺乏结构或通过 [vibe coding](https://www.aihero.dev/ai-coding-dictionary/vibe-coding) 构建的仓库运行，了解其实际状态。 |
| 遗留代码测试工作 | 在给难以测试的代码写测试之前，先用它寻找缺失的 seam。 |

容易与相邻技能混淆的地方：

- 设计已经选定的一个模块，用 [codebase-design](https://aihero.dev/skills-codebase-design)：它是工作台，本技能是找到要放到工作台上的对象的调研。
- 整项工作大到一场会话容纳不下，用 [wayfinder](https://aihero.dev/skills-wayfinder)。
- “这个具体东西坏了”，用 [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs)。如果真正的发现是缺少能通过测试锁定 bug 的合适 seam，它会交回这里。

<a id="prerequisites"></a>

## 前置条件

运行不需要前置条件。如果存在 `CONTEXT.md` 和 `docs/adr/` 下的 ADR，它会读取，并使用领域自己的名词：候选项会写成“加深 Order 接入模块”，而不是“重构 FooBarHandler”。

它会写入两处。报告放在仓库之外的 `<tmpdir>/architecture-review-<timestamp>.html`。追问循环中会向 `CONTEXT.md` 添加或精炼术语，文件不存在则创建；还会提议把被否决的候选项记录为 ADR，避免以后再次推荐。

<a id="depth-and-the-report-that-hunts-for-it"></a>

## 深度，以及寻找深度的报告

技能围绕一个概念运作：**深度**。深模块把大量行为放在小而稳定的接口后。浅模块则通过几乎与底层代码一样宽的接口泄漏实现。报告寻找三种浅层结构：仅为可测试性提取纯函数，真正的 bug 却藏在调用方式中（没有**局部性**）；模块跨 **seam** 泄漏；以及不打开五个文件就无法理解的概念。最后提出通过加深来解决问题的方案。

每个候选项是一张卡片：涉及的文件、阻力、浅显英语描述的方案、用**局部性**与**杠杆效应**说明的收益、改前／改后图示，以及强度徽章。

| 徽章 | 对你意味着什么 |
| --- | --- |
| `Strong` | 明确通过删除检验，而且阻力真实存在。应当认真对待。 |
| `Worth exploring` | 加深方案合理，但收益取决于代码接下来如何发展。 |
| `Speculative` | 为完整性而列出。大多数可以放心忽略。 |

报告以 **Top recommendation（首要推荐）**结束（它会最先处理的那一项），随后技能停下来询问你想探索哪个候选项。此时尚未作出任何决定，也没有改动代码。

<a id="what-happens-after-you-pick-one"></a>

## 选定之后会发生什么

选定候选项后，会围绕它启动一场 [grilling](https://aihero.dev/skills-grilling) 会话：约束、seam 背后放什么、哪些测试保留、加深后的接口应该是什么样子。会话输出是决策，不是 diff。之后走正常流程：把决策带入 [to-spec](https://aihero.dev/skills-to-spec)，然后 [to-tickets](https://aihero.dev/skills-to-tickets)，最后 [implement](https://aihero.dev/skills-implement)。

<a id="common-questions"></a>

## 常见问题

**它围绕一个想法追问了我一小时，却没有给出选项，能关闭吗？**

可以：调用时说明（"don't grill me, just show the report"，即不要追问，只展示报告）。这是本技能最强烈的抱怨。一位用户直言，本来喜欢它是因为“能方便地获得全面的改进分析”，加入追问循环后却觉得“几乎无法使用”，报告说会话提出单一方案后，又问“几十甚至几百个问题”。设计意图是先给报告，只针对你选中的候选项开始追问；但较弱的[模型](https://www.aihero.dev/ai-coding-dictionary/model)会直接就自己第一个想法访谈你。该讨论中的报告随模型差异很大，问题仍未解决：技能还没有文档化的“无追问”模式。

**报告打开后是没有样式、没有图示的原始 HTML，怎么回事？**

报告从 CDN 加载 Tailwind 和 Mermaid，所以打开时需要网络；脚本被阻止时，会静默失效。已登记的案例是安全 hook 要求 SRI hash：agent 加上后，CDN 给浏览器返回的字节与计算 hash 时 `curl` 获取的不同，浏览器便阻止了脚本。离线和受限环境也会遇到同样障碍。agent 看不到这一点，因为它从不渲染页面。应对办法是要求内联 CSS 和手工 SVG 图示，替代 CDN 骨架。这是尚未解决的真实问题。

**它给了十二个候选项，应当在同一会话逐个处理，还是新开会话？**

每场会话一个候选项。在一段对话里处理多个，会让报告、追问、领域模型编辑和代码改动同时塞满[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)。报告只存在临时文件中，因此应当带走候选项本身，而不是文件：选一个、追问、把决策带入 `/to-spec`，其余转成以后可独立处理的[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)。将选定的改进写进规格说明，不要直接实现。这是反复出现的问题，技能本身却没有记录对应工作流。

**应当怎样提示它？**

想着接下来要构建的事情。大型构建即将开始时，指向规格说明并问“怎样让这项变更更容易？”没有指定方向时，它会自行扫描热点，适合日常维护；但明确方向，才能让报告便于行动。

**对大型遗留代码库有效吗？**

部分有效。它擅长处理缺乏一致结构的大型既有代码库，也是一次性结构设置之后推荐的维护机制。需要坦诚补充：项目真正失控的用户报告它“有点帮助，但似乎仍不够”；一位维护八年遗留代码库的开发者报告，模型在其中兜圈子，而同一技能在整洁仓库上能产出清晰图示。目前还没有专门处理这种情况的 `/refactor` 技能。如果代码库完全没有共享词汇，先用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 建立，通常能显著改善本技能的输出。

**这与 `/codebase-design` 有什么区别？**

`/codebase-design` 是参考，不是会话驱动者。它提供词汇（模块、接口、深度、seam、适配器、杠杆效应、局部性），本技能借用这些词汇。让新 agent 把 `/codebase-design` 当作要“执行”的事情，是已知失败模式：它没有自己的流程，agent 就会发明一个，重新探索代码，运行很久才问你任何问题。用本技能驱动，把另一个作为参考。

**它会告诉我代码库已经很好了吗？**

很少，开始前应当知道这一点。技能的设计是输出发现，因此这个框架会推动它生成候选项，而不是得出“没有问题”的结论。强度徽章是防线：如果报告全部是 `Speculative`，那就是技能用自己唯一知道的方式告诉你，它什么也没找到。

**在 Codex 或其他运行环境中能工作吗？**

部分可以。探索步骤直接指定 Claude Code 的 `Agent` 工具和 `subagent_type=Explore`，所以没有该工具的[运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)可能跳过并行探索，而不是换成自己的工具。技能仍可运行，只是扫描不够彻底。已有与运行环境无关的改写提案，但尚未合并。

**究竟如何在 TypeScript 中实现深模块？**

技能没有随附好的答案。反复出现的请求是提供 `TYPESCRIPT.md`，为这些原则给出具体文件和模块布局，但它不存在。技能会告诉你哪里适合加深、seam 背后应当放什么；将其转成包或目录结构，目前仍由你负责。

<a id="its-working-if"></a>

## 如何判断它有效

- 候选项使用领域概念，而不是编造类名：“Order 接入模块”，不是“FooBarHandler”。
- 候选项集中在最近编辑的文件，而不是仓库中沉睡的角落。
- 运行期间没有代码改变。唯一新文件是临时目录中的 HTML 报告。
- 报告之后停下来问你要哪个候选项，而不是自行继续。
- 每张卡片用局部性或杠杆效应说明收益，并指出哪些测试会更简单，而不只是“这样更干净”。
- 基于持久理由否决候选项时，它会提议记录 ADR，避免下次重复建议。

<a id="where-it-fits"></a>

## 它在流程中的位置

`improve-codebase-architecture` 是**定期维护**：每隔几天在任何流程之外运行，用来排出工作，而不是执行工作。相邻技能包括 [codebase-design](https://aihero.dev/skills-codebase-design)，拥有描述每个候选项所用的深度与 seam 词汇；[grilling](https://aihero.dev/skills-grilling)，在选定候选项之后遍历决策树；以及 [domain-modeling](https://aihero.dev/skills-domain-modeling)，在决策明确时保持 `CONTEXT.md` 和 ADR 最新。它产出的是想法，通过 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 或 [to-spec](https://aihero.dev/skills-to-spec) 重新进入主构建流程。要判断某种情况适合哪个技能，[ask-matt](https://aihero.dev/skills-ask-matt) 是整套技能的路由入口。
