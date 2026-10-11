<a id="what-it-does"></a>

## 它能做什么

`pr` 规定 PR 正文的形式：展示变更的 **Summary**、证明有效的 **Evidence**，以及评估落地风险的 **Merge Danger**。它是格式参考，不是工作流。它不推送分支、创建 PR 或决定内容，只告诉 [agent](https://www.aihero.dev/ai-coding-dictionary/agent) 撰写正文时应采用什么形式。

摘要采用视觉表达，而非段落。普通 PR 正文用文字描述 diff，这项技能选择能讲清关键点的**最小视图**（伪代码、调用树、组件树、文件树、Mermaid 图或整理过的 diff），周围文字保持简短。审查者已经打开 diff，因此正文先展示整体形态，再供其阅读细节。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/pr`，或由 agent 在撰写 PR 正文时自动使用。

| 你的情况 | 使用 |
| --- | --- |
| 分支已就绪，需要便于审查者扫读的正文 | `pr` |
| 代码已写好，但还无人审查 | 先 [code-review](https://aihero.dev/skills-code-review)，再 `pr` |
| PR 已创建，开始收到审查评论 | 本套技能暂未覆盖，`pr` 只写正文 |

<a id="the-template"></a>

## 模板

按以下顺序包含三节：

- **Summary**：一项或多项小型视觉表达，各自紧挨所支持的短文字。通常用一项，有时多项，很少全部都用。只保留审查者需要的调用、文件、props 和边界。
- **Evidence**：前后对照。视觉变化且[环境](https://www.aihero.dev/ai-coding-dictionary/environment)能够截图时，截图是最有力证据。否则，用伪代码表达之前失败、现在通过的确切测试，或展示变化的控制台输出。
- **Merge Danger**：变更属于**单向门**还是**双向门**，以及**影响范围**。双向门可以低成本撤销；单向门（破坏性迁移、移除公共 API、难以撤销的决策）则不行。影响范围说明变更错误时可能破坏什么：布局位移、API 使用方、移动端响应式表现。

门的判断是引导观念。它将“是否能安全合并”从直觉变成审查者可以质疑的明确论断，也告诉审查者把[人工审查](https://www.aihero.dev/ai-coding-dictionary/human-review)精力花在哪里。影响范围小的双向门可以扫读，单向门则需仔细阅读。

<a id="common-questions"></a>

## 常见问题

**能相信 agent 自己对门的判断吗？**

不能盲信，这正是要求明确说明的原因。写出变更的 agent 也在评估变更，因此它声称“双向门、影响小”时最值得怀疑。Diff 也常隐藏可撤销性。一位用户说：“回滚提交不会撤回已发出的邮件。”带开关的发布也只有在新格式首次写入前才是双向门。技能给出定义（破坏性操作和难撤销决策是单向门），并非检查清单，所以尤其要核对 Merge Danger。两件事有帮助：确保 agent 面前有[工单](https://www.aihero.dev/ai-coding-dictionary/ticket)或[规格说明](https://www.aihero.dev/ai-coding-dictionary/spec)，不只 diff；把仓库始终视为单向门的变更（schema 迁移、对外发送或删除）记录在 agent 作判断前会读取的位置。

**它会替我创建 PR 吗？**

不会，`pr` 只处理正文。[implement](https://aihero.dev/skills-implement) 最后提交到当前分支。创建 PR 的技能或选项（`/to-pr`，或让 `implement` 创建 PR 而非提交）仍是开放建议。一位用户的办法是给本地 `implement` 加一句覆盖指令，要求创建 PR。[implement-spec](https://aihero.dev/skills-implement-spec) 是例外：跟踪器通过 PR 关闭工作或你提出要求时，它会创建草稿 PR。由于 `pr` 由模型调用，要求 agent 创建 PR 时，它会采用本技能的正文形式。

**会不会又生成一大堵文字和图？**

技能旨在防止这种情况，但仍可能发生。用户对 agent PR 正文的抱怨一致：“摘要很长，但我只想知道改了什么、如何验证、可能破坏什么、是否安全合并。”技能要求省去开场白、保持文字简短、选择最小视图，通常一幅图，很少全用。仍出现一叠图时，是 agent 忽略了要求。如果正文大是因为 diff 大，问题在 PR 的规模，`pr` 不会替你拆分。

**仓库已有 PR 模板，哪个优先？**

默认没有谁优先。`pr` 有自己的模板，不查找 `.github/pull_request_template.md` 等文件。已有多位用户要求采用仓库模板。没有额外指示时，agent 会面对两套竞争指令。请在仓库 agent 文档中解决，例如填写仓库模板，并在其中放入 Summary、Evidence 和 Merge Danger。

**输出是 HTML 吗？为什么 Mermaid 图不渲染？**

输出是 Markdown PR 正文，不是 HTML 页面。GitHub 和 GitLab 会渲染 PR 描述中的 Mermaid，终端不会，所以 agent 本地展示时看起来是原始文本。CLI 用户的办法是用 ASCII Mermaid 渲染器，或让 agent 为 PR 附上 HTML 版本。Mermaid 只是六种视图之一，调用树、文件树或整理过的 diff 在各处都能一致阅读。

**它能整理收到的审查评论吗？**

不能，写完正文就停止。用户多次要求分流开发者或审查 bot 的评论，判断哪些值得处理、哪些并非问题；本技能不处理这些。

**PR 改变时，它会同步更新正文吗？**

不会，它在某个时点撰写正文，审查中修改 PR 会让正文过时。大改后要求 agent 重写正文即可；它又在撰写 PR 正文，因此仍采用相同形式。

**改动没有 UI，Evidence 写什么？**

除截图外的证据都可使用。仅当变化是视觉性质时，截图才最有力。迁移、后台任务或重构的证据是之前失败、现在通过的确切测试，或变化的控制台输出。单独“测试全绿”只是论断，不是前后对照。

**它会注明正文由 LLM 撰写吗？**

不会自行注明。一位用户在仓库 agent 文档中设置常驻指令，要求每个 issue、评论和 PR 都以披露文字结尾。规则应属于仓库，覆盖 agent 发布的一切，而非仅针对一种文档的模板。

<a id="its-working-if"></a>

## 如何判断它有效

- 打开 diff 前，仅凭 Summary 视觉表达就能知道 PR 改了什么。
- 正文没有开场白，直接从 Summary 标题开始。
- Evidence 展示前后对照，而非只声称测试通过。
- 每个 PR 都说明门和影响范围，单向门是需要放慢审查的部分。

<a id="where-it-fits"></a>

## 它在流程中的位置

通过 PR 交付时，`pr` 在审查和复盘之间：`to-spec → to-tickets → implement → code-review → pr → retro`。它由模型调用，因此链条外 agent 撰写 PR 正文时也会自行使用。

- [code-review](https://aihero.dev/skills-code-review) 在前，因为正文应描述已经审查过的 diff。
- [implement](https://aihero.dev/skills-implement) 产出正文描述的提交。

不确定当前情况适合哪个技能时，[ask-matt](https://aihero.dev/skills-ask-matt) 会在整套技能中为你指路。
