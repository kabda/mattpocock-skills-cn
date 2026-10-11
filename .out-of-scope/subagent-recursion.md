<a id="guards-against-sub-agents-recursing-into-skills"></a>

# 防止子 agent 递归进入技能的约束

技能不添加防止子 agent 递归调用技能或继续启动嵌套 agent 的约束（例如 `/code-review` 子 agent 再调用 `/code-review`，或 `/research` agent 启动另一个 agent）。增加叶子 agent 指令、深度限制或“不要调用此技能”条款的请求不在范围内。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

阻止子 agent 无限循环应由 harness 负责。Harness 决定子 agent 能访问哪些工具和技能、允许嵌套多深，因此在该层设置限制能同时约束所有技能。单个技能正文中的约束只覆盖自己，每次运行都消耗 token，而且仍依赖模型选择遵守。

如果子 agent 递归或无限扩散，请向 harness 反馈。

<a id="prior-requests"></a>

## 既往请求

- #530：“research 技能：启动的后台 agent 能递归再启动 agent，嵌套不受控制”
- #573：“code-review 子 agent 递归调用 /code-review 并扩散”（PR #1186，“code-review：将 Standards 和 Spec 子 agent 设为叶子审查者”，已关闭）
