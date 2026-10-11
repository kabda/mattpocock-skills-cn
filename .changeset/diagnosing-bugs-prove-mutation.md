---
"mattpocock-skills": patch
---

`diagnosing-bugs` 的阶段 5 现在要求 agent 在相信 Red 结果前，用 `diff` 对照原始副本确认强制变异确实生效，避免没有实际修改任何内容的编辑被误当作失败测试（#955）。
