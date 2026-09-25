# 翻译基线与来源

- 原项目：`mattpocock/skills`，作者 Matt Pocock。
- 中文项目：`kabda/mattpocock-skills-cn`，非官方简体中文翻译。
- 冻结提交：`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`。
- Git tree：`0345ebb740dc47c09176a3b41a49cc11f4900073`。
- 源路径：`/Users/zxj/Developer/open-source/skills`；初始 HEAD 等于冻结提交，工作区干净，origin 为 `git@github.com:mattpocock/skills.git`。
- 目标路径：`/Users/zxj/Developer/open-source/mattpocock-skills-cn`；初始 main 尚无提交，origin 为 `git@github.com:kabda/mattpocock-skills-cn.git`。
- 169 个源路径，38 个 SKILL.md，38 个 agents/openai.yaml；engineering 18、productivity 7、misc 4、in-progress 9。插件注册 25 个正式技能。
- 从 Git tree 读取 mode 和 blob，逐路径复制，不读取源工作区作为翻译基线。
- 已有 `docs/codex-goals/完整中文翻译-Goal.md` 与 `wiki/translation-goal.html` 原样保留；初始 SHA-256 见 manifest。已有提示词与本次任务对应，不再添加副本。
- 继承的 Markdown 保留路径；新增用户说明使用 wiki 下的中文 HTML。新增研发资料及工具位于本目录，逐路径白名单见 manifest。
- 翻译验收阶段未提交、推送、发布或安装技能，也未执行技能正文描述的操作。验收完成后，用户另行授权提交并推送至 main；原安装来源仍指向英文上游。

## 处理分类

最终分类：115 个全文翻译、41 个部分字段翻译、13 个原样保留。展示字段已逐项核实，机器清单记录可变字段、最终状态、原译 hash 与保护理由。2026-09-25 完成全文校对及本地验收；自动检查不替代译义校对。
