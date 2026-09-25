<a id="ship-the-skill-set-as-a-native-claude-code-plugin-defer-a-native-codex-plugin"></a>

# 将整套技能作为原生 Claude Code 插件发布；暂缓原生 Codex 插件

这些技能一直可以通过 [skills.sh](https://skills.sh/mattpocock/skills) 安装（`npx skills add mattpocock/skills`），它把可编辑技能文件复制到用户项目，适用于 Claude Code、Codex 及其他支持 Agent Skills 标准的 harness。一个反复出现的请求是**即插即用**的分发方式：订阅只读、持续更新、无需编辑的整套包，而非拥有一份 fork。这正是原生插件系统提供的能力。

我们发布原生 **Claude Code 插件**，目前**暂缓**原生 **Codex 插件**。这种区别由两个生态的插件 manifest 选择技能的方式与本仓库分类布局之间的关系所迫。

<a id="the-constraint-bucketed-skills-vs-single-path-selection"></a>

## 约束：分类技能与单路径选择

技能位于 `skills/` 下的分类目录：`engineering/` 和 `productivity/` 是**正式收录**（发布）的；`misc/`、`personal/`、`in-progress/` 和 `deprecated/` **不是**。插件必须只暴露横跨两个分类目录的正式集合。

- **Claude Code**：`.claude-plugin/plugin.json` 接受 **显式技能目录路径数组**形式的 `skills`。我们逐个列出正式技能，毫无歧义地排除其他内容，并添加 `.claude-plugin/marketplace.json`，让仓库成为自己的单插件 marketplace。已端到端验证：`claude plugin validate . --strict` 通过，`marketplace add` → `install` 能解析全部正式技能。

- **Codex**：`.codex-plugin/plugin.json` 的 `skills` 只接受**单个路径字符串**（数组会因 `missing or invalid plugin.json` 被拒绝），Codex 在其下递归发现 `SKILL.md`。无法从一个路径指定两个分类目录或筛选子集。测试并排除了两个变通方案：
  - 指向 `./skills/` 会连带发布 `deprecated/`、`in-progress/`、`personal/` 和 `misc/`：这些是刻意不正式收录的退役、草稿和个人技能。
  - 建立指向分类目录的精选扁平**符号链接**目录，安装后无法保留：Codex 把插件树复制到缓存时会**丢弃符号链接**，导致收到的技能为空。

为 Codex 提供仅含正式技能的单路径，可靠方式只有：(a) **重组**，让 `skills/` 只含正式技能（把非正式分类移出去，广泛影响 `CLAUDE.md`、`scripts/link-skills.sh`、分类 README，以及依赖 `in-progress/` 和 `personal/` 的本地开发流程）；或 (b) 将正式技能的**重复副本提交**到扁平目录（带来同步负担和第二个权威来源）。两者都是结构性决策，不应捆绑进 Claude 插件发布。这很可能正是最初未发布插件、如今记忆模糊的原因：manifest 格式无法干净表达分类仓库中的精选子集。

<a id="decision"></a>

## 决策

- 现在发布 **Claude Code 插件**（`.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`），只收录正式集合，作为 v1.2 的主要交付。
- 保留 **skills.sh** 作为通用安装器：它已经服务 Codex 和其他 harness，因此 Codex 用户仍有安装路径。
- **暂缓**原生 Codex 插件，直到决定是重组 `skills/` 为仅正式技能，还是提交生成的扁平副本。Codex 支持 `skills` 数组/include-list，或安装时保留符号链接后，再重新考虑。

<a id="invariants-this-creates"></a>

## 由此产生的不变量

- 每项正式技能都在 `.claude-plugin/plugin.json` 的 `skills` 数组中有条目（这已是 `CLAUDE.md` 的规则，现在也限定插件内容）。
- `.claude-plugin/plugin.json` 的 `version` 跟随 `package.json` 版本：发布时一起升级。Claude 根据插件 `version` 决定何时向已安装用户显示更新。

<a id="update-2026-08-05"></a>

## 更新：2026-08-05

`mattpocock-skills` 已获准进入 **Claude Code 官方 marketplace**（配置名 `claude-plugins-official`，源仓库 `anthropics/claude-plugins-official`），每个 Claude Code 安装都默认配置了它。`claude plugins install mattpocock-skills` 现为文档推荐路线，取代上方 `marketplace add` → `install` 路径。安装措辞位于 [.agents/install-block.md](../install-block.md)。

官方条目指向本仓库 Git URL，直接读取 `.claude-plugin/plugin.json`，因此不依赖 `.claude-plugin/marketplace.json`。后者仅作为直接安装仓库（未发布提交或 fork）的回退方案保留。

2026-08-05，使用 Claude Code 2.1.222，对照线上条目验证：

- `claude plugins install mattpocock-skills` 无需先添加 marketplace 即可解析，并报告 `mattpocock-skills@claude-plugins-official`。
- 随后 `claude plugin details mattpocock-skills` 报告版本 1.2.0，并加载正式技能。
- 条目的 `source` 为 `{"source": "url", "url": "https://github.com/mattpocock/skills.git", "sha": …}`：**sha 被固定**，因此发布到达已安装用户的时间取决于该固定值何时移动，而非打 tag 的瞬间。撰写时固定值落后 `main` 两个提交，所以列出的是 22 项技能，而非 `plugin.json` 中的 24 项。
- **未**测试会话内的 `/plugin install mattpocock-skills`：无头会话（`claude -p`）不可用 `/plugin`。它与 CLI 使用同一解析器，文档中的示例形式是 `/plugin install <name>@claude-plugins-official`。
