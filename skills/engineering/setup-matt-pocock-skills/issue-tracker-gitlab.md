<a id="issue-tracker-gitlab"></a>

# Issue 跟踪器：GitLab

本仓库的 issue 和规格说明存放为 GitLab issue。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

<a id="conventions"></a>

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行描述使用 heredoc。传入 `--description -` 打开编辑器。
- **读取 issue**：`glab issue view <number> --comments`。使用 `-F json` 获取机器可读输出。
- **列出 issue**：`glab issue list -F json`，配合适当的 `--label` 筛选。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 将评论称为 "notes"。
- **添加／移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可以用逗号分隔，或重复传入标志。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，因此先用 `glab issue note <number> --message "..."` 发布解释，再关闭。
- **Merge request**：GitLab 将 PR 称为 "merge requests"。使用 `glab mr create`、`glab mr view`、`glab mr note` 等，形式与 `gh pr ...` 相同，只是用 `mr` 代替 `pr`，用 `note`/`--message` 代替 `comment`/`--body`。

根据 `git remote -v` 推断仓库；在克隆目录内运行时，`glab` 会自动完成。

<a id="merge-requests-as-a-triage-surface"></a>

## 将 merge request 作为分流来源

**MRs as a request surface: no.** _（如果本仓库把外部 merge request 视为功能请求，设为 `yes`；`/triage` 会读取此开关。）_

设为 `yes` 时，MR 使用与 issue 相同的标签和状态，通过对应的 `glab mr` 命令处理：

- **读取 MR**：`glab mr view <number> --comments`，以及用于获取 diff 的 `glab mr diff <number>`。
- **列出待分流的外部 MR**：`glab mr list -F json`，然后只保留作者不是项目成员／所有者的 MR（贡献者的 MR，而不是维护者进行中的工作）。
- **评论／加标签／关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 对 issue 和 MR 分别编号，因此只要知道维护者指的是哪种来源，`#42` 就没有歧义。

<a id="when-a-skill-says-publish-to-the-issue-tracker"></a>

## 当技能说“发布到 issue 跟踪器”

创建 GitLab issue。

<a id="when-a-skill-says-fetch-the-relevant-ticket"></a>

## 当技能说“获取相关工单”

运行 `glab issue view <number> --comments`。

## Wayfinding operations

由 `/wayfinder` 使用。**地图**是一个 issue，以**子 issue** 作为工单。

- **地图**：一个带 `wayfinder:map` 标签的 issue，正文包含 Notes / Decisions-so-far / Fog。`glab issue create --label wayfinder:map`。（在支持原生 epic 的 GitLab 套餐中，也可以由 epic 承载地图；带标签的 issue 则适用于所有环境。）
- **子工单**：issue 描述顶部包含 `Part of #<map>`，并带标签 `wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。领取后，工单分配给主导工作的开发者。
- **阻塞**：GitLab 的**原生阻塞链接**，是规范且在 UI 中可见的表示。使用 `/blocked_by #<n>` 快捷操作，以 note 发布（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接属于 Premium/Ultimate 功能；免费套餐（或不可用时）回退为描述顶部的一行 `Blocked by: #<n>, #<n>`。所有阻塞项关闭后，工单解除阻塞。
- **前沿查询**：使用 `glab issue list -F json`，限定为地图子项，排除存在开放阻塞项的条目：原生 `blocked_by` 链接指向开放 issue（`glab api projects/:id/issues/:iid/links`），或 `Blocked by` 行中有开放 issue；也排除已分配负责人的条目。按地图顺序取第一项。
- **领取**：`glab issue update <n> --assignee @me`，这是会话的第一次写入。
- **解决**：先 `glab issue note <n> --message "<answer>"`，再 `glab issue close <n>`，然后将上下文指针（要点 + 链接）追加到地图的 Decisions-so-far。
