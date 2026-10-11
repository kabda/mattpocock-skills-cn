---
name: setup-matt-pocock-skills
description: "为本仓库配置工程技能：设置 issue 跟踪器、分流标签词汇及领域文档布局。首次使用其他工程技能之前运行一次。"
disable-model-invocation: true
---

<a id="setup-matt-pococks-skills"></a>

# 设置 Matt Pocock 的技能

建立工程技能所假定的仓库级配置：

- **Issue 跟踪器**：issue 存放在哪里（默认 GitHub；也开箱支持本地 Markdown）
- **分流标签**：五种规范分流角色使用的字符串
- **领域文档**：`GLOSSARY.md` 与 ADR 存放在哪里，以及使用它们的技能应遵守的读取规则

这是由提示词驱动的技能，不是确定性脚本。先探索、呈现发现、与用户确认，再写入。

<a id="process"></a>

## 流程

<a id="1-explore"></a>

### 1. 探索

查看当前仓库，了解起始状态。读取已有内容，不要假设：

- `git remote -v` 和 `.git/config`：这是 GitHub 仓库吗？是哪一个？
- 仓库根目录的 `AGENTS.md` 和 `CLAUDE.md`：是否存在？其中是否已有 `## Agent skills` 章节？
- 仓库根目录的 `GLOSSARY.md` 和 `GLOSSARY-MAP.md`
- `docs/adr/` 及任何 `src/*/docs/adr/` 目录
- `docs/agents/`：是否已经存在本技能以前的输出？
- `.scratch/`：它可能表明已经采用本地 Markdown issue 跟踪约定
- 是否安装了 `triage` 技能？（本技能旁边有 `triage` 技能目录，或可用技能中包含 `triage`。）这决定是否执行 B 部分。
- Monorepo 信号：`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或有内容且包含自身 `src/` 的 `packages/*`。这些只出现在真正的大型多包仓库中；没有这些信号就意味着单上下文，而几乎所有仓库都属于这种情况。

<a id="2-present-findings-and-ask"></a>

### 2. 呈现发现并询问

总结已有与缺失的内容。然后依次处理各部分。一次一部分，得到一个回答，再进入下一部分。

每部分先给推荐答案，让用户可以用一个词接受。只有选择确实分叉时，才给一句解释；探索已经确定的部分完全跳过（未安装 `triage` 时跳过 B；没有 monorepo 时跳过 C）。

**A 部分：Issue 跟踪器。**

> 解释：“issue 跟踪器”是本仓库存放 issue 的地方。`to-tickets`、`triage`、`to-spec` 等技能会读写它。它们需要知道应当调用 `gh issue create`、在 `.scratch/` 下写 Markdown 文件，还是遵循你描述的其他流程。请选择实际用于跟踪本仓库工作的地方。

默认立场：这些技能是为 GitHub 设计的。如果 `git remote` 指向 GitHub，就推荐 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管主机），就推荐 GitLab。否则（或用户更偏好其他方式），提供：

- **GitHub**：issue 位于本仓库的 GitHub Issues（使用 `gh` CLI）
- **GitLab**：issue 位于本仓库的 GitLab Issues（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 Markdown**：issue 作为文件存放在本仓库的 `.scratch/<feature>/` 下（适合个人项目或没有 remote 的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述流程；技能将其记录为自由格式文字

将选择记录在 `docs/agents/issue-tracker.md`。GitHub 和 GitLab 模板带有“将 PR 作为请求来源”的开关，默认**关闭**。保持关闭，不要主动提出：希望把外部 PR 放入分流队列的用户，可以之后自行修改文件中的开关。

**B 部分：分流标签词汇。** 如果没有安装 `triage`（探索时已查明），完全跳过，因为未安装的技能不需要标签。

如果已安装，只问一个问题：

> 是否保留默认分流标签？（推荐：**是**）

默认是五种规范角色，标签字符串与角色名相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。回答**是**，就原样写入。只有用户说不时，通常因为跟踪器已有其他名称（例如以 `bug:triage` 对应 `needs-triage`），才收集覆盖映射，让 `triage` 使用现有标签而不是创建重复项。

**C 部分：领域文档。** 默认**单上下文**（仓库根目录的一个 `GLOSSARY.md` + `docs/adr/`）。这适合几乎所有仓库，无需询问，直接写入。

只有探索发现 monorepo 信号时，才提供**多上下文**方案（根 `GLOSSARY-MAP.md` 指向各上下文的 `GLOSSARY.md`）。然后确认用户希望哪种布局。

<a id="3-confirm-and-edit"></a>

### 3. 确认并编辑

向用户展示以下草稿：

- 要加入 `CLAUDE.md` / `AGENTS.md` 中所选文件的 `## Agent skills` 区块（选择规则见第 4 步）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一个仅在安装了 `triage` 时）

写入之前，让用户有机会修改。

<a id="4-write"></a>

### 4. 写入

**选择要编辑的文件：**

- 如果存在 `CLAUDE.md`，编辑它。
- 否则，如果存在 `AGENTS.md`，编辑它。
- 如果两者都不存在，询问用户创建哪一个，不要代替用户选择。

已有 `CLAUDE.md` 时，绝不创建 `AGENTS.md`（反之亦然）；始终编辑已有的那个文件。

如果所选文件已有 `## Agent skills` 区块，就原位更新内容，不要追加重复区块。不要覆盖用户对周围章节的编辑。

区块内容：

```markdown
## Agent skills

### Issue tracker

[一句话概述 issue 在哪里跟踪]。参见 `docs/agents/issue-tracker.md`。

### Triage labels

[一句话概述标签词汇]。参见 `docs/agents/triage-labels.md`。

### Domain docs

[一句话概述布局："single-context" 或 "multi-context"]。参见 `docs/agents/domain.md`。
```

只有安装了 `triage` 且执行过 B 部分，才包含 `### Triage labels` 子区块，并写入 `docs/agents/triage-labels.md`。否则两者都省略。

B 节在 GitHub 或 GitLab 上执行时，创建跟踪器中缺少的每个已配置标签（`gh label create` / `glab label create`）。

然后以本技能目录中的种子模板为起点，写入文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue 跟踪器
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue 跟踪器
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 Markdown issue 跟踪器
- [triage-labels.md](./triage-labels.md)：标签映射（仅在安装了 `triage` 时）
- [domain.md](./domain.md)：领域文档使用规则与布局

对于“其他”issue 跟踪器，根据用户描述从头编写 `docs/agents/issue-tracker.md`。

<a id="5-done"></a>

### 5. 完成

告诉用户设置已完成，以及哪些工程技能现在会读取这些文件。说明以后可以直接编辑 `docs/agents/*.md`；只有想切换 issue 跟踪器或从头开始时，才需要重新运行本技能。
