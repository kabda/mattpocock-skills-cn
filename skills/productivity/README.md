<a id="productivity"></a>

# 生产力

通用工作流工具，不限于代码。

<a id="user-invoked"></a>

## 用户调用

只有你输入时才可访问（Claude Code：`disable-model-invocation: true`；Codex：`agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`）。

- **[grill-me](./grill-me/SKILL.md)**：就计划或设计接受持续深入的访谈，直到设计树每条分支都已解决。
- **[handoff](./handoff/SKILL.md)**：把当前对话压缩成交接文档，让另一个 agent 继续工作。
- **[teach](./teach/SKILL.md)**：以当前目录作为有状态教学工作空间，跨多个会话教用户新技能或概念。
- **[to-questionnaire](./to-questionnaire/SKILL.md)**：把你无法独自回答的决策转成 Markdown 问卷，交给能回答的那个人（异步填写，或开会共同完成）。
- **[wait-what](./wait-what/SKILL.md)**：消息没讲明白时立即调用。agent 会用通俗英语和你的 `CONTEXT.md` 词汇重新解释，补上缺失上下文。

<a id="model-invoked"></a>

## 模型调用

模型或用户均可访问（带有丰富的触发措辞，使模型能按需使用）。

- **[grilling](./grilling/SKILL.md)**：围绕计划、决策或想法持续深入访谈用户，直到设计树每条分支都已解决。
- **[writing-for-agents](./writing-for-agents/SKILL.md)**：为 agent 编写文档：技能、AGENTS.md/CLAUDE.md，以及任何通过指针访问的文档。
