<a id="what-it-does"></a>

## 它能做什么

`grill-me` 从一个**松散的想法**开始，持续访谈你，直到你能对此作出承诺。开始时不需要成熟的计划：产出计划正是这场[会话](https://www.aihero.dev/ai-coding-dictionary/session)的目的。它按**轮次**提问：每轮覆盖整个**前沿**（所有前提已确定的问题），因此不会询问依赖于尚未得到答案的问题。

它是**[无状态](https://www.aihero.dev/ai-coding-dictionary/stateless)**的。不写文件，不留下工作区。唯一留下的是你头脑中更加清晰的想法。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/grill-me` 调用它；[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。请在**新对话**中启动，不要在已经让 agent 写好计划的对话上继续。

只要有一个值得认真对待的想法（功能、产品方向、业务决定、一篇文章），就可以使用，远不必等到想清楚它涉及什么。含糊不是等待的理由，正是这场会话要消化的东西。如果已经能精确描述，就不需要再追问。

该选三个追问技能中的哪一个，取决于眼前的情况：

- **任何主题，任何地方**：`grill-me`。不需要仓库，不写文件，主题也不必是代码。
- **需要对齐代码库**：[grill-with-docs](https://aihero.dev/skills-grill-with-docs)。同样的访谈，但[有状态](https://www.aihero.dev/ai-coding-dictionary/stateful)：它读取代码，并将所得记录到 `GLOSSARY.md` 和 ADR 中。
- **规模大到一场会话容纳不下**：[wayfinder](https://aihero.dev/skills-wayfinder)。它将工作绘成地图，并在地图中运行追问会话。

保持[计划模式](https://www.aihero.dev/ai-coding-dictionary/agent-mode)关闭。计划模式会让 agent 急于产出计划，这与持续探究的方向相反。

<a id="its-a-conversation-not-an-interview"></a>

## 这是对话，而非单向访谈

技能负责提问，但**你**掌控范围。人们往往忽略这一点，而它决定了会话是把想法转化为决策，还是产出信心十足的胡话。

失败模式是**被动**：四十个问题都回答“同意、同意、同意”，最后得到一份 agent 编写、你只负责点头的计划。因为耗时很长，所以感觉很有成效。实际上什么都没决定，结果却带着并无依据的确定感。

主动意味着引导。如果问题的细致程度低于你的需要，就提出异议。范围偏移时要指出。不知道就明确说“我不知道”。这个技能是为了辅助工程师，而不是替代工程师：产出取决于回答质量，而不是提问数量。

相反的错误也存在，只是较少：在访谈中停留太久，以至于始终无法进入代码阶段。

<a id="grillable-and-ungrillable"></a>

## 能靠追问解决与不能靠追问解决的问题

有些问题可以通过讨论回答。另一些不能，再多追问也无法解决。

“一张长表单，还是三页？”“这种交互应该是什么感觉？”属于**无法靠追问解决**的问题：它们需要一个可供观察和反馈的东西。遇到这种问题时，停止追问。用 [prototype](https://aihero.dev/skills-prototype) 构建一次性版本，看一看，再回来用一句话回答。

试图靠讨论解决这种问题，会让会话膨胀。agent 不断换一种问法，你不断猜测，范围也随着不确定性扩大。

<a id="its-working-if"></a>

## 如何判断它有效

- 你对某些内容提出了异议。如果你从未反驳，这场会话就没有必要。
- 问题分几轮提出，而不是漫长地一个接一个挤出来；后续轮次明显建立在你先前的回答上。
- 最终到达意料之外的位置，因为某个问题揭示了一项你此前一直在隐含作出的决策。
- 结束时，你能向未参与会话的人解释并捍卫每个选择。

<a id="common-questions"></a>

## 常见问题

**预计会有多少问题，怎样知道何时结束？**
数轮次，不要数问题。四轮、四十六个问题是很普通的一场会话。当前沿为空时就结束：所有分支都已访问，没有任何内容被默默假定。

**它问了我两百个问题，哪里出了问题？**
通常是范围太大。先让 agent 将工作拆成更小的部分，再逐个追问。过长的会话还会进入 **[dumb zone（迟钝区）](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**，此时[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)已经占用过多，问题质量开始下降。

**能恢复一次只问一个问题吗？**
可以。将以下内容加入全局 `CLAUDE.md`：

```
进行 grilling 时，一次只问一个问题。
```

**如果我确实不知道答案呢？**
就直说。“我不知道”是一个真正的答案，无法回答的问题通常意味着应当做原型，而不是猜测。

**写规格说明前，要新开一场会话吗？**
不要。这场会话的价值在于刚刚建立的[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。将同一段对话直接交给 [to-spec](https://aihero.dev/skills-to-spec)。

**模型有影响吗？**
比大多数技能都更有影响。追问依赖[模型](https://www.aihero.dev/ai-coding-dictionary/model)对系统如何出问题的判断，所以用你最好的模型。实现主要遵循上下文，可以容忍更便宜的模型。

<a id="where-it-fits"></a>

## 它在流程中的位置

`grill-me` 是**可以在任何地方、针对任何主题运行的独立工具**。无状态让它易于迁移：不需要仓库、工作区或设置，也不假设想法与软件有关。人们用它讨论业务决策、写作、下一步做什么：任何在脑海中难以定形的事情。

这种便携性就是它与 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 的全部区别，后者运行相同的访谈，但会读取代码库以便对齐，并将所得记录为 `GLOSSARY.md` 和 ADR。两者都建立在 [grilling](https://aihero.dev/skills-grilling) 这个基础技能上；`grill-me` 是用户调用的入口，不附带其他东西。

如果追问的主题最终确实涉及软件，可以将同一段对话交给 [to-spec](https://aihero.dev/skills-to-spec)，继续进入构建流程（这是一个选项，不是本技能的目的）。不确定哪个流程适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
