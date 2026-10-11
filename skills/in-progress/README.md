<a id="in-progress"></a>

# 开发中

Beta。这些技能刻意公开：试用并告诉我哪里出问题。在进入稳定分类前，它们不包含在插件或顶层 README 中，没有配套文档页，也可能不经通知就改变或消失。

插件不会提供这些技能。可以直接安装一项：

```bash
npx skills@latest add mattpocock/skills --skill=<name>
```

- **[loop-me](./loop-me/SKILL.md)**：以当前目录作为有状态工作空间，跨多个会话通过追问形成可实施的工作流规格说明。由用户调用。
- **[writing-beats](./writing-beats/SKILL.md)**：以自选冒险的方式，把文章塑成节拍之旅。选择起始节拍，只写该节拍，再转向下一节拍，直到文章自然结束。
- **[writing-fragments](./writing-fragments/SKILL.md)**：通过追问从你这里挖掘片段（各种形态的写作精华），追加到同一文档，作为未来文章的原始素材。
- **[writing-shape](./writing-shape/SKILL.md)**：读取原始素材 Markdown 文件，逐段塑成文章，每一步都讨论格式选择。
- **[claude-handoff](./claude-handoff/SKILL.md)**：通过 `claude --bg` 把交接摘要作为提示词，将当前对话交给立即接手工作的全新后台 agent。由用户调用。
- **[setup-ts-deep-modules](./setup-ts-deep-modules/SKILL.md)**：把 dependency-cruiser 接入 TypeScript 仓库，让每个包成为深模块：实现隐藏在子目录，只能经入口文件访问，测试也通过入口验证行为。由用户调用。
- **[chief-of-staff](./chief-of-staff/SKILL.md)**：在长时间运行的单个会话中，协调子 agent 和定期计划推进长期目标，并持续改善 agent 工作环境。由用户调用。
