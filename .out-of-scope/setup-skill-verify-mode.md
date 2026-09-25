<a id="verifycheck-mode-for-setup-matt-pocock-skills"></a>

# `setup-matt-pocock-skills` 的验证/检查模式

本项目不会为 `setup-matt-pocock-skills` 添加专门的验证/检查模式，也不会添加独立验证技能。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

用第二项技能（或 `--verify` 标志）检查 `docs/agents/*.md` 产物是否仍匹配初始模板 schema，会重复现有 setup 技能已经能通过对话处理的工作。

预期工作流是：**运行 `/setup-matt-pocock-skills`，告诉它验证当前设置。** 技能由提示词驱动，维护者可以把范围限定为一轮验证（“不要重写任何内容，只对照当前初始模板检查现有文件，报告偏差”），无需独立代码路径。添加标志或相邻技能，会把已经能通过自然语言入口表达的功能拆成多个界面。

将配置管理保留在一项技能中，也避免初始模板演变时，两项技能相互漂移的维护成本。

<a id="prior-requests"></a>

## 既往请求

- #106：功能请求：为 setup-matt-pocock-skills 添加验证/检查模式
