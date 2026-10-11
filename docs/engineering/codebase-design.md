<a id="what-it-does"></a>

## 它能做什么

`codebase-design` 统一设计模块时使用的词汇：**模块**、**接口**、**深度**、**seam**、**适配器**、**杠杆效应**、**局部性**。它精确定义每个词，禁止使用含混的替代词（"component"、"service"、"API"、"boundary"），并说明由这些定义推导出的几条原则。

它是参考，不是流程。没有要运行的循环，不产出任何交付物，也没有向你提问的检查点。其他涉及设计的技能都借用它的词汇；单独使用时，它给出语言，到此为止。调用前应当知道这一点，因为如果你把一个[会话](https://www.aihero.dev/ai-coding-dictionary/session)指向没有流程和停止规则的技能，并说“开始”，它就会即兴编出一套流程。实际会发生什么，参见下方的问题。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/codebase-design`，或者在设计任务适合时由 agent 自动使用它。

当你已经知道要重新设计哪些代码，需要思考其形态时使用：seam 放在哪里、接口能缩小到什么程度、一次提取是否有价值。需要解决对某个词含义的争论时，也可以使用它。

几个技能与它相近，请按问题选择：

| 问题 | 技能 |
|---|---|
| 一个模块的形态：接口、seam、深度 | `codebase-design` |
| *领域中的词语*："account" 有三种含义，两个人对 "cancellation" 的理解不同 | [domain-modeling](https://aihero.dev/skills-domain-modeling) |
| 还不知道应当重新设计*哪个*模块 | [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture)（通过调研寻找候选对象） |
| 希望有人质疑设计，而不只是给它命名 | [grilling](https://aihero.dev/skills-grilling) |
| 有具体行为需要构建，希望测试能够经受重构 | [tdd](https://aihero.dev/skills-tdd) |

<a id="the-vocabulary"></a>

## 词汇

术语表就是这个技能。每个术语都相对于其他术语定义，并指出它替代了哪个词。

| 术语 | 含义 | 不要说 |
|---|---|---|
| **模块（Module）** | 任何具有接口和实现的事物。刻意不限定规模：函数、类、包、跨技术层的切片。 | unit、component、service |
| **接口（Interface）** | 调用方为正确使用它必须知道的一切：类型签名，以及不变量、顺序约束、错误模式、必需配置和性能特征。 | API、signature |
| **深度（Depth）** | 接口处的杠杆效应：调用方或测试每学习一单位接口，就能使用多少行为。**深**：大量行为隐藏在小接口后。**浅**：接口几乎与实现一样复杂。 | 无 |
| **Seam** | Michael Feathers 的术语：无需在某处编辑代码，就能改变该处行为的位置。它是接口的*位置*；把它放在哪里，是与背后放什么相互独立的决策。 | boundary |
| **适配器（Adapter）** | 在 seam 处满足接口的具体事物。命名的是角色而非实质：内存 fake 与 Postgres 仓储都是适配器。 | 无 |
| **杠杆效应（Leverage）** | 调用方从深度中得到的收益：每学习一单位接口，就获得更多能力。 | 无 |
| **局部性（Locality）** | 维护者从深度中得到的收益：变更、bug 和验证集中在一处。修复一次，处处生效。 | 无 |

这里刻意*不把*深度定义为实现行数与接口行数的比值，尽管那是 Ousterhout 本人的定义。这个指标会鼓励给实现注水。因此改用“深度即杠杆效应”。

<a id="the-four-principles"></a>

## 四条原则

- **深度是接口的属性，而不是实现的属性。** 深模块内部可以由可替换的小组件构成。只是它们不会暴露给调用方。模块可以有供自身测试使用的内部 seam，以及位于接口处的一个外部 seam。
- **删除检验。** 想象删除模块。如果复杂性消失了，它只是透传层。如果复杂性重新出现在 N 个调用方中，它就有存在的价值。
- **接口就是测试面。** 调用方和测试跨越同一个 seam。如果你想*越过*接口测试，模块的形态就不对。
- **一个适配器意味着假想的 seam，两个适配器才意味着真实的 seam。** 确实存在跨 seam 的变化时，才划出 seam。只有一个适配器的 seam 只是间接层。

两份配套文件进一步展开这些内容，技能会按需读取，而不是预先全部读取。[DEEPENING.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/DEEPENING.md) 将候选对象的依赖分为四类（进程内、可在本地替代、远程但由自己控制、真正的外部依赖），因为类别决定了如何跨越 seam 测试加深后的模块。[DESIGN-IT-TWICE.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/DESIGN-IT-TWICE.md) 并行启动[子 agent](https://www.aihero.dev/ai-coding-dictionary/subagent)，为同一模块产出至少三个截然不同的接口，再比较其深度、局部性和 seam 位置。

<a id="common-questions"></a>

## 常见问题

**如何在 TypeScript 中实际构建深模块？**

这是最常见的问题，但技能没有回答。它定义深模块*是什么*，却不说明怎样阻止不当 import 绕过接口。[Issue #458](https://github.com/mattpocock/skills/issues/458) 说：“假设接口隐藏细节且令人满意，但怎样强制执行？没有 lint 或清晰约束，人和 LLM 都会逐渐把它弄乱。”讨论给出三个选项：包进类或 IIFE，接受类变大；做成 monorepo 包，接受工具链；或用 [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) 禁止绕过接口的 import。其中 Effect 最好，dependency-cruiser 次之。`in-progress/` 的 `setup-ts-deep-modules` 建立 `src/packages/<name>/index.ts` 约定，但属 beta，没有文档页，也不附带 lint 规则。

**我把会话指向它，它却花了 100k [token](https://www.aihero.dev/ai-coding-dictionary/token) 重新设计我从未要求处理的东西。**

这是已知问题，已记录为 [issue #449](https://github.com/mattpocock/skills/issues/449)。本技能可由模型调用，并将自己描述为词汇参考，但没有任何内容能硬性阻止 agent 把它当成可执行流程。当被要求“在 /codebase-design 中继续并推进未决事项”时，一个 agent 选用了它能找到的最像操作流程的内容：`DESIGN-IT-TWICE.md` 中的并行子 agent。它重新探索了前一场会话已经梳理过的代码，并在提出任何问题之前执行了很长一段。驱动型技能所具备的约束（检查点、一次一个问题、不自动推进）在这里都不存在，因为参考材料没有这些。应对方法是指定一个驱动技能，让本技能作为底层参考：使用 `/grill-with-docs`、`/improve-codebase-architecture` 或 `/tdd`，由 `codebase-design` 提供词汇。该 issue 仍未解决。

**`design-an-interface` 去哪了？有没有 `/interface-design` 技能？**

`design-an-interface` 已被移除并并入本技能。内容没有丢失：它的“设计两次”技术（来自 Ousterhout，由并行子 agent 生成截然不同的设计）在这里以 `DESIGN-IT-TWICE.md` 提供。另外，有几个人希望为深模块／薄接口理念设立专门的 `/interface-design` 技能；这套理念已经在这里，没有另建技能的计划。如果你是寻找这两个名称之一而来，找的就是本页。

**这不就是文件结构约定，比如目录、barrel 文件、功能切片吗？**

不是，面对多次质疑，技能一直坚持这条界线。[Issue #95](https://github.com/mattpocock/skills/issues/95) 提议用一种正式的分形树文件结构作为深模块的具体实现；回复指出两者正交：“深模块关心的是接口设计，以及无论文件系统是什么样，都通过严格接口访问。采用这种方法，完全可能仍然得到浅模块。”#458 也出现了同样的问题：“我认为你可能把模块概念与文件系统绑得太紧。文件系统当然可以为模块形态提供有用线索，但构建深模块并不需要借助文件系统。”术语表刻意将**模块**定义为与规模无关。

**`tdd` 真的使用这套词汇吗？**

现在是的。过去很长时间并没有。`tdd` 原有的内嵌深模块笔记在 v1.0 中被移除，改用这个共享技能，但替代笔记的引用却一直没有加上，因此 `tdd` 自行定义了 "seam"，也没有引用其他内容。这个缺口已经补上：如今 `tdd` 中有了引用，当未决问题是接口形态而不是测试时，就会查阅它。`tdd` 仍负责将 "seam" 作为开展*测试*的边界；本技能负责 seam 背后的模块形态。

**“设计两次”模式在 Claude Code 之外能正常使用吗？**

不能顺畅使用。`DESIGN-IT-TWICE.md` 写的是“使用 Agent 工具并行启动至少 3 个子 agent”，用的是 Claude Code 的[工具](https://www.aihero.dev/ai-coding-dictionary/tool)及其在 Claude Code 中的名称。仓库也提供包括 Codex 在内的其他 [agent 运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)的元数据，但那些环境可能没有这个名称的工具，因此并行设计阶段的可移植性低于技能元数据所暗示的程度。该问题记录在 [issue #564](https://github.com/mattpocock/skills/issues/564)，仍未解决。

**能往术语表中添加自己的概念，比如 connascence、模块秘密、[渐进式披露](https://www.aihero.dev/ai-coding-dictionary/progressive-disclosure)吗？**

已经有人提出过这些建议。[Issue #180](https://github.com/mattpocock/skills/issues/180) 添加 Parnas 的模块秘密和 Page-Jones 的 connascence，用来命名*什么*正在跨 seam 泄漏，并附有可用的 diff；[issue #303](https://github.com/mattpocock/skills/issues/303) 提议在实现内部使用渐进式披露，让公共接口很深的模块，其内部不至于是一整块毫无区分的代码。两者都仍然开放，尚未合并。当前提供的术语表刻意保持精简，原因就在技能正文里：保持语言一致才是全部目的，一个没人能一致使用的术语，比没有这个术语更糟。

<a id="its-working-if"></a>

## 如何判断它有效

- 设计讨论不再出现 "component"、"service"、"boundary"，转而使用 "module"、"interface"、"seam"。
- 有人能指着一个提议的提取方案，明确说出它是否通过删除检验。
- 提议 seam 时，能说出第二个适配器，而不只有第一个。
- 接口讨论涵盖不变量、顺序和错误模式，而不只是类型签名。
- 调用它不会启动一场会话。如果 agent 仅凭 `/codebase-design` 就开始读取文件、提出重构，它就把参考材料误当成了驱动工具。

<a id="where-it-fits"></a>

## 它在流程中的位置

`codebase-design` 是**随时可用的独立工具**，也是工程技能底下的词汇层，不是某条流程中的一个步骤。与它最接近的是 [domain-modeling](https://aihero.dev/skills-domain-modeling)，后者是*问题领域*词汇的平行参考，关注的不是模块形态。通常会同时需要两者，因为要给深模块起好名字，这两种词汇都不可少。另一个相邻技能是 [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture)：它调研代码库，寻找可加深的候选对象，并用这套术语表描述每一个对象；因此，它找到模块，本技能则提供设计模块的工作台。不确定哪个技能或流程适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。
