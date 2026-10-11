<a id="what-it-does"></a>

## 它能做什么

`implement-spec` 接受一份[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)及其[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)，在一次运行中实现全部内容。编排 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 将工单交给在独立 Git worktree 中工作的实现[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)，把完成的分支合到一个**集成分支**，对结果运行 [code-review](https://aihero.dev/skills-code-review)，并解决工单。

它把工单读取为**任务图**，而非列表。阻塞边决定哪些工单可以开始，因此任何时刻都有一个阻塞项已全部落地的工单**前沿**，前沿上所有工单同时运行。与逐张处理不同，进度由图的形状决定，而非跟踪器中的排列顺序。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/implement-spec` 调用，agent 不会自行使用。

| 你的情况 | 使用 |
| --- | --- |
| 已按阻塞关系拆成工单，希望一次完成的规格说明 | `/implement-spec` |
| 在自己的[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)逐张处理工单，工单间[清空上下文](https://www.aihero.dev/ai-coding-dictionary/clearing) | [implement](https://aihero.dev/skills-implement) |
| 还未拆成工单的规格说明 | 先用 [to-tickets](https://aihero.dev/skills-to-tickets) |
| 没有真正任务图的小改动 | 直接用 [implement](https://aihero.dev/skills-implement) |

<a id="prerequisites"></a>

## 前置条件

- **Issue 跟踪器。** 技能在 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 配置的跟踪器读取、解决工单。未配置时会停下，要求先运行 setup，不会猜测。
- **带阻塞边的工单**，形式如 [to-tickets](https://aihero.dev/skills-to-tickets) 的输出。没有边时图是平的，所有工单会同时开始。
- **能在后台运行子 agent，并为各自提供 Git worktree 的 [harness](https://www.aihero.dev/ai-coding-dictionary/harness)。** 技能旨在同时运行工单；harness 若只能逐个运行子 agent，它就只是更慢的 `implement`。

<a id="the-integration-branch"></a>

## 集成分支

所有工作落到同一分支。每个实现者：

1. 开始前确认自己的 worktree 基于集成分支，
2. 用 [tdd](https://aihero.dev/skills-tdd) 实现工单，逐切片进行 red-green，
3. 报告完成前将集成分支最新提交合入自己的分支，使结果落地时能 fast-forward。

跟踪器决定是否需要 PR。跟踪器通过 PR 关闭工作，或你提出要求时，技能在首次合并后创建草稿 PR，结束时标记 ready。否则运行停在集成分支，按跟踪器的关闭方式解决所有工单；使用本地 Markdown 跟踪器时可完全离线工作。

实现者通过[上下文指针](https://www.aihero.dev/ai-coding-dictionary/context-pointer)与编排者沟通（规格说明、工单、共享探索笔记、之前的提交），不粘贴摘要。这样各子 agent 的提示词保持精简，编排者窗口也有空间容纳任务图。

<a id="common-questions"></a>

## 常见问题

**它与我自行逐张运行 `/implement` 有何不同？**

本技能就是为回答这个问题而存在。发布前，用户不断自制类似版本；一位用户希望“让子 agent 实现工单”，而非“规格说明可能有五张以上工单，却必须逐张新建会话，逐张要求实现”。使用 `implement` 时，你就是调度者：每张工单一个[会话](https://www.aihero.dev/ai-coding-dictionary/session)，中间清空上下文，自行跟踪哪些工单已解除阻塞。`implement-spec` 将这项职责交给一个编排会话。代价是无法逐张在落地时阅读实现，改为最后审查集成分支。开始时清空上下文，输入 `/implement-spec` 并提供规格说明指针（issue 编号或文件路径）。没有真实任务图的小改动，直接用 `implement`。

**它需要 GitHub 吗？我希望停在分支。**

现在不需要了。一位喜欢 beta 版本的用户抱怨：“它最后创建 PR，因此需要 GitHub 这样的在线仓库。我希望能离线完成同样工作，停在已合并全部工作的分支。”现在运行结束于集成分支。只有配置的跟踪器通过 PR 关闭工作，或你要求时才创建 PR；本地 Markdown 跟踪器下，结束时所有工单已解决，工作已合入分支。

**审查和修复循环持续了数小时，或一直“修复”尚未实现的工单。**

`code-review` 在技能指定的唯一时点之外运行时，两种情况都可能发生。它用整份规格说明对照代码，因此只有全部工单落地后才有意义。中途运行会把未实现工单视为失败，agent 接着实现该工单，又触发一轮审查。技能在最后运行一次 `code-review`，把全部发现交给一个修复子 agent，但尚未规定修复后何时停止。一位用户报告，五张工单的功能“审查和修复循环约持续四小时”。看到第二轮全面审查开始时，要求针对已修复发现运行检查，然后停止。首次审查会发现真实问题，运行结果是靠审查完善的草稿，不能直接交付。

**它像 implement 一样驱动 tdd 吗？**

现在会，最初不会。使用 beta 版本的用户发现“实现子 agent 没有继承 /tdd 指令”，从单张工单扩大到整份规格说明后，red-green 就停止了。现在每个实现者都会用 `tdd`。仍没有 `implement` 会话中交互确认 seam 的步骤；需要固定 seam 时，在规格说明或工单中明确写出。

**并行实现者修改同一文件时发生冲突，或给同一概念起了不同名称。**

Worktree 不会消除冲突，只会把冲突延迟到合并时。根据工单文字写出的阻塞边，只是在猜测会触及哪些文件；“代码库不同部分”的两张工单仍可能共享消息目录、配置注册表或类型。每个实现者只看自己的工单和共享笔记，看不到另一人的进行中工作，因此一位用户的 Web 与移动端工单把同一字符串分别命名为 `blockedSince` 和 `blockedOn`。两张前沿工单触及同一共享文件时，添加阻塞边使它们顺序运行，或在探索笔记中固定各工单新增内容的准确名称。

**阻塞项合并后，被阻塞工单仍未启动。**

这是 GitHub 上的已知问题。跟踪器的 blocked-by 计数只在阻塞项*关闭*时减少，而工单通常在 PR 合并、整轮运行结束时才关闭。跟踪器适合提供初始图，中途状态却会过时。要求编排者自行记录哪些工单已合入集成分支，并据此计算前沿。

**它替代 Sandcastle 或 AFK 脚本吗？**

不会。用户提出这个问题，是因为技能现在延伸到实现：“Sandcastle 还有意义吗？你的技能似乎也能处理实现。”`implement-spec` 在一个 harness 会话中让 agent 负责编排，无需基础设施，可以观看并引导。真正 [AFK](https://www.aihero.dev/ai-coding-dictionary/afk) 的工作，用确定性循环（[Sandcastle](https://github.com/mattpocock/sandcastle)、shell 脚本或 CI 任务）更快、更省钱、更可靠，因为没有 agent 作编排决策。

**工单的关键测试在 worktree 中被跳过，却报告 Green。**

Worktree 只包含 Git 跟踪内容。读取 gitignored fixture、本地数据库或凭据的测试，可能在那里静默跳过。验证依赖未跟踪材料的工单，应要求编排者在主 checkout 运行。

<a id="its-working-if"></a>

## 如何判断它有效

- 图允许时，多个实现者同时运行，而非逐个运行。
- 最后一个阻塞项落到集成分支后，工单立即开始，不等整轮结束。
- 每张工单的执行轨迹都有 `tdd`，代码之前先出现失败测试。
- 合入集成分支采用 fast-forward，无需解决冲突。
- 结束时全部工单已解决，结果在同一分支；仅在跟踪器需要时附有 PR。

<a id="where-it-fits"></a>

## 它在流程中的位置

`implement-spec` 是主链条的构建步骤，也是逐张运行 [implement](https://aihero.dev/skills-implement) 的并行替代路线：

```txt
grill-with-docs → to-spec → to-tickets → implement-spec → retro
```

相邻技能包括 [to-tickets](https://aihero.dev/skills-to-tickets)，声明供它读取为任务图的阻塞边；以及 [code-review](https://aihero.dev/skills-code-review)，在收尾前审查集成分支。不确定所处流程时，[ask-matt](https://aihero.dev/skills-ask-matt) 是整套技能的路由器。
