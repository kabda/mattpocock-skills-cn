<a id="what-it-does"></a>

## 功能

`triage` 处理项目跟踪器上的 issue，让每项经过一个由**分流角色**（类别角色和状态角色）组成的小型状态机，最终留下 agent 可直接接手的简报、给报告者的具体问题，或带有原因记录的已关闭 issue。

它仅用于**不是你创建的** issue。未经整理的 bug 报告、收到的功能请求、突然出现的外部 pull request：从外部进入跟踪器、保持报告者原貌的工作。[to-tickets](https://aihero.dev/skills-to-tickets) 生成的[工单](https://www.aihero.dev/ai-coding-dictionary/ticket) 天生已经适合 agent 接手，再做 `triage`，最好的结果也只是浪费工作。规则很明确：`/triage` 仅用于收到的 issue，不用于你自己创建的 issue。

它与手动打标签的第二个区别是：先建议，再等待。它说明所建议的类别、状态及理由，以及在代码库中的发现；在你指示之前，不应用任何变更。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/triage`，再用普通语言描述需求即可调用。[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。“显示所有需要我关注的事项”“看看 #42”“把 #42 移到 ready-for-agent”。

| 你手上的内容 | 去哪里 |
| --- | --- |
| 跟踪器里堆满别人提交的原始报告 | `/triage` |
| 自己的粗略想法，还没写下来 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 已经讨论清楚，需要转成[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec) | [to-spec](https://aihero.dev/skills-to-spec) |
| 要拆成 agent 可接手工单的规格说明 | [to-tickets](https://aihero.dev/skills-to-tickets) |
| 已确认的 bug，需要找根因而非打标签 | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |

<a id="prerequisites"></a>

## 前置条件

`triage` 会读写 issue 跟踪器，因此必须先由 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 配置跟踪器和标签词汇。下面的角色名是**规范名称**；你的跟踪器可能使用不同标签字符串，setup 会提供映射。如果跟踪器已经精确使用规范名称，就无需映射，也无需设置。

跟踪器配置还决定是否将外部 pull request 视为请求入口，以及谁算外部作者。该标志默认关闭，也不再作为 setup 问题询问；如果希望把 PR 纳入范围，请在 `docs/agents/issue-tracker.md` 中切换。

<a id="the-state-machine"></a>

## 状态机

每项经过分流的事项，最终恰好带一个类别角色和一个状态角色。两个类别是 `bug`（某处出故障）和 `enhancement`（新功能或改进）。五个状态：

| 状态 | 含义 |
| --- | --- |
| `needs-triage` | 需要你评估。无标签 issue 通常首先进入这里。 |
| `needs-info` | 等待报告者。收到回复后回到 `needs-triage`。 |
| `ready-for-agent` | 规格已完整，附有 agent 简报。[AFK](https://www.aihero.dev/ai-coding-dictionary/afk) agent 可以接手。 |
| `ready-for-human` | 同样的简报，另加无法委派的原因：判断、外部访问、手动测试。 |
| `wontfix` | 已关闭，并记录原因。 |

这就是全部词汇。“恰好一个状态角色”的不变量让查询保持简单。它也是这项[技能](https://www.aihero.dev/ai-coding-dictionary/skill) 最常收到请求的领域：用户希望增加第六种状态，用于规格已定却被其他 issue 阻塞的工作；希望用 `deferred` 表示等待未来触发条件的工作；也希望有终态 `implemented`。这些都尚未发布。参见下方问题。

`wontfix` 分三种情况，区别很重要，因为只有一种会写入知识库：

| 关闭原因 | 会发生什么 |
| --- | --- |
| 已实现 | 评论指出已有实现的位置。不写入 `.out-of-scope/`，因为这是已构建而非被拒绝的功能，记录进去会污染去重检查。 |
| 被拒绝的 bug | 礼貌解释，然后关闭。 |
| 被拒绝的 enhancement | 在 `.out-of-scope/` 写文件，关闭评论链接到它，然后关闭。 |

`.out-of-scope/` 按被拒绝的**概念**保存 Markdown 文件，而非按 issue。文风是简短设计文档，而非数据库行：拒绝了什么、为什么，以及所有提出过它的 issue。`triage` 在评估任何事项前都会读取整个目录，按概念而非关键词匹配，所以“夜间主题”会匹配 `dark-mode.md`。找到匹配项时，它呈现旧决策，询问你是否仍持相同看法，而不是从头争论。

<a id="verify-before-you-brief"></a>

## 先验证，再写简报

任何[追问](https://www.aihero.dev/ai-coding-dictionary/grilling) 之前，`triage` 都会检查说法是否属实。对于 bug，按报告者步骤复现；对于 PR，检出分支并运行相关测试。然后报告三种结果之一：已确认并附代码路径；未能复现；信息不足，无法尝试，而这本身就是最强的 `needs-info` 信号。

同一轮还会对照代码库做两项检查：**重复性**（是否已实现，按领域概念而非报告者措辞搜索）和**既往拒绝**（`.out-of-scope/` 是否已否定它）。两项成本都很低，命中时都会得出 `wontfix`。

这一切都为做好一个产物：**agent 简报**，即 issue 转到 `ready-for-agent` 时发布的结构化评论。一经发布，简报就是契约，原报告仅提供上下文。简报追求**持久有效**，而非位置精确，因为 issue 可能在 `ready-for-agent` 停留数周，底下的代码一直变化。因此它指明类型、签名和行为契约，绝不指明文件路径或行号。确认过的复现比猜测能支撑可靠得多的简报。

<a id="a-pr-is-an-issue-with-attached-code"></a>

## PR 就是附带代码的 issue

跟踪器将外部 pull request 视为请求入口时，它们经过相同状态机，使用相同类别、状态和转换。只是状态针对 diff 解读：`ready-for-agent` 表示已附简报，应由 agent 对代码采取下一步行动；`ready-for-human` 表示已可由人合并。PR 简报描述对现有 diff 还要做什么，而不是如何从零构建。

发现阶段只显示*外部* PR，因为协作者正在处理的分支不是分流工作。该过滤只作用于发现阶段；明确指定 PR 时，无论谁写的都要分流。有一个粗糙之处：GitHub 模板的外部 PR 列表命令向 `gh pr list` 请求 `gh` 并未提供的 `authorAssociation` 字段，所以原样运行会直接失败（[#468](https://github.com/mattpocock/skills/issues/468)）。

<a id="common-questions"></a>

## 常见问题

**我运行了 `/to-spec` 和 `/to-tickets`，现在这些工单还没分流。要对它们运行 `/triage` 吗？**
不要。它们已经可以交给 agent，因为 `to-tickets` 发布时会应用 `ready-for-agent` 标签，正是为了让 AFK 执行器无需额外处理就能接手。遇到这个问题的用户运行了规格流程，看到输出带 `needs-triage`，结果 AFK 执行器全都忽略了。`triage` 是外来工作的入口支路；规格流程是你自己发起工作的通道。两者在 `ready-for-agent` 汇合，而非更早。

**现在有了 `to-spec` → `to-tickets` → `implement` 流程，`triage` 还有用吗？**
只有存在外来工作时才有用。`triage` 比这条主线更早，职责也不同：它是处理他人报告的通道。如果跟踪器中所有事项都来自你自己的规划，你很少会打开它。如果维护公开项目，或团队向你报告 bug，它就是前门。主要场景是开源仓库接收外部贡献者的 issue。

**agent 尝试应用 `ready-for-agent`，但 `gh` 说标签不存在。**
这是已知未关闭 bug（[#616](https://github.com/mattpocock/skills/issues/616)）。`setup-matt-pocock-skills` 把标签词汇写入 `docs/agents/triage-labels.md`，却不在跟踪器中创建标签。用 `gh label create` 或跟踪器 UI，自己一次性创建五个状态标签和两个类别标签，就不会再出现。issue 链接了一个社区修复分支，尚未合并。

**五种状态不够：被阻塞、推迟、已实现怎么办？**
这是该技能最常被报告的缺口，分三种情况。规格完整却等待另一个 issue 关闭的事项（[#139](https://github.com/mattpocock/skills/issues/139)），报告者认为此时 `ready-for-agent` “技术上没错”却误导人，agent 接手就碰壁。计划要做但尚不可行动、需等待触发条件的未来工作（[#297](https://github.com/mattpocock/skills/issues/297)）。以及“已实现，等待验证”的终态；没有它，AFK 执行器可能把已完成工单重新排队。Matt 承认阻塞场景确实存在，但还没决定名称（`blocked` 或 `paused`）。这些都尚未发布。常见变通是在类别之外加仓库本地标签，让规范状态槽位仍使用如实描述情况的状态，代价是技能并不知道额外标签。有个社区衍生版走得更远，增加了 `needs-slicing`、`tracking` 和工作量标签。那样可用，但属于他们的版本，不属于本技能。

**这与 `/diagnosing-bugs` 有什么不同？**
这里的验证刻意保持浅层（足以回答“这是真的吗，大致在哪里”），不负责找根因。若按报告者步骤几分钟内无法复现，诚实的做法是 `needs-info`；如果想现在追查，就用 [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs)。目前两项技能正文都没提到对方；用户发现了这个衔接缺口，它仍未解决。

**能否让它处理整个积压列表，自动跑完？**
可以要求，但要留意它读了什么。“展示需要关注的事项”是成本很低的列表查询，用于*选择*：你挑一个，再为选中的项收集完整[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。一次处理二十个 issue，agent 可能悄悄退回用那份简略列表作为证据，而该列表只有正文，没有评论。有用户恰好遇到过：三个 issue 已有“已修复，建议关闭”的评论，却全部被重新写了 agent 简报。想批量处理时，明确要求逐个读取评论。

**支持 Linear 或 GitHub Issues 之外的工具吗？**
支持，跟踪器是配置，不是硬编码假设。有人配合 Linear（通过 `linear` CLI）、GitLab，以及 `.scratch/` 下的普通 Markdown 文件使用。常见分工是 Linear 管 issue 和规划，GitHub 管代码和 PR：提到“issue tracker”的技能映射到 Linear，提到“PR”的技能映射到 GitHub。本地 Markdown 跟踪器有一个尚未修复的模板 bug：生成文件可能两次包含验收标准，一次在顶层，一次在 agent 简报内部（[#200](https://github.com/mattpocock/skills/issues/200)）。

<a id="its-working-if"></a>

## 有效运行的迹象

- 每个处理过的事项最终恰好带一个类别角色和一个状态角色，不会缺失，也不会出现两个冲突状态。
- 它给出有理由的建议后停下，而不是改完标签就继续。
- 进入 `ready-for-agent` 前，bug 已复现，或 PR 已检出并运行。
- 简报描述类型和行为，不含文件路径或行号。
- 六个月前被拒绝的请求再次出现时，它会指出这一点并引用旧理由，而非重新分流。
- 每条发布的评论都以 `> *This was generated by AI during triage.*` 开头。

<a id="where-it-fits"></a>

## 所处位置

`triage` 是**入口支路**，不是主链条的一步。主流程始于你自己的想法（追问、规格说明、工单、实现、审查），`triage` 则是外来工作的并行通道。两者汇入同一处：带 `ready-for-agent` 标签和简报的 issue，[implement](https://aihero.dev/skills-implement) 接手它的方式与接手 [to-tickets](https://aihero.dev/skills-to-tickets) 工单完全相同。请求需要打磨才能写简报时，`triage` 会同时运行 [grilling](https://aihero.dev/skills-grilling) 和 [domain-modeling](https://aihero.dev/skills-domain-modeling)，逐轮提问，让决策确定时就落入 `CONTEXT.md` 和 ADR。不确定自己在哪条通道时，用 [ask-matt](https://aihero.dev/skills-ask-matt) 指路。
