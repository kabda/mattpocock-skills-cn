<a id="writing-agent-briefs"></a>

# 编写 agent 简报

agent 简报是 issue 或 PR 转到 `ready-for-agent` 时发布在 GitHub 上的结构化评论。它是 AFK agent 开展工作的权威规格说明。原始正文和讨论提供上下文；agent 简报才是契约。

简报说明**agent 应当做什么**，适用于两种对象：对于 issue，是从零构建变更；对于 PR，是*对现有 diff* 还要做什么：完成它、补齐缺口、处理审查意见。两者原则相同；下方 PR 示例展示了区别。

<a id="principles"></a>

## 原则

<a id="durability-over-precision"></a>

### 持久有效比位置精确更重要

issue 可能在 `ready-for-agent` 停留数天或数周，期间代码库会变化。简报应当在文件被重命名、移动或重构后仍然有用。

- **应当**描述接口、类型和行为契约
- **应当**列出 agent 应查找或修改的具体类型、函数签名或配置形态
- **不要**引用文件路径：它们会过时
- **不要**引用行号
- **不要**假定当前实现结构会保持不变

<a id="behavioral-not-procedural"></a>

### 描述行为，而非操作步骤

描述系统应当做**什么**，而非**如何**实现。agent 会重新探索代码库，自行作出实现决策。

- **好：**“`SkillConfig` 类型应接受类型为 `CronExpression` 的可选 `schedule` 字段”
- **差：**“打开 src/types/skill.ts，在第 42 行加一个 schedule 字段”
- **好：**“用户不带参数运行 `/triage` 时，应看到需要关注的 issue 摘要”
- **差：**“在主处理函数中添加一个 switch 语句”

<a id="complete-acceptance-criteria"></a>

### 完整的验收标准

agent 需要知道何时完成。每份 agent 简报都必须有具体、可测试的验收标准，每一条都应当能独立验证。

- **好：**“运行 `gh issue list --label needs-triage`，返回已经过初步分类的 issue”
- **差：**“分流应当正常工作”

<a id="explicit-scope-boundaries"></a>

### 明确范围边界

说明哪些内容不在范围内，防止 agent 过度雕琢，或对相邻功能自行作出假设。

<a id="template"></a>

## 模板

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** 用一句话描述需要完成的事情

**Current behavior:**
描述当前发生的情况。对于 bug，这是出错的行为。
对于 enhancement，这是新功能所基于的现状。

**Desired behavior:**
描述 agent 完成工作后应当发生的情况。
具体说明边界情况和错误条件。

**Key interfaces:**
- `TypeName`：需要改变什么，以及为什么
- `functionName()` 返回类型：当前返回什么，应当返回什么
- 配置形态：需要哪些新的配置选项

**Acceptance criteria:**
- [ ] 具体、可测试的标准 1
- [ ] 具体、可测试的标准 2
- [ ] 具体、可测试的标准 3

**Out of scope:**
- 本 issue 不应当修改或处理的内容
- 看似相关但实际独立的相邻功能
```

<a id="examples"></a>

## 示例

<a id="good-agent-brief-bug"></a>

### 好的 agent 简报（bug）

```markdown
## Agent Brief

**Category:** bug
**Summary:** 技能描述在单词中间被截断，导致输出残缺

**Current behavior:**
技能描述超过 1024 个字符时，会恰好在第 1024 个字符处截断，
不考虑单词边界。因此，描述会在单词中途结束
（例如 "Use when the user wants to confi"）。

**Desired behavior:**
截断应发生在 1024 个字符之前的最后一个单词边界，
并附加 "..." 表示发生了截断。

**Key interfaces:**
- `SkillMetadata` 类型的 `description` 字段：无需改变类型，
  但填充它的验证/处理逻辑需要遵守单词边界
- 读取 SKILL.md frontmatter 并提取描述的所有函数

**Acceptance criteria:**
- [ ] 不足 1024 个字符的描述保持不变
- [ ] 超过 1024 个字符的描述，在 1024 个字符前的最后一个单词边界截断
- [ ] 截断后的描述以 "..." 结尾
- [ ] 包含 "..." 在内的总长度不超过 1024 个字符

**Out of scope:**
- 修改 1024 字符限制本身
- 支持多行描述
```

<a id="good-agent-brief-enhancement"></a>

### 好的 agent 简报（enhancement）

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** 增加 `.out-of-scope/` 目录支持，用于跟踪被拒绝的功能请求

**Current behavior:**
功能请求被拒绝时，issue 会被打上 `wontfix` 标签、留下评论并关闭。
决策和理由没有持久记录。
未来遇到类似请求，维护者必须回忆或搜索之前的讨论。

**Desired behavior:**
被拒绝的功能请求应记录在 `.out-of-scope/<concept>.md` 文件中，
包含决策、理由，以及所有曾提出该功能的 issue 链接。
分流新 issue 时，应检查这些文件是否存在匹配项。

**Key interfaces:**
- `.out-of-scope/` 中的 Markdown 文件格式：每个文件应有
  `# Concept Name` 标题、`**Decision:**` 行、`**Reason:**` 行，
  以及包含 issue 链接的 `**Prior requests:**` 列表
- 分流流程应及早读取所有 `.out-of-scope/*.md` 文件，
  按概念相似性与新收到的 issue 匹配

**Acceptance criteria:**
- [ ] 以 wontfix 关闭功能时，在 `.out-of-scope/` 中创建/更新文件
- [ ] 文件包含决策、理由和已关闭 issue 的链接
- [ ] 如果已有匹配的 `.out-of-scope/` 文件，将新 issue
      追加到其 "Prior requests" 列表，而不是创建重复文件
- [ ] 分流时检查已有 `.out-of-scope/` 文件，
      新 issue 匹配既往拒绝记录时将其呈现出来

**Out of scope:**
- 自动匹配（由人确认匹配结果）
- 重新开启此前被拒绝的功能
- Bug 报告（只有 enhancement 的拒绝记录进入 `.out-of-scope/`）
```

<a id="good-agent-brief-pr"></a>

### 好的 agent 简报（PR）

对于 PR，"Current behavior" 描述 diff 的状态；简报要求 agent 完成或修复它，而非从零构建。

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** 完成贡献者为 `triage list` 添加的 `--json` 输出标志

**Current behavior:**
该 PR 增加了 `--json` 标志，将 issue 列表序列化为 JSON。
正常路径可用，diff 符合项目命令结构。仍有两个缺口：
错误仍以供人阅读的文本输出（不是 JSON），新标志也没有测试覆盖。

**Desired behavior:**
使用 `--json` 时，所有输出（包括错误）都在 stdout 上以格式正确的 JSON 呈现，
命令退出码保持不变。不带该标志时，原有可读输出不变。

**Key interfaces:**
- 使用 `--json` 时，命令错误路径应输出 `{ "error": string }`，
  取代纯文本错误
- 复用 PR 已添加的序列化器，不要再引入第二个

**Acceptance criteria:**
- [ ] `triage list --json` 在成功和错误情况下都输出有效 JSON
- [ ] 退出码与非 JSON 命令一致
- [ ] 测试覆盖 `--json` 的成功输出和一个错误场景
- [ ] 默认（非 JSON）输出逐字节保持不变

**Out of scope:**
- 为任何其他命令添加 `--json`
- 修改 PR 已定义的成功响应 JSON 形态
```

<a id="bad-agent-brief"></a>

### 差的 agent 简报

```markdown
## Agent Brief

**Summary:** 修复分流 bug

**What to do:**
分流那块坏了。看看主文件，修一下。
第 150 行附近的函数有问题。

**Files to change:**
- src/triage/handler.ts (line 150)
- src/types.ts (line 42)
```

它的问题在于：
- 没有类别
- 描述含糊（“分流那块坏了”）
- 引用了会过时的文件路径和行号
- 没有验收标准
- 没有范围边界
- 没有描述当前行为与期望行为
