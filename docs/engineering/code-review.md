<a id="what-it-does"></a>

## 它能做什么

`code-review` 从两个维度审查 `HEAD` 与你指定固定基准点（提交、分支、标签、`main`、`HEAD~5`）之间的 diff。**Standards** 检查代码是否遵循仓库的编码方式。**Spec** 检查代码是否实现了原始 issue 或[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)的要求。每个维度由自己的[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)运行，双方都看不到对方的推理。

两个维度绝不合并，也绝不重新排序。报告最后给出*每个维度*最严重的问题，拒绝在两者之间选出唯一最严重的问题，因为一项变更可能通过一个维度，却在另一个维度失败：遵循所有约定却实现错误内容的代码，Standards 通过、Spec 失败；完全符合[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)要求却违反仓库约定的代码则相反。混合结论会让通过的维度掩盖失败的维度。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/code-review`，或在你要求审查分支、PR、进行中的工作，或任何 "since X"（自 X 以来）的改动时，由 agent 自动使用。

| 你的情况 | 使用 |
| --- | --- |
| 已有 diff，想知道是否实现正确，*并且*实现的是正确内容 | `code-review` |
| 想在 diff 中寻找 bug：空值路径、竞态、差一错误 | Claude Code 自带的审查，而不是本技能（参见下方名称冲突） |
| 尚未写代码，希望测试优先实现 | [tdd](https://aihero.dev/skills-tdd) |
| 需要构建整份规格说明，并包含审查 | [implement](https://aihero.dev/skills-implement)，它会自行调用本技能 |
| 偏移的是整个代码库，而不是一个 diff | [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) |
| 某处坏了，不知道为什么 | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |

你必须提供固定基准点。如果没有，技能会询问而不是猜测；之后在启动任何子 agent 之前，检查引用可解析且 diff 非空，因此拼错分支名会在你面前失败，而不是在两个子 agent 内部失败。

<a id="prerequisites"></a>

## 前置条件

Standards 维度不需要额外准备。它读取仓库记录的任何标准（`CODING_STANDARDS.md`、`CONTRIBUTING.md` 等），仓库没有记录时就使用内置基线。

Spec 维度需要存在且能找到规格说明。按以下顺序查找：

1. 提交信息中的 issue 引用（`#123`、`Closes #45`、GitLab 的 `!67`），通过 `docs/agents/issue-tracker.md` 获取。
2. 你通过参数传入的路径。
3. `docs/`、`specs/` 或 `.scratch/` 下与分支或功能名称匹配的规格说明文件。
4. 询问你。

第 1 步依赖 `docs/agents/issue-tracker.md`，由 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 写入。没有这个文件，只要你提供路径，这个维度仍然能工作。如果根本没有规格说明，就跳过 Spec 子 agent，并在报告中写 "no spec available"，而不是编造需求。

<a id="the-two-axes"></a>

## 两个维度

| | Standards | Spec |
| --- | --- | --- |
| 问题 | 是否实现正确？ | 是否实现了正确内容？ |
| 读取 | 仓库已记录的标准，加上坏味道基线 | 原始 issue 或规格说明 |
| 报告 | 违反已记录标准的情况（可以是硬性违规），以及坏味道（始终属于判断） | 缺失或部分完成的需求、范围蔓延、实现错误的需求 |
| 每项发现引用 | 标准文件与规则，或坏味道名称加 hunk | 规格说明中的对应行 |

不了解仓库标准的通用审查技能，正是这个设计试图避免的东西：它会标记代码库中有意为之的做法，却漏掉代码库真正依赖的不变量。因此，仓库自己的文档是 Standards 维度的[一手来源](https://www.aihero.dev/ai-coding-dictionary/primary-source)，而且**仓库规则始终优先**。

**坏味道基线**是其底线，来自 Fowler《Refactoring》第 3 章的十二种代码坏味道：Mysterious Name（含混的名称）、Duplicated Code（重复代码）、Feature Envy（依恋情结）、Data Clumps（数据泥团）、Primitive Obsession（基本类型偏执）、Repeated Switches（重复的条件分支）、Shotgun Surgery（霰弹式修改）、Divergent Change（发散式变化）、Speculative Generality（夸夸其谈的通用性）、Message Chains（消息链）、Middle Man（中间人）、Refused Bequest（拒绝继承的遗产）。每种都是带标签的启发式判断（"possible Feature Envy"），绝不是硬性违规；每种都按*是什么* → *如何修复*表述，因此发现附带改进动作，而不只是抱怨。两个维度都会跳过 linter 已强制执行的内容。

<a id="common-questions"></a>

## 常见问题

**它与 Claude Code 自带的 `/code-review` 冲突，怎么办？**

这是本技能被报告最多的问题，尚未修复。Claude Code 自带的 `/code-review` 做的是另一件事：在 diff 中找 bug，而本技能检查规格符合性和仓库标准。安装这个技能库后，其中一个会胜出，具体取决于安装方式。通过插件市场安装，所有内容都带有 `mattpocock-skills:` 前缀别名，内置技能难以通过不带限定的名称访问；通过普通技能安装，本地文件胜出，本技能会遮蔽内置技能。一种干净的处理方式是完全移除 Claude Code 内置技能：能节省大量[上下文](https://www.aihero.dev/ai-coding-dictionary/context)，名称冲突也不再重要。遮蔽本身可以说是 Claude Code [运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)的 bug（技能作者应当能自由命名技能），所以另一个办法是重命名本地副本。编辑 frontmatter 或重命名目录会被 `npx skills update` 撤销；用户报告的持久办法是将技能 fork 为新名称，并把 `code-review` 从受管理集合中移除，同时记录 fork 所依据的提交，便于手动重新同步。

**它的子 agent 不断再次调用 `/code-review`，启动更多 agent。**

这是已知的未解决 bug，多人在不止一种运行环境中复现。Standards 和 Spec 提示词没有禁止委派，因此子 agent 可能重新发现技能并再次展开：一份报告中达到了 50 多个 agent。人们在 fork 中采取的修复，是给两份子 agent 简报都追加一句：“不要调用 `/code-review` 或启动其他 agent：直接完成本次审查。”有人更愿意在运行环境层处理，让每个技能都继承这个约束。两种方式目前都没有进入已提供的技能。无人值守运行时，请关注 agent 数量。

**应该在编写代码的同一场[会话](https://www.aihero.dev/ai-coding-dictionary/session)中运行吗？**

优先使用新会话。正如一位读者所说：“同一上下文审查自己，不是审查，而是带斜杠命令的确认偏误。”编写代码的会话中的审查 agent，持有塑造代码的每一个假设；而独立审阅者恰恰不应拥有这些上下文。这也是人们希望 [implement](https://aihero.dev/skills-implement) 去掉内置审查步骤的原因：它在刚刚写出 diff 的会话中运行审查。从干净会话中自己调用 `/code-review`，才更符合独立审查的本意。

**每张工单后审查，还是最后审查一次？**

两者都可行，技能不会替你决定。逐工单审查让每个 diff 足够小，Spec 维度有一份清晰的规格说明可对照，这是 `implement` 使用的模式。等到分支结束后批量审查，可以发现逐工单审查各自漏掉的工单间交互。如果不确定，就逐工单审查，并在最后相对于分支起点再审查一次。

**能信任这些发现吗？**

不经检查就不能。子 agent 的输出是假设，不是证据：有一个团队报告，基于文字的审查放过了十几处破坏性改动。技能原样汇总两份报告，或只做轻微整理，不会对照文件重新验证每项断言，因此发现可能引用错误位置或夸大影响。采取行动之前，阅读每项发现的引用。每项都必须附带引用（标准规则、坏味道及其 hunk，或规格说明中的一行），才让这种核对成为可能。

**为什么每次运行都会发现新问题？**

因为修复会创造新的审查面，而且 Standards 维度中属于判断的那一半，在不同运行之间不是确定性的。一位读者直白地描述了这个循环：“/code-review 和 /improve-code-architecture 每次都发现新东西。我实施修复，重新运行这些技能，然后一遍又一遍。”没有收敛保证。把一次审查当成一组线索，处理其中有引用规则支撑的项，然后停止：不要循环运行直到它返回干净结果，因为它不会。

**它会审查未提交的工作吗？**

不会。它比较的是三点形式的 `<fixed-point>...HEAD`，从 merge-base 计算，不包含暂存区和工作区改动。如果 `implement` 没有做中间提交，即将提交的工作对审查不可见。先提交，再审查，然后 amend 或增加 fixup。

<a id="its-working-if"></a>

## 如何判断它有效

- 在启动任何子 agent 之前，它拒绝针对无效引用或空 diff 开始工作。
- 报告以 `## Standards` 和 `## Spec` 下的两个独立区块呈现，而不是一份合并列表。
- 每项 Standards 发现都指出仓库文件中的规则或十二种坏味道之一，并引用 hunk；每项 Spec 发现都引用规格说明中的一行。
- 结尾总结给出每个维度最严重的问题，拒绝选出总体最严重的一项。
- 没有规格说明时，Spec 区块明确说明，而不是列出从代码推测的需求。

<a id="where-it-fits"></a>

## 它在流程中的位置

`code-review` 是构建流程末尾的审查步骤：`grill-with-docs → to-spec → to-tickets → implement → code-review`。它也可以独立用于你指定的任何分支或 PR。

- [implement](https://aihero.dev/skills-implement) 是最接近的相邻技能：驱动构建，并在提交前调用本技能作为结束审查。
- [to-spec](https://aihero.dev/skills-to-spec) 和 [to-tickets](https://aihero.dev/skills-to-tickets) 产出 Spec 维度检查的文档；含糊的规格说明会让该维度也含糊。
- [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 是针对整个代码库的对应工具：本技能始终只看一个 diff。

不确定当前情况适合哪个技能时，[ask-matt](https://aihero.dev/skills-ask-matt) 会在整套技能中为你指路。
