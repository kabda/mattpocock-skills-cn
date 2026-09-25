<a id="the-canonical-install-block"></a>

# 规范安装片段

一种安装叙述，一套措辞。`README.md`、`.changeset/*` 和 `docs/` 下每一页都必须采用**这里的内容**，不能另写一套。先在这里修改，再传播到其他位置。

`mattpocock-skills` 已列入 **Claude Code 官方 marketplace**（配置名 `claude-plugins-official`，源仓库 `anthropics/claude-plugins-official`），每个 Claude Code 安装都开箱自带。无需先添加 marketplace。Anthropic 官方 marketplace 默认启用自动更新（[发现插件](https://code.claude.com/docs/en/discover-plugins)），所以“更新会自动到达”是真实陈述，而非愿望。

<a id="claude-code-the-plugin"></a>

## Claude Code：插件

<canonical-block name="claude-code">

```bash
claude plugins install mattpocock-skills
```

或者在会话内：

```
/plugin install mattpocock-skills
```

它已在 Claude Code 官方 marketplace 中，无需先添加任何内容，更新会自动到达。

</canonical-block>

<a id="codex-and-other-agents-skillssh"></a>

## Codex 及其他 agent：skills.sh

插件仅适用于 Claude Code。其他地方，[skills.sh](https://skills.sh/mattpocock/skills) 会把可编辑技能文件复制到项目。`README.md` 使用整套安装形式：

<canonical-block name="skills-sh-whole-set">

```bash
npx skills@latest add mattpocock/skills
```

选择想要的技能，以及安装到哪些编码 agent。**安装器允许选择技能：请务必选上 `setup-matt-pocock-skills`。**

</canonical-block>

单独提及某项技能时，则使用单技能形式。注意，**`docs/` 页面不消费这个片段**：ai-hero 在正文上方渲染安装组件，页面再写命令就会重复。参见 [writing-docs.md](./writing-docs.md)。

<canonical-block name="skills-sh-one-skill">

```bash
npx skills@latest add mattpocock/skills --skill=<name>
```

```bash
npx skills@latest update <name>
```

</canonical-block>

三处都固定使用 `skills@latest` 这一写法。`docs/` 页面以前各带一份这些命令，现在已删除这些片段，而非修正，因为网站自行渲染安装命令。

<a id="the-two-routes-are-exclusive"></a>

## 两条路线互斥

插件是你订阅的受管理、只读的包。skills.sh 写入你拥有并编辑的文件。两者都安装会让每项技能出现两份：始终说“选一种”。

<a id="not-the-install-story"></a>

## 不作为安装主线

`.claude-plugin/marketplace.json` 让仓库成为自己的单插件 marketplace（先 `/plugin marketplace add mattpocock/skills`，再 `/plugin install mattpocock-skills@mattpocock`）。官方条目已取代它。保留它是为了直接安装仓库（未发布提交或 fork）的回退方案，**不**向用户作为安装文档介绍。
