---
name: migrate-to-shoehorn
description: 将测试文件中的 `as` 类型断言迁移到 @total-typescript/shoehorn。用户提及 shoehorn、想替换测试中的 `as`，或需要部分测试数据时使用。
---

<a id="migrate-to-shoehorn"></a>

# 迁移到 Shoehorn

<a id="why-shoehorn"></a>

## 为什么用 shoehorn？

`shoehorn` 允许在测试中传入部分数据，同时满足 TypeScript 类型检查。它用类型安全的替代方案取代 `as` 断言。

**仅用于测试代码。** 绝不在生产代码中使用 shoehorn。

测试中使用 `as` 的问题：

- 一直被教导不要用它
- 必须手动指定目标类型
- 故意提供错误数据时，需要双重 as（`as unknown as Type`）

<a id="install"></a>

## 安装

```bash
npm i @total-typescript/shoehorn
```

<a id="migration-patterns"></a>

## 迁移模式

<a id="large-objects-with-few-needed-properties"></a>

### 只需少数字段的大对象

之前：

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

之后：

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

之前：

```ts
getUser({ body: { id: "123" } } as Request);
```

之后：

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

之前：

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

之后：

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

<a id="when-to-use-each"></a>

## 各函数何时使用

| 函数 | 使用场景 |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | 传入仍能通过类型检查的部分数据 |
| `fromAny()` | 传入刻意错误的数据（保留自动补全） |
| `fromExact()` | 强制完整对象（之后可换为 fromPartial） |

<a id="workflow"></a>

## 工作流

1. **收集需求**，询问用户：
   - 哪些测试文件中的 `as` 断言造成了问题？
   - 是否在处理只有部分属性重要的大对象？
   - 是否需要为错误测试传入刻意错误的数据？

2. **安装并迁移**：
   - [ ] 安装：`npm i @total-typescript/shoehorn`
   - [ ] 查找含 `as` 断言的测试文件：`grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
   - [ ] 将 `as Type` 替换为 `fromPartial()`
   - [ ] 将 `as unknown as Type` 替换为 `fromAny()`
   - [ ] 添加从 `@total-typescript/shoehorn` 的导入
   - [ ] 运行类型检查进行验证
