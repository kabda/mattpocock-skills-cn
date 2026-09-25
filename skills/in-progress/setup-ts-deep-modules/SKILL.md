---
name: setup-ts-deep-modules
description: 把 dependency-cruiser 接入 TypeScript 仓库，让每个包成为深模块：实现隐藏在子目录中，只能经入口文件访问。由用户调用。
disable-model-invocation: true
---

<a id="setup-ts-deep-modules"></a>

# 设置 TS 深模块

让仓库中每个包成为**深模块**：小接口背后承载大量行为。包的公共表面是它的**入口点**（包根目录的文件），子目录中的所有内容都被隐藏。本技能安装 [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) 及使入口点成为唯一访问通道的规则，再证明规则确实会生效。

有关词汇（深模块、接口、seam、深度），调用 Skill 工具加载 "codebase-design"，并全程使用其语言。

<a id="the-shape-this-enforces"></a>

## 强制采用的结构

```
src/packages/
  <name>/
    index.ts        ← 入口点（公开）。外部应导入此文件。
    client.ts       ← 另一个入口点。包可以公开多个入口。
    lib/            ← 实现：对外隐藏，内部可以相互自由导入。
    tests/          ← 就近放置的测试和 fixture（是子目录，因此私有）。
```

公共表面是包的**根目录文件**，不是指定的单个 `index.ts`。按约定，实现放在 `lib/`，测试放在 `tests/`，使每个包都采用相同的双目录结构。但规则本身是通用的：*任何*子目录中的*任何*内容都私有，因此新增目录永远不需要扩展配置。

四条规则，全部为 `error`：

1. **入口点边界**：包外代码（应用代码或其他包）只能导入该包的入口点（根目录文件），绝不能导入子目录内容。
2. **包内自由**：包自己的文件可相互自由导入。
3. **测试经入口点访问**：`<pkg>/tests/` 下的文件可导入任意包的入口点及自己 `tests/` 中的 fixture，但绝不能导入任何包的子目录内部实现（包括自己的）。跨包集成测试可以，深层导入不行。
4. **无环**：不允许依赖环。

**使用入口点，而非 barrel。** 公共表面包括*每个*根目录文件，因此包可以公开多个小入口（`index.ts`、`client.ts`、`server.ts`），不必把一切汇入巨大的 `index.ts`。不鼓励用 barrel 文件重新导出整个子树；保持入口点小，把实现隐藏在子目录中。

分层（哪些包可以依赖哪些包）是*另一个*关注点，配置中仅保留注释形式的桩，供本仓库填写。

<a id="steps"></a>

## 步骤

<a id="1-detect-the-environment"></a>

### 1. 检测环境

- **包管理器**：`pnpm-lock.yaml` → pnpm，`yarn.lock` → yarn，`bun.lockb` → bun，否则 npm。后续每条命令都使用它（`pnpm`/`yarn`/`npm run`/`bunx`）。
- **包根目录**：有 `src/` 就用 `src/packages`，否则用 `packages`。仓库已有其他明显约定时，与用户确认选择。
- **现有配置**：检查 `.dependency-cruiser.*` 文件。如果存在，**不要**覆盖：把四条规则和选项合并进去，告知用户添加了什么。

**完成条件：**包管理器、包根目录和现有配置状态均已明确。

<a id="2-install-dependency-cruiser"></a>

### 2. 安装 dependency-cruiser

用检测到的包管理器，将 `dependency-cruiser` 安装为 devDependency。

**完成条件：**`dependency-cruiser` 已在 `devDependencies` 中。

<a id="3-write-the-config"></a>

### 3. 写配置

将 [`dependency-cruiser.config.cjs`](./dependency-cruiser.config.cjs) 复制到仓库根目录，命名为 `.dependency-cruiser.cjs`。把 `PACKAGES_ROOT` 设为步骤 1 检测到的根目录。规则基于路径深度，与扩展名无关，因此无需其他适配。

**完成条件：**`.dependency-cruiser.cjs` 存在，`PACKAGES_ROOT` 正确，且四条禁止规则均存在。

<a id="4-wire-it-into-the-checks"></a>

### 4. 接入检查

- 添加 `lint:boundaries` 脚本：`depcruise <packages-root>`（或 `depcruise src`）。
- 纳入仓库统一检查命令，即已经运行 typecheck 的命令（例如 `check` / `ci` / `validate` 脚本）。**不要**修改 `tsconfig` 或添加路径别名。
- 没有统一脚本时，添加 `lint:boundaries`，并告诉用户将它纳入 CI。

**完成条件：**`lint:boundaries` 存在，并作为与 typecheck 相同命令的一部分运行。

<a id="5-scaffold-the-example-package"></a>

### 5. 搭建示例包

创建一个已提交的 `<packages-root>/example/`，作为可复制模板：

- `index.ts` 是入口点。导出一个委派给内部文件的函数（使包明显是*深模块*，而非简单透传）。
- `lib/impl.ts`：位于**子目录**的内部文件，由 `index.ts` 导入，外部不可访问。
- `tests/example.test.ts` **只**导入 `../index`（入口点），并针对公共函数断言。

告诉用户，这是可以复制或删除的起步模板。

**完成条件：**示例包存在，通过根目录入口公开行为，并将 `impl` 隐藏在子目录。

<a id="6-prove-the-rules-bite"></a>

### 6. 证明规则会生效

这是整个技能的完成标准：面对违规却不失败的配置毫无价值。

1. 运行 `lint:boundaries`，对干净示例必须**通过**。
2. 临时在 `tests/example.test.ts` 添加深层导入（例如 `import { thing } from "../lib/impl"`）。再次运行 `lint:boundaries`，必须因 `tests-through-entrypoints` 而**失败**。
3. 撤回深层导入，再运行一次，必须**通过**。

**完成条件：**已观察到先通过、再因深层导入失败、再通过。如果步骤 2 不失败，说明规则接入不正确，结束前必须修复。

<a id="7-document-the-convention"></a>

### 7. 记录约定

**在包目录中**写 `README.md`（`<packages-root>/README.md`，与其约束的包相邻），涵盖：`src/packages/<name>/` 布局（入口点在根目录、`lib/` 放实现、`tests/` 放测试）、“只通过包的入口点（根目录文件）导入”，以及如何运行 `lint:boundaries`。明确**不鼓励 barrel 文件**：公开多个小入口，不要通过单个 index 重新导出整个子树。只保留可复制示例，加上四条规则各一段说明。

然后，从仓库 agent 指令文件添加一个**上下文指针**（有 `CLAUDE.md` 就用它，否则用 `AGENTS.md`；两者都没有就创建 `AGENTS.md`）。一行足够，例如 `包是深模块：添加或导入包前，请阅读 [src/packages/README.md](./src/packages/README.md)。`。这让 agent 能发现边界规则，而非撞上它。

**完成条件：**`<packages-root>/README.md` 存在且不鼓励 barrel，仓库 `CLAUDE.md`/`AGENTS.md` 链接到它。

<a id="notes"></a>

## 说明

- 配置中的 `$1` 反向引用（dependency-cruiser 分组匹配）让包能访问自己的内部实现，同时阻止外部访问。不要把它们展开成每包单独一组规则。
- 公开与私有由**深度**决定：包根目录文件是入口点；子目录中所有内容都私有。约定子目录为 `lib/`（实现）和 `tests/`，但规则不硬编码它们：任意子目录都私有，所以新建目录永远不需要修改配置。新增入口点只需新增根目录文件（不用 barrel）。
- 包是**扁平**的：根目录下只有一层直接子目录。包内部可以任意嵌套，但包不能包含另一个包。
- 使用 `.cjs`（不是 `.js`），让配置中的 `module.exports` 在 `"type": "module"` 仓库中也可用。
