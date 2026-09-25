<a id="what-it-does"></a>

## 它能做什么

`tdd` 以测试优先的方式构建功能或修复 bug：先写一个失败的测试，再只写足够让它通过的代码，然后处理下一个行为。它提供让这个循环产出值得保留的测试的标准：什么是好测试、测试应当放在哪里、mock 用于什么，以及会悄悄毁掉测试套件的三种反模式。

它不会在你尚未同意的 seam 上编写测试。在任何测试出现之前，它会列出打算测试的公共边界，停下来等你确认，因为测试精力有限，而这里决定了你是把精力投入关键路径，还是每一种边界情况。另一点是，`tdd` 是**参考**，不是驱动者。它保存循环规则，由其他主体（你，或 [implement](https://aihero.dev/skills-implement)）运行应用这些规则的[会话](https://www.aihero.dev/ai-coding-dictionary/session)。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/tdd`，或者在任务适合时由 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 自动使用它：以测试优先的方式构建功能、修复 bug，或你说出 "red-green-refactor" 时。

当你要构建的具体行为具有输入和可观察的输出，并且希望测试能够经受重构时，就使用它。

| 你的情况 | 去哪里 |
| --- | --- |
| 输入和输出已经确定的行为（业务逻辑、请求／响应契约、转换、校验） | `tdd` |
| 行为尚未确定 | [to-spec](https://aihero.dev/skills-to-spec)，它也会在编写任何代码之前约定测试 seam |
| 真正的问题是接口形态，而不是测试 | [codebase-design](https://aihero.dev/skills-codebase-design) |
| 已有[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)或[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)，希望代为执行整个构建过程 | [implement](https://aihero.dev/skills-implement)，它会针对每张工单驱动 `tdd` |
| 配置、接线、胶水代码、类型注解、直接的 CRUD 委托 | 这里没有很适合的工具；参见下文尚未解决的缺口 |

最后一行是实际缺口，而不是风格偏好。该技能决定 seam 应当放在*哪里*；其中没有任何内容决定某项变更*是否*值得进入循环。如果某项变更没有可用于断言的独立权威来源，你对它运行这个技能，就会得到复述实现的测试：从另一个方向落入技能本身警告的同义反复反模式。这是 [issue #746](https://github.com/mattpocock/skills/issues/746)，目前仍未解决。在它关闭之前，这个判断由你或你的 `CLAUDE.md` 负责。

<a id="prerequisites"></a>

## 前置条件

需要安装 [codebase-design](https://aihero.dev/skills-codebase-design)。`tdd` 以前自带深模块和接口设计笔记；v1.0 删除了这些内容，改用共享技能，现在 `tdd` 依靠它提供接口设计词汇。除此之外没有其他条件；本技能[无状态](https://www.aihero.dev/ai-coding-dictionary/stateless)，不会写入自己的文件。

<a id="the-loop-and-the-seam-it-runs-at"></a>

## 循环及其所在的 seam

三个词支撑着这个技能。

**Red-green。** 先写失败的测试，再只写足够让它通过的代码。不要提前设想后面的测试。这里没有重构阶段：它在 2026 年 6 月被移除，因为 agent 实际上几乎从不执行它，而且把审查与实现分为不同会话效果更好。重构属于 [code-review](https://aihero.dev/skills-code-review)。

**纵向切片。** 一个 seam、一个测试、一个最小实现，然后重复；第一轮是一枚**曳光弹**，从端到端证明一条路径。相反的做法是横向切片：先写全部测试，再写全部代码。批量测试验证*想象中的*行为，它们检查事物的形状而不是用户的操作，并且在你理解实现之前就锁定测试结构。

**事先约定的 seam。** seam 是无需探入内部即可观察行为的公共边界。规则是绝对的：不能在未经确认的 seam 上测试。在完整流程中，会更早地在 [to-spec](https://aihero.dev/skills-to-spec) 阶段约定 seam：“`/tdd` 被要求只在事先约定的测试 seam 上工作，`/code-review` 会检查是否仅使用了约定的测试 seam。”单独调用时，`tdd` 会直接询问你。

它旨在防止三种反模式：

| 反模式 | 明显征兆 |
| --- | --- |
| 与实现耦合 | 重命名内部函数导致测试失败，但行为没有改变。mock 内部协作者、断言调用次数、通过数据库查询而不是接口进行验证。 |
| 同义反复 | 期望值的计算方式与代码相同，因此测试必然通过。期望值必须来自别处：已知正确的字面量、推演过的示例或规格说明。 |
| 横向切片 | 在任何实现出现之前，先写了一批测试。 |

mock 只用于系统边界：外部 API、时间、随机性，有时也用于文件系统或数据库。不用于你自己的模块。

<a id="common-questions"></a>

## 常见问题

**为什么不重构？描述里明明写着 "red-green-refactor"。**

因为重构步骤被移除了，描述却没有更新。这次移除是有意的：agent 实际上几乎从不执行它，而且让实现和审查处于不同会话效果更好。结果是否仍算教科书式 TDD，不如循环能否产出更好的代码重要。触发短语与正文不一致的问题已记录为 [issue #589](https://github.com/mattpocock/skills/issues/589)，目前仍未解决，所以 "red-green-refactor" 依然可以作为触发技能的短语。你得到的是 red → green，以及在 [code-review](https://aihero.dev/skills-code-review) 中进行的重构。

**它让我选择测试 seam，但我完全不知道该选哪一个。**

这是该技能被报告最多的使用障碍（[issue #607](https://github.com/mattpocock/skills/issues/607)）。提示只列出候选 seam 的名称，没有说明各自能捕获或漏掉什么，所以你只是在标签之间做选择。目前还没有发布修复。实际的应对方法是，先让 agent 说明取舍再作答：组件级 seam 会漏掉哪些集成 seam 能捕获的问题，以及后者会慢多少。这也是完整流程在 `to-spec` 中提前约定 seam 的原因：你能看到整个功能，而不只是一次提示。

**技能明明说先 Red，它却先写了实现再写测试。**

这种事确实会发生。有位用户就此追问[模型](https://www.aihero.dev/ai-coding-dictionary/model)，得到了一个少见的坦诚回答：“我知道技能说的是‘一次一个测试，观察它因正确的原因失败’。我读过。我只是默认回到了平常的习惯。”编写这个技能时接受了这种现实。没有指令能让 agent 百分之百遵守要求，更强硬地强调只会限制 agent 的创造力，收益却很小；即使执行不严格，这个循环仍值得运行，因为整体结果依然更好。如果某个切片需要严格遵守流程，就观察实际运行，而不是相信技能会强制执行。

**它应当先写浏览器测试或端到端测试吗？**

通常不应当，而本技能不会阻止这种做法。一位用户报告说，agent 先写了 Playwright 测试，然后长时间反复运行，最终认定*测试*有问题，实际上功能还不存在。请在你的 `CLAUDE.md` 中配置这一点。浏览器测试慢到足以让 red-green 反馈循环得不偿失；在仓库的 `CLAUDE.md` 中声明，等行为正常工作后再编写这类测试。

**`/tdd` 能取代 `/implement` 或课程中的 `/do-work` 吗？**

不能。`/tdd` 记录方法论；`/implement` 是一个非常简单的工作→反馈→提交循环，直接对应 `/do-work`。课程里单独的 `/do-work` 步骤如今被拆分到 `/implement`、`/tdd` 和 `/code-review`。如果你想知道该对一张工单运行哪一个，答案几乎总是 `/implement`。

**深模块和接口设计指南去哪了？**

在 v1.0 中被移到了 [codebase-design](https://aihero.dev/skills-codebase-design)，并泛化为多个技能共享的词汇。`refactoring.md` 同时被移除；重构如今由 [code-review](https://aihero.dev/skills-code-review) 负责，该技能包含 Fowler 的代码坏味道基线。

**它知道我的其他工单吗？**

不知道。针对一张工单运行时，它会毫不犹豫地提出属于同级工单的工作，因为它看不到其余 issue 关系图（[issue #129](https://github.com/mattpocock/skills/issues/129)）。Matt 的立场是，这不是 `tdd` 的职责。将规格说明与工单一同传入会有帮助；一开始就合理划分工单，帮助更大。

<a id="its-working-if"></a>

## 如何判断它有效

- 在任何测试文件出现之前，它停下来列出打算测试的 seam，并等待确认。
- 一个测试出现、变 Red、获得刚好足够通过的代码，然后才出现下一个测试，而不是一批测试后面跟着一批代码。
- 测试名称读起来像能力（"user can checkout with valid cart"），而不是内部细节（"checkout calls paymentService.process"）。
- 断言中的期望值是能追溯到规格说明的字面量，而不是以与代码相同的方式重新计算的值。
- 重命名内部函数不会破坏测试套件。
- mock 只出现在外部边界（支付 API、时钟），绝不包围你自己的模块。

<a id="where-it-fits"></a>

## 它在流程中的位置

`tdd` 是主流程构建步骤内部的引擎，而不是独立的一步：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

[to-spec](https://aihero.dev/skills-to-spec) 提前约定测试 seam，[implement](https://aihero.dev/skills-implement) 针对每张工单驱动 `tdd`，[code-review](https://aihero.dev/skills-code-review) 随后检查是否只使用了约定的 seam，并负责 `tdd` 已不再执行的重构。另一个相邻技能是 [codebase-design](https://aihero.dev/skills-codebase-design)，它是 `tdd` 所用 seam 与深模块词汇的共享来源。当有具体行为需要构建、却没有完整规格说明时，你也可以单独使用它。如果不确定哪个技能适合当前情况，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
