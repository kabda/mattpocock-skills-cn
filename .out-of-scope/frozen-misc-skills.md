<a id="changes-to-misc-skills"></a>

# 对 `misc/` 技能的修改

`skills/misc/` 下的技能（`git-guardrails-claude-code`、`migrate-to-shoehorn`、`scaffold-exercises`、`setup-pre-commit` 及之后放入的其他技能）已冻结。针对它们的 bug 报告、功能请求和 PR 都会关闭。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

`misc/` 保存我仍想保留但很少使用的技能。它们未正式收录：不随 Claude Code 插件发布，没有文档页，我也不日常使用，所以无法判断修复是否正确，或发现修复破坏了其他行为。按正式技能的标准维护它们，成本相同，使用收益却小得多。

它们仍未经维护地保留在仓库里，因为对某些人来说，当前版本仍能工作。如果某项不适合你，用 skills.sh 安装并修复自己的副本，文件归你编辑。

如果以后某项 `misc/` 技能重新晋升到 `engineering/` 或 `productivity/`，从那时起就重新纳入范围。

<a id="prior-requests"></a>

## 既往请求

- #14：“setup-pre-commit/SKILL.md 中可能有拼写错误”
- #301：“任意 Git 全局选项都能绕过 `block-dangerous-git.sh`（例如 `git -C <dir> push`）”
- #465：“git-guardrails-claude-code 文档未说明相对于 Claude Code 内置拒绝规则的优势”
- #898：“git-guardrails-claude-code：没有 jq 时 hook 放行，也遗漏了常见 Git 写法”
