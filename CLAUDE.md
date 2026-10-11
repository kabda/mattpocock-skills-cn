技能按分类目录组织在 `skills/` 下：

- `engineering/`：日常代码工作
- `productivity/`：日常非代码工作流工具
- `misc/`：保留但很少使用，未正式收录
- `in-progress/`：beta，刻意公开以征集反馈，不随插件发布
- `deprecated/`：不再使用

`engineering/` 或 `productivity/`（**正式收录**分类）中的每项技能，都必须在顶层 `README.md` 中被引用，并在 `.claude-plugin/plugin.json` 的 `skills` 数组中有条目（Claude Code 插件恰好只发布正式收录集合）。`misc/`、`in-progress/` 和 `deprecated/` 中的技能不得出现在这两处。

安装命令从 [.agents/install-block.md](./.agents/install-block.md) 逐字复制。`.claude-plugin/marketplace.json` 是本仓库自身的 marketplace。除 Claude Code 外，其他 agent 从这里安装以获取自动更新；Claude Code 使用 `claude-plugins-official`。修改任一 manifest 后，运行 `claude plugin validate . --strict`。[ADR 0002](./.agents/adr/0002-ship-as-a-claude-code-plugin.md) 记录了原因。

顶层 `README.md` 的每个技能条目，都必须以技能名链接到其 `SKILL.md`。

每个分类目录都有 `README.md`，用一行说明列出该分类的所有技能，并以技能名链接到其 `SKILL.md`。正式收录分类的 `README.md` 和顶层 `README.md` 按**用户调用**与**模型调用**分组；非正式收录分类（`misc/`、`in-progress/`）的 `README.md` 使用平铺列表。

`engineering/` 和 `productivity/` 中的技能还在 `docs/<bucket>/<skill-name>.md` 有面向人的文档页（docs 树镜像 `skills/` 下这两个分类目录）。无论分类，发布 URL 都是 `https://aihero.dev/skills-<skill-name>`，docs 路径仅用于仓库组织。新增、重命名或改变 `engineering/` 或 `productivity/` 中的技能行为时，按 [.agents/writing-docs.md](./.agents/writing-docs.md) 创建或同步文档页。完成的页面包含四节：**What it does**、**When to reach for it**、**Common questions**、**It's working if**。`writing-docs.md` 保存模板、章节顺序及寻找问题的方法。非正式分类（`misc/`、`in-progress/`、`deprecated/`）**不**配文档页。唯一例外是直接移除的正式技能，其页面继续保留并标记归档（参见 `writing-docs.md`）。

每个 `SKILL.md` 要么由用户调用（`disable-model-invocation: true` 加上 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`，仅人可访问），要么由模型调用（模型或用户均可访问）。参见 [.agents/invocation.md](./.agents/invocation.md)。

[`ask-matt`](./skills/engineering/ask-matt/SKILL.md) 是映射所有用户可访问技能及其关系的路由器。重新同步文档页的触发条件也适用于它：新增、重命名、移除用户可访问技能，或改变它在流程中的位置时，重新阅读并更新 `ask-matt` 的 `SKILL.md`，保持地图准确。新技能从不提及，或仍指向过时技能，都是路由器在说谎。

要把 `deprecated/` 和 `misc/` 之外的所有技能重新链接到本地 harness 技能目录（`~/.claude/skills`、`~/.agents/skills`），运行 `scripts/link-skills.sh`。每项都是指向本仓库的符号链接，所以 `git pull` 会使已安装技能保持最新；添加、移除或重命名技能后重新运行脚本。

本仓库所有文字中都不用 em dash（`SKILL.md`、docs、`README.md`、`CHANGELOG.md`、ADR、changeset、代码注释）。句子需要它时，按实际表达需要改用逗号、冒号、句号、括号或连词重写；绝不盲目替换字符。

## Agent skills

### Triage labels

规范名称保持不变，参见 `docs/agents/triage-labels.md`。按 [`SCOPE.md`](./SCOPE.md) 评估 issue。
