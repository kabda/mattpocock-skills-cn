<a id="html-report-format"></a>

# HTML 报告格式

架构审查呈现为操作系统临时目录中的单个自包含 HTML 文件。Tailwind 和 Mermaid 均来自 CDN。Mermaid 可靠地处理图结构图示；手工 div 和内联 SVG 处理更偏编辑设计的可视化（体量图、剖面图）。混合使用两者：不要事事依赖 Mermaid，否则会显得千篇一律。

<a id="scaffold"></a>

## 骨架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{{repo name}} 的架构审查</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

<a id="header"></a>

## 页头

仓库名、日期和简洁图例：实线框 = 模块，虚线 = seam，红箭头 = 泄漏，粗深色框 = 深模块。不要引言段落。直接进入候选项。

<a id="candidate-card"></a>

## 候选项卡片

图示承担主要表达。文字稀少、直白，自然使用术语表中的词（来自 `/codebase-design` 技能）。

每个候选项对应一个 `<article>`：

- **标题**：简短，点明加深动作（例如“合并 Order 接入流水线”）。
- **徽章行**：推荐强度（`Strong` = 翡翠绿，`Worth exploring` = 琥珀色，`Speculative` = 石板灰），加上依赖类别标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **文件**：等宽列表，`font-mono text-sm`。
- **改前／改后图示**：核心部分。两列并排。参见下方模式。
- **问题**：一句话。哪里难受。
- **解决方案**：一句话。改变什么。
- **收益**：列表，每项不超过 6 词。例如“测试只触及一个接口”“定价逻辑不再泄漏”“删除 4 个浅封装”。
- **ADR 提示**（如适用）：琥珀色背景框中的一行文字。

不要写成段的解释。如果图示需要一个段落才能理解，就重画图示。

<a id="diagram-patterns"></a>

## 图示模式

选择适合候选项的模式。混合使用。不要让每张图都一样。多样性也是目的的一部分。

<a id="mermaid-graph-the-workhorse-for-dependencies--call-flow"></a>

### Mermaid 图（依赖／调用流程的主力）

当重点是“X 调用 Y，Y 调用 Z，看看多乱”时，使用 Mermaid `flowchart` 或 `graph`。包在 Tailwind 样式卡片中，避免显得突兀。用 classDef 将泄漏边设为红色，深模块设为深色。时序图很适合表达“改前：6 次往返；改后：1 次”。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

<a id="hand-built-boxes-and-arrows-when-mermaids-layout-fights-you"></a>

### 手工框线与箭头（Mermaid 布局不合意时）

模块用带边框和标签的 `<div>` 表示。箭头用内联 SVG `<line>` 或 `<path>` 元素，在相对定位的容器上绝对定位。如果希望“改后”图像一个粗边框深模块，内部内容灰显，就使用这种方式，因为 Mermaid 无法以恰当的视觉分量呈现。

<a id="cross-section-good-for-layered-shallowness"></a>

### 剖面图（适合分层的浅模块）

堆叠水平带（`h-12 border-l-4`），展示一次调用经过的层。改前：6 个几乎什么也不做的薄层。改后：1 个标注合并后职责的厚带。

<a id="mass-diagram-good-for-interface-as-wide-as-implementation"></a>

### 体量图（适合“接口与实现一样宽”）

每个模块两个矩形：一个表示接口表面积，一个表示实现。改前：接口矩形几乎与实现矩形一样高（浅）。改后：接口矩形矮，实现矩形高（深）。

<a id="call-graph-collapse"></a>

### 调用图折叠

改前：函数调用树用嵌套框表示。改后：相同树折叠进一个框，现已内部化的调用在框内淡化显示。

<a id="style-guidance"></a>

## 样式指南

- 偏向编辑设计，不要像企业仪表盘。留白充足。标题可以用衬线字体（`font-serif` 与 stone/slate 很搭）。
- 克制用色：一种强调色（翡翠绿或靛蓝），加上表示泄漏的红色和表示警告的琥珀色。
- 图示高度保持约 320px，让改前／改后舒适并排，无需滚动。
- 图内模块标签使用 `text-xs uppercase tracking-wider`，让它们像示意图，而不是 UI。
- 唯一的脚本是 Tailwind CDN 和 Mermaid ESM 导入。除此之外报告是静态的：没有应用代码，除 Mermaid 自身渲染外没有交互。

<a id="top-recommendation-section"></a>

## 首要推荐章节

一张更大的卡片。候选项名称、一句话说明理由、指向其卡片的锚点链接。仅此而已。

<a id="tone"></a>

## 语气

使用浅显英语，简洁表达，但架构名词和动词直接取自 `/codebase-design` 技能。简洁不是偏离术语的借口。

**严格使用：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**绝不替换为：** component、service、unit（替代 module）；API、signature（替代 interface）；boundary（替代 seam）；layer、wrapper（本意是 module 时）。

**符合风格的表述：**

- “Order 接入模块很浅：接口几乎与实现一样复杂。”
- “定价逻辑跨 seam 泄漏。”
- “加深：一个接口，一个测试位置。”
- “两个适配器证明 seam 有必要：生产用 HTTP，测试用内存实现。”

**收益列表**用术语表词汇点明收益：*“局部性：bug 集中在一个模块”*、*“杠杆效应：一个接口，N 个调用点”*、*“接口缩小；实现吸收封装层”*。不要写*“更易维护”*或*“代码更干净”*，因为这些词不在术语表中，也没有提供足够价值。

不要含糊，不要铺垫，不要“值得注意的是……”。一句话能写成列表项，就写成列表项。一条列表项能删，就删。如果某术语不在 `/codebase-design` 术语表中，先寻找已有术语，再考虑发明新词。
