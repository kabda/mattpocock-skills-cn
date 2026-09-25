<a id="what-it-does"></a>

## 它能做什么

`resolving-merge-conflicts` 逐个 hunk 处理正在进行的 Git 合并或变基，随后运行项目自身的检查，并通过提交完成操作。

它拒绝把冲突视为纯文本问题。触碰某个 hunk 之前，它会将双方改动追溯到各自的**[一手来源](https://www.aihero.dev/ai-coding-dictionary/primary-source)**（提交信息、PR、原始 issue），因此它是在两种意图之间选择，而不是两段文本之间选择；只要兼容，就保留双方意图。确实不兼容时，选择符合本次合并所声明目标的一方，并说明取舍。它不会发明新行为来掩盖冲突，而且没有 `--abort` 这个选项：合并始终要推进到完成提交。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/resolving-merge-conflicts`，或者在任务适合时由 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 自动使用。

当 Git 已经停在无法自行解决的冲突上时使用。它的范围是眼前的冲突，不包括冲突前后的其他事情：

| 你的情况 | 技能 |
| --- | --- |
| 合并或变基进行中，工作树中存在冲突标记 | 本技能 |
| 合并已完成，但现在有些行为不正常，原因不明 | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |
| 规划如何拆分工作，减少分支冲突 | 两者都不是：参见下文有关并行工作的问题 |

<a id="primary-sources-over-ours-and-theirs"></a>

## 一手来源优先于 `ours` 和 `theirs`

本技能要消除的失败模式，是按标志解决冲突：使用 `--ours`、`--theirs`，或手动删除看起来较不重要的代码块，让冲突标记消失、构建能够编译。这种解决方式在语法上可能完美无缺，却悄悄丢掉了某个人有意作出的改动。

没有读过意图，就不可能保留意图。所以工作先从历史开始（提交、PR、[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)），之后才进入 diff。循环中的另一步也出于同样原因：技能找到仓库自身的[自动检查](https://www.aihero.dev/ai-coding-dictionary/automated-check)，在提交前运行，因为合并最容易产生这样的代码：看似兼顾两个分支，却通不过任何一方的测试。

<a id="common-questions"></a>

## 常见问题

**Claude Code 自己解决冲突已经不错了，为什么还需要技能？**

增加的价值是“寻找一手来源”和“运行反馈循环”这两步，否则每次都要手动提示。没有提示的 agent 通常只根据 diff 生成一个看似合理的解决方案，然后就停下。本技能的价值在于不允许跳过两步：阅读每一方为什么存在，以及之后运行检查。相对于一个好的[模型](https://www.aihero.dev/ai-coding-dictionary/model)，这点收益很薄，而这是有意的：至少有一位读者预测，随着模型改进，整个技能都会变得多余。

**为从源头避免冲突，是否应当禁止并行 agent 修改相同文件？**

大多数情况下不应当。给并行任务划分互不相碰的文件区域，成本比节省的成本更高，因为 agent 处理合并冲突的能力已经足够好，取舍并没有看起来那么严峻。值得保留的一项纪律是：先做大型重构。在十个分支已经分出之后才落地一次大规模重命名，才是持续昂贵的情况。

有一份关于并行 worktree 的用户报告提出了提醒：当同级[会话](https://www.aihero.dev/ai-coding-dictionary/session)各自在自己的工作树中实现工单时，最好由编写改动的会话负责合回，因为它已经知道意图。最后把所有人的冲突都交给一个 agent 批量处理，恰恰丢掉了本技能第 2 步需要重新构建的[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。

**为什么绝不 `--abort`？**

中止会丢掉已经完成的冲突解决工作，下次尝试时仍回到同一个没有改变的冲突。本技能针对的是合并确定要发生的情况。如果你已决定不应当合并，那是调用之前就应当作出的决定，不是循环内部的一条分支。

<a id="its-working-if"></a>

## 如何判断它有效

- 解决冲突时，agent 会向你引用提交信息、PR 或 issue，而不只是 diff hunk。
- 每个 hunk 最终保留双方行为，或者明确记录舍弃了什么以及原因。
- 结果中没有出现两个分支都不包含的内容。
- 在提交*之前*就找到了类型检查、测试和格式检查，并运行通过，而不是等你发现故障后才做。
- 最终工作树干净，操作已完成，包括多提交 rebase 中所有剩余提交。

<a id="where-it-fits"></a>

## 它在流程中的位置

这是随时可用的独立工具，不依赖其他技能：Git 停滞时开始，工作树干净且已提交时结束。唯一真正相邻的技能是 [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs)，当合并顺利解决但合并后的代码行为异常时，由它接手：那是诊断问题，而不是冲突问题。本技能完全位于从想法到交付的主流程之外，因此需要了解前后运行什么时，请查看 [ask-matt](https://aihero.dev/skills-ask-matt) 的地图。
