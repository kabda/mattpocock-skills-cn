<a id="grilling-through-the-harnesss-native-question-tool"></a>

# 通过 harness 原生提问工具进行追问

追问会话（`/grilling`、`/grill-me`、`/grill-with-docs` 及其他技能内部的追问）以普通聊天文本提问。要求改用 harness 内置提问 UI（Claude Code 的 `AskUserQuestion`、宿主“提问工具”、结构化或批量问卷模式）的请求不在范围内。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

技能是与 harness 无关的文本，运行在 Claude Code、Codex、Copilot、Cursor 及 skills.sh 支持的其他环境中。各 harness 的提问工具不同，甚至没有。点名某个 harness 的工具，就意味着每项追问技能都要有专用分支，或只能在某个平台正确工作。

提问 UI 也会改变追问本身。结构化选择器推动模型使用预设答案的选择题，而追问需要你用自己的话回答开放问题，每次解决决策树的一条分支。我试过 `AskUserQuestion` UI，不希望这些技能使用它。

如果更喜欢 harness 的提问工具，在自己的 `CLAUDE.md` / `AGENTS.md` 中说明即可（“追问时，通过 AskUserQuestion 提问”）。这是一行个人偏好，共享技能无需知道。

<a id="prior-requests"></a>

## 既往请求

- #19：“grill-me：并不总是使用提问工具”
- #643：“建议：追问会话中使用 AskQuestion 接收结构化输入”
- #840：“追问会话使用宿主提问工具”
- #1107：“Grilling 并未开箱即用地使用 Agent 原生问答工具”
- #1152：“建议：用于批量追问的实验性 HTML 问卷模式”
