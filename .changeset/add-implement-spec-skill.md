---
"mattpocock-skills": patch
---

添加 `implement-spec` 技能（in-progress 分类，用户调用）。它接收规格说明及其工单，推动完成一个 PR：把工单读作带阻塞关系的任务图，实现子 agent 在就绪前沿上使用后台 worktree 并发工作，合并子 agent 将每份结果并回 PR 分支，流程最后运行 `/code-review`，再把 PR 标记为可审查。
