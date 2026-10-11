---
name: domain-modeling
description: 构建并精炼项目的领域模型。在讨论代码库术语、编写或编辑 GLOSSARY.md，或记录、编辑 ADR 时使用。
---

<a id="domain-modeling"></a>

# 领域建模

设计时主动构建并精炼项目的领域模型。这是一项*主动*实践：质疑术语、构造边界情景，并在术语和决策明确的那一刻将它们写下来。（仅为获取词汇而*阅读* `GLOSSARY.md` 不属于本技能：那是任何技能都能执行的一条简单习惯。本技能用于改变模型，而不是仅仅使用模型。）

<a id="file-structure"></a>

## 文件结构

大多数仓库只有一个上下文：

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

根目录存在 `GLOSSARY-MAP.md` 时，仓库包含多个上下文。地图指向各上下文的位置：

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← 系统级决策
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← 特定上下文的决策
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

按需创建文件：有内容要写时才创建。如果不存在 `GLOSSARY.md`，就在第一个术语明确时创建。如果不存在 `docs/adr/`，就在需要第一份 ADR 时创建。

<a id="during-the-session"></a>

## 会话期间

<a id="challenge-against-the-glossary"></a>

### 对照术语表提出质疑

当用户使用的术语与 `GLOSSARY.md` 中现有语言冲突时，立即指出。“你的术语表把 'cancellation' 定义为 X，但你似乎在说 Y。到底是哪一个？”

<a id="sharpen-fuzzy-language"></a>

### 精炼模糊语言

当用户使用含糊或一词多义的术语时，提出精确的规范用词。“你说的是 'account'：指的是 Customer，还是 User？这是两种不同的东西。”

<a id="discuss-concrete-scenarios"></a>

### 讨论具体情景

讨论领域关系时，用具体情景进行压力测试。构造能探查边界情况的情景，迫使用户精确定义概念之间的边界。

<a id="cross-reference-with-code"></a>

### 与代码交叉核对

用户陈述某件事如何工作时，检查代码是否一致。发现矛盾就指出：“代码会取消整个 Orders，但你刚才说可以部分取消。哪个是对的？”

<a id="update-glossarymd-inline"></a>

### 随时更新 GLOSSARY.md

术语一旦明确，就立即更新 `GLOSSARY.md`。不要积攒起来批量处理：确定一项就记录一项。使用 [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) 中的格式。

`GLOSSARY.md` 应当完全不含实现细节。不要把 `GLOSSARY.md` 当成规格说明、草稿纸或存放实现决策的地方。它只是术语表，仅此而已。

<a id="offer-adrs-sparingly"></a>

### 谨慎提议 ADR

只有同时满足以下三个条件，才提议创建 ADR：

1. **难以撤销**：以后改变主意的成本确实不小
2. **缺少背景时令人困惑**：未来读者会问“他们为什么这样做？”
3. **来自真实的取舍**：确实存在其他方案，而你基于具体理由选择了其中一个

缺少任何一个条件，就跳过 ADR。使用 [ADR-FORMAT.md](./ADR-FORMAT.md) 中的格式。
