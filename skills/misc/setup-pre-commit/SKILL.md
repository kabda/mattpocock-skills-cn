---
name: setup-pre-commit
description: 在当前仓库设置 Husky pre-commit hooks，包含 lint-staged（Prettier）、类型检查和测试。用户想添加 pre-commit hooks、设置 Husky、配置 lint-staged，或添加提交时格式化/类型检查/测试时使用。
---

<a id="setup-pre-commit-hooks"></a>

# 设置 Pre-Commit Hooks

<a id="what-this-sets-up"></a>

## 将配置什么

- **Husky** pre-commit hook
- **lint-staged** 对所有暂存文件运行 Prettier
- **Prettier** 配置（如尚不存在）
- pre-commit hook 中的 **typecheck** 和 **test** 脚本

<a id="steps"></a>

## 步骤

<a id="1-detect-package-manager"></a>

### 1. 检测包管理器

检查 `package-lock.json`（npm）、`pnpm-lock.yaml`（pnpm）、`yarn.lock`（yarn）、`bun.lockb`（bun）。使用存在的那个。无法确定时默认 npm。

<a id="2-install-dependencies"></a>

### 2. 安装依赖

作为 devDependencies 安装：

```
husky lint-staged prettier
```

<a id="3-initialize-husky"></a>

### 3. 初始化 Husky

```bash
npx husky init
```

这会创建 `.husky/` 目录，并向 package.json 添加 `prepare: "husky"`。

<a id="4-create-huskypre-commit"></a>

### 4. 创建 `.husky/pre-commit`

写入以下文件（Husky v9+ 无需 shebang）：

```
npx lint-staged
npm run typecheck
npm run test
```

**适配**：将 `npm` 换为检测到的包管理器。如果仓库 package.json 没有 `typecheck` 或 `test` 脚本，省略对应行并告知用户。

<a id="5-create-lintstagedrc"></a>

### 5. 创建 `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

<a id="6-create-prettierrc-if-missing"></a>

### 6. 创建 `.prettierrc`（如尚不存在）

仅在没有 Prettier 配置时创建。使用以下默认值：

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

<a id="7-verify"></a>

### 7. 验证

- [ ] `.husky/pre-commit` 存在且可执行
- [ ] `.lintstagedrc` 存在
- [ ] package.json 中的 `prepare` 脚本为 `"husky"`
- [ ] 存在 `prettier` 配置
- [ ] 运行 `npx lint-staged` 验证可用

<a id="8-commit"></a>

### 8. 提交

暂存所有修改或新建的文件，使用以下 message 提交：`Add pre-commit hooks (husky + lint-staged + prettier)`

这会运行新的 pre-commit hooks，是验证一切正常的良好冒烟测试。

<a id="notes"></a>

## 说明

- Husky v9+ 的 hook 文件不需要 shebang
- `prettier --ignore-unknown` 跳过 Prettier 无法解析的文件（图片等）
- pre-commit 先运行 lint-staged（快速，仅暂存内容），再运行完整类型检查和测试
