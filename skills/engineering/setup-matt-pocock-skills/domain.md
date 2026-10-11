<a id="domain-docs"></a>

# 领域文档

工程技能探索代码库时，应当如何使用本仓库的领域文档。

<a id="before-exploring-read-these"></a>

## 探索之前先阅读

- 仓库根目录的 **`GLOSSARY.md`**，或
- 根目录存在 **`GLOSSARY-MAP.md`** 时，它指向每个上下文的一份 `GLOSSARY.md`。读取与主题有关的每一份。
- **`docs/adr/`**：阅读涉及即将工作区域的 ADR。多上下文仓库还要检查 `src/<context>/docs/adr/` 中限定于该上下文的决策。

如果这些文件不存在，**静默继续**。不要报告缺失，也不要建议提前创建。`/domain-modeling` 技能（通过 `/grill-with-docs` 和 `/improve-codebase-architecture` 使用）会在术语或决策真正明确时按需创建。

<a id="file-structure"></a>

## 文件结构

单上下文仓库（大多数仓库）：

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `GLOSSARY-MAP.md`）：

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← 系统级决策
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← 特定上下文的决策
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

<a id="use-the-glossarys-vocabulary"></a>

## 使用术语表词汇

输出涉及领域概念命名时（issue 标题、重构提案、假设、测试名称），使用 `GLOSSARY.md` 定义的术语。不要偏移到术语表明确避免的同义词。

如果需要的概念尚未出现在术语表中，这是一个信号：要么你在发明项目不用的语言（重新考虑），要么确实存在缺口（记下来，交给 `/domain-modeling`）。

<a id="flag-adr-conflicts"></a>

## 标出 ADR 冲突

如果输出与现有 ADR 冲突，明确指出，不要静默覆盖：

> _与 ADR-0007（事件溯源订单）冲突，但值得重新讨论，因为……_
