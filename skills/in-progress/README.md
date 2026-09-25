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
- **[implement-spec](./implement-spec/SKILL.md)**：在一个分支实现整份规格说明。把工单当作任务图而非列表，在就绪前沿上运行实现子 agent 以获得最大并发度，最终通过单个 PR 交付。由用户调用。
- **[pr](./pr/SKILL.md)**：pull request 正文形态的参考：基于一手来源（而非 diff）的摘要、展示变更的最小图示、前后成对证据、刻意排除的内容，以及单向门/双向门判断。由模型调用。
- **[retro](./retro/SKILL.md)**：会话后提出对编码 agent 环境的改进建议（引导文件、编码标准、自动检查、工具）。STUB：仅有设计笔记，尚不可用。由用户调用。
