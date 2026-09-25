<a id="issue-tracker-local-markdown"></a>

# Issue 跟踪器：本地 Markdown

本仓库的 issue 和规格说明作为 Markdown 文件存放在 `.scratch/` 中。

<a id="conventions"></a>

## 约定

- 每个功能一个目录：`.scratch/<feature-slug>/`
- 规格说明位于 `.scratch/<feature-slug>/spec.md`
- 实现 issue 每张工单一个文件，位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 编号，绝不合并为单个工单文件
- 分流状态记录为每个 issue 文件顶部附近的一行 `Status:`（角色字符串见 `triage-labels.md`）
- 评论和对话历史追加到文件底部的 `## Comments` 标题下

<a id="when-a-skill-says-publish-to-the-issue-tracker"></a>

## 当技能说“发布到 issue 跟踪器”

在 `.scratch/<feature-slug>/` 下创建新文件（必要时创建目录）。

<a id="when-a-skill-says-fetch-the-relevant-ticket"></a>

## 当技能说“获取相关工单”

读取所引用路径的文件。用户通常直接传入路径或 issue 编号。

## Wayfinding operations

由 `/wayfinder` 使用。**地图**是一个文件，每张工单一个**子文件**。

- **地图**：`.scratch/<effort>/map.md`（正文包含 Notes / Decisions-so-far / Fog）。
- **子工单**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 编号，正文包含问题。`Type:` 行记录工单类型（`research`/`prototype`/`grilling`/`task`）；`Status:` 行记录 `claimed`/`resolved`。
- **阻塞**：顶部附近的一行 `Blocked by: NN, NN`。列出的每个文件都为 `resolved` 时，工单解除阻塞。
- **前沿**：扫描 `.scratch/<effort>/issues/` 中开放、未阻塞、未领取的文件；编号最前的优先。
- **领取**：任何工作之前，先设置 `Status: claimed` 并保存。
- **解决**：将答案追加到 `## Answer` 标题下，设置 `Status: resolved`，再将上下文指针（要点 + 链接）追加到 `map.md` 的 Decisions-so-far 中。
