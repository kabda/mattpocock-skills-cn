本仓库是 Matt Pocock 的 mattpocock/skills 项目的非官方简体中文翻译，基于冻结提交 c55ee46073ed923f86ce59a5eb3b6d895095d1b7。下文第一人称及安装来源均保留上游身份，安装命令指向英文上游。详见[中文版本说明](wiki/translation.html)。

<p>
  <a href="https://www.aihero.dev/s/skills-newsletter">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skills-repo-dark_2x.png">
      <source media="(prefers-color-scheme: light)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png">
      <img alt="技能" src="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png" width="369">
    </picture>
  </a>
</p>

<a id="skills-for-real-engineers"></a>

# 为真正的软件工程打造的技能

[![skills.sh](https://skills.sh/b/mattpocock/skills)](https://skills.sh/mattpocock/skills)

这是我每天用于真正工程工作的 agent 技能，而非 vibe coding。

开发真正的应用很难。GSD、BMAD、Spec-Kit 等方法试图通过接管流程来提供帮助，但同时也夺走了你的控制权，使流程中的 bug 难以解决。

这些技能设计得小巧、易于调整、可组合，适用于任何模型，建立在数十年工程经验之上。尽情修改，变成你自己的工具。祝你用得愉快。

想了解这些技能的变化和我新创作的技能，可以和约 60,000 名开发者一起订阅我的 newsletter：

[订阅 Newsletter](https://www.aihero.dev/s/skills-newsletter)

<a id="installation-30-second-setup"></a>

## 安装（30 秒设置）

两种入口，两种理念。**[Claude Code 插件](https://code.claude.com/docs/en/plugins)** 将整套技能安装为受管理、只读的包，我发布时它就更新，因此你是在订阅，而非 fork。**[skills.sh](https://skills.sh/mattpocock/skills)** 将可编辑的技能文件复制到项目，让你修改并定制。选一种：两者都装，每项技能就会出现两份。

<a id="1-get-the-skills"></a>

### 1. 获取技能

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugins install mattpocock-skills
```

或者在会话内：

```
/plugin install mattpocock-skills
```

它已在 Claude Code 官方 marketplace 中，无需先添加任何内容，更新会自动到达。

</details>

<details>
<summary><strong>Codex 及其他 agent</strong></summary>

```bash
npx skills@latest add mattpocock/skills
```

选择想要的技能，以及安装到哪些编码 agent。**安装器允许选择技能，请务必选上 `setup-matt-pocock-skills`。**

原生 Codex 插件已列入路线图（参见 [`.agents/adr/0002-ship-as-a-claude-code-plugin.md`](./.agents/adr/0002-ship-as-a-claude-code-plugin.md)）。

</details>

<details>
<summary><strong>喜欢自行改造的用户</strong></summary>

在任何 agent（包括 Claude Code）上使用同一个安装器：

```bash
npx skills@latest add mattpocock/skills
```

它把技能作为普通文件写入仓库，归你所有、可以编辑。不会背着你更新；想获取我的最新改动时，运行 `npx skills update`。

</details>

<a id="2-run-setup-matt-pocock-skills"></a>

### 2. 运行 `/setup-matt-pocock-skills`

在 agent 中，每个仓库运行一次。它会：

- 询问你想用哪个 issue 跟踪器（GitHub、Linear 或本地文件）
- 询问分流工单时使用哪些标签（`/triage` 使用标签）
- 询问创建的文档要保存在哪里

<a id="3-bam---youre-ready-to-go"></a>

### 3. 好了，可以开始了。

<a id="why-these-skills-exist"></a>

## 为什么创建这些技能

我构建这些技能，是为了解决在 Claude Code、Codex 和其他编码 agent 上常见的失败模式。

<a id="1-the-agent-didnt-do-what-i-want"></a>

### #1：Agent 没有做我想要的事

> “没人确切知道自己想要什么。”
>
> David Thomas 与 Andrew Hunt，[《程序员修炼之道》](https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

**问题**。软件开发最常见的失败模式是理解不一致。你以为开发者知道你想要什么，看到做出来的东西后才发现，对方根本没理解。

AI 时代也一样。你与 agent 之间有沟通鸿沟。解决方法是开展一次**追问会话**，让 agent 就你正在构建的东西详细提问。

**解决办法**是使用：

- [`/grill-me`](./skills/productivity/grill-me/SKILL.md)：用于非代码场景
- [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md)：与 [`/grill-me`](./skills/productivity/grill-me/SKILL.md) 相同，但多了额外好处（见下文）

这是我最受欢迎的技能。它们帮助你在开始前与 agent 达成一致，并深入思考正在做的变更。*每次*想做变更时都使用它们。

<a id="2-the-agent-is-way-too-verbose"></a>

### #2：Agent 太啰嗦

> 有了通用语言，开发者之间的对话和代码中的表达，都源自同一个领域模型。
>
> Eric Evans，[《领域驱动设计》](https://www.amazon.co.uk/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)

**问题**：项目开始时，开发者与软件服务对象（领域专家）往往说着不同的语言。

我与 agent 之间也感到同样的张力。agent 通常被放进项目，边工作边摸索术语，于是一个词能说清的事，它要用二十个词。

**解决办法**是共享语言。用一份文档帮助 agent 理解项目术语。

<details>
<summary>
示例
</summary>

这是我的 `course-video-manager` 仓库中的一份 [`CONTEXT.md`](https://github.com/mattpocock/course-video-manager/blob/076a5a7a182db0fe1e62971dd7a68bcadf010f1c/CONTEXT.md) 示例。哪一种更容易读？

- **之前**：“把课程中某章节内的一课变成‘真实存在’的内容（也就是在文件系统中给它一个位置）时，出了问题。”
- **之后**：“物化级联出了问题。”

这种简洁在每次会话中都会带来收益。

</details>

这已经内置于 [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md)。它是一场追问会话，也帮助你与 AI 建立共享语言，并把难以解释的决策记入 ADR。

很难描述它有多强大。这可能是本仓库最酷的一项技巧。试试就知道。

> [!TIP]
> 共享语言除了减少啰嗦，还有很多好处：
>
> - **变量、函数和文件命名一致**，都使用共享语言
> - 因此，agent **更容易在代码库中导航**
> - agent **思考时消耗的 tokens 也更少**，因为它能使用更简洁的语言

<a id="3-the-code-doesnt-work"></a>

### #3：代码不能正常工作

> “始终迈出小而审慎的步子。反馈速率就是你的速度上限。绝不要接下过大的任务。”
>
> David Thomas 与 Andrew Hunt，[《程序员修炼之道》](https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

**问题**：假设你与 agent 已对要构建什么达成一致，但它*仍然*产出糟糕代码，怎么办？

该检查反馈循环了。没有代码实际运行情况的反馈，agent 就是在盲飞。

**解决办法**：需要常规的一组反馈循环：静态类型、浏览器访问和自动测试。

对自动测试而言，red-green-refactor 循环至关重要：agent 先写一个失败测试，再让测试通过。这给 agent 持续稳定的反馈，从而产出好得多的代码。

我构建了可以放入任意项目的 **[`/tdd`](./skills/engineering/tdd/SKILL.md) 技能**。它鼓励 red-green-refactor，并为好测试和坏测试提供大量指引。

针对调试，我还构建了 **[`/diagnosing-bugs`](./skills/engineering/diagnosing-bugs/SKILL.md)** 技能，把最佳调试实践封装成逐阶段设门槛的严谨循环。

<a id="4-we-built-a-ball-of-mud"></a>

### #4：我们造出了一团乱麻

> “*每天*都要投入系统设计。”
>
> Kent Beck，[《解析极限编程》](https://www.amazon.co.uk/Extreme-Programming-Explained-Embrace-Change/dp/0321278658)

> “最好的模块是深模块。它们让人通过简单接口访问大量功能。”
>
> John Ousterhout，[《软件设计的哲学》](https://www.amazon.co.uk/Philosophy-Software-Design-2nd/dp/173210221X)

**问题**：大多数用 agent 构建的应用复杂且难改。agent 大幅加快编码，也加速了软件熵增，代码库以空前速度变得复杂。

**解决办法**是对 AI 辅助开发采用一种激进的新方法：关心代码设计。

这贯穿整套技能的每一层：

- [`/to-spec`](./skills/engineering/to-spec/SKILL.md) 在创建规格说明前，会问你要触及哪些模块

尤其是 [`/improve-codebase-architecture`](./skills/engineering/improve-codebase-architecture/SKILL.md)，它调查代码库中的深化机会，把候选项交给你。我建议每隔几天就在代码库上运行一次。它做的是调查，不是救援：真正老旧的代码库里，它会发现实际候选项，但不会替你解开那团乱麻。

<a id="summary"></a>

### 总结

软件工程基础比以往更重要。这些技能是我尽力把基础浓缩为可重复实践的成果，希望帮助你交付职业生涯中最好的应用。祝你用得愉快。

<a id="reference"></a>

## 参考索引

技能按一个维度划分：谁能调用。**用户调用**的技能只有你输入时才能访问（例如 `/grill-me`），职责是编排。**模型调用**的技能可由你调用，*也可*在任务适合时由 agent 自动使用，承载可复用的方法。用户调用技能可以调用模型调用技能，但绝不能调用另一项用户调用技能。

<a id="engineering"></a>

### 工程

我每天用于代码工作的技能。

**用户调用**

- **[ask-matt](./skills/engineering/ask-matt/SKILL.md)**：询问哪项技能或流程适合你的情境。本仓库用户调用技能的路由器。
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**：在追问会话中同时构建项目领域模型，打磨术语，并同步更新 `CONTEXT.md` 和 ADR。
- **[triage](./skills/engineering/triage/SKILL.md)**：让 issue 流转经过分流角色状态机。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**：扫描代码库中的深化机会，以可视化 HTML 报告呈现，再对你选中的机会深入追问。
- **[setup-matt-pocock-skills](./skills/engineering/setup-matt-pocock-skills/SKILL.md)**：为本仓库配置工程技能所需的 issue 跟踪器、分流标签和领域文档布局。使用其他工程技能前，每个仓库运行一次。
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**：把当前对话转为规格说明，发布到 issue 跟踪器。不做访谈，只综合已经讨论过的内容。
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**：把任意计划、规格说明或对话拆成曳光弹工单，每张声明阻塞关系；在本地文件中写成文本，或在真正的跟踪器中设为原生阻塞链接。
- **[implement](./skills/engineering/implement/SKILL.md)**：实现规格说明或一组工单描述的工作，在事先约定的 seam 上驱动 `/tdd`，并在提交前用 `/code-review` 收尾。
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**：把超过一个 agent 会话容量的大型工作规划为 issue 跟踪器上的共享决策工单地图，逐一解决，直到通往目标的道路清晰。

**模型调用**

- **[prototype](./skills/engineering/prototype/SKILL.md)**：构建一次性原型，回答一个设计问题；状态/逻辑问题产出单个可分享 HTML 文件，UI 问题则产出可从同一路由切换的多个截然不同变体。
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**：用于棘手 bug 和性能回归的严谨诊断循环：建立能因这个 bug 变 Red 的反馈循环 → 最小化 → 提出假设 → 加观测 → 修复 → 回归测试。
- **[research](./skills/engineering/research/SKILL.md)**：由后台 agent 根据高可信一手来源调查问题，并在仓库中保存带引用的 Markdown 研究结果。
- **[tdd](./skills/engineering/tdd/SKILL.md)**：采用 red-green-refactor 循环的测试驱动开发，每次一个纵向切片地构建功能或修复 bug。
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)**：主动构建并打磨项目领域模型：对照术语表质疑用词，用边界场景做压力测试，并同步更新 `CONTEXT.md` 和 ADR。
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**：设计深模块的共享方法与词汇：在清晰 seam 处，以小接口封装大量行为，并可通过接口测试。
- **[code-review](./skills/engineering/code-review/SKILL.md)**：对固定基点以来的 diff 做双维度审查：**Standards**（是否遵守仓库编码标准及 Fowler 异味基线）和 **Spec**（是否忠实实现原始 issue/规格说明）。两个维度由并行子 agent 执行，避免相互干扰。
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**：逐块处理正在进行的 Git merge 或 rebase 冲突，追溯双方一手来源的意图来解决，再完成操作（绝不 `--abort`）。
- **[wizard](./skills/engineering/wizard/SKILL.md)**：生成交互式 bash 向导，引导人完成只有人能执行的步骤：开通基础设施、设置凭据或 CI secrets、操作陌生第三方控制台，或执行一次性迁移或切换。

<a id="productivity"></a>

### 生产力

通用工作流工具，不限于代码。

**用户调用**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**：就计划或设计接受持续深入的访谈，直到设计树每条分支都已解决。
- **[handoff](./skills/productivity/handoff/SKILL.md)**：把当前对话压缩成交接文档，让另一个 agent 继续工作。
- **[teach](./skills/productivity/teach/SKILL.md)**：以当前目录作为有状态教学工作空间，跨多个会话教用户新技能或概念。
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)**：把你无法独自回答的决策转成 Markdown 问卷，交给能回答的那个人，异步填写或开会共同完成。它追问的是发送安排（给谁、需要什么回复），不是主题本身。
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**：消息没讲明白时立即调用。agent 会用通俗英语和你的 `CONTEXT.md` 词汇重新解释，补上缺失上下文。

**模型调用**

- **[grilling](./skills/productivity/grilling/SKILL.md)**：围绕计划、决策或想法持续深入访谈用户，直到设计树每条分支都已解决。它是 `grill-me`、`grill-with-docs`、`triage`、`wayfinder` 和 `improve-codebase-architecture` 背后的可复用访谈基础技能。
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**：为 agent 编写文档：技能、AGENTS.md/CLAUDE.md，以及任何通过指针访问的文档。
