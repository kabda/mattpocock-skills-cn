<a id="issue-tracker-github"></a>

# Issue 跟踪器：GitHub

本仓库的 issue 和规格说明存放为 GitHub issue。所有操作使用 `gh` CLI。

<a id="conventions"></a>

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取 issue**：`gh issue view <number> --comments`，用 `jq` 筛选评论，并同时获取标签。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 和 `--state` 筛选。
- **评论 issue**：`gh issue comment <number> --body "..."`
- **添加／移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

根据 `git remote -v` 推断仓库；在克隆目录内运行时，`gh` 会自动完成。

<a id="pull-requests-as-a-triage-surface"></a>

## 将 pull request 作为分流来源

**PRs as a request surface: no.** _（如果本仓库把外部 PR 视为功能请求，设为 `yes`；`/triage` 会读取此开关。）_

设为 `yes` 时，PR 使用与 issue 相同的标签和状态，通过对应的 `gh pr` 命令处理：

- **读取 PR**：`gh pr view <number> --comments`，以及用于获取 diff 的 `gh pr diff <number>`。
- **列出待分流的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，然后只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的条目（排除 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论／加标签／关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 issue 和 PR 共用编号空间，因此裸 `#42` 可能是任意一种：先用 `gh pr view 42` 解析，失败后回退到 `gh issue view 42`。

<a id="when-a-skill-says-publish-to-the-issue-tracker"></a>

## 当技能说“发布到 issue 跟踪器”

创建 GitHub issue。

<a id="when-a-skill-says-fetch-the-relevant-ticket"></a>

## 当技能说“获取相关工单”

运行 `gh issue view <number> --comments`。

## Wayfinding operations

由 `/wayfinder` 使用。**地图**是一个 issue，以**子 issue** 作为工单。

- **地图**：一个带 `wayfinder:map` 标签的 issue，正文包含 Notes / Decisions-so-far / Fog。`gh issue create --label wayfinder:map`。
- **子工单**：以 GitHub 子 issue 方式链接到地图的 issue（对子 issue 端点使用 `gh api`）。未启用子 issue 时，将子项加入地图正文的任务列表，并在子项正文顶部放置 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。领取后，工单分配给主导工作的开发者。
- **阻塞**：GitHub 的**原生 issue 依赖**，是规范且在 UI 中可见的表示。使用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加关系，其中 `<blocker-db-id>` 是阻塞项的数值**数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，*不是* `#number` 或 `node_id`）。GitHub 报告 `issue_dependencies_summary.blocked_by`（只计开放阻塞项，作为实时关卡）。依赖功能不可用时，回退为子项正文顶部的一行 `Blocked by: #<n>, #<n>`。所有阻塞项关闭后，工单解除阻塞。
- **前沿查询**：列出地图的开放子项（`gh issue list --state open`，范围限定为地图的子 issue／任务列表），排除有开放阻塞项（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中有开放 issue）或已分配负责人的条目；按地图顺序取第一项。
- **领取**：`gh issue edit <n> --add-assignee @me`，这是会话的第一次写入。
- **解决**：先 `gh issue comment <n> --body "<answer>"`，再 `gh issue close <n>`，然后将上下文指针（要点 + 链接）追加到地图的 Decisions-so-far。
