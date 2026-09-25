<a id="out-of-scope-knowledge-base"></a>

# 范围之外知识库

仓库中的 `.out-of-scope/` 目录持久记录被拒绝的功能请求，有两个用途：

1. **组织记忆**：记录功能为何被拒绝，使理由不会随 issue 关闭而丢失
2. **去重**：新 issue 与既往拒绝记录匹配时，技能可以呈现先前决策，而不必重新争论

<a id="directory-structure"></a>

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个**概念**一个文件，而非每个 issue 一个文件。请求同一件事的多个 issue 归入同一文件。

<a id="file-format"></a>

## 文件格式

文件应采用轻松、易读的风格，更像简短设计文档，而非数据库条目。使用段落、代码示例和实例，把理由讲清楚，让初次接触的人也能受益。

```markdown
# 深色模式

本项目不支持深色模式或面向用户的主题功能。

## Why this is out of scope

渲染管线假定只有 `ThemeConfig` 中定义的一套调色板。
支持多个主题需要：

- 包裹整个组件树的主题上下文提供器
- 每个组件都能感知主题并解析样式
- 用于保存用户主题偏好的持久层

这是一项重大架构变化，与项目聚焦内容创作的方向不符。
主题应由嵌入或再分发输出的下游使用者负责。

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42: "添加深色模式支持"
- #87: "用于无障碍访问的夜间主题"
- #134: "深色主题选项"
```

### 文件命名

用简短、有描述性的 kebab-case 名称表示概念：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。名称应足够直观，让浏览目录的人无需打开文件就能知道拒绝了什么。

### 编写理由

理由应当有实质内容：不能只说“我们不想要”，而要解释为什么。好的理由会引用：

- 项目范围或理念（“本项目专注于 X；主题是下游的职责”）
- 技术限制（“支持它需要 Y，而 Y 与我们的 Z 架构冲突”）
- 战略决策（“我们选择 A 而不是 B，因为……”）

理由应当持久有效。避免引用临时情况（“我们现在太忙”）；那不是真正的拒绝，而是推迟。

## 何时检查 `.out-of-scope/`

分流期间（步骤 1：收集上下文），读取 `.out-of-scope/` 中的所有文件。评估新 issue 时：

- 检查请求是否匹配已有的范围外概念
- 按概念相似性匹配，不按关键词：“夜间主题”匹配 `dark-mode.md`
- 如果匹配，告知维护者：“这与 `.out-of-scope/dark-mode.md` 类似。我们此前因为 [原因] 拒绝过。你现在仍持相同看法吗？”

维护者可以：

- **确认**：把新 issue 加入现有文件的 "Prior requests" 列表，然后关闭
- **重新考虑**：删除或更新范围外文件，issue 进入正常分流
- **不同意匹配**：两个 issue 有关联但不同，继续正常分流

## 何时写入 `.out-of-scope/`

仅当 **enhancement**（不是 bug）因 `wontfix` 而*被拒绝*时。enhancement PR 与 issue 完全相同：被拒绝的 PR 记录在这里，防止同一请求换成新代码再次出现。

如果某项内容因**已经实现**而以 `wontfix` 关闭，**不要**写入这里。那是已构建的功能，不是被拒绝的功能；记录它会让去重检查产生错误的拒绝判定。此时应在关闭评论中指出已有功能的位置。

流程：

1. 维护者决定某功能请求超出范围
2. 检查是否已有匹配的 `.out-of-scope/` 文件
3. 如果有：把新 issue 追加到 "Prior requests" 列表
4. 如果没有：新建文件，包含概念名、决策、理由和首个既往请求
5. 在 issue 上发表评论，解释决策并提及 `.out-of-scope/` 文件
6. 以 `wontfix` 标签关闭 issue

## 更新或删除范围外文件

维护者对先前拒绝的概念改变主意时：

- 删除 `.out-of-scope/` 文件
- 技能无需重新开启旧 issue；它们是历史记录
- 触发重新考虑的新 issue 进入正常分流
