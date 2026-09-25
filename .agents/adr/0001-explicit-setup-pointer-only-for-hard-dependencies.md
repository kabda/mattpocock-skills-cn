<a id="explicit-setup-matt-pocock-skills-pointer-only-for-hard-dependencies"></a>

# 仅为硬依赖显式添加 `/setup-matt-pocock-skills` 指针

工程技能依赖 `/setup-matt-pocock-skills` 初始化的各仓库配置（issue 跟踪器、分流标签词汇、领域文档布局）。有些技能离开配置就无法有效工作：它们必须发布到特定 issue 跟踪器，或应用特定标签字符串。另一些仅用配置来提升输出精度（词汇、ADR 感知），缺少配置时可平稳降级。

我们将其分为**硬依赖**和**软依赖**技能：

- **硬依赖**（`to-tickets`、`to-spec`、`triage`）：明确加一行：*“……应当已提供给你；否则运行 `/setup-matt-pocock-skills`。”* 没有映射，输出会是错误的，而不只是模糊。
- **软依赖**（`diagnose`、`tdd`、`improve-codebase-architecture`）：只在一般性文字中提及“项目领域术语表”和“所涉及区域的 ADR”。文档不存在时，技能仍可运行，只是输出不够精确。

这种区分让软依赖技能保持较低 token 成本，避免机械照搬 setup 指针到并不依赖它的地方。
