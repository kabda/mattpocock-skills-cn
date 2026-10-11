# 历史记录：1.2.3 翻译验收

以下保存 2026-09-25 的验收记录，仅描述旧基线。当前结果见 [validation.md](validation.md)。

# 完整中文翻译验收记录

2026-09-25 完成冻结提交 `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` 的完整中文翻译及全部必需的本地验收。验收时交付保留在目标工作区，未提交、推送、发布或安装；其后用户另行授权提交全部变更并推送至 main。原项目来源见 [source.md](source.md)，用户阅读入口见 [中文版本说明](../../wiki/translation.html)。

## 验收结论

| 项目 | 结果与证据 |
| --- | --- |
| 完整范围 | 169 个冻结源路径全部对应；115 个全文翻译、41 个部分字段翻译、13 个原样保留；另有精确白名单中的 17 个管理/用户说明路径，其中 2 个为用户既有文件 |
| 全文校对 | 156 个可翻译文件均有逐文件全文对照记录，绑定源译 SHA-256；38 个 SKILL.md 与 38 个 agents/openai.yaml 齐全 |
| 技能分布 | engineering 18、productivity 7、misc 4、in-progress 9；deprecated 分类说明保留 |
| 文件与保护项 | mode、可执行位、符号链接及原样 bytes 通过；AGENTS.md 仍指向 CLAUDE.md；LICENSE、独立脚本、workflow、lockfile、配置代码原样 |
| 元数据 | 真实 YAML/JSON parser 比较字段路径、类型、不可变值和调用策略；仅登记的 description、argument-hint、short_description 可译；display_name、name、版本、作者、依赖和技能路径不变 |
| 插件与调用 | 正式注册仍为原有 25 项；根 README 索引、调用分组和 25 项配套 docs 集合一致；源译 slash/dollar 调用候选数量一致，当前技能引用按冻结 slug 分类 |
| Markdown / HTML | 标题层级、表格结构、围栏数量和语言、HTML 标签/属性/嵌套无翻译新增差异；58 个围栏原样，32 个仅翻译自然语言 |
| 链接与锚点 | 原链接、图片目标、引用式链接保持；566 个源标题兼容锚点已登记；解析到的仓库内链接无新增断链或无效 fragment；模板内链接和 655 次 URL 字面量通过补查 |
| 英文保留 | 扩大扫描至连续三个以上英文单词，逐项复核 195 个不同上下文中的候选、共 218 次出现；每项含具体保留理由。58 个原样围栏另逐块查看全文并分类，没有把自然语言模板一概跳过 |
| 中文说明页 | wiki/translation.html 为中文 HTML，身份与安装来源说明齐全，HTML 嵌套及本地链接通过，和 README 双向链接有效 |
| 原仓库与用户内容 | 源 main/HEAD/remote 不变，源工作区仍干净；两个用户既有文件 hash 与初始记录一致；目标 main 尚无首次提交，origin 不变 |

详见 [manifest.json](manifest.json)、[review.json](review.json)、[anchors.json](anchors.json)、[english-retained.json](english-retained.json)、[基础报告](report.json) 和 [补充报告](audit-report.json)。各清单的最终目标 hash 与当前工作区一致。

## 可重跑的检查

以下命令从中文仓库根目录运行。检查仅访问本地冻结 Git 对象与工作区，不运行技能描述的工作流。

```sh
rtk proxy uv run --offline --isolated --no-project --with pyyaml --with markdown-it-py --with beautifulsoup4 python docs/localization/validate.py
rtk proxy uv run --offline --isolated --no-project --with pyyaml --with markdown-it-py --with beautifulsoup4 python docs/localization/audit.py
rtk proxy node scripts/sync-plugin-version.mjs --check
```

| 命令 / 检查 | 最终退出状态 | 实际结果 |
| --- | --- | --- |
| validate.py（不带 --partial） | 0 | 全量 169 路径，156 校对文件，38 技能，13 原样路径；errors 为空；解析链接未发现上游断链候选或翻译新增断链 |
| audit.py | 0 | 195 项英文记录与当前上下文、出现次数精确匹配；58 原样围栏 hash 匹配；32 个译文围栏、655 次 URL、调用引用和正式技能 docs 集合通过 |
| sync-plugin-version.mjs --check | 0 | package.json 与 plugin.json 版本均为 1.2.3，没有写入版本 |
| 源 git status --porcelain=v1 | 0，输出空 | 仍为干净工作区 |
| 源 git rev-parse --verify HEAD | 0 | 仍为 c55ee46073ed923f86ce59a5eb3b6d895095d1b7 |
| 源冻结 tree 读取与比较 | 0 | 0345ebb740dc47c09176a3b41a49cc11f4900073，169 路径 |
| 两仓库 symbolic-ref / remote get-url | 0 | 均为 main；分别是 mattpocock/skills 与 kabda/mattpocock-skills-cn 的原 origin |
| 目标 git rev-parse --verify HEAD | 128（预期） | 目标尚无首次提交，符合初始状态；不为验收创建提交 |
| Claude CLI 发现 | 检查进程退出 0，shutil.which 返回 None | 本机无 Claude CLI，平台验证未运行 |

实际解析环境为 Python 3.13.13、PyYAML 6.0.3、markdown-it-py 4.2.0、BeautifulSoup 4.15.0，通过 uv 隔离缓存运行，未修改项目依赖或 lockfile。`--no-project` 的提示只说明源项目不是 Python 项目，不影响隔离运行。

`audit.py` 不会自动批准新英文候选；新增或变更上下文、次数、代码块 hash 都会与人工清单不匹配并失败。基础扫描没有纯英文长段不等于完整翻译正确，最终语义依据是此前逐文件全文校对及本轮逐项补查。

## 终检修正与允许变化

- 将 11 个文件中的 triage 自然语言译名“分诊”统一为“分流”，并更新术语表和对应标题映射。技能 slug、标签及固定字段未变。
- 翻译 setup-ts-deep-modules 中反引号包裹的一句普通文档指针，保留 src/packages/README.md 路径及链接；唯一精确例外登记于 manifest.inline_code_translations。
- 根 README 仅新增获授权的中文版本声明；banner 的 alt 展示文字由 Skills 译为“技能”，精确登记于 manifest。所有徽章、安装命令、图片地址和上游 URL 未改。
- 中文标题兼容的 566 个显式锚点只增加原 fragment，不重写外部 URL 或既有引用目标。
- 变更过的 Markdown 模板还比较其内部内联代码；固定模板标题、字段、触发词、示例输出与协议保持原文，其余自然说明已翻译。

## 上游原有差异

以下均来自冻结快照；译文保留原意，未顺手修复上游行为或宣称核验其远程现状。

1. **tdd**：description 和 agent 简介保留 red-green-refactor，正文将重构移至 code-review；配套文档也说明了差异。
2. **codebase-design**：配套文档引用的 Agent 工具措辞与本基线 DESIGN-IT-TWICE.md 不同；文档称 setup-ts-deep-modules 未带 lint 规则，但冻结树已有 dependency-cruiser 配置。
3. **diagnosing-bugs**：正文已有 Redact 段，配套文档仍称脱敏未实现；文档称 HITL 模板可执行，Git mode 实为 100644。
4. **implement / code-review**：前者在提交前调用审查，后者使用三点 diff，无法覆盖未提交的工作区和暂存改动；原配套文档已有讨论。
5. **prototype**：正文要求在原型化模块或页面附近放代码，配套文档建议独立目录或会话，原文两种说法均保留。
6. **wizard**：配套文档及部分历史说明称模板显示剩余时间，实际模板显示阶段计数。
7. **improve-codebase-architecture**：docs 提及 Agent/subagent_type=Explore，正文只要求启动子 agent；“唯一新文件为 HTML”与允许写 CONTEXT.md / ADR 的说法并存。
8. **setup / triage-labels**：模板要求改“右侧列”，但表格最右列是含义列。GitHub 外部 PR 示例请求的 authorAssociation 字段问题也由冻结配套文档指出；命令原样保留，未现场执行。
9. **ask-matt**：正文称两条入口支路却列出三条；docs 保留旧的 22 个技能、13 个禁用模型调用统计。实际清单和校验使用冻结树的 25 个正式注册项；历史 ADR 中的 22/24 等数字不改。
10. **triage**：OUT-OF-SCOPE.md 的外层 Markdown 和内层 TypeScript 围栏同为三个反引号，CommonMark 提前结束模板，末尾围栏又吞入后续内容。保留原布局并额外记录解析后的围栏；AGENT-BRIEF 的 enhancement 字段示例与 OUT-OF-SCOPE 的散文格式也不同。
11. **setup-ts-deep-modules**：正文称四条 forbidden 规则，配置实际五条（含 tests-folder-is-private）；步骤 4 允许没有统一脚本时只提醒 CI，完成条件却要求与 typecheck 同命令运行。
12. **teach**：附有 GLOSSARY-FORMAT.md，但 SKILL 未链接它；正文的 ./ 同时用于技能参考目录和使用者项目目录，原 docs 已说明。
13. **CONTEXT / in-progress**：CONTEXT 留有旧 ready-for-afk，并称一个 Issue 同时只有一个 Triage role，与新 triage 的一个类别加一个状态不同。in-progress README 将 retro 标为 STUB，pr 索引说一手来源及刻意排除项，而实际模板未明确要求。它们是上游原文状态，不是本次未完成译文。

## 检查边界与未运行项

- Claude CLI 不存在，`rtk proxy claude plugin validate . --strict` **未运行**；按本任务约定不阻塞必需的本地验收。没有进行平台安装或真实技能调用，不声称其通过。
- 没有访问外部链接、运行 CDN / Mermaid 脚本、渲染所有 Markdown 或校验远程平台实时行为。HTML 检查覆盖标签、属性、嵌套和本地链接，未作浏览器视觉验收。
- Markdown 使用 CommonMark + table；GitHub 自动 slug 采用本地兼容算法，并为 566 个已翻译标题保留显式 fragment。无法保证所有第三方 Markdown 渲染器支持 HTML 锚点。
- 相对文件链接由 parser 识别；使用者项目路径、glob、占位符、示例命令中的文件路径按语义保留，不要求在翻译仓库中真实存在。调用扫描排除 HTML 关闭标签、路径连接及人工确认的 include-list/build-tool 普通名词连接。
- 英文扫描是找漏辅助，不覆盖每一种自然语言句式；短技术词、固定字段、作者身份、英文触发词由全文校对覆盖。可执行代码、正则、程序字符串、伪代码及其保留注释不执行，也不据此承诺运行正确性。
- 自动通过只支持其覆盖的结构和契约。译义质量来自逐文件全文对照；上游设计缺陷或互相矛盾的行为不因翻译而被修复。

本地强制验收无未完成项。翻译验收阶段没有 commit、merge、push、发布、安装技能或修改用户配置。其后用户明确授权 Git 交付：提交全部变更至主干并推送远端，再清理已合并开发分支及 worktree。Git 交付前复核发现，本地为尚无首次提交的 main，远端为空，且只有主工作区、无开发分支，因此直接在 main 创建首次提交，无需额外合并或 worktree 清理。实际提交及推送状态以 Git 历史和 origin/main 为准。
