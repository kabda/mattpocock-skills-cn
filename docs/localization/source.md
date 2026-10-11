# 翻译基线与来源

2026-10-11 将中文仓库从旧基线同步到用户已更新的本地上游快照。所有对比读取 Git 对象，不读取插件缓存作为源文。

| 项目 | 旧基线 | 当前基线 |
| --- | --- | --- |
| 上游提交 | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | `49dd158d1076134a641b33efb035946536778336` |
| package / 插件版本 | 1.2.3 | 1.3.1 |
| 上游路径 | 169 | 190 |
| 全文翻译文件 | 115 | 131 |
| 部分展示字段翻译文件 | 41 | 44 |
| 原样保留路径 | 13 | 15 |
| SKILL.md / agents/openai.yaml | 38 / 38 | 38 / 38 |
| engineering / productivity / misc / in-progress | 18 / 7 / 4 / 9 | 20 / 7 / 4 / 7 |
| 正式插件注册 | 25 | 27 |

- 原项目：`mattpocock/skills`，作者 Matt Pocock，origin 为 `git@github.com:mattpocock/skills.git`。
- 原仓库：`/Users/zxj/Developer/open-source/skills`，开始同步时 main / HEAD 等于当前冻结提交，工作区干净。
- 当前 Git tree：`3ce485319972aae46dec0c2ac34cf4a7f28f7414`。上游版本字段是 1.3.1，但快照还包含 16 个待发布 changeset；本次也同步这些增量，不将它们误记为全部已发布。
- 中文项目：`kabda/mattpocock-skills-cn`，非官方简体中文翻译，origin 为 `git@github.com:kabda/mattpocock-skills-cn.git`。
- 中文仓库：`/Users/zxj/Developer/open-source/mattpocock-skills-cn`。初始 main 干净，已有提交 `b3b27a74c1bf69e7e18e7440c805a85e53555845`。
- 翻译工作分支：`codex/同步上游1.3.1中文翻译`；本地翻译验收后，用户已授权提交、合并至 `main` 并推送 `origin`。Git 交付状态以提交历史与 `origin/main` 为准；未安装技能。
- 原有 `docs/codex-goals/完整中文翻译-Goal.md` 与 `wiki/translation-goal.html` 原样保留，SHA-256 见 manifest。
- 继承上游 Markdown 保留原路径；本次新增用户说明使用 `wiki/` 下的 HTML，研发记录放本目录。

## 翻译与例外

131 个文件全文翻译，44 个文件只翻译已登记展示字段，15 个路径原样保留。命令、技术标识、URL、作者身份、策略布尔值、版本和程序行为以冻结源文为准。新 issue 表单只翻译名称、说明和展示标签，id、类型、校验规则和机器标签不变；Actions 工作流的运行字符串及评论按原字节保留。

新增 beta 技能 `chief-of-staff` 在上游分类 README 中漏列。本仓库按 AGENTS.md 补一行中文索引，精确增补内容登记于 manifest.localized_additions。正式插件及顶层 README 不包含它。上游移除 `resolving-merge-conflicts`，其 docs 页面按新上游规则继续保留为归档页，登记于 manifest.archived_docs。

本地比较清单见 [upstream-1.3.1.md](upstream-1.3.1.md)，当前验收见 [validation.md](validation.md)，旧时点记录见 [validation-1.2.3.md](validation-1.2.3.md)。
