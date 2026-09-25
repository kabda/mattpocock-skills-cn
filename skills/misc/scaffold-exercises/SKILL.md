---
name: scaffold-exercises
description: 创建包含章节、题目、解答和讲解、且能通过 lint 的练习目录结构。用户想搭建练习骨架、创建练习占位内容或设置新课程章节时使用。
---

<a id="scaffold-exercises"></a>

# 搭建练习骨架

创建能通过 `pnpm ai-hero-cli internal lint` 的练习目录结构，再用 `git commit` 提交。

<a id="directory-naming"></a>

## 目录命名

- **章节**：`exercises/` 内的 `XX-section-name/`（例如 `01-retrieval-skill-building`）
- **练习**：章节内的 `XX.YY-exercise-name/`（例如 `01.03-retrieval-with-bm25`）
- 章节编号 = `XX`，练习编号 = `XX.YY`
- 名称使用 dash-case（小写、连字符）

<a id="exercise-variants"></a>

## 练习变体

每个练习至少需要以下子目录之一：

- `problem/`：带 TODO 的学生工作空间
- `solution/`：参考实现
- `explainer/`：概念材料，没有 TODO

搭骨架时，除非计划另有规定，默认使用 `explainer/`。

<a id="required-files"></a>

## 必需文件

每个子目录（`problem/`、`solution/`、`explainer/`）都需要一个 `readme.md`，要求：

- **非空**（必须有实际内容，即使只有一行标题也可以）
- 没有断链

搭骨架时，创建包含标题和说明的最简 readme：

```md
# 练习标题

在此填写说明
```

子目录包含代码时，还需要 `main.ts`（大于 1 行）。但对于骨架，只有 readme 的练习也可以。

<a id="workflow"></a>

## 工作流

1. **解析计划**：提取章节名、练习名和变体类型
2. **创建目录**：为每条路径运行 `mkdir -p`
3. **创建 readme 骨架**：每个变体目录一个带标题的 `readme.md`
4. **运行 lint**：用 `pnpm ai-hero-cli internal lint` 验证
5. **修复错误**：迭代直到 lint 通过

<a id="lint-rules-summary"></a>

## Lint 规则概要

linter（`pnpm ai-hero-cli internal lint`）检查：

- 每个练习都有子目录（`problem/`、`solution/`、`explainer/`）
- 至少存在 `problem/`、`explainer/` 或 `explainer.1/` 之一
- 主子目录中存在非空的 `readme.md`
- 没有 `.gitkeep` 文件
- 没有 `speaker-notes.md` 文件
- readme 中没有断链
- readme 中没有 `pnpm run exercise` 命令
- 除非仅含 readme，否则每个子目录都需要 `main.ts`

<a id="movingrenaming-exercises"></a>

## 移动或重命名练习

重新编号或移动练习时：

1. 用 `git mv`（不用 `mv`）重命名目录，以保留 Git 历史
2. 更新数字前缀，保持顺序
3. 移动后重新运行 lint

示例：

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

<a id="example-stubbing-from-a-plan"></a>

## 示例：根据计划搭骨架

给定如下计划：

```
第 05 节：记忆技能训练
- 05.01 记忆入门
- 05.02 短期记忆（explainer + problem + solution）
- 05.03 长期记忆
```

创建：

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

然后创建 readme 骨架：

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# 记忆入门"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# 长期记忆"
```
