<a id="lazy-loading-writing-for-agents-in-skills-that-judge-agent-facing-writing"></a>

# 在评估 agent 文档的技能中延迟加载 `writing-for-agents`

`retro` 每次运行都加载 `writing-for-agents`，并非仅在写作前加载。要求延后到编辑技能、`AGENTS.md`/`CLAUDE.md` 或文档时才加载的请求不在范围内。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

`writing-for-agents` 不只是风格指南。它定义什么是 no-op 指令，什么样的技能才好；`retro` 在写任何东西前，就用这些定义评估读到的引导文件。只读并报告的复盘也需要它。延迟加载后，No-ops 和 Skills 候选项就失去了评判尺度。

<a id="prior-requests"></a>

## 既往请求

- #1238：“retro：仅在写作前加载 writing-for-agents”（已关闭）
