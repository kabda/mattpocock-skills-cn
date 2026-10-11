<a id="what-it-does"></a>

## 它能做什么

`retro` 回顾编码[会话](https://www.aihero.dev/ai-coding-dictionary/session)，建议改进 agent **[环境](https://www.aihero.dev/ai-coding-dictionary/environment)**，让下一次运行更顺利。它读取会话自己的记录（默认当前会话，也可指定会话日志中的其他会话），找出 agent 遇到困难的时刻，按严重程度列出修复候选。

它修改环境，而非代码。agent 交付的 bug、花二十次[工具调用](https://www.aihero.dev/ai-coding-dictionary/tool-call)才找到的文件、审查者遗漏的规则，`retro` 都不直接修复。它问仓库里的什么条件让问题发生，并建议下次可预防的检查、指针或标准。它只提出建议，选中候选前不作修改。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/retro` 调用，agent 不会自行使用。

会话比应有的更艰难时，在结束前使用。例如 agent 查找过久、犯了工具本可发现的错误，或无法访问所需信息。顺利会话没多少可学，发现来自困难会话。若想评价产出的代码，改用 [code-review](https://aihero.dev/skills-code-review)。

<a id="where-the-findings-land"></a>

## 发现落在哪里

每个候选属于一种类别，类别决定修复位置：

| 会话中出了什么问题 | 修复方式 |
| --- | --- |
| agent 查找文件或事实耗时过长 | 从它已读取的文件添加**导航指针** |
| 犯了工具本可发现的错误 | **[自动检查](https://www.aihero.dev/ai-coding-dictionary/automated-check)**：lint 规则、类型、测试、pre-commit hook、CI 任务 |
| 审查者漏掉需要判断的错误 | 给审查 agent 的 `CODING_STANDARDS.md` 规则 |
| `AGENTS.md` 或 `CLAUDE.md` 过大 | 将引导内容移到标准或检查中 |
| 工具调用的成本相对返回内容过高 | 精简或替换工具 |
| 引导文件中充满不改变行为的句子 | 删除 **no-op** |
| agent 无法访问所需信息 | 扩大访问：将开发服务器日志 tee 到文件，提供服务只读访问 |

引导观念是标准属于**审查者**，而非实现者。实现 agent 要探索、写代码、调试，承受最大上下文压力；审查 agent 只拿到 diff。因此新规则应放到有空间应用它的审查阶段，绝不放进无论相关与否都会加载到每个会话[上下文窗口](https://www.aihero.dev/ai-coding-dictionary/context-window)的 [AGENTS.md](https://www.aihero.dev/ai-coding-dictionary/agents-md)。

写规则前，`retro` 先分类违规。**机械**违规（禁用 API、import 形式、文件位置规则）用确定性检查，因为检查能失败，标准文件里的句子不能。只有 linter 无法强制执行的真正判断才写成文字。仓库完全没有约束（没有 pre-commit hook，也没有运行 lint、typecheck 和测试的 CI 任务）时，`retro` 会单独报告这一发现。

<a id="common-questions"></a>

## 常见问题

**它自行写 lint 规则，还是等我同意？能让它每个会话后运行吗？**

它会等待。`retro` 只提建议，选中候选前不手动编辑、不自动安装 hook。这是刻意设计，一位用户正是因为“自动 hook 阻挡了正确修改”而要求这样。决定什么值得成为永久检查需要判断，所以技能保持[人在循环中](https://www.aihero.dev/ai-coding-dictionary/human-in-the-loop)，由用户调用。有些用户每次实现后都运行，但顺利会话没多少可学，每次都运行多半生成不需要的规则。没有 dry-run 模式。建议的检查也是代码，在让它阻挡合并前先在仓库尝试。

**Lint 规则不会一直堆积吗？它会建议删除吗？**

部分会，这也是最弱的一点。它能移除文字：引导文件中的 no-op，以及 `AGENTS.md` 或 `CLAUDE.md` 中应属于标准或检查的内容。文件过大时会建议删除，但它仅根据一个会话判断，因此应把建议当作删除检验的候选，而非结论。它不审查上个月建议的 lint 规则、hook 或 CI 任务，只看一个会话，无法判断规则是否误报过多或背后的 bug 是否已消失。检查仍需自行精简。不断对正确代码报错，就该考虑删除规则。

**它不会为了填满类别而编造泛泛建议吗？**

这是最有力的批评。一位用户发现：“任务完成后，AI 往往忘记会话中途的困难，为满足 retro 分类而编造泛泛建议。”每个候选必须来自会话自身记录，使建议针对具体会话。好处也伴随成本：它较少编造无关建议，却可能过分重视当前会话的主题。无法追溯到具体时刻的候选应丢弃，严重程度排序也只是初稿，因为安静但代价高的错误，可能排在吵闹但代价低的错误之后。

**会话很长，现在运行还是新开会话？**

默认审查当前会话，这是最佳情况，因为困难仍在上下文窗口中。若已超出 [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)，先[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)，在新会话运行 `/retro`，指向日志中的旧会话。

**Agent 总犯同样错误，应给 `CLAUDE.md` 加一句吗？**

通常不应，这是 `retro` 最反对的做法。`CLAUDE.md` 中每句都会进入每个会话，削弱文件其他内容的权重，并随代码变化过时。机械错误用会失败的检查修复；需要判断的错误，放入审查者读取的编码标准。`AGENTS.md` 和 `CLAUDE.md` 主要用于导航指针。同理，`retro` 不是[记忆系统](https://www.aihero.dev/ai-coding-dictionary/memory-system)：不存储发生过什么，而是改变环境，使错误不再发生。

**配置提到 `CODING_STANDARDS.md`，但我没有，该从哪里来？**

没有技能附带这个文件。会话首次发现适合审查者的判断规则时，`retro` 建议创建；接受后，[code-review](https://aihero.dev/skills-code-review) 会读取它。既有标准文档，例如 `CONTRIBUTING.md`，作用相同。

**它与 `improve-codebase-architecture` 有何不同？**

输入不同。[improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 只需代码，寻找结构改进；`retro` 需要会话历史，改进 agent 工作的环境，而非代码。两者都可使用，互不替代。

<a id="its-working-if"></a>

## 如何判断它有效

- 每个候选指向会话的具体时刻，而非泛泛最佳实践。
- 重复错误转成会失败的检查，`AGENTS.md` 随时间缩短，而非变长。
- 检查已存在但未接入时，发现是接入它，而非再造一个。
- 下一次相同类型任务的会话，更快找到所需内容。

<a id="where-it-fits"></a>

## 它在流程中的位置

`retro` 是主链条最后一步，回顾链条执行得怎样：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

在值得学习的构建后使用，可留在同一会话，或指向其日志。顺利构建后可以跳过。

- [code-review](https://aihero.dev/skills-code-review) 是 `retro` 最常调校的审查 agent。新编码标准放在其 Standards 维度会读取的位置。
- [writing-for-agents](https://aihero.dev/skills-writing-for-agents) 规定 `retro` 建议的引导文件和技能的写作风格；`retro` 开始前就加载它。

不确定情境需要哪项技能时，[ask-matt](https://aihero.dev/skills-ask-matt) 路由整套技能。
