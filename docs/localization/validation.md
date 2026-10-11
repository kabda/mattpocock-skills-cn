# 当前中文翻译验收记录

2026-10-11 完成上游快照 `49dd158d1076134a641b33efb035946536778336` 的增量翻译与全量本地验收。版本字段为 1.3.1，快照还包含 16 个待发布 changeset。旧基线记录保存在 [validation-1.2.3.md](validation-1.2.3.md)，来源见 [source.md](source.md)，完整路径对比见 [upstream-1.3.1.md](upstream-1.3.1.md)。

## 验收结论

| 项目 | 当前结果 |
| --- | --- |
| 范围 | 190 个冻结路径全部对应：131 全文翻译、44 部分展示字段翻译、15 原样保留 |
| 校对记录 | 175 个可翻译路径绑定源译 SHA-256；新增内容逐段翻译，增量逐行核对，未变化内容继承旧校对记录 |
| 技能与元数据 | 38 个 SKILL.md、38 个 agents/openai.yaml；engineering 20、productivity 7、misc 4、in-progress 7 |
| 发布集合 | 27 个正式技能，根索引、正式分类索引与插件清单一致；配套 docs 27 页，另有 1 页归档文档 |
| 分类索引 | 各分类覆盖全部技能；chief-of-staff 的 beta 索引补充为精确登记的本地例外 |
| 文件保护 | 可执行位、AGENTS.md 符号链接及 15 个原样路径 bytes 与源文相同；两个用户既有文件 hash 不变 |
| 元数据保护 | YAML/JSON 的字段、类型、不可变值及调用策略一致；issue 表单只开放登记的展示字段，工作流原字节保留 |
| Markdown / HTML | 标题层级、表格结构、围栏数量与语言、HTML 标签/属性/嵌套通过；60 个围栏原样，38 个仅翻译自然语言部分 |
| 链接与字面量 | 原链接和图片目标一致；617 个英文 fragment 兼容锚点登记；仓库内链接无新增断链；767 次 URL 字面量及调用候选数量一致 |
| 英文保留 | 203 项不同上下文、227 次出现有逐项保留理由；未分类新增候选会使 audit.py 失败 |
| 版本 | package.json 与 plugin.json 均为 1.3.1；上游版本同步脚本检查退出 0 |
| Shell 语法 | 5 个 shell 文件通过 bash -n；未执行脚本业务逻辑 |
| Git 交付 | 翻译在 codex/同步上游1.3.1中文翻译 分支验收；用户随后授权提交、合并 main 并推送 origin，准确状态以 Git 历史和 origin/main 为准；未安装技能 |

机器证据见 [manifest.json](manifest.json)、[review.json](review.json)、[anchors.json](anchors.json)、[english-retained.json](english-retained.json)、[基础报告](report.json) 和 [补充报告](audit-report.json)。自动检查覆盖结构和契约，不证明译义或平台运行结果。

## 实际检查命令

从中文仓库根目录运行，依赖通过 uv 离线隔离环境读取缓存；未修改项目依赖或 lockfile。

```sh
rtk proxy uv run --offline --isolated --no-project --with pyyaml --with markdown-it-py --with beautifulsoup4 python docs/localization/validate.py
rtk proxy uv run --offline --isolated --no-project --with pyyaml --with markdown-it-py --with beautifulsoup4 python docs/localization/audit.py
rtk proxy node scripts/sync-plugin-version.mjs --check
```

| 检查 | 实际结果 |
| --- | --- |
| validate.py 全量检查 | 退出 0，errors 为空；190 路径、175 校对记录、38 技能、15 原样路径 |
| audit.py | 退出 0，errors 为空；英文上下文/出现次数、围栏 hash、URL 和调用引用、正式及归档 docs 集合匹配 |
| sync-plugin-version.mjs --check | 退出 0，1.3.1 已同步 |
| bash -n | scripts/list-skills.sh、scripts/link-skills.sh、Git guardrails 脚本、HITL 模板、wizard 模板全部退出 0 |
| em dash 扫描 | 没有匹配；rg 的无匹配退出状态为 1 |
| rtk proxy claude plugin validate . --strict | RTK 退出 1，提示找不到 claude 可执行文件；未进入 Claude 平台验证 |
| shellcheck 发现 | 未安装，未运行 |

## 上游仍存的文档差异

以下根据本地冻结源文与实际文件对比记录，不推断远程 issue 的当前状态。译文保留原意，不把文档中的旧陈述改成未经上游授权的修正。

1. **ask-matt**：技能正文已要求描述前先读 SKILL.md，配套 docs 的旧问答仍称没有这项约束；正文“两个入口支路”实际列出三条。Beta 技能未纳入正式路由图。
2. **GLOSSARY.md**：根文档改名后仍保留 ready-for-afk 示例和一个 issue 一个 Triage role 的旧模型，而当前 triage 是一个类别角色加一个状态角色。
3. **domain-modeling / codebase-design**：部分配套 docs 仍将 GLOSSARY.md 与教学术语表的文件名视为冲突；codebase-design docs 仍称 setup-ts-deep-modules 无 lint 规则，而附带配置已存在。
4. **setup / triage**：SKILL 已要求创建缺失标签，部分 docs 仍将标签未创建描述为未修复；GitHub 外部 PR 命令已去掉旧 authorAssociation 查询字段，但 docs 的旧问答仍讨论此错误。
5. **diagnosing-bugs**：SKILL 已含脱敏要求，docs 仍说未实现；docs 称 HITL 模板可执行，Git mode 为 100644。
6. **teach**：正文已区分工作空间路径与技能目录，并要求改变正确答案位置，docs 中部分旧问答仍称未修复答案顺序问题；GLOSSARY-FORMAT.md 仍未由 SKILL 链接。
7. **wizard**：历史说明及部分 docs 称显示时间估算，当前模板只显示阶段计数；本次新模板修复不改变这项事实。
8. **implement / code-review**：implement 在提交前调用审查，而 code-review 的固定 HEAD 三点 diff 无法覆盖未提交工作区；配套 docs 保留这一限制。
9. **prototype / improve-codebase-architecture**：代码放置方式的 docs 与正文表述不同；架构报告“唯一新文件为 HTML”与允许写 GLOSSARY.md / ADR 的说法仍并存。
10. **triage 模板**：OUT-OF-SCOPE.md 的外层与内层围栏同为三个反引号，CommonMark 会提前结束外层模板；布局按源文保留，并比较解析后的围栏。
11. **setup-ts-deep-modules**：正文称四条 forbidden 规则，配置实际五条；步骤允许无统一脚本时仅提示 CI，完成条件却要求同命令运行。
12. **tdd**：description 仍提 red-green-refactor，正文将重构交给 code-review；译文保留这项上游差异。

## 边界

- 未访问外部 URL，安装与工具可用性描述按冻结源文翻译。未进行 Claude、Codex、Copilot 或 Gemini 的真实安装，也未运行技能示例、issue 工作流或发布流程。
- 未运行 link-skills.sh，用户的真实技能目录保持不变；这里的文件迁移不等同于重新安装。
- Shell 检查只证明语法解析成功，不证明 env 写入、后台交接、EOF 或平台命令实际工作。
- Markdown 使用 CommonMark + table，并补原英文 fragment 显式锚点。HTML 检查覆盖嵌套及本地链接，不运行 CDN 或所有模板页面。
- 英文扫描按连续三个以上英文单词寻找候选；短词、技术标识与译义由人工差分校对覆盖。新原样围栏逐块检查，并保留具体理由。
- 本次唯一额外正文补充是 beta 分类 chief-of-staff 索引，见 manifest.localized_additions；其余路径、调用分组和保护项以冻结快照为准。
