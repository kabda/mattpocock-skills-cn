# 上游 1.3.1 快照增量对比

本次对比范围是 `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` 至 `49dd158d1076134a641b33efb035946536778336`。版本字段从 1.2.3 升到 1.3.1；当前快照还含 16 个待发布 changeset。采用 Git rename detection 的结果为 118 条路径变更：60 修改、36 新增、15 删除、7 重命名。某些技能移动因为同时大改，Git 识别成新增与删除；以下技能层面的说明按实际迁移解释。

## 技能集合与目录

| 变化 | 中文同步结果 |
| --- | --- |
| implement-spec、pr、retro 从 in-progress 转入 engineering | 移动技能及 agent 元数据，翻译新增正式文档，更新根 README、分类 README、插件清单和 ask-matt 流程 |
| 移除 resolving-merge-conflicts | 删除技能与元数据，移除正式索引和路由；docs 页面保留归档说明 |
| 新增 chief-of-staff beta | 翻译技能和简介，补齐上游遗漏的 beta 分类索引，保持不随正式插件发布 |
| CONTEXT.md 改名 GLOSSARY.md | 同步根文档、GLOSSARY-FORMAT.md、GLOSSARY-MAP.md 约定与当前技能引用；历史日志中的旧文件名保留 |
| 新增贡献范围规则与 issue 表单 | 翻译 SCOPE.md、6 项新增范围之外政策、bug/idea 表单及展示入口；工作流原样同步 |

正式发布集合从 25 增为 27；总技能数量仍为 38。新中文用户入口见 [更新对比页](../../wiki/upstream-1.3.1.html)。

## 行为变化

| 技能 / 范围 | 上游变化 |
| --- | --- |
| ask-matt | 描述技能作用或建议跳步前先读 SKILL.md；加入并行实现、PR 正文、复盘路线，移除合并冲突路线 |
| code-review | 搜索所有标准来源，存在时必须包含 CODING_STANDARDS.md 和 CONTRIBUTING.md；同时在前台发起两个审查子 agent；通过已配置的跟踪器文档获取规格说明 |
| diagnosing-bugs | 强制变异制造 Red 时，先以 diff 对照原始副本证明变异生效 |
| implement | 先读取传入工单引用并核对标题；明确通过 Skill 工具调用参考技能 |
| implement-spec | 按任务图前沿在独立 worktree 并行实现，汇集集成分支；是否创建 PR 由跟踪器关闭方式或用户要求决定 |
| setup / tracker 模板 | 创建缺失标签；修正 GitHub 外部 PR 查询、sub-issues 命令和数据库 id 使用；GitLab JSON 输出改用 -O json；模板说明准确指向标签映射列 |
| to-tickets | 支持 GitHub 原生 sub-issues；仅没有原生阻塞边时才在正文保留 Blocked by 节 |
| tdd | 每个建议 seam 用一行说明能发现什么、会遗漏什么 |
| wayfinder | 地图和决策工单不带 ready-for-agent 等分流标签；第二遍用真实 id 写交叉引用；研究分支推送且不建 PR；按标签读取类型 |
| grilling | 用户只回复 yes 等确认时，接受 agent 已提出的建议 |
| handoff / claude-handoff | 临时目录使用 TMPDIR、/tmp 或 Windows TEMP；后台交接从文件读取，避免摘要经 shell 展开 |
| teach | 区分教学工作目录与技能格式目录；测验改变正确答案位置 |
| wizard | 模板原字节同步：更稳健的 env 写入、EOF 和 readline 处理、符号链接及 run_wizard 入口 |
| 安装 | Claude 官方 marketplace、Codex marketplace、Copilot autoUpdate、VS Code 入口与 Gemini 路径更新；skills.sh 手动更新说明 |

这些是冻结源文的行为要求，未进行实际 harness、GitHub 或 GitLab 运行验证。

## 检查发现与处理

- 上游新 beta 技能缺少分类索引，按本仓库规则补齐一行，精确登记为本地增补。
- 原自动验收将路径数、分类数和正式集合固定为旧版本。本次改为登记并核对冻结快照计数，补充分类索引完整性检查；归档 docs 单独核对。
- 新 YAML 表单仅允许精确登记的展示字段变化，其余字段仍做结构、类型和值比较。
- 新增文档的标题全部译成中文，保持英文 fragment 兼容；命令和固定模板字面量保留原文。
- 旧基线记录移至 [validation-1.2.3.md](validation-1.2.3.md)；当前来源、进度、验收及中文说明全部同步。
- 上游尚有文档与技能正文之间的旧描述，逐项列于 [validation.md](validation.md)。译文保留源文语义，未改写为假定行为。

## 完整源路径变更清单

以下清单由两个冻结提交的 Git 对象生成。状态是 Git 对文件相似度的判断，不等同于技能的业务迁移分类。

| 状态 | 原路径 | 当前路径 |
| --- | --- | --- |
| 修改 | `.agents/adr/0002-ship-as-a-claude-code-plugin.md` | `.agents/adr/0002-ship-as-a-claude-code-plugin.md` |
| 修改 | `.agents/install-block.md` | `.agents/install-block.md` |
| 修改 | `.agents/invocation.md` | `.agents/invocation.md` |
| 修改 | `.agents/writing-docs.md` | `.agents/writing-docs.md` |
| 删除 | `.changeset/add-implement-spec-skill.md` | 无 |
| 删除 | `.changeset/add-pr-skill.md` | 无 |
| 新增 | 无 | `.changeset/ask-matt-read-skill-first.md` |
| 新增 | 无 | `.changeset/code-review-standards-and-subagents.md` |
| 新增 | 无 | `.changeset/diagnosing-bugs-prove-mutation.md` |
| 删除 | `.changeset/domain-modeling-trigger-context-adr.md` | 无 |
| 删除 | `.changeset/fix-yaml-frontmatter-colons.md` | 无 |
| 新增 | 无 | `.changeset/github-tracker-external-pr-list.md` |
| 删除 | `.changeset/grilling-add-hr-between-questions.md` | 无 |
| 删除 | `.changeset/grilling-remove-em-dashes.md` | 无 |
| 新增 | 无 | `.changeset/grilling-yes-accepts-recommendation.md` |
| 新增 | 无 | `.changeset/handoff-temp-dir.md` |
| 新增 | 无 | `.changeset/implement-skill-tool-wording.md` |
| 新增 | 无 | `.changeset/implement-ticket-reference.md` |
| 删除 | `.changeset/remove-em-dashes-repo-wide.md` | 无 |
| 删除 | `.changeset/retro-deterministic-checks.md` | 无 |
| 新增 | 无 | `.changeset/setup-tracker-fixes.md` |
| 删除 | `.changeset/skill-tool-invocation-terminology.md` | 无 |
| 新增 | 无 | `.changeset/tdd-seam-tradeoffs.md` |
| 新增 | 无 | `.changeset/teach-quiz-answer-position.md` |
| 新增 | 无 | `.changeset/teach-workspace-root.md` |
| 新增 | 无 | `.changeset/to-tickets-sub-issues.md` |
| 删除 | `.changeset/user-invoked-skill-invocation.md` | 无 |
| 删除 | `.changeset/wait-what-context-map.md` | 无 |
| 新增 | 无 | `.changeset/wayfinder-labels-refs-research-prs.md` |
| 新增 | 无 | `.changeset/wizard-template-fixes-2.md` |
| 新增 | 无 | `.changeset/wizard-template-fixes.md` |
| 修改 | `.claude-plugin/plugin.json` | `.claude-plugin/plugin.json` |
| 新增 | 无 | `.github/ISSUE_TEMPLATE/bug.yml` |
| 新增 | 无 | `.github/ISSUE_TEMPLATE/config.yml` |
| 新增 | 无 | `.github/ISSUE_TEMPLATE/idea.yml` |
| 新增 | 无 | `.github/workflows/needs-info.yml` |
| 新增 | 无 | `.github/workflows/triage-label.yml` |
| 新增 | 无 | `.out-of-scope/frozen-misc-skills.md` |
| 新增 | 无 | `.out-of-scope/harness-name-collisions.md` |
| 新增 | 无 | `.out-of-scope/lazy-load-writing-for-agents.md` |
| 修改 | `.out-of-scope/mainstream-issue-trackers-only.md` | `.out-of-scope/mainstream-issue-trackers-only.md` |
| 新增 | 无 | `.out-of-scope/native-question-tool.md` |
| 新增 | 无 | `.out-of-scope/new-skills.md` |
| 新增 | 无 | `.out-of-scope/subagent-recursion.md` |
| 修改 | `CHANGELOG.md` | `CHANGELOG.md` |
| 修改 | `CLAUDE.md` | `CLAUDE.md` |
| 重命名（100%） | `CONTEXT.md` | `GLOSSARY.md` |
| 修改 | `README.md` | `README.md` |
| 新增 | 无 | `SCOPE.md` |
| 新增 | 无 | `docs/agents/triage-labels.md` |
| 修改 | `docs/engineering/ask-matt.md` | `docs/engineering/ask-matt.md` |
| 修改 | `docs/engineering/code-review.md` | `docs/engineering/code-review.md` |
| 修改 | `docs/engineering/codebase-design.md` | `docs/engineering/codebase-design.md` |
| 修改 | `docs/engineering/diagnosing-bugs.md` | `docs/engineering/diagnosing-bugs.md` |
| 修改 | `docs/engineering/domain-modeling.md` | `docs/engineering/domain-modeling.md` |
| 修改 | `docs/engineering/grill-with-docs.md` | `docs/engineering/grill-with-docs.md` |
| 新增 | 无 | `docs/engineering/implement-spec.md` |
| 修改 | `docs/engineering/implement.md` | `docs/engineering/implement.md` |
| 修改 | `docs/engineering/improve-codebase-architecture.md` | `docs/engineering/improve-codebase-architecture.md` |
| 新增 | 无 | `docs/engineering/pr.md` |
| 修改 | `docs/engineering/prototype.md` | `docs/engineering/prototype.md` |
| 修改 | `docs/engineering/research.md` | `docs/engineering/research.md` |
| 修改 | `docs/engineering/resolving-merge-conflicts.md` | `docs/engineering/resolving-merge-conflicts.md` |
| 新增 | 无 | `docs/engineering/retro.md` |
| 修改 | `docs/engineering/setup-matt-pocock-skills.md` | `docs/engineering/setup-matt-pocock-skills.md` |
| 修改 | `docs/engineering/tdd.md` | `docs/engineering/tdd.md` |
| 修改 | `docs/engineering/to-spec.md` | `docs/engineering/to-spec.md` |
| 修改 | `docs/engineering/to-tickets.md` | `docs/engineering/to-tickets.md` |
| 修改 | `docs/engineering/triage.md` | `docs/engineering/triage.md` |
| 修改 | `docs/engineering/wayfinder.md` | `docs/engineering/wayfinder.md` |
| 修改 | `docs/engineering/wizard.md` | `docs/engineering/wizard.md` |
| 修改 | `docs/productivity/grill-me.md` | `docs/productivity/grill-me.md` |
| 修改 | `docs/productivity/grilling.md` | `docs/productivity/grilling.md` |
| 修改 | `docs/productivity/handoff.md` | `docs/productivity/handoff.md` |
| 修改 | `docs/productivity/teach.md` | `docs/productivity/teach.md` |
| 修改 | `docs/productivity/to-questionnaire.md` | `docs/productivity/to-questionnaire.md` |
| 修改 | `docs/productivity/wait-what.md` | `docs/productivity/wait-what.md` |
| 修改 | `docs/productivity/writing-for-agents.md` | `docs/productivity/writing-for-agents.md` |
| 修改 | `package.json` | `package.json` |
| 修改 | `skills/engineering/README.md` | `skills/engineering/README.md` |
| 修改 | `skills/engineering/ask-matt/SKILL.md` | `skills/engineering/ask-matt/SKILL.md` |
| 修改 | `skills/engineering/code-review/SKILL.md` | `skills/engineering/code-review/SKILL.md` |
| 修改 | `skills/engineering/codebase-design/DESIGN-IT-TWICE.md` | `skills/engineering/codebase-design/DESIGN-IT-TWICE.md` |
| 修改 | `skills/engineering/diagnosing-bugs/SKILL.md` | `skills/engineering/diagnosing-bugs/SKILL.md` |
| 重命名（070%） | `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | `skills/engineering/domain-modeling/GLOSSARY-FORMAT.md` |
| 修改 | `skills/engineering/domain-modeling/SKILL.md` | `skills/engineering/domain-modeling/SKILL.md` |
| 新增 | 无 | `skills/engineering/implement-spec/SKILL.md` |
| 重命名（051%） | `skills/in-progress/implement-spec/agents/openai.yaml` | `skills/engineering/implement-spec/agents/openai.yaml` |
| 修改 | `skills/engineering/implement/SKILL.md` | `skills/engineering/implement/SKILL.md` |
| 修改 | `skills/engineering/improve-codebase-architecture/SKILL.md` | `skills/engineering/improve-codebase-architecture/SKILL.md` |
| 新增 | 无 | `skills/engineering/pr/CREDITS.md` |
| 重命名（096%） | `skills/in-progress/pr/SKILL.md` | `skills/engineering/pr/SKILL.md` |
| 重命名（100%） | `skills/in-progress/pr/agents/openai.yaml` | `skills/engineering/pr/agents/openai.yaml` |
| 删除 | `skills/engineering/resolving-merge-conflicts/SKILL.md` | 无 |
| 删除 | `skills/engineering/resolving-merge-conflicts/agents/openai.yaml` | 无 |
| 重命名（100%） | `skills/in-progress/retro/SKILL.md` | `skills/engineering/retro/SKILL.md` |
| 重命名（100%） | `skills/in-progress/retro/agents/openai.yaml` | `skills/engineering/retro/agents/openai.yaml` |
| 修改 | `skills/engineering/setup-matt-pocock-skills/SKILL.md` | `skills/engineering/setup-matt-pocock-skills/SKILL.md` |
| 修改 | `skills/engineering/setup-matt-pocock-skills/domain.md` | `skills/engineering/setup-matt-pocock-skills/domain.md` |
| 修改 | `skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md` | `skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md` |
| 修改 | `skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md` | `skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md` |
| 修改 | `skills/engineering/setup-matt-pocock-skills/triage-labels.md` | `skills/engineering/setup-matt-pocock-skills/triage-labels.md` |
| 修改 | `skills/engineering/tdd/SKILL.md` | `skills/engineering/tdd/SKILL.md` |
| 修改 | `skills/engineering/to-tickets/SKILL.md` | `skills/engineering/to-tickets/SKILL.md` |
| 修改 | `skills/engineering/triage/SKILL.md` | `skills/engineering/triage/SKILL.md` |
| 修改 | `skills/engineering/wayfinder/SKILL.md` | `skills/engineering/wayfinder/SKILL.md` |
| 修改 | `skills/engineering/wizard/template.sh` | `skills/engineering/wizard/template.sh` |
| 修改 | `skills/in-progress/README.md` | `skills/in-progress/README.md` |
| 新增 | 无 | `skills/in-progress/chief-of-staff/SKILL.md` |
| 新增 | 无 | `skills/in-progress/chief-of-staff/agents/openai.yaml` |
| 修改 | `skills/in-progress/claude-handoff/SKILL.md` | `skills/in-progress/claude-handoff/SKILL.md` |
| 删除 | `skills/in-progress/implement-spec/SKILL.md` | 无 |
| 删除 | `skills/in-progress/pr/CREDITS.md` | 无 |
| 修改 | `skills/productivity/README.md` | `skills/productivity/README.md` |
| 修改 | `skills/productivity/grilling/SKILL.md` | `skills/productivity/grilling/SKILL.md` |
| 修改 | `skills/productivity/handoff/SKILL.md` | `skills/productivity/handoff/SKILL.md` |
| 修改 | `skills/productivity/teach/SKILL.md` | `skills/productivity/teach/SKILL.md` |
| 修改 | `skills/productivity/wait-what/SKILL.md` | `skills/productivity/wait-what/SKILL.md` |
