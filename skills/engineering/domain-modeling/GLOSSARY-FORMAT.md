<a id="glossarymd-format"></a>

# GLOSSARY.md 格式

<a id="structure"></a>

## 结构

```md
# {上下文名称}

{用一两句话说明该上下文是什么，以及为什么存在。}

## Language

**Order**:
{用一两句话描述该术语}
_Avoid_: Purchase, transaction

**Invoice**:
交付后发送给客户的付款请求。
_Avoid_: Bill, payment request

**Customer**:
下订单的个人或组织。
_Avoid_: Client, buyer, account
```

<a id="rules"></a>

## 规则

- **要有明确判断。** 同一概念存在多个词时，选择最合适的一个，将其他词列在 `_Avoid_` 下。
- **定义要简练。** 最多一两句话。定义它是什么，而不是它做什么。
- **只包含这个项目上下文特有的术语。** 通用编程概念（超时、错误类型、工具模式）不应包含在内，即使项目大量使用它们。添加术语前先问：这是该上下文特有的概念，还是通用编程概念？只有前者应当收录。
- 出现自然分组时，**在子标题下对术语分组**。如果所有术语都属于一个紧密相关的领域，平铺列表即可。

<a id="single-vs-multi-context-repos"></a>

## 单上下文与多上下文仓库

**单上下文（大多数仓库）：** 仓库根目录有一个 `GLOSSARY.md`。

**多个上下文：** 仓库根目录的 `GLOSSARY-MAP.md` 列出各上下文、所在位置及彼此关系：

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): 接收并跟踪客户订单
- [Billing](./src/billing/GLOSSARY.md): 生成发票并处理付款
- [Fulfillment](./src/fulfillment/GLOSSARY.md): 管理仓库拣货和发运

## Relationships

- **Ordering → Fulfillment**: Ordering 发出 `OrderPlaced` 事件；Fulfillment 消费这些事件以开始拣货
- **Fulfillment → Billing**: Fulfillment 发出 `ShipmentDispatched` 事件；Billing 消费这些事件以生成发票
- **Ordering ↔ Billing**: 共享 `CustomerId` 和 `Money` 类型
```

技能会推断适用哪种结构：

- 存在 `GLOSSARY-MAP.md` 时，读取它以找到上下文
- 如果只有根目录的 `GLOSSARY.md`，则为单上下文
- 如果两者都不存在，在第一个术语明确时按需创建根目录的 `GLOSSARY.md`

存在多个上下文时，推断当前话题与哪个上下文有关。不清楚时就询问。
