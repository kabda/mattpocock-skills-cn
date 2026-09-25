# 翻译术语表

| 英文 | 采用形式 | 使用说明 |
| --- | --- | --- |
| skill | 技能 / skill | 自然语言用技能；slug、调用名不译 |
| agent / subagent | agent / 子 agent | 保留工具名与固定角色标识 |
| deep module | 深模块 | 小接口隐藏大量实现复杂性 |
| shallow module | 浅模块 | 接口相对实现过大、隐藏能力不足 |
| interface | 接口 | 公共契约，不等同于用户界面 |
| seam | seam（可替换边界） | 首次解释，后续保留 seam；避免误写成具体实现 |
| boundary | 边界 | 模块、系统或权限边界，依上下文限定 |
| TDD | TDD | 测试驱动开发；保留 red-green-refactor 等固定词 |
| red / green / refactor | Red / Green / 重构 | 固定输出或触发词保留原始拼写 |
| mock / fixture | mock / fixture | 不改代码标识和示例输出 |
| frontmatter | frontmatter | YAML 元数据块，键与类型不变 |
| ADR | ADR | 架构决策记录；固定模板字段保留 |
| context / CONTEXT.md | 上下文 / CONTEXT.md | 文件名保留 |
| tracer bullet | 曳光弹 | 最小端到端路径，用于尽早取得反馈 |
| vertical slice | 纵向切片 | 跨层的完整行为切片 |
| horizontal slice | 横向切片 | 按技术层拆分 |
| harness | agent 运行环境 / harness | 依上下文，不把不同平台工具混同 |
| user-invoked | 用户调用 | 调用策略字段不变 |
| model-invoked | 模型调用 | 模型或用户均可触发 |
| promoted | 正式收录 | 仅 engineering 与 productivity |
| worktree | worktree | Git 工作树；命令与路径不译 |
| grill / grilling | 追问 / grilling | 触发词原文保留，不新增触发场景 |
| MUST / SHOULD / MAY | 必须 / 应当 / 可以 | RFC 2119 等规范关键字按契约保留 |
| ticket / issue / PR | 工单 / issue / PR | 工具及固定字段保留原文 |
| source of truth | 权威来源 | 不弱化其约束地位 |
| out of scope | 范围之外 | 文件名、模板依赖标题和标签保留 |
| blocker | 阻塞问题 | 区别于建议、待选方案 |
| disposition | 处置结论 | triage 的固定枚举保留 |
| frontier | 前沿 | 前提已确定的问题或阻塞项已完成的工单集合 |
| round | 轮次 | grilling 每轮覆盖当时的整个前沿 |
| ubiquitous language | 通用语言 | 领域建模中的共享精确词汇 |
| prefactoring | 预先重构 | 先让变更更容易，再实施变更 |
| blast radius | 影响范围 | 变更波及的调用点与区域 |
| expand–contract | expand–contract（扩展－收缩） | 大范围重构的固定阶段术语；含中间迁移阶段 |
| primary source / secondary source | 一手来源 / 二手来源 | 研究证据与上下文留存中的来源级别 |
| tight loop | 紧凑循环 | 快速、确定且针对确切症状的反馈循环 |
| red-capable | 能够变 Red | 确实能因目标 bug 失败，不只是运行成功 |
| throwaway | 一次性 | 原型不进 main；按原技能保留到临时用途分支 |
| Standards / Spec | Standards（标准）/ Spec（规格说明） | code-review 固定报告标题原样保留 |
| destination | 目标 | wayfinder 地图的终点，确定范围 |
| fog of war | 战争迷雾 | 范围内但尚不能精确表述为工单的问题 |
| decision ticket | 决策工单 | 产出决策，不等同实现工单 |
| mission | 学习使命 | teach 的现实学习原因与目标 |
| zone of proximal development | 最近发展区 | 挑战恰到好处的学习范围 |
| fluency strength / storage strength | 提取流畅度 / 存储强度 | 当下提取与长期保留的区别 |
| context pointer | 上下文指针 | 同时指明材料与访问条件 |
| context load / cognitive load | 上下文负荷 / 认知负荷 | agent 窗口成本与人的索引负担 |
| leading word | 引导词 | 保留具体英文示例以维护触发概念 |
| progressive disclosure | 渐进披露 | 参考通过指针按需加载 |
| co-location / duplication | 同处放置 / 重复 | 概念相邻组织与多处复述需区分 |
| sediment / sprawl / no-op | 沉积 / 蔓延 / no-op | 陈旧堆积、过长、无行为增益三种失败模式 |
| explore / exploit | 探索 / 利用 | 写作技能两个阶段，保留英文触发概念 |
| beat | 节拍 / 叙事节拍 | 文章旅程的一次推进，不等同固定段数 |
| grounding / grounded | 奠基 / 已奠基 | 读者事先已知或文章已引入概念 |
| triage | 分流 | 指 issue 分类、验证和流转；slug、状态角色和标签保留原文 |
