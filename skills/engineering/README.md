<a id="engineering"></a>

# 工程

我每天用于代码工作的技能。

<a id="user-invoked"></a>

## 用户调用

只有你输入时才可访问（Claude Code：`disable-model-invocation: true`；Codex：`agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`）。

- **[ask-matt](./ask-matt/SKILL.md)**：询问哪项技能或流程适合你的情境。本仓库用户调用技能的路由器。
- **[grill-with-docs](./grill-with-docs/SKILL.md)**：在追问会话中同时构建项目领域模型，打磨术语，并同步更新 `CONTEXT.md` 和 ADR。
- **[triage](./triage/SKILL.md)**：让 issue 流转经过分流角色状态机。
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)**：扫描代码库中的深化机会，以可视化 HTML 报告呈现，再对你选中的机会深入追问。
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)**：为本仓库配置工程技能所需的 issue 跟踪器、分流标签和领域文档布局。每个仓库运行一次。
- **[to-spec](./to-spec/SKILL.md)**：把当前对话转为规格说明，发布到 issue 跟踪器。
- **[to-tickets](./to-tickets/SKILL.md)**：把任意计划、规格说明或对话拆成曳光弹工单，每张声明阻塞关系，既可以是本地文件中的文本，也可以是真正跟踪器中的原生阻塞链接。
- **[implement](./implement/SKILL.md)**：实现规格说明或一组工单描述的工作，在事先约定的 seam 上驱动 `/tdd`，并在提交前用 `/code-review` 收尾。
- **[wayfinder](./wayfinder/SKILL.md)**：把大型工作（超过一个 agent 会话所能容纳的规模）规划为 issue 跟踪器上的共享决策工单地图，逐一解决，直到通往目标的道路清晰。

<a id="model-invoked"></a>

## 模型调用

模型或用户均可访问（带有丰富的触发措辞，使模型能按需使用）。

- **[prototype](./prototype/SKILL.md)**：构建一次性原型回答设计问题：状态/逻辑使用单个可分享 HTML 文件，UI 使用多个可切换变体。

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**：用于棘手 bug 和性能回归的严谨诊断循环：建立能因这个 bug 变 Red 的反馈循环 → 最小化 → 提出假设 → 加观测 → 修复 → 回归测试。
- **[research](./research/SKILL.md)**：由后台 agent 根据高可信一手来源调查问题，在仓库中保存带引用的 Markdown 研究结果。
- **[tdd](./tdd/SKILL.md)**：采用 red-green-refactor 循环的测试驱动开发，每次一个纵向切片地构建功能或修复 bug。
- **[domain-modeling](./domain-modeling/SKILL.md)**：通过质疑术语、用场景做压力测试，以及同步更新 `CONTEXT.md` 和 ADR，主动构建并打磨项目领域模型。
- **[codebase-design](./codebase-design/SKILL.md)**：设计深模块的共享方法与词汇：小接口、清晰 seam，以及通过接口测试。
- **[code-review](./code-review/SKILL.md)**：由并行子 agent 对固定基点以来的 diff 做双维度审查：**Standards**（是否遵守仓库编码标准及 Fowler 异味基线）和 **Spec**（是否忠实实现原始 issue/规格说明）。
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)**：逐块处理正在进行的 Git merge 或 rebase 冲突，追溯双方一手来源的意图来解决，再完成操作，绝不 `--abort`。
- **[wizard](./wizard/SKILL.md)**：生成交互式 bash 向导，引导人完成只有人能执行的步骤：开通基础设施、设置凭据或 CI secrets、操作陌生第三方控制台，或执行一次性迁移或切换。
