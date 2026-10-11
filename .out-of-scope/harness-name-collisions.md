<a id="renaming-skills-to-dodge-harness-built-in-commands"></a>

# 为避开 harness 内置命令而重命名技能

不会因为 harness 发布了同名内置命令或技能，就修改技能名称（例如 `/prototype`、`/research`、`/code-review`）。为避开冲突而重命名技能或添加别名的请求不在范围内。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

Harness 不断增加内置功能，且各自选择名称。每次碰到现有名称都改名，就得在 Claude Code、Copilot、Devin 等平台之间追逐不断变化的目标，每次也会打破所有用户的习惯和技能间的交叉引用。

同名项如何解析，是 harness 的行为，而非技能的行为。无论如何解析，技能文本本身都正确。

解决方式是使用命名空间调用。Claude Code 插件在插件名下暴露每项技能，因此始终可以明确调用本仓库的版本：

```
/mattpocock-skills:research
/mattpocock-skills:code-review
```

如果通过 skills.sh 安装，文件归你所有：修改副本中的目录名和 `name:` 字段即可。

如果 harness 完全没有调用命名空间技能或重命名技能的方式，请向 harness 反馈。

<a id="prior-requests"></a>

## 既往请求

- #423：“/code-review 遮蔽 Claude Code 自带的审查技能”
- #483：“/code-review 与 Claude Code 内置名称冲突”
- #857：“重命名 research 技能，避免与 Copilot 内置 /research 命令冲突”
- #1019：“简写 `/prototype` 与新加入但隐藏的 Claude Code 内置技能 `/prototype` 冲突”
- #1037：“技能名称与 Devin CLI 内置命令重叠”
