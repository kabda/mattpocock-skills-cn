<a id="what-it-does"></a>

## 它能做什么

`implement` 实现已经决定好的工作。你把一张[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)、一份[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)，或刚在对话中商定的计划交给它，它就会写代码、在 seam 上驱动 [tdd](https://aihero.dev/skills-tdd)、过程中进行类型检查、结束时运行 [code-review](https://aihero.dev/skills-code-review)，并提交到当前分支。

它绝不会重新讨论计划。没有访谈、澄清轮次，也不会提议其他方案。上游确定的内容就是输入，技能的全部职责就是把它变成一次提交。这与对一个新 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 说“构建这个”不同，后者很可能边构建边重新设计工作。

<a id="when-to-reach-for-it"></a>

## 何时使用

由你亲自输入 `/implement` 调用它：agent 不会自行使用。它带有 `disable-model-invocation: true`，因此其他技能也不能调用它。[ask-matt](https://aihero.dev/skills-ask-matt) 或 [to-tickets](https://aihero.dev/skills-to-tickets) 中凡是写着“然后针对每张工单运行 `/implement`”，都是给你的指令，不是 agent 会自行执行的操作。

工作当前存放在哪里，决定了本技能是否合适：

| 工作目前是…… | 使用 |
| --- | --- |
| 跟踪器中的一张工单 | `/implement #42`，每场[会话](https://www.aihero.dev/ai-coding-dictionary/session)一张工单，工单之间[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)上下文 |
| 尚未拆分的规格说明，构建需要跨多场会话 | 先用 [to-tickets](https://aihero.dev/skills-to-tickets)，再对每张工单运行 `/implement` |
| 一份规格说明，且构建规模很小 | 直接对规格说明运行 `/implement` |
| 只存在于刚才的对话中，且仍然很小 | 就在当前窗口、同一段对话中运行 `/implement` |
| 还没有记录到任何地方 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)；没有代码库时用 [grill-me](https://aihero.dev/skills-grill-me) |
| 一个想用测试优先方式实现的具体行为，没有规格说明 | 直接用 [tdd](https://aihero.dev/skills-tdd) |
| 已经构建完成，想检查一下 | 直接用 [code-review](https://aihero.dev/skills-code-review) |

同一会话中的情况值得单独说明，因为技能自己的第一行没有覆盖它。`SKILL.md` 写的是“规格说明或工单”，这会促使[模型](https://www.aihero.dev/ai-coding-dictionary/model)去寻找一个并不存在的文件。如果计划只在对话中，调用时请明确说明。

<a id="prerequisites"></a>

## 前置条件

`implement` 会提交到你当前所在的分支。它不会创建分支，也不会询问。开始之前，请检查当前分支就是你希望放置这些工作的分支。

如果工单来自 [to-tickets](https://aihero.dev/skills-to-tickets)，其所在跟踪器已由 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 配置。`code-review` 在收尾时读取相同配置，查找原始规格说明。

<a id="what-one-run-does"></a>

## 一次运行做什么

一次运行依次包含五个环节：

1. 阅读工单或规格说明，弄清 seam。
2. 在事先约定的 seam 上驱动 [tdd](https://aihero.dev/skills-tdd)，一次一个 red-green 切片。
3. 经常进行类型检查，过程中运行单个测试文件。
4. 结束时运行一次完整测试套件。
5. 运行 [code-review](https://aihero.dev/skills-code-review)，然后提交到当前分支。

一次运行覆盖一张工单。[to-tickets](https://aihero.dev/skills-to-tickets) 产出的工单是曳光弹式纵向切片，大小适合一个全新的[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)，因此预期节奏是：清空上下文、实现一张工单、提交、再次清空。每张工单都自包含，所以前一张工单的上下文可以丢弃。

<a id="pre-agreed-seams"></a>

## 事先约定的 seam

支撑本技能的概念是 **seam**：无需探入内部即可观察行为的公共边界。测试位于 seam 上。在编写任何代码之前约定 seam，并在该处工作，才能让测试持久有效，因为底层实现可以重写，而测试无需改动。

“事先约定”这几个字承担着实际作用，同时也是本技能最薄弱的连接处。`implement` 内部没有约定 seam 的步骤。负责询问的是 `tdd`，它拒绝在未经确认的 seam 上编写测试。因此实践中，约定要么发生在上游规格说明中，要么发生在运行开始时的第一次交流中。如果两处都没发生，前置条件就始终没有触发，运行会悄悄变成“直接写代码”。在规格说明中明确列出 seam，才能阻止这种情况。

<a id="common-questions"></a>

## 常见问题

**它完成了，但工单仍然开放，验收标准也没有勾选。**

没错，这符合预期。`implement` 没有完成工单的步骤。它在提交后结束，绝不会触碰工作项；这一点已在 GitHub Issues 和本地 Markdown 跟踪器中得到确认，因此不是跟踪器集成问题。它也不会处理 `code-review` 产出的发现，不会勾选原始 issue 中的 `- [ ]` 复选框。你需要自己关闭工单并核对标准。依赖链受到的影响最大，因为 `to-tickets` 将前沿定义为所有阻塞项均已关闭的工单。如果什么都不关闭，就永远看不到任何工单解除阻塞。

**能一次把所有工单交给它，或并行运行几个吗？**

不能。一次调用，一张工单。针对工单队列的批量分派和[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)并行展开都被反复请求过，但都还不存在。在同一个 checkout 中并排运行多个 `/implement` 会话，比“不受支持”更糟：一份实际报告描述了同一下午、三个 issue 中发生的事故：某个会话的 `git commit --amend` 改到了另一个会话的提交，stash 从 `refs/stash` 消失，提交落到错误分支。这些会话共享一个工作目录、一个索引和一个 HEAD。社区的应对办法是 Git worktree；但要注意，`refs/stash` 在 worktree 之间也共享，所以仅有 worktree 无法解决 stash 问题。如果现在就要并行，只能自行组装流程。

**它能创建 pull request，而不是直接提交吗？**

没有内置支持。它直接提交到当前分支，有些人认为过于急切：还没来得及验证代码是否工作，就已经提交了。没有配置开关，也没有 PR 模式。人们会在调用中覆盖要求（“提交到一个分支并创建 PR”），或编辑本地技能副本。

**`code-review` 说看不到我的改动。**

`code-review` 审查的是 `git diff <fixed-point>...HEAD`，不包含暂存区和工作区改动。`implement` 在提交之前运行它，因此除非已经有中间提交，否则这个 diff 中没有任何可审查内容。多个人报告过，两边都尚未修复。先提交，再相对于分支创建时的基准点进行审查。

另外，有些人刻意不希望在运行内部做审查，因为 agent 审查自己刚写的代码，会偏向自己的方案。在新会话中对固定基准点运行 [code-review](https://aihero.dev/skills-code-review) 是合理的替代方式；这也正是该技能用独立子 agent 执行两个审查维度的原因。

**一张工单消耗了 150k token，是我用错了吗？**

更可能是工单太大，而不是技能用错了。一次运行包括代码库探索、每个 seam 上的 red-green 循环、完整测试套件和审查，因此非简单工单超过 100k [token](https://www.aihero.dev/ai-coding-dictionary/token) 属于正常情况，不代表哪里坏了。调整点在上游：在 [to-tickets](https://aihero.dev/skills-to-tickets) 中合理划分工单，让每张都适合一个全新窗口。如果某张工单持续超出承载范围，应当拆分它，而不是提高[推理力度](https://www.aihero.dev/ai-coding-dictionary/effort)。

**在新会话中运行 `/implement #2`，却做了完全无关的事情。**

`#2` 会相对于 agent 能看到的编号列表解析；在新会话中，这可能是待办文件、检查清单或另一份工作列表，而不是已配置的跟踪器。解析方式是自信地选定，而不是遇到不确定就停止，所以往往开始之后才发现错误。请传入完整引用、issue URL 或 `owner/repo#2`，并要求开始前复述标题供你确认。

<a id="its-working-if"></a>

## 如何判断它有效

- 会话从阅读工单或规格说明、复述将要构建的内容开始，而不是问你要构建什么。
- 运行记录中能看到实际的 `/tdd` 调用，而不只是 diff 中出现测试。
- 过程中反复运行类型检查和单个测试文件，在接近结束时运行一次完整套件。
- 无需你催促继续，运行就能在当前分支产生一次提交。
- diff 的范围等于一张工单：贯穿各层的纵向切片，而不是把几张工单混在一起。

<a id="where-it-fits"></a>

## 它在流程中的位置

`implement` 是主流程的构建步骤，位于倒数第二位：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

它的相邻技能是 [to-tickets](https://aihero.dev/skills-to-tickets)，产出它使用的工单，并声明决定执行顺序的阻塞关系；[tdd](https://aihero.dev/skills-tdd)，由它在每个 seam 上内部驱动；以及 [code-review](https://aihero.dev/skills-code-review)，在提交前运行。它位于规划技能的下游，并信任这些技能。它不会重新验证交付给它的工作形态，所以结构不良的地图或按横向技术层划分的工单，也会被照原样实现。

正因为这种信任，[wayfinder](https://aihero.dev/skills-wayfinder) 会在 [to-spec](https://aihero.dev/skills-to-spec) 处接入主流程，而不是将地图直接循环交给 `implement`。只有工作量最终确实很小时，才从地图直接进入 `implement`。

不确定自己处于哪条流程时，[ask-matt](https://aihero.dev/skills-ask-matt) 是整套技能的路由入口。
