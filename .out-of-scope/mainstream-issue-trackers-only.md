<a id="issue-tracker-integrations-github-gitlab-and-local-markdown-only"></a>

# Issue 跟踪器集成：仅 GitHub、GitLab 和本地 Markdown

`setup-matt-pocock-skills` 只为三种 issue 跟踪器提供一等支持，在 `skills/engineering/setup-matt-pocock-skills/` 中各有一个初始模板：

- **GitHub**（`issue-tracker-github.md`，通过 `gh`）
- **GitLab**（`issue-tracker-gitlab.md`，通过 `glab`）
- **本地 Markdown**（`issue-tracker-local.md`，文件位于 `.scratch/`）

为其他跟踪器添加一等后端支持的请求不在范围内，包括 Jira、Linear、Azure DevOps、Trello、YouTrack 和新兴面向 agent 的跟踪器。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

每个 issue 跟踪器后端都会把 CLI 形式硬编码进技能（命令、参数、输出解析）。每个新后端都带来永久维护面：工具 CLI 演变时必须继续工作，还要持续对照 `/to-spec`、`/to-tickets`、`/triage` 等验证。我使用 GitHub，所以能真正维护其正确性。GitLab 形式足够相近，可以一同维护；本地 Markdown 则完全不需要 CLI。

流行程度不会改变这一点。Jira 使用广泛，也有官方 CLI（`acli`），但仍不会新增模板：我不使用这个后端，却要持续验证它特有的链接语义、工作流状态和 CLI 特性。无论工具是否主流，成本都由我承担。

其他跟踪器都通过 `/setup-matt-pocock-skills` 的 **Other** 选项配置：用一段话描述工作流，技能把它记录为 `docs/agents/issue-tracker.md` 中的文字说明。该文件归你所有。如果打磨出可用的 Jira 或 Linear 工作流，保留在自己的仓库或发布出来，并让 setup 引用它。

<a id="prior-requests"></a>

## 既往请求

- #99：“添加 dex 作为 issue 跟踪器后端”（请求时 dex 约发布 3 个月，约有 300 stars）
- #258：“通过 Rovo MCP 为 Jira 添加一等 issue 跟踪器支持”
- #1137：“通过 Atlassian 官方 CLI（`acli`）为 Jira 添加一等 issue 跟踪器支持”
