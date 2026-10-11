# Matt Pocock Skills

供 Claude Code 加载的一组 agent 技能（slash command 和行为）。技能按分类组织，并通过 `/setup-matt-pocock-skills` 生成的各仓库配置使用。

## Language

**Issue tracker**（issue 跟踪器）：
承载仓库 issue 的工具：GitHub Issues、Linear、本地 `.scratch/` Markdown 约定，或类似工具。`to-tickets`、`to-spec`、`triage` 等技能会读写它。
_Avoid_: backlog manager, backlog backend, issue host

**Issue**：
**Issue tracker** 内单个被跟踪的工作单位：bug、任务、规格说明，或 `to-tickets` 产出的切片。
_Avoid_: ticket（仅在引用将其称为 ticket 的外部系统，或指下文的 **Decision ticket** 时使用）

**Decision ticket**（决策工单）：
`wayfinder` 的工作单位：`wayfinder:map` 的子 **Issue**，承载一个解决后产出决策的*问题*，而非待执行的构建切片。**decision** 限定词将它与实现工单区分开；`wayfinder` 引入该术语后，简称 "ticket"。

**Triage role**（分流角色）：
分流时应用到 **Issue** 的规范状态机标签（例如 `needs-triage`、`ready-for-afk`）。每个角色通过 `docs/agents/triage-labels.md` 映射到 **Issue tracker** 中的真实标签字符串。

<a id="relationships"></a>

## 关系

- 一个 **Issue tracker** 承载多个 **Issue**
- 一个 **Issue** 同时带一个 **Triage role**
- **Decision ticket** 是一种 **Issue**（`wayfinder:map` 的子项）

<a id="flagged-ambiguities"></a>

## 已标记的歧义

- "backlog" 以前既指承载 issue 的*工具*，也指其中的*工作集合*。已解决：工具称为 **Issue tracker**；"backlog" 不再作为领域术语。
- "backlog backend" / "backlog manager"。已解决：合并为 **Issue tracker**。
