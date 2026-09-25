<a id="what-it-does"></a>

## 它能做什么

`setup-matt-pocock-skills` 回答一个仓库的三个问题：issue 放在哪里、分流标签叫什么、领域文档位于何处。它将答案记录为 `docs/agents/` 下的 Markdown 文件。

仓库之间只有这些文件不同。技能本身在各处完全相同；运行时读取 `docs/agents/issue-tracker.md`，并按其中说明执行。因此，这套技能不绑定 GitHub，也无需编辑任何技能文件来改用其他位置。用 "link the skills to a custom issue tracker"（将技能连接到自定义 issue 跟踪器）调用，任何可通过程序连接的系统都能使用，技能无需改动。

这是由提示词驱动的技能，不是确定性脚本。它读取 `git remote`、现有 `CLAUDE.md` 和 `CONTEXT.md`，提出基于发现的建议，等待确认后才写入任何内容。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/setup-matt-pocock-skills` 调用；[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 不会自行使用。它被刻意标记为不可自动调用，因此其他技能也不能替你触发。

每个仓库运行一次，在首次使用任何其他工程技能之前。如果 [triage](https://aihero.dev/skills-triage)、[to-spec](https://aihero.dev/skills-to-spec)、[to-tickets](https://aihero.dev/skills-to-tickets) 或 [wayfinder](https://aihero.dev/skills-wayfinder) 开始猜测 issue 去向，或添加跟踪器中不存在的标签，就说明尚未在这里完成设置。项目做到一半的仓库也很适合运行；技能读取已有内容，不会浪费此前工作。

<a id="prerequisites"></a>

## 前置条件

它会写入运行所在的仓库：

| 写入什么 | 位置 |
| --- | --- |
| `issue-tracker.md` | `docs/agents/` |
| `domain.md` | `docs/agents/` |
| `triage-labels.md` | `docs/agents/`，仅在安装了 `triage` 技能时 |
| 一个 `## Agent skills` 区块 | `CLAUDE.md` / `AGENTS.md` 中已有的那个 |

全部都是提交到仓库的 Markdown。没有用户级或全局模式：配置位于仓库中，因此每个仓库都有自己的副本。

<a id="the-three-decisions"></a>

## 三项决策

每部分先给推荐答案，探索已经确定的内容就跳过。大多数运行确认两次就结束。

| 决策 | 推荐什么 | 实际何时询问 |
| --- | --- | --- |
| **Issue 跟踪器** | 与 `git remote` 匹配的跟踪器 | 始终询问：这是唯一真正需要选择的项 |
| **分流标签** | 保留五个规范名称（`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`） | 仅在安装了 `triage` 技能时 |
| **领域文档** | 单上下文：根目录一个 `CONTEXT.md` 加 `docs/adr/` | 仅在发现 monorepo 信号时，提供多上下文 `CONTEXT-MAP.md` 选项 |

跟踪器选项：

| 选项 | Issue 存放位置 | 需要什么 |
| --- | --- | --- |
| **GitHub** | 仓库的 GitHub Issues | `gh` CLI |
| **GitLab** | 仓库的 GitLab Issues | `glab` CLI |
| **本地 Markdown** | 本仓库 `.scratch/<feature>/` 下的文件 | 什么都不需要，连 remote 都不需要 |
| **其他** | 你指定的位置 | 由你用一段话描述流程 |

前三种随技能提供模板，开箱即用。本地 Markdown 是完整支持的选项，不是后备方案：没有 remote 的个人项目也完全支持。有一点值得重申：如果使用 GitHub，就不要再使用本地 Markdown。它们是替代关系，不是叠加层。

“其他”也不是空壳。Jira、Linear、Azure DevOps 和 Beads 能工作，正是因为这条路径：你描述流程，技能将文字记录到 `docs/agents/issue-tracker.md`，下游技能遵循这些文字。社区已经这样做过：通过 [MCP](https://www.aihero.dev/ai-coding-dictionary/mcp) 使用 Jira 的变体、形似 `gh` 的 Gitea CLI，以及手工构建的本地仪表盘。

<a id="common-questions"></a>

## 常见问题

**必须使用 GitHub 吗？**

不必。GitHub、GitLab 和 `.scratch/` 下的本地 Markdown 都有现成模板，其他系统通过“其他”路径工作。这是记录中重复最多的问题，大致措辞是：*“硬绑定 GitHub”*、*“能用 GitLab / Jira 吗”*、*“Azure DevOps 呢”*。每次答案都一样：跟踪器是设置时的选择，不是技能属性。

**更新技能后需要重新运行吗？**

v1.1 之后有人直接问过，Matt 回答需要。技能自己的结束说明更宽松：它告诉你，只有切换跟踪器或从头开始才需要重跑。两种说法都可以理解，差异的原因真实存在：种子模板在不同版本间变化，旧版本写出的 `docs/agents/issue-tracker.md`，相对于现在读取它的技能可能已经过时。如果下游技能的行为与文档描述开始不同，重新运行是低成本修复。

**我用的是 Codex，它却写入 `CLAUDE.md`。**

这是已知缺口，仍未解决。文件选择规则是“存在 `CLAUDE.md` 就编辑，否则选 `AGENTS.md`”：它检查哪个文件存在，而不是正在使用哪个 [agent 运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)。如果仓库留有 Claude Code 时代的 `CLAUDE.md`，`## Agent skills` 区块就会写到 Codex 不读取的地方。有两种流传的应对办法：手动把区块移到 `AGENTS.md`；或以 `AGENTS.md` 为权威来源，让 `CLAUDE.md` 只保留一行指向它的内容。如果两者都不存在，技能会问你创建哪一个，而不是自行选择；这让一些原本期待它直接决定的人困惑。

**它没有创建分流标签。**

它不会创建。`docs/agents/triage-labels.md` 是一份*映射*：告诉 `/triage`，跟踪器中的哪些字符串对应五种规范角色。它不运行 `gh label create`。在新 GitHub 仓库中，这些标签确实还不存在，已不止一次被报为 bug。另有两点：

- 如果跟踪器已使用规范名称，映射就是同名对照表，没有需要配置的内容。这是预期的常见情况，不是遗漏步骤。
- [wayfinder](https://aihero.dev/skills-wayfinder) 的 `wayfinder:map` 和 `wayfinder:<type>` 标签也不会在这里创建，而且 `gh issue create --label <missing>` 会直接失败，不会自动创建标签。首次在 GitHub 仓库运行 wayfinder 之前，请手动创建。

**能在这里配置其他技能的行为吗（[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)节奏、问题格式、语气）？**

不能。它只配置三件事：跟踪器、标签、文档布局。有人直接请求让它承载用户偏好，而一贯的回答是技能应当保持主张：*"Config is death."（配置就是死路。）* 偏好应当以普通指令放进 `CLAUDE.md`，每个技能本来就会读取。

**能把配置放进 `~/.claude`，而不是提交到每个仓库吗？**

目前不能。一个在多个仓库使用这些技能的人提出了完全相同的请求，目前仍未解决，没有用户级模式。每个仓库都携带自己的 `docs/agents/`。

**用一个技能配置其他技能，不奇怪吗？**

有一个长期存在的抱怨认为是的，原话大意是：*“用一个技能设置另一个技能让我觉得不对：这意味着 LLM 在配置自己的技能。”* 这种取舍真实存在，也被承认：不设置这一步，就得把跟踪器指令复制进每个处理 issue 的技能。缓解手段是输出可检查、可编辑的 Markdown：你可以阅读每个写出的文件，并手动修改；日常调整正应如此，不需要再运行一遍技能。

<a id="its-working-if"></a>

## 如何判断它有效

- `docs/agents/issue-tracker.md` 和 `docs/agents/domain.md` 存在；安装了 `triage` 时，还存在 `triage-labels.md`。
- 你的运行环境实际读取的指令文件中出现 `## Agent skills` 章节，用一句话概述分别指向上述文件。
- 推荐的跟踪器匹配你实际使用的 remote，标签字符串匹配跟踪器中真实存在的标签。
- 此后，`/to-tickets` 发布时不再问 issue 存在哪里，`/triage` 使用标签而不是编造标签。
- 技能文件本身没有任何改动。如果设置过程编辑了 `SKILL.md`，就出了问题。

<a id="where-it-fits"></a>

## 它在流程中的位置

`setup-matt-pocock-skills` 是工程流程中**运行一次的设置**，是其他一切所假定的前提，而不是流程链中的一步。相邻技能就是这些文件的读取者：[triage](https://aihero.dev/skills-triage) 使用这里写出的标签词汇；[to-spec](https://aihero.dev/skills-to-spec) 和 [to-tickets](https://aihero.dev/skills-to-tickets) 发布到这里指定的跟踪器；[wayfinder](https://aihero.dev/skills-wayfinder) 读取同一跟踪器文件的 "Wayfinding operations" 章节，了解地图和子[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)如何存储。这里记录的领域文档布局，随后由 [domain-modeling](https://aihero.dev/skills-domain-modeling) 填充：只有术语或决策真正明确时，才按需创建 `CONTEXT.md` 和 ADR，因此设置后仓库仍空着是预期状态。接下来该用哪个技能，[ask-matt](https://aihero.dev/skills-ask-matt) 会为整套技能指路。
