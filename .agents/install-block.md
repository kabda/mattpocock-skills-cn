<a id="the-canonical-install-block"></a>

# 规范安装片段

一种安装叙述，一套措辞。`README.md`、`.changeset/*` 和 `docs/` 下每一页都必须采用**这里的内容**，不能另写一套。先在这里修改，再传播到其他位置。

<a id="managed-installs-first"></a>

## 优先使用受管理安装

优先展示自动更新的安装方式。只有 agent 没有这种安装方式时，才回退到 skills.sh，并标注“手动更新”。只有无需用户执行命令就能更新的路线，才称为受管理安装。需要一次性启用更新时，把说明放在安装命令旁。绝不承诺“即时”。

Claude Code 从官方 marketplace `claude-plugins-official` 安装。其他受管理路线都从本仓库的 `.claude-plugin/marketplace.json` 和 `plugin.json` 安装。这些路线仅在 `plugin.json` 的 `version` 变化后重新安装。Release 工作流执行 `npm run version`，从 `package.json` 复制该字段，因此 “chore: version skills” PR 合并后，用户便会收到发布版本。

| Agent | 路线 | 自动更新？ |
| ------------- | -------------------------------- | ---------------------------------------------------------------- |
| Claude Code | `@claude-plugins-official` | 是，默认启用 |
| Codex | `@mattpocock` marketplace | 是，默认在启动时更新 |
| Copilot CLI | `@mattpocock` marketplace | 是，需一次性设置 `autoUpdate: true` |
| VS Code | Chat: Install Plugin From Source | 是，默认每天更新 |
| Gemini CLI | `gemini skills install`（复制文件） | 否。Gemini extension 需要扁平的 `skills/<name>/` 布局 |
| 其他所有 agent | skills.sh | 否。运行 `npx skills update`，并重新运行 `add` 获取新技能 |

来源（2026-10-08）：Codex `core-plugins/src/manager.rs`；Copilot [cli-config-dir-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)；VS Code `pluginAutoUpdate.ts`；Gemini `skillLoader.ts`。

尚未有人用 Auggie、Droid、Qwen 或 Goose 验证本仓库，因此在有人验证前，它们继续使用 skills.sh。

## Claude Code

<canonical-block name="claude-code">

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

默认自动更新。

</canonical-block>

## Codex

<canonical-block name="codex">

```bash
codex plugin marketplace add mattpocock/skills
codex plugin add mattpocock-skills@mattpocock
```

启动时自动更新。

</canonical-block>

<a id="github-copilot-cli-and-vs-code"></a>

## GitHub Copilot（CLI 和 VS Code）

使用 marketplace，不用 `copilot plugin install mattpocock/skills`。Copilot 已弃用直接从仓库安装的方式，而且该方式无法自动更新。`extraKnownMarketplaces` 条目遵循文档中的 schema，但尚未有人实际运行验证。

<canonical-block name="copilot">

```bash
copilot plugin marketplace add mattpocock/skills
copilot plugin install mattpocock-skills@mattpocock
```

然后在 `~/.copilot/settings.json` 中添加以下内容，只需一次：

```json
{
  "extraKnownMarketplaces": {
    "mattpocock": { "source": { "source": "github", "repo": "mattpocock/skills" }, "autoUpdate": true }
  }
}
```

在 VS Code 中运行 **Chat: Install Plugin From Source**，输入 `https://github.com/mattpocock/skills`。它每天自动更新。

</canonical-block>

## Gemini CLI

Gemini 不读取 `.claude-plugin`，且 `--path` 每次只接受一个分类。为每个正式分类各安装一次，恰好得到正式收录集合（27 个技能，2026-10-07 验证）。

<canonical-block name="gemini">

```bash
gemini skills install https://github.com/mattpocock/skills.git --path skills/engineering
gemini skills install https://github.com/mattpocock/skills.git --path skills/productivity
```

重新运行这两条命令即可更新。

</canonical-block>

<a id="every-other-agent-or-editable-files-skillssh"></a>

## 其他所有 agent，或可编辑文件（skills.sh）

`-a` 预选 agent。注释中每个 agent 都在 2026-10-07 运行过。优先使用 skills.sh，而非 agent 自带的仓库安装器，例如 `amp skill add` 或 `pi install git:…`，因为后两者也会引入 `misc/` 和 `in-progress/`。`npx skills update` 会跳过上次 `add` 后上游新增的技能，所以安装片段要求用户重新运行 `add`。

<canonical-block name="other-agents">

```bash
npx skills@latest add mattpocock/skills -a <agent>  # cursor, opencode, devin, windsurf, amp, pi; omit -a to choose
```

安装器询问要安装哪些技能时，请包含 `setup-matt-pocock-skills`。更新时运行 `npx skills@latest update`，并重新运行 `add` 获取新技能。

</canonical-block>

单独提到一项技能时，使用单技能安装形式。`docs/` 页面不用这个片段，因为 ai-hero 在页面正文上方渲染安装组件。参见 [writing-docs.md](./writing-docs.md)。

<canonical-block name="skills-sh-one-skill">

```bash
npx skills@latest add mattpocock/skills --skill=<name>
```

```bash
npx skills@latest update <name>
```

</canonical-block>

所有地方统一采用 `skills@latest` 这一拼写。

<a id="the-two-routes-are-exclusive"></a>

## 两条路线互斥

插件是你订阅的受管理、只读的包。skills.sh 写入你拥有并编辑的文件。两者都安装会让每项技能出现两份：始终说“选一种”。
